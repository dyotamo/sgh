from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_required

from models import Room
from dao import get_all, create, get, update, get_where
from forms.room import RoomForm
from utils.security import allowed_profile
from utils.extra import get_formdata


rooms = Blueprint('rooms', __name__, url_prefix='/rooms')


@rooms.route('/', methods=['GET'])
@login_required
@allowed_profile(['receptionist', 'manager'])
def room_index():
    return render_template('rooms/index.html', rooms=get_all(Room))


@rooms.route('/new', methods=['GET', 'POST'])
@login_required
@allowed_profile(['receptionist', 'manager'])
def room_new():
    form = RoomForm()

    if form.validate_on_submit():
        number = form.number.data

        if get_where(Room, number=number):
            flash('Quarto com o número {} já existe.'.format(number), 'danger')
        else:
            data = get_formdata(form)
            validate_room(data)
            create(Room, **data)

            flash('Quarto cadastrado.', 'success')
            return redirect(url_for('rooms.room_index'))
    return render_template('rooms/new.html', form=form)


@rooms.route('/<int:room_id>/edit', methods=['GET', 'POST'])
@login_required
@allowed_profile(['receptionist', 'manager'])
def room_edit(room_id):
    form = RoomForm(obj=get(Room, room_id))

    if form.validate_on_submit():
        data = get_formdata(form)
        update(Room, room_id, **data)

        flash('Quarto alterado.', 'success')
        return redirect(url_for('rooms.room_index'))

    return render_template('rooms/edit.html', form=form)
