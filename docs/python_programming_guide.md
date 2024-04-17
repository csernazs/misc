
# Python programming guide

## Intro

Despite the title, this document describes how I write python code, what
principles I use, and what I think about a well written code. This is solely my
own thinking and in its current form, it has nothing to do with others.

## Users

Every code should take the users, and the usage into consideration. For example there's a
different approach between a publicly facing website vs a script which is used
by just a few users. Code quality, test coverage, etc, can vary between these
cases. Every code which is written should focus on their users, to improve their
quality of living to make their life easier, not harder.

## Structure of a python program

Any python code which processes some data (which is most of the python code I
have seen or worked with), should have the following parts:

1. reads in some data (from file, db, HTTP, stdin, etc)
2. parses it into some data representation (into plain old python objects or
   data classes, or DAO or something)
3. validates the data
4. does the processing on the abstract data structure
5. persist the end result (writes to stdout, file, persist in DB, etc..)

This is somewhat similar to the [hexagon
architecture](https://en.wikipedia.org/wiki/Hexagonal_architecture_(software)).

The key point in the above design is that all parts of the code, mostly the 1-3,
4, 5 parts should be implemented independently. That means that data processing should
have no knowledge about how the data was collected.

This helps a lot testing the business logic (4. step).

In the following sections we go through each of the steps above.

### Data reading and pre-parsing

This is the step where the I/O part is separated from everything. Not only the
actual I/O part, but also the data transformation and the parsing of the data
format is done here.

If there's a `foo.txt` file, which should be processed line by line, then it
should return the lines of the file in a string, with some decoding applied.

If the file is `foo.json`, it should parse the json to python native types
(dict, list, int, string, etc...).

If the file is `foo.yaml`, it should parse the yaml to python native types
(dict, list, int, string, etc...).

Once the data is loaded to the memory, it usually loses the origin, where it was
loaded from. For example, if we receive a list of strings at the end, we should
not know what was the original format.

This gives flexibility in terms of re-factoring, if one file format turns out to
be infeasible.

Note should be taken here, that while the origin is lost, when an error happens
(see the detalis below) it is crucial to inform the user about the source (eg.
the file path), so they will know, which file caused the error.


### Parsing

The data received in the previous step is now loaded into some abstract data
type. This should receive a pre-processed data, eg not raw data but some data
consisting of python native types, such as list, dict, string, int, etc.

At the end of the parsing, an abstract data structure should be resulted where
the type conversion are done to the native python type and also some container
objects (plain old python object, dataclass, etc) are created at the end. There
should be no dicts of pre-defined keys, or such beyond this point.

Data object may have methods to look up data in them.

This abstract data structure should be independent from the parser, and it
should be possible to create this structure programmatically (eg. without
parsing an actual json file).

For parsing I ususally create `from_dict` or `from_json` classmethods for the
dataclasses, which accept the data from the parsers and `to_json` or `to_dict`
which serializes the data. By this way, these classes can be tested better as
they have their own methods.


### Validating

There are different aspects of the validation and it depends hugely of the
target users, the task and the whole program. In some cases it can be left out
without any issue, for example, when the list of the users is limited, the code
is not running in any end-product and nothing can go wrong (beyond having an
unhandled exception at maximum).

In every other cases there should be a validation step, which again can be some
minimum thing to help the user to a full validation (eg in a user facing web app
served publicly) where having an unhandled exception is not acceptable.

This also opens the topic of error message, i18n, and such.

### Processing

The processing code should work on an abstract data sctructure which can be
provided as-is, so that makes the processing code testable. For example if the
real data comes from a database, then the processing code can
still be tested without the requirement of a runnning database service.

I like to separate the classes which hold the data and have some basic/trivial
metods to look up/edit some data, and the classes which do the processing
(business logic). This also helps if the processing needs to take multiple data
objects.

### Persisting

Persistence is usually done by the methods of the objects keeping the data, so
at the end they will produce some json or yaml serializable data (eg dicts,
lists, etc).

This is then written to some file on the disk.

Similar to loading, this layer should also be flexible, in terms of file format
or target.


## Naming convention

...with some notable exceptions:

* Class names should be nouns.
* Callable object, (eg. methods, functions) should start with verbs.
* Attributes should be nouns.

There's a well defined scheme for defining function/method names, which should
guarantee the behavior and define a contract for the developer.

* Starting with `get_`: function should not change any value in the object or in
  anything. Definitely not having any side effect, such as modifying file
  content.
* Starting with `create_`: function should create some object or file or
  database record. If uniqueness is required, then it should raise an exception.
  Eg. if a file to be created already exists, that would be the proper behavior.
* Starting with `ensure_`: similar to create, but the object may be existing and
  that must be handled without raising exception. It also ensures that in such
  case, the existing object is not modified.
* Starting with `update_`: update some existing state. This should definitely
  not create anything new data. If the object to be updated does not exist, then
  it should raise an exception.
* Starting with `delete_`: delete the specified object. Exception should be
  raised if that object does not exist.

* Starting with `to_`: convert the data in this object to some other format. Eg.
  `to_dict` converts to a dictionary.

In class methods:

* Starting with `from_` specifies the data source where the constructor will be
  called, eg `from_json` or `from_dict` specifies the type of the data which
  will be used to initialize the object.


Exception class names should end with `Error`.


## No side effects in `__init__`

If it is possible, there should be no side effects in `__init__`. If it is not
possible, there should be a way to disable the side effect. For example if
there's a class wanting to connect to the database, there should be a (boolean)
parameter specifying whether to allow the `__init__` to connect to the db.

## Limit the exceptions in properties

Accessing a property and the attribute works the same way:
```python
foo.bar # is bar a property or an attribute?
```

If the property raises an exception that will be pretty much suprising for the
user, eg from this code:

```python
foo.bar
```

The only acceptable exception should be `AttributeError`, `AssertionError` (this
is for really exceptional "no way this will happen" cases) and nothing else. For
example, if there's a file operation in the property (which could raise I/O
error), then it should be converted to a method instead, or the exception should
be handled properly.

