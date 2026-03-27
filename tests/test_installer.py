import tempfile
from pathlib import Path
from src.installer import ToolInstaller
from src.models import ToolComponent


def test_detect_conflicts(tmp_path):
    installer = ToolInstaller(target_path=str(tmp_path))
    (installer.claude_dir / "hooks").mkdir(parents=True)
    (installer.claude_dir / "hooks" / "test.json").write_text("existing")

    components = [
        ToolComponent(
            type="hooks",
            content="new content",
            filename="test.json",
            target_path="hooks/test.json",
        ),
        ToolComponent(
            type="claude_md",
            content="new",
            filename="CLAUDE.md",
            target_path="CLAUDE.md",
        ),
    ]
    conflicts = installer.detect_conflicts(components)
    assert len(conflicts) == 1
    assert conflicts[0].filename == "test.json"


def test_install_skip_conflict(tmp_path):
    installer = ToolInstaller(target_path=str(tmp_path))
    (installer.claude_dir / "hooks").mkdir(parents=True)
    existing_file = installer.claude_dir / "hooks" / "test.json"
    existing_file.write_text("existing")

    components = [
        ToolComponent(
            type="hooks",
            content="new content",
            filename="test.json",
            target_path="hooks/test.json",
        ),
    ]
    result = installer.install(components, conflict_strategy="skip")
    assert len(result["installed"]) == 0
    assert len(result["skipped"]) == 1
    assert existing_file.read_text() == "existing"
