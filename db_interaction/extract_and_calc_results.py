from . import __all_tables
import json

CATEGORIES = ('арифметика', '1', '2', '3')
SCORES = ('10', '20', '30', '40')


def team_results(team, db_sess):
    """returns abaka table"""
    line_bonus = 0
    column_bonus = 0

    table = json.loads(team.results)
    res = 0

    for solving in db_sess.query(__all_tables.contests.SolvingProcess).filter(
            (__all_tables.contests.SolvingProcess.ok == 1) | (__all_tables.contests.SolvingProcess.ok == 0)):
        n, m = convert_indexes(solving.problem.category, solving.problem.number)
        table[n][m] = solving.ok
    for line in table:
        if '?' not in line and 0 not in line:
            line_bonus += 40
    for col in range(4):
        for row in range(4):
            b = True
            if table[row][col] == '?' or table[row][col] == 0:
                b = False
            else:
                res += 1
        if b:
            column_bonus += (col + 1) * 10
    team.results = json.dumps(table)
    db_sess.commit()
    return table, return_res_and_str(res, line_bonus, column_bonus)


def all_results(db_sess):
    data = []
    for team in db_sess.query(__all_tables.teams.Team):
        table, res = team_results(team, db_sess)
        data.append((team.id, table, res))
    db_sess.commit()
    return data


def return_res_and_str(res, line_bonus, column_bonus):
    s = str(res) + '+' + str(line_bonus) + '+' + str(column_bonus)
    return eval(s), s


def convert_indexes(ct, pr):
    if ct == CATEGORIES[0]:
        ct = 0
    elif ct == CATEGORIES[1]:
        ct = 1
    elif ct == CATEGORIES[2]:
        ct = 2
    else:
        ct = 3
    return ct, pr
