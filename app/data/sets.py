import datetime
import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Set(SqlAlchemyBase):
    __tablename__ = "sets"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    weight = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    reps = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    exercise_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('exercises.id'))
    exercise = orm.relationship('Exercise')
    workout_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('workouts.id'))
    workout = orm.relationship('Workout')
