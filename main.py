import asyncio
import logging
from fastapi import FastAPI, BackgroundTasks
from typing import Dict
import threading
from message_management import MessageManagement
import uvicorn

app = FastAPI()


# @app.on_event("startup")
# async def startup_event():
#     management = MessageManagement()
#     message_thred = threading.Thread(target=management.check_scheduled_messages())
#     # message_thred.daemon = True
#     message_thred.start()


@app.get('/')
def root():
    return "im Alive"


@app.post('/echoAtTime')
async def add_message(value: Dict[str, str]):
    management = MessageManagement()
    message_time = value.get('message_time')
    message = value.get('message')
    management.echoAtTime(message_time, message)
    return "hii"



if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8080)

