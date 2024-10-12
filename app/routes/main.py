# app/routes/main.py

from flask import Blueprint, render_template, current_app

main = Blueprint('main', __name__)

@main.route('/')
def index():
    print('main: ', current_app.config.get('UPLOAD_FOLDER'))
    return render_template('index.html')
