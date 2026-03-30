from typing import List, TYPE_CHECKING
import importlib.resources
import re
import tenacity
from loguru import logger
from langchain_core.messages import HumanMessage
from src.models import RoleMeta, PackageMeta, ToolComponent
from src.validator import OutputValidator
from src.config import settings
from src.exceptions import GenerationFailedError, LLMTimeoutError, LLMRateLimitError

if TYPE_CHECKING:
    from .workflow import GenerationWorkflowState


def load_prompt(filename: str) -> str:
    """Load prompt template from file."""
    with importlib.resources.files(
        "src.services.llm.generation.prompts"
    ).joinpath(filename).open(encoding="utf-8") as f:
        return f.read()


async def read_source_node(state: "GenerationWorkflowState") -> dict:
    """Read source document content."""
    role = state["role"]
    logger.debug(f"Reading source: {role.source_path}")
    with open(role.source_path, "r", encoding="utf-8") as f:
        content = f.read()
    logger.debug(f"Source loaded: {len(content)} characters")
    return {"source_content": content}


async def parallel_generation_node(state: "GenerationWorkflowState") -> dict:
    """Generate all requested components: generate all non-claude_md first, then generate claude_md last.

    This ensures CLAUDE.md can index all other generated files.
    """
    import asyncio

    role = state["role"]
    source_content = state["source_content"]
    requested = state["requested_components"]
    llm = state["_llm"]
    concurrency = state["_concurrency"]

    # Split components: generate all non-claude_md first
    other_components = [c for c in requested if c != "claude_md"]
    has_claude_md = "claude_md" in requested

    logger.info(f"Workflow starting generation: {len(requested)} total components, "
                f"{len(other_components)} first, CLAUDE.md generated last for {role.category}/{role.name}")
    semaphore = asyncio.Semaphore(concurrency)

    @tenacity.retry(
        stop=tenacity.stop_after_attempt(3),
        wait=tenacity.wait_exponential(multiplier=1, min=2, max=10),
        retry=tenacity.retry_if_exception_type((LLMTimeoutError, LLMRateLimitError)),
        before_sleep=lambda retry_state: logger.warning(f"Retrying LLM call (attempt {retry_state.attempt_number + 1})"),
    )
    async def call_llm_with_retry(prompt: str) -> str:
        """Call LLM API with retries (same as legacy _call_llm)"""
        logger.debug(f"Calling LLM with {len(prompt)} character prompt")
        try:
            response = await llm.ainvoke([HumanMessage(content=prompt)])
            content = response.content.strip()
            logger.debug(f"LLM response received: {len(content)} characters")
            return content
        except TimeoutError:
            logger.error("LLM call timed out")
            raise LLMTimeoutError("LLM call timed out")
        except Exception as e:
            if "rate limit" in str(e).lower():
                logger.error(f"LLM rate limit exceeded: {str(e)}")
                raise LLMRateLimitError(f"LLM rate limit: {e}")
            logger.error(f"LLM call failed: {str(e)}")
            raise GenerationFailedError(f"LLM call failed: {e}")

    async def generate_one(
        comp_type: str,
        all_components: list[str],
        generated_components: list[ToolComponent] | None = None,
    ) -> ToolComponent | None:
        async with semaphore:
            logger.info(f"Generating component: {comp_type}")
            prompt = build_prompt(comp_type, source_content, role, all_components, generated_components)
            logger.debug(prompt)
            logger.debug(f"Prompt built: {len(prompt)} characters")
            try:
                content = await call_llm_with_retry(prompt)
            except (LLMTimeoutError, LLMRateLimitError, GenerationFailedError) as e:
                logger.warning(f"LLM generation failed for {comp_type}: {str(e)}")
                return None
            parsed = parse_response(comp_type, content, role)
            logger.success(f"Component {comp_type} parsed: {len(parsed)} file(s)")
            return parsed

    # First generate all other components in parallel
    generated: List[ToolComponent] = []
    failed: List[str] = []

    if other_components:
        tasks = [generate_one(comp, requested, None) for comp in other_components]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        for comp_type, result in zip(other_components, results):
            if isinstance(result, Exception):
                logger.error(f"Component generation failed: {comp_type}, error: {str(result)}")
                failed.append(comp_type)
                continue
            if result:
                if isinstance(result, list):
                    generated.extend(result)
                else:
                    generated.append(result)

    # Generate CLAUDE.md last - now it gets the list of all other generated files
    if has_claude_md:
        logger.info("Generating CLAUDE.md last, with complete list of other component files")
        result = await generate_one("claude_md", requested, generated)
        if isinstance(result, Exception):
            failed.append("claude_md")
            logger.error(
                "CLAUDE.md generation failed: "
                f"error: {str(result)}"
            )
        elif result is not None:
            if isinstance(result, list):
                generated.extend(result)
            else:
                generated.append(result)

    logger.info(f"Generation complete: {len(generated)} files generated, {len(failed)} failed")
    return {
        "generated_components": generated,
        "failed_components": failed,
    }


async def validate_components_node(state: "GenerationWorkflowState") -> dict:
    """Validate all generated components against schema."""
    validator = state["_validator"]
    generated = state["generated_components"]
    failed = state["failed_components"]

    logger.info(f"Validating {len(generated)} generated components")
    valid_components: List[ToolComponent] = []
    for comp in generated:
        try:
            comp.schema_valid = validator.validate(comp)
            if comp.schema_valid:
                valid_components.append(comp)
            else:
                logger.warning(f"Validation failed, skipping: {comp.filename}")
                if comp.type not in failed:
                    failed.append(comp.type)
        except Exception:
            comp.schema_valid = False
            logger.warning(f"Validation exception, skipping: {comp.filename}")
            if comp.type not in failed:
                failed.append(comp.type)

    logger.info(f"Validation complete: {len(valid_components)} valid, {len(failed)} failed")
    return {
        "validated_components": valid_components,
        "failed_components": failed,
    }


