from langchain_core.language_models.chat_models import BaseChatModel
from langgraph.graph import END, StateGraph
from langgraph.graph.state import CompiledStateGraph

from .nodes import (
    generate_final_document,
    generate_question,
    get_next_step,
)
from .state import RoleDesignState


def should_continue(state: RoleDesignState) -> str:
    """Determine if we need to continue asking questions or generate final document."""
    next_step = get_next_step(state)
    if next_step == "generate_final":
        return "generate"
    else:
        return "collect_input"


def create_role_design_graph(llm: BaseChatModel) -> CompiledStateGraph:
    """Create the role design LangGraph."""
    builder = StateGraph(RoleDesignState)

    # Add nodes - use partial application for passing llm
    from functools import partial
    builder.add_node(
        "ask_question",
        partial(ask_question_node, llm=llm)
    )
    builder.add_node("collect_input", collect_input_node)
    builder.add_node(
        "generate_final",
        partial(generate_final_node, llm=llm)
    )

    # Add edges
    builder.set_entry_point("ask_question")
    builder.add_conditional_edges(
        "ask_question",
        should_continue,
        {
            "collect_input": "collect_input",
            "generate": "generate_final",
        },
    )
    builder.add_edge("collect_input", "ask_question")
    builder.add_edge("generate_final", END)

    return builder.compile()


async def ask_question_node(
    state: RoleDesignState, llm: BaseChatModel
) -> RoleDesignState:
    """Generate the next question (output to user)."""
    # Question generation happens before human input
    state.question = await generate_question(state, llm)
    return state


async def collect_input_node(
    state: RoleDesignState,
) -> RoleDesignState:
    """No-op node - user input is collected externally and state is already updated."""
    return state


async def generate_final_node(
    state: RoleDesignState,
    llm: BaseChatModel,
) -> RoleDesignState:
    """Generate the final document."""
    final_doc = await generate_final_document(state, llm)
    state.final_document = final_doc
    return state
