import json
import yaml
from jsonschema import validate, ValidationError as SchemaValidationError
from .models import ToolComponent
from .exceptions import ValidationError

# JSON Schemas for Claude Code components
HOOK_SCHEMA = {
    "type": "object",
    "required": ["name", "description", "triggers", "hooks"],
    "properties": {
        "name": {"type": "string"},
        "description": {"type": "string"},
        "triggers": {"type": "array", "items": {"type": "string"}},
        "matcher": {"type": "string"},
        "hooks": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["type", "command"],
                "properties": {
                    "type": {"type": "string"},
                    "command": {"type": "string"},
                    "timeout": {"type": "integer"},
                },
            },
        },
    },
}

AGENT_SCHEMA = {
    "type": "object",
    "required": ["name", "description", "system_prompt"],
    "properties": {
        "name": {"type": "string"},
        "description": {"type": "string"},
        "model": {"type": "string"},
        "system_prompt": {"type": "string"},
        "tools": {"type": "array", "items": {"type": "string"}},
        "allowed_paths": {"type": "array", "items": {"type": "string"}},
    },
}

RULE_SCHEMA = {
    "type": "object",
    "required": ["name", "rules"],
    "properties": {
        "name": {"type": "string"},
        "version": {"type": "string"},
        "rules": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["id", "description", "pattern", "severity"],
                "properties": {
                    "id": {"type": "string"},
                    "description": {"type": "string"},
                    "pattern": {"type": "string"},
                    "severity": {"type": "string", "enum": ["error", "warning", "info"]},
                },
            },
        },
    },
}


class OutputValidator:
    """Validate LLM generated output against schemas"""

    def validate(self, component: ToolComponent) -> bool:
        """Validate component content based on type"""
        try:
            if component.type == "claude_md":
                return self._validate_markdown(component.content)
            elif component.type == "hooks":
                return self._validate_json(component.content, HOOK_SCHEMA)
            elif component.type == "commands":
                return self._validate_markdown(component.content)
            elif component.type == "agents":
                return self._validate_markdown(component.content)
            elif component.type == "rules":
                return self._validate_markdown(component.content)
            elif component.type == "skills":
                return self._validate_markdown(component.content)
            return True
        except SchemaValidationError as e:
            raise ValidationError(f"Schema validation failed for {component.type}: {e}")

    def _validate_json(self, content: str, schema: dict) -> bool:
        """Validate JSON against schema"""
        # Clean content: extract from code blocks if present
        content = self._extract_code_block(content)
        try:
            data = json.loads(content)
            validate(instance=data, schema=schema)
            return True
        except json.JSONDecodeError as e:
            raise ValidationError(f"Invalid JSON: {e}")

    def _validate_yaml(self, content: str, schema: dict) -> bool:
        """Validate YAML against schema"""
        content = self._extract_code_block(content)
        try:
            data = yaml.safe_load(content)
            validate(instance=data, schema=schema)
            return True
        except yaml.YAMLError as e:
            raise ValidationError(f"Invalid YAML: {e}")

    def _validate_markdown(self, content: str) -> bool:
        """Markdown validation is just checking it's not empty"""
        return len(content.strip()) > 0

    def _extract_code_block(self, content: str) -> str:
        """Extract content from ```json ... ``` when present"""
        content = content.strip()
        # Remove leading/trailing code blocks
        if content.startswith("```"):
            lines = content.split("\n")
            # Skip first line (```json or similar)
            start = 1
            # Find last line that is ```
            for i in range(len(lines) - 1, -1, -1):
                if lines[i].strip() == "```":
                    end = i
                    break
            else:
                end = len(lines)
            content = "\n".join(lines[start:end])
        return content.strip()
