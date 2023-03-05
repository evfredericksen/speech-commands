from dragonfly import *
import srabuilder.actions
from srabuilder import rules

import utils, vscode2
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
    "skiff": vscode2.insert_padded("if "),
    "let": vscode2.insert_padded("let "),
    "const": vscode2.insert_padded("const "),
    "if state": "if () {{}}{left}{enter}{up}{end}{left:3}",
    "while loop": "while () {{}}{left}{enter}{up}{end}{left:3}",
    "for loop": "for (const x of ) {{}}{left}{enter}{up}{end}{left:3}",
    "c for loop": "for (let i = 0; i < ; i++) {{}}{left}{enter}{up}{end}{left:8}",
    "what about": "else if () {{}}{left}{enter}{up}{end}{left:3}",
    "else state": "else {{}}{left}{enter}",
    "switch state": "switch () {{}}{left}{enter}{up}{end}{left:3}",
    "case state": "case :{left}",
    "assign": vscode2.insert_padded(" = "),
    "double compare": vscode2.insert_padded(" == "),
    "compare": vscode2.insert_padded(" === "),
    "double contrast": vscode2.insert_padded(" != "),
    "contrast": vscode2.insert_padded(" !== "),
    "stand": vscode2.insert_padded(" && "),
    "store": vscode2.insert_padded(" || "),
    "not": "!",
    "true": "true",
    "false": "false",
    "null": "null",
    "undefined": "undefined",
    "document": "document",
    "await": vscode2.insert_padded("await "),
    "a sink": vscode2.insert_padded("async "),
    "new": vscode2.insert_padded("new "),
    "return": vscode2.insert_padded("return "),
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
    "define constructor": "constructor",
    "just number": "number",
    "just string": "string",
    "import state": 'import  from "";{left:9}',
    "import": vscode2.insert_padded("import "),
    "document": "document",
    "this": "this",
}

extras = [Choice("functions", functions), Choice("namespaces", namespaces)]
utils.load_commands(contexts.javascript, commands=mapping, extras=extras)
