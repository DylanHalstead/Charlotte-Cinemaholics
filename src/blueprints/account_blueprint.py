from flask import Flask, Blueprint, abort, redirect, render_template, request, session
from src.models import db
from datetime import datetime
from flask_bcrypt import Bcrypt

router = Blueprint('account_router', __name__, url_prefix='/account')

app = Flask(__name__)
bcrypt = Bcrypt(app)

@router.get('/edit')
def edit_account():
    return render_template('edit_account.html')
