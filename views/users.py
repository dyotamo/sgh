from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import login_required
from playhouse.flask_utils import object_list
from peewee import IntegrityError

from models import User
from dao import get_all, get
from forms.user import UserForm
from utils.security import allowed_profile
from utils.extra import get_formdata
from utils.validators import validate_user


users = Blueprint('users', __name__, url_prefix='/users')


@users.route('/', methods=['GET'])
@login_required
@allowed_profile(['admin'])
def user_index():
    return object_list('users/index.html', query=get_all(User),
                       context_variable='users', paginate_by=7, check_bounds=False)


@users.route('/new', methods=['GET', 'POST'])
@login_required
@allowed_profile(['admin'])
def user_new():
    user = User()
    if request.method == 'POST':
        form = UserForm(request.form, obj=user)
        if form.validate():
            try:
                form.populate_obj(user)
                validate_user(user)
                user.save()
                flash('Yes, usuário cadastrado com sucesso.', 'success')
                return redirect(url_for('users.user_index'))
            except AttributeError as e:
                flash(str(e), 'warning')
    else:
        form = UserForm(obj=user)
    return render_template('users/new.html', form=form)


@users.route('/<int:user_id>/edit', methods=['GET', 'POST'])
@login_required
@allowed_profile(['admin'])
def user_edit(user_id: int):
    user = get(User, user_id)
    if request.method == 'POST':
        form = UserForm(request.form, obj=user)
        if form.validate():
            form.populate_obj(user)
            user.save()
            flash('Yes, usuário alterado com sucesso.', 'success')
            return redirect(url_for('users.user_index'))
    else:
        form = UserForm(obj=user)
    return render_template('users/edit.html', form=form)
