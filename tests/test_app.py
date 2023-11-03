from page_analyzer.app import app
from page_analyzer.url_check import validate
import string
import random
import pytest


@pytest.fixture
def client():
    app.config['TESTING'] = True
    client = app.test_client()
    yield client


def test_home(client):
    app.config['TESTING'] = True
    response = client.get('/')
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
