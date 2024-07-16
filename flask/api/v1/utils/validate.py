from .error import InvalidAPIUsage


def validate_data(schema, data):
    error = schema.validate(data)
    if error:
        raise InvalidAPIUsage(error)
