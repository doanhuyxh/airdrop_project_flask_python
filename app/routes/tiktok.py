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

tiktok = Blueprint("tiktok", __name__)


@tiktok.before_request
@token_required
def check_token():
    pass


@tiktok.route("/tiktok", methods=["GET"])
def index():
    return render_template("tiktok/index.html")


@tiktok.route("/tiktok/form_get", methods=["GET"])
def form_create():
    return render_template("tiktok/form.html")


@tiktok.route("/tiktok/update_form", methods=["GET"])
def form_update():
    id = request.args.get("id")
    if id:
        tiktok_data = current_app.tiktok.find_one({"_id": ObjectId(id)})
        tiktok_data["_id"] = str(tiktok_data["_id"])
        return render_template("tiktok/update_form.html", tiktok=tiktok_data)
    return render_template("tiktok/update_form.html")


@tiktok.route("/tiktok/get_devices", methods=["GET"])
def get_devices():
    devices = current_app.tiktok.distinct("device")
    return jsonify({"code": 200, "data": devices})


@tiktok.route("/tiktok/get_country", methods=["GET"])
def get_country():
    countries = current_app.tiktok.distinct("country")
    return jsonify({"code": 200, "data": countries})


@tiktok.route("/tiktok/get_data", methods=["POST"])
def get_data():

    device = request.json.get("device")
    country = request.json.get("country")
    search = request.json.get("search")
    page = request.json.get("page")
    pageSize = request.json.get("pageSize")
    order_by = request.json.get("order_by")
    order_type = request.json.get("order_type")

    query = {}

    if device:
        query["device"] = {"$regex": device, "$options": "i"}

    if country:
        query["country"] = {"$regex": country, "$options": "i"}

    if search:
        query["$or"] = [
            {"username": {"$regex": search, "$options": "i"}},
            {"phone": {"$regex": search, "$options": "i"}},
            {"email": {"$regex": search, "$options": "i"}},
            {"password": {"$regex": search, "$options": "i"}},
            {"passkey": {"$regex": search, "$options": "i"}},
            {"birthday": {"$regex": search, "$options": "i"}},
            {"country": {"$regex": search, "$options": "i"}},
            {"device": {"$regex": search, "$options": "i"}},
        ]

    if order_by is None:
        order_by = "_id"

    if order_type is None:
        order_type = -1

    total_results = current_app.tiktok.count_documents(query)
    total_pages = ceil(total_results / pageSize)
    skip = (page - 1) * pageSize

    tiktok_data = (
        current_app.tiktok.find(query)
        .sort(order_by, order_type)
        .skip(skip)
        .limit(pageSize)
    )

    data = []
    for detail in tiktok_data:
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


@tiktok.route("/tiktok/save", methods=["POST"])
def save():
    data = request.json
    id = data.get("id")
    username = data.get("username")
    phone = data.get("phone")
    email = data.get("email")
    password = data.get("password")
    passkey = data.get("passkey")
    birthday = data.get("birthday")
    country = data.get("country")
    device = data.get("device")

    key_update = data.get("key_update")
    value_update = data.get("value_update")

    # if id:
    #     current_app.tiktok.update_one(
    #         {"_id": ObjectId(id)}, {"$set": {key_update: value_update}}
    #     )

    #     return jsonify({"code": 200, "message": "Dữ liệu đã được cập nhật"})

    if id:
        current_app.tiktok.update_one(
            {"_id": ObjectId(id)},
            {
                "$set": {
                    "username": username,
                    "phone": phone,
                    "email": email,
                    "password": password,
                    "passkey": passkey,
                    "birthday": birthday,
                    "phone": phone,
                    "country": country,
                    "device": device,
                }
            },
        )

        return jsonify({"code": 200, "message": "Dữ liệu đã được cập nhật"})

    check_exit = current_app.tiktok.find_one(
        {
            "$or": [
                {"username": username},
                {"phone": phone},
                {"email": email},
            ]
        }
    )

    if check_exit is not None:
        current_app.tiktok.update_one(
            {"_id": check_exit["_id"]},
            {
                "$set": {
                    "password": password,
                    "passkey": passkey,
                    "birthday": birthday,
                    "country": country,
                    "device": device,
                }
            },
        )
    else:
        current_app.tiktok.insert_one(
            {
                "username": username,
                "phone": phone,
                "email": email,
                "password": password,
                "passkey": passkey,
                "birthday": birthday,
                "phone": phone,
                "country": country,
                "device": device,
                "created_at": datetime.now(),
            }
        )

    return jsonify({"code": 200, "message": "Dữ liệu đã được thêm mới"})


@tiktok.route("/tiktok/delete", methods=["GET"])
def delete():
    id = request.args.get("id")
    current_app.tiktok.delete_one({"_id": ObjectId(id)})
    return jsonify({"code": 200, "message": "Dữ liệu đã được xóa"})
