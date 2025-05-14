import datetime
import sqlalchemy

from .db_session import SqlAlchemyBase


class User(SqlAlchemyBase):
    __tablename__ = "users"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    username = sqlalchemy.Column(sqlalchemy.String, unique=True, nullable=True)
    password_hash = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    time_create = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now())
