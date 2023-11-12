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
            url = cursor.fetchone()
    return url


def insert_url_in_db(url):
    url_data = {
        'url': url,
        'created_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    values = (url_data['url'], url_data['created_at'])

    with get_connection() as connection:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            query = '''INSERT
                        INTO urls (name, created_at)
                        VALUES (%s, %s)'''
            cursor.execute(query, values)


def get_urls_with_checks():
    with get_connection() as connection:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            query_sort_urls = '''SELECT *
                                FROM urls
                                ORDER BY id DESC;'''
            cursor.execute(query_sort_urls)
            urls = cursor.fetchall()
            query_sort_checks = '''SELECT DISTINCT ON (url_id) *'
                                    FROM url_checks
                                    ORDER BY url_id DESC, created_at DESC;'''
            cursor.execute(query_sort_checks)
            checks = cursor.fetchall()

    result = []
    checks_by_url_id = {check['url_id']: check for check in checks}
    for url in urls:
        url_data = {}
        check = checks_by_url_id.get(url['id'])
        url_data['id'] = url['id']
        url_data['name'] = url['name']
        url_data['last_check_date'] = check['created_at'] if check else ''
        url_data['status_code'] = check['status_code'] if check else ''
        result.append(url_data)

    return result


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
    with get_connection() as connection:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
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
            cursor.execute(query, values)


def get_all_checks(id):
    with get_connection() as connection:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            query = '''SELECT *
                        FROM url_checks
                        WHERE url_id=(%s)
                        ORDER BY id DESC'''
            cursor.execute(query, (id, ))
            checks = cursor.fetchall()
    return checks


def get_url_info(url):
    response = requests.get(url)
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
