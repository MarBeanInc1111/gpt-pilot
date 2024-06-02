from peewee import AutoField, ForeignKeyField, TextField, CharField

from database.models.components.base_models import BaseModel
from database.models.app import App

class UserInputs(BaseModel):
    """
    A model representing user inputs for a specific app.

    Attributes:
        id (AutoField): The unique identifier for the user input.
        app (ForeignKeyField): The app associated with the user input.
        query (TextField): The user's search query.
        user_input (TextField): The user's input for the current step.
        hint (TextField): A hint to help the user complete the current step.
        previous_step (ForeignKeyField): The previous step in the high-level process.
        high_level_step (CharField): The current step in the high-level process.
    """
    id = AutoField(default=AutoField.auto_increment)
    app = ForeignKeyField(App, on_delete='CASCADE')
    query = TextField(null=True)
    user_input = TextField(null=True)
    hint = TextField(null=True)
    previous_step = ForeignKeyField('self', null=True, column_name='previous_step', default=None)
    high_level_step = CharField(null=True)

    class Meta:
        """
        Meta options for the UserInputs model.

        Attributes:
            table_name (str): The name of the table in the database.
            indexes (list): A list of indexes to create on the table.
            unique_together (list): A list of unique constraints to enforce on the table.
        """
        table_name = 'user_inputs'
        indexes = (
            (('app', 'previous_step', 'high_level_step'), True),
        )
        unique_together = (('app', 'previous_step', 'high_level_step'),)


    class Meta:
        table_name = 'user_inputs'
        indexes = (
            (('app', 'previous_step', 'high_level_step'), True),
            (('app', 'previous_step', 'high_level_step'), True),
        )
