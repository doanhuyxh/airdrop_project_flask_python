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

appleId = Blueprint("appleId", __name__)


@appleId.before_request
@token_required
def check_token():
    pass


@appleId.route("/appleId", methods=["GET"])
def index():
    return render_template("appleId/index.html")


@appleId.route("/appleId/form_get", methods=["GET"])
def form_get():
    return render_template("appleId/form.html")

@appleId.route("/appleId/get_devices", methods=["GET"])
def get_devices():
    list_devices = current_app.apple_id.distinct("device")
    return jsonify({"code": 200, "data": list_devices})

@appleId.route("/appleId/save", methods=["POST"])
def save():
    data = request.get_json()
    
    account = data.get("account")
    password = data.get("password")
    question = data.get("question")
    birthday = data.get("birthday")
    country = data.get("country")
    mail = data.get("mail")
    phone = data.get("phone")
    device = data.get("device")
    status = data.get("status")
    created_at = data.get("created_at")
    
    if created_at is None:
        created_at = datetime.now().strftime("%d/%m/%Y")
    
    check_data = current_app.apple_id.find_one({
        "account": account
    })
    
    if check_data:
        update_data = {}
        if password is not None:
            update_data["password"] = password
        if question is not None:
            update_data["question"] = question
        if birthday is not None:
            update_data["birthday"] = birthday
        if country is not None:
            update_data["country"] = country
        if mail is not None:
            update_data["mail"] = mail
        if phone is not None:
            update_data["phone"] = phone
        
        if update_data:
            current_app.apple_id.update_one({
                "_id": check_data["_id"]
            }, {
                "$set": update_data
            })
        
        return jsonify({"code": 200, "message": "Data updated successfully"})
    else:
        current_app.apple_id.insert_one({
            "account": account,
            "password": password,
            "question": question,
            "birthday": birthday,
            "country": country,
            "mail": mail,
            "phone": phone,
            "device": device,
            "status": status,
            "created_at": created_at
        })
        
        return jsonify({"code": 200, "message": "Data created successfully"})
  
    
@appleId.route("/appleId/get_data", methods=["POST"])
def get_data():
    device = request.json.get("device")
    country = request.json.get("country")
    search = request.json.get("search")
    page = request.json.get("page")
    pageSize = request.json.get("pageSize")
    order_by = request.json.get("order_by")
    order_type = request.json.get("order_type")
    status = request.json.get("status")

    query = {}

    if device is not None and len(device) > 0:
        query["device"] = {"$regex": device, "$options": "i"}

    if country is not None and len(country) > 0:
        query["country"] = {"$regex": country, "$options": "i"}

    if status is not None and len(status) > 0:
        query["status"] = status

    if search:
        query["$or"] = [
            {"mail": {"$regex": search, "$options": "i"}},
            {"phone": {"$regex": search, "$options": "i"}},
            {"account": {"$regex": search, "$options": "i"}},
            {"question": {"$regex": search, "$options": "i"}},
            {"birthday": {"$regex": search, "$options":"i"}}
        ]


    if order_by is None:
        order_by = "_id"
        
    if order_type is None:
        order_type = -1

    list_devices = current_app.apple_id.distinct("device")
    list_country = current_app.apple_id.distinct("country")
    list_status = current_app.apple_id.distinct("status")

    total_results = current_app.apple_id.count_documents(query)
    total_pages = ceil(total_results / pageSize)
    skip = (page - 1) * pageSize

    print(query)
    
    appleId_data = (
        current_app.apple_id.find(query).sort(order_by, order_type).skip(skip).limit(pageSize)
    )

    data = []
    for detail in appleId_data:
        detail["_id"] = str(detail["_id"])
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
                "list_country": list_country,
                "list_status": list_status
            }
        ),
        200,
    )
    
    
@appleId.route("/appleId/delete", methods=["POST"])
def delete():
    data = request.get_json()
    ids = data.get("ids")
    
    for id in ids:
        current_app.apple_id.delete_one({
            "_id": ObjectId(id)
        })    

    return jsonify({"code": 200, "message": "Data berhasil dihapus"})