from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from data.db_session import SqlAlchemyBase


class Workout(SqlAlchemyBase):
    __tablename__ = 'workouts'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    date = Column(DateTime, nullable=False)
    duration = Column(Integer, nullable=True)  # in minutes
    user_id = Column(Integer, ForeignKey('users.id'))
