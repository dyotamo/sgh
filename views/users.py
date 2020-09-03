from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_required

from models import User
from dao import get_all, create, get, update
from forms.user import UserForm
from utils.security import allowed_profile
from utils.extra import get_formdata


users = Blueprint('users', __name__, url_prefix='/users')


@users.route('/', methods=['GET'])
@login_required
@allowed_profile(['admin'])
def user_index():
    return render_template('users/index.html', users=get_all(User))


@users.route('/new', methods=['GET', 'POST'])
@login_required
@allowed_profile(['admin'])
def user_new():
    form = UserForm()
    if form.validate_on_submit():
        data = get_formdata(form)
        data['password'] = 'passwd'  # TODO random generate_password_hash
        create(User, **data)
        flash('Yes, usuário cadastrado com sucesso.', 'success')
        return redirect(url_for('users.user_index'))
    return render_template('users/new.html', form=form)


@users.route('/<int:user_id>/edit', methods=['GET', 'POST'])
@login_required
@allowed_profile(['admin'])
def user_edit(user_id: int):
    form = UserForm(obj=get(User, user_id))
    if form.validate_on_submit():
        data = get_formdata(form)
        update(User, user_id, **data)
        flash('Yes, usuário alterado com sucesso.', 'success')
        return redirect(url_for('users.user_index'))
    return render_template('users/edit.html', form=form)
