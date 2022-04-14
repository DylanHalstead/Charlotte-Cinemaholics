from flask import Blueprint, abort, redirect, render_template, request, session
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


@router.get('/new')
def get_new_post_form():
    if 'user' in session:
        return render_template('create_post.html')
    else: 
        return redirect('/posts/')

@router.post('/')
def create_post():
    title = request.form.get('title', '')
    print(title)
    #user = TODO get current user

    user_id = session['user'].get('user_id')
    body = request.form.get('body', '')
    time = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    likes = 0

    if title == '' or body == '':
        abort(400)

    new_post = Post(title=title, user_id=user_id, body=body, post_time = time, likes = likes)
    db.session.add(new_post)
    db.session.commit()

    return redirect(f'/posts/{new_post.post_id}')

@router.post('/<post_id>')
def create_reply(post_id):
    #createDummyUsers()
    if 'user' in session:
        user_id = session['user'].get('user_id')
        body = request.form.get('body', '')
        time = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        likes = 0

        if body == '':
            abort(400)

        reply = Reply(post_id = post_id, user_id=user_id, body=body, post_time = time, likes = likes)
        db.session.add(reply)
        db.session.commit()

    return redirect(f'/posts/{post_id}')

#TODO add edit post page
@router.get('/<post_id>/edit')
def get_edit_post_form(post_id): 
    #TODO add check if user is a moderator as well
    post_to_edit = Post.query.get_or_404(post_id)
    if 'user' in session:
        user_id = session['user'].get('user_id')
        if post_to_edit.user_id == user_id:
            return render_template('edit_post.html', post=post_to_edit)
            
    return redirect(f'/posts/{post_id}')

@router.post('/<post_id>/edit')
def update_post(post_id): 
    post = Post.query.get_or_404(post_id)
    title = request.form.get('title', '')
    body = request.form.get('body', '')

    if body == '' or title == '':
        abort(400)

    post.title = title
    post.body = body

    db.session.commit()

    return redirect(f'/posts/{post_id}')


@router.get('/<int:post_id>/reply/<int:reply_id>/edit')
def get_edit_reply_form(post_id, reply_id): 
    #TODO add check if user is a moderator as well
    reply = Reply.query.get_or_404(reply_id)
    
    if 'user' in session:
        user_id = session['user'].get('user_id')
        if reply.user_id == user_id:
            return render_template('edit_reply.html', reply = reply)
            
    return redirect(f'/posts/{reply.post_id}')

@router.post('/<int:post_id>/reply/<int:reply_id>/edit')
def edit_reply(post_id, reply_id): 
    reply = Reply.query.get_or_404(reply_id)
    body = request.form.get('body', '')

    if body == '':
        abort(400)

    reply.body = body

    db.session.commit()

    return redirect(f'/posts/{reply.post_id}')




#TODO add delete post page
@router.post('/<post_id>/delete')
def delete_post(post_id):
    post_to_delete = Post.query.get_or_404(post_id)
    if 'user' in session:
        user_id = session['user'].get('user_id')
        if post_to_delete.user_id == user_id:
            db.session.delete(post_to_delete)
            db.session.commit()
            return redirect('/posts/')
    return redirect('/posts/{post_id}')

@router.post('/<int:post_id>/reply/<int:reply_id>/delete')
def delete_reply(post_id, reply_id):
    post_to_delete = Reply.query.get_or_404(reply_id)
    if 'user' in session:
        user_id = session['user'].get('user_id')
        if post_to_delete.user_id == user_id:
            db.session.delete(post_to_delete)
            db.session.commit()
            return redirect('/posts/')
    return redirect('/posts/{post_id}')


def createDummyUsers(): #dummy users to test post functionality
    if User.query.first() == None:
        user = User(username = "unccstudent", email = "aa", passkey = "sjs", pfp = "pfp1.png", about = "")
        user2 = User(username = "austin", email = "p", passkey = "sds", pfp = "pfp5.png", about = "")
        user3 = User(username = "mitchel", email = "d", passkey = "d", pfp = "pfp3.png", about = "")
        db.session.add(user)
        db.session.add(user2)
        db.session.add(user3)
        db.session.commit()
