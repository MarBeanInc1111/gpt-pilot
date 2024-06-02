import os
from pathlib import Path
from typing import Dict, List
from database.database import save_user_app

def get_parent_folder(folder_name: str) -> Path:
    """
    Returns the parent folder of the given folder name.
    """
    current_path = Path(os.path.abspath(__file__)).resolve()
    while current_path.name != folder_name:
        current_path = current_path.parent
    return current_path.parent

def setup_workspace(args: Dict[str, str]) -> Path:
    """
    Creates and returns the path to the project workspace.
    """
    workspace = args.get('workspace')
    root = args.get('root', get_parent_folder('pilot').as_posix())
    name = args.get('name', 'default_project_name')

    project_path = create_directory(os.path.join(root, 'workspace'), name)
    save_user_app(args.get('user_id'), args.get('app_id'), project_path.as_posix())

    print(f'Project folder name: {name}')
    return project_path

def create_directory(parent_directory: str, new_directory: str) -> Path:
    """
    Creates a new directory and returns its path.
    """
    new_directory_path = Path(os.path.join(parent_directory, new_directory))
    new_directory_path.mkdir(parents=True, exist_ok=True)
    return new_directory_path

def count_lines_of_code(files: List[Dict[str, str]]) -> int:
    """
    Returns the total number of lines of code in the given list of files.
    """
    return sum(len(file['content'].splitlines()) for file in files)
