import sqlalchemy
from .__db_session import SqlAlchemyBase
import sqlalchemy.orm as orm


class Contest(SqlAlchemyBase):
    __tablename__ = 'contests'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    contest_type = sqlalchemy.Column(sqlalchemy.String)
    solving_processes = orm.relation('SolvingProcess')
    secret_key = sqlalchemy.Column(sqlalchemy.String)


class SolvingProcess(SqlAlchemyBase):
    __tablename__ = "solving_processes"
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    team_id = sqlalchemy.Column(sqlalchemy.Integer)
    problem_id = sqlalchemy.Column(sqlalchemy.Integer)
    time = sqlalchemy.Column(sqlalchemy.Time)
    solving_process = orm.relation('SolvingProcess')
    sqlalchemy.Column('teams', sqlalchemy.Integer, sqlalchemy.ForeignKey('news.id'))
    sqlalchemy.Column('problems', sqlalchemy.Integer, sqlalchemy.ForeignKey('problems.id'))
