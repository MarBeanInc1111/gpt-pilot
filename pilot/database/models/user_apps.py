from peewee import AutoField, CharField, ForeignKeyField

from database.models.components.base_models import BaseModel
from database.models.app import App
from database.models.user import User

class UserApp(BaseModel):
    id = AutoField()
    app = ForeignKeyField(App, on_delete='CASCADE')
    user = ForeignKeyField(User, on_delete='CASCADE')
    workspace = CharField(null=True)

    class Meta:
        table_name = 'user_apps'
        indexes = (
            (('app', 'user'), True),
            (('user', 'app'), True),  # Added this index for better performance when querying by user and app
        )

    def __str__(self):
        return f"<UserApp: {self.app.name} by {self.user.username} in {self.workspace}>"

