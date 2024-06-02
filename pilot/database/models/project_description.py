from peewee import TextField
from playhouse.migrate import SqliteDatabase, migrate
from database.models.components.progress_step import ProgressStep

db = SqliteDatabase('path/to/your/database.db')

class ProjectDescription(ProgressStep):
    prompt = TextField()
    summary = TextField()

    class Meta:
        table_name = 'project_description'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.table_name = 'project_description'

def create_table():
    with db:
        db.create_tables([ProjectDescription])

if __name__ == '__main__':
    create_table()
