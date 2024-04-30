import json
import os

import requests
from flask import Flask, redirect, request
from flask import render_template
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

from data import db_session
from data.add_product_form import AddProductForm
from data.address_form import AddressForm
from data.edit_profile import EditProfileForm
from data.login_form import LoginForm
from data.user import RegisterForm
from data.users import User, Product, Address, AddProduct

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)


def get_name_by_id(user_id):
    db_sess = db_session.create_session()
    temp = db_sess.query(User).filter(User.id == str(user_id)).first()
    db_sess.close()
    if temp:
        return temp.name
    return ''


def get_all_address():
    db_sess = db_session.create_session()
    temp = db_sess.query(Address).all()
    db_sess.close()
    if temp:
        return temp
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
            dct[i[2]][6] = round(dct[i[2]][6], 5)
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


def get_email_by_id(user_id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == str(user_id)).first()
    db_sess.close()
    if user:
        return user.email
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
                print(file)
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


def get_coord(st):
    geocoder_request = f"http://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493-4b70-98ba-98533de7710b&geocode={st}&format=json"

    response = requests.get(geocoder_request).json()
    longitude, lattitude = response["response"]["GeoObjectCollection"]["featureMember"][0]['GeoObject']["Point"][
        "pos"].split()
    return float(longitude), float(lattitude)


def getImage(coords):
    map_request = f"http://static-maps.yandex.ru/1.x/?lang=ru_RU&ll=30.258814,59.908805&size=500,450&z=10&apikey=1a414c4d-1ca3-4d7a-accf-39ce347917f8&l=map"
    if coords:
        res = '&pt='
        for i in coords:
            res += f'{i[0]},{i[1]},pm2dbm~'
        map_request += res.strip('~')

    response = requests.get(map_request)
    if not response:
        print("Http статус:", response.status_code, "(", response.reason, ")")

    # Запишем полученное изображение в файл.
    map_file = "static/images/map.png"
    with open(map_file, "wb") as file:
        file.write(response.content)


def get_map():
    cords = get_all_address()
    lst = []
    for i in cords:
        lst.append(get_coord(i.desc))
    getImage(lst)


@app.route('/address', methods=['POST', 'GET'])
def address_page():
    get_map()
    form = AddressForm()

    if request.method == 'POST':
        db_sess = db_session.create_session()
        address = Address()

        address.name = form.name.data
        address.desc = form.desc.data
        address.work_time = form.work_time.data
        print(form.name.data, form.desc.data, form.work_time.data)
        db_sess.add(address)
        db_sess.commit()
        db_sess.close()
        get_map()
        return redirect('/address')

    user = get_email_by_id(current_user)
    flag = False
    if user == 'admin@gmail.com':
        flag = True

    return render_template('address.html',
                           username=get_name_by_id(current_user),
                           filename=get_src_by_id(current_user),
                           products=len(get_product_by_id(current_user)),
                           active_page='find_a_store',
                           items=get_all_address(),
                           flag=flag,
                           form=form)


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


def get_all_products_by_group(group):
    db_sess = db_session.create_session()
    res = db_sess.query(AddProduct).filter(AddProduct.group == str(group)).all()

    if res:
        return res
    return ''


def get_product_by_name(name):
    db_sess = db_session.create_session()
    res = db_sess.query(AddProduct).filter(AddProduct.name == str(name)).first()
    if res:
        return res
    return ''


@app.route('/menu', methods=['GET', 'POST'])
def blog_page():
    form = AddProductForm()
    if request.method == 'POST':
        name = list(request.values.items())[-1][0]
        if name == 'add_product':
            try:
                db_sess = db_session.create_session()
                add_product = AddProduct()

                add_product.name = form.name.data
                add_product.price = form.price.data
                add_product.desc = form.desc.data
                add_product.group = form.group.data

                file = form.file.data

                src = f'static/images/{file.filename}'
                file.save(src)

                add_product.file = src

                db_sess.add(add_product)
                db_sess.commit()
                db_sess.close()
            except Exception as ex:
                print(ex)
                redirect('/menu')
        else:
            info_product = get_product_by_name(name)
            db_sess = db_session.create_session()
            # print(info_product)
            product = Product()

            product.user_id = str(current_user)
            product.name = name
            product.price = info_product.price
            product.image_src = info_product.file

            db_sess.add(product)
            db_sess.commit()

        return redirect('/menu')

    drinks = some_func('Drinks')
    food = some_func('Food')
    flag = True if get_email_by_id(current_user) == 'admin@gmail.com' else False

    return render_template('menu.html',
                           username=get_name_by_id(current_user),
                           filename=get_src_by_id(current_user),
                           products=len(get_product_by_id(current_user)),
                           active_page='menu', drinks=drinks, food=food, form=form, flag=flag)


def some_func(group):
    items = []
    item = []
    lst = get_all_products_by_group(group)
    for i in range(len(lst)):
        item.append(lst[i])
        if i % 2 == 1 and i != 0:
            items.append(item)
            item = []
    if item:
        items.append(item)
    return items


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
    print(info)
    info2 = get_product_no_repeat(info)
    result = 0
    for k, v in info2.items():
        result += v[-1]
    return render_template('market_buy.html',
                           username=get_name_by_id(current_user),
                           filename=get_src_by_id(current_user), products_list=info2,
                           products=len(info),
                           result=round(result, 2))


@app.route('/pay', methods=['POST', 'GET'])
def pay():
    # если нет адреса не давать купить
    return ''


def main():
    db_session.global_init('db/users_data_base.db')
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)


if __name__ == '__main__':
    main()
