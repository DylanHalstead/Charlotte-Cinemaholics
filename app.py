from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
from blueprints.posts_blueprint import router as posts_router
from blueprints.movie_blueprint import router as movie_router
from blueprints.account_blueprint import router as account_router

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