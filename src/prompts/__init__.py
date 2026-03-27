from .claude_md import PROMPT as CLAUDE_MD_PROMPT
from .hooks import PROMPT as HOOKS_PROMPT
from .commands import PROMPT as COMMANDS_PROMPT
from .agents import PROMPT as AGENTS_PROMPT
from .rules import PROMPT as RULES_PROMPT
from .skills import PROMPT as SKILLS_PROMPT

PROMPTS = {
    "claude_md": CLAUDE_MD_PROMPT,
    "hooks": HOOKS_PROMPT,
    "commands": COMMANDS_PROMPT,
    "agents": AGENTS_PROMPT,
    "rules": RULES_PROMPT,
    "skills": SKILLS_PROMPT,
}
