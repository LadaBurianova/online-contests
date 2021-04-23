from . import __db_session
from .contests import SolvingProcess
import json


def team_results(team):
    """returns abaka table"""
    db_sess = __db_session.create_session()
    table = json.loads(team.results)
    for solving_process in db_sess.query(SolvingProcess).filter((SolvingProcess.team_id == team.id)):
        if solving_process.ok == 1:
            pass


def recount_bonuses(team, problem):
    pass


def print_table(table):  # just for test
    pass
