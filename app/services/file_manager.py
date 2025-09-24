import os
import re
from pathlib import Path
from typing import List, Optional, Union


class FileManager:
    @staticmethod
    def get_folder_list(root_path: str) -> List[str]:
        return [f for f in os.listdir(root_path) if os.path.isdir(os.path.join(root_path, f))]

    @staticmethod
    def get_file_by_ext(directory: Union[str, Path], ext: str, latest: bool = False, recursive: bool = False, ) -> Union[
        List[Path], Optional[Path]]:
        directory = Path(directory)
        ext = ext.lower().lstrip(".")
        pattern = f"**/*.{ext}" if recursive else f"*.{ext}"
        files = [p for p in directory.glob(pattern) if p.is_file()]

        if not latest:
            return files

        def version_key(p: Path):
            # Extract trailing digits from the stem (name without extension)
            m = re.search(r"(\d+)$", p.stem)
            if m:
                # (is_unversioned, version) -> unversioned should sort last (latest)
                return (0, int(m.group(1)))
            else:
                # No number => treat as latest: rank higher than any numbered file
                return (1, float("inf"))

        if not files:
            return None
        # Pick the max by our custom key; unversioned wins, else highest number wins
        return max(files, key=version_key)
