from base64 import b64decode
from typing import Any

from peewee import SqliteDatabase, PostgresqlDatabase
import pytest

from database.config import DATABASE_TYPE, DB_NAME, DB_HOST
from database.database import TABLES, database as db_module
from database.models.user import User
from database.models.app import App
from database.models.development_steps import DevelopmentSteps
from database.models.files import File
from database.models.file_snapshot import FileSnapshot

EMPTY_PNG = b64decode(
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg=="
)


class PostgresRollback(Exception):
    pass


@pytest.fixture
def db() -> Any:
    """
    Set up a new empty initialized test database.

    In case of SQlite, the database is created in-memory. In case of PostgreSQL,
    the database should already exist and be empty.

    This fixture will create all the tables and run the test in an isolated transaction.
    which gets rolled back after the test. The fixture also drops all the tables at the
    end.
    """
    Database = SqliteDatabase if DATABASE_TYPE == "sqlite" else PostgresqlDatabase
    db = Database(
        DB_NAME if DATABASE_TYPE == "postgres" else ":memory:",
        host=DB_HOST,
        user=DB_USER if DATABASE_TYPE == "postgres" else None,
        password=DB_PASSWORD if DATABASE_TYPE == "postgres" else None,
    )

    db.bind(TABLES)

    try:
        db.create_tables(TABLES)
        with db.atomic():
            yield db
            raise PostgresRollback()
    finally:
        db.drop_tables(TABLES)


@pytest.fixture
def user_app_step(db: db_module.Database) -> tuple[User, App, DevelopmentSteps]:
    user = User.create(email="", password="")
    app = App.create(user=user)
    step = DevelopmentSteps.create(app=app, llm_response={})
    return user, app, step