Also, handling the exception would look strange:

```
try:
    foo.bar
except OSError:
    ...
```

## Exceptions vs None as return value

Exceptions are for exceptional cases, so this should be taken into
consideration. I prefer returning with `None` in most of the cases.

For example if there's a `find_foo` method, then it is fine to return `None` if the
object is not found.

Whether the program could continue in the case the caller code not checking the
`None` value should be taken into account.


## Defining constants or superglobals

Instead of having the following in a file called `constants.py`:

```python
FOO = 123
```

At minimum, this should be converted to:
```
class Config:
    FOO = 123
```

This is to avoid the situation where some code is doing:
```python
from constants import FOO
```

While the other (test code, for example) is doing
```python
import constants
constants.FOO = 345
```

Then the `FOO` value in the first import won't be updated. By putting this value
to the `Config` class, this can be solved by:

```python
from constants import Config
```

and

```python
from constants import Config
Config.FOO = 345
```


## Boolean parameters

Boolean parameters should be kwarg only.

## `retval` variable

Within a function I use the `retval` variable to keep the return value. This
might not be matching with the return type, though, as in the last step
sometimes I do the conversion to the return type.

## TOCTOU

If we want 100% correctness, there should be no TOCTOU in codes but readability
also matters and for example the following code is usually ok for me:

```python

def read_config(path: Path):
    if not path.is_file():
        raise UsageError(f"No such file: {path}")
    # read the file, which can still raise exceptions but those are exceptional cases
```

## Checking files, directories

When TOCTOU is not feasible, we want to check for the existence of the path.

Notable differences in python that it can check for a path existence
(`path.exists()`)  and specifically for existence of a file (`path.is_file()`)
or a directory (`path.is_dir()`) or for other special cases.

If there's a check before open for a path, then it should be checked by
`is_file`. Similar, if the code following expect the path to be directory it
should be checked by `is_dir` (eg you want to get the contents of the directory).

For such checks it is important that for the users we communicate it in a proper
way, eg *no such file* or *no such directory* but not like *path does not exist*.


