from functools import reduce
import operator
from typing import Dict, Any
import psycopg2
from psycopg2.extensions import quote_ident
from peewee import DoesNotExist, IntegrityError, Model, SqliteDatabase, PostgresqlDatabase
from playhouse.shortcuts import model_to_dict

DATABASE_TYPES = {"sqlite": SqliteDatabase, "postgres": PostgresqlDatabase}

def db_connect(database_type: str, db_name: str, db_user: str, db_password: str, db_host: str, db_port: str):
    db = DATABASE_TYPES[database_type](db_name)
    db.connect(user=db_user, password=db_password, host=db_host, port=db_port)
    return db

def db_close(db: Model):
    db.close()

def get_app_helper(app_id: int, error_if_not_found: bool = True):
    try:
        app = App.get(App.id == app_id)
    except DoesNotExist:
        if error_if_not_found:
            raise ValueError(f"No app with id: {app_id}")
        return None
    return app

def create_tables(database_type: str, db_name: str, db_user: str, db_password: str, db_host: str, db_port: str):
    db = db_connect(database_type, db_name, db_user, db_password, db_host, db_port)
    with db:
        if database_type == "postgres":
            sql = reduce(operator.add, [model._meta.create_table_sql() for model in TABLES])
        elif database_type == "sqlite":
            sql = reduce(operator.add, [model._meta.create_table_sql() for model in TABLES if not model._meta.table_exists()])
        else:
            raise ValueError(f"Unsupported DATABASE_TYPE: {database_type}")
        db.execute_sql(sql)
    db_close(db)

def drop_tables(database_type: str, db_name: str, db_user: str, db_password: str, db_host: str, db_port: str):
    db = db_connect(database_type, db_name, db_user, db_password, db_host, db_port)
    with db:
        if database_type == "postgres":
            sql = reduce(operator.add, [f'DROP TABLE IF EXISTS "{model._meta.table_name}" CASCADE' for model in TABLES])
        elif database_type == "sqlite":
            sql = reduce(operator.add, [f'DROP TABLE IF EXISTS "{model._meta.table_name}"' for model in TABLES])
        else:
            raise ValueError(f"Unsupported DATABASE_TYPE: {database_type}")
        db.execute_sql(sql)
    db_close(db)

def database_exists(database_type: str, db_name: str, db_user: str, db_password: str, db_host: str, db_port: str):
    db = db_connect(database_type, db_name, db_user, db_password, db_host, db_port)
    try:
        db.connect()
        db_close(db)
        return True
    except Exception:
        return False

def create_database(database_type: str, db_name: str, db_user: str, db_password: str, db_host: str, db_port: str):
    if database_type == "postgres":
        conn = psycopg2.connect(
            dbname='postgres',
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port
        )
        conn.autocommit = True
        cursor = conn.cursor()

        safe_db_name = quote_ident(db_name, conn)
        cursor.execute(f"CREATE DATABASE {safe_db_name}")

        cursor.close()
        conn.close()
    else:
        pass

def tables_exist(database_type: str, db_name: str, db_user: str, db_password: str, db_host: str, db_port: str):
    db = db_connect(database_type, db_name, db_user, db_password, db_host, db_port)
    result = all([model._meta.table_exists() for model in TABLES])
    db_close(db)
    return result

# The rest of the code remains the same
