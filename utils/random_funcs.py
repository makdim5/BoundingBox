from random import randrange

MIN_VALUE, MAX_VALUE = 0, 255


def get_random_number(min_value=MIN_VALUE, max_value=MAX_VALUE):
    return randrange(min_value, max_value)


def get_random_color():
    return (get_random_number(),
            get_random_number(),
            get_random_number())
