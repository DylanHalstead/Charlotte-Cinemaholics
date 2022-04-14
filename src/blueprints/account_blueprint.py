from flask import Blueprint, abort, redirect, render_template, request, redirect
from src.models import db, User, Playlist, User_Playlist
from datetime import datetime
from app import session
#from app import user

router = Blueprint('account_router', __name__)

@router.get('/username')
def account():
    createDummyUser()
    user_id = 1
    user = User.query.get_or_404(user_id)
    user2 = User.query.filter_by(user_id=user.user_id).first()
    user_playlist_name = 'Watchlist'
    #user_playlist = User_Playlist.query.filter_by(user_id = User_Playlist.user_id).all()
    #playlist = Playlist.query.filter_by(user_playlist = User_Playlist.playlist_id).first()
    return render_template('account.html', user2=user2)

@router.get('/username/edit')
def get_edit_account():
    return render_template("edit_account.html")

@router.post('/username/edit')
def edit_account():
    if 'user' in session:
        profilePhoto = request.form.get('profilePhoto')
        username = request.form.get('name')
        aboutMe = request.form.get('about')
        user = User.query.filter_by(email = session['user']['email'])
        user.username = username
        user.pfp = profilePhoto
        user.about = aboutMe
        db.session.commit()
        return redirect('/username')
    return redirect('/')

def createDummyUser(): #dummy users to test post functionality, when logging in gets implemented this will be removed
    if User.query.first() == None:
        user = User(username = "unccstudent", email = "aa", passkey = "sjs", pfp = "pfp1.png", about = " dsh")
        db.session.add(user)
        db.session.commit()
