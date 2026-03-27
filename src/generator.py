import asyncio
import re
from typing import List, Tuple
import tenacity
from litellm import acompletion
from .config import settings
from .models import RoleMeta, PackageMeta, ToolComponent
from .prompts import PROMPTS
from .validator import OutputValidator
from .exceptions import (
    LLMConfigError,
    LLMTimeoutError,
    LLMRateLimitError,
    GenerationFailedError,
)


class ToolGenerator:
    """Generate tool components using LLM"""

    def __init__(self):
        self.provider = settings.llm_provider
        self.model = settings.llm_model
        self.api_key = settings.llm_api_key
        self.timeout = settings.llm_timeout
        self.max_retries = settings.llm_max_retries
        self.concurrency = settings.llm_concurrency
        self.validator = OutputValidator()

        if not self.api_key:
            raise LLMConfigError(
                "LLM API Key not configured. Set OH_ROLES_LLM_API_KEY environment variable."
            )

    async def generate_package(
        self,
        role: RoleMeta,
        components: List[str] | None = None,
    ) -> Tuple[PackageMeta, List[ToolComponent]]:
        """Generate complete tool package for a role"""
        components = components or settings.default_components

        # Read source content
        source_content = self._read_source(role.source_path)

        # Generate components concurrently with semaphore limit
        semaphore = asyncio.Semaphore(self.concurrency)

        async def generate_one(comp_type: str) -> ToolComponent | None:
            async with semaphore:
                return await self._generate_component(comp_type, source_content, role)

        tasks = [generate_one(comp_type) for comp_type in components]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Collect successful results
        generated_components: List[ToolComponent] = []
        failed_components: List[str] = []

        for comp_type, result in zip(components, results):
            if isinstance(result, Exception):
                failed_components.append(comp_type)
                continue
            if result is not None:
                # _generate_component can return multiple components
                if isinstance(result, list):
                    generated_components.extend(result)
                else:
                    generated_components.append(result)

        if not generated_components and failed_components:
            raise GenerationFailedError(
                f"All components failed generation: {', '.join(failed_components)}"
            )

        from datetime import datetime

        package_meta = PackageMeta(
            role=role,
            version=role.version,
            generated_at=datetime.now(),
            llm_provider=self.provider,
            llm_model=self.model,
            components=[c.type for c in generated_components],
        )

        return package_meta, generated_components

    async def _generate_component(
        self,
        component_type: str,
        source_content: str,
        role: RoleMeta,
    ) -> List[ToolComponent] | ToolComponent | None:
        """Generate single component with validation"""
        prompt = self._build_prompt(component_type, source_content, role)

        try:
            content = await self._call_llm(prompt)
        except (LLMTimeoutError, LLMRateLimitError, GenerationFailedError):
            return None

        components = self._parse_response(component_type, content, role)

        for comp in components:
            try:
                comp.schema_valid = self.validator.validate(comp)
            except Exception:
                comp.schema_valid = False

        # Return all parsed components
        return components

    def _build_prompt(
        self,
        component_type: str,
        source_content: str,
        role: RoleMeta,
    ) -> str:
        """Build prompt from template"""
        template = PROMPTS[component_type]
        return template.format(
            role_name=role.display_name,
            role_description=role.description,
            source_content=source_content,
        )

    @tenacity.retry(
        stop=tenacity.stop_after_attempt(3),
        wait=tenacity.wait_exponential(multiplier=1, min=2, max=10),
        retry=tenacity.retry_if_exception_type((LLMTimeoutError, LLMRateLimitError)),
        before_sleep=lambda retry_state: None,
    )
    async def _call_llm(self, prompt: str) -> str:
        """Call LLM API with retries"""
        try:
            response = await acompletion(
                model=f"{self.provider}/{self.model}",
                messages=[{"role": "user", "content": prompt}],
                api_key=self.api_key,
                base_url=settings.llm_base_url,
                timeout=self.timeout,
            )
            return response.choices[0].message.content.strip()
        except TimeoutError:
            raise LLMTimeoutError("LLM call timed out")
        except Exception as e:
            if "rate limit" in str(e).lower():
                raise LLMRateLimitError(f"LLM rate limit: {e}")
            raise GenerationFailedError(f"LLM call failed: {e}")

    def _read_source(self, source_path: str) -> str:
        """Read source document content"""
        with open(source_path, "r", encoding="utf-8") as f:
            return f.read()

    def _parse_response(
        self,
        component_type: str,
        content: str,
        role: RoleMeta,
    ) -> List[ToolComponent]:
        """Parse LLM response into ToolComponents"""
        components: List[ToolComponent] = []

        # For claude_md: whole content is one file
        if component_type == "claude_md":
            components.append(ToolComponent(
                type=component_type,
                content=content,
                filename="CLAUDE.md",
                target_path="CLAUDE.md",
            ))
            return components

        # For other types: LLM outputs multiple files with ## filename headers
        # Split by "## 文件名: " pattern
        pattern = r"##\s+文件名:\s+(.+?)\n"
        parts = re.split(pattern, content)

        if len(parts) == 1:
            # Single file, guess filename
            ext = self._get_extension(component_type)
            filename = f"{role.name}.{ext}"
            target_path = self._get_target_path(component_type, filename)
            components.append(ToolComponent(
                type=component_type,
                content=parts[0],
                filename=filename,
                target_path=target_path,
            ))
        else:
            # Skip first empty part, then pairs of (filename, content)
            if parts[0].strip() == "":
                parts = parts[1:]
            for i in range(0, len(parts), 2):
                if i + 1 >= len(parts):
                    break
                filename = parts[i].strip()
                file_content = parts[i + 1].strip()
                # Remove wrapping code block if present
                if file_content.startswith("```"):
                    file_content = file_content[file_content.find("\n")+1:].rstrip()
                    if file_content.endswith("```"):
                        file_content = file_content[:-3].rstrip()
                target_path = self._get_target_path(component_type, filename)
                components.append(ToolComponent(
                    type=component_type,
                    content=file_content,
                    filename=filename,
                    target_path=target_path,
                ))

        return components

    def _get_extension(self, component_type: str) -> str:
        """Get file extension for component type"""
        ext_map = {
            "claude_md": "md",
            "hooks": "json",
            "commands": "md",
            "agents": "json",
            "rules": "yaml",
            "skills": "md",
        }
        return ext_map.get(component_type, "md")

    def _get_target_path(self, component_type: str, filename: str) -> str:
        """Get target installation path"""
        path_map = {
            "claude_md": "CLAUDE.md",
            "hooks": f"hooks/{filename}",
            "commands": f"commands/{filename}",
            "agents": f"agents/{filename}",
            "rules": f"rules/{filename}",
            "skills": f"skills/{filename}",
        }
        return path_map.get(component_type, filename)
