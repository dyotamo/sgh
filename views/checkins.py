from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import login_required
from peewee import IntegrityError
from playhouse.flask_utils import object_list

from models import CheckIn, CheckInGuest
from dao import get_all, get, delete
from forms.checkin import CheckInForm, CheckInGuestForm
from utils.security import allowed_profile
from utils.extra import get_formdata
from utils.validators import (
    validate_check_in_creation, validate_check_in_edit, validate_check_in_guest)


checkins = Blueprint('checkins', __name__, url_prefix='/checkins')


@checkins.route('/', methods=['GET'])
@login_required
@allowed_profile(['receptionist', 'manager', 'admin'])
def checkin_index():
    return object_list('checkins/index.html', query=get_all(CheckIn),
                       context_variable='checkins', paginate_by=7, check_bounds=False)


@checkins.route('/new', methods=['GET', 'POST'])
@login_required
@allowed_profile(['receptionist', 'manager', 'admin'])
def checkin_new():
    checkin = CheckIn()
    if request.method == 'POST':
        form = CheckInForm(request.form, obj=checkin)
        if form.validate():
            try:
                form.populate_obj(checkin)
                validate_check_in_creation(checkin)
                checkin.save()
                flash('Yes, check in feito com sucesso.', 'success')
                return redirect(url_for('checkins.checkin_index'))
            except AttributeError as e:
                flash(str(e), 'warning')
    else:
        form = CheckInForm(obj=checkin)
    return render_template('checkins/new.html', form=form)


@checkins.route('/<int:checkin_id>/edit', methods=['GET', 'POST'])
@login_required
@allowed_profile(['receptionist', 'manager', 'admin'])
def checkin_edit(checkin_id: int):
    checkin = get(CheckIn, checkin_id)
    if request.method == 'POST':
        form = CheckInForm(request.form, obj=checkin)
        if form.validate():
            try:
                form.populate_obj(checkin)
                validate_check_in_edit(checkin)
                checkin.save()
                flash('Yes, check in alterado com sucesso.', 'success')
                return redirect(url_for('checkins.checkin_index'))
            except AttributeError as e:
                flash(str(e), 'warning')
    else:
        form = CheckInForm(obj=checkin)
    return render_template('checkins/edit.html', form=form)


@checkins.route('/<int:checkin_id>', methods=['GET', 'POST'])
@login_required
@allowed_profile(['manager', 'admin'])
def checkin_details(checkin_id: int):
    checkin = get(CheckIn, checkin_id)
    checkinguest = CheckInGuest(check_in=checkin_id)
    if request.method == 'POST':
        form = CheckInGuestForm(request.form, obj=checkinguest)
        if form.validate():
            try:
                form.populate_obj(checkinguest)
                validate_check_in_guest(checkinguest)
                checkinguest.save()
                flash('Yes, hóspede adicionado com sucesso.', 'success')
                return redirect(url_for('checkins.checkin_details', checkin_id=checkin_id))
            except IntegrityError:
                flash('Oops, hóspede já foi cadastrado.', 'warning')
            except AttributeError as e:
                flash(str(e), 'warning')
    else:
        form = CheckInGuestForm(obj=checkinguest)
    return render_template('checkins/details.html', checkin=checkin, form=form)


@checkins.route('/<int:checkin_id>/remove_guest', methods=['POST'])
@login_required
@allowed_profile(['manager', 'admin'])
def checkin_guest_remove(checkin_id: int):
    checkin_guest = get(CheckInGuest, request.form['checkin_guest_id'])
    delete(checkin_guest)
    flash(f'Yes, {checkin_guest.guest.name} removido com sucesso.', 'success')
    return redirect(url_for('checkins.checkin_details', checkin_id=checkin_id))
