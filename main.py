from flask import Flask, render_template, redirect
from flask_login import LoginManager
from flask_ngrok import run_with_ngrok
import os
from data import db_session
from data.products import Products
from data.users import User
from data.login_form import LoginForm

from werkzeug.security import generate_password_hash, check_password_hash

from forms.user import RegisterForm
from forms.product import InBasket

with open("static/txt/logs.txt", mode="w") as is_login_txt:
    is_login_txt.write("False")


def set_password(self, password):
    self.hashed_password = generate_password_hash(password)

def check_password(self, password):
    return check_password_hash(self.hashed_password, password)

db_session.global_init("db/data.db")
app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
run_with_ngrok(app)

login_manager = LoginManager()
login_manager.init_app(app)

with open("static/txt/logs.txt", mode="r") as is_login_txt:
    is_login = is_login_txt.readlines()[0] == "True"

@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/')
def show():
    with open("static/txt/logs.txt", mode="r") as is_login_txt:
        is_login = is_login_txt.readlines()[0] == "True"
    return render_template("index.html", status_login=is_login)

@app.route('/delivery')
def delivery():
    with open("static/txt/logs.txt", mode="r") as is_login_txt:
        is_login = is_login_txt.readlines()[0] == "True"
    return render_template("delivery.html", title="Доставка", status_login=is_login)

@app.route('/smartphones')
def smartphones():
    form = InBasket()
    with open("static/txt/logs.txt", mode="r") as is_login_txt:
        is_login = is_login_txt.readlines()[0] == "True"
    db_sess = db_session.create_session()
    data = db_sess.query(Products).filter(Products.categories == 1)
    return render_template("product.html", title="Каталог", data_info=data, form=form, status_login=is_login)

@app.route('/headphones')
def headphones():
    form = InBasket()
    with open("static/txt/logs.txt", mode="r") as is_login_txt:
        is_login = is_login_txt.readlines()[0] == "True"
    db_sess = db_session.create_session()
    data = db_sess.query(Products).filter(Products.categories == 2)
    return render_template("product.html", title="Каталог", data_info=data, form=form, status_login=is_login)

@app.route('/chargers')
def chargers():
    form = InBasket()
    with open("static/txt/logs.txt", mode="r") as is_login_txt:
        is_login = is_login_txt.readlines()[0] == "True"
    db_sess = db_session.create_session()
    data = db_sess.query(Products).filter(Products.categories == 3)
    return render_template("product.html", title="Каталог", data_info=data, form=form, status_login=is_login)


@app.route('/login', methods=['GET', 'POST'])
def login():
    with open("static/txt/logs.txt", mode="w") as is_login_txt:
        is_login_txt.write("False")
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.password == form.password.data:
            with open("static/txt/logs.txt", mode="w") as is_login_txt:
                is_login_txt.write("True")
            return redirect("/")
        return render_template('login.html',  title='Авторизация', message="Неверный логин или пароль", form=form, status_login=is_login)
    return render_template('login.html', title='Авторизация', form=form, status_login=is_login)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    with open("static/txt/logs.txt", mode="w") as is_login_txt:
        is_login_txt.write("False")
    form = RegisterForm()
    if form.validate_on_submit():
        print(form.validate_on_submit)
        if form.password.data != form.password_again.data:
            return render_template('registration.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают",
                                   status_login=is_login)
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('registration.html', title='Регистрация',
                                   form=form, css_connect='<link rel="stylesheet" href="css/style.css">',
                                   message="Такой пользователь уже есть",
                                   status_login=is_login)
        user = User()
        user.name=form.name.data
        user.email=form.email.data
        user.surname=form.surname.data
        user.password=form.password.data
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('registration.html', title='Регистрация',
                           css_connect='<link rel="stylesheet" href="css/style.css">',
                           form=form,
                           status_login=is_login)


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
