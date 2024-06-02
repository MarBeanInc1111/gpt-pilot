from peewee import ForeignKeyField, CharField

from database.models.components.base_models import BaseModel
from database.models.user import User

class AppStatus(BaseModel):
    status = CharField()

class AppType(BaseModel):
    app_type = CharField()

class App(BaseModel):
    user = ForeignKeyField(User, backref='apps')
    app_type = ForeignKeyField(AppType, backref='apps')
    name = CharField()
    status = ForeignKeyField(AppStatus, backref='apps')
