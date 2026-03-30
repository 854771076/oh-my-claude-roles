from pydantic import BaseModel, Field


class RoleDesignState(BaseModel):
    """State for role design interactive agent."""

    # Collected role information
    name: str | None = Field(None, description="Unique role identifier")
    display_name: str | None = Field(None, description="Display name for UI")
    description: str | None = Field(None, description="Short description")
    category: str | None = Field(
        None, description="Category (backend/frontend/devops etc.)"
    )
    tags: list[str] = Field(default_factory=list, description="List of tags")
    target_domain: str | None = Field(
        None, description="Target domain and use case description"
    )
    tech_stack: str | None = Field(
        None, description="Technology stack requirements"
    )
    coding_standards: str | None = Field(
        None, description="Coding standards and best practices"
    )
    custom_content: str | None = Field(
        None, description="User-customized content"
    )

    # Additional information for enterprise-level documentation
    project_scale: str | None = Field(
        None, description="Project scale (e.g., small team <5, medium 5-20, large 20+)"
    )
    team_size: str | None = Field(None, description="Team size and composition")
    compliance_requirements: str | None = Field(
        None,
        description=(
            "Any specific compliance or "
            "regulatory requirements (e.g., GDPR, SOC 2)"
        )
    )

    # Conversation state
    current_step: str = Field(default="start", description="Current step identifier")
    conversation_history: list[dict] = Field(
        default_factory=list, description="Conversation history"
    )
    question: str | None = Field(None, description="Current question to ask user")

    # Final output
    final_document: str | None = Field(
        None, description="Final formatted Markdown document"
    )
    output_path: str | None = Field(None, description="Output file path")
