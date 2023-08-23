from datetime import datetime
from enum import Enum

from pydantic import BaseModel


# MeasuredPart = Literal['first20', 'second20', 'third20']


class RunPart(str, Enum):
    first20 = 'first20'
    second20 = 'second20'
    third20 = 'third20'


# class MeasurementsToDB(BaseModel):
#     run_number: int
#     measuredpart: str
#     measure_datetime: datetime
#     user_id: int
#     data: list[float]
