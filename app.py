import datetime
import json
import os
import pprint

from flask import url_for
from flask import Flask, redirect, request
from data import db_session
from data.users import User
from flask import render_template
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from data.login_form import LoginForm
from data.user import RegisterForm
from werkzeug.utils import secure_filename
from data.edit_profile import EditProfileForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
app.config['UPLOADED_IMAGES_DEST'] = 'static/avatars'
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
        return temp.name
    return ''


def get_src_by_id(user_id):
    db_sess = db_session.create_session()
    temp = db_sess.query(User).filter(User.id == str(user_id)).first()
    if temp:
        return temp.file
    return ''


@app.route('/home')
@app.route('/')
def home_page():
    return render_template('index.html', username=get_name_by_id(current_user), filename=get_src_by_id(current_user))


@app.route('/myprofile', methods=['GET', 'POST'])
def my_profile():
    form = EditProfileForm()
    db_sess = db_session.create_session()
    res = db_sess.query(User).filter(User.id == str(current_user)).first()
    if request.method == 'POST':
        if form.validate_on_submit():
            try:
                file = form.file.data
                frm = file.mimetype.split('/')[-1]
                name_fl = file.filename.split(frm)[0][0:-1:1]
                user = db_sess.query(User).filter(User.id == str(current_user)).first()
                src = f'static/avatars/{name_fl}_{str(user.id)}.{frm}'
                file.save(src)

                res.name = form.name.data if form.name.data else res.name
                res.surname = form.surname.data if form.surname.data else res.surname
                res.email = form.email.data if form.email.data else res.email
                res.phone = form.phone.data if form.phone.data else res.phone
                res.file = src if file else res.file

                # Адрес запись в db
                res.street = form.street.data if form.street.data else res.street
                res.apartment = form.apartment.data if form.apartment.data else res.apartment
                res.entrance = form.entrance.data if form.entrance.data else res.entrance
                res.floor = form.floor.data if form.floor.data else res.floor
                res.intercom = form.intercom.data if form.intercom.data else res.intercom

                db_sess.add(res)
                db_sess.commit()
                return redirect('/myprofile')
            except Exception:
                return redirect('/myprofile')
    elif request.method == 'GET':
        return render_template('myprofile.html', first_name=res.name, surname=res.surname, username=res.name,
                               filename=res.file, form=form, phone=res.phone, email=res.email,
                               street=res.street, apartment=res.apartment, entrance=res.entrance,
                               floor=res.floor, intercom=res.intercom)


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
            surname=form.surname.data,
            email=form.email.data,
            phone=form.phone.data,
            file='static/avatars/base_avatar.png'
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
    return render_template('address.html', username=get_name_by_id(current_user), filename=get_src_by_id(current_user))


@app.route('/blog')
def blog_page():
    return render_template('blog.html', username=get_name_by_id(current_user), filename=get_src_by_id(current_user))


@app.route('/recipes')
def recipes_page():
    with open('static/coffe.json') as file:
        data = json.load(file)
        lst = [data['list1'], data['list2'], data['list3']]
        pprint.pprint(lst)
    return render_template('recipes.html', username=get_name_by_id(current_user), filename=get_src_by_id(current_user),
                           item=lst)


@app.route('/recipes/<coffee_type>')
def coffee_page(coffee_type):
    if coffee_type in ['espresso', 'americano', 'cappuccino',
                       'kon_panna', 'latte', 'lungo', 'macchiato', 'ristretto', 'mocha']:
        return render_template(f'{coffee_type}.html')
    else:
        abort(404)


def main():
    db_session.global_init('db/users_data_base.db')
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)


if __name__ == '__main__':
    main()
