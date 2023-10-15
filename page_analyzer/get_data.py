import os
from dotenv import load_dotenv
from psycopg2 import connect
from psycopg2.extras import RealDictCursor


load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')


def get_url_by_field(field, data):
    connection = connect(DATABASE_URL)
    with connection.cursor(cursor_factory=RealDictCursor) as cursor:
        query = f'''SELECT *
                    FROM urls
                    WHERE {field}=(%s);'''
        cursor.execute(query, [data])
        urls = cursor.fetchone()
    connection.close()
    return urls


def add_in_db(query, values):
    connection = connect(DATABASE_URL)
    with connection.cursor() as cursor:
        cursor.execute(query, values)
        connection.commit()
    connection.close()


def get_all_strings():
    connection = connect(DATABASE_URL)
    with connection.cursor(cursor_factory=RealDictCursor) as cursor:
        query = '''SELECT DISTINCT ON (urls.id)
                        urls.id AS id,
                        urls.name AS name,
                        url_checks.created_at AS check_last
                    FROM urls
                    LEFT JOIN url_checks
                    ON urls.id = url_checks.url_id
                    AND url_checks.id = (SELECT MAX(id)
                                        FROM url_checks
                                        WHERE url_id = urls.id)
                    ORDER BY urls.id DESC;'''
        cursor.execute(query)
        urls = cursor.fetchall()
    connection.close()
    return urls


def get_all_checks(id):
    connection = connect(DATABASE_URL)
    with connection.cursor(cursor_factory=RealDictCursor) as cursor:
        query = '''SELECT *
                    FROM url_checks
                    WHERE url_id=(%s)
                    ORDER BY id DESC'''
        cursor.execute(query, [id])
        checks = cursor.fetchall()
    connection.close()
    return checks
