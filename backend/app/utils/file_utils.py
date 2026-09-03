import os
import shutil
from typing import List


def list_files_recursive(directory: str, extensions: List[str] = None) -> List[str]:
    file_list = []
    if not os.path.exists(directory):
        return file_list

    for root, _, files in os.walk(directory):
        for file in files:
            if extensions:
                if any(file.endswith(ext) for ext in extensions):
                    file_list.append(os.path.join(root, file))
            else:
                file_list.append(os.path.join(root, file))
    return file_list


def create_clean_directory(directory_path: str):
    if os.path.exists(directory_path):
        shutil.rmtree(directory_path)
    os.makedirs(directory_path, exist_ok=True)
