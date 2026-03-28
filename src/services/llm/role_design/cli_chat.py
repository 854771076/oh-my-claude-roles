import asyncio
from pathlib import Path
from typing import Optional
from langchain_core.language_models.chat_models import BaseChatModel
from rich.console import Console
from rich.markdown import Markdown
from .state import RoleDesignState
from .nodes import load_prompt
from .graph import create_role_design_graph


console = Console()


class CLIRoleDesignChat:
    """Interactive CLI chat for role design."""

    def __init__(self, llm: BaseChatModel):
        self.llm = llm
        self.graph = create_role_design_graph(llm)

    async def run(
        self,
        output_path: Optional[str] = None,
    ) -> Optional[str]:
        """Run the interactive chat session."""
        state = RoleDesignState()

        # Show welcome
        welcome = load_prompt("welcome.md")
        console.print(Markdown(welcome))

        while True:
            # Check if we're done
            if state.final_document is not None:
                break

            # Get next question
            current_step = state.current_step
            if current_step != "start" and current_step != "ask_name":
                # Generate question with LLM
                from .nodes import generate_question
                question = await generate_question(state, self.llm)
                console.print("\n" + question)

            # Get user input
            try:
                user_input = input("\n> ").strip()
            except (KeyboardInterrupt, EOFError):
                console.print("\n[yellow]Design cancelled.[/yellow]")
                return None

            if not user_input:
                continue

            # Update state with user input
            from .nodes import collect_user_input
            state = collect_user_input(state, user_input)

            # Already updated current_step in collect_user_input (from our previous fix)

            if state.current_step == "generate_final":
                console.print("\n[green]Generating final document...[/green]")
                from .nodes import generate_final_document
                final_doc = await generate_final_document(state, self.llm)
                state.final_document = final_doc
                break

        # Show final document preview
        console.print("\n[green]✅ Design complete! Final document:[/green]\n")
        preview = state.final_document[:500] + ("..." if len(state.final_document) > 500 else "")
        console.print(Markdown(preview))

        # Get output path if not provided
        if output_path is None:
            default_path = f"roles/{state.category}/{state.name}.md" if state.category else f"roles/{state.name}.md"
            console.print(f"\nWhere would you like to save this file? (default: {default_path})")
            try:
                user_input = input("> ").strip()
                output_path = user_input or default_path
            except (KeyboardInterrupt, EOFError):
                console.print("[yellow]Document not saved.[/yellow]")
                return state.final_document

        # Save the document
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(state.final_document, encoding="utf-8")
        console.print(f"\n[green]✅ Document saved to: {output_path}[/green]")

        return state.final_document


def run_interactive(
    llm: BaseChatModel,
    output_path: Optional[str] = None,
) -> Optional[str]:
    """Run interactive role design synchronously."""
    chat = CLIRoleDesignChat(llm)
    return asyncio.run(chat.run(output_path))