## Avoid nested ifs

It is ok to check some value and then `return` or `break` or `continue`.

Instead:
```python
def foo(x: int):
    if x > 0:
        # some processing for 50 lines or more...
    else:
        raise ValueError(x)
```

```python
def foo(x: int):
    if x <= 0:
        raise ValueError(x)
    # some processing for 50 lines or more...
```

Same applies for loops:

```python
def foo(x: list[int]):
    for item in x:
        if x <= 0:
            continue # only if it is ok to ignore that element
        # some processing for 50 lines or more...
```

## Static vs dynamic typing

Although python is a dynamically typed language, use classes, add type hints for
function definitions (at least).

Use `mypy` or some other type checker.

Sometimes it is also good to have different classes by the values. Some weird
example:

```python

class Integer:
    def __init__(self, value: int):
        self.value = value

class PositiveInteger(Integer):
    def __init__(self, value: int):
        if value < 0:
            raise ValueError("Positive number required")
        self.value = value

# then in a function, specify:

def foo(x: PositiveInteger):
    ...

```

## Private methods

I never use double underscores as it is just a name mangling. Having a single
underscore as a prefix is a good practice though to indicate that the
method/attribute should not be used from the outer world.

## Context managers

Context managers are good and every resource should be closed or returned at the
point where it is no longer needed.

When writing an API, consider implementing a context manager if your code is
using some external resource.

Context managers are also a must when some process-global state is modified (eg.
current directory, environment variable) and their lifetime needs to be
controlled (in other words: it needs to be restored to their previous value).

## Atomic transactions

If some persistent data is changed, it should be atomic. This can be done by
rename or by making begin..commit in databases.

## Building blocks, SRP

[SRP](https://en.wikipedia.org/wiki/Single_responsibility_principle) says that
everything should have a single responsibility. What I get from it is that the
program should be built from building blocks which can work together.

This means that classes or data structures should have their limited data stored
in them and they should operate mostly on their data. This results a code where
the instances of their classes can be re-used without any struggle.

## Composition vs. inheritance

If you follow SRP then to build complex things you have to compose objects. In
python, in my experience this usually means passing the instances to the other
object constructor and then constructing the desired functionality.

```python
SomeClass(Database(), Config())
```

So the `SomeClass` receive the `Database` and `Config` instances, so it can operate on
them. The `SomeClass` has no code dealing with the database directly, it operates on
the database via the object it received, and it is same for the config object.

At the end, you can test all the 3 classes. Also you can test the `SomeClass` by
providing a fake database and a fake config object to it (eg. to simulate various
errors).

You can also do this by inheritance. This also works in some other cases where
you have to extend or override some method in a class to change the
functionality.


## Optional dependencies

If a program optionally requires a package and can function without it, it can
be handled by:

```python
try:
    import foobar
except ModuleNotFoundError:
    foobar=None
```

Later the code can check `if foobar is not None` for the availability of the `foobar`.

I find putting these code pieces depending on optional deps to a separate python
module better so in that case the code can be separated.

It it make sense, null object (or noop objects) can be defined in the case the
optional dependency is missing, so the optional package availability will be
opaque for the others.


## Program style and unification

If an existing code needs to be changed, it should be done in a way as the
original code was written, regardless which would be the "better" solution.

For example if a python code uses `str.format` method to format string, the
code which is added should also use that way to format the strings (instead of
f-strings). Same applies to pathlib. Path vs str paths.

Needless to say that upgrading the code and moving forward is a required thing
with every piece of code but I think that unification is more important.

Refactoring can be done however with some parts of the code also, but that part
should be definied clearly.

## CLI is a lib + entry point

A command-line program is just a library, and it has an entry point defined by
setuptools or by other way.
This usually has an `Application` class with a `main` function.

I usually do the argument parsing with `argparse`, but the point here is that
instead of using `sys.argv` directly, there should be a help for `--help`, which
also implies that there is a description (either programmatically or not)
somewhere about the CLI parameters.

For a larger CLI program, this `Application` class has the only purpose of
parsing the command line arguments, setting up logging, and whatever resources
needs to be set up (calling functions to parse config files, or load data) and
then passes the control to the lib. In other words it should not contain
business logic, unless it is so little and trivial that creating a separate
function or class would be overkill.

## What a lib code must never ever do

* Calling `sys.exit()` or raising `SystemExit`
* printing to stdout
* In general: using stdout, stderr and stdin directly

## Custom exceptions

For a larger app, create a base exeption class which will be used for all
exceptions defined in that code:

```python

class Error(Exception):
    pass

class MyError(Error):
    pass
```

So the user of your library can do:

```python
from foo.exc import Error

try:
    foo.whatever()
except Error as err:
    ...
```

The larger app should define all the exceptions in a well defined python
submodule in it (`exc.py`, `error.py`, `exceptions.py`, etc).

Also, decide if you want to re-use exceptions. I mostly re-use:

* `ValueError`: when the specified value for the function is out of bounds, or invalid
* `TypeError`: when isinstance fails

But as the code grows, it should use its own exceptions instead.

Exceptions which must never ever be re-used:

* `RuntimeError` is for python internals
* `NameError` for variable name lookup errors
* `SyntaxError` for python syntax errors

*watch this space* :)

