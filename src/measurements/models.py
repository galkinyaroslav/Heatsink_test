import enum
from datetime import datetime
from typing import Literal, get_args

from sqlalchemy.dialects import postgresql
from sqlalchemy import Integer, ForeignKey, Table, Column, TIMESTAMP, ARRAY, Float, String, Enum
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


MeasuredPart = Literal['first20', 'second20', 'third20']


class Run(Base):
    __tablename__ = 'run_table'
    id:  Mapped[int] = mapped_column(Integer, primary_key=True)
    number: Mapped[int] = mapped_column(Integer, nullable=False)


class Measurement(Base):
    # __table_args__ = {'extend_existing': True}
    __tablename__ = 'measurements_table'
    id:  Mapped[int] = mapped_column(Integer, primary_key=True)
    run_number:  Mapped[int] = mapped_column(Integer, nullable=False)
    measuredpart: Mapped[MeasuredPart] = mapped_column(Enum(
        *get_args(MeasuredPart),
        name='measuredpart_enum',
        create_constraint=True,
        create_type=True,
        validate_strings=True,
    ))
    measure_datetime:  Mapped[TIMESTAMP] = mapped_column(TIMESTAMP, default=datetime.utcnow)
    user_id:  Mapped[int] = mapped_column(Integer, ForeignKey('users_table.id'), )
    data: Mapped[list[float]] = mapped_column(ARRAY(Float))


