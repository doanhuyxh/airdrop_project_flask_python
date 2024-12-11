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
from datetime import datetime
from app.middlewares.auth import token_required
from math import ceil

facebook = Blueprint("facebook", __name__)


@facebook.before_request
@token_required
def check_token():
    pass


@facebook.route("/facebook", methods=["GET"])
def index():
    return render_template("facebook/index.html")


@facebook.route("/facebook/form_get", methods=["GET"])
def form_create():
    return render_template("facebook/form.html")


@facebook.route("/facebook/update_form", methods=["GET"])
def form_update():
    id = request.args.get("id")
    if id:
        facebook_data = current_app.facebook.find_one({"_id": ObjectId(id)})
        facebook_data["_id"] = str(facebook_data["_id"])
        return render_template("facebook/update_form.html", facebook_data=facebook_data)
    return render_template("facebook/update_form.html")


@facebook.route("/facebook/get_devices", methods=["GET"])
def get_devices():
    devices = current_app.facebook.distinct("device")
    return jsonify({"code": 200, "data": devices})


@facebook.route("/facebook/get_data", methods=["POST"])
def get_data():

    device = request.json.get("device")
    search = request.json.get("search")
    page = request.json.get("page")
    pageSize = request.json.get("pageSize")
    order_by = request.json.get("order_by")
    order_type = request.json.get("order_type")

    query = {}

    if device:
        query["device"] = {"$regex": device, "$options": "i"}

    if search:
        query["$or"] = [
            {"account": {"$regex": search, "$options": "i"}},
            {"password": {"$regex": search, "$options": "i"}},
            {"sync_code": {"$regex": search, "$options": "i"}},
            {"sync_code": {"$regex": search, "$options": "i"}},
            {"email_reg_pass": {"$regex": search, "$options": "i"}},
            {"phone": {"$regex": search, "$options": "i"}},
            {"email_recovery": {"$regex": search, "$options": "i"}},
            {"email_recovery_pass": {"$regex": search, "$options": "i"}},
            {"profile_link": {"$regex": search, "$options": "i"}},
            {"facebook_ads": {"$regex": search, "$options": "i"}},
        ]

    if order_by is None:
        order_by = "_id"

    if order_type is None:
        order_type = -1

    total_results = current_app.facebook.count_documents(query)
    total_pages = ceil(total_results / pageSize)
    skip = (page - 1) * pageSize

    facebook_data = (
        current_app.facebook.find(query)
        .sort(order_by, order_type)
        .skip(skip)
        .limit(pageSize)
    )

    data = []
    for detail in facebook_data:
        detail["_id"] = str(detail["_id"])
        if detail["created_at"] is not None:
            detail["created_at"] = datetime.fromisoformat(
                str(detail["created_at"])
            ).strftime("%Y-%m-%d %H:%M:%S")
        data.append(detail)

    return (
        jsonify(
            {
                "code": 200,
                "data": data,
                "page": page,
                "pageSize": pageSize,
                "totalPages": total_pages,
                "totalResults": total_results,
            }
        ),
        200,
    )


@facebook.route("/facebook/save", methods=["POST"])
def save():
    data = request.json
    id = data.get("id")
    account = data.get("account")
    password = data.get("password")
    sync_code = data.get("sync_code")
    email_reg = data.get("email_reg")
    email_reg_pass = data.get("email_reg_pass")
    phone = data.get("phone")
    email_recovery = data.get("email_recovery")
    email_recovery_pass = data.get("email_recovery_pass")
    profile_link = data.get("profile_link")
    facebook_ads = data.get("facebook_ads")
    device = data.get("device")

    key_update = data.get("key_update")
    value_update = data.get("value_update")

    # if id:
    #     current_app.facebook.update_one(
    #         {"_id": ObjectId(id)}, {"$set": {key_update: value_update}}
    #     )

    #     return jsonify({"code": 200, "message": "Dữ liệu đã được cập nhật"})

    if id:
        current_app.facebook.update_one(
            {"_id": ObjectId(id)},
            {
                "$set": {
                    "account": account,
                    "password": password,
                    "sync_code": sync_code,
                    "email_reg": email_reg,
                    "email_reg_pass": email_reg_pass,
                    "phone": phone,
                    "email_recovery": email_recovery,
                    "email_recovery_pass": email_recovery_pass,
                    "profile_link": profile_link,
                    "facebook_ads": facebook_ads,
                    "device": device,
                }
            },
        )

        return jsonify({"code": 200, "message": "Dữ liệu đã được cập nhật"})

    check_exit = current_app.facebook.find_one(
        {
            "$or": [
                {"account": account},
                {"email_reg": email_reg},
            ]
        }
    )

    if check_exit is not None:
        current_app.facebook.update_one(
            {"_id": check_exit["_id"]},
            {
                "$set": {
                    "password": password,
                    "sync_code": sync_code,
                    "email_reg_pass": email_reg_pass,
                    "phone": phone,
                    "email_recovery": email_recovery,
                    "email_recovery_pass": email_recovery_pass,
                    "profile_link": profile_link,
                    "facebook_ads": facebook_ads,
                    "device": device,
                }
            },
        )
    else:
        current_app.facebook.insert_one(
            {
                "account": account,
                "password": password,
                "sync_code": sync_code,
                "email_reg": email_reg,
                "email_reg_pass": email_reg_pass,
                "phone": phone,
                "email_recovery": email_recovery,
                "email_recovery_pass": email_recovery_pass,
                "profile_link": profile_link,
                "facebook_ads": facebook_ads,
                "device": device,
                "created_at": datetime.now(),
            }
        )

    return jsonify({"code": 200, "message": "Dữ liệu đã được thêm mới"})


@facebook.route("/facebook/delete", methods=["GET"])
def delete():
    id = request.args.get("id")
    current_app.facebook.delete_one({"_id": ObjectId(id)})
    return jsonify({"code": 200, "message": "Dữ liệu đã được xóa"})
