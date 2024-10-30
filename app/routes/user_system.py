from flask import (
    Flask,
    jsonify,
    request,
    redirect,
    url_for,
    render_template,
    Blueprint,
    current_app,
)
from app.middlewares.auth import token_required


user_system = Blueprint("user_system", __name__)


@user_system.before_request
@token_required
def check_token():
    pass


@user_system.route("/user")
def index():
    return render_template("user/index.html")


@user_system.route("/user/get_user", methods=["GET"])
def get_user():

    user_sys = current_app.user_system.find({})
    users = []
    for user in user_sys:
        user["_id"] = str(user["_id"])
        users.append(user)

    return jsonify({"data": users, "code": 200})
