import sqlalchemy
from .__db_session import SqlAlchemyBase
import sqlalchemy.orm as orm


class Line(SqlAlchemyBase):
    __tablename__ = 'lines'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    bonus_available = sqlalchemy.Column(sqlalchemy.Boolean)
    bonus = sqlalchemy.Column(sqlalchemy.Integer)


class Problem(SqlAlchemyBase):
    __tablename__ = 'problems'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    number = sqlalchemy.Column(sqlalchemy.String, unique=True)
    problem_text = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    picture_link = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    correct_answer = sqlalchemy.Column(sqlalchemy.String)
    line_id = sqlalchemy.Column(sqlalchemy.Integer)
    line = orm.relation('Line')
