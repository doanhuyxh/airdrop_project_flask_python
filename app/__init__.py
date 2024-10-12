# app/__init__.py

from flask import Flask, jsonify
from pymongo import MongoClient, ASCENDING
from werkzeug.exceptions import HTTPException

from app.ultils.clear_cache import clear_all_pycache
from config import Config
#from app.cronjob.run_check_proxy_job import run_check_proxy_job


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Connect to MongoDB and define the collection
    client = MongoClient(Config.MONGO_URI)
    app.db = client.get_default_database()

    app.user_system = app.db["user_system"]
    app.project = app.db["project"]
    app.data = app.db["data"]
    
    # Register the schedule job
    # run_check_proxy_job()


    @app.errorhandler(Exception)
    def handle_exception(e):
        if isinstance(e, HTTPException):
            code = e.code  # Lấy mã lỗi từ HTTPException
        else:
            code = 500  # Mặc định là 500 nếu không phải HTTPException
        return (
            jsonify({"code": code, "message": str(e) }),
            200,
        )

    # Register the blueprints routes
    from .routes.main import main
    from .routes.auth import auth
    from .routes.dashboard import dashboard
    from .routes.project import project
    app.register_blueprint(main)
    app.register_blueprint(auth)
    app.register_blueprint(dashboard)
    app.register_blueprint(project)
    clear_all_pycache()
    
    return app
