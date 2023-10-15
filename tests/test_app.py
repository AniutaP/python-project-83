from page_analyzer.app import app
from page_analyzer.url_check import validate
from page_analyzer.get_data import get_url_by_name
import string
import random


def test_home():
    response = app.test_client().get('/')
    html = response.data.decode()
    assert response.status_code == 200
    assert '<a class="navbar-brand" href="/">Анализатор страниц</a>' in html
    assert '<a class="nav-link" href="/urls">Сайты</a>' in html


def test_validate():
    url = 'https://check.su/contact'
    assert validate(url) == {'url': 'https://check.su', 'error': None}

    url = random.choices(string.ascii_letters + string.digits, k=256)
    assert validate(url) == {'url': url, 'error': 'Слишком длинный URL'}

    url = 'bcajsbc'
    assert validate(url) == {'url': 'bcajsbc', 'error': 'Некорректный URL'}

