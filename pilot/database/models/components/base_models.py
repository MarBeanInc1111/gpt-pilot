import uuid
from datetime import datetime
from peewee import Model, UUIDField, DateTimeField

from database.config import DATABASE_TYPE
from database.connection import get_database

class BaseModel(Model):
    id = UUIDField(primary_key=True, default=uuid.uuid4)
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)

    class Meta:
        database = get_database()

def get_database():
    if DATABASE_TYPE == "postgres":
        return get_postgres_database()
    return get_sqlite_database()
