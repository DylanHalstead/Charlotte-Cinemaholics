from flask import Blueprint, abort, redirect, render_template, request
from datetime import datetime
from src.models import Post, Reply, User, db
import random #need to remove

router = Blueprint('posts_router', __name__, url_prefix='/posts')

@router.get('/')
def all_posts():
    all_posts = Post.query.order_by(Post.post_id.desc()).all()
    users = User.query.all()

    return render_template('all_posts.html', posts=all_posts, users = users)

@router.get('/<post_id>')
def get_post(post_id):
    post = Post.query.get_or_404(post_id)
    replies = Reply.query.filter_by(post_id=post_id)
    users = User.query.all()
    user = User.query.filter_by(user_id=post.user_id).first()
    return render_template('post.html', post = post, replies = replies, user = user, users = users)
    
@router.post('/<post_id>/')
def create_reply(post_id):
    createDummyUsers()
    #user = TODO get current user
    user_id = random.randrange(1,4) #TODO change to actual user
    body = request.form.get('body', '')
    now = datetime.now()
    time = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    likes = 0

    if body == '':
        abort(400)

    reply = Reply(post_id = post_id, user_id=user_id, body=body, post_time = time, likes = likes)
    db.session.add(reply)
    db.session.commit()

    return redirect(f'/posts/{post_id}')


@router.get('/new')
def get_new_post_form():
    return render_template('create_post.html')

@router.post('/')
def create_post():
    createDummyUsers()
    title = request.form.get('title', '')
    print(title)
    #user = TODO get current user
    user_id = random.randrange(1,4) #TODO change to actual user
    body = request.form.get('body', '')
    print(body)
    time = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    print(time)
    likes = 0

    if title == '' or body == '':
        abort(400)

    new_post = Post(title=title, user_id=user_id, body=body, post_time = time, likes = likes)
    db.session.add(new_post)
    db.session.commit()

    return redirect(f'/posts/{new_post.post_id}')




#TODO add edit post page

#TODO add delete post page


def createDummyUsers(): #dummy users to test post functionality, when logging in gets implemented this will be removed
    if User.query.first() == None:
        user = User(username = "unccstudent", email = "aa", passkey = "sjs", pfp = "pfp1.png", about = "")
        user2 = User(username = "austin", email = "p", passkey = "sds", pfp = "pfp5.png", about = "")
        user3 = User(username = "mitchel", email = "d", passkey = "d", pfp = "pfp3.png", about = "")
        db.session.add(user)
        db.session.add(user2)
        db.session.add(user3)
        db.session.commit()
