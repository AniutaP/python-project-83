#!/usr/bin/env python3
from flask import Flask, render_template
import psycopg2
import os
from dotenv import load_dotenv


load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

DATABASE_URL = os.getenv('DATABASE_URL')
conn = psycopg2.connect(DATABASE_URL)


@app.route('/')
def home():
    return render_template('home_page.html')


@app.route('/urls')
def urls_conteiner():
    return render_template('urls.html')
