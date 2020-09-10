from datetime import date
from unittest import TestCase, main
from utils.validators import (validate_check_in, validate_guest,
                              validate_reservation, validate_check_in)


class TestValidators(TestCase):
    def test_invalid_check_in(self):
        with self.assertRaises(AttributeError):
            validate_check_in(dict(check_out_time=date(2020, 9, 5)))

    def test_invalid_reservation(self):
        with self.assertRaises(AttributeError):
            validate_reservation(dict(check_out_time=date(2020, 8, 4)))

    def test_invalid_guest(self):
        with self.assertRaises(AttributeError):
            validate_guest(dict(cellphone='+2588915652'))

    def test_valid_guest(self):
        validate_guest(dict(cellphone='+258840256000'))

    def test_invalid_company(self):
        with self.assertRaises(AttributeError):
            validate_guest(dict(telephone='+258840000000',
                                cellphone='+2588915652', fax='+2588915652', nuit='100000008'))

    def test_valid_company(self):
        validate_guest(dict(telephone='+258840000000',
                            cellphone='+258840000000', fax='+258840000000', nuit='100000008'))


if __name__ == '__main__':
    main()
