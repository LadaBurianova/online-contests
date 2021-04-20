import sqlalchemy
from .__db_session import SqlAlchemyBase


class Problem(SqlAlchemyBase):
    __tablename__ = 'problems'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    number = sqlalchemy.Column(sqlalchemy.Integer)  # number - номер строчки. Баллы - то же число.
    category = sqlalchemy.Column(sqlalchemy.String)  # category - название типа задач (колонки)
    problem_text = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    picture_link = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    correct_answer = sqlalchemy.Column(sqlalchemy.String)
