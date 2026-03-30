from langchain_core.language_models.chat_models import BaseChatModel

from src.config import settings
from src.exceptions import LLMProviderError


def create_llm() -> BaseChatModel:
    """Create LangChain ChatModel based on configuration."""
    provider = settings.llm_provider.lower()
    model = settings.llm_model
    api_key = settings.llm_api_key
    base_url = settings.llm_base_url
    timeout = settings.llm_timeout

    if provider == "openai":
        from langchain_openai import ChatOpenAI
        return ChatOpenAI(
            model=model,
            api_key=api_key,
            base_url=base_url,
            timeout=timeout,
        )
    elif provider == "anthropic":
        from langchain_anthropic import ChatAnthropic
        return ChatAnthropic(
            model=model,
            api_key=api_key,
            base_url=base_url,
            timeout=timeout,
        )
    elif provider == "azure":
        from langchain_openai import AzureChatOpenAI
        return AzureChatOpenAI(
            azure_deployment=model,
            api_key=api_key,
            azure_endpoint=base_url,
            timeout=timeout,
        )
    elif provider == "gemini":
        from langchain_google_genai import ChatGoogleGenerativeAI
        return ChatGoogleGenerativeAI(
            model=model,
            api_key=api_key,
            base_url=base_url,
            timeout=timeout,
        )
    elif provider == "ollama":
        from langchain_community.chat_models import ChatOllama
        return ChatOllama(
            model=model,
            base_url=base_url,
            timeout=timeout,
        )
    else:
        raise LLMProviderError(
            f"Unsupported LLM provider: {provider}. "
            "Supported providers: openai, anthropic, azure, gemini, ollama"
        )
