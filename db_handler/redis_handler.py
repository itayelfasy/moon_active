import time

import redis


class RedisHandler:
    def __init__(self):
        self.redis_client = redis.StrictRedis(host='localhost', port=6379)
        self.management_key = 'management_messages'

    def add_message(self, message, scheduled_time_timestamp):
        """add message by timestamp order to redis db"""
        try:
            self.redis_client.zadd(self.management_key, {message: scheduled_time_timestamp})
            return True
        except redis.RedisError as e:
            print(f"Error writing to Redis: {e}")
            return False

    def get_current_messages(self):
        """get all messages that have not been deleted up to the current time"""
        try:
            current_time = time.time()
            messages = self.redis_client.zrangebyscore(self.management_key, 0, current_time, withscores=True)
            return messages

        except redis.RedisError as e:
            print(f"Error reading from Redis: {e}")
            return None

    def delete_message(self, message):
        """delete message from db"""
        try:
            self.redis_client.zrem(self.management_key, message)
            return True

        except redis.RedisError as e:
            print(f"Error deleting from Redis: {e}")
            return False
