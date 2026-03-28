import importlib.resources
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import HumanMessage
from .state import RoleDesignState


def load_prompt(filename: str) -> str:
    """Load prompt template from file."""
    with importlib.resources.files(
        "src.services.llm.role_design.prompts"
    ).joinpath(filename).open(encoding="utf-8") as f:
        return f.read()


def get_next_step(state: RoleDesignState) -> str:
    """Determine the next step based on collected information."""
    if state.name is None:
        return "ask_name"
    elif state.display_name is None:
        return "ask_display_name"
    elif state.description is None:
        return "ask_description"
    elif state.category is None:
        return "ask_category"
    elif not state.tags:
        return "ask_tags"
    elif state.target_domain is None:
        return "ask_target_domain"
    elif state.tech_stack is None:
        return "ask_tech_stack"
    elif state.coding_standards is None:
        return "ask_coding_standards"
    elif state.project_scale is None:
        return "ask_project_scale"
    elif state.team_size is None:
        return "ask_team_size"
    elif state.compliance_requirements is None:
        return "ask_compliance_requirements"
    elif state.custom_content is None:
        return "ask_custom_content"
    else:
        return "generate_final"


def collect_user_input(state: RoleDesignState, user_input: str) -> RoleDesignState:
    """Collect user input into state based on current step."""
    current_step = state.current_step

    if current_step == "ask_name":
        state.name = user_input.strip().lower().replace(" ", "-")
    elif current_step == "ask_display_name":
        state.display_name = user_input.strip()
    elif current_step == "ask_description":
        state.description = user_input.strip()
    elif current_step == "ask_category":
        state.category = user_input.strip().lower()
    elif current_step == "ask_tags":
        tags = [t.strip().lower() for t in user_input.split(",") if t.strip()]
        state.tags = tags
    elif current_step == "ask_target_domain":
        state.target_domain = user_input.strip()
    elif current_step == "ask_tech_stack":
        state.tech_stack = user_input.strip()
    elif current_step == "ask_coding_standards":
        state.coding_standards = user_input.strip()
    elif current_step == "ask_project_scale":
        state.project_scale = user_input.strip()
    elif current_step == "ask_team_size":
        state.team_size = user_input.strip()
    elif current_step == "ask_compliance_requirements":
        state.compliance_requirements = user_input.strip()
    elif current_step == "ask_custom_content":
        state.custom_content = user_input.strip()

    # Update current step to next step after collecting input
    state.current_step = get_next_step(state)
    return state


async def generate_question(
    state: RoleDesignState,
    llm: BaseChatModel,
) -> str:
    """Generate the next question using LLM."""
    template = load_prompt("ask_step_question.md")

    collected_info = "\n".join([
        f"- name: {state.name}",
        f"- display_name: {state.display_name}",
        f"- description: {state.description}",
        f"- category: {state.category}",
        f"- tags: {state.tags}",
        f"- target_domain: {state.target_domain}",
        f"- tech_stack: {state.tech_stack}",
        f"- coding_standards: {state.coding_standards}",
        f"- project_scale: {state.project_scale}",
        f"- team_size: {state.team_size}",
        f"- compliance_requirements: {state.compliance_requirements}",
        f"- custom_content: {state.custom_content}",
    ])

    prompt = template.format(
        current_step=state.current_step,
        collected_info=collected_info,
        name=state.name or "(not collected)",
        display_name=state.display_name or "(not collected)",
        description=state.description or "(not collected)",
        category=state.category or "(not collected)",
        tags=state.tags or "(not collected)",
        target_domain=state.target_domain or "(not collected)",
        tech_stack=state.tech_stack or "(not collected)",
        coding_standards=state.coding_standards or "(not collected)",
        project_scale=state.project_scale or "(not collected)",
        team_size=state.team_size or "(not collected)",
        compliance_requirements=state.compliance_requirements or "(not collected)",
        custom_content=state.custom_content or "(not collected)",
    )

    response = await llm.ainvoke([HumanMessage(content=prompt)])
    return response.content.strip()


async def generate_final_document(
    state: RoleDesignState,
    llm: BaseChatModel,
) -> str:
    """Generate the final Markdown document."""
    template = load_prompt("generate_document.md")

    collected_info = f"""
name: {state.name}
display_name: {state.display_name}
description: {state.description}
category: {state.category}
tags: {', '.join(state.tags)}
target_domain: {state.target_domain}
tech_stack:

{state.tech_stack}

coding_standards:

{state.coding_standards}

project_scale:

{state.project_scale}

team_size:

{state.team_size}

compliance_requirements:

{state.compliance_requirements}

custom_content:

{state.custom_content}
"""

    prompt = template.format(collected_info=collected_info)
    response = await llm.ainvoke([HumanMessage(content=prompt)])
    content = response.content.strip()

    # Remove wrapping code block if present
    if content.startswith("```"):
        content = content[content.find("\n")+1:].rstrip()
        if content.endswith("```"):
            content = content[:-3].rstrip()

    return content
