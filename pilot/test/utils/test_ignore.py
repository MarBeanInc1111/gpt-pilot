import os
import pathlib
from typing import Any
from unittest.mock import create_autospec, patch

import pytest
from tempfile import TemporaryDirectory

from utils.ignore import IgnoreMatcher


@pytest.fixture
def matcher() -> IgnoreMatcher:
    """Create a reusable `IgnoreMatcher` instance."""
    return IgnoreMatcher(root_path=pathlib.Path("."))


@pytest.mark.parametrize(
    ("path", "expected"),
    [
        (".git", True),
        (".gpt-pilot", True),
        (".idea", True),
        (".vscode", True),
        (".DS_Store", True),
        (pathlib.Path("subdirectory", ".DS_Store"), True),
        ("__pycache__", True),
        (pathlib.Path("subdirectory", "__pycache__"), True),
        ("node_modules", True),
        (pathlib.Path("subdirectory", "node_modules"), True),
        ("package-lock.json", True),
        ("venv", True),
        ("dist", True),
        ("build", True),
        ("target", True),
        (".gitignore", False),
        ("server.js", False),
    ],
)
def test_default_ignore(matcher: IgnoreMatcher, path: str, expected: bool) -> None:
    """Test the default ignore patterns."""
    assert matcher.ignore(path) == expected


@pytest.mark.parametrize(
    ("ignore", "path", "expected"),
    [
        ("*.py[co]", "test.pyc", True),
        ("*.py[co]", "subdir/test.pyo", True),
        ("*.py[co]", "test.py", False),
        ("*.min.js", f"public/js/script.min.js", True),
        ("*.min.js", f"public/js/min.js", False),
    ],
)
def test_additional_ignore(matcher: IgnoreMatcher, ignore: str, path: str, expected: bool) -> None:
    """Test additional ignore patterns."""
    matcher.add_ignore(ignore)
    assert matcher.ignore(path) == expected


@pytest.mark.parametrize(
    ("ignore", "path", "expected"),
    [
        ("jquery.js", "jquery.js", True),
        ("jquery.js", "otherdir/jquery.js", True),
        ("jquery.js", f"{os.sep}test{os.sep}jquery.js", True),
    ],
)
def test_full_path(matcher: IgnoreMatcher, ignore: str, path: str, expected: bool) -> None:
    """Test ignoring files by full path."""
    matcher.add_ignore(ignore, full_path=True)
    assert matcher.ignore(path) == expected


@pytest.mark.parametrize(
    ("size", "expected"),
    [
        (1024 * 1024, True),  # 1MB
        (49999, False),  # one byte less than the threshold
    ],
)
def test_ignore_large_files(matcher: IgnoreMatcher, size: int, expected: bool) -> None:
    """Test ignoring large files."""
    matcher.set_large_file_threshold(size)
    assert matcher.ignore("fakefile.txt") is expected


@pytest.mark.parametrize(
    ("content", "expected"),
    [
        (b"hello world ŠĐŽČĆ", False),  # text
        (b"\x89\x50\x4e\x47\x0d\x0a\x1a\x0a\x00\x00\x00\x0d\x49\x48\x44\x52", True),  # image
    ],
)
def test_ignore_binary_files(matcher: IgnoreMatcher, content: bytes, expected: bool) -> None:
    """Test ignoring binary files."""
    with TemporaryDirectory() as tmpdir:
        path = os.path.join(tmpdir, "testfile.txt")
        with open(path, "wb") as fp:
            fp.write(content)

        matcher.root_path = pathlib.Path(tmpdir)
        assert matcher.ignore("testfile.txt") is expected
        assert matcher.ignore(path) is expected


@patch("utils.ignore.os.path.isfile")
@patch("utils.ignore.os.path.getsize")
@patch("utils.ignore.open")
def test_ignore_permission_denied(
    mock_open: create_autospec, mock_getsize: create_autospec, mock_isfile: create_autospec
) -> None:
    """Test ignoring files that raise a `PermissionError`."""
    mock_isfile.return_value = True
    mock_getsize.return_value = 100
    mock_open.side_effect = PermissionError("Permission denied")

    matcher = IgnoreMatcher()
    with pytest.raises(PermissionError):
        matcher.ignore("somefile.txt")

    mock_open.assert_called_once_with("somefile.txt", "r", encoding="utf-8")
