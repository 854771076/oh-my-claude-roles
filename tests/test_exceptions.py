import pytest
from src.exceptions import (
    OhRolesError,
    RoleNotFoundError,
    CacheCorruptedError,
    LLMConfigError,
    LLMTimeoutError,
    LLMRateLimitError,
    GenerationFailedError,
    ValidationError,
    InstallError,
)

def test_exception_codes():
    assert RoleNotFoundError.code == "ROLE_NOT_FOUND"
    assert CacheCorruptedError.code == "CACHE_CORRUPTED"
    assert LLMConfigError.code == "LLM_CONFIG_ERROR"
    assert LLMTimeoutError.code == "LLM_TIMEOUT"
    assert LLMRateLimitError.code == "LLM_RATE_LIMIT"
    assert GenerationFailedError.code == "GENERATION_FAILED"
    assert ValidationError.code == "VALIDATION_ERROR"
    assert InstallError.code == "INSTALL_ERROR"

def test_exception_message():
    err = RoleNotFoundError("role not found")
    assert str(err) == "[ROLE_NOT_FOUND] role not found"