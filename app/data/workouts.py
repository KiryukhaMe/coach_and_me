from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from data.db_session import SqlAlchemyBase
import datetime


class Workout(SqlAlchemyBase):
    __tablename__ = 'workouts'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    date = Column(DateTime, default=datetime.datetime.now, nullable=False)
    duration = Column(Integer, nullable=True)
    user_id = Column(Integer, ForeignKey('users.id'))
