from flask import request, jsonify, redirect
from functools import wraps
from app.ultils.jwt_token import verify_token

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        # Lấy token từ cookie
        token = request.cookies.get('token')

        if not token:
            #return jsonify({'code': 401, 'message': 'Token is missing!'}), 200
            return redirect('/login')

        # Xác thực token
        payload, error = verify_token(token)
        if error:
            #return jsonify({'code': 302, 'message': error}), 200
            return redirect('/login')

        # Lấy user_id từ payload
        current_user_id = payload.get('id')
        request.current_user_id = current_user_id
        return f(*args, **kwargs)  # Truyền user_id cho route
    return decorated
