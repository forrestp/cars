import string
import unittest
from random import choice, randint

from graphql import GraphQLError

from cars.mutations.validations import validate_mutation


def randStr(chars=string.ascii_uppercase + string.digits, N=10):
    return ''.join(choice(chars) for _ in range(N))


class ValidateMutation_Test(unittest.TestCase):

    def test_max_value_success(self):
        max_value = randint(0, 100)
        validate_dict = {'dummy': {'max': max_value}}
        dummy_data = {
            'dummy': max_value
        }
        validate_mutation(validate_dict, dummy_data)

    def test_max_value_error(self):
        max_value = randint(0, 100)
        validate_dict = {'dummy': {'max': max_value}}
        dummy_data = {
            'dummy': max_value + 1
        }
        with self.assertRaises(GraphQLError):
            validate_mutation(validate_dict, dummy_data)

    def test_min_value_success(self):
        min_value = randint(0, 100)
        validate_dict = {
            'dummy': {'min': min_value}
        }
        dummy_data = {
            'dummy': min_value
        }
        validate_mutation(validate_dict, dummy_data)

    def test_min_value_error(self):
        min_value = randint(0, 100)
        validate_dict = {'dummy': {'min': min_value}}
        dummy_data = {
            'dummy': min_value - 1
        }
        with self.assertRaises(GraphQLError):
            validate_mutation(validate_dict, dummy_data)

    def test_max_length_success(self):
        max_length = randint(0, 100)
        validate_dict = {
            'dummy': {'max': max_length}
        }
        dummy_data = {
            'dummy': randStr(N=max_length)
        }
        validate_mutation(validate_dict, dummy_data)

    def test_max_length_error(self):
        max_length = randint(0, 100)
        validate_dict = {
            'dummy': {'max': max_length}
        }
        dummy_data = {
            'dummy': randStr(N=max_length + 1)
        }
        with self.assertRaises(GraphQLError):
            validate_mutation(validate_dict, dummy_data)

    def test_min_length_success(self):
        min_length = randint(0, 100)
        validate_dict = {
            'dummy': {'min': min_length}
        }
        dummy_data = {
            'dummy': randStr(N=min_length)
        }
        validate_mutation(validate_dict, dummy_data)

    def test_min_length_error(self):
        min_length = randint(0, 100)
        validate_dict = {
            'dummy': {'min': min_length}
        }
        dummy_data = {
            'dummy': randStr(N=min_length - 1)
        }
        with self.assertRaises(GraphQLError):
            validate_mutation(validate_dict, dummy_data)
