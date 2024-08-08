# app/__init__.py

from flask import Flask
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


    # Register the blueprints routes
    from .routes.main import main
    from .routes.proxy import proxy

    app.register_blueprint(main)
    app.register_blueprint(proxy, url_prefix='/proxy')

    return app
