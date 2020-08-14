# The MobileNumber class is a model representing a single phone number.

import json
import re


class CorrectableError(ValueError):
    pass


class NonCorrectableError(ValueError):
    pass


class MobileNumber:
    def __init__(self, id_, string_number):
        self.id_ = id_
        self.number = string_number
        self.status = None
        self.suggested_correction = None
        self.annotation = None
        try:
            if self.confirm_number():
                self.status = 'accepted'
        except CorrectableError:
            self.catch_correctable_error()
        except NonCorrectableError:
            self.catch_non_correctable_error()

    def confirm_number(self):
        """Return True if number is correct, else raise exception"""
        if re.match(r'^27\d{9}$', self.number):
            return True
        if re.match(r'^7?\d{9}$', self.number):
            raise CorrectableError
        raise NonCorrectableError

    def catch_correctable_error(self):
        missing_digits = '2' if len(self.number) == 10 else '27'
        self.suggested_correction = missing_digits + self.number
        self.status = 'corrected'
        self.annotation = 'Correction: missing 27 prefix'

    def catch_non_correctable_error(self):
        self.status = 'rejected'
        errors = {
            'length': [r'^\d{12,}$|^\d{,10}$', 'the number does not contain 11 digits'],
            'prefix': [r'^\d(?<!2)\d*$', 'the number prefix is not 27']
        }
        message = []
        for error, pattern_message in errors.items():
            if re.match(pattern_message[0], self.number):
                message.append(pattern_message[1])
        # formatting annotation for human readers
        self.annotation = 'Rejection: '
        if message:
            self.annotation += '; '.join(message) + '.'
        else:
            self.annotation += 'the entered string contains non numeric character.'

    @property
    def number_evaluation_message(self):
        messages = {
            'accepted': f'The number {self.number} is correct.',
            'corrected': f'The number {self.number} is not correct.\n'
                         f'However the error is most likely a missing prefix 27.\n'
                         f'The proposed corrected number is {self.suggested_correction}.',
            'rejected': f'The number {self.number} is not correct and cannot be corrected.\n'
                        f'{self.annotation}'
        }
        return messages[self.status]

    def __str__(self):
        return json.dumps(self.__dict__)
