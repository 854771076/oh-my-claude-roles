import pytest
from unittest.mock import patch, AsyncMock
from src.generator import ToolGenerator
from src.models import RoleMeta, PackageMeta, ToolComponent


@pytest.mark.asyncio
async def test_workflow_generates_same_output_structure():
    """Test that use_workflow=True returns same structure as legacy mode."""
    mock_content = """## 文件名: CLAUDE.md
# Test Content
"""

    with patch("src.generator.create_llm") as mock_create_llm:
        mock_llm = AsyncMock()
        mock_create_llm.return_value = mock_llm

        class MockResponse:
            content = mock_content

        mock_llm.ainvoke.return_value = MockResponse()

        role = RoleMeta(
            name="python",
            category="backend",
            display_name="Python后端",
            description="Python开发规范",
            source_path=__file__,
            source_hash="abc123",
            version="1.0.0",
        )

        # Test with workflow
        generator_workflow = ToolGenerator(use_workflow=True)
        meta_wf, components_wf = await generator_workflow.generate_package(role, ["claude_md"])

        # Check return types
        assert isinstance(meta_wf, PackageMeta)
        assert isinstance(components_wf, list)
        assert len(components_wf) == 1
        assert all(isinstance(c, ToolComponent) for c in components_wf)

        # Check metadata
        assert meta_wf.role == role
        assert meta_wf.version == role.version
        assert meta_wf.components == ["claude_md"]
        assert meta_wf.llm_provider is not None
        assert meta_wf.llm_model is not None

        # Check component
        comp = components_wf[0]
        assert comp.type == "claude_md"
        assert comp.filename == "CLAUDE.md"
        assert comp.target_path == "CLAUDE.md"
        assert "# Test Content" in comp.content
        assert comp.schema_valid is not None


@pytest.mark.asyncio
async def test_workflow_handles_multiple_components():
    """Test that workflow handles multiple components correctly."""
    with patch("src.generator.create_llm") as mock_create_llm:
        mock_llm = AsyncMock()
        mock_create_llm.return_value = mock_llm

        class MockResponse:
            content = "## 文件名: test.md\n# Test"

        mock_llm.ainvoke.return_value = MockResponse()

        role = RoleMeta(
            name="python",
            category="backend",
            display_name="Python后端",
            description="Python开发规范",
            source_path=__file__,
            source_hash="abc123",
        )

        generator = ToolGenerator(use_workflow=True)
        meta, components = await generator.generate_package(role, ["claude_md", "hooks"])

        assert len(components) == 2
        assert len(meta.components) == 2
        assert meta.version == "1.0.0"  # Default from RoleMeta


@pytest.mark.asyncio
async def test_workflow_parses_multiple_files_per_component():
    """Test that workflow correctly parses multiple files from one component."""
    multi_file_content = """## 文件名: python.json
{
  "key": "value"
}

## 文件名: another.json
{
  "key2": "value2"
}
"""

    with patch("src.generator.create_llm") as mock_create_llm:
        mock_llm = AsyncMock()
        mock_create_llm.return_value = mock_llm

        class MockResponse:
            content = multi_file_content

        mock_llm.ainvoke.return_value = MockResponse()

        role = RoleMeta(
            name="python",
            category="backend",
            display_name="Python后端",
            description="Python开发规范",
            source_path=__file__,
            source_hash="abc123",
        )

        generator = ToolGenerator(use_workflow=True)
        meta, components = await generator.generate_package(role, ["hooks"])

        assert len(components) == 2
        assert components[0].filename == "python.json"
        assert components[1].filename == "another.json"
        assert components[0].target_path == "hooks/python.json"
        assert components[1].target_path == "hooks/another.json"
