import datetime
from flask import Flask, render_template, render_template_string, request, redirect, url_for, session, make_response
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length
from flask_wtf import FlaskForm
import re


app = Flask(__name__)

app.config['SECRET_KEY'] = 'xxxxxxx'

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=20)])
    submit = SubmitField('Register')
    
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=20)])
    submit = SubmitField('Login')

class Candy:
    def __init__(self, name, image):
        self.name = name
        self.image = image

class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def verify_password(self, username, password):
        return (self.username==username) & (self.password==password)
class Admin:
    def __init__(self):
        self.username = ""
        self.identity = ""

def sanitize_inventory_sold(value):
    return re.sub(r'[a-zA-Z_]', '', str(value))
def merge(src, dst):
    for k, v in src.items():
        if hasattr(dst, '__getitem__'):
            if dst.get(k) and type(v) == dict:
                merge(v, dst.get(k))
            else:
                dst[k] = v
        elif hasattr(dst, k) and type(v) == dict:
            merge(v, getattr(dst, k))
        else:
            setattr(dst, k, v)

candies = [Candy(name="Lollipop", image="images/candy1.jpg"),
    Candy(name="Chocolate Bar", image="images/candy2.jpg"),
    Candy(name="Gummy Bears", image="images/candy3.jpg")
]
users = []
admin_user = []
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, password=form.password.data)
        users.append(user)
        return redirect(url_for('login'))
    
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        for u in users:
            if u.verify_password(form.username.data, form.password.data):
                session['username'] = form.username.data
                session['identity'] = "guest"
                return redirect(url_for('home'))
    
    return render_template('login.html', form=form)

inventory = 500
sold = 0
@app.route('/home', methods=['GET', 'POST'])
def home():
    global inventory, sold
    message = None
    username = session.get('username')
    identity = session.get('identity')

    if not username:
        return redirect(url_for('register'))
    
    if sold >= 10 and sold < 500:
        sold = 0
        inventory = 500
        message = "But you have bought too many candies!"
        return render_template('home.html', inventory=inventory, sold=sold, message=message, candies=candies)

    if request.method == 'POST':
        action = request.form.get('action')
        if action == "buy_candy":
            if inventory > 0:
                inventory -= 3
                sold += 3
            if inventory == 0:
                message = "All candies are sold out!"
            if sold >= 500:
                with open('secret.txt', 'r') as file:
                    message = file.read()

    return render_template('home.html', inventory=inventory, sold=sold, message=message, candies=candies)


@app.route('/admin', methods=['GET', 'POST'])
def admin():
    username = session.get('username')
    identity = session.get('identity')
    if not username or identity != 'admin':
        return redirect(url_for('register'))
    admin = Admin()
    merge(session,admin)
    admin_user.append(admin)
    return render_template('admin.html', view='index')

@app.route('/admin/view_candies', methods=['GET', 'POST'])
def view_candies():
    username = session.get('username')
    identity = session.get('identity')
    if not username or identity != 'admin':
        return redirect(url_for('register'))
    return render_template('admin.html', view='candies', candies=candies)

@app.route('/admin/add_candy', methods=['GET', 'POST'])
def add_candy():
    username = session.get('username')
    identity = session.get('identity')
    if not username or identity != 'admin':
        return redirect(url_for('register'))
    candy_name = request.form.get('name')
    candy_image = request.form.get('image')
    if candy_name and candy_image:
        new_candy = Candy(name=candy_name, image=candy_image)
        candies.append(new_candy)
    return render_template('admin.html', view='add_candy')

@app.route('/admin/view_inventory', methods=['GET', 'POST'])
def view_inventory():
    username = session.get('username')
    identity = session.get('identity')
    if not username or identity != 'admin':
        return redirect(url_for('register'))
    inventory_value = sanitize_inventory_sold(inventory)
    sold_value = sanitize_inventory_sold(sold)
    return render_template_string("商店库存:" + inventory_value + "已售出" + sold_value)

@app.route('/admin/add_inventory', methods=['GET', 'POST'])
def add_inventory():
    global inventory
    username = session.get('username')
    identity = session.get('identity')
    if not username or identity != 'admin':
        return redirect(url_for('register'))
    if request.form.get('add'):
        num = request.form.get('add')
        inventory += int(num)
    return render_template('admin.html', view='add_inventory')

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=1337)
