import sqlalchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from .db_session import SqlAlchemyBase


class User(SqlAlchemyBase, UserMixin):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    email = sqlalchemy.Column(sqlalchemy.String, index=True, unique=True, nullable=True)
    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    def __repr__(self):
        return str(self.id)

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)


class Item(SqlAlchemyBase, UserMixin):
    __tablename__ = 'files'

    user_id = sqlalchemy.Column(sqlalchemy.Integer)
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, unique=True)
    src = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    file_name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    date = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    status = sqlalchemy.Column(sqlalchemy.Integer)

    def __repr__(self):
        return f'Запись: {str(self.id)} Юзер: {self.user_id}'