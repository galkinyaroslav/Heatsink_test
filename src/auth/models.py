from datetime import datetime

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import MetaData, Integer, String, ForeignKey, Table, Column, JSON, Boolean, TIMESTAMP, ARRAY, Float
# from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column, relationship, DeclarativeBase
from measurements.models import Measurement
from database import Base

# auth_metadata = MetaData()
# class Base(DeclarativeBase):
#     pass
# role = Table(
#     'role',
#     metadata,
#     Column('id', Integer, primary_key=True),
#     Column('name', String, nullable=False),
#     Column('permissions', JSON),
# )

# user = Table(
#     'user',
#     metadata,
#     Column('id', Integer, primary_key=True),
#     Column('username', String, nullable=False),
#     Column('registered_datetime', TIMESTAMP, default=datetime.utcnow),
#     Column('role_id', Integer, ForeignKey(role.c.id)),
#     Column('email', String(length=320), nullable=False),
#     Column('hashed_password', String(length=1024), nullable=False),
#     Column('is_active', Boolean, default=True, nullable=False),
#     Column('is_superuser', Boolean, default=False, nullable=False),
#     Column('is_verified', Boolean, default=False, nullable=False),
# )


class Role(Base):
    __tablename__ = 'roles_table'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    permissions: Mapped[JSON] = mapped_column(JSON, nullable=True)
    users: Mapped[list['User']] = relationship()


class User(SQLAlchemyBaseUserTable[int], Base):
    # __table_args__ = {'extend_existing': True}
    __tablename__ = 'users_table'
    id:  Mapped[int] = mapped_column(Integer, primary_key=True)
    username:  Mapped[str] = mapped_column(String, nullable=False)
    registered_datetime:  Mapped[TIMESTAMP] = mapped_column(TIMESTAMP, default=datetime.utcnow)
    role_id:  Mapped[int] = mapped_column(Integer, ForeignKey('roles_table.id'))
    email: Mapped[str] = mapped_column(String(length=320), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(length=1024), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    measurements: Mapped[list['Measurement']] = relationship()





