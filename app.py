import datetime
import os

from flask import url_for
from flask import Flask, redirect, request
from data import db_session
from data.users import User
from flask import render_template
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from data.login_form import LoginForm
from data.user import RegisterForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)


def form_(s):
    return request.form[s]


@app.route('/form')
def take_form():
    return render_template('form.html')


def get_name_by_id(user_id):
    db_sess = db_session.create_session()
    temp = db_sess.query(User).filter(User.id == str(user_id)).first()
    if temp:
        print(temp.name)
        return temp.name
    return ''


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/result', methods=['POST'])
def show_result():
    beans = form_('beans')
    bean_type = form_('beantype')
    bags = form_('bags')
    date = form_('date')
    extras = form_('extras[]')
    name = form_('name')
    address = form_('address')
    city = form_('city')
    state = form_('state')
    zip_ = form_('zip')
    phone = form_('phone')
    comments = form_('comments')
    lst = [beans, bean_type, bags, date, extras, name, address, city, state, zip_, phone]
    if all(lst):
        return render_template('result.html',
                               beans_the=beans, bean_type_the=bean_type,
                               bags_the=bags, date_the=date,
                               extras_the=extras, name_the=name,
                               address_the=address, city_the=city,
                               state_the=state, zip_the=zip_,
                               phone_the=phone, comments_the=comments)
    else:
        return 'Не все поля были заполнены'


@app.route('/address')
def address_page():
    return render_template('address.html')


@app.route('/home')
@app.route('/')
def home_page():
    name = get_name_by_id(current_user)
    return render_template('index.html', username=name)


@app.route('/blog')
def blog_page():
    return render_template('blog.html')


@app.route('/recipes')
def recipes_page():
    return render_template('recipes.html')


@app.route('/recipes/espresso')
def espresso_coffe_page():
    return render_template('эспрессо.html')


@app.route('/recipes/americano')
def americano_coffe_page():
    return render_template('американо.html')


@app.route('/recipes/cappuccino')
def cappuccino_coffe_page():
    return render_template('капучино.html')


@app.route('/recipes/kon_panna')
def kon_panna_coffe_page():
    return render_template('кон_панна.html')


@app.route('/recipes/latte')
def latte_coffe_page():
    return render_template('латте.html')


@app.route('/recipes/lungo')
def lungo_coffe_page():
    return render_template('лунго.html')


@app.route('/recipes/macchiato')
def macchiato_coffe_page():
    return render_template('макиато.html')


@app.route('/recipes/ristretto')
def ristretto_coffe_page():
    return render_template('ристретто.html')


@app.route('/recipes/mocha')
def mocha_coffe_page():
    return render_template('мокко.html')


def main():
    db_session.global_init('db/users_data_base.db')
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)


if __name__ == '__main__':
    main()

# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///login.db'
# db = SQLAlchemy(app)
#
#
# class Item(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String(100), nullable=False)
#     price = db.Column(db.Integer, nullable=False)
#     isActive = db.Column(db.Boolean, default=True)
#     # text = db.Column(db.Text, nullable=False)


# чтобы создать базу данных надо в консоли прописать команды
# python
# from app import db
# db.create_all()
# exit()
