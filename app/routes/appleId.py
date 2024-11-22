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
    birthday= data.get("birthday")
    country = data.get("country")
    mail = data.get("mail")
    phone = data.get("phone")
    device = data.get("device")
    
    
    check_data = current_app.apple_id.find_one({
        "account": account,
        "device":device
    })
    
    if check_data:
        current_app.apple_id.update_one({
            "_id": check_data["_id"]
        },{
            "$set":{
                "password": password,
                "question": question,
                "birthday": birthday,
                "country": country,
                "mail": mail,
                "phone": phone
            }
        })
        
        return jsonify({"code": 200, "message": "Data berhasil disimpan"})
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
            "created_at": datetime.now()
        })
        
        return jsonify({"code": 200, "message": "Data berhasil disimpan"})
    
    
@appleId.route("/appleId/get_data", methods=["POST"])
def get_data():
    device = request.json.get("device")
    country = request.json.get("country")
    search = request.json.get("search")
    page = request.json.get("page")
    pageSize = request.json.get("pageSize")
    order_by = request.json.get("order_by")
    order_type = request.json.get("order_type")

    query = {}

    if device:
        query["device"] = {"$regex": device, "$options": "i"}

    if country:
        query["country"] = {"$regex": country, "$options": "i"}

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

    total_results = current_app.apple_id.count_documents(query)
    total_pages = ceil(total_results / pageSize)
    skip = (page - 1) * pageSize

    appleId_data = (
        current_app.apple_id.find(query).sort(order_by, order_type).skip(skip).limit(pageSize)
    )

    data = []
    for detail in appleId_data:
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
                "list_country": list_country
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