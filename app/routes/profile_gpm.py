# app/routes/main.py

from flask import (
    Blueprint,
    render_template,
    current_app,
    redirect,
    url_for,
    request,
    jsonify,
)
from bson import ObjectId
from math import ceil
from datetime import datetime

from app.middlewares.auth import token_required


profile_gpm = Blueprint("profile_gpm", __name__)


@profile_gpm.before_request
@token_required
def check_token():
    pass


@profile_gpm.route("/profile_gpm")
def index():
    return render_template("profile_gpm/index.html")


@profile_gpm.route("/profile_gpm/get_devices", methods=["GET"])
def get_devices():
    devices = current_app.profile_gpm.distinct("profile_device")
    return jsonify({"code": 200, "data": devices}), 200


@profile_gpm.route("/profile_gpm/list", methods=["POST"])
def get_data():
    page = int(request.json.get("page", 1))
    pageSize = int(request.json.get("pageSize", 10))
    order_by = request.json.get("order_by")
    device = request.json.get("device")
    status = request.json.get("status")
    name = request.json.get("name")
    session = request.json.get("session")
    query = {}

    if device is not None and len(device) > 0:
        query["profile_device"] = device

    if status is not None and len(status) > 0:
        query["status"] = status

    if order_by is None:
        order_by = "last_time"

    if name is not None and len(name) > 0:
        query["profile_name"] = {"$regex": name, "$options": "i"}

    if session is not None and len(session) > 0:
        query["session"] = {"$regex": session, "$options": "i"}

    list_device = current_app.profile_gpm.distinct("profile_device")
    list_status = current_app.profile_gpm.distinct("status")

    total_results = current_app.profile_gpm.count_documents(query)
    total_pages = ceil(total_results / pageSize)
    skip = (page - 1) * pageSize

    profile = (
        current_app.profile_gpm.find(query)
        .sort(order_by, -1)
        .skip(skip)
        .limit(pageSize)
    )

    data = []
    for p in profile:
        p["_id"] = str(p["_id"])
        if p.get("last_time") is not None:
            p["last_time"] = datetime.fromisoformat(str(p["last_time"])).strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        data.append(p)

    return (
        jsonify(
            {
                "code": 200,
                "data": data,
                "page": page,
                "pageSize": pageSize,
                "totalPages": total_pages,
                "totalResults": total_results,
                "device": list_device,
                "status": list_status,
            }
        ),
        200,
    )


@profile_gpm.route("/profile_gpm/get_data", methods=["GET"])
def getKeyData():
    key = request.args.get("key")

    if key is None:
        return jsonify({"code": 400, "message": "Key is required"}), 400

    profiles = current_app.profile_gpm.find({})

    if key == "session":
        data = []
        for profile in profiles:
            if profile.get("session") is not None:
                data.append(
                    str(profile["profile_name"])
                    + " - "
                    + str(profile["profile_device"])
                    + " - "
                    + str(profile["session"])
                    + "\n\n"
                )
        return jsonify({"code": 200, "data": data}), 200

    return jsonify({"code": 200, "data": ""}), 200


@profile_gpm.route("/profile_gpm/form")
def form():
    id = request.args.get("id")

    if id is None:
        return render_template("profile_gpm/form.html")

    profile = current_app.profile_gpm.find_one({"_id": ObjectId(id)})

    if profile is None:
        return render_template("profile_gpm/form.html")

    profile["id"] = str(profile["_id"])

    return render_template("profile_gpm/form.html", profile=profile)


@profile_gpm.route("/profile_gpm/update_field", methods=["POST"])
def update_field():
    data = request.json
    key = data.get("key")
    value = data.get("value")

    if key is None or value is None:
        return jsonify({"code": 400, "message": "Key and value is required"}), 400

    current_app.profile_gpm.update_many({}, {"$set": {key: value}})

    return jsonify({"code": 200, "message": "Success"}), 200


@profile_gpm.route("/profile_gpm/save", methods=["POST"])
def saveData():
    data = request.json
    profile_id = data.get("profile_id")
    profile_name = data.get("profile_name")
    profile_device = data.get("profile_device")

    if profile_id is None or len(profile_id) < 3:
        current_app.profile_gpm.insert_one(
            {"profile_name": profile_name, "profile_device": profile_device}
        )
    else:
        current_app.profile_gpm.update_one(
            {"_id": ObjectId(profile_id)},
            {"$set": {"profile_name": profile_name, "profile_device": profile_device}},
        )

    return jsonify({"code": 200, "message": "Success"}), 200


@profile_gpm.route("/profile_gpm/delete", methods=["GET"])
def deteleData():
    profile_id = request.args.get("id")

    if profile_id is None:
        return jsonify({"code": 400, "message": "Profile ID is required"}), 200

    current_app.profile_gpm.delete_one({"_id": ObjectId(profile_id)})

    return jsonify({"code": 200, "message": "Success"}), 200


@profile_gpm.route("/profile_gpm/get_profile", methods=["GET"])
def get_profile():
    device = request.args.get("device")

    if not device:
        return jsonify({"code": 400, "message": "Device is required", "data": []}), 400

    try:
        profile = current_app.profile_gpm.find(
            {"profile_device": device}, {"_id": 0, "profile_name": 1}
        )
        profile_data = []
        for p in profile:
            profile_data.append(p["profile_name"])

        if not profile_data:
            return (
                jsonify({"code": 404, "message": "Profile not found", "data": []}),
                404,
            )

        return jsonify({"code": 200, "data": profile_data}), 200

    except Exception as e:
        return (
            jsonify(
                {
                    "code": 500,
                    "message": "An error occurred while fetching the profile",
                    "error": str(e),
                }
            ),
            500,
        )
