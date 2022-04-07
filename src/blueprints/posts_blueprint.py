from flask import Blueprint, abort, redirect, render_template, request
from datetime import datetime

router = Blueprint('posts_router', __name__, url_prefix='/posts')

@router.get('/')
def all_posts():
    return render_template('all_posts.html')

@router.get('/<post_id>')
def get_post(post_id):
    return render_template('post.html')
    

@router.get('/new')
def create_post():
    return render_template('create_post.html')

#TODO add edit post page

#TODO add delete post page
