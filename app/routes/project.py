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
from datetime import datetime, timedelta
import logging

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
      
        
        if project["created_at"] is not None:
            project["created_at"] = project["created_at"]
        else:
            project["created_at"] = None
            
        if project["start_date"] is not None:
            project["start_date"] = project["start_date"].strftime("%d-%m-%Y")
        else:
            project["end_date"] = None
            
        if project["end_date"] is not None:
            project["end_date"] = project["end_date"].strftime("%d-%m-%Y")
        else:
            project["end_date"] = None

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
    
    project_slug = project_slug.lower()
    if start_date is None:
        start_date = datetime.now()
    
    if end_date is None:
        start_date = datetime.now().__add__(timedelta(days=60))
        
    if token_name is None or len(token_name) < 1:
        token_name = "Chưa rõ"
    
    if project_image is None or len(project_image) < 3:
        project_image = "https://via.placeholder.com/150"
    
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
    project["end_date"] = project["end_date"]
    project["created_by"] = current_app.user_system.find_one({"_id": project["created_by"]}).get("username")
    return render_template("project/detail.html", project=project)

@project.route("/project/detail/get_data", methods=["POST"])
def data_detail_get():
    project_id = request.json.get("id")
    device = request.json.get("device")
    status = request.json.get("status")
    search = request.json.get("search")
    
    print(project_id, device, status)
    
    query = {"project_id": ObjectId(project_id)}
    
    if device:
        query["device"] = {"$regex": device, "$options": "i"}
    if status:
        query["status"] = status
        
    if search:
        query["profile"] = {"$regex": search, "$options": "i"}
        

    project_detail_data = current_app.project_detail.find(query).sort("_id", -1)
    
    data = []
    for detail in project_detail_data:
        detail["_id"] = str(detail["_id"])
        detail["project_id"] = str(detail["project_id"])
        data.append(detail)
        
    return jsonify({"code": 200, "data": data}), 200
    

@project.route("/project/detail/delete", methods=["GET"])
def delete_detail():
    id = request.args.get("id")
    current_app.project_detail.delete_one({"_id": ObjectId(id)})
    return jsonify({"code": 200, "message": "Delete detail successfully"}), 200


@project.route("/project/detail/point", methods=["GET"])
def project_detail_point():
    project_id = request.args.get("id")
    project = current_app.project.find_one({"_id": ObjectId(project_id)})
    project["_id"] = str(project["_id"])
    project["created_at"] = project["created_at"].strftime("%d-%m-%Y")
    project["start_date"] = project["start_date"].strftime("%d-%m-%Y")
    project["end_date"] = project["end_date"]
    project["created_by"] = current_app.user_system.find_one({"_id": project["created_by"]}).get("username")
    return render_template("project/project_detail_point.html", project=project)


@project.route("/project/detail/point/get_data", methods=["GET"])
def project_detail_point_get():
    project_id = request.args.get("id")
    search = request.args.get("search")
    
    query = {"project_id": ObjectId(project_id)}
    
    if search:
        query["profile"] = {"$regex": search, "$options": "i"}
    
    
    project_detail_point_data = current_app.project_detail_point.find(query).sort("_id", -1)
    data = []
    for detail in project_detail_point_data:
        detail["_id"] = str(detail["_id"])
        detail["project_id"] = str(detail["project_id"])
        data.append(detail)
    
    print(data)
    return jsonify({"code": 200, "data": data}), 200