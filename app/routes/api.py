
from flask import Blueprint, render_template, current_app, jsonify, request
from bson import ObjectId
from datetime import datetime


api = Blueprint('api', __name__)

@api.route("/api/project/detail/push", methods=["POST"])
def data_detail_push():
    data = request.json
    profile = data.get("profile")
    device = data.get("device")
    status = data.get("status")
    project_slug = data.get("project")
    
    project = current_app.project.find_one({"project_slug": str(project_slug).lower()})
    
    if project is None:
            current_app.project_detail.insert_one({
            "project_id": None,
            "profile": profile,
            "device": device,
            "status": status,
            "created_at": datetime.now()
        })
    else:
        current_app.project_detail.insert_one({
            "project_id": ObjectId(project["_id"]),
            "profile": profile,
            "device": device,
            "status": status,
            "created_at": datetime.now()
        })
    
    return jsonify({"code": 200, "message": "Push data detail successfully"}), 200
