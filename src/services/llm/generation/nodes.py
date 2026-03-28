from typing import List, TYPE_CHECKING
import importlib.resources
import re
from loguru import logger
from langchain_core.messages import HumanMessage
from src.models import RoleMeta, PackageMeta, ToolComponent
from src.validator import OutputValidator
from src.config import settings
from src.exceptions import GenerationFailedError

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
    """Generate all requested components in parallel."""
    import asyncio

    role = state["role"]
    source_content = state["source_content"]
    requested = state["requested_components"]
    llm = state["_llm"]
    concurrency = state["_concurrency"]

    logger.info(f"Workflow starting parallel generation: {len(requested)} components, concurrency={concurrency} for {role.category}/{role.name}")
    semaphore = asyncio.Semaphore(concurrency)

    async def generate_one(comp_type: str) -> ToolComponent | None:
        async with semaphore:
            logger.info(f"Generating component: {comp_type}")
            prompt = build_prompt(comp_type, source_content, role, requested)
            logger.debug(f"Prompt built: {len(prompt)} characters")
            response = await llm.ainvoke([HumanMessage(content=prompt)])
            content = response.content.strip()
            logger.debug(f"LLM response: {len(content)} characters")
            parsed = parse_response(comp_type, content, role)
            logger.success(f"Component {comp_type} parsed: {len(parsed)} file(s)")
            return parsed

    tasks = [generate_one(comp) for comp in requested]
    results = await asyncio.gather(*tasks, return_exceptions=True)

    generated: List[ToolComponent] = []
    failed: List[str] = []

    for comp_type, result in zip(requested, results):
        if isinstance(result, Exception):
            logger.error(f"Component generation failed: {comp_type}, error: {str(result)}")
            failed.append(comp_type)
            continue
        if result:
            if isinstance(result, list):
                generated.extend(result)
            else:
                generated.append(result)

    logger.info(f"Parallel generation complete: {len(generated)} files generated, {len(failed)} failed")
    return {
        "generated_components": generated,
        "failed_components": failed,
    }


async def validate_components_node(state: "GenerationWorkflowState") -> dict:
    """Validate all generated components against schema."""
    validator = state["_validator"]
    generated = state["generated_components"]

    logger.info(f"Validating {len(generated)} generated components")
    for comp in generated:
        try:
            comp.schema_valid = validator.validate(comp)
            if not comp.schema_valid:
                logger.warning(f"Validation failed for: {comp.filename}")
        except Exception:
            comp.schema_valid = False
            logger.warning(f"Validation exception for: {comp.filename}")

    logger.info(f"Validation complete: {len(generated)} components processed")
    return {
        "validated_components": generated,
        "failed_components": state["failed_components"],
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

    package_meta = PackageMeta(
        role=role,
        version=role.version,
        generated_at=datetime.now(),
        llm_provider=settings.llm_provider,
        llm_model=settings.llm_model,
        components=[c.type for c in components],
    )

    logger.success(f"Package generation complete: {role.category}/{role.name}")
    return {"package_meta": package_meta}


def build_prompt(
    component_type: str,
    source_content: str,
    role: RoleMeta,
    all_components: list[str],
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
        lines = [f"- {comp}: {component_descriptions.get(comp, comp)}" for comp in all_components]
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
    pattern = r"##\s+文件名:\s+(.+?)\n"
    parts = re.split(pattern, content)

    if len(parts) == 1:
        # Single file, guess filename
        ext = _get_extension(component_type)
        filename = f"{role.name}.{ext}"
        target_path = _get_target_path(component_type, filename)
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
        "rules": "yaml",
        "skills": "md",
    }
    return ext_map.get(component_type, "md")


def _get_target_path(component_type: str, filename: str) -> str:
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
