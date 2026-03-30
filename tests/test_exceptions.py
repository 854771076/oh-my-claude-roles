from src.exceptions import (
    CacheCorruptedError,
    DocumentSaveError,
    GenerationFailedError,
    InstallError,
    LLMConfigError,
    LLMProviderError,
    LLMRateLimitError,
    LLMTimeoutError,
    OhRolesError,
    RoleDesignError,
    RoleNotFoundError,
    ValidationError,
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
    assert LLMProviderError.code == "LLM_PROVIDER_ERROR"
    assert RoleDesignError.code == "ROLE_DESIGN_ERROR"
    assert DocumentSaveError.code == "DOCUMENT_SAVE_ERROR"

def test_exception_message():
    err = RoleNotFoundError("role not found")
    assert str(err) == "[ROLE_NOT_FOUND] role not found"


def test_all_exceptions_inherit_from_base():
    """Verify all exception classes inherit from OhRolesError"""
    assert issubclass(RoleNotFoundError, OhRolesError)
    assert issubclass(CacheCorruptedError, OhRolesError)
    assert issubclass(LLMConfigError, OhRolesError)
    assert issubclass(LLMTimeoutError, OhRolesError)
    assert issubclass(LLMRateLimitError, OhRolesError)
    assert issubclass(GenerationFailedError, OhRolesError)
    assert issubclass(ValidationError, OhRolesError)
    assert issubclass(InstallError, OhRolesError)
    assert issubclass(LLMProviderError, OhRolesError)
    assert issubclass(RoleDesignError, OhRolesError)
    assert issubclass(DocumentSaveError, OhRolesError)


def test_base_exception_instantiation():
    """Verify base class can be instantiated without crashing"""
    err = OhRolesError("base error")
    assert err.message == "base error"
    assert err.code == ""
    assert str(err) == "[] base error"


def test_all_exceptions_message_and_formatting():
    """Verify message attribute is set and string formatting works for all exceptions"""
    test_message = "test error message"

    # Test each exception type
    exceptions = [
        (RoleNotFoundError, "ROLE_NOT_FOUND"),
        (CacheCorruptedError, "CACHE_CORRUPTED"),
        (LLMConfigError, "LLM_CONFIG_ERROR"),
        (LLMTimeoutError, "LLM_TIMEOUT"),
        (LLMRateLimitError, "LLM_RATE_LIMIT"),
        (GenerationFailedError, "GENERATION_FAILED"),
        (ValidationError, "VALIDATION_ERROR"),
        (InstallError, "INSTALL_ERROR"),
        (LLMProviderError, "LLM_PROVIDER_ERROR"),
        (RoleDesignError, "ROLE_DESIGN_ERROR"),
        (DocumentSaveError, "DOCUMENT_SAVE_ERROR"),
    ]

    for exc_class, expected_code in exceptions:
        err = exc_class(test_message)
        assert isinstance(err, OhRolesError)
        assert err.message == test_message
        assert err.code == expected_code
        assert str(err) == f"[{expected_code}] {test_message}"
