import sqlalchemy
from .db_session import SqlAlchemyBase


class Categories(SqlAlchemyBase):
    __tablename__ = 'categories'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    categories = sqlalchemy.Column(sqlalchemy.String)
