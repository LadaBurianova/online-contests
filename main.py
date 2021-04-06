from flask import Flask
from db_interaction import __db_session

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


if __name__ == "__main__":
    __db_session.global_init("db_interaction/users_data.db")
    app.run(port=8080, host="127.0.0.1")
