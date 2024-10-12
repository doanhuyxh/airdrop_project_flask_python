# config.py

import os

class Config:
    SECRET_KEY = 'LZ3TjUBusAh3zbOWt9Wlg8ubcEaywQg0'
    MONGO_URI = 'mongodb://localhost:27017/AirDropProject'
    SERVER_HOST = '127.0.0.1'
    SERVER_PORT = 8080
    DEBUG = True
    UPLOAD_FOLDER = os.path.join(os.getcwd(), "app", "static", 'uploads')
    ALLOWED_EXTENSIONS = {'.txt', '.pdf', '.png', '.jpg', '.jpeg', '.gif', '.csv', '.xlsx', '.xls', ".mp4", ".mp3"}