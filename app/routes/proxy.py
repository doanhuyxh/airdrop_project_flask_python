from flask import Blueprint, render_template, jsonify, current_app, request
from bson import ObjectId
import threading

import app.ultils.time_ultils as time_ultils

proxy = Blueprint('admin', __name__)
db_lock = threading.Lock()


@proxy.route('/', methods=['GET'])
def get_all_proxies():
    list_proxies = current_app.proxy_collection.find()
    result = []
    for proxy in list_proxies:
        proxy['_id'] = str(proxy['_id'])
        result.append(proxy)
    return jsonify(result)


@proxy.route("get", methods=['GET'])
def get_proxy():
    proxy = current_app.proxy_collection.find_one({'used': 'no'})
    return jsonify({'proxy': proxy})


@proxy.route("add_update", methods=['POST'])
def add_update_proxy():
    proxy = request.json

    id = proxy.get('id')
    if not id:
        current_app.proxy_collection.insert_one({
            'username': proxy.get('username'),
            'password': proxy.get('password'),
            'port': proxy.get('port'),
            'host': proxy.get('host'),
            'type': proxy.get('type'),
            'used': 'no',
            "last_used": time_ultils.get_current_time()
        })

        return jsonify({'message': 'Proxy added successfully'})
    else:
        current_app.proxy_collection.update_one({'_id': ObjectId(id)}, {
            '$set': {
                'username': proxy.get('username'),
                'password': proxy.get('password'),
                'port': proxy.get('port'),
                'host': proxy.get('host'),
                'type': proxy.get('type'),
                'used': 'no',
                "last_used": time_ultils.get_current_time()
            }
        })
        return jsonify({'message': 'Proxy updated successfully'})
@proxy.route("add_range", methods=['POST'])
def add_range_proxy():
    proxy = request.json
    start = proxy.get('start')
    end = proxy.get('end')
    type = proxy.get('type')
    for i in range(int(start), int(end) + 1):
        current_app.proxy_collection.insert_one({
            'username': proxy.get('username'),
            'password': proxy.get('password'),
            'port': i,
            'host': proxy.get('host'),
            'type': proxy.get('type'),
            'used': 'no',
            "last_used": time_ultils.get_current_time()
        })
    return jsonify({'message': 'Proxy added successfully'})

@proxy.route("delete", methods=['GET'])
def delete_proxy():
    id = request.args.get('id')
    current_app.proxy_collection.delete_one({'_id': ObjectId(id)})
    return jsonify({'message': 'Proxy deleted successfully'})


@proxy.route("update_used", methods=['GET'])
def update_used():
    id = request.args.get('id')
    status = request.args.get('status')
    if not status:
        status = 'no'
    current_app.proxy_collection.update_one({'_id': ObjectId(id)}, {
        '$set': {
            'used': status,
            "last_used": time_ultils.get_current_time()
        }
    })
    return jsonify({'message': 'Proxy changed successfully'})


@proxy.route("get_used", methods=['GET'])
def get_used():
    # Lấy địa chỉ IP của client
    client_ip = request.remote_addr
    type = request.args.get('type')

    if not type:
        return jsonify({'proxy': '', 'id': '', 'port': ''})

    with db_lock:  # Sử dụng lock để đảm bảo các truy vấn là tuần tự
        proxy = current_app.proxy_collection.find_one({'used': 'no', "type": type})
        if not proxy:
            return jsonify({'proxy': '', 'id': '', 'port': ''})
        proxy_string = f"socks5://{proxy['username']}:{proxy['password']}@{proxy['host']}:{proxy['port']}"
        # Cập nhật trạng thái của proxy vừa lấy ra
        current_app.proxy_collection.update_one(
            {'_id': ObjectId(proxy['_id'])},
            {
                '$set': {
                    'used': 'yes',
                    'last_used': time_ultils.get_current_time()
                }
            }
        )
        print(f"Proxy_port: {proxy['port']} -- ip: {client_ip}")
        return jsonify({'proxy': proxy_string, 'id': str(proxy['_id']), 'port': proxy['port']})
