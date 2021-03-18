import sqlalchemy
from .__db_session import SqlAlchemyBase


class Contest(SqlAlchemyBase):
    __tablename__ = 'contests'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String)


#  Связь с командами типа "многие ко многим"
#  Связь с задачами типа "многие ко многим"
