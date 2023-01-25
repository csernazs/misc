
# Python programming guide

## Intro

Despite the title, this document is mainly about how I write python code, which
principles I use, and what I think about a well written code.

## Users

Every code should take the users, and the usage into consideration. For example there's a
different approach between a publicly facing website vs a script which is used
by just a few users. Code quality, test coverage, etc, can vary between these
cases.

## Structure of a python program

Any python code which processes some data (which is most of the python code I
have seen or worked with), should have the following parts:

1. reads in some data (from file, db, HTTP, stdin, etc)
2. parses it into some data representation (into plain old python objects or
   data classes, or DAO or something)
3. validates the data
4. does the processing on the abstract data
5. persist the end result (writes to stdout, file, persist in DB, etc..)

This is somewhat similar to the [hexagon
architecture](https://en.wikipedia.org/wiki/Hexagonal_architecture_(software)).

The key point in the above design is that all parts of the code, mostly the 1-3,
4, 5 parts should be implemented indepently. That means that data processing should
have no knowledge about how the data was collected.

### Data reading and pre-parsing

This is the step where the IO part is separated from everything. Not only the
actual IO part, but also the data transformation and the parsing of the data
format is done here.

If there's a `foo.txt` file, which should be processed line by line, then it
should return the lines of the file in a string, with an decoding applied.

If the file is `foo.json`, it should parse the json to a python dict or list or
whatever it have.

If the file is `foo.yaml`, it should parse the yaml to a python dict or list or
whatever it have.

By that means, each of these can procude a list of string so those can be passed
to the next layer.


### Parsing

The data received in the previous step should be parsed into some abstract data
type. This should receive a pre-processed data, eg not raw data but some data
consisting of python list, dict, string, int, etc.

At the end of the parsing, an abstract data structure should be resulted where
the type conversion are done to the native python type and also some container
objects (plain old python object, dataclass, etc) are created at the end. There
should be no dicts of pre-defined keys, or such.

Data object may have methods to look up data in them.

This abstract data structure should be indepenent from the parser, and it should
be possible to create this structure programmatically.

For parsing I ususally create `from_dict` or `from_json` classmethods for the
classes, which accept the data from the parsers and `to_json` or `to_dict` which
serializes the data. By this way, these classes can be tested better as they
have their own methods.


### Validating

There are different aspects of the validation and it depends hugely of the
target users, the task and the whole program. In some cases it can be left out
without any issue, eg when the users are limited, the code is not running in any
end-product and nothing can go wrong (beyond having an unhandled exception at
maximum).


In every other cases there should be a validation step, which again can be some
minimum thing to help the user to a full validation (eg in a user facing web app
served publicly) where having an unhandled exception is not possible.

This also raises the topic of error message, i18n, and such.

### Processing

The processing code should work on an abstract data sctructure which can be
provided as-is, so that makes the processing code testable. For example if the
real data comes from a database, then the processing code can
still be tested without the requirement of a runnning database service.

### Persisting

Persistance is usually done by the methods of the objects keeping the data, so
at the end they will produce some json or yaml serializable data (eg dicts,
lists, etc).

This is then written to some file on the disk.



## Naming convention

...with some notable exceptions:
* Class names should be nouns.
* Callable object, (eg. methods, functions) should be verbs.
* Attributes should be nouns.

There's a well defined scheme for defining function/method names, which should
guarantee the behavior.

* Starting with `get_`: function should not change any value in the object or in
  anything. Definitely not having any side effect, such as modifying a file
  content.
* Starting with `create_`: function should create some object or file or
  database record. If there is some uniqueness to be guaranteed, then it should
  raise an exception. Eg. if a file to be created already exists, that would be
  the proper behavior.
* Starting with `ensure_`: similar to create, but the object may be existing and
  that must be handled without raising exception. It should also guaranntee that
  in such case, the existing object is not modified.
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

## No side effects in `__init__`

If it is possible, there should be no side effects in `__init__`. If it is not
possible, there should be a way to disable the side effect. For example if
there's a class wanting to connect to the database, there should be a boolean
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
The only possible exception should be `AttributeError` and nothing else. For
example, if there's a file operation in the property (which could raise IO error), then it should be
converted to a method instead, or the exception should be handled properly.

## Exceptions vs None as return value

Exceptions are for exceptional cases, so this should be taken into
consideration. I prefer returning with `None` in most of the cases.

For example if there's a `find_foo` method, then it is fine to return `None` if the
object is not found.


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

While the other is doing
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

Sometimes it is also good to have different classes by the contents. Some weird
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

## Program style and unification

If an existing code needs to be changed, it should be done in a way as the
original code was written, regardless which would be the "better" solution.

For example if a python code uses `str.format` method to format string, the
code which is added should also use that way to format the strings (instead of
f-strings). Same applies to pathlib. Path vs str paths.

Regardless to say that upgrading the code and moving forward is a required thing
with every code but I think that unification is more important.

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
needs to be set up and then passes the control to the lib. In other words it
should not contain business logic.

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
except foo.Error as err:
    ...
```

The larger app should define all the exceptions in a well defined python submodule
in it (`exc.py`, `error.py`, `exceptions.py`, whatever).

Also, decide if you want to re-use exceptions. I mostly re-use:

* `ValueError`: when the specified value for the function is out of bounds, or invalid
* `TypeError`: when isinstance fails

But as the code grows, it should use its own exceptions instead.

Exceptions which must never ever be re-used:

* `RuntimeError` is for python internals

*watch this space* :)

## Idiomatic way of using datetime

`import datetime as dt`


## Handling current time

When current time is queried, this should be taken very carefully to not query
it again within the code segment you want to keep in sync, it is sometimes the
whole app.

The reason for this is the time passes between the calls and if you check the
date in the first call to be Sunday but the additional code also checks it (for
whatever reason) then it can be Monday for the next call and if you want to
behave consistently then you need to "stop" the time for this case.

Needless to say if your code works with passing time (eg it calculates the
elapsed time, or it relies on the passing time), then it does not make any
sense.

In the library code, it is good to accept it as a parameter from the outside
(see the hexagon pattern I described above), this helps testing a lot also.

## Measuring elapsed time

This should be done by `time.monotonic()` or `time.perf_counter()`, but not with
`time.time()`.


## Handling global state

It is good to avoid global variables, but there are cases when it is acceptable,
such case is logging where the code obtains the logger object (which is somewhat
global).

But all of the global state needs to be handled very carefully. In Linux there
are a couple of global properties of the process so if a code changes it, then
it will affect other code.
To deal with it, one may use a context manager which ensures that the values are
restored to their original state. I really like context managers to handle
resources, and this is another good examples.

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
  subprocess (there's an API for this)


## One language

If it is possible, a code should be written in one language only. This means
that if some python code was written, it may run external programs, but those
should belong to other software (I have no problem with running `cp` instead of
using `shutil`, also it may be easier to run `ping` than writing it with the
`socket` module).

But if some functionality can be implemented in python better, and cleaner, it
should not be run by external code. For example `grep` should not be used from a
python code as it can filter the lines, and apply regexp.

There is one important exeptions to these, which is the performance of the code,
it is feasible and recommended way to call into C/C++ or rust or whatever
language which is more perfomant than python, but only if the performance is
crucial.


## Tests

Use pytest for test writing. Use fixtures as much as possible.

Separate the tests:
* unit: focus on a single class, module
* integration: focus on how the classes, modules work together
* e2e: testing IO and dependency on the outer world

If you follow the _Structure of a python program_ descibed above, you can write:

* unit tests for parsing
* integration tests for processing
* e2e tests for IO (reading, persisting data)

As unit and integration tests does not depend on any resources, those can be
written for every little edge cases, while e2e tests should only focus on the
IO, eg to check if the 3rd party library is working as expected, nothing more.

Use `assert`s as much as possible, for me it is completely ok to have a test
function with multiple asserts, eg checking various attributes of an object.

Where complex setup is needed, I usually prefer to write an `Environment` class
where I collect all the resources the test needs and then yield this from a
fixture.

For mocking I prefer to use the `pytest-mocker` plugin.
