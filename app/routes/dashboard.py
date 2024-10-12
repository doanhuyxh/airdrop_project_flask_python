
from flask import Flask, jsonify, request, redirect, url_for, render_template, Blueprint
from app.middlewares.auth import token_required

dashboard = Blueprint('dashboard', __name__)

@dashboard.before_request
@token_required
def check_token():
    pass

@dashboard.route('/dashboard', methods=['GET'])
def index():
    print('dashboard: ', request.current_user_id)
    return render_template('dashboard/index.html')

