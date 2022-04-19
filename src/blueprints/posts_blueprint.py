from flask import Blueprint, abort, redirect, render_template, request, session
from datetime import datetime, timedelta
from src.models import Edits, Post, Reply, User, db
import math

router = Blueprint('posts_router', __name__, url_prefix='/posts')

@router.get('/')
def all_posts():
    all_posts = Post.query.order_by(Post.post_id.desc()).all()
    for post in all_posts:
        old_time = post.post_time
        post.post_time = getTime(old_time)
        
    users = User.query.all()

    return render_template('all_posts.html', posts=all_posts, users = users)

@router.get('/<post_id>')
def get_post(post_id):
    post = Post.query.get_or_404(post_id)
    old_time = post.post_time
    post.post_time = getTime(old_time)

    replies = Reply.query.filter_by(post_id=post_id)
    edits = Edits.query.filter_by(post_id=post_id)

    reply_edits = []
    for reply in replies:
        old_time = reply.post_time
        reply.post_time = getTime(old_time)

        temp = []
        for edit in edits:
            if edit.reply_id != None and reply.reply_id == edit.reply_id:
                old_time = edit.time
                edit.time = getTime(old_time)
                temp.append(edit)
        if len(temp) != 0:
            reply_edits.append(temp[len(temp)-1]) 
    
        
    descending = Edits.query.order_by(Edits.edit_id.desc()).filter_by(post_id=post_id, reply_id = None)

    post_edit = descending.first()
    if post_edit != None:
        old_time = post_edit.time
        post_edit.time = getTime(old_time)

    users = User.query.all()
    user = User.query.filter_by(user_id=post.user_id).first()
    return render_template('post.html', post = post, replies = replies, user = user, users = users, post_e = post_edit, reply_e = reply_edits)


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
    reason = request.form.get('reason', '')
    time = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    edit = Edits(user_id = session['user'].get('user_id'), post_id = post_id, reason = reason, time = time)
    if body == '' or title == '':
        abort(400)

    post.title = title
    post.body = body
    db.session.add(edit)
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
    reason = request.form.get('reason', '')
    time = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    edit = Edits(user_id = session['user'].get('user_id'),post_id = reply.post_id, reply_id = reply_id, reason = reason, time = time)

    if body == '':
        abort(400)

    reply.body = body
    db.session.add(edit)
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

def getTime(time_str):
    datetime_object = datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S')
    now = datetime.now()
    time = now - datetime_object
    print(time.days)
    if time.days > 365:
        years = math.floor(time.days/365)
        if years == 1:
            return str(years) + " year ago"
        return str(years) + " years ago"
    elif time.days > 30:
        months = math.floor(time.days/30)
        if months == 1:
            return str(months) + " month ago"
        return str(months) + " months ago"
    elif time.days > 7:
        weeks = math.floor(time.days/7)
        if weeks == 1:
            return str(weeks) + " week ago"
        return str(weeks) + " weeks ago"
    elif time.days < 1: 
        hour = int(time.seconds / 3600)
        if hour < 1:
            minute = int(time.seconds / 60)
            if minute < 1:
                return "just now"
            if minute == 1:
                return str(minute) + " ago"
            return str(minute) + "s ago"
    else: 
        return str(time.days) + " days ago"


def createDummyUsers(): #dummy users to test post functionality
    if User.query.first() == None:
        user = User(username = "unccstudent", email = "aa", passkey = "sjs", pfp = "pfp1.png", about = "")
        user2 = User(username = "austin", email = "p", passkey = "sds", pfp = "pfp5.png", about = "")
        user3 = User(username = "mitchel", email = "d", passkey = "d", pfp = "pfp3.png", about = "")
        db.session.add(user)
        db.session.add(user2)
        db.session.add(user3)
        db.session.commit()
