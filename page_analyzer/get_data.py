import os
from dotenv import load_dotenv
from psycopg2.extras import RealDictCursor
import requests
from bs4 import BeautifulSoup
from psycopg2 import pool


load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')

postgresql_pool = pool.SimpleConnectionPool(minconn=1,
                                            maxconn=10,
                                            dsn=DATABASE_URL)


def get_url_by_field(field, data):
    connection = postgresql_pool.getconn()
    with connection.cursor(cursor_factory=RealDictCursor) as cursor:
        query = f'''SELECT *
                    FROM urls
                    WHERE {field}=(%s);'''
        cursor.execute(query, [data])
        urls = cursor.fetchone()
    cursor.close()
    postgresql_pool.putconn(connection)
    return urls


def add_in_db(query, values):
    connection = postgresql_pool.getconn()
    with connection.cursor() as cursor:
        cursor.execute(query, values)
        connection.commit()
    cursor.close()
    postgresql_pool.putconn(connection)


def get_all_strings():
    connection = postgresql_pool.getconn()
    with connection.cursor(cursor_factory=RealDictCursor) as cursor:
        query = '''SELECT
                        urls.id AS id,
                        urls.name AS name,
                        url_checks.created_at AS check_last,
                        url_checks.status_code AS status_code
                    FROM urls
                    LEFT JOIN url_checks
                    ON urls.id = url_checks.url_id
                    AND url_checks.id = (SELECT MAX(id)
                                        FROM url_checks
                                        WHERE url_id = urls.id)
                    ORDER BY urls.id;'''
        cursor.execute(query)
        urls = cursor.fetchall()
    cursor.close()
    postgresql_pool.putconn(connection)
    return urls


def get_all_checks(id):
    connection = postgresql_pool.getconn()
    with connection.cursor(cursor_factory=RealDictCursor) as cursor:
        query = '''SELECT *
                    FROM url_checks
                    WHERE url_id=(%s)
                    ORDER BY id DESC'''
        cursor.execute(query, [id])
        checks = cursor.fetchall()
    cursor.close()
    postgresql_pool.putconn(connection)
    return checks


def get_url_info(url):
    response = requests.get(url)

    if response.status_code != 200:
        raise requests.RequestException

    check = {'status_code': response.status_code}

    soup = BeautifulSoup(response.text, 'html.parser')

    h1 = soup.find('h1')
    if h1:
        check['h1'] = h1.text
    else:
        check['h1'] = ''

    title = soup.find('title')
    if title:
        check['title'] = title.text
    else:
        check['title'] = ''

    description = soup.find('meta', attrs={'name': 'description'})
    if description:
        check['description'] = description['content']
    else:
        check['description'] = ''

    return check
