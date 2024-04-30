import sqlalchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from .db_session import SqlAlchemyBase


class AddProduct(SqlAlchemyBase, UserMixin):
    __tablename__ = 'menu_products'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    price = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    desc = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    group = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    file = sqlalchemy.Column(sqlalchemy.String, nullable=True)


class Address(SqlAlchemyBase, UserMixin):
    __tablename__ = 'address'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    desc = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    work_time = sqlalchemy.Column(sqlalchemy.String, nullable=True)


class Product(SqlAlchemyBase, UserMixin):
    __tablename__ = 'products'

    user_id = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String(100), nullable=True)
    price = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    image_src = sqlalchemy.Column(sqlalchemy.String, nullable=True)


class User(SqlAlchemyBase, UserMixin):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    surname = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    phone = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    email = sqlalchemy.Column(sqlalchemy.String, index=True, unique=True, nullable=True)
    file = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    street = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    apartment = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    entrance = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    floor = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    intercom = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    def __repr__(self):
        return str(self.id)

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)
