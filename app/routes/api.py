from flask import Blueprint, render_template, current_app, jsonify, request
from bson import ObjectId
from datetime import datetime


api = Blueprint("api", __name__)


@api.route("/api/project/detail/push", methods=["POST"])
def data_detail_push():
    data = request.json
    profile = data.get("profile")
    device = data.get("device")
    status = data.get("status")
    project_slug = data.get("project")

    project = current_app.project.find_one({"project_slug": str(project_slug).lower()})

    if project is None:
        current_app.project_detail.insert_one(
            {
                "project_id": None,
                "profile": profile,
                "device": device,
                "status": status,
                "last_time": datetime.now(),
            }
        )
    else:
        current_app.project_detail.insert_one(
            {
                "project_id": ObjectId(project["_id"]),
                "profile": profile,
                "device": device,
                "status": status,
                "last_time": datetime.now(),
            }
        )

    return jsonify({"code": 200, "message": "Push data detail successfully"}), 200


@api.route("/api/project/detail/point/push", methods=["POST"])
def project_detail_point_push():
    data = request.json
    profiles = data.get("profile")
    device = data.get("device")
    point = data.get("point")
    project_slug = data.get("project")
    status = data.get("status")

    with open("log.txt", "a") as f:
        f.write(f"{datetime.now()} - {profiles} - {device} - {point} - {project_slug} - {status}\n")

    project = current_app.project.find_one({"project_slug": str(project_slug).lower()})
    
    check_exit = current_app.project_detail_point.find_one(
        {"profile": profiles, "device": device, "project_id": ObjectId(project["_id"])}
    )
    if check_exit:
        current_app.project_detail_point.update_one(
            {"profile": profiles, "device": device, "project_id": ObjectId(project["_id"])},
            {"$set": {"point": point, "last_time": datetime.now(), "status": status}},
        )
        return (
            jsonify(
                {"code": 200, "message": "Update project detail point successfully"}
            ),
            200,
        )

    # tạo mới dữ liệu
    
    if project is None:
        current_app.project_detail_point.insert_one(
            {
                "project_id": None,
                "profile": profiles,
                "device": device,
                "point": point,
                "last_time": datetime.now(),
                "status": None,
            }
        )
    else:
        current_app.project_detail_point.insert_one(
            {
                "project_id": ObjectId(project["_id"]),
                "profile": profiles,
                "device": device,
                "point": point,
                "last_time": datetime.now(),
                "status": None,
            }
        )

    return (
        jsonify({"code": 200, "message": "Push project detail point successfully"}),
        200,
    )
