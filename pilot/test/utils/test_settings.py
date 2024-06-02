import json
import os
from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest
from git import Repo  # Added to get the git commit hash
import pkg_resources  # Added to get the package version

from utils.settings import (
    Loader,
    Settings,
    get_git_commit,
    get_package_version,
    get_version,
)


@pytest.fixture
def expected_config_location():
    config_home = os.getenv("XDG_CONFIG_HOME")
    if config_home:
        return Path(config_home) / "gpt-pilot" / "config.json"
    else:
        platform = sys.platform
        if platform == "darwin" or platform == "linux":
            return Path.home() / ".gpt-pilot" / "config.json"
        elif platform == "win32":
            return Path(os.environ["APPDATA"]) / "GPT Pilot" / "config.json"
        else:
            raise RuntimeError(f"Unknown platform: {platform}")


def test_settings_initializes_known_variables():
    settings = Settings()
    assert settings.openai_api_key is None
    assert settings.telemetry is None


def test_settings_init_ignores_unknown_variables():
    settings = Settings(unknown="value")
    assert not hasattr(settings, "unknown")


def test_settings_forbids_saving_unknown_variables():
    settings = Settings()

    with pytest.raises(AttributeError):
        settings.unknown = "value"


def test_settings_update():
    settings = Settings()
    settings.update(openai_api_key="test_key")
    assert settings.openai_api_key == "test_key"


def test_settings_to_dict():
    settings = Settings()
    settings.update(openai_api_key="test_key")
    assert dict(settings) == {
        "openai_api_key": "test_key",
        "telemetry": None,
    }


def test_loader_config_file_location(expected_config_location):
    settings = Settings()
    assert Loader(settings).config_path == expected_config_location


@patch("utils.settings.open")
@patch("utils.settings.Loader.update_settings_from_env")
def test_loader_load_config_file(_mock_from_env, mock_open, expected_config_location):
    settings = Settings()
    fake_config = json.dumps(
        {
            "openai_api_key": "test_key",
            "telemetry": {
                "id": "fake-id",
                "endpoint": "https://example.com",
            },
        }
    )
    mock_open.return_value.__enter__.return_value = fake_config

    loader = Loader(settings)
    loader.load()

    assert loader.config_path == Path(expected_config_location)
    mock_open.assert_called_once_with(loader.config_path, "r", encoding="utf-8")

    assert settings.openai_api_key == "test_key"
    assert settings.telemetry["id"] == "fake-id"
    assert settings.telemetry["endpoint"] == "https://example.com"


@patch("utils.settings.open")
@patch("utils.settings.Loader.update_settings_from_env")
def test_loader_load_no_config_file(_mock_from_env, mock_open, expected_config_location):
    settings = Settings()
    loader = Loader(settings)
    loader.config_path = Path(expected_config_location)

    loader.load()

    mock_open.assert_not_called()

    assert settings.openai_api_key is None
    assert settings.telemetry is None


@patch("utils.settings.getenv")
def test_loader_load_from_env(mock_getenv):
    settings = Settings()
    mock_getenv.side_effect = lambda key: {
        "TELEMETRY_ID": "fake-id",
        "TELEMETRY_ENDPOINT": "https://example.com",
        "OPENAI_API_KEY": "test_key",
    }.get(key)

    Loader(settings).update_settings_from_env(settings)
    assert settings.openai_api_key == "test_key"
    assert settings.telemetry["id"] == "fake-id"
    assert settings.telemetry["endpoint"] == "https://example.com"


def test_get_git_commit():
    repo = Repo()
    try:
        expected_commit_hash = repo.head.object.hexsha
    except:
        expected_commit_hash = None

    assert get_git_commit() == expected_commit_hash


def test_get_package_version():
    assert get_package_version().startswith("0.")


def test_get_version():
    try:
        commit_suffix = (
            "-git"
            + get_git_commit()[:7] if get_git_commit() else ""
        )
    except:
        commit_suffix = ""

    assert get_version().endswith(commit_suffix)
