# Unittest for class: MobileNumber

import unittest
from mock import patch
from challenge_backend.MobileNumber import MobileNumber, NonCorrectableError, CorrectableError


class MobileNumberTestCase(unittest.TestCase):
    @patch('challenge_backend.MobileNumber.MobileNumber.confirm_number')
    def test_confirm_number_is_called(self, confirm_number_mock):
        """Testing that method confirm_number is called by constructor"""
        MobileNumber('ID', '27345678901')
        assert confirm_number_mock.call_count == 1

    def test_confirm_number_set_return_true(self):
        """Testing that method confirm_number returns True when number is correct"""
        record = MobileNumber('ID', '27345678901')
        self.assertEqual(record.confirm_number(), True)

    def test_confirm_number_set_status_accepted(self):
        """Testing that method confirm_number modifies the instance "status" attribute when number is correct"""
        record = MobileNumber('ID', '27345678901')
        self.assertEqual(record.status, 'accepted')

    def test_confirm_number_not_correctable_numbers(self):
        """Testing that method confirm_number raises the NonCorrectableError error"""
        numbers = '273456789012', '123456789012', '27345678', '12345678', '27345abc901', '12345678', '1234567890', \
                  '12345678901 '
        for n in numbers:
            with self.subTest(msg=n):
                record = MobileNumber('ID', n)
                self.assertRaises(NonCorrectableError, record.confirm_number)

    def test_confirm_number_correctable_numbers(self):
        """Testing that method confirm_number raises the CorrectableError error"""
        numbers = '123456789', '7234567890'
        for n in numbers:
            with self.subTest(msg=n):
                record = MobileNumber('ID', n)
                self.assertRaises(CorrectableError, record.confirm_number)

    @patch('challenge_backend.MobileNumber.MobileNumber.catch_correctable_error')
    def test_catch_correctable_error_is_called(self, catch_correctable_error_mock):
        """Testing that method catch_correctable_error is called"""
        MobileNumber(None, '7345678901')
        assert catch_correctable_error_mock.call_count == 1

    def test_catch_correctable_error_set_status(self):
        """Testing that the catch_correctable_error method set instance attribute "status" into "corrected"""
        record = MobileNumber(None, '27345678901')
        assert record.status != 'corrected'
        record.catch_correctable_error()
        self.assertEqual(record.status, 'corrected')

    def test_catch_correctable_error_set_annotation(self):
        """Testing that the catch_correctable_error method set instance attribute "annotation" into "Correction:
        missing 27 prefix"""
        record = MobileNumber(None, '27345678901')
        assert record.annotation != 'Correction: missing 27 prefix'
        record.catch_correctable_error()
        self.assertEqual(record.annotation, 'Correction: missing 27 prefix')

    @patch('challenge_backend.MobileNumber.MobileNumber.catch_non_correctable_error')
    def test_catch_correctable_error_is_called(self, catch_non_correctable_error_mock):
        """Testing that method catch_non_correctable_error is called"""
        MobileNumber(None, '45678901')
        assert catch_non_correctable_error_mock.call_count == 1

    def test_catch_non_correctable_error_set_status(self):
        """Testing that the catch_non_correctable_error method set instance attribute "rejected" into "corrected"""
        record = MobileNumber(None, '27345678901')
        assert record.status != 'rejected'
        record.catch_non_correctable_error()
        self.assertEqual(record.status, 'rejected')

    def test_number_evaluation_message(self):
        number_message = {
            '27345678901': 'The number 27345678901 is correct.',
            '7234567890': f'The number 7234567890 is not correct.\n'
                          f'However the error is most likely a missing prefix 27.\n'
                          f'The proposed corrected number is 27234567890.',
            '234567890': f'The number 234567890 is not correct.\n'
                         f'However the error is most likely a missing prefix 27.\n'
                         f'The proposed corrected number is 27234567890.',
            '273456789012': 'The number 273456789012 is not correct and cannot be corrected.\n'
                            f'Rejection: the number does not contain 11 digits.',
            '2734567890': 'The number 2734567890 is not correct and cannot be corrected.\n'
                          f'Rejection: the number does not contain 11 digits.',
            '12345678901': 'The number 12345678901 is not correct and cannot be corrected.\n'
                           f'Rejection: the number prefix is not 27.',
            '1234': 'The number 1234 is not correct and cannot be corrected.\n'
                    f'Rejection: the number does not contain 11 digits; the number prefix is not 27.',
            '123456789012': 'The number 123456789012 is not correct and cannot be corrected.\n'
                            f'Rejection: the number does not contain 11 digits; the number prefix is not 27.',
            '27123456789a1': 'The number 27123456789a1 is not correct and cannot be corrected.\n'
                             f'Rejection: the entered string contains non numeric character.',
            '2734567890a12': 'The number 2734567890a12 is not correct and cannot be corrected.\n'
                             f'Rejection: the entered string contains non numeric character.',
            '1734567890a1': 'The number 1734567890a1 is not correct and cannot be corrected.\n'
                            f'Rejection: the entered string contains non numeric character.',
        }
        for number, message in number_message.items():
            with self.subTest(msg=number):
                record = MobileNumber('ID', number)
                self.assertEqual(record.number_evaluation_message, message)


if __name__ == '__main__':
    unittest.main()
