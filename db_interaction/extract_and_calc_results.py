from . import __db_session
from .contests import SolvingProcess


def team_results(team):
    """returns abaka table"""
    db_sess = __db_session.create_session()
    for solving_process in db_sess.query(SolvingProcess).filter((SolvingProcess.team_id == team.id)):
        pass


def recount_bonuses(team, problem):
    pass


def print_table(table):
    pass
