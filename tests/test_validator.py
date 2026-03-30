import pytest

from src.exceptions import ValidationError
from src.models import ToolComponent
from src.validator import OutputValidator


def test_validate_json_valid():
    validator = OutputValidator()
    comp = ToolComponent(
        type="hooks",
        content='{"name": "test", "description": "test", "triggers": ["PreToolUse"], "hooks": []}',
        filename="test.json",
        target_path="hooks/test.json",
    )
    result = validator.validate(comp)
    assert result is True


def test_validate_json_invalid():
    validator = OutputValidator()
    comp = ToolComponent(
        type="hooks",
        content="not valid json",
        filename="test.json",
        target_path="hooks/test.json",
    )
    with pytest.raises(ValidationError):
        validator.validate(comp)
