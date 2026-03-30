from unittest.mock import patch

import pytest

from src.exceptions import LLMProviderError
from src.services.llm.factory import create_llm


def test_create_llm_invalid_provider():
    with patch("src.config.settings.llm_provider", "invalid"):
        with pytest.raises(LLMProviderError):
            create_llm()


def test_create_llm_openai():
    from langchain_openai import ChatOpenAI
    with patch("src.config.settings.llm_provider", "openai"):
        with patch("src.config.settings.llm_api_key", "test-key"):
            llm = create_llm()
            assert isinstance(llm, ChatOpenAI)
