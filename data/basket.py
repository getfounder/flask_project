import sqlalchemy
from .db_session import SqlAlchemyBase


class Baskets(SqlAlchemyBase):
    __tablename__ = 'basket'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    id_of_person = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    list_of_products = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("products.id"))
