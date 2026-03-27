from datetime import datetime
from src.models import RoleMeta, PackageMeta, ToolComponent


def test_role_meta_creation():
    role = RoleMeta(
        name="python",
        category="backend",
        display_name="Python企业级后端开发规范",
        description="Python 后端开发规范",
        source_path="roles/backend/python.md",
        source_hash="abc123",
        tags=["python", "backend"],
    )
    assert role.name == "python"
    assert role.category == "backend"
    assert role.version == "1.0.0"  # default


def test_tool_component_defaults():
    comp = ToolComponent(
        type="claude_md",
        content="# CLAUDE.md",
        filename="CLAUDE.md",
        target_path="CLAUDE.md",
    )
    assert comp.schema_valid is False