async def build_package_node(state: "GenerationWorkflowState") -> dict:
    """Build final package metadata."""
    from datetime import datetime

    role = state["role"]
    components = state["validated_components"]

    logger.info(f"Building final package: {len(components)} valid components")

    if not components and state["failed_components"]:
        logger.error(f"All components failed generation: {state['failed_components']}")
        raise GenerationFailedError(
            f"All components failed generation: {', '.join(state['failed_components'])}"
        )

    # Get unique component types (remove duplicates)
    unique_components = list({c.type for c in components})
    package_meta = PackageMeta(
        role=role,
        version=role.version,
        generated_at=datetime.now(),
        llm_provider=settings.llm_provider,
        llm_model=settings.llm_model,
        components=unique_components,
    )

    logger.success(f"Package generation complete: {role.category}/{role.name}")
    return {"package_meta": package_meta}


def build_prompt(
    component_type: str,
    source_content: str,
    role: RoleMeta,
    all_components: list[str],
    generated_components: list[ToolComponent] | None = None,
) -> str:
    """Build prompt from template."""
    template = load_prompt(f"{component_type}.md")
    template_vars = {
        "role_name": role.display_name,
        "role_description": role.description,
        "source_content": source_content,
    }
    # Add component list for claude_md - ensures CLAUDE.md indexes all components
    if component_type == "claude_md":
        component_descriptions = {
            "claude_md": "CLAUDE.md - 项目核心指令文件",
            "hooks": "Hooks - 钩子脚本，自动执行任务",
            "commands": "Commands - 自定义斜杠命令",
            "agents": "Agents - 子代理配置",
            "rules": "Rules - 规则文件",
            "skills": "Skills - 技能文件",
        }
        # If we have already generated other components, include their actual filenames
        if generated_components is not None and len(generated_components) > 0:
            lines = []
            for comp in generated_components:
                desc = component_descriptions.get(comp.type, comp.type)
                lines.append(f"- `.claude/{comp.target_path}` - {desc}")
            template_vars["component_list"] = "\n".join(lines)
        else:
            # Fallback: list component types, exclude claude_md itself
            lines = [
                f"- {comp}: {component_descriptions.get(comp, comp)}"
                for comp in all_components if comp != "claude_md"
            ]
            template_vars["component_list"] = "\n".join(lines)
    return template.format(**template_vars)


def parse_response(component_type: str, content: str, role: RoleMeta) -> List[ToolComponent]:
    """Parse LLM response into ToolComponents. Reuses logic from ToolGenerator."""
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
    pattern = r"##\s+文件名:\s*"
    parts = re.split(pattern, content)

    if len(parts) == 1:
        # No filename headers, single file with default name
        ext = _get_extension(component_type)
        filename = f"{role.name}.{ext}"
        target_path = _get_target_path(component_type, filename)
        components.append(ToolComponent(
            type=component_type,
            content=content.strip(),
            filename=filename,
            target_path=target_path,
        ))
        return components
    else:
        # Skip first empty part, then process the rest
        if parts[0].strip() == "":
            parts = parts[1:]

        for part in parts:
            # Split into filename and content at first newline
            if '\n' in part:
                raw_filename, file_content = part.split('\n', 1)
            else:
                raw_filename = part
                file_content = ""

            raw_filename = raw_filename.strip()
            file_content = file_content.strip()

            # Clean filename
            filename = raw_filename.split('\n')[0]
            filename = re.sub(r'[<>:"/\\|?*]', '', filename)
            filename = filename.replace(' ', '-')

            # If filename is empty after cleaning, use default
            if not filename:
                ext = _get_extension(component_type)
                filename = f"{role.name}.{ext}"
            # If filename is still too long (contains content), use default
            if len(filename) > 50:
                ext = _get_extension(component_type)
                filename = f"{role.name}.{ext}"

            # Remove wrapping code block if present
            if file_content.startswith("```"):
                first_newline = file_content.find("\n")
                if first_newline != -1:
                    file_content = file_content[first_newline+1:].rstrip()
                else:
                    file_content = file_content[3:].rstrip()
            file_content = file_content.rstrip()
            if file_content.endswith("```"):
                last_backtick = file_content.rfind("```")
                if last_backtick > 0:
                    file_content = file_content[:last_backtick].rstrip()

            target_path = _get_target_path(component_type, filename)
            components.append(ToolComponent(
                type=component_type,
                content=file_content,
                filename=filename,
                target_path=target_path,
            ))

    return components


def _get_extension(component_type: str) -> str:
    """Get file extension for component type"""
    ext_map = {
        "claude_md": "md",
        "hooks": "json",
        "commands": "md",
        "agents": "json",
        "rules": "md",
        "skills": "md",
    }
    return ext_map.get(component_type, "md")


def _get_target_path(component_type: str, filename: str) -> str:
    """Get target installation path"""
    # If filename already contains a path (includes / or \), use it as-is
    # This prevents double nesting when LLM already output the component type prefix
    # Handles both forward slashes (Unix/macOS/Linux) and backslashes (Windows)
    if '/' in filename or '\\' in filename:
        # Normalize to forward slashes for consistent path handling across platforms
        return filename.replace('\\', '/')
    path_map = {
        "claude_md": "CLAUDE.md",
        "hooks": f"hooks/{filename}",
        "commands": f"commands/{filename}",
        "agents": f"agents/{filename}",
        "rules": f"rules/{filename}",
        "skills": f"skills/{filename}",
    }
    return path_map.get(component_type, filename)
