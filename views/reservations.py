from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import login_required
from playhouse.flask_utils import object_list

from models import Reservation
from dao import get_all, get
from forms.reservation import ReservationForm
from utils.security import allowed_profile
from utils.validators import validate_reservation


reservations = Blueprint('reservations', __name__, url_prefix='/reservations')


@reservations.route('/', methods=['GET'])
@login_required
@allowed_profile(['receptionist', 'manager', 'admin'])
def reservation_index():
    return object_list('reservations/index.html', query=get_all(Reservation),
                       context_variable='reservations', paginate_by=7,
                       check_bounds=False)


@reservations.route('/new', methods=['GET', 'POST'])
@login_required
@allowed_profile(['receptionist', 'manager', 'admin'])
def reservation_new():
    reservation = Reservation()
    if request.method == 'POST':
        form = ReservationForm(request.form, obj=reservation)
        if form.validate():
            try:
                form.populate_obj(reservation)
                validate_reservation(reservation)
                reservation.save()
                flash('Yes, reserva cadastrado com sucesso.', 'success')
                return redirect(url_for('reservations.reservation_index'))
            except AttributeError as e:
                flash(str(e), 'warning')
    else:
        form = ReservationForm(obj=reservation)
    return render_template('reservations/new.html', form=form)


@reservations.route('/<int:reservation_id>/edit', methods=['GET', 'POST'])
@login_required
@allowed_profile(['receptionist', 'manager', 'admin'])
def reservation_edit(reservation_id: int):
    reservation = get(Reservation, reservation_id)
    if request.method == 'POST':
        form = ReservationForm(request.form, obj=reservation)
        if form.validate():
            try:
                form.populate_obj(reservation)
                validate_reservation(reservation)
                reservation.save()
                flash('Yes, reserva alterada com sucesso.', 'success')
                return redirect(url_for('reservations.reservation_index'))
            except AttributeError as e:
                flash(str(e), 'warning')
    else:
        form = ReservationForm(obj=reservation)
    return render_template('reservations/edit.html', form=form)
