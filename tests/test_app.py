from page_analyzer.app import app
from page_analyzer.url_check import validate
import string
import random


def test_validate():
    url = 'https://check.su/contact'
    assert validate(url) == {'url': 'https://check.su', 'error': None}

    url = random.choices(string.ascii_letters + string.digits, k=256)
    assert validate(url) == {'url': url, 'error': 'Слишком длинный URL'}

    url = 'bcajsbc'
    assert validate(url) == {'url': 'bcajsbc', 'error': 'Некорректный URL'}
