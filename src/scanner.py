import hashlib
import re
from pathlib import Path
from typing import List, Optional

import frontmatter

from .config import settings
from .models import RoleMeta


class RoleScanner:
    """Scan roles directory and parse role documents"""

    def __init__(self, roles_dir: str | None = None, include_user_dir: bool = True):
        self.roles_dir = Path(roles_dir or settings.roles_dir).resolve()
        self.include_user_dir = include_user_dir

    def scan_all(self) -> List[RoleMeta]:
        """Scan all roles in multiple directories (user dir + current dir)"""
        roles: List[RoleMeta] = []

        # Scan user directory first
        if self.include_user_dir and settings.user_roles_dir.exists():
            user_roles = self._scan_directory(settings.user_roles_dir)
            roles.extend(user_roles)

        # Scan current directory
        current_roles = self._scan_directory(self.roles_dir)

        # Merge current roles, replacing duplicates from user directory
        role_map = {f"{r.category}/{r.name}": r for r in roles}
        for role in current_roles:
            key = f"{role.category}/{role.name}"
            role_map[key] = role

        return list(role_map.values())

    def _scan_directory(self, directory: Path) -> List[RoleMeta]:
        """Scan roles in a single directory"""
        roles: List[RoleMeta] = []

        if not directory.exists():
            return roles

        for category_dir in directory.iterdir():
            if not category_dir.is_dir() or category_dir.name.startswith("."):
                continue
            for doc_file in category_dir.glob("*.md"):
                role = self._parse_role(doc_file, category_dir.name)
                if role:
                    roles.append(role)

        return roles

    def _parse_role(self, file_path: Path, category: str) -> Optional[RoleMeta]:
        """Parse single role document from file"""
        try:
            content = file_path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            # Try GBK encoding
            try:
                content = file_path.read_text(encoding="gbk")
            except Exception:
                return None

        # Try parse YAML frontmatter
        post = frontmatter.loads(content)
        meta = post.metadata
        content_body = post.content

        if "name" in meta:
            # Has frontmatter
            return RoleMeta(
                name=meta.get("name", file_path.stem),
                category=category,
                display_name=meta.get("display_name", ""),
                description=meta.get("description", ""),
                source_path=str(file_path),
                source_hash=self._hash_content(content),
                tags=meta.get("tags", []),
                version=meta.get("version", "1.0.0"),
            )

        # Fallback: extract from content
        name = file_path.stem
        display_name = self._extract_title(content_body)
        description = self._extract_description(content_body)
        tags = self._extract_tags(content_body)

        return RoleMeta(
            name=name,
            category=category,
            display_name=display_name or name,
            description=description or "",
            source_path=str(file_path),
            source_hash=self._hash_content(content),
            tags=tags,
        )

    def _extract_title(self, content: str) -> str | None:
        """Extract title from first # heading"""
        for line in content.split("\n"):
            line = line.strip()
            if line.startswith("# "):
                return line[2:].strip()
        return None

    def _extract_description(self, content: str) -> str | None:
        """Extract description from first non-empty paragraph after title"""
        lines = content.split("\n")
        found_title = False
        for line in lines:
            line = line.strip()
            if line.startswith("# "):
                found_title = True
                continue
            if (
                found_title
                and line
                and not line.startswith("#")
                and not line.startswith("---")
            ):
                return line
        return None

    def _extract_tags(self, content: str) -> List[str]:
        """Extract tags from comment <!-- tags: a, b -->"""
        match = re.search(r"<!--\s*tags:\s*(.+?)\s*-->", content)
        if match:
            return [t.strip() for t in match.group(1).split(",") if t.strip()]
        return []

    def _hash_content(self, content: str) -> str:
        """Compute SHA256 hash, return first 16 characters"""
        return hashlib.sha256(content.encode("utf-8")).hexdigest()[:16]
