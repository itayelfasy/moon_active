import threading
from typing import Dict

import uvicorn
from fastapi import FastAPI

from message_management import MessageManagement

app = FastAPI()
management = MessageManagement()


class BackgroundTask(threading.Thread):
    def run(self) -> None:
        management.check_scheduled_messages()


@app.get('/')
def root():
    return "im Alive"


@app.post('/echoAtTime')
async def add_message_to_redis(value: Dict[str, str]):
    return management.add_message_to_redis(value)


if __name__ == '__main__':
    task = BackgroundTask()
    task.start()
    uvicorn.run(app, host='0.0.0.0', port=8080)
