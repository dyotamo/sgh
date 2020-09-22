from os import environ

from flask import Flask, render_template, redirect, url_for, flash
from flask_minify import minify
from flask_login import LoginManager, login_required, login_user, logout_user

from models import User
from dao import get
from forms.login import LoginForm
from utils.security import allowed_profile, check_user
from views import rooms, companies, users, guests, room_types, reservations, checkins
from template_filters import pretty_date
from context_processors import pagination_processor


app = Flask(__name__)
app.config['SECRET_KEY'] = environ['SECRET_KEY']

app.register_blueprint(rooms)
app.register_blueprint(companies)
app.register_blueprint(users)
app.register_blueprint(guests)
app.register_blueprint(room_types)
app.register_blueprint(reservations)
app.register_blueprint(checkins)

# Registering template filters
app.add_template_filter(pretty_date, 'pretty_date')

# Template context processors
app.context_processor(pagination_processor)

# Minify if in production
if bool(environ.get('PRODUCTION')):
    mini = minify(html=True, js=True, cssless=True)
    mini.init_app(app)

# Flask login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'É necessário autenticar-se.'
login_manager.login_message_category = "warning"


@login_manager.user_loader
def load_user(user_id):
    return get(User, user_id)


@app.route('/accounts/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = check_user(email=email, password=password)
        if user is None:
            flash('Credenciais inválidas.', 'warning')
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


@app.errorhandler(404)
def not_found(e):
    return render_template('errors/404.html')


@app.errorhandler(403)
def forbidden(e):
    return render_template('errors/403.html')


@app.errorhandler(405)
def method_not_allowed(e):
    return render_template('errors/405.html')


@app.errorhandler(505)
def server_error(e):
    return render_template('errors/505.html')


@app.route('/', methods=['GET'])
@login_required
@allowed_profile(['receptionist', 'manager', 'admin'])
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
