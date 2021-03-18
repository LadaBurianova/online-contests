import sqlalchemy
import sqlalchemy.orm as orm
from .__db_session import SqlAlchemyBase


class Lines(SqlAlchemyBase):
    __tablename__ = 'lines'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    bonus = sqlalchemy.Column(sqlalchemy.Integer)
    solved = sqlalchemy.Column(sqlalchemy.Integer)


# связь с задачами

class Problems(SqlAlchemyBase):
    __tablename__ = 'problems'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    number = sqlalchemy.Column(sqlalchemy.String, unique=True)
    problem_text_link = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    picture_link = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    correct_answer = sqlalchemy.Column(sqlalchemy.String)
    bonus_available = sqlalchemy.Column(sqlalchemy.String)


association_table = sqlalchemy.Table('association', SqlAlchemyBase.metadata,
                                     sqlalchemy.Column('lines', sqlalchemy.Integer, sqlalchemy.ForeignKey('news.id')),
                                     sqlalchemy.Column('problems', sqlalchemy.Integer,
                                                       sqlalchemy.ForeignKey('problems.id')))

categories = orm.relation("Lines", secondary="lines_to_problems_association", backref="problems")
