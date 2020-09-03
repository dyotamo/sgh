from os import environ
from flask import Flask, render_template, jsonify, redirect, url_for, flash
from flask_minify import minify
from flask_login import LoginManager, login_required, login_user, logout_user

from models import User
from dao import get
from forms.login import LoginForm
from utils.security import allowed_profile, check_user

from views import rooms, companies, users, guests


app = Flask(__name__)
app.config['SECRET_KEY'] = environ['SECRET_KEY']

app.register_blueprint(rooms)
app.register_blueprint(companies)
app.register_blueprint(users)
app.register_blueprint(guests)


if bool(environ.get('PRODUCTION')):
    mini = minify(html=True, js=True, cssless=True)
    mini.init_app(app)


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'É necessário autenticar-se.'
login_manager.login_message_category = "warning"


@login_manager.user_loader
def load_user(user_id):
    return get(User, user_id)


@app.route('/', methods=['GET'])
@login_required
@allowed_profile(['receptionist', 'manager', 'admin'])
def index():
    return render_template('index.html')


@app.errorhandler(404)
def not_found(e):
    resp = jsonify(dict(error="not found"))
    resp.status_code = 404
    return resp


@app.errorhandler(403)
def forbidden(e):
    resp = jsonify(dict(error="forbidden"))
    resp.status_code = 403
    return resp


@app.route('/accounts/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        user = check_user(email=email, password=password)

        if user is None:
            flash('Credenciais inválidas.', 'danger')
        else:
            login_user(user)
            flash('Entrou como {}.'.format(user.email), 'success')
            return redirect(url_for('index'))
    return render_template('accounts/login.html', form=form)


@app.route('/accounts/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
