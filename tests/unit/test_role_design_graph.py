from src.services.llm.role_design.state import RoleDesignState
from src.services.llm.role_design.nodes import get_next_step


def test_get_next_step_start():
    state = RoleDesignState()
    assert get_next_step(state) == "ask_name"


def test_get_next_step_after_name():
    state = RoleDesignState(name="test")
    assert get_next_step(state) == "ask_display_name"


def test_get_next_step_complete():
    state = RoleDesignState(
        name="test",
        display_name="Test",
        description="Test description",
        category="test",
        tags=["test"],
        target_domain="Testing",
        tech_stack="Python",
        coding_standards="PEP8",
        custom_content="None",
    )
    assert get_next_step(state) == "generate_final"


def test_get_next_step_after_project_scale():
    # After project_scale, go directly to generate_final (no ask_team_size anymore)
    state = RoleDesignState(
        name="test",
        display_name="Test",
        description="Test description",
        category="test",
        tags=["test"],
        target_domain="Testing",
        tech_stack="Python",
        coding_standards="PEP8",
        project_scale="medium",
    )
    assert get_next_step(state) == "generate_final"


def test_get_next_step_complete_all():
    state = RoleDesignState(
        name="test",
        display_name="Test",
        description="Test description",
        category="test",
        tags=["test"],
        target_domain="Testing",
        tech_stack="Python",
        coding_standards="PEP8",
        project_scale="medium",
        team_size="5 people",
        compliance_requirements="GDPR",
        custom_content="None",
    )
    assert get_next_step(state) == "generate_final"
