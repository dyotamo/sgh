from datetime import datetime

from werkzeug.security import generate_password_hash
from flask_login import UserMixin
from flask_login import current_user
from peewee import (SqliteDatabase, Model, CharField,
                    DateTimeField, ForeignKeyField, IntegerField, FloatField,)

db = SqliteDatabase('dev.db')


class BaseModel(Model):
    class Meta:
        database = db


class User(BaseModel, UserMixin):
    name = CharField(max_length=255)
    email = CharField(max_length=255, unique=True)
    profile = CharField(max_length=50,
                        choices=[('admin', 'Administrador'),
                                 ('receptionist', 'Recepcionista'),
                                 ('manager', 'Gerente')])
    password = CharField(max_length=255)


class Creatable(BaseModel):
    created_at = DateTimeField(default=datetime.now())
    updated_at = DateTimeField(null=True)
    created_by = ForeignKeyField(User, column_name='created_by', null=True)
    updated_by = ForeignKeyField(User,  column_name='updated_by', null=True)


class Company(Creatable):
    name = CharField(max_length=255)
    nuit = CharField(max_length=9)
    activity_branch = CharField(max_length=255)
    address = CharField(max_length=255)
    telephone = CharField(max_length=50)
    fax = CharField(max_length=50)
    cellphone = CharField(max_length=50)
    email = CharField(max_length=255)


class Guest(Creatable):
    name = CharField(max_length=255)
    id_number = CharField(max_length=50)
    address = CharField(max_length=255)
    age = IntegerField()
    cellphone = CharField(max_length=50, null=True)
    gender = CharField(max_length=10, choices=[('male', 'Masculino'),
                                               ('female', 'Female'),
                                               ('other', 'Outro')])
    father_name = CharField(max_length=255, null=True)
    mother_name = CharField(max_length=255, null=True)
    escolarity = CharField(max_length=50, null=True)
    marital_status = CharField(max_length=20)
    nationality = CharField(max_length=255)
    passport = CharField(max_length=20, null=True)
    company = ForeignKeyField(Company, null=True)


class Room(Creatable):
    CATEGORIES = [('single', 'Solteiro'), ('couple', 'Casal')]
    STATUSES = [('available', 'Disponível'), ('busy', 'Ocupado'),
                ('sweeping', 'Em arrumação'), ('closed', 'Encerrado')]

    number = IntegerField(unique=True)
    category = CharField(max_length=50, choices=CATEGORIES)
    status = CharField(max_length=50, choices=STATUSES)
    daily_amount = FloatField()

    def get_category_label(self):
        return dict(self.CATEGORIES)[self.category]

    def get_status_label(self):
        return dict(self.STATUSES)[self.status]


class Reservation(Creatable):
    check_in_time = DateTimeField()
    check_out_time = DateTimeField()
    adult_number = IntegerField()
    children_number = IntegerField()
    company_number = CharField(max_length=255)


class CheckIn(Creatable):
    in_date = DateTimeField()
    out_date = DateTimeField()
    room = ForeignKeyField(Room)


class CheckInGuest(BaseModel):
    guest = ForeignKeyField(Guest)
    check_in = ForeignKeyField(CheckIn)


class Expense(Creatable):
    category = CharField(max_length=50, choices=[])
    description = CharField(max_length=255)
    quantity = IntegerField()
    amount = FloatField()
    check_in = ForeignKeyField(CheckIn)


class CheckOut(Creatable):
    out_date = DateTimeField()
    expenses_total = FloatField()
    payment_type = CharField(max_length=50)
    dailt_total = IntegerField()
    check_in = ForeignKeyField(CheckIn)


class Invoice(Creatable):
    pass


class Receipt(Creatable):
    pass


if __name__ == "__main__":
    db.create_tables([User, Guest, Company, Room,
                      Invoice, Receipt, CheckIn, CheckOut])
    User.create(name='Dássone Yotamo', email='dyotamo@gmail.com',
                profile='manager', password=generate_password_hash('passwd'))
