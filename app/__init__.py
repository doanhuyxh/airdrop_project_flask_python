# app/__init__.py
import traceback
from flask import Flask, jsonify, request
from pymongo import MongoClient, ASCENDING
from werkzeug.exceptions import HTTPException
from flask_swagger_ui import get_swaggerui_blueprint
import logging
from datetime import datetime
from threading import Thread

from app.middlewares.auth import token_update
from app.ultils.clear_cache import clear_all_pycache
from config import Config


def log_to_mongo(collection_Db, log_document):
    """Hàm ghi log vào MongoDB."""
    try:
        collection_Db.insert_one(log_document)
    except Exception as e:
        logging.error(f"Error during logging to MongoDB: {e}\n{traceback.format_exc()}")


#from app.cronjob.run_check_proxy_job import run_check_proxy_job


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 # 16MB gới hạn upload file
    
    # Connect to MongoDB and define the collection
    client = MongoClient(Config.MONGO_URI)
    app.db = client.get_database(Config.DATABASE)
    
    app.profile_gpm = app.db["profile_gpm"]
    
    app.user_system = app.db["user_system"]

    app.project = app.db["project"]
    app.project_detail = app.db["project_detail"]
    app.project_detail_point = app.db["project_detail_point"]
    
    app.wallet =app.db["wallet"]
    app.wallet_detail = app.db["wallet_detail"]
    
    app.mail = app.db["mail"]

    app.host_mail = app.db["host_mail"]
    
    app.apple_id = app.db["apple_id_new"]

    app.log_request = app.db["log_request"]
    
    app.sim_card = app.db["sim_card"]
    
    app.facebook = app.db["facebook"]
    
    app.tiktok = app.db["tiktok"]
    
    # Register the schedule job
    # run_check_proxy_job()

    @app.after_request
    @token_update
    def after_request(response):
        try:

            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            method = request.method
            url = request.url
            ip_address = request.remote_addr
            status_code = response.status
            data = request.data.decode('utf-8') if request.data else ""
            query_params = request.args.to_dict()

            log_document = {
                "timestamp": timestamp,
                "method": method,
                "url": url,
                "ip_address": ip_address,
                "status_code": status_code,
                "data": data,
                "query_params": str(query_params)
            }
            
            if "static" not in url and "get" not in url and "list" not in url and "log_request" not in url and "favicon" not in url:
                app.log_request.insert_one(log_document)

            logging.info(
                f"[{timestamp}] {method} {url} (IP: {ip_address}) | Query: {query_params} | Data: {data} | Response: {status_code}"
            )
        except Exception as e:
            logging.error(f"Error during logging request/response: {e}\n{traceback.format_exc()}")

        # Thêm header CORS
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response
    
    @app.errorhandler(Exception)
    def handle_exception(e):
        if isinstance(e, HTTPException):
            code = e.code
        else:
            code = 500        
        stack_trace = traceback.format_exc()
        ip_address = request.remote_addr
        if ip_address != "127.0.0.1" and ip_address != "localhost" and ip_address != "::1":
            stack_trace = ""
        return (
            jsonify({"code": code, "message": str(e), "data":[], "stack_trace": stack_trace }),
            200,
        )

    # Register the blueprints routes
    SWAGGER_URL = '/api'
    API_URL = '/static/swagger.json'
    swaggerui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={
            'app_name': "API for AirDrop System"
        }
    )

    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)
    
    from .routes.main import main
    from .routes.auth import auth
    from .routes.dashboard import dashboard
    from .routes.project import project
    from .routes.upload import upload
    from .routes.profile_gpm import profile_gpm
    from .routes.api import api
    from .routes.user_system import user_system
    from .routes.wallet import wallet
    from .routes.mail import mail
    from .routes.host_mail import host_mail
    from .routes.appleId import appleId
    from .routes.log_request import log_request
    from .routes.sim_card import sim_card
    from .routes.facebook import facebook
    from .routes.tiktok import tiktok
    app.register_blueprint(main)
    app.register_blueprint(auth)
    app.register_blueprint(dashboard)
    app.register_blueprint(project)
    app.register_blueprint(upload)
    app.register_blueprint(profile_gpm)
    app.register_blueprint(api)
    app.register_blueprint(user_system)
    app.register_blueprint(wallet)
    app.register_blueprint(mail)
    app.register_blueprint(host_mail)
    app.register_blueprint(appleId)
    app.register_blueprint(log_request)
    app.register_blueprint(sim_card)
    app.register_blueprint(facebook)
    app.register_blueprint(tiktok)

    clear_all_pycache()
    
    return app
