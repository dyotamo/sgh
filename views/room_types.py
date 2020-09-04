from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_required
from peewee import IntegrityError

from models import RoomType
from dao import get_all, create, get, update
from forms.room_type import RoomTypeForm
from utils.security import allowed_profile
from utils.extra import get_formdata


room_types = Blueprint('room_types', __name__, url_prefix='/room_types')


@room_types.route('/', methods=['GET'])
@login_required
@allowed_profile(['admin'])
def room_type_index():
    return render_template('room_types/index.html', room_types=get_all(RoomType))


@room_types.route('/new', methods=['GET', 'POST'])
@login_required
@allowed_profile(['admin'])
def room_type_new():
    form = RoomTypeForm()
    if form.validate_on_submit():
        try:
            data = get_formdata(form)
            create(RoomType, **data)
            flash('Yes, tipo de quarto cadastrado com sucesso.', 'success')
            return redirect(url_for('room_types.room_type_index'))
        except IntegrityError:
            flash('Oops, este tipo de quarto já existe.', 'warning')
    return render_template('room_types/new.html', form=form)


@room_types.route('/<int:room_type_id>/edit', methods=['GET', 'POST'])
@login_required
@allowed_profile(['admin'])
def room_type_edit(room_type_id: int):
    form = RoomTypeForm(obj=get(RoomType, room_type_id))
    if form.validate_on_submit():
        try:
            data = get_formdata(form)
            update(RoomType, room_type_id, **data)
            flash('Yes, tipo de quarto alterado com sucesso.', 'success')
            return redirect(url_for('room_types.room_type_index'))
        except IntegrityError:
            flash('Oops, este tipo de quarto já existe.', 'warning')
    return render_template('room_types/edit.html', form=form)
