import time
from datetime import datetime

def get_current_time():
    current_time = datetime.now()
    formatted_time = current_time.strftime('%Y-%m-%d %H:%M:%S')
    return formatted_time


def check_time_difference(minutes = 10, time_str = ""):
    time_format = "%Y-%m-%d %H:%M:%S"
    try:
        current_time = datetime.now()
        given_time = datetime.strptime(time_str, time_format)
        time_diff = abs((current_time - given_time).total_seconds())
        # So sánh sự khác biệt với số phút đã cho
        return time_diff >= minutes * 60

    except ValueError as e:
        # Nếu có lỗi khi phân tích chuỗi thời gian
        print(f"Error parsing dates: {e}")
        return False