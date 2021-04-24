import sqlalchemy
from .__db_session import SqlAlchemyBase
import sqlalchemy.orm as orm


class Problem(SqlAlchemyBase):
    __tablename__ = 'problems'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    number = sqlalchemy.Column(sqlalchemy.Integer)  # number - номер строки. Баллы - то же число.
    category = sqlalchemy.Column(sqlalchemy.String)  # category - название типа задач (столбца)
    problem_text = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    picture_link = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    correct_answer = sqlalchemy.Column(sqlalchemy.String)
    solving_process = orm.relation("SolvingProcess", back_populates='problem')
