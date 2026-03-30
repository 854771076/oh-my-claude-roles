import json

import yaml
from jsonschema import ValidationError as SchemaValidationError
from jsonschema import validate

from .exceptions import ValidationError
from .models import ToolComponent

# JSON Schemas for Claude Code components
# HOOK_SCHEMA = {
#     "type": "object",
#     "required": ["hooks"],
#     "properties": {
#         "description": {"type": "string"},
#         "hooks": {
#             "type": "object",
#             "additionalProperties": {
#                 "type": "array",
#                 "items": {
#                     "type": "object",
#                     "properties": {
#                         "matcher": {"type": "string"},
#                         "hooks": {
#                             "type": "array",
#                             "items": {
#                                 "type": "object",
#                                 "required": ["type"],
#                                 "oneOf": [
#                                     {"required": ["command"]},
#                                     {"required": ["prompt"]}
#                                 ],
#                                 "properties": {
#                                     "type": {"type": "string", "enum": ["command", "prompt"]},
#                                     "command": {"type": "string"},
#                                     "prompt": {"type": "string"},
#                                     "timeout": {"type": "integer"},
#                                 },
#                             },
#                         },
#                     },
#                 },
#             },
#         },
#     },
# }



class OutputValidator:
    """Validate LLM generated output against schemas"""

    def validate(self, component: ToolComponent) -> bool:
        """Validate component content based on type"""
        try:
            if component.type == "claude_md":
                return self._validate_markdown(component.content)
            elif component.type == "hooks":
                return self._validate_json(component.content)
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

    def _validate_json(self, content: str, schema: dict={}) -> bool:
        """Validate JSON against schema"""
        # Clean content: extract from code blocks if present
        content = self._extract_code_block(content)
        try:
            json.loads(content)
            # validate(instance=data, schema=schema)
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
