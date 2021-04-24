from flask import Flask, render_template, redirect, request, url_for
from flask_login import LoginManager, login_user, logout_user, login_required
from forms.user import RegistrationForm, LoginForm
from db_interaction import __db_session
from db_interaction import __all_tables
from db_interaction import extract_and_calc_results
from db_interaction import constants


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = __db_session.create_session()
    return db_sess.query(__all_tables.teams.User).get(user_id)


@app.route('/main', methods=['GET', 'POST'])
def main_page():
    return render_template('startpage.html', links=[])


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = __db_session.create_session()
        user = db_sess.query(__all_tables.teams.User).filter(__all_tables.teams.User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            if form.secret_code == constants.ADMIN_PASSWORD:
                return redirect('/checking')
            return redirect('/solving')
        return render_template('login_form.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login_form.html', title='Авторизация', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    """Registration form. redirects to main if everything is correct."""
    form = RegistrationForm()
    if form.validate_on_submit():
        if form.password.data != form.password_copy.data:
            return render_template('register_form.html', title='Регистрация', form=form, message='Пароли не совпадают')

        db_sess = __db_session.create_session()
        if db_sess.query(__all_tables.teams.User).filter(__all_tables.teams.User.email == form.email.data).first():
            return render_template('register_form.html', title='Регистрация', form=form,
                                   message="Такой пользователь уже есть")
        user = __all_tables.teams.User(email=form.email.data)
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/main')
    return render_template('register_form.html', title='Регистрация', form=form)


@app.route('/solving', methods=['GET', 'POST'])
def solving():
    db_sess = __db_session.create_session()
    team = db_sess.query(__all_tables.teams.Team).filter()
    if request.method == 'POST':
        data = request.form.to_dict()
        answer = data['answer']
        p_id, t_id = list(filter(lambda a: a != 'answer', data.keys()))[
            0].split('&')
        solving_process = __all_tables.contests.SolvingProcess()
        solving_process.problem = db_sess.query(__all_tables.problems.Problem).filter(__all_tables.problems.Problem.id
                                                                == p_id).first()
        solving_process.team = db_sess.query(__all_tables.teams.Team).filter(__all_tables.teams.Team.id ==
                                                          t_id).first()
        solving_process.answer = answer
        solving_process.ok = 2
        db_sess.commit()
        return redirect('/solving')
    db_sess = __db_session.create_session()
    data = []
    for i in db_sess.query(__all_tables.problems.Problem):
        print(i)
        if db_sess.query(__all_tables.contests.SolvingProcess).filter(
                __all_tables.contests.SolvingProcess.team_id == i.id).first() is not None:
            print(i, i.solving_process)
            status = i.solving_process.ok
        else:
            status = ''
        data.append([
            str(i.id + '&' + i.solving_process.team.id),
            str(i.problem.problem_text),
            str(status)
        ])
    return render_template('solving.html', problems=data)


@app.route('/check', methods=['GET', 'POST'])
def check():
    """Page for checking answers. Button 0- for wrong, 1- for correct."""
    if request.method == 'POST':
        db_sess = __db_session.create_session()
        data = request.form.to_dict()
        ok = int(list(data.keys())[0]) % 2
        pr_id, t_id = map(int, list(data.values())[0].split('&'))  # problem_id and team_id from form
        process = db_sess.query(__all_tables.contests.SolvingProcess).filter(
            __all_tables.contests.SolvingProcess.team_id == t_id,
            __all_tables.contests.SolvingProcess.problem_id == pr_id).first()
        process.ok = ok
        db_sess.commit()
    db_sess = __db_session.create_session()
    data = []
    counter = 0
    for i in db_sess.query(__all_tables.contests.SolvingProcess).filter(__all_tables.contests.SolvingProcess.ok == 2):
        data.append([i, str(counter), str(counter + 1), str(i.problem.id) + '&' + str(i.team.id)])
        counter += 2
    return render_template("checking_page.html", answers=data)


@app.route('/results', methods=['GET', 'POST'])
def results():
    db_sess = __db_session.create_session()
    res = extract_and_calc_results.all_results(db_sess)
    teams = [(el[0], el[2][0]) for el in res]
    return render_template('results.html',  # ADD BOTH LISTS
                           results=res,
                           teams=teams)


"""[('команда1', [[1, 2, 3, 4],
                   [5, 6, 7, 8],
                   [9, 10, 11, 12],
                   [13, 14, 15, 16]], (136, '1+4+1+130'))]"""


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect("/main")


if __name__ == "__main__":
    __db_session.global_init("db_interaction/users_data.db")
    app.run(port=8080, host="127.0.0.1")
