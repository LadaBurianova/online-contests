import sqlalchemy
from .__db_session import SqlAlchemyBase
import sqlalchemy.orm as orm


class Contest(SqlAlchemyBase):
    __tablename__ = 'contests'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    secret_key = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    solving_process_id = sqlalchemy.Column(sqlalchemy.Integer,
                                           sqlalchemy.ForeignKey("solving_processes.id"))
    solving_process = orm.relation('SolvingProcess')


class SolvingProcess(SqlAlchemyBase):
    __tablename__ = "solving_processes"
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    ok = sqlalchemy.Column(sqlalchemy.Integer)
    answer = sqlalchemy.Column(sqlalchemy.String)
    contest = orm.relation('Contest', back_populates='solving_process')
    team = orm.relation('Team')
    team_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("teams.id"))
    problem = orm.relation('Problem')
    problem_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("problems.id"))
