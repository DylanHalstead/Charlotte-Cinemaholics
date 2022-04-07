from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
from src.blueprints.posts_blueprint import router as posts_router
from src.blueprints.movie_blueprint import router as movie_router
from src.blueprints.account_blueprint import router as account_router

import os
from dotenv import load_dotenv
load_dotenv()
db_user = os.getenv('DB_USER', 'root')
db_pass = os.getenv('DB_PASS')
db_host = os.getenv('DB_HOST', 'localhost')
db_port = os.getenv('DB_PORT', '3306')
db_name = os.getenv('DB_NAME', 'final')
connection_string = f'mysql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}'

app = Flask(__name__)

@app.get('/')
def index():
    return render_template('index.html')

app.register_blueprint(posts_router)
app.register_blueprint(movie_router)
app.register_blueprint(account_router)

@app.get('/report')
def report():
    return render_template('report.html')

@app.get('/username')
def account():
    return render_template('account.html')

@app.get('/username/edit')
def edit_account():
    return render_template("edit_account.html")