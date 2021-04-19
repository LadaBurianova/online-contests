import json
from . import __db_session
from .contests import Contest
from .problems import Problem
from .teams import Team, User


def add_from_json():
    with open('test_contest/data.json', 'r') as f:
        data = json.load(f)
    contest = Contest()
    contest.title = data['contest']['title']
    contest.secret_key = data['contest']['secret_key']
    db_sess = __db_session.create_session()
    db_sess.add(contest)
    for d in data['problems']:
        problem = Problem()
        problem.number = d['number']
        problem.category = d['category']
        problem.problem_text = d['text']
        problem.picture_link = d['link']
        problem.correct_answer = d['answer']
        db_sess.add(problem)
    db_sess.commit()
