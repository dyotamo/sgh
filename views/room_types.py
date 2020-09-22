from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import login_required
from peewee import IntegrityError

from models import RoomType
from dao import get_all, get
from forms.room_type import RoomTypeForm
from utils.security import allowed_profile


room_types = Blueprint('room_types', __name__, url_prefix='/room_types')


@room_types.route('/', methods=['GET'])
@login_required
@allowed_profile(['admin'])
def room_type_index():
    return render_template('room_types/index.html',
                           room_types=get_all(RoomType))


@room_types.route('/new', methods=['GET', 'POST'])
@login_required
@allowed_profile(['admin'])
def room_type_new():
    room_type = RoomType()
    if request.method == 'POST':
        form = RoomTypeForm(request.form, obj=room_type)
        if form.validate():
            try:
                form.populate_obj(room_type)
                room_type.save()
                flash('Yes, tipo de quarto cadastrado com sucesso.', 'success')
                return redirect(url_for('room_types.room_type_index'))
            except IntegrityError:
                flash('Oops, este tipo de quarto já existe.', 'warning')
    else:
        form = RoomTypeForm(obj=room_type)
    return render_template('room_types/new.html', form=form)


@room_types.route('/<int:room_type_id>/edit', methods=['GET', 'POST'])
@login_required
@allowed_profile(['admin'])
def room_type_edit(room_type_id: int):
    room_type = get(RoomType, room_type_id)
    if request.method == 'POST':
        form = RoomTypeForm(request.form, obj=room_type)
        if form.validate():
            try:
                form.populate_obj(room_type)
                room_type.save()
                flash('Yes, tipo de quarto alterado com sucesso.', 'success')
                return redirect(url_for('room_types.room_type_index'))
            except IntegrityError:
                flash('Oops, este tipo de quarto já existe.', 'warning')
    else:
        form = RoomTypeForm(obj=room_type)
    return render_template('room_types/edit.html', form=form)
