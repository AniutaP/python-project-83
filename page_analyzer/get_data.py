from psycopg2.extras import RealDictCursor
import requests
from bs4 import BeautifulSoup
from page_analyzer.get_conn import get_connection
from datetime import datetime


def get_url_by_field(field, data):
    with get_connection() as connection:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            query = f'''SELECT *
                        FROM urls
                        WHERE {field}=(%s);'''
            cursor.execute(query, [data])
            urls = cursor.fetchone()
    return urls


def add_in_db(query, values):
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(query, values)


def get_data_for_post_url(url):
    query = '''INSERT
                INTO urls (name, created_at)
                VALUES (%s, %s)'''

    url_data = {
        'url': url,
        'created_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    values = (url_data['url'], url_data['created_at'])

    return query, values


def get_all_strings():
    with get_connection() as connection:
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
    return urls


def url_checks_by_id(id, check):
    check['url_id'] = id
    check['checked_at'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    values = (
        check['url_id'],
        check['status_code'],
        check['h1'],
        check['title'],
        check['description'],
        check['checked_at']
    )

    query = '''INSERT
                        INTO url_checks (
                            url_id,
                            status_code,
                            h1,
                            title,
                            description,
                            created_at
                            )
                        VALUES (%s, %s, %s, %s, %s, %s)'''

    return query, values


def get_all_checks(id):
    with get_connection() as connection:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            query = '''SELECT *
                        FROM url_checks
                        WHERE url_id=(%s)
                        ORDER BY id DESC'''
            cursor.execute(query, [id])
            checks = cursor.fetchall()
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
