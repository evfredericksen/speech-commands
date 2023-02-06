from dragonfly import *
import utils
import contexts

functions = {
    "absolute": "abs",
    "a sink context manager": "asynccontextmanager",
    "all": "all",
    "any": "any",
    "boolean": "bool",
    "callable": "callable",
    "context manager": "contextmanager",
    "default (dictionary | dict)": "defaultdict",
    "dear": "dir",
    "delete attribute": "delattr",
    "enumerate": "enumerate",
    "eye d": "id",
    "filter": "filter",
    "float": "float",
    "format": "format",
    "global's": "globals",
    "get attribute": "getattr",
    "input": "input",
    "int": "int",
    "is instance": "isinstance",
    "it er": "iter",
    "join": "join",
    "length": "len",
    "list": "list",
    "locals": "locals",
    "min": "min",
    "max": "max",
    "object": "object",
    "open": "open",
    "print": "print",
    "range": "range",
    "reversed": "reversed",
    "round": "round",
    "set": "set",
    "set attribute": "setattr",
    "slice": "slice",
    "sorted": "sorted",
    "split": "split",
    "string": "str",
    "sum": "sum",
    "super": "super",
    "two pull": "tuple",
    "update": "update",
    "oh ess [dot] path [dot] join": "os.path.join",
    "zip": "zip",
}

errors = {
    "(assert|assertion) error": "AssertionError",
    "key error": "KeyError",
    "exception": "Exception",
    "import error": "ImportError",
    "index error": "IndexError",
    "not implemented error": "NotImplementedError",
    "oh s error": "OSError",
    "run time error": "RuntimeError",
    "type error": "TypeError",
    "value error": "ValueError",
}

modules = {
    'arg parse': 'argparse',
    'a sink eye oh': 'asyncio',
    'context lib': 'contextlib',
    "sea ess v": "csv",
    'collections': 'collections',
    '(jay son | jay saw n)': 'json',
    'logging': 'logging',
    'eye oh': 'io',
    "it er tools": "itertools",
    'multi processing': 'multiprocessing',
    'o s': "os",
    'o s [dot] path': "os.path",
    'queue': 'queue',
    'regular (expression | expressions)': 're',
    'requests': 'requests',
    's h you till': 'shutil',
    'sis': 'sys',
    'time': 'time',
    'threading': 'threading',
    'types': 'types',
    'typing': 'typing',
    'unit test': 'unittest',
    "you you eye dee": "uuid",
    "z lib": "zlib",
    "funk tools": "functools",
    "statistics": "statistics",
    "random": "random",
    "math": "math",
    "copy": "copy",
    "weak ref": "weakref",
    "date time": "datetime",
    "sis": "sys",
}

mapping = {
    "import": "import ",
    "raise": "raise ",
    "import <modules>": "import %(modules)s",
    "from <modules> import": "from %(modules)s import ",
    "just <modules>": "%(modules)s",
    "assign": " = ",
    "compare": " == ",
    "contrast": " != ",
    "list comprehension": "[x for x in ]{left}",
    "from": "from ",
    "assert": "assert ",
    "return": "return ",
    "break": "break",
    "continue": "continue",
    "fin": " in ",
    "fizz": " is ",
    "not": "not ",
    "skiff": "if ",
    "else": "else ",
    "stand": " and ",
    "store": " or ",
    "a sink": "async",
    "<errors>": "%(errors)s",
    "if expression": " if  else {left:10}",
    "if state": "if :{left}",
    "while loop": "while :{left}",
    "else state": "else:{enter}",
    "if else state": "if :\npass\nelse:\npass{up:3}{left}",
    "what about": "elif ",
    "what about state": "elif :{left}",
    "try except": "try:{c-enter}pass{c-enter}except:{c-enter}pass{up:2}{c-d}",
    "pass": "pass",
    "true": "True",
    "false": "False",
    "none": "None",
    "list": "[]{left}",
    "dictionary": "{{}}{left}",
    "slice": "[:]{left:2}",
    "new function": "def ():{left:3}",
    "new lambda": "lambda :{left}",
    "new method": "def (self):{left:7}",
    "new class": "class :{enter}def __init__(self):{enter}pass{up:2}{end}{left}",
    "just <functions>": "%(functions)s",
    "double under": "____{left:2}",
    "call <functions>": "%(functions)s(){left}",
    "read file": "with open() as f:{left:7}",
    "write file": "with open(, 'w') as f:{left:12}",
    "read binary": "with open(, 'rb') as f:{left:14}",
    "write binary": "with open(, 'wb') as f:{left:14}",
    "with state": "with :{left}",
    "with ": "with ",
    "as ": " as ",
    "for loop": "for :{left}",
    "for enumerate": "for i,  in enumerate():{left:16}",
    "index": "[]{left}",
    "string": '""{left}',
    "single string": "''{left}",
    "f string": 'f""{left}',
    "single f string": "f''{left}",
    "args": '*args',
    "kwargs": '**kwargs',
    "initializer": "def __init__(self):{left:2}",
    "annotate": ": ",
    "this": "self",
}
extras = [Choice("functions", functions), Choice("errors", errors), Choice('modules', modules)]
utils.load_commands(contexts.python, commands=mapping, extras=extras)
