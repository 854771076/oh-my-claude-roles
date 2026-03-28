import asyncio
import re
import tenacity
from typing import List, Tuple

from loguru import logger
from langchain_core.messages import HumanMessage

from src.config import settings
from src.exceptions import (
    GenerationFailedError,
    LLMConfigError,
    LLMRateLimitError,
    LLMTimeoutError,
)
from src.models import PackageMeta, RoleMeta, ToolComponent
from src.services.llm.factory import create_llm
from src.services.llm.generation.workflow import create_generation_workflow
from src.validator import OutputValidator


class ToolGenerator:
    """Generate tool components using LLM"""

    def __init__(self, use_workflow: bool = True):
        self.llm = create_llm()
        self.concurrency = settings.llm_concurrency
        self.validator = OutputValidator()
        self.use_workflow = use_workflow
        if self.use_workflow:
            self.workflow = create_generation_workflow(
                llm=self.llm,
                validator=self.validator,
                concurrency=self.concurrency
            )

    async def generate_package(
        self,
        role: RoleMeta,
        components: List[str] | None = None,
    ) -> Tuple[PackageMeta, List[ToolComponent]]:
        """Generate complete tool package for a role"""
        if self.use_workflow:
            return await self.generate_package_with_workflow(role, components)


    async def generate_package_with_workflow(
        self,
        role: RoleMeta,
        components: List[str] | None = None,
    ) -> Tuple[PackageMeta, List[ToolComponent]]:
        """Generate complete tool package for a role using LangGraph workflow"""
        components = components or settings.default_components

        initial_state = {
            "role": role,
            "requested_components": components,
            "source_content": None,
            "generated_components": [],
            "validated_components": [],
            "failed_components": [],
            "package_meta": None,
            "error": None,
            "_llm": self.llm,
            "_validator": self.validator,
            "_concurrency": self.concurrency,
        }

        final_state = await self.workflow.ainvoke(initial_state)
        return final_state["package_meta"], final_state["validated_components"]
