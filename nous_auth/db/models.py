from sqlalchemy import (
    Table,
    MetaData,
    Column,
    Integer,
    String,
    Text,
    BigInteger,
    SmallInteger,
)
from ..const import UserTypes

# https://alembic.sqlalchemy.org/en/latest/naming.html
convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

meta = MetaData(naming_convention=convention)

user = Table(
    'user',
    meta,
    Column('id', Integer, primary_key=True),
    Column('login', String(length=32), nullable=False, index=True),
    Column('password', Text, nullable=False, index=True),
    Column('username', String(length=128), nullable=False),
    Column('phone', Integer, nullable=True, index=True),
    Column('create_date', Integer, nullable=False),
    Column('vip', Integer, nullable=True),
    Column('blocked', Integer, nullable=False, default=0),
    Column('role', SmallInteger, nullable=False, default=UserTypes.USER),
)
token = Table(
    'token',
    meta,
    Column('id', BigInteger, primary_key=True),
    Column('user_id', Integer, nullable=False, index=True),
    Column('token', Text, nullable=False, index=True),
    Column('create_date', Integer, nullable=False),
)
history = Table(
    'history',
    meta,
    Column('id', BigInteger, primary_key=True),
    Column('type', SmallInteger, nullable=False, index=True),
    Column('text', Text, nullable=False),
)
