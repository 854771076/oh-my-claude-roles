class OhRolesError(Exception):
    """Base exception for oh-roles"""
    code: str = ""
    message: str

    def __init__(self, message: str):
        self.message = message
        super().__init__(f"[{self.code}] {message}")


class RoleNotFoundError(OhRolesError):
    """Role not found in roles directory"""
    code = "ROLE_NOT_FOUND"


class CacheCorruptedError(OhRolesError):
    """Cache is corrupted and needs to be regenerated"""
    code = "CACHE_CORRUPTED"


class LLMConfigError(OhRolesError):
    """LLM configuration error (missing API key, invalid provider)"""
    code = "LLM_CONFIG_ERROR"


class LLMTimeoutError(OhRolesError):
    """LLM API call timed out"""
    code = "LLM_TIMEOUT"


class LLMRateLimitError(OhRolesError):
    """LLM API rate limit hit"""
    code = "LLM_RATE_LIMIT"


class GenerationFailedError(OhRolesError):
    """Generation of tool failed after retries"""
    code = "GENERATION_FAILED"


class ValidationError(OhRolesError):
    """LLM output validation failed (wrong format)"""
    code = "VALIDATION_ERROR"


class InstallError(OhRolesError):
    """Installation failed (permission, disk full)"""
    code = "INSTALL_ERROR"


class LLMProviderError(OhRolesError):
    """Unsupported LLM provider"""
    code = "LLM_PROVIDER_ERROR"
    message = "Unsupported LLM provider"


class RoleDesignError(OhRolesError):
    """Error during interactive role design"""
    code = "ROLE_DESIGN_ERROR"
    message = "Error during interactive role design"


class DocumentSaveError(OhRolesError):
    """Failed to save role document"""
    code = "DOCUMENT_SAVE_ERROR"
    message = "Failed to save role document"
