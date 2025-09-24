import os
import re
from pathlib import Path
from typing import List, Optional, Union
from collections import defaultdict


class FileManager:
    @staticmethod
    def get_folder_list(root_path: str) -> List[str]:
        return [f for f in os.listdir(root_path) if os.path.isdir(os.path.join(root_path, f))]

    @staticmethod
    def get_file_by_ext(directory: Union[str, Path], ext: str, latest: bool = False, recursive: bool = False, ) -> \
    Union[
        List[Path], Optional[Path]]:
        directory = Path(directory)
        ext = ext.lower().lstrip(".")
        pattern = f"**/*.{ext}" if recursive else f"*.{ext}"
        files = [p for p in directory.glob(pattern) if p.is_file()]

        if not latest:
            return sorted(files, key=lambda x: x.name)

        groups = defaultdict(list)
        for f in files:
            m = re.match(r"^(.*?)(\d+)?$", f.stem)
            if m:
                base, num = m.groups()
                version = int(num) if num else None
                groups[base].append((version, f))

        result = []
        for base, items in groups.items():
            no_num = [f for v, f in items if v is None]
            if no_num:
                result.append(no_num[0])  # unversioned wins
            else:
                latest_file = max(items, key=lambda x: x[0])[1]
                result.append(latest_file)

        return sorted(result, key=lambda x: x.name)

    @staticmethod
    def combine_paths(*args: str) -> Path:
        return Path(*args)
