import pytest
from unittest.mock import patch, AsyncMock
from src.generator import ToolGenerator
from src.models import RoleMeta
from src.config import settings


def test_build_prompt():
    generator = ToolGenerator()
    role = RoleMeta(
        name="python",
        category="backend",
        display_name="Python后端",
        description="Python开发规范",
        source_path="test.md",
        source_hash="abc123",
    )
    prompt = generator._build_prompt("claude_md", "test content", role, ["claude_md", "hooks", "commands"])
    assert "Python后端" in prompt
    assert "Python开发规范" in prompt
    assert "test content" in prompt
    assert "本次生成将包含以下组件" in prompt
    assert "claude_md" in prompt
    assert "hooks" in prompt


@pytest.mark.asyncio
async def test_call_llm_retries():
    # Patch the create_llm function to return a mock
    with patch("src.generator.create_llm") as mock_create_llm:
        # Create a mock LLM instance
        mock_llm = AsyncMock()
        mock_create_llm.return_value = mock_llm

        # Create a mock response object for LangChain
        class MockResponse:
            content = "test output"

        # First call: TimeoutError → code converts to LLMTimeoutError (retryable)
        # Second call: Exception with "rate limit" → code converts to LLMRateLimitError (retryable)
        # Third call: success
        mock_llm.ainvoke.side_effect = [
            TimeoutError("timed out"),
            Exception("rate limit hit"),
            MockResponse()
        ]

        generator = ToolGenerator()
        result = await generator._call_llm("test prompt")
        assert result == "test output"
        assert mock_llm.ainvoke.call_count == 3
