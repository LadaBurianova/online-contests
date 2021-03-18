import sqlalchemy
from .__db_session import SqlAlchemyBase


class Teams(SqlAlchemyBase):
    __tablename__ = 'teams'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    result = sqlalchemy.Column(sqlalchemy.Integer)  # баллы
    bonuses = sqlalchemy.Column(sqlalchemy.String)  # бонусы (для абаки - названия строк-столбцов через пробелы)
    correct_answers = sqlalchemy.Column(sqlalchemy.String)  # список правильно решённых задач
    wrong_answers = sqlalchemy.Column(sqlalchemy.String)  # список неправильно решённых задач


#  связь с участниками типа один ко многим
#  связь с lines columns
