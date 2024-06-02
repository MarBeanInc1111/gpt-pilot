from database.config import DATABASE_TYPE
from database.models.components.progress_step import ProgressStep
from database.models.components.sqlite_middlewares import JSONField
from playhouse.postgres_ext import BinaryJSONField

class UserStoriesJSONField:
    def __init__(self):
        self.field = None
        if DATABASE_TYPE == 'postgres':
            self.field = BinaryJSONField()
        else:
            self.field = JSONField()  # Custom JSON field for SQLite

