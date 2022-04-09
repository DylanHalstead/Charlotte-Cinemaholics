from flask import Blueprint, abort, redirect, render_template, request
from src.models import db, User, Playlist, User_Playlist
from datetime import datetime

router = Blueprint('account_router', __name__)

@router.get('/username')
def account():
    createDummyUser()
    user_id = 1
    user = User.query.get_or_404(user_id)
    user2 = User.query.filter_by(user_id=user.user_id).first()
    user_playlist_name = 'Watchlist'
    #user_playlist = Playlist.query.filter_by(user_id = User_Playlist.playlist_id).all()
    #playlist = Playlist.query.filter_by(user_playlist = Playlist.playlist_id).first()
    return render_template('account.html', user2=user2)

@router.get('/username/edit')
def edit_account():
    
    return render_template("edit_account.html")

def createDummyUser(): #dummy users to test post functionality, when logging in gets implemented this will be removed
    if User.query.first() == None:
        user = User(username = "unccstudent", email = "aa", passkey = "sjs", pfp = "pfp1.png", about = " dsh")
        db.session.add(user)
        db.session.commit()