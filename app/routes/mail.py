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

mail = Blueprint("mail", __name__)


@mail.before_request
@token_required
def check_token():
    pass


@mail.route("/mail", methods=["GET"])
def index():
    return render_template("mail/index.html")


@mail.route("/mail/form_get", methods=["GET"])
def form_create():
    return render_template("mail/form.html")

@mail.route("/mail/update_form", methods=["GET"])
def form_update():
    id = request.args.get("id")
    if id:
        mail_data = current_app.mail.find_one({"_id": ObjectId(id)})
        mail_data["_id"] = str(mail_data["_id"])
        return render_template("mail/update_form.html", mail_data=mail_data)
    return render_template("mail/update_form.html")

@mail.route("/mail/get_data", methods=["POST"])
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
            {"mail": {"$regex": search, "$options": "i"}},
            {"password": {"$regex": search, "$options": "i"}},
            {"mail_recovery": {"$regex": search, "$options": "i"}},
            {"phone": {"$regex": search, "$options": "i"}},
            {"birthday": {"$regex": search, "$options": "i"}},
            {"google_ads": {"$regex": search, "$options": "i"}},
        ]

    if order_by is None:
        order_by = "_id"

    if order_type is None:
        order_type = -1

    list_devices = current_app.mail.distinct("device")

    total_results = current_app.mail.count_documents(query)
    total_pages = ceil(total_results / pageSize)
    skip = (page - 1) * pageSize

    mail_data = (
        current_app.mail.find(query)
        .sort(order_by, order_type)
        .skip(skip)
        .limit(pageSize)
    )

    data = []
    for detail in mail_data:
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


@mail.route("/mail/get_devices", methods=["GET"])
def get_devices():
    list_devices = current_app.mail.distinct("device")
    return jsonify({"code": 200, "data": list_devices})


@mail.route("/mail/save", methods=["POST"])
def form_mail():
    _id = request.json.get("id")
    device = request.json.get("device")
    mail = str(request.json.get("email")).lower().strip()
    password = request.json.get("password")
    phone = request.json.get("phone")
    birthday = request.json.get("birthday")
    mail_recovery = request.json.get("mail_recovery")
    google_ads = request.json.get("google_ads")
    f2a = request.json.get("f2a")
    old_password = request.json.get("old_password")
    key = request.json.get("key")
    value_update = request.json.get("value_update")

    if _id:
        
        if key == "password":
            mail_data = current_app.mail.find_one({"_id": ObjectId(_id)})
            current_app.mail.update_one(
                {"_id": ObjectId(_id)},
                {
                    "$set": {
                        "old_password": mail_data["password"],
                    }
                },
            )
            
        current_app.mail.update_one(
            {"_id": ObjectId(_id)},
            {
                "$set": {
                    key: value_update,
                }
            },
        )
        
        return jsonify({"code": 200, "message": "Dữ liệu đã được cập nhật"})

    check_mail_exist = current_app.mail.find_one({"mail": mail})
    if check_mail_exist:
        
        if check_mail_exist["password"] != password:
            current_app.mail.update_one(
                {"_id": check_mail_exist["_id"]},
                {
                    "$set": {
                        "old_password": check_mail_exist["password"],
                        "password": password,
                    }
                })
        
        current_app.mail.update_one(
            {"_id": check_mail_exist["_id"]},
            {
                "$set": {
                    "device": device,
                    "password": password,
                    "phone": phone,
                    "birthday": birthday,
                    "mail_recovery": mail_recovery,
                    "google_ads": google_ads,
                    "f2a": f2a,
                }
            },
        )
    else:
        current_app.mail.insert_one(
            {
                "device": device,
                "mail": mail,
                "password": password,
                "phone": phone,
                "birthday": birthday,
                "mail_recovery": mail_recovery,
                "google_ads": google_ads,
                "created_at": datetime.now(),
                "f2a": f2a,
                "old_password": "",
            }
        )

    return jsonify({"code": 200, "message": "Tạo tài khoản thành công"})


@mail.route("/mail/delete", methods=["GET"])
def delete_mail():
    _id = request.args.get("id")
    current_app.mail.delete_one({"_id": ObjectId(_id)})

    return jsonify({"code": 200, "message": "Data berhasil dihapus"})
