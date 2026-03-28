"""Shared utility functions for LLM generation workflows and legacy generator."""
import importlib.resources
from typing import List
from src.models import RoleMeta, ToolComponent


def load_prompt(filename: str) -> str:
    """Load prompt template from file."""
    with importlib.resources.files(
        "src.services.llm.generation.prompts"
    ).joinpath(filename).open(encoding="utf-8") as f:
        return f.read()


def build_prompt(
    component_type: str,
    source_content: str,
    role: RoleMeta,
    all_components: list[str],
) -> str:
    """Build prompt from template. Reuses logic from ToolGenerator."""
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
    import re
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
