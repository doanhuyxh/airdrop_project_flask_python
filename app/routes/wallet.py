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
import json
from app.middlewares.auth import token_required
from app.ultils.time_ultils import convertTime
from bson import ObjectId, json_util
from datetime import datetime, timedelta
import logging
from math import ceil


wallet = Blueprint("wallet", __name__)


@wallet.before_request
@token_required
def check_token():
    pass


@wallet.route("/wallet")
def index():
    return render_template("wallet/index.html")


@wallet.route("/wallet/list")
def wallet_get_data():
    page = int(request.args.get("page", 1))
    pageSize = int(request.args.get("pageSize", 10))

    projects = current_app.wallet.find().skip((page - 1) * pageSize).limit(pageSize)
    data = []
    for project in projects:
        project["_id"] = str(project["_id"])
        data.append(project)

    return jsonify({"code": 200, "data": json.loads(json_util.dumps(data))}), 200


@wallet.route("/wallet/form")
def wallet_form():

    id = request.args.get("id")

    if id is None or len(id) < 3:
        return render_template("wallet/form.html")

    wallet = current_app.wallet.find_one({"_id": ObjectId(id)})

    if wallet is None:
        return render_template("wallet/form.html")

    wallet["id"] = str(wallet["_id"])

    return render_template("wallet/form.html", wallet=wallet)


@wallet.route("/wallet/save", methods=["POST"])
def wallet_save():

    id = request.json.get("id")
    name = request.json.get("name")
    slug = request.json.get("slug")

    if id is not None and len(id) > 3:
        current_app.wallet.update_one(
            {"_id": ObjectId(id)}, {"$set": {"name": name, "slug": slug}}
        )
    else:
        current_app.wallet.insert_one(
            {"name": name, "slug": slug, "created_at": datetime.now()}
        )

    return jsonify({"code": 200, "message": "Create project successfully"}), 200


@wallet.route("/wallet/delete")
def wallet_delete():
    id = request.args.get("id")
    current_app.wallet.delete_one({"_id": ObjectId(id)})
    return jsonify({"code": 200, "message": "Delete project successfully"}), 200


@wallet.route("/wallet/detail")
def wallet_detail():
    wallet_id = request.args.get("id")
    wallet = current_app.wallet.find_one({"_id": ObjectId(wallet_id)})
    wallet["_id"] = str(wallet["_id"])
    return render_template("wallet/detail.html", wallet=wallet)


@wallet.route("/wallet/detail/get_data", methods=["POST"])
def wallet_detail_get_data():
    wallet_id = request.json.get("id")
    device = request.json.get("device")
    status = request.json.get("status")
    status_tomarket = request.json.get("status_tomarket")
    search = request.json.get("search")
    page = request.json.get("page")
    pageSize = request.json.get("pageSize")
    order_by = request.json.get("order_by")

    query = {"wallet_id": ObjectId(wallet_id)}

    if device:
        query["device"] = device

    if status:
        query["status"] = status

    if search:
        query["profile"] = {"$regex": search, "$options": "i"}

    if order_by is None:
        order_by = "_id"

    list_devices = current_app.wallet_detail.distinct(
        "device", {"wallet_id": ObjectId(wallet_id)}
    )
    list_status = current_app.wallet_detail.distinct(
        "status", {"wallet_id": ObjectId(wallet_id)}
    )
    list_status_tomarket = current_app.wallet_detail.distinct(
        "status_tomarket", {"wallet_id": ObjectId(wallet_id)}
    )

    total_results = current_app.wallet_detail.count_documents(query)
    total_pages = ceil(total_results / pageSize)
    skip = (page - 1) * pageSize


    wallet_detail_data = (
        current_app.wallet_detail.find(query)
        .sort(order_by, -1)
        .skip(skip)
        .limit(pageSize)
    )

    data = []
    for detail in wallet_detail_data:
        detail["_id"] = str(detail["_id"])
        detail["wallet_id"] = str(detail["wallet_id"])
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
                "list_status": list_status,
                "list_status_tomarket": list_status_tomarket,
            }
        ),
        200,
    )


@wallet.route("/wallet/detail/get_data_filter")
def wallet_detail_get_data_filter():
    wallet_id = request.args.get("id")
    device = request.args.get("device")
    status = request.args.get("status")

    query = {"wallet_id": ObjectId(wallet_id)}

    if device:
        query["device"] = device

    if status:
        query["status"] = status


    wallet_detail_data = current_app.wallet_detail.find(query)

    data = []
    for detail in wallet_detail_data:
        data.append(detail["profile"])

    return (
        jsonify(
            {
                "code": 200,
                "data": data,
            }
        ),
        200,
    )


@wallet.route("/wallet/detail/update", methods=["POST"])
def wallet_detail_update():
    data = request.json
    wallet_detail_id = data.get("id")
    field = data.get("field")
    value = data.get("value")

    current_app.wallet_detail.find_one_and_update(
        {"_id": ObjectId(wallet_detail_id)}, {"$set": {field: value}}
    )

    return jsonify({"code": 200, "message": "Update wallet detail successfully"}), 200


@wallet.route("/wallet/detail/delete", methods=["GET"])
def wallet_detail_delete():
    wallet_detail_id = request.args.get("id")

    current_app.wallet_detail.delete_one({"_id": ObjectId(wallet_detail_id)})

    return jsonify({"code": 200, "message": "Delete wallet detail successfully"}), 200


@wallet.route("/wallet/detail/delete_all", methods=["GET"])
def wallet_detail_delete_all():
    wallet = request.args.get("id")
    device = request.args.get("device")

    if wallet is None:
        return jsonify({"code": 400, "message": "wallet is required"}), 200

    if device is None:
        return jsonify({"code": 400, "message": "Device is required"}), 200

    current_app.wallet_detail.delete_many(
        {"wallet_id": ObjectId(wallet), "device": device}
    )
    return (
        jsonify({"code": 200, "message": "Delete All detail point successfully"}),
        200,
    )
