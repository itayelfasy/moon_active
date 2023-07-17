import time
from datetime import datetime

import redis
from fastapi import HTTPException

from db_handler.redis_handler import RedisHandler
from time_parser import datetime_to_timestamp, timestamp_to_string_datetime


class MessageManagement:
    """
    this class mange all message actions
    """

    def __init__(self):
        self.redis_handler = RedisHandler()

    def echo_at_time(self, sender_time: str, message: str):
        """
        this func allows you to schedule a message to be sent at a specific time
        in the future.
        this data save in redis

        :param sender_time: time to send the message
        :param message: message to send
        :return: TRUE if this message insert to redis else Fasle
        """
        current_time = time.time()
        scheduled_time_timestamp = datetime_to_timestamp(sender_time)
        delay = scheduled_time_timestamp - current_time
        if delay <= 0:
            raise HTTPException(status_code=400, detail="Error: Scheduled time must be in the future")
        return self.redis_handler.add_message(message, scheduled_time_timestamp)

    def check_scheduled_messages(self):
        """
        this func run at the background of the serves and print
        every message that should be print
        """
        while True:

            messages = self.redis_handler.get_current_messages()

            if messages:
                for message_tuple in messages:
                    message = message_tuple[0].decode()
                    time_to_send = timestamp_to_string_datetime(message_tuple[1])
                    print(message)
                    print(f"time the message should be sent: {time_to_send},"
                          f" time the message sent: {str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))} ")
                    self.redis_handler.delete_message(message)
