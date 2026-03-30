from pathlib import Path
from typing import Dict, List

from .exceptions import InstallError
from .models import ToolComponent


class ToolInstaller:
    """Install tool package to target project .claude directory"""

    def __init__(self, target_path: str = "."):
        self.target = Path(target_path).resolve()
        self.claude_dir = self.target / ".claude"

    def detect_conflicts(self, components: List[ToolComponent]) -> List[ToolComponent]:
        """Detect which components have conflicting existing files"""
        conflicts: List[ToolComponent] = []
        for comp in components:
            target_file = self.claude_dir / comp.target_path
            if target_file.exists():
                conflicts.append(comp)
        return conflicts

    def install(
        self,
        components: List[ToolComponent],
        conflict_strategy: str = "ask",  # ask, overwrite, skip
        dry_run: bool = False,
    ) -> Dict:
        """Install components to .claude directory"""
        installed: List[ToolComponent] = []
        skipped: List[ToolComponent] = []

        for comp in components:
            target_file = self.claude_dir / comp.target_path

            if target_file.exists():
                if conflict_strategy == "skip":
                    skipped.append(comp)
                    continue
                # if 'ask', handled at CLI level before calling install

            if not dry_run:
                try:
                    target_file.parent.mkdir(parents=True, exist_ok=True)
                    target_file.write_text(comp.content, encoding="utf-8")
                    installed.append(comp)
                except Exception as e:
                    raise InstallError(f"Failed to write {target_file}: {e}")
            else:
                installed.append(comp)

        return {
            "installed": installed,
            "skipped": skipped,
            "target_dir": str(self.claude_dir),
        }

    def uninstall(self, components: List[ToolComponent]) -> Dict:
        """Uninstall components"""
        removed: List[ToolComponent] = []
        for comp in components:
            target_file = self.claude_dir / comp.target_path
            if target_file.exists():
                target_file.unlink()
                removed.append(comp)
                # Cleanup empty parent directory
                try:
                    target_file.parent.rmdir()
                except OSError:
                    # Directory not empty
                    pass
        return {"removed": removed}

    def backup(self, components: List[ToolComponent]) -> Dict[str, str]:
        """Backup existing files before overwrite"""
        backup: Dict[str, str] = {}
        for comp in components:
            target_file = self.claude_dir / comp.target_path
            if target_file.exists():
                backup[str(target_file)] = target_file.read_text(encoding="utf-8")
        return backup

    def rollback(self, backup: Dict[str, str]) -> None:
        """Rollback from backup after failed install"""
        for path_str, content in backup.items():
            path = Path(path_str)
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")
        # Remove any new files that were added during failed install
        # (simplified: just restore what existed before)
