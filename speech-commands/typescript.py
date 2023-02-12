from dragonfly import *
import srabuilder.actions
from srabuilder import rules

import utils
import contexts


functions = {
    "console [dot] log": "console.log",
    "entries": "entries",
    "is array": "isArray",
    "length": "length",
    "slice": "slice",
    "set timeout": "setTimeout",
    "set interval": "setInterval",
    "fetch": "fetch",
    "get element by id": "getElementById",
    "sort": "sort",
    "map": "map",
    "filter": "filter",
    "has own property": "hasOwnProperty",
    "use state": "useState",
}

namespaces = {
    "array": "Array",
    "object": "Object",
}

mapping = {
    "skiff": "if ",
    "let": "let ",
    "const": "const ",
    "if state": "if () {{}}{left}{enter}{up}{end}{left:3}",
    "while loop": "while () {{}}{left}{enter}{up}{end}{left:3}",
    "for loop": "for (const x of ) {{}}{left}{enter}{up}{end}{left:3}",
    "c for loop": "for (let i = 0; i < ; i++) {{}}{left}{enter}{up}{end}{left:8}",
    "what about": "else if () {{}}{left}{enter}{up}{end}{left:3}",
    "else state": "else {{}}{left}{enter}",
    "switch state": "switch () {{}}{left}{enter}{up}{end}{left:3}",
    "case state": "case :{left}",
    "assign": " = ",
    "double compare": " == ",
    "compare": " === ",
    "double contrast": " != ",
    "contrast": " !== ",
    "not": "!",
    "stand": " && ",
    "store": " || ",
    "true": "true",
    "false": "false",
    "null": "null",
    "undefined": "undefined",
    "document": "document",
    "await": "await ",
    "a sink": "async ",
    "new": "new ",
    "return": "return ",
    "break": "break",
    "continue": "continue",
    "scope": "{{}}{left}{enter}",
    "define function": "function () {{}}{left}{enter}{up}{end}{left:4}",
    "define arrow function": "() => {{}}{left}{enter}",
    "define inline arrow function": "() => ",
    "arrow": " => ",
    "define method": "() {{}}{left}{enter}{up}{end}{left:4}",
    "define class": "class  {{}}{left}{enter}constructor() {{}}{left}{enter}{up:2}{end}{left:2}",
    "just <functions>": "%(functions)s",
    "just <namespaces>": "%(namespaces)s",
    "<namespaces> (dot | period) <functions> ": "%(namespaces)s.%(functions)s",
    "call <functions>": "%(functions)s(){left}",
    "array": "[]{left}",
    "object": "{{}}{left}",
    "true": "true",
    "false": "false",
    "null": "null",
    "[double] string": '""{left}',
    "single string": "''{left}",
    "template string": "``{left}",
    "export": "export ",
    "default": "default ",
    "interface": "interface ",
    "define constructor": "constructor",
    "type": "type ",
    "key of": "keyof ",
    "annotate": ": ",
    "just number": "number",
    "just string": "string",
    "implements": "implements ",
    "extends": "extends ",
    "generic": "<>{left}",
    "import statement": 'import  from "";{left:9}',
    "import": "import ",
    "document": "document",
    "this": "this",
}

extras = [Choice("functions", functions), Choice("namespaces", namespaces)]
utils.load_commands(contexts.javascript, commands=mapping, extras=extras)