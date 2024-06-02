from peewee import AutoField, ForeignKeyField, TextField, CharField, IntegerField

from database.models.components.base_models import BaseModel
from database.models.app import App


class CommandRuns(BaseModel):
    """
    Represents a command run for an app.
    """
    id: int = AutoField()
    app: App = ForeignKeyField(App, on_delete='CASCADE')
    command: str = TextField(null=True)
    cli_response: str = TextField(null=True, default='')
    done_or_error_response: str = TextField(null=True, default='')
    exit_code: int = IntegerField(null=True, default=0)
    previous_step: 'CommandRuns' = ForeignKeyField('self', null=True, column_name='previous_step', default=None)
    high_level_step: str = CharField(null=True)

    class Meta:
        """
        Meta options for the CommandRuns model.
        """
        table_name = 'command_runs'
        indexes = (
            (('app', 'previous_step', 'high_level_step'), True),
        )
        unique_together = (('app', 'previous_step', 'high_level_step'),)
