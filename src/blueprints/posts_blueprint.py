from flask import Blueprint, abort, redirect, render_template, request, session, url_for
from datetime import datetime, timedelta

import sqlalchemy
from src.models import Edits, Post, Reply, User, db, PostLike, ReplyLike, Reply_Quote
from sqlalchemy import func

router = Blueprint('posts_router', __name__, url_prefix='/posts')

@router.get('/')
def all_posts():
    searched = request.args.get('search')
    sort = request.args.get("sort")
    if searched != None:
        all_posts = Post.query.filter(Post.title.contains(searched))
        if sort == "oldest":
            all_posts = all_posts.order_by(Post.post_id).all()
        elif sort == "latest":
            all_posts =all_posts.order_by(Post.post_id.desc()).all()  
        elif sort == "liked":
            query_posts = db.session.query(Post, func.count(PostLike.user_id).label('total')).join(PostLike).group_by(Post).order_by(sqlalchemy.sql.text('total DESC'))
            all_posts = []
            for row in query_posts:
                p = row._mapping.get("Post")
                if searched in p.title:
                    all_posts.append(p)
        else: #default to latest
            all_posts =all_posts.order_by(Post.post_id.desc()).all()
            return render_template('all_posts.html', posts=all_posts, searched = searched)
    else:
        if sort == "oldest":
            all_posts = Post.query.order_by(Post.post_id).all()
        elif sort == "latest":
            all_posts = Post.query.order_by(Post.post_id.desc()).all()
        elif sort == "liked":
            query_posts = db.session.query(Post, func.count(PostLike.user_id).label('total')).join(PostLike).group_by(Post).order_by(sqlalchemy.sql.text('total DESC'))
            all_posts = []
            for row in query_posts:
                p = row._mapping.get("Post")
                all_posts.append(p)
        else: #default to latest
            all_posts = Post.query.order_by(Post.post_id.desc()).all()
    
    return render_template('all_posts.html', posts=all_posts, sort = sort, searched = searched)

@router.get('/<post_id>')
def get_post(post_id):
    post = Post.query.get_or_404(post_id)
    replies = Reply.query.filter_by(post_id=post_id)
    users = User.query.all()
    user = User.query.get(post.user_id)
    s_u = None
    if 'user' in session:
        user_id = session['user'].get('user_id')
        s_u = User.query.get(user_id)

    return render_template('post.html', post = post, replies = replies, user = user, users = users, session_user = s_u)


@router.get('/new')
def get_new_post_form():
    if 'user' in session:
        return render_template('create_post.html')
    else: 
        return redirect('/posts/')

@router.post('/')
def create_post():
    title = request.form.get('title', '')
    user_id = session['user'].get('user_id')
    body = request.form.get('body', '')
    time = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    
    if title == '' or body == '':
        abort(400)
    new_post = Post(title=title, user_id=user_id, body=body, post_time = time)
    db.session.add(new_post)
    db.session.commit()
    current_user = User.query.get(user_id)
    current_user.like_post(new_post)
    db.session.commit()

    return redirect(f'/posts/{new_post.post_id}')

@router.get('/<int:post_id>/reply/<int:reply_id>/quote')
def get_create_reply_form(post_id, reply_id): 
    reply = Reply.query.get_or_404(reply_id)
    if 'user' in session:
        return render_template('create_reply.html', reply = reply)
    return redirect(f'/posts/{reply.post_id}#reply-{reply.reply_id}')

@router.post('/<int:post_id>/reply/<int:reply_id>/quote')
def create_quote_reply(post_id, reply_id): 
    if 'user' in session:
        user_id = session['user'].get('user_id')
        body = request.form.get('body', '')
        time = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        
        if body == '':
            abort(400)

        reply = Reply(post_id = post_id, user_id=user_id, body=body, post_time = time)
        db.session.add(reply)
        db.session.commit()
        quote = Reply_Quote(reply_id = reply.reply_id, parent_id = reply_id)
        db.session.add(quote)
        db.session.commit()

        current_user = User.query.get(user_id)
        current_user.like_reply(reply)
        db.session.commit()
    return redirect(f'/posts/{reply.post_id}#reply-{reply.reply_id}')

@router.post('/<int:post_id>')
def create_reply(post_id):
    #createDummyUsers()
    if 'user' in session:
        user_id = session['user'].get('user_id')
        body = request.form.get('body', '')
        time = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        
        if body == '':
            abort(400)

        reply = Reply(post_id = post_id, user_id=user_id, body=body, post_time = time)
        db.session.add(reply)
        db.session.commit()

        current_user = User.query.get(user_id)
        current_user.like_reply(reply)
        db.session.commit()

    return redirect(f'/posts/{post_id}#reply-{reply.reply_id}')

@router.get('/<int:post_id>/edit')
def get_edit_post_form(post_id): 
    #TODO add check if user is a moderator as well
    post_to_edit = Post.query.get_or_404(post_id)
    if 'user' in session:
        user_id = session['user'].get('user_id')
        user = User.query.get(user_id)
        if post_to_edit.user_id == user_id or user.isAdmin():
            return render_template('edit_post.html', post=post_to_edit)
    return redirect(f'/posts/{post_id}')

@router.post('/<int:post_id>/edit')
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
    reply = Reply.query.get_or_404(reply_id)
    
    if 'user' in session:
        user_id = session['user'].get('user_id')
        usr = User.query.get(user_id)
        if reply.user_id == user_id or usr.isAdmin():
            return render_template('edit_reply.html', reply = reply)
            
    return redirect(f'/posts/{reply.post_id}#reply-{reply.reply_id}')

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
    return redirect(f'/posts/{reply.post_id}#reply-{reply.reply_id}')

