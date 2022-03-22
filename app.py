from flask import Flask, render_template, request, redirect, url_for
app = Flask(__name__)


@app.get('/')
def index():
    return render_template('index.html')