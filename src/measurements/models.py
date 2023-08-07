from datetime import datetime

from sqlalchemy import MetaData, Integer, ForeignKey, Table, Column, TIMESTAMP, ARRAY, Float, String
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class Measurement(Base):
    # __table_args__ = {'extend_existing': True}
    __tablename__ = 'measurements_table'
    id:  Mapped[int] = mapped_column(Integer, primary_key=True)
    run_number:  Mapped[int] = mapped_column(Integer, nullable=False)
    measure_datetime:  Mapped[TIMESTAMP] = mapped_column(TIMESTAMP, default=datetime.utcnow)
    user_id:  Mapped[int] = mapped_column(Integer, ForeignKey('users_table.id'), )
    data: Mapped[str] = mapped_column(String(length=320), unique=True, index=True, nullable=False)

#
# from auth.models import user
#
# metadata = MetaData()
#
#
# measurement = Table(
#     'measurement',
#     metadata,
#     Column('id', Integer, primary_key=True),
#     Column('run_number', Integer, nullable=False),
#     Column('measure_datetime', TIMESTAMP, default=datetime.utcnow),
#     Column('user_id', Integer, ForeignKey(user.c.id), extend_existing=True),
#     Column('data', ARRAY(Float)),
#     extend_existing=True,
# )
#
#
