from flask import Flask, render_template, request

app = Flask(__name__)


def form_(s):
    return request.form[s]


@app.route('/form')
def take_form():
    return render_template('form.html')


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
    return render_template('index.html')


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


if __name__ == '__main__':
    app.run(debug=True)

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
