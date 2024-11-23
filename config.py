# config.py

import os

class Config:
    SECRET_KEY = 'LZ3TjUBusAh3zbOWt9Wlg8ubcEaywQg0'
    MONGO_URI = 'mongodb://127.0.0.1:27017'
    DATABASE = 'AirDropProject'
    SERVER_HOST = '0.0.0.0'
    SERVER_PORT = 9999
    DEBUG = True
    UPLOAD_FOLDER = os.path.join(os.getcwd(), "app", "static", 'uploads')
    ALLOWED_EXTENSIONS = {'.txt', '.pdf', '.png', '.jpg', '.jpeg', '.gif', '.csv', '.xlsx', '.xls', ".mp4", ".mp3"}