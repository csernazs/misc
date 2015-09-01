import unittest
from declarative import *


class TestVariable(unittest.TestCase):

    def test_variable(self):
        ctx = Context()
        program = CompositeCommand([
            VariableSetter(Variables.VARIABLE_A, Value("hello world")),
            VariableSetter(
                Variables.VARIABLE_B, VariableRetriever(Variables.VARIABLE_A))
        ])

        program.run(ctx)
        self.assertEqual(ctx.variables[Variables.VARIABLE_A], "hello world")
        self.assertEqual(ctx.variables[Variables.VARIABLE_B], "hello world")

    def test_list_creator(self):
        ctx = Context()

        program = CompositeCommand([
            VariableSetter(Variables.VARIABLE_A, ListCreator()),
            ListAppender(VariableRetriever(Variables.VARIABLE_A), Value("a")),
            ListAppender(VariableRetriever(Variables.VARIABLE_A), Value("b")),
            ListAppender(VariableRetriever(Variables.VARIABLE_A), Value("c")),
        ])

        program.run(ctx)
        self.assertEqual(ctx.variables[Variables.VARIABLE_A], ["a", "b", "c"])

    def test_addition(self):
        ctx = Context()
        program = CompositeCommand([
            VariableSetter(
                Variables.VARIABLE_A, AdditionCommand(Value(1), Value(2)))
        ])

        program.run(ctx)

        self.assertEqual(ctx.variables[Variables.VARIABLE_A], 3)

    def test_list_iterator(self):
        ctx = Context()

        program = CompositeCommand([
            VariableSetter(Variables.VARIABLE_A, ListCreator()),
            VariableSetter(Variables.VARIABLE_C, Value("")),
            ListAppender(VariableRetriever(Variables.VARIABLE_A), Value("a")),
            ListAppender(VariableRetriever(Variables.VARIABLE_A), Value("b")),
            ListAppender(VariableRetriever(Variables.VARIABLE_A), Value("c")),
            Iterator(
                VariableRetriever(Variables.VARIABLE_A), VariableFactory(
                    Variables.VARIABLE_B),
                VariableSetter(Variables.VARIABLE_C,
                               AdditionCommand(
                                   VariableRetriever(
                                       Variables.VARIABLE_C),
                                   VariableRetriever(Variables.VARIABLE_B))))
        ])

        program.run(ctx)
        self.assertEqual(ctx.variables[Variables.VARIABLE_C], "abc")

    def test_controller(self):
        ctx = Context()

        program = CompositeCommand([
            VariableSetter(Variables.VARIABLE_A, Value(1)),
            VariableSetter(Variables.VARIABLE_B, Value(2)),
            Controller(
                EqualityChecker(
                    VariableRetriever(
                        Variables.VARIABLE_A), VariableRetriever(
                            Variables.VARIABLE_B)),
                VariableSetter(Variables.VARIABLE_C, Value(1)), VariableSetter(Variables.VARIABLE_D, Value(1)))
        ])

        program.run(ctx)

        self.assertEqual(ctx.variables[Variables.VARIABLE_D], 1)


if __name__ == '__main__':
    unittest.main()
