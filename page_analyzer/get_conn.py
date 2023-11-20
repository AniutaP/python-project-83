import os
from psycopg2 import pool
from contextlib import contextmanager


postgresql_pool = None


def init_db_pool():
    global postgresql_pool
    DATABASE_URL = os.getenv('DATABASE_URL')
    APP_ENV = os.getenv('APP_ENV')
    if APP_ENV != "tests":
        postgresql_pool = pool.SimpleConnectionPool(minconn=1,
                                                    maxconn=10,
                                                    dsn=DATABASE_URL)
    else:
        postgresql_pool = None


@contextmanager
def get_connection():
    connection = None
    try:
        connection = postgresql_pool.getconn()
        yield connection
        connection.commit()
    except Exception as error:
        connection.rollback()
        raise error
    finally:
        postgresql_pool.putconn(connection)
