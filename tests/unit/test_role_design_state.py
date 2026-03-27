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
