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
    get_all_strings, get_url_by_id, get_url_by_name, add_url_string)
from page_analyzer.url_check import validate
from datetime import datetime


load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


@app.route('/')
def home():
    return render_template('home_page.html')


@app.get('/urls')
def urls_table():
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
        if error == 'Уже существует':
            id = get_url_by_name(url)['id']
            flash('Страница уже существует', 'info')
            return redirect(url_for(
                'url_show_page',
                id=id
            ))
        else:
            flash(error, 'danger')
            messages = get_flashed_messages(with_categories=True)
            return render_template(
                'home_page.html',
                messages=messages
            ), 422
    else:
        url_string_to_dict = {
            'url': url,
            'created_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        add_url_string(url_string_to_dict)
        id = get_url_by_name(url)['id']
        flash('Страница успешно добавлена', 'success')
        return redirect(url_for(
            'url_show_page',
            id=id
        ))


@app.route('/urls/<int:id>')
def url_show_page(id):
    url = get_url_by_id(id)
    messages = get_flashed_messages(with_categories=True)
    return render_template(
        'urls_id.html',
        url=url,
        messages=messages
    )
