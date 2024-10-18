
from flask import Flask, jsonify, request, redirect, url_for, render_template, Blueprint
from app.middlewares.auth import token_required


user_system = Blueprint('user_system', __name__)

@user_system.before_request
@token_required
def check_token():
    pass

@user_system.route('/user')
def index():
    return render_template('user/index.html')
