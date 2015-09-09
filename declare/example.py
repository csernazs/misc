from declarative import *


def main():
    ctx = Context()
    program = CompositeCommand(
        [VariableSetter(Variables.VARIABLE_M, Value(0)),
         VariableSetter(Variables.VARIABLE_A, ListCreator()),
         ListAppender(VariableRetriever(Variables.VARIABLE_A), Value(5)),
         ListAppender(VariableRetriever(Variables.VARIABLE_A), Value(10)),
         ListAppender(VariableRetriever(Variables.VARIABLE_A), Value(7)),
         ListAppender(VariableRetriever(Variables.VARIABLE_A), Value(1)),
         ListAppender(VariableRetriever(Variables.VARIABLE_A), Value(4)),
         Iterator(VariableRetriever(Variables.VARIABLE_A), VariableFactory(
             Variables.VARIABLE_B), CompositeCommand([Controller(
                 GreaterThanChecker(VariableRetriever(Variables.VARIABLE_B),
                                    VariableRetriever(Variables.VARIABLE_M)),
                 VariableSetter(Variables.VARIABLE_M, VariableRetriever(
                     Variables.VARIABLE_B)), NoOpCommand(),)])),
         Printer(VariableRetriever(Variables.VARIABLE_M)),])

    program.run(ctx)


if __name__ == "__main__":
    main()
