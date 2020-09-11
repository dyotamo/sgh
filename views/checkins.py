from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import login_required
from peewee import IntegrityError
from playhouse.flask_utils import object_list

from models import CheckIn, CheckInGuest
from dao import get_all, create, get, update, delete
from forms.checkin import CheckInForm, CheckInGuestForm
from utils.security import allowed_profile
from utils.extra import get_formdata
from utils.validators import validate_check_in
from services import toogle_activation


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


@checkins.route('/<int:checkin_id>', methods=['GET', 'POST'])
@login_required
@allowed_profile(['manager', 'admin'])
def checkin_details(checkin_id: int):
    checkin = get(CheckIn, checkin_id)
    form = CheckInGuestForm()
    if form.validate_on_submit():
        if checkin.is_active:
            try:
                data = get_formdata(form)
                create(CheckInGuest, check_in=checkin_id, **data)
                flash('Yes, hóspede adicionado com sucesso.', 'success')
                return redirect(url_for('checkins.checkin_details', checkin_id=checkin_id))
            except IntegrityError:
                flash('Oops, hóspede já foi cadastrado.', 'warning')
        else:
            flash('Oops, não podes adicionar hóspedes num check-in inactivo.', 'danger')
    return render_template('checkins/details.html', checkin=checkin, form=form)


@checkins.route('/<int:checkin_id>/remove_guest', methods=['POST'])
@login_required
@allowed_profile(['manager', 'admin'])
def checkin_guest_remove(checkin_id: int):
    checkin_guest = get(CheckInGuest, request.form['checkin_guest_id'])
    delete(checkin_guest)
    flash('Yes, {} removido com sucesso.'.format(
        checkin_guest.guest.name), 'success')
    return redirect(url_for('checkins.checkin_details', checkin_id=checkin_id))
