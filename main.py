from flask import Flask
from data import db_session
from data.users import User
from data.products import Products
from data.basket import Baskets

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


def main():
    db_session.global_init("db/data.db")
    user = User()
    db_sess = db_session.create_session()
    user.surname = "Колесникова"
    user.name = 'Елизавета'
    user.email = "Ekolesnikova2005@yandex.ru"
    user.username = 'Lizok'
    user.hashed_password = '1234567890'
    db_sess.add(user)
    db_sess.commit()
    products1 = Products()
    db_sess = db_session.create_session()
    products1.products = "Телефон1"
    products1.description = 'Намбер ван'
    products1.img_scr = "gfregre"
    db_sess.add(products1)
    db_sess.commit()
    bas = Baskets()
    db_sess = db_session.create_session()
    bas.id = 1
    bas.id_of_person = 1
    bas.list_of_products = 1
    db_sess.add(bas)
    db_sess.commit()
    #app.run()


if __name__ == '__main__':
    main()