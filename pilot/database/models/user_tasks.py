from database.config import DATABASE_TYPE
from database.models.components.progress_step import ProgressStep
from database.models.components.sqlite_middlewares import JSONField
from playhouse.postgres_ext import BinaryJSONField


class UserTasks(ProgressStep):
    if DATABASE_TYPE == 'postgres':
        user_tasks = BinaryJSONField(index=True)
    else:
        user_tasks = JSONField()  # Custom JSON field for SQLite

    class Meta:
        table_name = 'user_tasks'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.user_tasks is None:
            self.user_tasks = {}

    def save(self, *args, **kwargs):
        if self.user_tasks is None:
            self.user_tasks = {}
        return super().save(*args, **kwargs)
