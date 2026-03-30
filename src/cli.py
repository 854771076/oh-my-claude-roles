import asyncio
from pathlib import Path
from typing import Optional

import questionary
import typer
from rich.console import Console
from rich.prompt import Confirm
from rich.table import Table

from src.services.llm.factory import create_llm
from src.services.llm.role_design.cli_chat import run_interactive

from . import __version__
from .config import settings
from .exceptions import OhRolesError
from .generator import ToolGenerator
from .installer import ToolInstaller
from .logger import setup_logger
from .packager import PackageCache
from .scanner import RoleScanner

app = typer.Typer(
    name="oh-roles",
    help="Claude Code 角色工具包管理器 - 一键安装角色规范到你的项目",
    add_completion=False,
)
console = Console()


def version_callback(value: bool):
    if value:
        console.print(f"Oh-My-Claude-Roles version: {__version__}")
        raise typer.Exit()


@app.command(name="install")
def install(
    role_name: Optional[str] = typer.Argument(
        None, help="角色名称，如 backend/python"
    ),
    target: str = typer.Option(".", "--target", "-t", help="目标项目路径"),
    dry_run: bool = typer.Option(False, "--dry-run", help="预览模式，不实际写入"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="详细输出"),
    quiet: bool = typer.Option(False, "--quiet", "-q", help="静默模式"),
):
    """安装角色工具包到目标项目"""
    setup_logger(verbose)

    # Scan all roles
    scanner = RoleScanner()
    all_roles = scanner.scan_all()

    if not all_roles:
        console.print("[red]错误: 未找到任何角色文档，请检查 roles/ 目录[/red]")
        raise typer.Exit(1)

    # Select role
    if not role_name:
        choices = [
            (
                f"{r.category}/{r.name}",
                f"{r.category}/{r.name} - {r.display_name}"
            )
            for r in all_roles
        ]
        role_choice = questionary.select(
            "选择要安装的角色:",
            choices=[c[1] for c in choices],
        ).ask()
        if not role_choice:
            raise typer.Exit(0)
        role_name = next(c[0] for c in choices if c[1] == role_choice)

    # Find role
    role = next(
        (r for r in all_roles if f"{r.category}/{r.name}" == role_name),
        None,
    )
    if not role:
        console.print(f"[red]错误: 角色 {role_name} 不存在[/red]")
        raise typer.Exit(1)

    # Select components
    component_choices = [
        ("CLAUDE.md", "claude_md", "项目指令文件", True),
        ("Hooks", "hooks", "钩子脚本", True),
        ("Commands", "commands", "斜杠命令", True),
        ("Agents", "agents", "子代理配置", True),
        ("Rules", "rules", "规则文件", True),
        ("Skills", "skills", "技能文件", True),
    ]
    selected_components = questionary.checkbox(
        "选择要安装的工具包类型 (空格选择，回车确认):",
        choices=[
            questionary.Choice(title, value, checked=checked)
            for title, value, _, checked in component_choices
        ],
    ).ask()
    if not selected_components:
        selected_components = settings.default_components

    # Check cache
    cache = PackageCache()
    cached = cache.get(role)

    use_cache = False
    components_to_install = None

    if cached and cache.is_latest(role):
        use_cache = Confirm.ask(
            (
                "✅ 发现已缓存的工具包 ("
                f"{cached['meta'].generated_at.strftime('%Y-%m-%d %H:%M')}"
                ")，是否使用?"
            ),
            default=True,
        )
        if use_cache:
            components_to_install = cached["components"]

    if not use_cache or not components_to_install:
        # Need to generate
        try:
            generator = ToolGenerator()
        except OhRolesError as e:
            console.print(f"[red]错误: {e.message}[/red]")
            console.print("💡 请配置环境变量 OH_ROLES_LLM_API_KEY")
            raise typer.Exit(1)

        with console.status("[bold green]正在生成工具包...[/bold green]"):
            try:
                meta, components_to_install = asyncio.run(
                    generator.generate_package(role, selected_components)
                )
                cache.save(meta, components_to_install)
            except OhRolesError as e:
                console.print(f"[red]生成失败: {e.message}[/red]")
                raise typer.Exit(1)

    if not components_to_install:
        console.print("[red]错误: 没有生成任何组件[/red]")
        raise typer.Exit(1)

    # Detect conflicts
    installer = ToolInstaller(target)
    conflicts = installer.detect_conflicts(components_to_install)

    conflict_strategy = "ask"
    if conflicts:
        console.print("[yellow]⚠ 检测到文件冲突:[/yellow]")
        for c in conflicts:
            console.print(f"  - .claude/{c.target_path}")

        strategy_choice = questionary.select(
            "如何处理冲突?",
            choices=[
                questionary.Choice("覆盖替换", "overwrite"),
                questionary.Choice("跳过保留", "skip"),
                questionary.Choice("取消安装", "cancel"),
            ],
        ).ask()

        if strategy_choice == "cancel":
            console.print("安装已取消")
            raise typer.Exit(0)

        conflict_strategy = strategy_choice
    else:
        conflict_strategy = "overwrite"

    # Install
    try:
        result = installer.install(
            components_to_install,
            conflict_strategy=conflict_strategy,
            dry_run=dry_run,
        )
    except OhRolesError as e:
        console.print(f"[red]安装失败: {e.message}[/red]")
        raise typer.Exit(1)

    if dry_run:
        console.print("[green]✅ 预览完成，没有写入任何文件[/green]")
    else:
        console.print("[green]✅ 安装完成！[/green]")

    console.print(f"  目标目录: {result['target_dir']}")
    console.print(f"  已安装: {len(result['installed'])} 个组件")
    if result["skipped"]:
        console.print(f"  已跳过: {len(result['skipped'])} 个组件")