## Idiomatic way of using datetime

`import datetime as dt`

Acceptable in some cases:

`from datetime import datetime`

## Handling current time

When current time is queried, this should be taken very carefully to not query
it again within the code segment you want to keep the time freezed. This code
segment is sometimes the whole app.

The reason for this is the fact that time passes between the calls and if you
check the date in the first call to be Sunday but the additional code also
checks it (for whatever reason) then it can be Monday for the next call and if
you want to behave consistently then you need to "stop" the time for this case.

Also, if you work with local time or utc, this can go backward and could end up
in surprising results having negative elapsed time.

In the library code, it is good to accept the current time as a parameter from
the outside (see the hexagon pattern I described above), this helps testing a
lot, as code which is tested will be run in a well defined environment and
won't be subject to the actual date or time.

It should be never assumed that between two `datetime.now()` calls there's so
little time that going from one day to the next one impossible.

Needless to say if the code works with passing time (eg it calculates the
elapsed time, or it relies on the passing time), then it does not make any
sense. In such case the code must be prepared for backward ticking time by using
monotonic time (see below).


## Measuring elapsed time

This should be done by `time.monotonic()` or `time.perf_counter()`, but not with
`time.time()` as it can go backward.


## Handling global state

It is good to avoid global variables, but there are cases when it is acceptable,
such case is logging where the code obtains the logger object (which is somewhat
global).

But all of the global state needs to be handled very carefully. In Linux there
are a couple of global properties of the process so if a code changes it, then
it will affect other code.

To deal with it, one may use a context manager which ensures that the values are
restored to their original state. I really like context managers to handle
resources, and this is another good example.

Such global states are (list is not full):

* signal handlers
* current working directory
* environment variables
* ulimits, rlimits
* capabilities
* time?


If possible, it is a good way to set these at the beginning and then not change
them at all, or have the context manager I mentioned to keep them under control.

Setting some global states can be (and should be) avoided, such as:

* current working directory: use absolute path
* environment variables: set the environment variables when you are running a
  subprocess (there's an API for this, for example the `env` parameter of the
  `subprocess.run` function).

## Singleton

Singleton is a global variable, so there are some clever solutions on the
internet how can you create a class which returns the same instance, mostly with
`__new__` or others.

There's one problem with it. It really does not allow to instantiate a new
object (unless you do hacks). If you want to tweak something for your tests for
example, you are stuck.

So for this "singleton" like behavior, it is better to store the instance
variable at module level:

```python
class MySingleton:
    ...

myvar = MySingleton()
```

And then use `myvar` everywhere. You can implement a function returning this if
you want and add an underscore to this variable to sign that nobody should
access it directly.

```python
def get_var():
    return _myvar
```


## Units

This is about the real units, like seconds, meters, pixels, whatever.
These are very important. Some team crashed a probe to the surface of Mars
because they used different systems (imperial vs metric).

