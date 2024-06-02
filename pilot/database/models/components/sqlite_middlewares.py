from peewee import *
from peewee_mysql import JSONField


db = MySQLDatabase('database_name', **database_settings)

class BaseModel(Model):
    class Meta:
        database = db

class MyModel(BaseModel):
    data = JSONField()

    def __init__(self, *args, **kwargs):
        if 'data' in kwargs:
            kwargs['data'] = json.loads(kwargs['data'])
        super().__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        if self.data is not None:
            kwargs['data'] = json.dumps(self.data)
        super().save(*args, **kwargs)
