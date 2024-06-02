import ast
import json
import argparse
from logging import getLogger
from pathlib import Path
import sys
from typing import Any, Dict, Optional

from dotenv import load_dotenv

load_dotenv()

log = getLogger(__name__)

AVAILABLE_SETTINGS: tuple[str, ...] = (
    "telemetry",
    "openai_api_key",
)


class Settings:
    """Application settings."""

    def __init__(self, **kwargs: Any):
        for key in AVAILABLE_SETTINGS:
            setattr(self, key, None)

        self.update(**kwargs)

    def __iter__(self):
        for key in AVAILABLE_SETTINGS:
            yield key, getattr(self, key)

    def update(self, **kwargs: Any):
        """Update settings."""
        for key, value in kwargs.items():
            if key in AVAILABLE_SETTINGS:
                setattr(self, key, value)


class Loader:
    """Loader for application settings."""

    APP_NAME: str = "GPT Pilot"

    def __init__(self, settings: Settings):
        self.config_dir: Path = self.resolve_config_dir()
        self.config_path: Path = self.config_dir / "config.json"
        self.settings = settings

    def load(self):
        """Load settings."""
        self.settings.update(**self._load_config())
        self.update_settings_from_env(self.settings)
        self.update_settings_from_args(self.settings)

    @classmethod
    def resolve_config_dir(cls) -> Path:
        """Figure out where to store the config file(s)."""
        posix_app_name = cls.APP_NAME.replace(" ", "-").lower()

        xdg_config_home = getenv("XDG_CONFIG_HOME")
        if xdg_config_home:
            return Path(xdg_config_home) / Path(posix_app_name)

        if sys.platform == "win32" and getenv("APPDATA"):
            return Path(getenv("APPDATA")) / Path(cls.APP_NAME)

        return Path().expanduser() / Path(f".{posix_app_name}")

    def _load_config(self) -> Dict[str, Any]:
        """Load settings from the config file."""
        if not self.config_path.exists():
            return {}

        log.debug(f"Loading settings from config file: {self.config_path}")
        with open(self.config_path, "r", encoding="utf-8") as fp:
            return json.load(fp, object_hook=lambda d: dict(d))

    def _save_config(self, config: Dict[str, Any]):
        """Save settings to the config file."""
        if not self.config_dir.exists():
            log.debug(f"Creating config directory: {self.config_dir}")
            self.config_dir.mkdir(parents=True, exist_ok=True)

        log.debug(f"Saving settings to config file: {self.config_path}")
        self.config_path.write_text(json.dumps(config, indent=2), encoding="utf-8")

    def save(self, *args: list[str]):
        """Save one or more settings to the config file."""
        settings_from_config = self._load_config()

        for key in args:
            if key in AVAILABLE_SETTINGS:
                settings_from_config[key] = getattr(self.settings, key)

        self._save_config(settings_from_config)

    def update_settings_from_env(self, settings: Settings):
        """Update settings from environment variables."""
        settings.telemetry = {
            "id": getenv("TELEMETRY_ID"),
            "endpoint": getenv("TELEMETRY_ENDPOINT"),
        }

        settings.openai_api_key = getenv("OPENAI_API_KEY")

    def update_settings_from_args(self, settings: Settings):
        """Update settings from command-line arguments."""
        parser = argparse.ArgumentParser()
        for key in AVAILABLE_SETTINGS:
            parser.add_argument(f"--{key}", default=None)

        args = parser.parse_args()

        for key in AVAILABLE_SETTINGS:
            value = getattr(args, key)
            if value is not None:
                setattr(settings, key, value)


def get_git_commit() -> Optional[str]:
    """Return the current git commit (if running from a repo)."""
    git_dir = Path(__file__).parent.parent.parent / ".git"

    if not git_dir.is_dir():
        return None

    git_head = git_dir / "HEAD"
    if not git_head.is_file():
        return None

    with open(git_head, "r", encoding="utf-8") as fp:
        ref = fp.read().strip()
        if ref.startswith("ref: "):
            ref = ref[5:]
            with open(git_dir / ref, "r", encoding="utf-8") as fp:
                return fp.read().strip()
        else:
            return ref


def get_package_version() -> str:
    """Get package version."""
    setup_file = Path(__file__).parent.parent.parent / "setup.py"

    if not setup_file.is_file():
        return "0.0.0"

    with open(setup_file, "r", encoding="utf-8") as fp:
        code = ast.parse(fp.read(), filename="setup.py")
        for node in code.body:
            if (
                isinstance(node, ast.Assign)
                and len(node.targets) == 1
                and isinstance(node.targets[0], ast.Name)
                and node.targets[0].id == "VERSION"
                and isinstance(node.value, ast.Constant)
            ):
                return str(node.value.value)

    return "0.0.0"


def get_version() -> str:
    """Find and return the current version of GPT Pilot."""
    version = get_package_version()
    commit = get_git_commit()
    if commit:
        version = f"{version}-git{commit[:7]}"

    return version


version = get_version()
settings = Settings()
loader = Loader(settings)
loader.load()
config_path = loader.config_path

__all__ = ["version", "settings", "loader", "config_path"]
