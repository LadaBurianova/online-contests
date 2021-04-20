import json
from db_interaction import __db_session, __all_tables


def add_from_json():
    __db_session.global_init("db_interaction/users_data.db")
    with open('test_contest/data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    contest = __all_tables.contests.Contest()
    contest.title = data['contest']['title']
    contest.secret_key = data['contest']['secret_key']
    db_sess = __db_session.create_session()
    db_sess.add(contest)
    for d in data['problems']:
        problem = __all_tables.problems.Problem()
        problem.number = int(d['number'])
        problem.category = d['category']
        problem.problem_text = d['text']
        problem.picture_link = d['link']
        problem.correct_answer = d['answer']
        db_sess.add(problem)
    db_sess.commit()


def add_to_solving_process():
    __db_session.global_init("db_interaction/users_data.db")
    db_sess = __db_session.create_session()
    process1 = __all_tables.contests.SolvingProcess()
    process2 = __all_tables.contests.SolvingProcess()
    process1.ok = 2
    process2.ok = 2
    process1.problem_id = process2.problem_id = 1
    process1.answer = '4'
    process2.answer = 'не знаю'
    process1.team_id = 1
    process2.team_id = 2
    process1.problem_id = 1
    process2.problem_id = 1

    db_sess.add(process1)
    db_sess.add(process2)
    db_sess.commit()


def test():
    __db_session.global_init("db_interaction/users_data.db")
    db_sess = __db_session.create_session()
    for i in db_sess.query(__all_tables.problems.Problem):
        print(i.number, i.category)


add_from_json()
#  test()
add_to_solving_process()
