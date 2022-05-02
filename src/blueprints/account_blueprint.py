from flask import Blueprint, abort, redirect, render_template, request, redirect
<<<<<<< HEAD
from sqlalchemy import true
from src.models import Movie, db, User, Post
from datetime import datetime
=======
from src.models import db, User, Playlist, User_Playlist, Post
>>>>>>> main
from app import session
#from app import user

router = Blueprint('account_router', __name__)


@router.get('/username')
def account():
    sessionUser = User.query.filter_by(user_id=session['user']['user_id']).first()
    if 'user' not in session:
        abort('/login')
    #userWatch = grab_watchlist()
    #need to grab the watchlisted movies id's then in render_template make movies=that variable
    return render_template('account.html', sessionUser=sessionUser)

@router.get('/username/posts')
def account_posts():
    
    if 'user' not in session:
        abort('/login')
    else:
        sessionUser = User.query.filter_by(user_id=session['user']['user_id']).first()
        posts = Post.query.filter_by(user_id=sessionUser.user_id)
        return render_template('account_posts.html', user=sessionUser, posts = posts)

@router.get('/username/edit')
def get_edit_account():
    return render_template("edit_account.html")

@router.post('/username/edit')
def edit_account():
    if 'user' in session:
        profilePhoto = request.form.get('profilePhoto')
        username = request.form.get('username')
        aboutMe = request.form.get('about')
        user = User.query.filter_by(email = session['user']['email']).first()
        print(user.pfp)
        user.username = username
        user.pfp = profilePhoto
        user.about = aboutMe
        session['user'] = {
            'email': user.email,
            'username': user.username,
            'user_id': user.user_id,
            'pfp': user.pfp
        }
        db.session.commit()
        return redirect('/username')
    return redirect('/')

