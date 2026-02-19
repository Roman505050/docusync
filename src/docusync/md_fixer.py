"""Markdown/MDX file fixer for Docusaurus compatibility."""

from pathlib import Path
from typing import List, Optional, Tuple

from docusync.exceptions import FileOperationError
from docusync.fixers import Fixer, get_all_fixers
from docusync.logger import USER_LOG


class MarkdownFixer:
    """Fixes common MDX/Markdown issues that cause Docusaurus build failures."""

    def __init__(self, fixers: Optional[List[Fixer]] = None) -> None:
        """Initialize the markdown fixer.

        :param fixers: Optional list of fixers to use. If None, uses all available fixers.
        """
        self.fixers = fixers if fixers is not None else get_all_fixers()
        self.fixes_applied: List[Tuple[str, int]] = []

    def fix_file(self, file_path: Path, dry_run: bool = False) -> bool:
        """Fix MDX/Markdown issues in a file.

        :param file_path: Path to the markdown file
        :param dry_run: If True, only report issues without fixing
        :returns: True if fixes were applied or would be applied
        :raises FileOperationError: If file cannot be read or written
        """
        if not file_path.exists():
            raise FileOperationError(f"File does not exist: {file_path}")

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
        except OSError as e:
            raise FileOperationError(f"Failed to read {file_path}: {e}") from e

        original_content = content
        self.fixes_applied = []

        # Apply all fixes dynamically
        for fixer in self.fixers:
            content, fix_count = fixer.fix(content)
            if fix_count > 0:
                self.fixes_applied.append((fixer.name, fix_count))

        if content != original_content:
            if not dry_run:
                try:
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write(content)
                    USER_LOG.success(f"Fixed {file_path}")
                    for fix_name, count in self.fixes_applied:
                        USER_LOG.info(f"  • {fix_name}: {count} fixes")
                except OSError as e:
                    raise FileOperationError(
                        f"Failed to write {file_path}: {e}"
                    ) from e
            else:
                USER_LOG.info(f"Would fix {file_path}")
                for fix_name, count in self.fixes_applied:
                    USER_LOG.info(f"  • {fix_name}: {count} fixes")
            return True

        return False

    def fix_directory(
        self, directory: Path, dry_run: bool = False, recursive: bool = True
    ) -> int:
        """Fix all markdown files in a directory.

        :param directory: Directory to scan
        :param dry_run: If True, only report issues without fixing
        :param recursive: If True, scan subdirectories recursively
        :returns: Number of files fixed
        :raises FileOperationError: If directory doesn't exist
        """
        if not directory.exists():
            raise FileOperationError(f"Directory does not exist: {directory}")

        if not directory.is_dir():
            raise FileOperationError(f"Not a directory: {directory}")

        pattern = "**/*.md" if recursive else "*.md"
        md_files = list(directory.glob(pattern))

        if not md_files:
            USER_LOG.warning(f"No markdown files found in {directory}")
            return 0

        USER_LOG.info(
            f"Scanning {len(md_files)} markdown files in {directory}..."
        )

        fixed_count = 0
        for md_file in md_files:
            try:
                if self.fix_file(md_file, dry_run=dry_run):
                    fixed_count += 1
            except FileOperationError as e:
                USER_LOG.error(f"Error processing {md_file}: {e}")

        return fixed_count
