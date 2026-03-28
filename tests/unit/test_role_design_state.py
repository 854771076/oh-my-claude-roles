from src.services.llm.role_design.state import RoleDesignState


def test_state_defaults():
    state = RoleDesignState()
    assert state.name is None
    assert state.display_name is None
    assert state.tags == []
    assert state.current_step == "start"
    assert state.final_document is None


def test_state_with_values():
    state = RoleDesignState(
        name="python-backend",
        display_name="Python Backend",
        tags=["python", "backend"]
    )
    assert state.name == "python-backend"
    assert state.display_name == "Python Backend"
    assert state.tags == ["python", "backend"]


def test_state_with_new_fields():
    state = RoleDesignState(
        name="python-backend",
        display_name="Python Backend Developer",
        tags=["python", "backend"],
        project_scale="medium team 5-20",
        team_size="5 developers",
        compliance_requirements="GDPR, SOC 2",
    )
    assert state.name == "python-backend"
    assert state.display_name == "Python Backend Developer"
    assert state.tags == ["python", "backend"]
    assert state.project_scale == "medium team 5-20"
    assert state.team_size == "5 developers"
    assert state.compliance_requirements == "GDPR, SOC 2"


def test_new_fields_defaults():
    state = RoleDesignState(name="test")
    assert state.project_scale is None
    assert state.team_size is None
    assert state.compliance_requirements is None
