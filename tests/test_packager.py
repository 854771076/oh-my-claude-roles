import tempfile
from datetime import datetime
from pathlib import Path

from src.models import PackageMeta, RoleMeta, ToolComponent
from src.packager import PackageCache


def test_save_and_get():
    with tempfile.TemporaryDirectory() as tmpdir:
        cache = PackageCache(packages_dir=tmpdir)
        role = RoleMeta(
            name="python",
            category="backend",
            display_name="Python",
            description="Python",
            source_path="test.md",
            source_hash="abc123",
        )
        meta = PackageMeta(
            role=role,
            version="1.0.0",
            generated_at=datetime.now(),
            llm_provider="openai",
            llm_model="gpt-4o",
            components=["claude_md"],
        )
        components = [
            ToolComponent(
                type="claude_md",
                content="# Test",
                filename="CLAUDE.md",
                target_path="CLAUDE.md",
            )
        ]
        cache.save(meta, components)

        cached = cache.get(role)
        assert cached is not None
        assert cached["meta"].role.name == "python"
        assert len(cached["components"]) == 1
        assert cached["components"][0].content == "# Test"


def test_is_latest():
    with tempfile.TemporaryDirectory() as tmpdir:
        cache = PackageCache(packages_dir=tmpdir)
        assert cache is not None


def test_versioned_cache_save_and_get():
    """Test that different versions are stored in different directories."""
    with tempfile.TemporaryDirectory() as tmpdir:
        cache = PackageCache(packages_dir=tmpdir)

        # Version 1.0.0
        role_v1 = RoleMeta(
            name="python",
            category="backend",
            display_name="Python",
            description="Python",
            source_path="test.md",
            source_hash="abc123",
            version="1.0.0",
        )
        meta_v1 = PackageMeta(
            role=role_v1,
            version="1.0.0",
            generated_at=datetime.now(),
            llm_provider="openai",
            llm_model="gpt-4o",
            components=["claude_md"],
        )
        components_v1 = [
            ToolComponent(
                type="claude_md",
                content="# Version 1.0.0",
                filename="CLAUDE.md",
                target_path="CLAUDE.md",
            )
        ]
        cache.save(meta_v1, components_v1)

        # Version 2.0.0
        role_v2 = RoleMeta(
            name="python",
            category="backend",
            display_name="Python",
            description="Python",
            source_path="test.md",
            source_hash="def456",
            version="2.0.0",
        )
        meta_v2 = PackageMeta(
            role=role_v2,
            version="2.0.0",
            generated_at=datetime.now(),
            llm_provider="openai",
            llm_model="gpt-4o",
            components=["claude_md"],
        )
        components_v2 = [
            ToolComponent(
                type="claude_md",
                content="# Version 2.0.0",
                filename="CLAUDE.md",
                target_path="CLAUDE.md",
            )
        ]
        cache.save(meta_v2, components_v2)

        # Both versions should exist
        cached_v1 = cache.get(role_v1)
        cached_v2 = cache.get(role_v2)

        assert cached_v1 is not None
        assert cached_v2 is not None
        assert "# Version 1.0.0" in cached_v1["components"][0].content
        assert "# Version 2.0.0" in cached_v2["components"][0].content
        assert cached_v1["meta"].version == "1.0.0"
        assert cached_v2["meta"].version == "2.0.0"


def test_list_cached_includes_both_versioned_and_legacy():
    """Test that list_cached finds both versioned and legacy caches."""

    with tempfile.TemporaryDirectory() as tmpdir:
        cache = PackageCache(packages_dir=tmpdir)

        # Create a versioned cache
        role_v1 = RoleMeta(
            name="python",
            category="backend",
            display_name="Python",
            description="Python",
            source_path="test.md",
            source_hash="abc123",
            version="1.0.0",
        )
        meta_v1 = PackageMeta(
            role=role_v1,
            version="1.0.0",
            generated_at=datetime.now(),
            llm_provider="openai",
            llm_model="gpt-4o",
            components=["claude_md"],
        )
        components_v1 = [
            ToolComponent(
                type="claude_md",
                content="# Version 1.0.0",
                filename="CLAUDE.md",
                target_path="CLAUDE.md",
            )
        ]
        cache.save(meta_v1, components_v1)

        # Manually create a legacy cache for another role
        legacy_dir = Path(tmpdir) / "frontend" / "javascript"
        legacy_dir.mkdir(parents=True, exist_ok=True)

        legacy_role = RoleMeta(
            name="javascript",
            category="frontend",
            display_name="JavaScript",
            description="JS",
            source_path="test.md",
            source_hash="legacy456",
            version="1.0.0",
        )
        legacy_meta = PackageMeta(
            role=legacy_role,
            version="1.0.0",
            generated_at=datetime.now(),
            llm_provider="openai",
            llm_model="gpt-4",
            components=["claude_md"],
        )

        meta_file = legacy_dir / "meta.json"
        meta_file.write_text(legacy_meta.model_dump_json(indent=2), encoding="utf-8")

        # List cached roles
        cached_roles = cache.list_cached()
        role_names = {r.name for r in cached_roles}

        assert "python" in role_names
        assert "javascript" in role_names
        assert len(cached_roles) == 2
