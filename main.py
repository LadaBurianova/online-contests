from flask import Flask, render_template, redirect, request
from flask_login import LoginManager, login_user, logout_user, login_required
from forms.user import RegistrationForm, LoginForm
from db_interaction import __db_session
from db_interaction.teams import User

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)


def check_answers(answer, team):    # HERE YOU CHECK ANSWERS
    pass


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
        return redirect('/login')
    return render_template('register_form.html', title='Регистрация', form=form)


@app.route('/solving', methods=['POST'])
def solving():
    if request.method == 'POST':
        check_answers(dict(request.form), 'TEAM')   # ADD WHICH TEAM SUBMITTED
        return redirect('/solving')
    return render_template('thing.html', problems=[])   # ADD PROBLEMS


@app.route('/results')
def results():
    return render_template('results.html',              # ADD BOTH LISTS
                           results=[('команда1', [
                               [1, 2, 3, 4],
                               [5, 6, 7, 8],
                               [9, 10, 11, 12],
                               [13, 14, 15, 16]
                           ], (136, '1+4+1+130'))],
                           teams=[('команда1', 136)])


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


if __name__ == "__main__":
    __db_session.global_init("db_interaction/users_data.db")
    app.run(port=8080, host="127.0.0.1")
