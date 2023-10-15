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
    get_all_checks)
from page_analyzer.url_check import validate
from datetime import datetime


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
    field = 'name'
    id = get_url_by_field(field, url)['id']

    if get_url_by_field(field, url):
        flash('Страница уже существует', 'info')
        return redirect(url_for(
            'url_show_page',
            id=id
        ))
    else:
        query = '''INSERT
                    INTO urls (name, created_at)
                    VALUES (%s, %s)'''
        values = {
            'url': url,
            'created_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        add_in_db(query, values)
        flash('Страница успешно добавлена', 'success')
        return redirect(url_for(
            'url_show_page',
            id=id
        ))


@app.route('/urls/<int:id>')
def url_show_page(id):
    field = 'id'
    url = get_url_by_field(field, id)
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
    check = {
        'checked_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'url_id': id
    }
    query = '''INSERT
                       INTO url_checks (url_id, created_at)
                       VALUES (%s, %s)'''
    add_in_db(query, check)
    flash('Страница успешно проверена', 'success')
    return redirect(url_for(
        'url_show_page',
        id=id
    ))
