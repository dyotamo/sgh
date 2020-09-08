from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import login_required
from peewee import IntegrityError

from models import Reservation
from dao import get_all, create, get, update
from forms.reservation import ReservationForm
from utils.security import allowed_profile
from utils.extra import get_formdata
from utils.validators import validate_reservation
from services import toogle_activation


reservations = Blueprint('reservations', __name__, url_prefix='/reservations')


@reservations.route('/', methods=['GET'])
@login_required
@allowed_profile(['receptionist', 'manager', 'admin'])
def reservation_index():
    return render_template('reservations/index.html', reservations=get_all(Reservation))


@reservations.route('/new', methods=['GET', 'POST'])
@login_required
@allowed_profile(['receptionist', 'manager', 'admin'])
def reservation_new():
    form = ReservationForm()
    if form.validate_on_submit():
        try:
            data = get_formdata(form)
            validate_reservation(data)
            create(Reservation, **data)
            flash('Yes, reserva cadastrado com sucesso.', 'success')
            return redirect(url_for('reservations.reservation_index'))
        except AttributeError as e:
            flash(str(e), 'warning')
    return render_template('reservations/new.html', form=form)


@reservations.route('/<int:reservation_id>/edit', methods=['GET', 'POST'])
@login_required
@allowed_profile(['receptionist', 'manager', 'admin'])
def reservation_edit(reservation_id: int):
    form = ReservationForm(obj=get(Reservation, reservation_id))
    if form.validate_on_submit():
        try:
            data = get_formdata(form)
            validate_reservation(data)
            update(Reservation, reservation_id, **data)
            flash('Yes, reserva alterado com sucesso.', 'success')
            return redirect(url_for('reservations.reservation_index'))
        except AttributeError as e:
            flash(str(e), 'warning')
    return render_template('reservations/edit.html', form=form)


@reservations.route('/<int:reservation_id>/deactivate', methods=['GET', 'POST'])
@login_required
@allowed_profile(['manager', 'admin'])
def reservation_deactivate(reservation_id: int):
    reservation = get(Reservation, reservation_id)
    if request.method == 'POST':
        toogle_activation(reservation)
        flash('Yes, reserva {} com sucesso.'.format(
            'reactivada' if reservation.is_active else 'desactivada'), 'success')
        return redirect(url_for('reservations.reservation_index'))
    return render_template('reservations/deactivate.html', reservation=reservation)
