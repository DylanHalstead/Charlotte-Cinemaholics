import os
from flask import Flask, render_template, request, redirect, url_for, session, abort, send_from_directory
from datetime import datetime
from src.blueprints.posts_blueprint import router as posts_router
from src.blueprints.movie_blueprint import router as movie_router, imdbpy, top_films, trending, worst_films, add_movie, get_rated_IDs
from src.blueprints.account_blueprint import router as account_router
from src.models import db, User, Movie, Issue
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy


load_dotenv()

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('CLEARDB_DATABASE_URL', 'sqlite:///test.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

bcrypt = Bcrypt(app)
app.secret_key = os.getenv('SECRET_KEY')

db.init_app(app)

@app.get('/')
def index(): 
    # Grab first 5 top films
    for movie in range(5):
        if not isinstance(top_films[movie], dict):
            pass
            add_movie(top_films[movie])
            top_films[movie] = Movie.query.filter_by(movie_id=top_films[movie].movieID).first().to_dict()
    # Grab first 5 trending films
    for movie in range(5):
        if not isinstance(trending[movie], dict):
            pass
            add_movie(trending[movie])
            trending[movie] = Movie.query.filter_by(movie_id=trending[movie].movieID).first().to_dict()
    # Grab first 5 watchlisted films if user's signed in
    if 'user' in session:
        sessionUser = User.query.filter_by(user_id=session['user']['user_id']).first()
        userWatchlisted = sessionUser.watchlistMovies
        updatedWatchlist = []
        # Regrab data incase rated
        for watchlist in range(len(userWatchlisted)):
            updatedWatchlist.append(userWatchlisted[watchlist].to_dict())
        ratedMovies = get_rated_IDs()
    else:
        ratedMovies = []
        updatedWatchlist = []
        userWatchlisted = 0
    
    return render_template('index.html', top_films=top_films, popular_films=trending, movies=updatedWatchlist, ratedMovies=ratedMovies)

app.register_blueprint(posts_router)
app.register_blueprint(movie_router)
app.register_blueprint(account_router)

# app.add_url_rule('/favicon.ico', redirect_to=url_for('static', filename='logos/cinemaholics.ico'))
@app.get('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/png')


@app.get('/report')
def report():
    return render_template('report.html')

@app.get('/username/edit')
def edit_account():
    if 'user' in session:
        return render_template("edit_account.html")
    abort(401)

# Login and Sign in Page
@app.get('/login')
def get_login():
    if 'user' in session:
        return redirect('/')
    return render_template('login.html')

@app.post('/login')
def login():
    email = request.form.get('email', '')
    password = request.form.get('password', '')

    if email == '' or password == '':
        abort(401)

    existing_user = User.query.filter_by(email=email).first()
    if not existing_user or existing_user.user_id == 0:
        abort(401)

    if not bcrypt.check_password_hash(existing_user.passkey, password):
        abort(401)

    session['user'] = {
        'email': existing_user.email,
        'username': existing_user.username,
        'user_id': existing_user.user_id,
        'pfp': existing_user.pfp
    }

    return redirect('/')

@app.get('/register')
def get_register():
    if 'user' in session:
        return render_template('/')
    return render_template('register.html')

@app.post('/register')
def register():
    email = request.form.get('email', '')
    userPfp = request.form.get('profilePhoto', 'default_user.png')
    username = request.form.get('username', '')
    password = request.form.get('password', '')

    if email == '' or '@uncc.edu' not in email or username == '' or password == '':
        abort(400)

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    if User.query.filter_by(username = username).count() > 0:
        return render_template('register.html', error = f'{username} is not available')
    if User.query.filter_by(email = email).count() > 0:
        return render_template('register.html', error = f'{email} has already been used')

    new_user = User(email=email, username=username, passkey=hashed_password, pfp=userPfp)
    db.session.add(new_user)
    db.session.commit()

    # Go ahead and log in user once they're in the database
    session['user'] = {
        'email': new_user.email,
        'username': new_user.username,
        'user_id': new_user.user_id,
        'pfp': new_user.pfp
    }


    return redirect('/')

@app.get('/logout')
def logout():
    if 'user' not in session:
        abort(401)
    del session['user']
    return redirect('/')

@app.get('/fail')
def fail():
    return render_template('fail.html')

@app.get('/filter/watchlist')
def filter_watchlist():
    if 'user' in session:
        sessionUser = User.query.filter_by(user_id=session['user']['user_id']).first()
        userWatchlisted = sessionUser.watchlistMovies
    else:
        abort(401)
    return render_template('watchlist.html', movies = userWatchlisted, user = sessionUser)

@app.get('/filter/rated')
def filter_ratings():
    if 'user' in session:
        user = User.query.filter_by(user_id = session['user']['user_id']).first()
        ratedMovies = []
        for userRating in user.movie_rating:
            ratedMov = userRating.movie.to_dict()
            ratedMovies.append(ratedMov)
        db.session.commit()
    else:
        abort(400)
    return render_template('rated_movies.html', movies = ratedMovies, user = user)

@app.post('/report')
def report_email():
    issueTitle = request.form.get('issuetitle')
    issueText = request.form.get('issuetext')
    userEmail = request.form.get('email')
    newIssue = Issue(users_email = userEmail, issue_title = issueTitle, issue_text = issueText)
    db.session.add(newIssue)
    db.session.commit()
    return redirect('/')

# Server Errors
# Server cant return response bc an issue with user browser
@app.errorhandler(400)
def bad_request(e):
    return render_template('400.html'), 400

# Unauthorized; Used when you try to log in and the server can't identify you
@app.errorhandler(401)
def unauthorized_credientials(e):
    return render_template('401.html'), 401

# Forbidden; When a user tries to see something they are not allowed to see
@app.errorhandler(403)
def forbidden_request(e):
    return render_template('403.html'), 403

# Not Found
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404