import sqlalchemy
from sqlalchemy.types import JSON
from sqlalchemy.schema import Column
from .__db_session import SqlAlchemyBase
import sqlalchemy.orm as orm
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class Team(SqlAlchemyBase):
    __tablename__ = 'teams'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    current_result = sqlalchemy.Column(sqlalchemy.Integer)  # баллы
    secret_code = sqlalchemy.Column(sqlalchemy.Integer)
    results = Column('data', JSON)
    user = orm.relation('User', back_populates='team')
    solving_process = orm.relation('SolvingProcess', back_populates='team')


class User(SqlAlchemyBase, UserMixin):
    __tablename__ = 'users'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    email = sqlalchemy.Column(sqlalchemy.String, unique=True)
    surname = sqlalchemy.Column(sqlalchemy.String)
    name = sqlalchemy.Column(sqlalchemy.String)
    nickname = sqlalchemy.Column(sqlalchemy.String, unique=True)
    password = sqlalchemy.Column(sqlalchemy.String)
    team_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("teams.id"))
    team = orm.relation('Team')

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
