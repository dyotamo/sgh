from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_required
from peewee import IntegrityError
from playhouse.flask_utils import object_list

from models import Room
from dao import get_all, create, get, update
from forms.room import RoomForm
from utils.security import allowed_profile
from utils.extra import get_formdata


rooms = Blueprint('rooms', __name__, url_prefix='/rooms')


@rooms.route('/', methods=['GET'])
@login_required
@allowed_profile(['receptionist', 'manager', 'admin'])
def room_index():
    return object_list('rooms/index.html', query=get_all(Room),
                       context_variable='rooms', paginate_by=7, check_bounds=False)


@rooms.route('/new', methods=['GET', 'POST'])
@login_required
@allowed_profile(['receptionist', 'manager', 'admin'])
def room_new():
    form = RoomForm()
    if form.validate_on_submit():
        try:
            data = get_formdata(form)
            create(Room, **data)  # TODO validate if room number already exists
            flash('Yes, quarto cadastrado com sucesso.', 'success')
            return redirect(url_for('rooms.room_index'))
        except IntegrityError:
            flash('Oops, este número de quarto já está ocupado.', 'warning')
    return render_template('rooms/new.html', form=form)


@rooms.route('/<int:room_id>/edit', methods=['GET', 'POST'])
@login_required
@allowed_profile(['receptionist', 'manager', 'admin'])
def room_edit(room_id: int):
    form = RoomForm(obj=get(Room, room_id))
    if form.validate_on_submit():
        data = get_formdata(form)
        update(Room, room_id, **data)
        flash('Yes, quarto alterado com sucesso.', 'success')
        return redirect(url_for('rooms.room_index'))
    return render_template('rooms/edit.html', form=form)
