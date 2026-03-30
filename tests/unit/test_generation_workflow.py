from src.services.llm.factory import create_llm
from src.services.llm.generation.workflow import create_generation_workflow
from src.validator import OutputValidator


def test_workflow_creation():
    """Test that generation workflow can be created."""
    llm = create_llm()
    validator = OutputValidator()
    workflow = create_generation_workflow(llm, validator)
    assert workflow is not None
    assert hasattr(workflow, "invoke")

