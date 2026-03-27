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
    prompt = generator._build_prompt("claude_md", "test content", role)
    assert "Python后端" in prompt
    assert "Python开发规范" in prompt
    assert "test content" in prompt


@pytest.mark.asyncio
async def test_call_llm_retries():
    # Patch where it's used (src.generator) not where it's imported from
    from src import generator
    with patch("src.generator.acompletion", new_callable=AsyncMock) as mock:
        # Create a mock response object with proper attribute access
        class MockMessage:
            content = "test output"
        class MockChoice:
            message = MockMessage()
        class MockResponse:
            choices = [MockChoice()]

        # First call: TimeoutError → code converts to LLMTimeoutError (retryable)
        # Second call: Exception with "rate limit" → code converts to LLMRateLimitError (retryable)
        # Third call: success
        mock.side_effect = [
            TimeoutError("timed out"),
            Exception("rate limit hit"),
            MockResponse()
        ]
        # We need to create after patching when constructor potentially calls
        # But constructor only checks api key, so just set it
        from src.config import settings
        generator = ToolGenerator()
        # Override api key for test
        generator.api_key = "test-key"
        result = await generator._call_llm("test prompt")
        assert result == "test output"
        assert mock.call_count == 3
