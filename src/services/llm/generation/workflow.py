from typing import TypedDict, List, Optional
from langgraph.graph import StateGraph, END
from langchain_core.language_models.chat_models import BaseChatModel
from src.models import RoleMeta, PackageMeta, ToolComponent
from src.validator import OutputValidator
from .nodes import (
    read_source_node,
    parallel_generation_node,
    validate_components_node,
    build_package_node,
)


class GenerationWorkflowState(TypedDict):
    """State for the generation workflow."""
    role: RoleMeta
    requested_components: List[str]
    source_content: Optional[str]
    generated_components: List[ToolComponent]
    validated_components: List[ToolComponent]
    failed_components: List[str]
    package_meta: Optional[PackageMeta]
    error: Optional[str]
    _llm: Optional[BaseChatModel]
    _validator: Optional[OutputValidator]
    _concurrency: int


def create_generation_workflow(
    llm: BaseChatModel,
    validator: OutputValidator,
    concurrency: int = None,
) -> StateGraph:
    """Create LangGraph workflow for complete tool package generation."""

    workflow = StateGraph(GenerationWorkflowState)

    # Add nodes
    workflow.add_node("read_source", read_source_node)
    workflow.add_node("generate_components", parallel_generation_node)
    workflow.add_node("validate_components", validate_components_node)
    workflow.add_node("build_package", build_package_node)

    # Define edges
    workflow.set_entry_point("read_source")
    workflow.add_edge("read_source", "generate_components")
    workflow.add_edge("generate_components", "validate_components")
    workflow.add_edge("validate_components", "build_package")
    workflow.add_edge("build_package", END)

    return workflow.compile()
