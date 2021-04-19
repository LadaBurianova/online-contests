import sqlalchemy
from .__db_session import SqlAlchemyBase
import sqlalchemy.orm as orm


class Contest(SqlAlchemyBase):
    __tablename__ = 'contests'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    contest_type = sqlalchemy.Column(sqlalchemy.String)
    secret_key = sqlalchemy.Column(sqlalchemy.String)
    contest_id = sqlalchemy.Column('solving_processes', sqlalchemy.Integer, sqlalchemy.ForeignKey('solving_processes.id'))


class SolvingProcess(SqlAlchemyBase):
    __tablename__ = "solving_processes"
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    time = sqlalchemy.Column(sqlalchemy.Time)
    ok = sqlalchemy.Column(sqlalchemy.Integer)
    solving_process = orm.relation('Contest')
    team_id = sqlalchemy.Column('teams', sqlalchemy.Integer, sqlalchemy.ForeignKey('teams.id'))
    problem_id = sqlalchemy.Column('problems', sqlalchemy.Integer, sqlalchemy.ForeignKey('problems.id'))
