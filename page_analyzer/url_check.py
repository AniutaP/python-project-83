#!/usr/bin/env python3
from validators import url


def validate(url_addres):
    errors = []
    if not url:
        errors.append('Не введен URL')
    elif len(url_addres) > 255:
        errors.append('Слишком длинный URL')
    elif not url(url_addres):
        errors.append('Некорректный URL')
    return errors
