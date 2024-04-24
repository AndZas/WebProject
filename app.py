import json
import os

from flask import url_for
from flask import Flask, redirect, request
from data import db_session
from data.users import User, Product
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

products_dct = {
    'espresso': [3.1, '../static/images/Default_Espresso_0.jpg'],
    'cappuccino': [3.1, '../static/images/капучино.png'],
    'frappuccino': [3.1, '../static/images/Default_Frappuccino_1.jpg'],
    'hot_chocolate': [3, '../static/images/Default_Hot_chocolate_1.jpg'],
    'irish_coffee': [3.1, '../static/images/Default_Irish_coffee_0.jpg'],
    'vanilla_latte': [3, '../static/images/Default_Vanilla_latte_1.jpg'],
    'vanilla_mocha': [3, '../static/images/Default_Vanilla_mocha_1.jpg'],
    'caramel_mocha': [3, '../static/images/Default_Caramel_mocha_1.jpg'],
    'cheesecake': [2.5, '../static/images/Default_Cheesecake_0.jpg'],
    'croissant': [1.5, '../static/images/Default_Croissant_0.jpg'],
    'muffin': [2, '../static/images/Default_Muffin_0.jpg'],
    'tiramisu': [5, '../static/images/Default_Tiramisu_1.jpg'],
    'sandwich': [2, '../static/images/Default_sandwich_0.jpg'],
    'cookies': [1.5, '../static/images/Default_Cookie_1.jpg'],
}


def get_name_by_id(user_id):
    db_sess = db_session.create_session()
    temp = db_sess.query(User).filter(User.id == str(user_id)).first()
    db_sess.close()
    if temp:
        return temp.name
    return ''


def get_product_no_repeat(lst):
    dct = {}
    for i in lst:
        if i[2] not in dct:
            dct[i[2]] = [i[0], [i[1]], i[2], i[3], i[4], 1, i[3]]
        else:
            dct[i[2]][1].append(i[1])
            dct[i[2]][5] += 1
            dct[i[2]][6] += i[3]
    dct = {k: v for k, v in sorted(dct.items(), key=lambda x: x[1][5])[::-1]}
    return dct


def get_product_by_id(user_id):
    db_sess = db_session.create_session()
    try:
        temp = db_sess.query(Product).filter(Product.user_id == str(user_id)).all()
        lst = []
        for i in temp:
            lst.append([i.user_id, i.id, i.name, i.price, i.image_src])
        db_sess.close()
        if temp:
            return lst
        return ''
    except Exception:
        return ''


def get_src_by_id(user_id):
    db_sess = db_session.create_session()
    temp = db_sess.query(User).filter(User.id == str(user_id)).first()
    db_sess.close()
    if temp:
        return temp.file
    return ''


@app.route('/home')
@app.route('/')
def home_page():
    return render_template('index.html', username=get_name_by_id(current_user), filename=get_src_by_id(current_user),
                           products=len(get_product_by_id(current_user)))


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
        return render_template('myprofile.html',
                               first_name=res.name, surname=res.surname,
                               username=res.name, filename=res.file,
                               form=form, phone=res.phone,
                               email=res.email, street=res.street,
                               apartment=res.apartment, entrance=res.entrance,
                               floor=res.floor, intercom=res.intercom,
                               products=len(get_product_by_id(current_user))
                               )


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
            return render_template('register.html',
                                   title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html',
                                   title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")

        user = User()

        user.name = form.name.data
        user.surname = form.surname.data
        user.email = form.email.data
        user.phone = form.phone.data

        user.file = 'static/avatars/base_avatar.png'
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


@app.route('/address')
def address_page():
    return render_template('address.html',
                           username=get_name_by_id(current_user),
                           filename=get_src_by_id(current_user),
                           products=len(get_product_by_id(current_user)),
                           active_page='find_a_store')


@app.route('/about_us')
def about_us_page():
    return render_template('about_us.html',
                           username=get_name_by_id(current_user),
                           filename=get_src_by_id(current_user),
                           products=len(get_product_by_id(current_user)),
                           active_page='about_us')


@app.route('/about_coffee')
def about_coffee_page():
    return render_template('about_coffee.html',
                           username=get_name_by_id(current_user),
                           filename=get_src_by_id(current_user),
                           products=len(get_product_by_id(current_user)),
                           active_page='about_coffee')


@app.route('/menu', methods=['POST', 'GET'])
def blog_page():
    if request.method == 'POST':
        name = list(request.values.items())[0][0]
        info_product = products_dct[name]
        db_sess = db_session.create_session()

        product = Product()

        product.user_id = str(current_user)
        product.name = name
        product.price = info_product[0]
        product.image_src = info_product[1]

        db_sess.add(product)
        db_sess.commit()
        return redirect('/menu')
    prices = [i[0] for i in products_dct.values()]
    return render_template('menu.html',
                           username=get_name_by_id(current_user),
                           filename=get_src_by_id(current_user),
                           products=len(get_product_by_id(current_user)),
                           active_page='menu', prices=prices)


@app.route('/recipes')
def recipes_page():
    with open('static/coffe.json') as file:
        data = json.load(file)
        lst = [data['list1'], data['list2'], data['list3']]
    return render_template('recipes.html',
                           username=get_name_by_id(current_user),
                           filename=get_src_by_id(current_user),
                           item=lst,
                           products=len(get_product_by_id(current_user)),
                           active_page='recipes')


@app.route('/recipes/<coffee_type>')
def coffee_page(coffee_type):
    if coffee_type in ['espresso', 'americano', 'cappuccino',
                       'kon_panna', 'latte', 'lungo', 'macchiato', 'ristretto', 'mocha']:
        return render_template(f'{coffee_type}.html',
                               username=get_name_by_id(current_user),
                               filename=get_src_by_id(current_user),
                               products=len(get_product_by_id(current_user)))
    else:
        abort(404)


@app.route('/cart', methods=['POST', 'GET'])
def cart():
    if request.method == 'POST':
        name = list(request.values.items())[0][0]
        db_sess = db_session.create_session()
        record = db_sess.query(Product).filter(Product.id == name).first()
        if record:
            db_sess.delete(record)
            db_sess.commit()
            db_sess.close()
        redirect('/cart')

    info = get_product_by_id(current_user)
    info2 = get_product_no_repeat(info)
    result = 0
    for k, v in info2.items():
        result += v[-1]
    return render_template('market_buy.html',
                           username=get_name_by_id(current_user),
                           filename=get_src_by_id(current_user), products_list=info2,
                           products=len(info),
                           result=result)


@app.route('/pay', methods=['POST', 'GET'])
def pay():
    return ''


def main():
    db_session.global_init('db/users_data_base.db')
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)


if __name__ == '__main__':
    main()