@router.post('/<int:post_id>/delete')
def delete_post(post_id):
    post_to_delete = Post.query.get_or_404(post_id)
    if 'user' in session:
        user_id = session['user'].get('user_id')
        user = User.query.get(user_id)
        if post_to_delete.user_id == user_id or user.isAdmin():
            PostLike.query.filter_by(post_id=post_id).delete()
            Edits.query.filter_by(post_id=post_id).delete()

            replies = Reply.query.filter_by(post_id=post_id)
            for reply in replies:
                Edits.query.filter_by(reply_id=reply.reply_id).delete()
                ReplyLike.query.filter_by(reply_id=reply.reply_id).delete()
                Reply_Quote.query.filter_by(reply_id=reply.reply_id).delete()

            Reply.query.filter_by(post_id=post_id).delete()
            
            db.session.delete(post_to_delete)
            db.session.commit()
            return redirect('/posts/')
    return redirect('/posts/{post_id}')

@router.post('/<int:post_id>/reply/<int:reply_id>/delete')
def delete_reply(post_id, reply_id):
    post_to_delete = Reply.query.get_or_404(reply_id)
    if 'user' in session:
        p_id = post_to_delete.post_id
        user_id = session['user'].get('user_id')
        user = User.query.get(user_id)
        if post_to_delete.user_id == user_id or user.isAdmin():
            edits = Edits.query.filter_by(reply_id=reply_id)
            for edit in edits:
                edit.reply_id = None
            ReplyLike.query.filter_by(reply_id=reply_id).delete()
            Reply_Quote.query.filter_by(reply_id=reply_id).delete()
            quoted = Reply_Quote.query.filter_by(parent_id=reply_id)
            for q in quoted:
                q.parent_id = -1
                db.session.add(q)
            db.session.delete(post_to_delete)
            db.session.commit()
            return redirect(f'/posts/{post_id}')
    return redirect(f'/posts/{post_id}')

@router.route('/like/<int:post_id>/<action>')
def like_action(post_id, action):
    post = Post.query.filter_by(post_id=post_id).first_or_404()
    if 'user' in session:
        user_id = session['user'].get('user_id')
        current_user = User.query.get(user_id)
        if action == 'like':
            current_user.like_post(post)
            db.session.commit()
        if action == 'unlike':
            current_user.unlike_post(post)
            db.session.commit()
        return redirect(request.referrer)

@router.route('/like/<int:post_id>/<int:reply_id>/<action>')
def like_action_reply(post_id,reply_id, action):
    reply = Reply.query.filter_by(reply_id=reply_id).first_or_404()
    if 'user' in session:
        user_id = session['user'].get('user_id')
        current_user = User.query.get(user_id)
        if action == 'like':
            current_user.like_reply(reply)
            db.session.commit()
        if action == 'unlike':
            current_user.unlike_reply(reply)
            db.session.commit()
        return redirect(request.referrer)


# ⣞⢽⢪⢣⢣⢣⢫⡺⡵⣝⡮⣗⢷⢽⢽⢽⣮⡷⡽⣜⣜⢮⢺⣜⢷⢽⢝⡽⣝ 
#⠸⡸⠜⠕⠕⠁⢁⢇⢏⢽⢺⣪⡳⡝⣎⣏⢯⢞⡿⣟⣷⣳⢯⡷⣽⢽⢯⣳⣫⠇ 
#⠀⠀⢀⢀⢄⢬⢪⡪⡎⣆⡈⠚⠜⠕⠇⠗⠝⢕⢯⢫⣞⣯⣿⣻⡽⣏⢗⣗⠏⠀ 
#⠀⠪⡪⡪⣪⢪⢺⢸⢢⢓⢆⢤⢀⠀⠀⠀⠀⠈⢊⢞⡾⣿⡯⣏⢮⠷⠁⠀⠀
#⠀⠀⠀⠈⠊⠆⡃⠕⢕⢇⢇⢇⢇⢇⢏⢎⢎⢆⢄⠀⢑⣽⣿⢝⠲⠉⠀⠀⠀⠀
#⠀⠀⠀⠀⠀⡿⠂⠠⠀⡇⢇⠕⢈⣀⠀⠁⠡⠣⡣⡫⣂⣿⠯⢪⠰⠂⠀⠀⠀⠀
#⠀⠀⠀⠀⡦⡙⡂⢀⢤⢣⠣⡈⣾⡃⠠⠄⠀⡄⢱⣌⣶⢏⢊⠂⠀⠀⠀⠀⠀⠀
#⠀⠀⠀⠀⢝⡲⣜⡮⡏⢎⢌⢂⠙⠢⠐⢀⢘⢵⣽⣿⡿⠁⠁⠀⠀⠀⠀⠀⠀⠀
#⠀⠀⠀⠀⠨⣺⡺⡕⡕⡱⡑⡆⡕⡅⡕⡜⡼⢽⡻⠏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
#⠀⠀⠀⠀⣼⣳⣫⣾⣵⣗⡵⡱⡡⢣⢑⢕⢜⢕⡝⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
#⠀⠀⠀⣴⣿⣾⣿⣿⣿⡿⡽⡑⢌⠪⡢⡣⣣⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
#⠀⠀⠀⡟⡾⣿⢿⢿⢵⣽⣾⣼⣘⢸⢸⣞⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
#⠀⠀⠀⠀⠁⠇⠡⠩⡫⢿⣝⡻⡮⣒⢽⠋

#          No Posts?