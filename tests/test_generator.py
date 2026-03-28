import pytest
from src.services.llm.generation.nodes import build_prompt
from src.models import RoleMeta


def test_build_prompt():
    role = RoleMeta(
        name="python",
        category="backend",
        display_name="Python后端",
        description="Python开发规范",
        source_path="test.md",
        source_hash="abc123",
    )
    prompt = build_prompt("claude_md", "test content", role, ["claude_md", "hooks", "commands"])
    assert "Python后端" in prompt
    assert "Python开发规范" in prompt
    assert "test content" in prompt
    # claude_md is excluded from component list when generating claude_md itself
    assert "hooks" in prompt
    assert "commands" in prompt
