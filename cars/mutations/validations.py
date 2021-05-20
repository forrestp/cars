from graphene.utils.str_converters import to_camel_case
from graphql import GraphQLError


def validate_mutation(validate_dict, data):
    for key in validate_dict.keys():
        if key in data.keys():
            validator = validate_dict[key]
            camel_case_key = to_camel_case(key)
            if type(data[key]) == str:

                max_length = validator.get('max')
                max_length_invalid = max_length is not None and len(data[key]) > max_length

                min_length = validator.get('min')
                min_length_invalid = min_length is not None and len(data[key]) < min_length

                if max_length_invalid or min_length_invalid:
                    raise GraphQLError(f'Value in field {camel_case_key} outside constraints')
            else:
                max_value = validator.get('max')
                max_value_invalid = max_value is not None and data[key] > validator['max']

                min_value = validator.get('min')
                min_value_invalid = min_value is not None and data[key] < validator['min']

                if max_value_invalid or min_value_invalid:
                    raise GraphQLError(f'Value in field {camel_case_key} outside constraints')
