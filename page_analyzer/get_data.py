import os
from dotenv import load_dotenv
from psycopg2 import connect
from psycopg2.extras import RealDictCursor


load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')


def get_url_by_id(id):
    connection = connect(DATABASE_URL)
    with connection.cursor(cursor_factory=RealDictCursor) as cursor:
        query = '''SELECT *
                    FROM urls
                    WHERE id=(%s);'''
        cursor.execute(query, [id])
        urls = cursor.fetchone()
    connection.close()
    return urls


def get_url_by_name(name):
    connection = connect(DATABASE_URL)
    with connection.cursor(cursor_factory=RealDictCursor) as cursor:
        query = '''SELECT *
                    FROM urls
                    WHERE name=(%s)'''
        cursor.execute(query, [name])
        urls = cursor.fetchone()
    connection.close()
    return urls


def add_url_string(url_string_to_dict):
    connection = connect(DATABASE_URL)
    with connection.cursor() as cursor:
        query = '''INSERT
                    INTO urls (name, created_at)
                    VALUES (%s, %s)'''
        cursor.execute(query, (
            url_string_to_dict['url'],
            url_string_to_dict['created_at']
        ))
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


def add_check(check):
    connection = connect(DATABASE_URL)
    with connection.cursor() as cursor:
        query = '''INSERT
                   INTO url_checks (url_id, created_at)
                   VALUES (%s, %s)'''
        cursor.execute(query, (
            check['url_id'],
            check['checked_at']
        ))
        connection.commit()
    connection.close()


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
