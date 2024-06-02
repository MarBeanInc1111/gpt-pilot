from peewee import ForeignKeyField, AutoField, TextField, IntegerField, CharField, JSONField
from database.config import DATABASE_TYPE
from database.models.components.base_models import BaseModel
from database.models.app import App

class DevelopmentSteps(BaseModel):
    id = AutoField()  # This will serve as the primary key
    app = ForeignKeyField(App, on_delete='CASCADE')
    prompt_path = TextField(null=True)
    llm_req_num = IntegerField(null=True)
    token_limit_exception_raised = TextField(null=True)
    messages = JSONField(null=True)
    llm_response = JSONField(null=False)
    prompt_data = JSONField(null=True)
    previous_step = ForeignKeyField('self', null=True, column_name='previous_step')
    high_level_step = CharField(null=True)

    class Meta:
        table_name = 'development_steps'
        indexes = (
            (('app', 'previous_step', 'high_level_step'), True),
        )

    def __init__(self, *args, **kwargs):
        if DATABASE_TYPE == 'postgres':
            kwargs['llm_response'] = kwargs.pop('llm_response', {})
            kwargs['messages'] = kwargs.pop('messages', {})
            kwargs['prompt_data'] = kwargs.pop('prompt_data', {})
        super().__init__(*args, **kwargs)
