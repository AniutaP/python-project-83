#!/usr/bin/env python3
import validators
from urllib.parse import urlparse


def validate(url):
    error = None
    if not validators.url:
        error = 'Не введен URL'
    elif len(url) > 255:
        error = 'Слишком длинный URL'
    elif not validators.url(url):
        error = 'Некорректный URL'
    else:
        parsed_url = urlparse(url)
        normalized_url = f'{parsed_url.scheme}://{parsed_url.netloc}'
        url = normalized_url

    validate_url = {'url': url, 'error': error}
    return validate_url
