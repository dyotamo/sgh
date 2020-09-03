from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_required

from models import Guest
from dao import get_all, create, get, update
from forms.guest import GuestForm
from utils.security import allowed_profile
from utils.extra import get_formdata
from utils.validators import validate_guest


guests = Blueprint('guests', __name__, url_prefix='/guests')


@guests.route('/', methods=['GET'])
@login_required
@allowed_profile(['admin'])
def guest_index():
    return render_template('guests/index.html', guests=get_all(Guest))


@guests.route('/new', methods=['GET', 'POST'])
@login_required
@allowed_profile(['admin'])
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
@allowed_profile(['admin'])
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
