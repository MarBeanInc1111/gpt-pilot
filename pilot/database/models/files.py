import os
from pathlib import Path
from os.path import commonprefix
from peewee import AutoField, CharField, TextField, ForeignKeyField

from database.models.components.base_models import BaseModel
from database.models.app import App

def update_paths() -> None:
    """
    Updates the `full_path` attribute of all `File` objects in the database to use the correct
    workspace directory.
    """
    workspace_dir = Path(__file__).parent.parent.parent.parent / "workspace"
    if not workspace_dir.exists():
        # This should only happen on first run
        return

    paths = [file.full_path for file in File.select(File.full_path).distinct()]
    if not paths:
        # No paths in the database, so nothing to fix
        return

    old_prefix = commonprefix(paths)
    if old_prefix == str(workspace_dir):
        # Paths are up to date, nothing to fix
        return

    common_sep = "\\" if ":\\" in old_prefix else "/"
    common_parts = common_prefix(paths).split(common_sep)
    try:
        workspace_index = common_parts.index("workspace")
    except ValueError:
        # There's something strange going on, better not touch anything
        return

    old_prefix = common_sep.join(common_parts[:workspace_index + 1])

    print(f"Updating file paths from {old_prefix} to {workspace_dir}")
    for file in File.select():
        if file.full_path == old_prefix:
            continue
        parts = file.full_path.split(common_sep)
        new_path = str(workspace_dir) + sep + sep.join(parts[workspace_index + 1:])
        if file.full_path == new_path:
            continue
        if not new_path.startswith(str(workspace_dir)):
            continue
        file.full_path = new_path
        file.save()

class File(BaseModel):
    id: int = AutoField()
    app: App = ForeignKeyField(App, on_delete='CASCADE')
    name: str = CharField()
    path: str = CharField()
    full_path: str = CharField()
    description: str = TextField(null=True)

    class Meta:
        indexes = (
            (('app', 'name', 'path'), True),
        )

    @staticmethod
    def update_paths() -> None:
        """
        Updates the `full_path` attribute of all `File` objects in the database to use the correct
        workspace directory.
        """
        workspace_dir = Path(__file__).parent.parent.parent.parent / "workspace"
        if not workspace_dir.exists():
            # This should only happen on first run
            return

        paths = [file.full_path for file in File.select(File.full_path).distinct()]
        if not paths:
            # No paths in the database, so nothing to fix
            return

        old_prefix = commonprefix(paths)
        if old_prefix == str(workspace_dir):
            # Paths are up to date, nothing to fix
            return

        common_sep = "\\" if ":\\" in old_prefix else "/"
        common_parts = common_prefix(paths).split(common_sep)
        try:
            workspace_index = common_parts.index("workspace")
        except ValueError:
            # There's something strange going on, better not touch anything
            return

        old_prefix = common_sep.join(common_parts[:workspace_index + 1])

        print(f"Updating file paths from {old_prefix} to {workspace_dir}")
        for file in File.select():
            if file.full_path == old_prefix:
                continue
            parts = file.full_path.split(common_sep)
            new_path = str(workspace_dir) + sep + sep.join(parts[workspace_index + 1:])
            if file.full_path == new_path:
                continue
            if not new_path.startswith(str(workspace_dir)):
                continue
            file.full_path = new_path
            file.save()
