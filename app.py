import os
from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
from blueprints.posts_blueprint import router as posts_router
from blueprints.movie_blueprint import router as movie_router
from blueprints.account_blueprint import router as account_router
from dotenv import load_dotenv

load_dotenv()
db_user = os.getenv('DB_USER', 'root')
db_pass = os.getenv('DB_PASS')
connection_string = f'mysql://{db_user}:{db_pass}@localhost:3306/final'

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