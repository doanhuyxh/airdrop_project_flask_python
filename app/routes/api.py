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
        
        check = current_app.project_detail.find_one(
            {
                "project_id": ObjectId(project["_id"]),
                "profile": profile,
                "device": device,
            }
        )
        
        if check:
            current_app.project_detail.update_one(
                {
                    "project_id": ObjectId(project["_id"]),
                    "profile": profile,
                    "device": device,
                },
                {"$set": {"status": status, "last_time": datetime.now()}},
            )
            return (
                jsonify({"code": 200, "message": "Update data detail successfully"}),
                200,
            )
        
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

    project = current_app.project.find_one({"project_slug": str(project_slug).lower()})

    check_exit = current_app.project_detail_point.find_one(
        {"profile": profiles, "device": device, "project_id": ObjectId(project["_id"])}
    )
    if check_exit:
        current_app.project_detail_point.update_one(
            {
                "profile": profiles,
                "device": device,
                "project_id": ObjectId(project["_id"]),
            },
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
                "status": status,
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
                "status": status,
            }
        )

    return (
        jsonify({"code": 200, "message": "Push project detail point successfully"}),
        200,
    )


@api.route("/api/wallet/detail/push", methods=["POST"])
def wallet_detail_push():
    data = request.json

    profile = data.get("profile")
    device = data.get("device")
    wallet_type = data.get("wallet")
    address = data.get("address")
    password = data.get("password")
    password_mobile = data.get("password_mobile")
    recovery_phrase = data.get("recovery_phrase")
    status = data.get("status")
    project_name = data.get("project")

    wallet = current_app.wallet.find_one({"slug": str(wallet_type).lower()})

    if wallet is None:
        current_app.wallet_detail.insert_one(
            {
                "profile": profile,
                "device": device,
                "wallet_id": None,
                "address": address,
                "password": password,
                "password_mobile": password_mobile,
                "recovery_phrase": recovery_phrase,
                "last_time": datetime.now(),
                "status": status,
            }
        )

        return (
            jsonify({"code": 200, "message": "Create wallet successfully"}),
            200,
        )

    check_exit = current_app.wallet_detail.find_one(
        {"profile": profile, "device": device, "wallet_id": ObjectId(wallet["_id"])}
    )

    if check_exit:
        update_fields = {}

        if address and len(address) >= 3:
            update_fields["address"] = address

        if password and len(password) >= 3:
            update_fields["password"] = password

        if recovery_phrase and len(recovery_phrase) >= 3:
            update_fields["recovery_phrase"] = recovery_phrase
            
        if password_mobile and len(password_mobile) >= 3:
            update_fields["password_mobile"] = password_mobile

        if status and len(status) >= 3:
            update_fields["status"] = status
        
        
        if update_fields:
            update_fields["last_time"] = datetime.now()

        current_app.wallet_detail.update_one(
            {
                "profile": profile,
                "device": device,
                "wallet_id": ObjectId(wallet["_id"]),
            },
            {"$set": update_fields},
        )
        return (
            jsonify({"code": 200, "message": "Update wallet successfully"}),
            200,
        )

    current_app.wallet_detail.insert_one(
        {
            "profile": profile,
            "device": device,
            "wallet_id": ObjectId(wallet["_id"]),
            "address": address,
            "password": password,
            "recovery_phrase": recovery_phrase,
            "password_mobile": password_mobile,
            "last_time": datetime.now(),
            "status": status,
        }
    )

    return (
        jsonify({"code": 200, "message": "Create wallet successfully"}),
        200,
    )


@api.route("/api/wallet/detail/get_wallet", methods=["POST"])
def wallet_detail_get():
    data = request.json
    profile = data.get("profile")
    device = data.get("device")
    wallet_type = data.get("wallet")
    
    wallet = current_app.wallet.find_one({"slug": str(wallet_type).lower()})
    if wallet is None:
        return jsonify({"code": 404, "message": "Wallet not found", "data":""}), 200
    
    wallet_detail = current_app.wallet_detail.find_one({
        "profile": profile,
        "device": device,
        "wallet_id": ObjectId(wallet["_id"])
    })
    
    if wallet_detail is None:
        return jsonify({"code": 404, "message": "Wallet detail not found", "data":""}), 200
    
    data = {
        "recovery_phrase": wallet_detail.get("recovery_phrase"),
        "profile": wallet_detail.get("profile"),
    }
    return jsonify({"code": 200, "message": "Get wallet detail successfully", "data": data}), 200