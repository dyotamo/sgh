from datetime import datetime
from os import environ

from playhouse.db_url import connect
from flask_login import UserMixin
from werkzeug.security import generate_password_hash as gph
from peewee import (Model, CharField, DateField, ForeignKeyField,
                    IntegerField, FloatField, BooleanField)

from utils.constants import (PROFILES, GENDERS, ROOM_CATEGORIES,
                             ROOM_STATUSES, ID_TYPES, MARITAL_STATUSES)

db = connect(environ.get('DATABASE_URL') or 'sqlite:///dev.db')


class BaseModel(Model):
    class Meta:
        database = db


class User(BaseModel, UserMixin):
    name = CharField(max_length=255)
    email = CharField(max_length=255, unique=True)
    profile = CharField(max_length=50, choices=PROFILES)
    password = CharField(max_length=255, default=gph('passwd'))

    def get_profile_label(self):
        return dict(PROFILES)[self.profile]

    def __str__(self):
        return self.email


class Company(BaseModel):
    name = CharField(max_length=255)
    nuit = CharField(max_length=9)
    activity_branch = CharField(max_length=255)
    address = CharField(max_length=255)
    telephone = CharField(max_length=50)
    fax = CharField(max_length=50)
    cellphone = CharField(max_length=50)
    email = CharField(max_length=255)

    def __str__(self):
        return self.name


class Guest(BaseModel):
    name = CharField(max_length=255)
    id_type = CharField(max_length=10, choices=ID_TYPES)
    id_number = CharField(max_length=50)
    address = CharField(max_length=255)
    age = IntegerField()
    cellphone = CharField(max_length=50)
    father_name = CharField(max_length=255, null=True)
    mother_name = CharField(max_length=255, null=True)
    marital_status = CharField(max_length=20, choices=MARITAL_STATUSES)
    nationality = CharField(max_length=255)
    company = ForeignKeyField(Company, backref='guests', null=True)
    gender = CharField(max_length=10, choices=GENDERS)

    def get_company(self):
        return self.company.name

    def get_id_type_label(self):
        return dict(ID_TYPES)[self.id_type]

    def get_marital_status_label(self):
        return dict(MARITAL_STATUSES)[self.marital_status]

    def get_gender_label(self):
        return dict(GENDERS)[self.gender]

    def __str__(self):
        return self.name


class RoomType(BaseModel):
    name = CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Room(BaseModel):
    number = IntegerField(unique=True)
    category = ForeignKeyField(RoomType, backref='rooms', null=True)
    status = CharField(max_length=50, choices=ROOM_STATUSES)
    daily_amount = FloatField()

    def get_category_label(self):
        return dict(ROOM_CATEGORIES)[self.category]

    def get_status_label(self):
        return dict(ROOM_STATUSES)[self.status]

    def __str__(self):
        return str(self.number)


class Reservation(BaseModel):
    check_in_time = DateField()
    check_out_time = DateField()
    adult_number = IntegerField()
    children_number = IntegerField()
    company = ForeignKeyField(Company, backref='reservations', null=True)

    def __str__(self):
        return str(self.__dict__['__data__'])


class CheckIn(BaseModel):
    check_in_time = DateField(default=datetime.now().date)
    check_out_time = DateField()
    room = ForeignKeyField(Room, backref='checkins', null=True)

    def __str__(self):
        return str(self.__dict__['__data__'])


class CheckInGuest(BaseModel):
    guest = ForeignKeyField(Guest, backref='checkinguests', null=True)
    check_in = ForeignKeyField(CheckIn, backref='checkinguests', null=True)

    class Meta:
        indexes = ((('guest', 'check_in'), True),)

    def __str__(self):
        return str(self.__dict__['__data__'])


class Expense(BaseModel):
    category = CharField(max_length=50, choices=ROOM_CATEGORIES)
    description = CharField(max_length=255)
    quantity = IntegerField()
    amount = FloatField()
    check_in = ForeignKeyField(CheckIn, backref='expenses')

    def __str__(self):
        return str(self.__dict__['__data__'])


class CheckOut(BaseModel):
    out_date = DateField()
    expenses_total = FloatField()
    payment_type = CharField(max_length=50)
    dailt_total = IntegerField()
    check_in = ForeignKeyField(CheckIn, backref='checkout')
    is_active = BooleanField(default=True)

    def __str__(self):
        return str(self.__dict__['__data__'])


class Invoice(BaseModel):
    is_active = BooleanField(default=True)
    is_duplicate = BooleanField(default=True)

    def __str__(self):
        return str(self.__dict__['__data__'])


class Receipt(BaseModel):
    is_active = BooleanField(default=True)
    is_duplicate = BooleanField(default=True)

    def __str__(self):
        return str(self.__dict__['__data__'])


if __name__ == "__main__":
    db.create_tables([User, Guest, Company, RoomType, Room,
                      CheckIn, CheckInGuest, Reservation])

    User.create(name='Dássone Yotamo', email='dyotamo@gmail.com',
                profile='admin', password=gph('passwd'))
