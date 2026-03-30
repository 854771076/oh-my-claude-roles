import json
from pathlib import Path
from typing import Dict, List, Optional

from loguru import logger

from .config import settings
from .exceptions import CacheCorruptedError
from .models import PackageMeta, RoleMeta, ToolComponent


class PackageCache:
    """Manage cached tool packages"""

    def __init__(self, packages_dir: str | None = None):
        # User packages directory (primary)
        self.user_packages_dir = settings.user_packages_dir
        self.user_packages_dir.mkdir(parents=True, exist_ok=True)

        # Current directory packages (secondary)
        self.packages_dir = Path(packages_dir or settings.packages_dir).resolve()
        self.packages_dir.mkdir(parents=True, exist_ok=True)

    def get(self, role: RoleMeta) -> Optional[Dict]:
        """Get cached package if exists.
        First checks user directory, then falls back to current directory.
        Falls back to legacy unversioned directory if versioned doesn't exist.
        """
        # Check user directory first
        user_cache_dir = self._get_cache_dir(role, self.user_packages_dir)
        meta_file = user_cache_dir / "meta.json"

        if not meta_file.exists():
            # Fallback to legacy unversioned path in user directory
            legacy_user_cache_dir = self.user_packages_dir / role.category / role.name
            legacy_meta_file = legacy_user_cache_dir / "meta.json"
            if legacy_meta_file.exists():
                user_cache_dir = legacy_user_cache_dir
                meta_file = legacy_meta_file
            else:
                # Check current directory
                current_cache_dir = self._get_cache_dir(role, self.packages_dir)
                meta_file = current_cache_dir / "meta.json"

                if not meta_file.exists():
                    # Fallback to legacy unversioned path in current directory
                    legacy_current_cache_dir = self.packages_dir / role.category / role.name
                    legacy_meta_file = legacy_current_cache_dir / "meta.json"
                    if legacy_meta_file.exists():
                        current_cache_dir = legacy_current_cache_dir
                        meta_file = legacy_meta_file
                    else:
                        logger.debug(f"No cached package found for {role.name}")
                        return None
                else:
                    user_cache_dir = current_cache_dir

        logger.debug(f"Loading cached package from: {user_cache_dir}")
        try:
            meta_data = json.loads(meta_file.read_text(encoding="utf-8"))
            meta = PackageMeta(**meta_data)

            # Load all components
            components: List[ToolComponent] = []
            for comp_type in meta.components:
                if comp_type == "claude_md":
                    # claude_md is directly at cache_dir/CLAUDE.md
                    claude_file = user_cache_dir / "CLAUDE.md"
                    if claude_file.exists():
                        components.append(ToolComponent(
                            type=comp_type,
                            content=claude_file.read_text(encoding="utf-8"),
                            filename="CLAUDE.md",
                            target_path=self._get_target_path(comp_type, "CLAUDE.md"),
                        ))
                else:
                    # Other types are in their type subdirectory
                    comp_dir = user_cache_dir / comp_type
                    if comp_dir.exists():
                        for f in comp_dir.iterdir():
                            if f.is_file():
                                components.append(ToolComponent(
                                    type=comp_type,
                                    content=f.read_text(encoding="utf-8"),
                                    filename=f.name,
                                    target_path=self._get_target_path(
                                        comp_type, f.name
                                    ),
                                ))

            logger.debug(f"Loaded cached package: {len(components)} component(s)")
            return {"meta": meta, "components": components}
        except Exception as e:
            logger.error(f"Cache load failed: {e}")
            raise CacheCorruptedError(f"Cache corrupted for {role.name}: {e}")

    def save(self, meta: PackageMeta, components: List[ToolComponent]) -> None:
        """Save generated package to cache (default: user directory)"""
        cache_dir = self._get_cache_dir(meta.role, self.user_packages_dir)
        logger.info(f"Saving package to cache: {cache_dir}")
        cache_dir.mkdir(parents=True, exist_ok=True)

        # Save metadata
        meta_file = cache_dir / "meta.json"
        meta_file.write_text(meta.model_dump_json(indent=2), encoding="utf-8")
        logger.debug(f"Saved metadata: {meta_file}")

        # Save each component by type directory
        for comp in components:
            # comp.target_path already includes type subdirectory
            # like "hooks/filename.json"
            comp_file = cache_dir / comp.target_path
            comp_file.parent.mkdir(parents=True, exist_ok=True)
            comp_file.write_text(comp.content, encoding="utf-8")
            logger.debug(
                f"Saved component: {comp_file}"
            )

        logger.success(
            f"Package cached successfully: {len(components)} component(s) saved"
        )

    def is_latest(self, role: RoleMeta) -> bool:
        """Check if cached version is latest (source hash matches)"""
        cached = self.get(role)
        if not cached:
            return False
        return cached["meta"].role.source_hash == role.source_hash

    def clean(self, role_name: str | None = None) -> int:
        """Clean cache. If role_name given, clean only that role."""
        cleaned = 0

        if role_name:
            parts = role_name.split("/")
            if len(parts) == 2:
                category, name = parts
                # Clean user directory
                user_role_dir = self.user_packages_dir / category / name
                if user_role_dir.exists():
                    import shutil
                    shutil.rmtree(user_role_dir)
                    cleaned += 1

                # Clean current directory
                current_role_dir = self.packages_dir / category / name
                if current_role_dir.exists():
                    import shutil
                    shutil.rmtree(current_role_dir)
                    cleaned += 1
            return cleaned
        else:
            # Clean all
            import shutil

            # Clean user directory
            user_count = sum(1 for _ in self.user_packages_dir.iterdir() if _.is_dir())
            for item in self.user_packages_dir.iterdir():
                if item.is_dir():
                    shutil.rmtree(item)
            self.user_packages_dir.mkdir(parents=True, exist_ok=True)

            # Clean current directory
            current_count = sum(1 for _ in self.packages_dir.iterdir() if _.is_dir())
            for item in self.packages_dir.iterdir():
                if item.is_dir():
                    shutil.rmtree(item)
            self.packages_dir.mkdir(parents=True, exist_ok=True)

            return user_count + current_count

    def list_cached(self) -> List[RoleMeta]:
        """List all cached roles from both user directory and current directory"""
        roles: List[RoleMeta] = []

        # Scan user directory
        user_roles = self._list_cached_in_directory(self.user_packages_dir)
        roles.extend(user_roles)

        # Scan current directory
        current_roles = self._list_cached_in_directory(self.packages_dir)

        # Merge current roles, replacing duplicates from user directory
        role_map = {f"{r.category}/{r.name}": r for r in roles}
        for role in current_roles:
            key = f"{role.category}/{role.name}"
            role_map[key] = role

        return list(role_map.values())

    def _list_cached_in_directory(self, directory: Path) -> List[RoleMeta]:
        """List cached roles in a single directory"""
        roles: List[RoleMeta] = []
        for category_dir in directory.iterdir():
            if not category_dir.is_dir():
                continue
            for role_dir in category_dir.iterdir():
                if not role_dir.is_dir():
                    continue
                # Check for versioned layout: role_dir/vX.X.X/meta.json
                found = False
                for version_dir in role_dir.iterdir():
                    if not version_dir.is_dir():
                        continue
                    meta_file = version_dir / "meta.json"
                    if meta_file.exists():
                        try:
                            data = json.loads(meta_file.read_text())
                            roles.append(RoleMeta(**data["role"]))
                        except Exception:
                            continue
                        found = True
                if not found:
                    # Legacy unversioned layout
                    meta_file = role_dir / "meta.json"
                    if meta_file.exists():
                        try:
                            data = json.loads(meta_file.read_text())
                            roles.append(RoleMeta(**data["role"]))
                        except Exception:
                            continue
        return roles

    def _get_cache_dir(self, role: RoleMeta, base_dir: Path | None = None) -> Path:
        """Get cache directory for role, includes version."""
        if base_dir is None:
            base_dir = self.packages_dir
        return base_dir / role.category / role.name / f"v{role.version}"

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
