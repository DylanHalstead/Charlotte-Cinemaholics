from flask import Blueprint, abort, redirect, render_template, request, redirect
from src.models import db, User, Playlist, User_Playlist, Post
from datetime import datetime
from app import session
from src.blueprints.posts_blueprint import getTime
#from app import user

router = Blueprint('account_router', __name__)

@router.get('/username')
def account():
    sessionUser = User.query.filter_by(user_id=session['user']['user_id']).first()
    if 'user' not in session:
        abort('/login')

    user_playlist_name = 'Watchlist'
    #user_playlist = User_Playlist.query.filter_by(user_id = User_Playlist.user_id).all()
    #playlist = Playlist.query.filter_by(user_playlist = User_Playlist.playlist_id).first()
    return render_template('account.html', sessionUser=sessionUser)

@router.get('/username/posts')
def account_posts():
    
    if 'user' not in session:
        abort('/login')
    else:
        sessionUser = User.query.filter_by(user_id=session['user']['user_id']).first()
        posts = Post.query.filter_by(user_id=sessionUser.user_id)
        for post in posts:
            tmp = post.post_time
            post.post_time = getTime(tmp)
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

def createDummyUser(): #dummy users to test post functionality, when logging in gets implemented this will be removed
    if User.query.first() == None:
        user = User(username = "unccstudent", email = "aa", passkey = "sjs", pfp = "pfp1.png", about = " dsh")
        db.session.add(user)
        db.session.commit()
