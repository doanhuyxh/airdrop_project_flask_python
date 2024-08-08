# config.py

import os

class Config:
    SECRET_KEY = 'your-secret-key'
    MONGO_URI = 'mongodb://localhost:27017/autoTouch'
    SERVER_HOST = '127.0.0.1'
    SERVER_PORT = 8080
    DEBUG = True