from pathlib import Path
import os
from typing import Optional, Union

# Import custom modules after fixing the related issues
# from utils.style import color_green
# from utils.ignore import IgnoreMatcher

def update_file(path: str, new_content: Union[str, bytes], project: Optional[str] = None):
    """
    Update file with the new content.

    :param path: Full path to the file
    :param new_content: New content to write to the file
    :param project: Optional; a Project object related to the file update. Default is None.

    Any intermediate directories will be created if they don't exist.
    If file is text, it will be written using UTF-8 encoding.
    """
    # Create the enclosing directory if it does not exist
    os.makedirs(os.path.dirname(path), exist_ok=True)

    file_mode = "w" if isinstance(new_content, str) else "wb"
    encoding = "utf-8" if isinstance(new_content, str) else None

    with open(path, file_mode, encoding=encoding) as file:
        file.write(new_content)

        if project is not None:  # project can be None only in tests
            # ... (project-related functionality)

def get_file_contents(
    path: str, project_root_path: str
) -> dict[str, Union[str, bytes]]:
    """
    Get file content and metadata.

    :param path: Full path to the file
    :param project_root_path: Full path to the project root directory
    :return: Object with the following keys:
        - name: File name
        - path: Relative path to the file
        - content: File content (str or bytes)
        - full_path: Full path to the file

    If file is text, it will be read using UTF-8 encoding and `content`
    will be a Python string. If that fails, it will be treated as a
    binary file and `content` will be a Python bytes object.
    """
    full_path = Path(path).absolute().resolve()

    try:
        # Assume it's a text file using UTF-8 encoding
        file_content = full_path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        # If that fails, we'll treat it as a binary file
        file_content = full_path.read_bytes()
    except FileNotFoundError:
        raise ValueError(f"File not found: {full_path}")
    except Exception as e:
        raise ValueError(f"Exception in get_file_contents: {e}")

    file_name = full_path.name
    relative_path = full_path.relative_to(project_root_path)

    return {
        "name": file_name,
        "path": str(relative_path),
        "content": file_content,
        "full_path": str(full_path),
        "lines_of_code": len(file_content.splitlines()),
    }


def get_directory_contents(
    directory: str,
    ignore: Optional[list[str]] = None
) -> list[dict[str, Union[str, bytes]]]:
    """
    Get the content of all files in the given directory.

    :param directory: Full path to the directory to search
    :param ignore: List of files or folders to ignore (optional)
    :return: List of file objects as returned by `get_file_contents`

    See `get_file_contents()` for the details on the output structure
    and how files are read.
    """
    return_array = []

    # Use pathlib.Path.glob() instead of os.walk()
    for file_path in Path(directory).glob("*"):
        if file_path.is_file():
            if ignore and file_path.name in ignore:
                continue
            return_array.append(get_file_contents(str(file_path), directory))

    return return_array


def clear_directory(directory: str, ignore: Optional[list[str]] = None):
    """
    Delete all files and directories (except ignored ones) in the given directory.

    :param dir_path: Full path to the directory to clear
    :param ignore: List of files or folders to ignore (optional)
    """
    for file_path in Path(directory).glob("*"):
        if file_path.is_file():
            if ignore and file_path.name in ignore:
                continue
            try:
                file_path.unlink()
            except Exception:  # noqa
                pass
        elif file_path.is_dir():
            if ignore and file_path.name in ignore:
                continue
            try:
                if not list(file_path.glob("*")):
                    file_path.rmdir()
            except Exception:  # noqa
                pass
