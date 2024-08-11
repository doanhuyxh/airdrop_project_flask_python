# app/__init__.py

from flask import Flask,jsonify
from pymongo import MongoClient, ASCENDING

from config import Config
from app.cronjob.run_check_proxy_job import run_check_proxy_job

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Connect to MongoDB and define the collection
    client = MongoClient(Config.MONGO_URI)
    app.db = client.get_default_database()
    app.proxy_collection = app.db["proxy"]

    # create index for proxy collection
    app.proxy_collection.create_index([('used', ASCENDING)])


    # Register the schedule job
    run_check_proxy_job()

    # Định nghĩa các trình xử lý lỗi trước
    app.errorhandler(500)
    def handle_500_error(e):
        return jsonify({"error": "Internal Server Error", "details": str(e)}), 500

    app.errorhandler(Exception)
    def handle_exception(e):
        return jsonify({"error": "An error occurred", "details": str(e)}), 500


    # Register the blueprints routes
    from .routes.main import main
    from .routes.proxy import proxy

    app.register_blueprint(main)
    app.register_blueprint(proxy, url_prefix='/proxy')

    return app
