from flask import request, jsonify, redirect, g, make_response
from functools import wraps
from app.ultils.jwt_token import verify_token, create_refresh_token, create_token

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        
        token = request.cookies.get('token')
        refresh_token = request.cookies.get('refresh_token')

        if not token or not refresh_token:
            return redirect('/login')

        payload, error = verify_token(token)
        if error:
            payload, error_refresh = verify_token(refresh_token)
            if error_refresh:
                return redirect('/login')
            else:
                new_token = create_token(payload.get('id'), payload.get('user'))
                new_refresh_token = create_refresh_token(payload.get('id'), payload.get('user'))
                g.new_token = new_token
                g.new_refresh_token = new_refresh_token

        current_user_id = payload.get('id')
        request.current_user_id = current_user_id
        return f(*args, **kwargs) 
    
    return decorated


def token_update(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        response = f(*args, **kwargs)
        if hasattr(g, 'new_token'):
            response.set_cookie('token', g.new_token, httponly=True, secure=False, samesite='Strict')
        if hasattr(g, 'new_refresh_token'):
            response.set_cookie('refresh_token', g.new_refresh_token, httponly=True, secure=False, samesite='Strict')
        return response
    
    return decorated


def clear_cookies(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        response = f(*args, **kwargs)
    
        if isinstance(response, str):
            response = make_response(response)
        response.delete_cookie('token')
        response.delete_cookie('refresh_token')
        return response
    return decorated