@app.command(name="generate")
def generate(
    role_name: str = typer.Argument(..., help="角色名称，如 backend/python"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="详细输出"),
):
    """强制重新生成并打包角色工具包，不安装"""
    setup_logger(verbose)
    scanner = RoleScanner()
    all_roles = scanner.scan_all()
    role = next(
        (r for r in all_roles if f"{r.category}/{r.name}" == role_name),
        None,
    )
    if not role:
        console.print(f"[red]错误: 角色 {role_name} 不存在[/red]")
        raise typer.Exit(1)

    try:
        generator = ToolGenerator()
    except OhRolesError as e:
        console.print(f"[red]错误: {e.message}[/red]")
        raise typer.Exit(1)

    with console.status("[bold green]正在生成工具包...[/bold green]"):
        try:
            meta, components = asyncio.run(generator.generate_package(role))
            cache = PackageCache()
            cache.save(meta, components)
        except OhRolesError as e:
            console.print(f"[red]生成失败: {e.message}[/red]")
            raise typer.Exit(1)

    console.print("[green]✅ 生成完成，缓存已保存[/green]")
    console.print(f"  角色: {role.display_name}")
    console.print(f"  组件: {len(components)} 个")


@app.command(name="list")
def list_roles(
    cached: bool = typer.Option(False, "--cached", help="只列出已缓存的角色"),
    installed: bool = typer.Option(False, "--installed", help="只列出已安装的角色"),
):
    """列出所有可用角色"""
    setup_logger()

    if cached:
        cache = PackageCache()
        cached_roles = cache.list_cached()
        if not cached_roles:
            console.print("没有已缓存的角色")
            return
        table = Table(title="已缓存的角色")
        table.add_column("名称", style="cyan")
        table.add_column("分类")
        table.add_column("描述")
        table.add_column("版本")
        for r in cached_roles:
            table.add_row(
                f"{r.category}/{r.name}",
                r.category,
                r.description[:50] + (
                    "..." if len(r.description) > 50 else ""
                ),
                r.version,
            )
        console.print(table)
        return

    scanner = RoleScanner()
    all_roles = scanner.scan_all()
    if not all_roles:
        console.print("没有找到任何角色")
        return

    table = Table(title="可用角色列表")
    table.add_column("名称", style="cyan")
    table.add_column("显示名称")
    table.add_column("描述")
    table.add_column("标签")
    for r in all_roles:
        table.add_row(
            f"{r.category}/{r.name}",
            r.display_name,
            r.description[:40] + ("..." if len(r.description) > 40 else ""),
            ", ".join(r.tags),
        )
    console.print(table)


@app.command(name="uninstall")
def uninstall(
    role_name: str = typer.Argument(..., help="角色名称，如 backend/python"),
    target: str = typer.Option(".", "--target", "-t", help="目标项目路径"),
):
    """卸载已安装的角色工具包"""
    setup_logger()
    # TODO: 需要跟踪已安装的信息才能卸载
    console.print("[yellow]警告: 卸载功能尚未实现[/yellow]")
    raise typer.Exit(1)


@app.command(name="config")
def show_config():
    """显示当前配置"""
    setup_logger()
    table = Table(title="当前配置")
    table.add_column("配置项", style="cyan")
    table.add_column("值")
    table.add_row("LLM Provider", settings.llm_provider)
    table.add_row("LLM Model", settings.llm_model)
    table.add_row(
        "API Key", "已配置" if settings.llm_api_key else "[red]未配置[/red]"
    )
    table.add_row("Timeout", f"{settings.llm_timeout}s")
    table.add_row("Max Retries", str(settings.llm_max_retries))
    table.add_row("Concurrency", str(settings.llm_concurrency))
    table.add_row("Roles Dir", settings.roles_dir)
    table.add_row("Packages Dir", settings.packages_dir)
    console.print(table)


@app.command(name="clean")
def clean(
    role_name: Optional[str] = typer.Argument(None, help="要清理缓存的角色"),
):
    """清理缓存"""
    setup_logger()
    cache = PackageCache()
    if role_name:
        count = cache.clean(role_name)
        console.print(f"✅ 已清理缓存: {count} 个角色")
    else:
        count = cache.clean()
        console.print(f"✅ 已清理全部缓存: {count} 个目录")


@app.command(name="version")
def show_version():
    """显示版本信息"""
    console.print(f"Oh-My-Claude-Roles v{__version__}")


@app.command()
def create(
    output: Optional[Path] = None,
    verbose: bool = typer.Option(False, "--verbose", "-v", help="详细输出"),
):
    """Create a new role document interactively with AI guidance.

    Starts an interactive conversation that guides you through designing
    a complete role specification document, and saves the final result.
    """
    setup_logger(verbose)
    llm = create_llm()
    output_path = str(output) if output else None
    run_interactive(llm, output_path)


def main():
    app()


if __name__ == "__main__":
    main()
