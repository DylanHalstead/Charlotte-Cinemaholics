from flask import Blueprint, abort, redirect, render_template, request, redirect
from src.models import Movie, UserRating, db, User, Post
from datetime import datetime
from app import session
#from app import user

router = Blueprint('account_router', __name__)


@router.get('/username')
def account():
    sessionUser = User.query.filter_by(user_id=session['user']['user_id']).first()
    if 'user' not in session:
        abort('/login')
    userWatchlisted = sessionUser.watchlistMovies
    user = User.query.filter_by(user_id = session['user']['user_id']).first()
    ratedMovies = []
    for userRating in user.movie_rating:
        ratedMov = userRating.movie.to_dict()
        print(userRating)
        ratedMovies.append(ratedMov)
    db.session.commit()
    return render_template('account.html', sessionUser=sessionUser, movies = userWatchlisted, rated = ratedMovies)

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

