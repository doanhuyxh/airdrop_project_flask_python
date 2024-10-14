import jwt
import datetime
from functools import wraps
from config import Config

def create_token(obj_id, username):
    # Tạo payload cho token
    token_payload = {
        "id": obj_id,
        'user': username,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }
    token = jwt.encode(token_payload, Config.SECRET_KEY, algorithm='HS256')
    return token

def verify_token(token):
    try:
        # Giải mã token
        payload = jwt.decode(token, Config.SECRET_KEY, algorithms=['HS256'])
        return payload, None
    except jwt.ExpiredSignatureError:
        return None, 'Signature has expired'
    except jwt.InvalidTokenError:
        return None, 'Invalid token'