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
from math import ceil
from bson import ObjectId
from datetime import datetime
from app.middlewares.auth import token_required

host_mail = Blueprint("host_mail", __name__)


@host_mail.before_request
@token_required
def check_token():
    pass


@host_mail.route("/host_mail", methods=["GET"])
def index():
    return render_template("host_mail/index.html")


@host_mail.route("/host_mail/form_get", methods=["GET"])
def form_create():
    return render_template("host_mail/form.html")

@host_mail.route("/host_mail/update_form", methods=["GET"])
def form_update():
    id = request.args.get("id")
    if id:
        host_mail_data = current_app.host_mail.find_one({"_id": ObjectId(id)})
        host_mail_data["_id"] = str(host_mail_data["_id"])
        return render_template("host_mail/update_form.html", host_mail_data=host_mail_data)
    return render_template("host_mail/update_form.html")

@host_mail.route("/host_mail/get_data", methods=["POST"])
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
            {"host_mail": {"$regex": search, "$options": "i"}},
            {"password": {"$regex": search, "$options": "i"}},
            {"host_mail_recovery": {"$regex": search, "$options": "i"}},
            {"phone": {"$regex": search, "$options": "i"}},
            {"birthday": {"$regex": search, "$options": "i"}},
        ]

    if order_by is None:
        order_by = "_id"

    if order_type is None:
        order_type = -1

    list_devices = current_app.host_mail.distinct("device")

    total_results = current_app.host_mail.count_documents(query)
    total_pages = ceil(total_results / pageSize)
    skip = (page - 1) * pageSize

    host_mail_data = (
        current_app.host_mail.find(query)
        .sort(order_by, order_type)
        .skip(skip)
        .limit(pageSize)
    )

    data = []
    for detail in host_mail_data:
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
                "list_devices": list_devices,
            }
        ),
        200,
    )


@host_mail.route("/host_mail/get_devices", methods=["GET"])
def get_devices():
    list_devices = current_app.host_mail.distinct("device")
    return jsonify({"code": 200, "data": list_devices})


@host_mail.route("/host_mail/save", methods=["POST"])
def form_host_mail():
    _id = request.json.get("id")
    device = request.json.get("device")
    host_mail = str(request.json.get("host_mail")).lower().strip()
    password = request.json.get("password")
    phone = request.json.get("phone")
    birthday = request.json.get("birthday")
    host_mail_recovery = request.json.get("host_mail_recovery")
    f2a = request.json.get("f2a")
    old_password = request.json.get("old_password")
    key = request.json.get("key")
    value_update = request.json.get("value_update")

    if _id:
        
        if key == "password":
            host_mail_data = current_app.host_mail.find_one({"_id": ObjectId(_id)})
            current_app.host_mail.update_one(
                {"_id": ObjectId(_id)},
                {
                    "$set": {
                        "old_password": host_mail_data["password"],
                    }
                },
            )
            
        current_app.host_mail.update_one(
            {"_id": ObjectId(_id)},
            {
                "$set": {
                    key: value_update,
                }
            },
        )
        
        return jsonify({"code": 200, "message": "Dữ liệu đã được cập nhật"})

    check_host_mail_exist = current_app.host_mail.find_one({"host_mail": host_mail})
    if check_host_mail_exist:
        if check_host_mail_exist["password"] != password:
            current_app.host_mail.update_one(
                {"_id": check_host_mail_exist["_id"]},
                {
                    "$set": {
                        "old_password": check_host_mail_exist["password"],
                        "password": password,
                    }
                })
        
        current_app.host_mail.update_one(
            {"_id": check_host_mail_exist["_id"]},
            {
                "$set": {
                    "device": device,
                    "password": password,
                    "phone": phone,
                    "birthday": birthday,
                    "host_mail_recovery": host_mail_recovery,
                    "f2a": f2a,
                }
            },
        )
    else:
        current_app.host_mail.insert_one(
            {
                "device": device,
                "host_mail": host_mail,
                "password": password,
                "phone": phone,
                "birthday": birthday,
                "host_mail_recovery": host_mail_recovery,
                "f2a": f2a,
                "old_password": "",
                "created_at": datetime.now(),
            }
        )

    return jsonify({"code": 200, "message": "Tạo tài khoản thành công"})


@host_mail.route("/host_mail/delete", methods=["GET"])
def delete_host_mail():
    _id = request.args.get("id")
    current_app.host_mail.delete_one({"_id": ObjectId(_id)})

    return jsonify({"code": 200, "message": "Data berhasil dihapus"})
