import hashlib
import re
from pathlib import Path
from typing import List, Optional

import frontmatter

from .config import settings
from .models import RoleMeta


class RoleScanner:
    """Scan roles directory and parse role documents"""

    def __init__(self, roles_dir: str | None = None):
        self.roles_dir = Path(roles_dir or settings.roles_dir).resolve()

    def scan_all(self) -> List[RoleMeta]:
        """Scan all roles in roles directory"""
        roles: List[RoleMeta] = []

        if not self.roles_dir.exists():
            return roles

        for category_dir in self.roles_dir.iterdir():
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
