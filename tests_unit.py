from datetime import date, timedelta, datetime
from unittest import TestCase, main

from models import Reservation, CheckIn, Guest, Company
from utils.validators import (
    validate_check_in_creation, validate_guest, validate_reservation, validate_company)


class TestReservation(TestCase):
    def test_valid_reservation(self):
        today = datetime.now().date()
        reservation = Reservation(
            check_in_time=today + timedelta(days=1), check_out_time=today + timedelta(days=15))
        validate_reservation(reservation)

    def test_invalid_reservation_1(self):
        today = datetime.now().date()
        reservation = Reservation(
            check_in_time=today - timedelta(days=1), check_out_time=today + timedelta(days=15))
        with self.assertRaises(AttributeError):
            validate_reservation(reservation)

    def test_invalid_reservation_2(self):
        today = datetime.now().date()
        reservation = Reservation(
            check_in_time=today + timedelta(days=1), check_out_time=today - timedelta(days=15))
        with self.assertRaises(AttributeError):
            validate_reservation(reservation)


class TestCheckIn(TestCase):
    def test_invalid_check_in(self):
        checkin = CheckIn(check_out_time=date(2020, 9, 5))
        with self.assertRaises(AttributeError):
            validate_check_in_creation(checkin)


class TestGuest(TestCase):
    def test_invalid_guest(self):
        guest = Guest(cellphone='+2588915652')
        with self.assertRaises(AttributeError):
            validate_guest(guest)

    def test_valid_guest(self):
        guest = Guest(cellphone='+258840256000')
        validate_guest(guest)


class TestCompany(TestCase):
    def test_invalid_company(self):
        company = Company(telephone='+258840000000',
                          cellphone='+2588915652', fax='+2588915652', nuit='100000008')
        with self.assertRaises(AttributeError):
            validate_company(company)

    def test_valid_company(self):
        company = Company(telephone='+258840000000',
                          cellphone='+258840000000', fax='+258840000000', nuit='100000008')
        validate_company(company)


if __name__ == '__main__':
    main()
