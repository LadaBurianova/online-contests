import json
from db_interaction import __db_session, __all_tables


def add_from_json():
    __db_session.global_init("db_interaction/users_data.db")
    with open('test_contest/data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    db_sess = __db_session.create_session()
    contest = __all_tables.contests.Contest()
    contest.title = data['contest']['title']
    contest.secret_key = data['contest']['secret_key']
    db_sess.add(contest)
    team_1 = __all_tables.teams.Team()
    team_2 = __all_tables.teams.Team()
    db_sess.add(team_1)
    db_sess.add(team_2)
    user_1 = __all_tables.teams.User(email='user_1@mail.ru', surname='Иванов', name='Иван', nickname='user_1',
                                     team=team_1)
    user_1.set_password('user_1')
    user_2 = __all_tables.teams.User(email='user_2@mail.ru', surname='Петров', name='Пётр', nickname='user_2',
                                     team=team_2)
    user_2.set_password('user_2')
    db_sess.add(user_1)
    db_sess.add(user_2)
    for d in data['problems']:
        problem = __all_tables.problems.Problem()
        problem.number = int(d['number'])
        problem.category = d['category']
        problem.problem_text = d['text']
        problem.picture_link = d['link']
        problem.correct_answer = d['answer']
        db_sess.add(problem)
        process1 = __all_tables.contests.SolvingProcess(team=team_1,
                                                        problem=problem, ok=2, answer='4')
        process2 = __all_tables.contests.SolvingProcess(team=team_2,
                                                        problem=problem, ok=2, answer='не знаю')
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
