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
from bson import ObjectId

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

@user_system.route("/user/update", methods=["POST"])
def update_data():
    data = request.json
    id = data.get("id")
    key_update = data.get("key_update")
    value_update = data.get("value_update")
    
    if not id or not key_update or not value_update:
        return jsonify({"code": 400, "message": "Thiếu thông tin"}), 200
    
    current_app.user_system.update_one({"_id": ObjectId(id)}, {"$set": {key_update: value_update}})
    
    return jsonify({"code": 200, "message": "Update successfully"})
    