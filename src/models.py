from datetime import datetime

from pydantic import BaseModel


class RoleMeta(BaseModel):
    """Role metadata from parsing markdown document"""
    name: str                    # Role name, e.g. "python"
    category: str                # Category, e.g. "backend"
    display_name: str            # Display name for UI
    description: str             # Short description
    source_path: str             # Source document path
    source_hash: str             # SHA256 hash of source (first 16 chars)
    tags: list[str] = []         # Tags for filtering
    version: str = "1.0.0"       # Document version


class PackageMeta(BaseModel):
    """Package metadata for cached tool package"""
    role: RoleMeta               # Associated role
    version: str                 # Semantic version
    generated_at: datetime       # Generation timestamp
    llm_provider: str            # Which LLM provider used
    llm_model: str               # Which model used
    components: list[str]        # List of generated component types


class ToolComponent(BaseModel):
    """Single tool component (file to install)"""
    type: str                    # Component type: claude_md, hooks, commands, etc.
    content: str                 # File content
    filename: str                # Output filename
    target_path: str             # Target installation path (relative to .claude/)
    schema_valid: bool = False   # Whether passed schema validation
