import sqlalchemy
from .db_session import SqlAlchemyBase


class Products(SqlAlchemyBase):
    __tablename__ = 'products'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    products = sqlalchemy.Column(sqlalchemy.String)
    description = sqlalchemy.Column(sqlalchemy.String)
    img_scr = sqlalchemy.Column(sqlalchemy.String)
    costs = sqlalchemy.Column(sqlalchemy.Integer)
    count = sqlalchemy.Column(sqlalchemy.Integer)
    categories = sqlalchemy.Column(sqlalchemy.String, sqlalchemy.ForeignKey("categories.id"))
