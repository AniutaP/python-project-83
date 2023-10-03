#!/usr/bin/env python3
from flask import Flask, render_template


app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home_page.html')


@app.route('/urls')
def urls_conteiner():
    return render_template('urls.html')
