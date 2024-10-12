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
from app.middlewares.auth import token_required
from app.ultils.time_ultils import convertTime
from bson import ObjectId
from datetime import datetime

project = Blueprint("project", __name__)


@project.before_request
@token_required
def check_token():
    pass


@project.route("/project", methods=["GET"])
def index():
    return render_template("project/index.html")

@project.route("/project/list", methods=["GET"])
def get_data():
    
    page = int(request.args.get("page", 1))
    pageSize = int(request.args.get("pageSize", 10))
    
    projects = current_app.project.find().skip((page - 1) * pageSize).limit(pageSize)
    data = []
    for project in projects:
        project["_id"] = str(project["_id"])
        project["created_at"] = project["created_at"].strftime("%d-%m-%Y")
        project["start_date"] = project["start_date"].strftime("%d-%m-%Y")
        project["end_date"] = project["end_date"].strftime("%d-%m-%Y")
        project["created_by"] = current_app.user_system.find_one({"_id": project["created_by"]}).get("username")
        data.append(project)
    return jsonify({"code": 200, "data": data}), 200

@project.route("/project/form", methods=["GET"])
def create():
    id = request.args.get("id")
    
    if id is None:
        return render_template("project/form.html")
    
    project = current_app.project.find_one({"_id": ObjectId(id)})
    
    if project is None:
        return render_template("project/form.html")
    
    project["id"] = str(project["_id"])
    project["start_date"] = project["start_date"].strftime("%Y-%m-%d")
    project["end_date"] = project["end_date"].strftime("%Y-%m-%d")
    
    print(project)
    return render_template("project/form.html", project=project)
    
@project.route("/project/save", methods=["POST"])
def store():
    
    admin_id = request.current_user_id
    data = request.form
    project_id = data.get("project_id")
    project_name = data.get("project_name")
    project_slug = data.get("project_slug")
    description = data.get("project_description")
    start_date = data.get("start_date")  # yyyy-mm-dd
    end_date = data.get("end_date")  # yyyy-mm-dd
    token_name = data.get("token_name")
    project_image = data.get("project_image")
    
    if project_id is None or len(project_id) < 3:
        current_app.project.insert_one(
            {
                "project_name": project_name,
                "project_slug": project_slug,
                "description": description,
                "start_date": convertTime(start_date),
                "end_date": convertTime(end_date),
                "token_name": token_name,
                "project_image": project_image,
                "created_at": datetime.now(),
                "created_by": ObjectId(admin_id),
            }
        )
    else:
        current_app.project.update_one(
            {"_id": ObjectId(project_id)},
            {
                "$set": {
                    "project_name": project_name,
                    "project_slug": project_slug,
                    "description": description,
                    "start_date": convertTime(start_date),
                    "end_date": convertTime(end_date),
                    "token_name": token_name,
                    "project_image": project_image,
                }
            },
        )

    return jsonify({"code": 200, "message": "Create project successfully"}), 200

@project.route("/project/delete", methods=["GET"])
def delete():
    id = request.args.get("id")
    current_app.project.delete_one({"_id": ObjectId(id)})
    return jsonify({"code": 200, "message": "Delete project successfully"}), 200


@project.route("/project/detail", methods=["GET"])
def detail():
    id = request.args.get("id")
    project = current_app.project.find_one({"_id": ObjectId(id)})
    project["_id"] = str(project["_id"])
    project["created_at"] = project["created_at"].strftime("%d-%m-%Y")
    project["start_date"] = project["start_date"].strftime("%d-%m-%Y")
    project["end_date"] = project["end_date"].strftime("%d-%m-%Y")
    project["created_by"] = current_app.user_system.find_one({"_id": project["created_by"]}).get("username")
    return render_template("project/detail.html", project=project)