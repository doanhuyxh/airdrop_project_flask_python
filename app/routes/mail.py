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


@mail.route("/mail/get_data", methods=["POST"])
def get_data():

    device = request.json.get("device")
    search = request.json.get("search")
    page = request.json.get("page")
    pageSize = request.json.get("pageSize")
    order_by = request.json.get("order_by")

    query = {}

    if device:
        query["device"] = {"$regex": device, "$options": "i"}

    if search:
        query["mail"] = {"$regex": search, "$options": "i"}

    if order_by is None:
        order_by = "_id"

    list_devices = current_app.mail.distinct("device")

    total_results = current_app.mail.count_documents(query)
    total_pages = ceil(total_results / pageSize)
    skip = (page - 1) * pageSize

    mail_data = (
        current_app.mail.find(query).sort(order_by, -1).skip(skip).limit(pageSize)
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
                "totalPages": "{:,}".format(total_pages),
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
    mail = request.json.get("email")
    password = request.json.get("password")
    phone = request.json.get("phone")
    key = request.json.get("key")
    value_update = request.json.get("value_update")

    if _id:
        current_app.mail.update_one(
            {"_id": ObjectId(_id)},
            {
                "$set": {
                    key: value_update,
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
                "created_at": datetime.now(),
            }
        )

    return jsonify({"code": 200, "message": "Data berhasil disimpan"})


@mail.route("/mail/delete", methods=["GET"])
def delete_mail():
    _id = request.args.get("id")
    current_app.mail.delete_one({"_id": ObjectId(_id)})

    return jsonify({"code": 200, "message": "Data berhasil dihapus"})
