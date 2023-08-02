from datetime import datetime

from sqlalchemy import MetaData, Integer, String, ForeignKey, Table, Column, JSON, Boolean
from sqlalchemy.dialects.postgresql import TIMESTAMP

metadata = MetaData()

role = Table(
    'role',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String, nullable=False),
    Column('permissions', JSON)
)

user = Table(
    'user',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('username', String, nullable=False),
    Column('registered_datetime', TIMESTAMP, default=datetime.utcnow),
    Column('role_id', Integer, ForeignKey(role.c.id)),
    Column('email', String(length=320), nullable=False),
    Column('hashed_password', String(length=1024), nullable=False),
    Column('is_active', Boolean, default=True, nullable=False),
    Column('is_superuser', Boolean, default=False, nullable=False),
    Column('is_verified', Boolean, default=False, nullable=False)
)


