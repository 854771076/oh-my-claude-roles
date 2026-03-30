from unittest.mock import AsyncMock, patch

import pytest

from src.exceptions import GenerationFailedError, LLMRateLimitError
from src.generator import ToolGenerator
from src.models import PackageMeta, RoleMeta, ToolComponent


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

        # First call: hooks needs valid JSON matching schema
        class MockResponseHooks:
            content = """## 文件名: python.json
{
  "name": "python",
  "description": "Python development",
  "triggers": ["pre-commit"],
  "hooks": [
    {
      "type": "shell",
      "command": "echo hello"
    }
  ]
}"""

        class MockResponseClaude:
            content = "## 文件名: test.md\n# Test"

        # hooks is generated first, then claude_md
        mock_llm.ainvoke.side_effect = [MockResponseHooks(), MockResponseClaude()]

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
    multi_file_content = """## 文件名: python-hooks.json
{
  "name": "python-hooks",
  "description": "Python development hooks",
  "triggers": ["pre-commit"],
  "hooks": [
    {
      "type": "shell",
      "command": "lint python files"
    }
  ]
}

## 文件名: test-hooks.json
{
  "name": "test-hooks",
  "description": "Test development hooks",
  "triggers": ["pre-push"],
  "hooks": [
    {
      "type": "shell",
      "command": "run tests"
    }
  ]
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
        assert components[0].filename == "python-hooks.json"
        assert components[1].filename == "test-hooks.json"
        assert components[0].target_path == "hooks/python-hooks.json"
        assert components[1].target_path == "hooks/test-hooks.json"


# Legacy mode no longer exists - only workflow mode is supported
# @pytest.mark.asyncio
# async def test_workflow_vs_legacy_output_identical():
#     """Test that workflow mode produces identical output to legacy mode."""
#     mock_content = """## 文件名: CLAUDE.md
# # Test Content
# """
#
#     with patch("src.generator.create_llm") as mock_create_llm:
#         mock_llm = AsyncMock()
#         mock_create_llm.return_value = mock_llm
#
#         class MockResponse:
#             content = mock_content
#
#         mock_llm.ainvoke.return_value = MockResponse()
#
#         role = RoleMeta(
#             name="python",
#             category="backend",
#             display_name="Python后端",
#             description="Python开发规范",
#             source_path=__file__,
#             source_hash="abc123",
#             version="1.0.0",
#         )
#
#         # Test both modes
#         generator_legacy = ToolGenerator(use_workflow=False)
#         meta_legacy, components_legacy = await generator_legacy.generate_package(role, ["claude_md"])
#
#         generator_workflow = ToolGenerator(use_workflow=True)
#         meta_wf, components_wf = await generator_workflow.generate_package(role, ["claude_md"])
#
#         # Compare outputs
#         assert isinstance(meta_legacy, PackageMeta)
#         assert isinstance(meta_wf, PackageMeta)
#         assert meta_legacy.role == meta_wf.role
#         assert meta_legacy.version == meta_wf.version
#         assert meta_legacy.components == meta_wf.components
#         assert meta_legacy.llm_provider == meta_wf.llm_provider
#         assert meta_legacy.llm_model == meta_wf.llm_model
#
#         assert len(components_legacy) == len(components_wf)
#         for comp_legacy, comp_wf in zip(components_legacy, components_wf):
#             assert comp_legacy.type == comp_wf.type
#             assert comp_legacy.filename == comp_wf.filename
#             assert comp_legacy.target_path == comp_wf.target_path
#             assert comp_legacy.content == comp_wf.content
#             assert comp_legacy.schema_valid == comp_wf.schema_valid


@pytest.mark.asyncio
async def test_workflow_handles_llm_timeout():
    """Test that workflow mode handles LLM timeout errors identically to legacy mode."""
    import tenacity
    with patch("src.generator.create_llm") as mock_create_llm:
        mock_llm = AsyncMock()
        mock_create_llm.return_value = mock_llm
        mock_llm.ainvoke.side_effect = TimeoutError("LLM call timed out")

        role = RoleMeta(
            name="python",
            category="backend",
            display_name="Python后端",
            description="Python开发规范",
            source_path=__file__,
            source_hash="abc123",
            version="1.0.0",
        )

        # Test workflow mode - can get tenacity.RetryError when retries are exhausted
        generator_workflow = ToolGenerator(use_workflow=True)
        with pytest.raises((GenerationFailedError, tenacity.RetryError)):
            await generator_workflow.generate_package(role, ["claude_md"])


@pytest.mark.asyncio
async def test_workflow_handles_rate_limit():
    """Test that workflow mode handles rate limit errors identically to legacy mode."""
    import tenacity
    with patch("src.generator.create_llm") as mock_create_llm:
        mock_llm = AsyncMock()
        mock_create_llm.return_value = mock_llm
        mock_llm.ainvoke.side_effect = LLMRateLimitError("Rate limit exceeded")

        role = RoleMeta(
            name="python",
            category="backend",
            display_name="Python后端",
            description="Python开发规范",
            source_path=__file__,
            source_hash="abc123",
            version="1.0.0",
        )

        generator_workflow = ToolGenerator(use_workflow=True)
        with pytest.raises((GenerationFailedError, tenacity.RetryError)):
            await generator_workflow.generate_package(role, ["claude_md"])


@pytest.mark.asyncio
async def test_workflow_handles_generation_failure():
    with patch("src.generator.create_llm") as mock_create_llm:
        mock_llm = AsyncMock()
        mock_create_llm.return_value = mock_llm
        mock_llm.ainvoke.side_effect = GenerationFailedError("Generation failed")

        role = RoleMeta(
            name="python",
            category="backend",
            display_name="Python后端",
            description="Python开发规范",
            source_path=__file__,
            source_hash="abc123",
            version="1.0.0",
        )

        generator_workflow = ToolGenerator(use_workflow=True)
        with pytest.raises(GenerationFailedError):
            await generator_workflow.generate_package(role, ["invalid_component"])
