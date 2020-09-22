from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import login_required
from playhouse.flask_utils import object_list

from models import Guest
from dao import get_all, get
from forms.guest import GuestForm
from utils.security import allowed_profile
from utils.extra import get_formdata
from utils.validators import validate_guest


guests = Blueprint('guests', __name__, url_prefix='/guests')


@guests.route('/', methods=['GET'])
@login_required
@allowed_profile(['receptionist', 'manager', 'admin'])
def guest_index():
    return object_list('guests/index.html', query=get_all(Guest),
                       context_variable='guests', paginate_by=7, check_bounds=False)


@guests.route('/<int:guest_id>', methods=['GET'])
@login_required
@allowed_profile(['receptionist', 'manager', 'admin'])
def guest_details(guest_id: int):
    return render_template('guests/details.html', guest=get(Guest, guest_id))


@guests.route('/new', methods=['GET', 'POST'])
@login_required
@allowed_profile(['receptionist', 'manager', 'admin'])
def guest_new():
    guest = Guest()
    if request.method == 'POST':
        form = GuestForm(request.form, obj=guest)
        if form.validate():
            try:
                form.populate_obj(guest)
                validate_guest(guest)
                guest.save()
                flash('Yes, hóspede cadastrado com sucesso.', 'success')
                return redirect(url_for('guests.guest_index'))
            except AttributeError as e:
                flash(str(e), 'warning')
    else:
        form = GuestForm(obj=guest)
    return render_template('guests/new.html', form=form)


@guests.route('/<int:guest_id>/edit', methods=['GET', 'POST'])
@login_required
@allowed_profile(['receptionist', 'manager', 'admin'])
def guest_edit(guest_id: int):
    guest = get(Guest, guest_id)
    if request.method == 'POST':
        form = GuestForm(request.form, obj=guest)
        if form.validate():
            try:
                form.populate_obj(guest)
                validate_guest(guest)
                guest.save()
                flash('Yes, hóspede alterado com sucesso.', 'success')
                return redirect(url_for('guests.guest_index'))
            except AttributeError as e:
                flash(str(e), 'warning')
    else:
        form = GuestForm(obj=guest)
    return render_template('guests/edit.html', form=form)
