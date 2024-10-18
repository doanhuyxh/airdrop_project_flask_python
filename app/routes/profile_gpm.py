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

from app.middlewares.auth import token_required


profile_gpm = Blueprint("profile_gpm", __name__)


@profile_gpm.before_request
@token_required
def check_token():
    pass


@profile_gpm.route("/profile_gpm")
def index():
    return render_template("profile_gpm/index.html")


@profile_gpm.route("/profile_gpm/list", methods=["POST"])
def get_data():
    page = int(request.json.get("page", 1))
    pageSize = int(request.json.get("pageSize", 10))
    order_by = request.json.get("order_by")
    device = request.json.get("device")
    query = {}

    if device is not None and len(device) > 0:
        query["profile_device"] = device
        
    if order_by is None:
        order_by = "_id"

    
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
            }
        ),
        200,
    )


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
