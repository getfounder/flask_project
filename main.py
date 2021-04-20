from flask import Flask, render_template, redirect
from flask_login import LoginManager, logout_user, login_required, login_user

from data import db_session
from data.users import User
from data.login_form import LoginForm

from werkzeug.security import generate_password_hash, check_password_hash

from forms.user import RegisterForm


def set_password(self, password):
    self.hashed_password = generate_password_hash(password)

def check_password(self, password):
    return check_password_hash(self.hashed_password, password)


db_session.global_init("db/data.db")
app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/')
def show():
    return render_template("index.html")

@app.route('/delivery')
def delivery():
    return render_template("delivery.html", title="Доставка")

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.password == form.password.data:
            return redirect("/")
        return render_template('login.html', message="Wrong login or password", form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('registration.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('registration.html', title='Регистрация',
                                   form=form, css_connect='<link rel="stylesheet" href="css/style.css">',
                                   message="Такой пользователь уже есть")
        user = User()
        user.name=form.name.data
        user.email=form.email.data
        user.surname=form.surname.data
        user.password=form.password.data
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('registration.html', title='Регистрация', css_connect='<link rel="stylesheet" href="css/style.css">', form=form)


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
