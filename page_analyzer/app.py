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
    get_urls_with_checks,
    get_url_by_field,
    get_all_checks,
    get_url_info,
    url_checks_by_id,
    insert_url_in_db)
from page_analyzer.url_check import validate
import requests
from page_analyzer.get_conn import init_db_pool


load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
init_db_pool()


@app.route('/')
def index():
    return render_template('home_page.html')


@app.get('/urls')
def urls_checks_show():
    urls = get_urls_with_checks()
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

    insert_url_in_db(url)
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
        url_checks_by_id(id, check)
        response = requests.get(url)
        response.raise_for_status()
        flash('Страница успешно проверена', 'success')

    except requests.exceptions.RequestException:
        flash('Произошла ошибка при проверке', 'danger')

    return redirect(url_for(
        'url_show_page',
        id=id
    ))
