from random import choice

from faker import Faker

from models import User, Company, RoomType, Room
from dao import create, get_random, get
from utils.constants import PROFILES, ROOM_STATUSES


fake = Faker()


def _create_users(size: int):
    for _ in range(size):
        create(User, name=fake.name(), email=fake.email(),
               profile=choice(PROFILES)[0])


def _create_companies(size: int):
    for _ in range(size):
        create(Company, name=fake.company(), nuit='100000008',
               activity_branch=fake.bs().title(), address=fake.address(),
               telephone=fake.phone_number(), fax=fake.phone_number(),
               cellphone=fake.phone_number(), email=fake.email())


def _create_room_types():
    create(RoomType, name='Solteiro')
    create(RoomType, name='Casal')
    create(RoomType, name='Familiar')
    create(RoomType, name='Presidencial')


def _create_rooms(size: int):
    for number in range(size):
        Room.create(number=number, category=get_random(RoomType),
                    status=choice(ROOM_STATUSES)[0], daily_amount=1500)


if __name__ == '__main__':
    _create_users(5)
    _create_companies(5)
    _create_room_types()
    _create_rooms(10)
