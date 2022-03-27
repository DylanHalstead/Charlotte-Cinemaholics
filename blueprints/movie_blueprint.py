from flask import Blueprint, abort, redirect, render_template, request
from models import Post, db
from datetime import datetime

router = Blueprint('movie_router', __name__, url_prefix='/movies')

@router.get('/')
def all_movies():
    return render_template('all_movies.html')