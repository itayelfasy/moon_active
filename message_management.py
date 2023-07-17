import asyncio
import time
import threading
import redis
from datetime import datetime
from db_handler.redis_handler import RedisHandler
import parser


class MessageManagement:
    def __init__(self):
        self.redis_client = redis.StrictRedis(host='localhost', port=6379)
        self.scheduler_key = 'management_messages'

    def echoAtTime(self, scheduled_time: str, message: str):
        current_time = time.time()
        scheduled_time_timestamp = datetime_to_timestamp(scheduled_time)
        delay = scheduled_time_timestamp - current_time

        if delay <= 0:
            print(f"Error: Scheduled time must be in the future.")
            return

        self.redis_client.zadd(self.scheduler_key, {message: scheduled_time_timestamp})

    def check_scheduled_messages(self):
        print("start")
        while True:
            current_time = time.time()
            messages = self.redis_client.zrangebyscore(self.scheduler_key, 0, current_time)
            if messages:
                for message in messages:
                    print(str(datetime.now()) + message.decode())
                    self.redis_client.zrem(self.scheduler_key, message)
            time.sleep(1)


def datetime_to_timestamp(date_time_str):
    try:
        # Parse the string into a datetime object
        dt_object = datetime.strptime(date_time_str, "%Y-%m-%d %H:%M:%S")
        # Convert datetime object to timestamp using the timestamp() method
        timestamp = dt_object.timestamp()
        return timestamp
    except ValueError:
        raise ValueError("Invalid date-time format. Expected format: 'YYYY-MM-DD HH:MM:SS'")

# if __name__ == '__main__':
#     messege = MessageManagement()
#     messege.check_scheduled_messages()
#     messege.echoAtTime('2023-07-17 17:31:00','send agin')
