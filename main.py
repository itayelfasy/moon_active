import threading
from typing import Dict

import uvicorn
from fastapi import FastAPI,HTTPException

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
async def add_message(value: Dict[str, str]):
    message_time = value.get('message_time')
    message = value.get('message')
    if not message or not message_time:
        raise HTTPException(status_code=400, detail="Error: message or message_time are empty")
    response = management.echo_at_time(message_time, message)
    if response:
        return "message insert success"
    else:
        return "message insert fail"


if __name__ == '__main__':
    task = BackgroundTask()
    task.start()
    uvicorn.run(app, host='0.0.0.0', port=8080)
