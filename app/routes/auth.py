from flask import (
    Flask,
    jsonify,
    request,
    redirect,
    url_for,
    render_template,
    current_app,
    Blueprint,
    make_response
)
from datetime import datetime, timedelta
from bson import ObjectId
import threading

from app.ultils.time_ultils import get_current_time, check_time_difference
from app.ultils.jwt_token import create_token, create_refresh_token
from app.middlewares.auth import clear_cookies

auth = Blueprint("auth", __name__)

@auth.route("/login", methods=["GET"])
def login():
    return render_template("auth/login.html")

@auth.route("/login", methods=["POST"])
def login_post():
    data = request.json
    username = data.get("username")
    password = data.get("password")
    
    if not username or not password:
        return jsonify({"code": 400, "message": "Thiếu username hoặc password"}), 200
    
    user = current_app.user_system.find_one({"username": username, "password": password})
    if not user:
        return jsonify({"code": 405, "message": "Tài khoản không tồn tại"}), 200
    
    
    if user.get("status") == "de_active":
        return jsonify({"code": 405, "message": "Tài khoản chưa kích hoạt"}), 200
    
    if user.get("status") == "block":
        return jsonify({"code": 405, "message": "Tài khoản đã bị khóa"}), 200
    
    token = create_token(str(user.get("_id")), user.get("username"))
    refresh_token = create_refresh_token(str(user.get("_id")), user.get("username"))
    response = jsonify({"code": 200, "message": "Login successfully", "token": token})
    response.set_cookie('token', token, httponly=True, secure=True, path='/', expires=datetime.now() + timedelta(minutes=10))
    response.set_cookie('refresh_token', refresh_token, httponly=True, secure=True,  path='/', expires=datetime.now() + timedelta(days=1))
    
    
    return response, 200
    


@auth.route("/register", methods=["GET"])
def register():
    return render_template("auth/register.html")


@auth.route("/register", methods=["POST"])
def register_post():
    data = request.json
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    if not username or not password or not email:
        return (
            jsonify({"code": 400, "message": "Thiếu username, email hoặc password"}),
            200,
        )

    check_exit_user = current_app.user_system.find_one({"username": username})

    if check_exit_user:
        return jsonify({"code": 202, "message": "Tài khoản đã tồn tại"}), 200

    current_app.user_system.insert_one(
        {
            "username": username,
            "email": email,
            "password": password,
            "role":"user",
            "status":"de_active",
            "created_at": datetime.now(),
        }
    )

    return jsonify({"code": 200, "message": "Register successfully"}), 200


@auth.route("/logout", methods=["GET"])
@clear_cookies
def logout():
    return redirect("/login")