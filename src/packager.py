import json
from pathlib import Path
from typing import List, Dict, Optional
from .config import settings
from .models import RoleMeta, PackageMeta, ToolComponent
from .exceptions import CacheCorruptedError


class PackageCache:
    """Manage cached tool packages"""

    def __init__(self, packages_dir: str | None = None):
        self.packages_dir = Path(packages_dir or settings.packages_dir).resolve()
        self.packages_dir.mkdir(parents=True, exist_ok=True)

    def get(self, role: RoleMeta) -> Optional[Dict]:
        """Get cached package if exists"""
        cache_dir = self._get_cache_dir(role)
        meta_file = cache_dir / "meta.json"

        if not meta_file.exists():
            return None

        try:
            meta_data = json.loads(meta_file.read_text(encoding="utf-8"))
            meta = PackageMeta(**meta_data)

            # Load all components
            components: List[ToolComponent] = []
            for comp_type in meta.components:
                comp_dir = cache_dir / comp_type
                if comp_dir.exists():
                    for f in comp_dir.iterdir():
                        if f.is_file():
                            components.append(ToolComponent(
                                type=comp_type,
                                content=f.read_text(encoding="utf-8"),
                                filename=f.name,
                                target_path=self._get_target_path(comp_type, f.name),
                            ))

            return {"meta": meta, "components": components}
        except Exception as e:
            raise CacheCorruptedError(f"Cache corrupted for {role.name}: {e}")

    def save(self, meta: PackageMeta, components: List[ToolComponent]) -> None:
        """Save generated package to cache"""
        cache_dir = self._get_cache_dir(meta.role)
        cache_dir.mkdir(parents=True, exist_ok=True)

        # Save metadata
        meta_file = cache_dir / "meta.json"
        meta_file.write_text(meta.model_dump_json(indent=2), encoding="utf-8")

        # Save each component by type directory
        for comp in components:
            comp_dir = cache_dir / comp.type
            comp_dir.mkdir(parents=True, exist_ok=True)
            comp_file = comp_dir / comp.filename
            comp_file.write_text(comp.content, encoding="utf-8")

    def is_latest(self, role: RoleMeta) -> bool:
        """Check if cached version is latest (source hash matches)"""
        cached = self.get(role)
        if not cached:
            return False
        return cached["meta"].role.source_hash == role.source_hash

    def clean(self, role_name: str | None = None) -> int:
        """Clean cache. If role_name given, clean only that role."""
        if role_name:
            parts = role_name.split("/")
            if len(parts) == 2:
                cache_dir = self.packages_dir / parts[0] / parts[1]
                if cache_dir.exists():
                    import shutil
                    shutil.rmtree(cache_dir)
                    return 1
            return 0
        else:
            # Clean all
            import shutil
            count = sum(1 for _ in self.packages_dir.iterdir() if _.is_dir())
            for item in self.packages_dir.iterdir():
                if item.is_dir():
                    shutil.rmtree(item)
            self.packages_dir.mkdir(parents=True, exist_ok=True)
            return count

    def list_cached(self) -> List[RoleMeta]:
        """List all cached roles"""
        roles: List[RoleMeta] = []
        for category_dir in self.packages_dir.iterdir():
            if not category_dir.is_dir():
                continue
            for role_dir in category_dir.iterdir():
                if not role_dir.is_dir():
                    continue
                meta_file = role_dir / "meta.json"
                if meta_file.exists():
                    try:
                        data = json.loads(meta_file.read_text())
                        roles.append(data["role"])
                    except Exception:
                        continue
        return roles

    def _get_cache_dir(self, role: RoleMeta) -> Path:
        """Get cache directory for role"""
        return self.packages_dir / role.category / role.name

    def _get_target_path(self, comp_type: str, filename: str) -> str:
        """Get target installation path in cache"""
        path_map = {
            "claude_md": "CLAUDE.md",
            "hooks": f"hooks/{filename}",
            "commands": f"commands/{filename}",
            "agents": f"agents/{filename}",
            "rules": f"rules/{filename}",
            "skills": f"skills/{filename}",
        }
        return path_map.get(comp_type, filename)
