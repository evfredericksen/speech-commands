from dragonfly import *
from srabuilder import rules
import utils
import contexts

functions = {
    "absolute": "abs",
    "all": "all",
    "any": "any",
    "boolean": "bool",
    "callable": "callable",
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
    'collections': 'collections',
    '(jay son | jay saw n)': 'json',
    'logging': 'logging',
    'eye oh': 'io',
    's h you till': 'shutil',
    'time': 'time',
    'sis': 'sys',
    'o s': "os",
    'o s [dot] path': "os.path",
    'multi processing': 'multiprocessing',
    'a sink eye oh': 'asyncio',
    'queue': 'queue',
    'threading': 'threading',
    'unit test': 'unittest',
    'requests': 'requests',
    'types': 'types',
    'typing': 'typing',
    'regular (expression | expressions)': 're',
    "sea ess v": "csv",
    "it er tools": "itertools",
    "funk tools": "functools",
    "statistics": "statistics",
    "random": "random",
    "math": "math",
    "copy": "copy",
    "weak ref": "weakref",
    "date time": "datetime",
}

mapping = {
    "import": Text("import "),
    "import <modules>": "import %(modules)s",
    "name <modules>": "%(modules)s",
    "assign": Text(" = "),
    "compare": Text(" == "),
    "list comprehension": "[x for x in ]{left}",
    "from": Text("from "),
    "assert": Text("assert "),
    "return": Text("return "),
    "break": Text("break"),
    "continue": Text("continue"),
    "say in": Text(" in "),
    "say is": Text(" is "),
    "say not": Text("not "),
    "say and": Text(" and "),
    "say or": Text(" or "),
    "<errors>": "%(errors)s",
    "if expression": " if  else {left:10}",
    "if statement": "if :{left}",
    "while loop": "while :{left}",
    "else statement": "else:{enter}",
    "if else": "if :\npass\nelse:\npass{up:3}{left}",
    "else if [statement]": "elif :{left}",
    "try except": "try:{c-enter}pass{c-enter}except:{c-enter}pass{up:2}{c-d}",
    "pass": "pass",
    "true": "True",
    "false": "False",
    "none": "None",
    "dictionary": "{{}}{left}",
    "slice": "[:]{left:2}",
    "new function": "def ():{left:3}",
    "new lambda": "lambda :{left}",
    "new method": "def (self):{left:7}",
    "new class": "class :{enter}def __init__(self):{enter}pass{up:2}{end}{left}",
    "name <functions>": "%(functions)s",
    "under": "____{left:2}",
    "call <functions>": "%(functions)s(){left}",
    "read file": "with open() as f:{left:7}",
    "write file": "with open(, 'w') as f:{left:12}",
    "read binary": "with open(, 'rb') as f:{left:14}",
    "write binary": "with open(, 'wb') as f:{left:14}",
    "with statement": "with :{left}",
    "with as": "with  as :{left:5}",
    "for loop": "for :{left}",
    "for enumerate": "for i,  in enumerate():{left:16}",
    "index": "[]{left}",
    "string": "''{left}",
    "double string": '""{left}',
    "f string": "f''{left}",
    "double f string": 'f""{left}',
    "args": '*args',
    "kwargs": '**kwargs',
    "initializer": "def __init__(self):{left:2}",
}
extras = [Choice("functions", functions), Choice("errors", errors), Choice('modules', modules)]
utils.load_commands(contexts.python, commands=mapping, extras=extras)
