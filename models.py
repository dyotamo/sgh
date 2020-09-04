from datetime import datetime

from werkzeug.security import generate_password_hash as gph
from flask_login import UserMixin
from peewee import (SqliteDatabase, Model, CharField, DateTimeField,
                    ForeignKeyField, IntegerField, FloatField, BooleanField)


from utils.constants import (PROFILES, GENDERS, CATEGORIES,
                             ROOM_STATUSES, ID_TYPES, MARITAL_STATUSES)

db = SqliteDatabase('dev.db')


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
    created_by = ForeignKeyField('self', column_name='created_by', null=True)
    updated_by = ForeignKeyField('self',  column_name='updated_by', null=True)

    def get_profile_label(self):
        return dict(PROFILES)[self.profile]


class Mutable(BaseModel):
    created_at = DateTimeField(default=datetime.now())
    updated_at = DateTimeField(null=True)
    created_by = ForeignKeyField(User, column_name='created_by', null=True)
    updated_by = ForeignKeyField(User,  column_name='updated_by', null=True)


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
    company = ForeignKeyField(Company, null=True)
    gender = CharField(max_length=10, choices=GENDERS)

    def get_company(self):
        try:
            return self.company.name
        except Company.DoesNotExist:
            return 'Nenhuma'

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
    category = ForeignKeyField(RoomType)
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
    company = ForeignKeyField(Company, null=True)
    is_active = BooleanField(default=True)


class CheckIn(Mutable):
    in_date = DateTimeField()
    out_date = DateTimeField()
    room = ForeignKeyField(Room)
    is_active = BooleanField(default=True)


class CheckInGuest(BaseModel):
    guest = ForeignKeyField(Guest)
    check_in = ForeignKeyField(CheckIn)


class Expense(Mutable):
    category = CharField(max_length=50, choices=CATEGORIES)
    description = CharField(max_length=255)
    quantity = IntegerField()
    amount = FloatField()
    check_in = ForeignKeyField(CheckIn)


class CheckOut(Mutable):
    out_date = DateTimeField()
    expenses_total = FloatField()
    payment_type = CharField(max_length=50)
    dailt_total = IntegerField()
    check_in = ForeignKeyField(CheckIn)
    is_active = BooleanField(default=True)


class Invoice(Mutable):
    is_active = BooleanField(default=True)
    is_duplicate = BooleanField(default=True)


class Receipt(Mutable):
    is_active = BooleanField(default=True)
    is_duplicate = BooleanField(default=True)


if __name__ == "__main__":
    db.create_tables([User, Guest, Company, RoomType, Room,
                      Invoice, Receipt, CheckIn, CheckOut, Reservation])

    User.create(name='Dássone Yotamo', email='dyotamo@gmail.com',
                profile='admin', password=gph('passwd'))
