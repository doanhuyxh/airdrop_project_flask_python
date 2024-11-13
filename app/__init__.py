# app/__init__.py
import traceback
from flask import Flask, jsonify, request
from pymongo import MongoClient, ASCENDING
from werkzeug.exceptions import HTTPException
#from flask_swagger_ui import get_swaggerui_blueprint
import logging

from app.middlewares.auth import token_update
from app.ultils.clear_cache import clear_all_pycache
from config import Config

#from app.cronjob.run_check_proxy_job import run_check_proxy_job

logging.basicConfig(level=logging.ERROR)
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
    
    # Register the schedule job
    # run_check_proxy_job()

    @app.after_request
    @token_update
    def after_request(response):
        return response
    
    @app.errorhandler(Exception)
    def handle_exception(e):
        if isinstance(e, HTTPException):
            code = e.code
        else:
            code = 500
        
        stack_trace = traceback.format_exc()
        print(request.get_data(as_text=True))
        return (
            jsonify({"code": code, "message": str(e), "data":[], "stack_trace": stack_trace }),
            200,
        )

    # Register the blueprints routes
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
    
    clear_all_pycache()
    
    return app
