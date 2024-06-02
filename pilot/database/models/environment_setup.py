from database.models.components.progress_step import ProgressStep

class EnvironmentSetup(ProgressStep):
    class Meta:
        db_table = 'environment_setup'
        primary_key = True


from database.models.components import ProgressStep

class EnvironmentSetup(ProgressStep):
    db_table = 'environment_setup'
    primary_key = True
