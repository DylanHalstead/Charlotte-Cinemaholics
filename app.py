import os
from flask import Flask, render_template, request, redirect, url_for, session, abort
from datetime import datetime
from src.blueprints.posts_blueprint import router as posts_router
from src.blueprints.movie_blueprint import router as movie_router
from src.blueprints.account_blueprint import router as account_router
from src.models import db, User
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv

load_dotenv()
db_user = os.getenv('DB_USER', 'root')
db_pass = os.getenv('DB_PASS', '12345')
db_host = os.getenv('DB_HOST', 'localhost')
db_port = os.getenv('DB_PORT', '3306')
db_name = os.getenv('DB_NAME', 'cinemaholics_db')
connection_string = f'mysql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}'


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = connection_string
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
bcrypt = Bcrypt(app)

db.init_app(app)

@app.get('/')
def index():
    if 'user' in session:
        return render_template('index.html')
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

# Login and Sign in Page
@app.get('/login')
def get_login():
    if 'user' in session:
        return render_template('/')
    return render_template('signin.html')

@app.post('/login')
def login():
    email = request.form.get('email', '')
    password = request.form.get('password', '')

    if email == '' or password == '':
        abort(400)

    existing_user = User.query.filter_by(email=email).first()

    if not existing_user or existing_user.user_id == 0:
        return redirect('/fail')

    if not bcrypt.check_password_hash(existing_user.passkey, password):
        return redirect('/fail')

    session['user'] = {
        'email': email,
        'user_id': existing_user.user_id,
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

    # Make sure user follows requirements creating an account
    if (email == '' or '@uncc.edu' not in email or username == '' or len(username) > 15 or ' ' in password or username == '' or len(password) < 8 or ' ' in password):
        abort(400)

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    new_user = User(email=email, username=username, passkey=hashed_password, pfp=userPfp)
    db.session.add(new_user)
    db.session.commit()

    # Go ahead and log in user once they're in the database
    session['user'] = {
        'username': username,
        'user_id': new_user.user_id,
        'pfp': new_user.pfp
    }

    return redirect('/')

@app.get('/fail')
def fail():
    return render_template('fail.html')