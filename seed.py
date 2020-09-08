from random import choice
from datetime import datetime

from peewee import fn
from faker import Faker

from models import User, Company, RoomType, Room
from utils.constants import PROFILES, ROOM_STATUSES

fake = Faker()


# Users
for _ in range(10):
    User.create(name=fake.name(), email=fake.email(),
                profile=choice(PROFILES)[0])

# Companies
for _ in range(25):
    Company.create(name=fake.company(), nuit='100000008',
                   activity_branch=fake.bs().title(), address=fake.address(),
                   telephone=fake.phone_number(), fax=fake.phone_number(), cellphone=fake.phone_number(),
                   email=fake.email(), created_by=1, created_at=datetime.now())

# Room types
RoomType.create(name='Solteiro', created_by=1, created_at=datetime.now())
RoomType.create(name='Casal', created_by=1, created_at=datetime.now())
RoomType.create(name='Familiar', created_by=1, created_at=datetime.now())
RoomType.create(name='Presidencial', created_by=1, created_at=datetime.now())


# Rooms
for number in range(50):
    Room.create(number=number, category=RoomType.select().order_by(
        fn.Random()).get(), status=choice(ROOM_STATUSES)[0], daily_amount=1500, created_by=1, created_at=datetime.now())

print('Done.')
