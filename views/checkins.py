from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import login_required
from peewee import IntegrityError

from models import CheckIn
from dao import get_all, create, get, update
from forms.checkin import CheckInForm
from utils.security import allowed_profile
from utils.extra import get_formdata
from utils.validators import validate_check_in
from services import toogle_activation


checkins = Blueprint('checkins', __name__, url_prefix='/checkins')


@checkins.route('/', methods=['GET'])
@login_required
@allowed_profile(['receptionist', 'manager', 'admin'])
def checkin_index():
    return render_template('checkins/index.html', checkins=get_all(CheckIn))


@checkins.route('/new', methods=['GET', 'POST'])
@login_required
@allowed_profile(['receptionist', 'manager', 'admin'])
def checkin_new():
    form = CheckInForm()
    if form.validate_on_submit():
        try:
            data = get_formdata(form)
            validate_check_in(data)
            create(CheckIn, **data)
            flash('Yes, checkin cadastrado com sucesso.', 'success')
            return redirect(url_for('checkins.checkin_index'))
        except AttributeError as e:
            flash(str(e), 'warning')
    return render_template('checkins/new.html', form=form)


@checkins.route('/<int:checkin_id>/edit', methods=['GET', 'POST'])
@login_required
@allowed_profile(['receptionist', 'manager', 'admin'])
def checkin_edit(checkin_id: int):
    form = CheckInForm(obj=get(CheckIn, checkin_id))
    if form.validate_on_submit():
        try:
            data = get_formdata(form)
            validate_check_in(data)
            update(CheckIn, checkin_id, **data)
            flash('Yes, checkin alterado com sucesso.', 'success')
            return redirect(url_for('checkins.checkin_index'))
        except AttributeError as e:
            flash(str(e), 'warning')
    return render_template('checkins/edit.html', form=form)


@checkins.route('/<int:checkin_id>/deactivate', methods=['GET', 'POST'])
@login_required
@allowed_profile(['manager', 'admin'])
def checkin_deactivate(checkin_id: int):
    checkin = get(CheckIn, checkin_id)
    if request.method == 'POST':
        toogle_activation(checkin)
        flash('Yes, checkin {} com sucesso.'.format(
            'reactivado' if checkin.is_active else 'desactivado'), 'success')
        return redirect(url_for('checkins.checkin_index'))
    return render_template('checkins/deactivate.html', checkin=checkin)
