from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import login_required
from peewee import IntegrityError
from playhouse.flask_utils import object_list

from models import Room
from dao import get_all, get
from forms.room import RoomForm
from utils.security import allowed_profile
from utils.validators import validate_room


rooms = Blueprint('rooms', __name__, url_prefix='/rooms')


@rooms.route('/', methods=['GET'])
@login_required
@allowed_profile(['receptionist', 'manager', 'admin'])
def room_index():
    return object_list('rooms/index.html', query=get_all(Room),
                       context_variable='rooms', paginate_by=7,
                       check_bounds=False)


@rooms.route('/new', methods=['GET', 'POST'])
@login_required
@allowed_profile(['receptionist', 'manager', 'admin'])
def room_new():
    room = Room()
    if request.method == 'POST':
        form = RoomForm(request.form, obj=room)
        if form.validate():
            try:
                form.populate_obj(room)
                validate_room(room)
                room.save()
                flash('Yes, quarto cadastrado com sucesso.', 'success')
                return redirect(url_for('rooms.room_index'))
            except IntegrityError:
                flash('Oops, este quarto já foi cadastrado.', 'warning')
            except AttributeError as e:
                flash(str(e), 'warning')
    else:
        form = RoomForm(obj=room)
    return render_template('rooms/new.html', form=form)


@rooms.route('/<int:room_id>/edit', methods=['GET', 'POST'])
@login_required
@allowed_profile(['receptionist', 'manager', 'admin'])
def room_edit(room_id: int):
    room = get(Room, room_id)
    if request.method == 'POST':
        form = RoomForm(request.form, obj=room)
        if form.validate():
            try:
                form.populate_obj(room)
                validate_room(room)
                room.save()
                flash('Yes, quarto alterado com sucesso.', 'success')
                return redirect(url_for('rooms.room_index'))
            except AttributeError as e:
                flash(str(e), 'warning')
    else:
        form = RoomForm(obj=room)
    return render_template('rooms/edit.html', form=form)
