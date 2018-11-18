"""
Some
module
level
docstring
"""

"some single line text"

__MODULE_PRIVATE = 999


def __foo():  # some comment here
    __inside_private = 123
    return __inside_private


class MyClass:
    __class_private_attribute = 555
    """
    Some
    Text
    """

    def __init__(self):
        self.__private_method_called = False

    def __private_method(self):
        self.__private_method_called = True
        self.__instance_private_attribute = 789

    def public_method(self):
        self.__private_method()
        self.__instance_private_attribute = 999

    def get_values(self):
        return (
            self.__class_private_attribute,
            self.__instance_private_attribute,
            self.__private_method_called,
        )


a = MyClass()
a.public_method()
assert __foo() == 123
assert a.get_values() == (555, 999, True)
