from flask import Blueprint, abort, redirect, render_template, request
from models import Post, db
from datetime import datetime

router = Blueprint('account_router', __name__, url_prefix='/account')

@router.get('/edit')
def edit_account():
    return render_template('edit_account.html')
