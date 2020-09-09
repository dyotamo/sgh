from datetime import datetime
from os import environ

from playhouse.db_url import connect
from playhouse.signals import Model, pre_save
from flask_login import UserMixin, current_user
from werkzeug.security import generate_password_hash as gph
from peewee import (SqliteDatabase, PostgresqlDatabase, CharField, DateTimeField,
                    ForeignKeyField, IntegerField, FloatField, BooleanField, CompositeKey)

from utils.constants import (PROFILES, GENDERS, CATEGORIES,
                             ROOM_STATUSES, ID_TYPES, MARITAL_STATUSES)

db = connect(environ.get('DATABASE_URL') or 'sqlite:///dev.db')


class BaseModel(Model):
    class Meta:
        database = db


class User(BaseModel, UserMixin):
    name = CharField(max_length=255)
    email = CharField(max_length=255, unique=True)
    profile = CharField(max_length=50, choices=PROFILES)
    password = CharField(max_length=255, default=gph(
        'passwd'))  # TODO remove it later

    created_at = DateTimeField(default=datetime.now())
    updated_at = DateTimeField(null=True)
    created_by = ForeignKeyField(
        'self', column_name='created_by', null=True, backref='created')
    updated_by = ForeignKeyField(
        'self',  column_name='updated_by', null=True, backref='updated')

    def get_profile_label(self):
        return dict(PROFILES)[self.profile]


class Mutable(BaseModel):
    created_at = DateTimeField(default=datetime.now())
    updated_at = DateTimeField(null=True)
    created_by = ForeignKeyField(
        User, column_name='created_by', null=True, backref='created')
    updated_by = ForeignKeyField(
        User,  column_name='updated_by', null=True, backref='updated')


class Company(Mutable):
    name = CharField(max_length=255)
    nuit = CharField(max_length=9)
    activity_branch = CharField(max_length=255)
    address = CharField(max_length=255)
    telephone = CharField(max_length=50)
    fax = CharField(max_length=50)
    cellphone = CharField(max_length=50)
    email = CharField(max_length=255)


class Guest(Mutable):
    name = CharField(max_length=255)
    id_type = CharField(max_length=10, choices=ID_TYPES)
    id_number = CharField(max_length=50)
    address = CharField(max_length=255)
    age = IntegerField()
    cellphone = CharField(max_length=50)
    father_name = CharField(max_length=255)
    mother_name = CharField(max_length=255)
    marital_status = CharField(max_length=20)
    nationality = CharField(max_length=255)
    company = ForeignKeyField(Company, null=True, backref='guests')
    gender = CharField(max_length=10, choices=GENDERS)

    def get_company(self):
        return self.company.name

    def get_id_type_label(self):
        return dict(ID_TYPES)[self.id_type]

    def get_marital_status_label(self):
        return dict(MARITAL_STATUSES)[self.marital_status]

    def get_gender_label(self):
        return dict(GENDERS)[self.gender]


class RoomType(Mutable):
    name = CharField(max_length=255, unique=True)


class Room(Mutable):
    number = IntegerField(unique=True)
    category = ForeignKeyField(RoomType, backref='rooms')
    status = CharField(max_length=50, choices=ROOM_STATUSES)
    daily_amount = FloatField()

    def get_category_label(self):
        return dict(CATEGORIES)[self.category]

    def get_status_label(self):
        return dict(ROOM_STATUSES)[self.status]


class Reservation(Mutable):
    check_in_time = DateTimeField()
    check_out_time = DateTimeField()
    adult_number = IntegerField()
    children_number = IntegerField()
    company = ForeignKeyField(Company, null=True, backref='reservations')
    is_active = BooleanField(default=True)


class CheckIn(Mutable):
    check_in_time = DateTimeField(default=datetime.now())
    check_out_time = DateTimeField()
    room = ForeignKeyField(Room, backref='checkins')
    is_active = BooleanField(default=True)


class CheckInGuest(BaseModel):
    guest = ForeignKeyField(Guest, backref='checkinguests')
    check_in = ForeignKeyField(CheckIn, backref='checkinguests')

    class Meta:
        primary_key = CompositeKey('guest', 'check_in')


class Expense(Mutable):
    category = CharField(max_length=50, choices=CATEGORIES)
    description = CharField(max_length=255)
    quantity = IntegerField()
    amount = FloatField()
    check_in = ForeignKeyField(CheckIn, backref='expenses')


class CheckOut(Mutable):
    out_date = DateTimeField()
    expenses_total = FloatField()
    payment_type = CharField(max_length=50)
    dailt_total = IntegerField()
    check_in = ForeignKeyField(CheckIn, backref='checkout')
    is_active = BooleanField(default=True)


class Invoice(Mutable):
    is_active = BooleanField(default=True)
    is_duplicate = BooleanField(default=True)


class Receipt(Mutable):
    is_active = BooleanField(default=True)
    is_duplicate = BooleanField(default=True)


# @pre_save(sender=Mutable)
def on_save_handler(model_class, instance, created):
    if created:
        instance.created_by = current_user.id
    else:
        instance.updated_by = current_user.id
        instance.updated_at = datetime.now()


if __name__ == "__main__":
    db.create_tables([User, Guest, Company, RoomType, Room, Expense,
                      Invoice, Receipt, CheckIn, CheckInGuest, CheckOut, Reservation])

    User.create(name='Dássone Yotamo', email='dyotamo@gmail.com',
                profile='admin', password=gph('passwd'))
