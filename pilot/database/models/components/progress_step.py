from peewee import ForeignKeyField, CharField, BooleanField, DateTimeField, JSONField
from database.config import DATABASE_TYPE
from database.models.components.base_models import BaseModel
from database.models.app import App

class ProgressStep(BaseModel):
    app = ForeignKeyField(App, primary_key=True, on_delete='CASCADE')
    step = CharField()
    app_data = JSONField()
    data = JSONField(null=True)
    messages = JSONField(null=True)
    completed = BooleanField(default=False)
    completed_at = DateTimeField(null=True)

    if DATABASE_TYPE == 'postgres':
        app_data = BinaryJSONField()
        data = BinaryJSONField(null=True)
        messages = BinaryJSONField(null=True)
