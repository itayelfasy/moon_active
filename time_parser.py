from datetime import datetime

import maya
from fastapi import HTTPException


def datetime_to_timestamp(datetime_str: str):
    "this func parse datetime string to timestamp"""
    try:

        dt_object = maya.parse(datetime_str, "Israel").datetime()
        timestamp = dt_object.timestamp()
        return timestamp
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid date-time format. {e}")


def timestamp_to_string_datetime(timestamp: float):
    dt = datetime.fromtimestamp(timestamp)
    return dt.strftime('%Y-%m-%d %H:%M:%S')
