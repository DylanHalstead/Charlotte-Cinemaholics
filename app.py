from flask import Flask, render_template, request, redirect, url_for
app = Flask(__name__)


@app.get('/')
def index():
    return render_template('index.html')

@app.get('/movies')
def all_movies():
    return render_template('all_movies.html')

@app.get('/posts')
def all_posts():
    return render_template('all_posts.html')

@app.get('/create-post')
def create_post():
    return render_template('create_post.html')

@app.get('/edit-account')
def edit_account():
    return render_template('edit_account.html')

@app.get('/report')
def report():
    return render_template('report.html')

@app.get('/username')
def account():
    return render_template('account.html')