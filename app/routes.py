from app import app
from flask import render_template, flash, redirect, request, url_for, jsonify #,current_app
from app import app
from app.forms import LoginForm
import requests
from app import db
from flask_login import current_user, login_user
from app.models import User
from flask_login import logout_user
from flask_login import login_required
from flask import request
from urllib.parse import urlparse
from app.forms import RegistrationForm


#routes – URLs where a flask app accepts requests
@app.route('/')
@app.route('/index')
#a view function – route handler
def index():
    user = {'username': 'byan'}
    classes = [{'classInfo': {'code': 'ITE367', 'title': 'Enterprise App Development'}, 'instructor': 'Baoqiang Yan'}, {'classInfo': {'code': 'CS318', 'title': 'Computer Science II'}, 'instructor': 'Adam Lewis'}]
    # print(current_app.config)
    return render_template('index.html', title='Home', user=user, classes=classes) 


@app.route('/login',methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/json', methods=['GET'])
def jsonTest():
    # return jsonify(list(range(5)))
    instructor = {"username": "byan",
                  "role": "instructor",
                  "uid": 11,
                  "name":
                      {"firstname": "Baoqiang",
                       "lastname": "Yan"
                       }
                  }

    return jsonify(instructor)

'''
@app.route('/restlogin', methods=['GET', 'POST'])
def loginAPI():
    json_data = request.get_json(force = True)
    if json_data:
        username = json_data["username"]
        password = json_data["password"]
    else:
        return '{"Success":false}'
    if username == 'byan' and password == '123':
        return '{"Success":true}'
    return '{"Success":false}'
'''

@app.route('/loginapi', methods=['GET', 'POST'])
def loginAPI():
    json_data = request.get_json(force = True)
    if json_data:
        username = json_data["username"]
        password = json_data["password"]
    else:
        return jsonify(Success=False)
    if username == 'byan' and password == '123':
        return jsonify(Success=True, uid=11)
    return jsonify(Success=False)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, password_hash=form.password.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)
