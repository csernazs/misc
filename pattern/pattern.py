

class NoPattern(Exception):
    pass


class Any:
    pass


class Param:
    def __init__(self, name):
        self.name = name


class Value:
    def __init__(self, param: Param, value):
        self.param = param
        self.value = value

    def match(self, arg):
        if arg == self.value:
            return {self.param.name: self.value}
        else:
            return None

class HeadTail:
    def __init__(self, head: Param, tail: Param):
        self.head = head
        self.tail = tail

    def match(self, arg):
        if isinstance(arg, (tuple, list)):
            if len(arg) > 1:
                return {self.head.name: arg[0], self.tail.name: arg[1:]}

        return None


class Pattern:
    def __init__(self, args):
        self.args = args

    def match(self, func_args):
        retval = {}
        for func_arg, pattern_arg in zip(func_args, self.args):
            result = pattern_arg.match(func_arg)
            if isinstance(result, dict):
                retval.update(result)
            else:
                return None

        return retval


class FunctionGroup:
    def __init__(self):
        self.functions = []

    def pattern(self, *match_args):
        pattern = Pattern(match_args)

        def decorator(func):
            self.functions.append((pattern, func))

            def wrapped(*func_args):
                match = self.match(*func_args)
                if match is None:
                    raise NoPattern("No pattern found for arguments: {!r}".format(func_args))
                callable, pattern_args = match
                retval = callable(**pattern_args)
                print(retval)
                return retval

            return wrapped

        return decorator

    def match(self, *func_args):
        for pattern, function in self.functions:
            match = pattern.match(func_args)
            if match:
                return (function, match)

        return None


fg = FunctionGroup()


# Here, I want the head of the list and the rest of the elements
# in 'head' and 'tail' parameters. This works only for lists
# having at least two elements.
@fg.pattern(HeadTail(Param("head"), Param("tail")))
def hello(head, tail):
    print(head, tail)

# This says that if the function is called with an empty list, then
# this function should be called instead.
@fg.pattern(Value(Param("empty"), []))
def hello2(empty):
    print("empty list", empty)

# you can call any 'member' of the function group, it does not really
# matter as the pattern matching will determine the final function to
# be actually called...
hello([]) # this will call hello2()
hello([1, 2, 3]) # this will call hello()
