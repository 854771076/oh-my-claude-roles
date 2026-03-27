from langgraph.graph import StateGraph, END
from langchain_core.language_models.chat_models import BaseChatModel
from .state import RoleDesignState
from .nodes import get_next_step, collect_user_input, generate_question, generate_final_document


def should_continue(state: RoleDesignState) -> str:
    """Determine if we need to continue asking questions or generate final document."""
    next_step = get_next_step(state)
    if next_step == "generate_final":
        return "generate"
    else:
        return "ask"


async def ask_question_node(state: RoleDesignState, llm: BaseChatModel) -> RoleDesignState:
    """Generate the next question (output to user)."""
    # Question generation happens before human input
    state.question = await generate_question(state, llm)
    return state


async def collect_input_node(
    state: RoleDesignState,
    user_input: str,
) -> RoleDesignState:
    """Collect user input and update state."""
    return collect_user_input(state, user_input)


async def generate_final_node(
    state: RoleDesignState,
    llm: BaseChatModel,
) -> RoleDesignState:
    """Generate the final document."""
    final_doc = await generate_final_document(state, llm)
    state.final_document = final_doc
    return state


def create_role_design_graph(llm: BaseChatModel) -> StateGraph:
    """Create the role design LangGraph."""
    builder = StateGraph(RoleDesignState)

    # Add nodes
    builder.add_node("ask_question", lambda state: ask_question_node(state, llm))
    builder.add_node("collect_input", collect_input_node)
    builder.add_node("generate_final", lambda state: generate_final_node(state, llm))

    # Add edges
    builder.set_entry_point("ask_question")
    builder.add_conditional_edges(
        "ask_question",
        should_continue,
        {
            "ask": "collect_input",
            "generate": "generate_final",
        },
    )
    builder.add_edge("collect_input", "ask_question")
    builder.add_edge("generate_final", END)

    return builder.compile()
