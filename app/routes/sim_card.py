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
from math import ceil
from bson import ObjectId
from datetime import datetime

sim_card = Blueprint("sim_card", __name__)


@sim_card.before_request
@token_required
def check_token():
    pass


@sim_card.route("/sim_card", methods=["GET"])
def index():
    return render_template("sim_card/index.html")


@sim_card.route("/sim_card/form_get", methods=["GET"])
def form_create():
    return render_template("sim_card/form.html")


@sim_card.route("/sim_card/get_data", methods=["POST"])
def get_data():
    sim_type = request.json.get("sim_type")
    search = request.json.get("search")
    page = request.json.get("page")
    pageSize = request.json.get("pageSize")
    order_by = request.json.get("order_by")
    order_type = request.json.get("order_type")

    query = {}

    if sim_type:
        query["sim_type"] = {"$regex": sim_type, "$options": "i"}

    if search:
        query["$or"] = [
            {"sim_type": {"$regex": search, "$options": "i"}},
            {"date_expired": {"$regex": search, "$options": "i"}},
            {"gmail": {"$regex": search, "$options": "i"}},
            {"telegram": {"$regex": search, "$options": "i"}},
            {"AppleId": {"$regex": search, "$options": "i"}},
        ]

    if order_by is None:
        order_by = "_id"

    if order_type is None:
        order_type = -1

    list_sim_type = current_app.sim_card.distinct("sim_type")

    total_results = current_app.sim_card.count_documents(query)
    total_pages = ceil(total_results / pageSize)
    skip = (page - 1) * pageSize

    sim_card_data = (
        current_app.sim_card.find(query)
        .sort(order_by, order_type)
        .skip(skip)
        .limit(pageSize)
    )

    data = []
    for detail in sim_card_data:
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
                "totalPages": total_pages,
                "totalResults": total_results,
                "list_sim_type": list_sim_type,
            }
        ),
        200,
    )


@sim_card.route("/sim_card/save", methods=["POST"])
def form_mail():
    _id = request.json.get("id")
    phoneNumber = request.json.get("phoneNumber")
    sim_type = str(request.json.get("sim_type")).lower().strip()
    date_expired = request.json.get("date_expired")
    gmail = request.json.get("gmail")
    telegram = request.json.get("telegram")
    AppleId = request.json.get("AppleId")
    key = request.json.get("key")
    value_update = request.json.get("value_update")

    if _id:
        current_app.sim_card.update_one(
            {"_id": ObjectId(_id)},
            {
                "$set": {
                    key: value_update,
                }
            },
        )
        return jsonify({"code": 200, "message": "Dữ liệu đã được cập nhật"})

    check_sim_exist = current_app.sim_card.find_one({"phoneNumber": phoneNumber})

    if check_sim_exist:
        current_data = current_app.sim_card.find_one({"_id": check_sim_exist["_id"]})
        update_fields = {}
        if sim_type:
            update_fields["sim_type"] = sim_type
        if date_expired:
            update_fields["date_expired"] = date_expired
        if gmail:
            update_fields["gmail"] = gmail
        if AppleId:
            update_fields["AppleId"] = AppleId
        if telegram:
            update_fields["telegram"] = telegram
        current_app.sim_card.update_one(
            {"_id": check_sim_exist["_id"]}, {"$set": update_fields}
        )
    else:
        current_app.sim_card.insert_one(
            {
                "phoneNumber": phoneNumber,
                "sim_type": sim_type,
                "date_expired": date_expired,
                "gmail": gmail,
                "AppleId": AppleId,
                "telegram": telegram,
                "created_at": datetime.now(),
            }
        )

    return jsonify({"code": 200, "message": "Tạo sim thành công"})


@sim_card.route("/sim_card/delete", methods=["GET"])
def delete_sim():
    _id = request.args.get("id")
    current_app.sim_card.delete_one({"_id": ObjectId(_id)})
    return jsonify({"code": 200, "message": "Xóa sim thành công"})
