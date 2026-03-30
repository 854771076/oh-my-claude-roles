from pathlib import Path

from src.scanner import RoleScanner

TEST_DIR = Path(__file__).parent / "data"


def test_scan_with_frontmatter():
    scanner = RoleScanner(roles_dir=str(TEST_DIR))
    roles = scanner.scan_all()
    # Should find at least one role
    assert any(r.name == "python" for r in roles)


def test_parse_frontmatter_extracts_correctly():
    scanner = RoleScanner()
    file_path = TEST_DIR / "test_role_with_frontmatter.md"
    role = scanner._parse_role(file_path, "test")
    assert role is not None
    assert role.name == "python"
    assert role.display_name == "Python企业级后端开发规范"
    assert "全异步" in role.description
    assert sorted(role.tags) == sorted(["python", "backend", "async", "fastapi"])
    assert role.version == "1.0.0"


def test_parse_without_frontmatter():
    scanner = RoleScanner()
    file_path = TEST_DIR / "test_role.md"
    role = scanner._parse_role(file_path, "test")
    assert role is not None
    assert role.name == "test_role"
    assert role.display_name == "Python后端开发规范"
    assert "Python后端开发规范的描述" in role.description
    assert role.tags == ["python", "backend"]


def test_hash_content():
    scanner = RoleScanner()
    content = "test content"
    hash_val = scanner._hash_content(content)
    assert len(hash_val) == 16  # first 16 chars of SHA256
