#!/usr/bin/env python3
from flask import (
    Flask,
    render_template,
    request,
    redirect,
    flash,
    url_for,
    get_flashed_messages)
import os
from dotenv import load_dotenv
from page_analyzer.get_data import (
    get_all_strings,
    get_url_by_field,
    add_in_db,
    get_all_checks,
    get_url_info)
from page_analyzer.url_check import validate
from datetime import datetime
import requests


load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


@app.route('/')
def home():
    return render_template('home_page.html')


@app.get('/urls')
def urls_checks_table():
    urls = get_all_strings()
    messages = get_flashed_messages(with_categories=True)
    return render_template(
        'urls.html',
        urls=urls,
        messages=messages
    )


@app.post('/urls')
def urls_post():
    url_get = request.form.get('url')
    validation = validate(url_get)
    error = validation['error']
    url = validation['url']

    if error:
        flash(error, 'danger')
        messages = get_flashed_messages(with_categories=True)
        return render_template(
            'home_page.html',
            messages=messages
        ), 422

    if get_url_by_field('name', url):
        id = get_url_by_field('name', url)['id']
        flash('Страница уже существует', 'info')
        return redirect(url_for(
            'url_show_page',
            id=id
        ))
    else:
        query = '''INSERT
                    INTO urls (name, created_at)
                    VALUES (%s, %s)'''

        url_data = {
            'url': url,
            'created_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        values = (url_data['url'], url_data['created_at'])

        add_in_db(query, values)
        id = get_url_by_field('name', url)['id']
        flash('Страница успешно добавлена', 'success')
        return redirect(url_for(
            'url_show_page',
            id=id
        ))


@app.route('/urls/<int:id>')
def url_show_page(id):
    url = get_url_by_field('id', id)
    checks = get_all_checks(id)
    messages = get_flashed_messages(with_categories=True)
    return render_template(
        'urls_id.html',
        url=url,
        messages=messages,
        checks=checks
    )


@app.post('/urls/<int:id>/checks')
def url_checks(id):
    try:
        url = get_url_by_field('id', id)['name']
        check = get_url_info(url)
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

        add_in_db(query, values)
        flash('Страница успешно проверена', 'success')

    except requests.RequestException:
        flash('Произошла ошибка при проверке', 'danger')

    return redirect(url_for(
        'url_show_page',
        id=id
    ))
