from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_required
from playhouse.flask_utils import object_list

from models import Guest
from dao import get_all, create, get, update
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
    form = GuestForm()
    if form.validate_on_submit():
        try:
            data = get_formdata(form)
            validate_guest(data)
            create(Guest, **data)
            flash('Yes, hóspede cadastrado com sucesso.', 'success')
            return redirect(url_for('guests.guest_index'))
        except AttributeError as e:
            flash(str(e), 'warning')
    return render_template('guests/new.html', form=form)


@guests.route('/<int:guest_id>/edit', methods=['GET', 'POST'])
@login_required
@allowed_profile(['receptionist', 'manager', 'admin'])
def guest_edit(guest_id: int):
    form = GuestForm(obj=get(Guest, guest_id))
    if form.validate_on_submit():
        try:
            data = get_formdata(form)
            validate_guest(data)
            update(Guest, guest_id, **data)
            flash('Yes, hóspede alterado com sucesso.', 'success')
            return redirect(url_for('guests.guest_index'))
        except AttributeError as e:
            flash(str(e), 'warning')
    return render_template('guests/edit.html', form=form)
