import schedule
import time
import threading
from pymongo import MongoClient
from config import Config
import app.ultils.time_ultils as time_ultils

client = MongoClient(Config.MONGO_URI)
db = client.get_default_database()
proxy_collection = db["proxy"]

def job():
    print(f"Chạy quét db proxy {time.strftime('%Y-%m-%d %H:%M:%S')}")
    proxy = proxy_collection.find({'used': 'yes'})
    for item in proxy:
        if time_ultils.check_time_difference(1, item['last_used']):
            proxy_collection.update_one({'_id': item['_id']}, {
                '$set': {
                    'used': 'no'
                }
            })


def start_schedule():
    while True:
        schedule.run_pending()
        time.sleep(1)


def run_check_proxy_job():
    schedule.every(30).seconds.do(job)
    scheduler_thread = threading.Thread(target=start_schedule)
    scheduler_thread.daemon = True # Chỉ định luồng này sẽ kết thúc khi chương trình chính kết thúc
    scheduler_thread.start()