Either the variable name should suggest the unit like this:

```python
def sleep(secs: float):
    ...
```

...or the docstring:

```python
def sleep(duration: float):
    """
    :param duration: amount of time to spent in seconds
    """
    ...
```

## Frozen dataclasses

It is a good thing to always make the dataclasses frozen:

```python

@dataclass(frozen=True)
class Person:
    name: str
    age: int
```

So it will make it hashable (you can add it to sets and use as keys in dict).
But on the other hand, it makes it virtually impossible to change the fields
once the class is instantiated. This is good because if you add some validators
to `__post_init__` then it can provide some constraints on the data.
Also, it is good to have immutable types in the program as a rule of thumb.


## One language

If it is possible, a code should be written in one language only. This means
that if some python code was written, it may run external programs, but those
should belong to other software (I have no problem with running `cp` instead of
using `shutil`, also it may be easier to run `ping` than writing it with the
`socket` module).

But if some functionality can be implemented in python better, and cleaner, it
should not be run by external code. For example `grep` should not be used from a
python code as python can filter the lines, by a regexp wiht a few lines of
code.

There is one important exeptions to these, which is the performance of the code.
It is feasible and recommended way to call into C/C++ or rust or whatever
language which is more perfomant than python, but only if the performance is
crucial.


## Tests

Use pytest for test writing. Use fixtures as much as possible.

Separate the tests:
* unit: focus on a single class, module
* integration: focus on how the classes, modules work together
* e2e: testing I/O and dependency on the outer world, may run external programs

If you follow the _Structure of a python program_ descibed above, you can write:

* unit tests for parsing
* integration tests for processing
* e2e tests for I/O (reading, persisting data)

As unit and integration tests does not depend on any resources, those can be
written for every little edge cases, while e2e tests should only focus on the
I/O, compatibility with external processes or resources. While unit tests may
"see" the code which is tested, e2e should use a black-box model, having no
information about the implementation details.

Use `assert`s as much as possible, for me it is completely ok to have a test
function with multiple asserts, eg checking various attributes of an object.

Where complex setup is needed, I usually prefer to write an `Environment` class
where I collect all the resources the test needs and then yield this from a
fixture.

For mocking I prefer to use the `pytest-mock` plugin.

Create coverage reports. 100% is not a target, and not the percentage which
matters but the uncovered lines. Some IDEs have plugins which can show the
results instantly, but a html can also be rendered from the coverage report.

For variable comparison `dirty-equals` is a great library.

# Usability, UX

## CLI

### Error messages

Error messages for the users should contain the exact error we found, and it
must be:
1. explicit: the error should be communicated with no frills, however context
   may be added to it.
2. real: This is not acceptable to say that "No such file" for a file which exists.


There are two categories of the errors:
1. it is fixable by the user
2. it is not fixable by the user

When it is fixable by the user, it should be communicated to them. For example if
there's not sufficient free space, we should also communicate where to look for
possibly removable content.

If a config file missing, we should inform the user how to create the config
file.

If a config seems to be a temporary issue, the user should know what they can
give it another try.

If this issue cannot be fixed, we should inform the user to contact the group
responsible for the software.

Tracebacks should be avoided at all places where we know what the error was. CLI
code should handle exceptions whenever possible, for example file I/O errors
should be communicated without traceback.

Tracebacks are reserved for internal, unhandled, most serious errors where the
error is most likely caused by a bug in the code.

### status

If it makes sense (eg the program has some state), the CLI should have a
`status` subcommand, which similar to `git` would show what is the current
status. It should provide details about what is set up, probably from the
configuration files, and also about what the user could possibly do next.

### Logging

Users should receive log messages even if the program works normally. They
should receive some message when the processing will take long time, or when
some checkpoint is reached in the processing.

They should be warned if something takes longer than expected.

Errors should always be communicated and visible.

Debug messages are optional and can help debugging but these are disabled by
default to avoid confusion.

Logging to file should have timestamps while logging to the user does not
requires timestamps.
