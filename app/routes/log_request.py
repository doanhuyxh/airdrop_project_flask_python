
from flask import Flask, jsonify, request, redirect, url_for, render_template, Blueprint, current_app
from math import ceil
from bson import ObjectId
from app.middlewares.auth import token_required


log_request = Blueprint('log_request', __name__)

@log_request.before_request
@token_required
def check_token():
    pass

@log_request.route('/log_request', methods=['GET'])
def index():
    return render_template('log_request/index.html')

@log_request.route("/log_request/get_data", methods=["POST"])
def get_data():
    page = request.json.get("page")
    pageSize = request.json.get("pageSize")
    search = request.json.get("search")
    filter_ip = request.json.get("filter_ip")
    
    query = {}
    
    if filter_ip:
        query["ip_address"] = filter_ip
    
    if search:
        query["$or"] = [
            {"timestamp": {"$regex": search, "$options": "i"}},
            {"method": {"$regex": search, "$options": "i"}},
            {"url": {"$regex": search, "$options": "i"}},
            {"ip_address": {"$regex": search, "$options": "i"}},
            {"data": {"$regex": search, "$options":"i"}}
        ]
    list_ips = current_app.log_request.distinct("ip_address")
    total_results = current_app.log_request.count_documents(query)
    total_pages = ceil(total_results / pageSize)
    skip = (page - 1) * pageSize
    log_request_data = (
       current_app.log_request.find(query).sort("_id", -1).skip(skip).limit(pageSize)
    )
    
    data = []
    for i in log_request_data:
        i["_id"] = str(i["_id"])
        data.append(i)
    
    return (
        jsonify(
            {
                "code": 200,
                "data": data,
                "page": page,
                "pageSize": pageSize,
                "totalPages": total_pages,
                "totalResults": total_results,
                "list_ip":list_ips
            }
        ),
        200,
    )
    
    
@log_request.route("/log_request/delete", methods=["POST"])
def delete_data():
    data = request.get_json()
    ids = data.get("ids")
    
    if len(ids) == 0:
        current_app.log_request.delete_many({})
    else:
        for id in ids:
            current_app.log_request.delete_one({
                "_id": ObjectId(id)
            })  
            
    return jsonify({"code": 200, "message": "Data berhasil dihapus"})