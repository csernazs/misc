from __future__ import print_function


class Variables:
    VARIABLE_A = "a"
    VARIABLE_B = "b"
    VARIABLE_C = "c"
    VARIABLE_D = "d"
    VARIABLE_E = "e"
    VARIABLE_F = "f"
    VARIABLE_G = "g"
    VARIABLE_H = "h"
    VARIABLE_I = "i"
    VARIABLE_J = "j"
    VARIABLE_K = "k"
    VARIABLE_L = "l"
    VARIABLE_M = "m"
    VARIABLE_N = "n"
    VARIABLE_O = "o"
    VARIABLE_P = "p"
    VARIABLE_Q = "q"
    VARIABLE_R = "r"
    VARIABLE_S = "s"
    VARIABLE_T = "t"
    VARIABLE_U = "u"
    VARIABLE_V = "v"
    VARIABLE_W = "w"
    VARIABLE_X = "x"
    VARIABLE_Y = "y"
    VARIABLE_Z = "z"

    VALID_VARIABLES = {
        VARIABLE_A,
        VARIABLE_B,
        VARIABLE_C,
        VARIABLE_D,
        VARIABLE_E,
        VARIABLE_F,
        VARIABLE_G,
        VARIABLE_H,
        VARIABLE_I,
        VARIABLE_J,
        VARIABLE_K,
        VARIABLE_L,
        VARIABLE_M,
        VARIABLE_N,
        VARIABLE_O,
        VARIABLE_P,
        VARIABLE_Q,
        VARIABLE_R,
        VARIABLE_S,
        VARIABLE_T,
        VARIABLE_U,
        VARIABLE_V,
        VARIABLE_W,
        VARIABLE_X,
        VARIABLE_Y,
        VARIABLE_Z,
    }


class Context:

    def __init__(self):
        self.variables = {}


class Error(Exception):
    pass


class VariableError(Error):
    pass


class Command:

    def _validate_variable(self, variable):
        if variable not in Variables.VALID_VARIABLES:
            raise VariableError("Invalid variable: {}".format(variable))


class CompositeCommand(Command):

    def __init__(self, commands):
        self.__commands = commands

    def run(self, context):
        retval = []
        for command in self.__commands:
            retval.append(command.run(context))

        return retval


class Value(Command):

    def __init__(self, value):
        self.__value = value

    def run(self, context):
        return self.__value


class VariableSetter(Command):

    def __init__(self, variable, command):
        self._validate_variable(variable)
        self.__variable = variable
        self.__command = command

    def run(self, context):
        context.variables[self.__variable] = self.__command.run(context)


class VariableRetriever(Command):

    def __init__(self, variable):
        self._validate_variable(variable)
        self.__variable = variable

    def run(self, context):
        return context.variables[self.__variable]


class CommandFactory:
    pass


class VariableFactory:

    def __init__(self, variable):
        self.__variable = variable

    def get_new_instance(self, item):
        return VariableSetter(self.__variable, item)


class ListCreator(Command):

    def run(self, context):
        return []


class ListAppender(Command):

    def __init__(self, list_retriever, value_retriever):
        self.__list_retriever = list_retriever
        self.__value_retriever = value_retriever

    def run(self, context):
        retrieved_list = self.__list_retriever.run(context)
        retrieved_list.append(self.__value_retriever.run(context))


class Iterator(Command):

    def __init__(self, list_retriever, value_factory, body_command):
        self.__list_retriever = list_retriever
        self.__value_factory = value_factory
        self.__body_command = body_command

    def run(self, context):
        iter_list = self.__list_retriever.run(context)

        for item in iter_list:
            command = self.__value_factory.get_new_instance(Value(item))
            command.run(context)
            self.__body_command.run(context)


class BinaryCommand(Command):

    def __init__(self, variable_a_retriever, variable_b_retriever):
        self._value_retriever_a = variable_a_retriever
        self._value_retriever_b = variable_b_retriever

    def _get_values(self, context):
        return (
            self._value_retriever_a.run(context),
            self._value_retriever_b.run(context)
        )


class BinaryOperation(BinaryCommand):

    def run(self, context):
        value_a, value_b = self._get_values(context)
        return self._operation(value_a, value_b)


class AdditionCommand(BinaryOperation):

    def _operation(self, value_a, value_b):
        return value_a + value_b


class EqualityChecker(BinaryOperation):

    def _operation(self, value_a, value_b):
        return value_a == value_b


class GreaterThanChecker(BinaryOperation):

    def _operation(self, value_a, value_b):
        return value_a > value_b


class Controller(Command):

    def __init__(self, value_retriever, positive_command, negative_command):
        self.__value_retriever = value_retriever
        self.__positive_command = positive_command
        self.__negative_command = negative_command

    def run(self, context):
        value = self.__value_retriever.run(context)
        if value:
            self.__positive_command.run(context)
        else:
            self.__negative_command.run(context)


class Printer(Command):

    def __init__(self, value_retriever):
        self.__value_retriever = value_retriever

    def run(self, context):
        print(self.__value_retriever.run(context))


class NoOpCommand(Command):

    def __init__(self):
        pass

    def run(self, context):
        pass
