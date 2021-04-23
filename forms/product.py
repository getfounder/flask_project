from flask_wtf import FlaskForm
from wtforms import SubmitField


class InBasket(FlaskForm):
    submit = SubmitField('Добавить в Корзину')
