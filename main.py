from flask import Flask, render_template, redirect, request
from flask_login import LoginManager, login_user, logout_user, login_required
from forms.user import RegistrationForm, LoginForm
from db_interaction import __db_session
from db_interaction.teams import User
from db_interaction.contests import SolvingProcess
from db_interaction.problems import Problem
from random import shuffle

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = __db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/', methods=['GET', 'POST'])
def main_page():
    return render_template('base.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = __db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect('/')
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
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register_form.html', title='Регистрация', form=form,
                                   message="Такой пользователь уже есть")
        user = User(email=form.email.data)
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/main')
    return render_template('register_form.html', title='Регистрация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/check', methods=['GET', 'POST'])
def check():
    """Page for checking answers. Button 0- for wrong, 1- for correct."""
    if request.method == 'POST':
        db_sess = __db_session.create_session()
        data = request.form.to_dict()
        ok = int(list(data.keys())[0]) % 2
        pr_id, t_id = map(int, list(data.values())[0].split('&'))
        process = db_sess.query(SolvingProcess).filter(SolvingProcess.team_id == t_id, SolvingProcess.problem_id == pr_id).first()
        print(process)
        process.ok = ok
        db_sess.commit()
    db_sess = __db_session.create_session()
    data = []
    counter = 0
    for i in db_sess.query(SolvingProcess).filter(SolvingProcess.ok == 2):
        data.append([i, str(counter), str(counter + 1),
                     str(i.problem.id) + '&' + str(i.team.id)])  # i.problem.correct_answer, i.answer
        counter += 2
    return render_template("checking_page.html", answers=data)


if __name__ == "__main__":
    __db_session.global_init("db_interaction/users_data.db")
    app.run(port=8080, host="127.0.0.1")
