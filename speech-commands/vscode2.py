import time
import string
import tempfile
import threading
import re
import os
import os.path
import keyboard
import uuid
import json
import contexts
import queue
import dragonfly as df
import utils
import vscode_utils
from breathe import Breathe
from srabuilder.actions import surround, between
from srabuilder import rules
from typing import List, Dict, Any

RPC_INPUT_FILE = os.path.join(tempfile.gettempdir(), "speech-commands-input.json")
RPC_OUTPUT_FILE = os.path.join(tempfile.gettempdir(), "speech-commands-output.json")
RESPONSES_DICT: Dict[str, Any] = {}


def watch_output_file():
    prev_stamp = 0
    while True:
        stamp = os.stat(RPC_OUTPUT_FILE).st_mtime
        if stamp != prev_stamp:
            with open(RPC_OUTPUT_FILE) as f:
                text = f.read()
                try:
                    resp = json.loads(text)
                except json.decoder.JSONDecodeError:
                    pass
                else:
                    RESPONSES_DICT[resp["id"]] = (resp, stamp)
            prev_stamp = stamp
        time.sleep(0.01)


threading.Thread(target=watch_output_file, daemon=True).start()


def smart_action_text(**kw):
    params = {
        'target': {
            "pattern": re.escape(kw['all_chars']), 
            "count": kw.get('digits', 1)
        },
        'direction': 'backwards' if 'back' in kw['_node'].words() else 'forwards'
    }
    action = kw['action']
    if action in ("start", "end"):
        params['target']['side'] = action
        action = "move"
    return smart_action_request(action, params)

def smart_action(**kw):
    get_every = 'every' in kw['_node'].words()
    node = kw['node']
    params = {
        'target': {"selector": node, 'getEvery': get_every},
        'direction': kw.get('direction', 'smart')
    }
    action = kw['action']
    if action in ("start", "end"):
        params['target']['side'] = action
        action = "move"
    return smart_action_request(action, params)

def smart_action_request(action: str, params: Dict):
    assert "action" not in params
    return send_request("SMART_ACTION", {**params, "action": action})

def select_node(pattern: str | List[str], direction: str, select_type: str, on_done: str):
    params = {
        "pattern": pattern,
        "direction": direction,
        "count": 1,
        "selectType": select_type,
        "onDone": on_done,
    }
    send_request("SELECT_NODE", params)


def format_request(method: str, params=None) -> dict:
    request_id = str(uuid.uuid4())
    request = {"jsonrpc": "2.0", "id": request_id, "method": method}
    if params:
        request["params"] = params
    return request


def send_request(method: str, params=None):
    request = format_request(method, params)
    request_id = request["id"]
    with open(RPC_INPUT_FILE, "w") as f:
        json.dump(request, f)
    return get_response(request_id)


def get_response(request_id: str):
    val = RESPONSES_DICT.get(request_id)
    start_time = time.time()
    while True:
        curr_time = time.time()
        val = RESPONSES_DICT.get(request_id)
        if val is not None:
            break
        if curr_time - start_time > 5:
            raise TimeoutError
        time.sleep(0.01)
    try:
        del RESPONSES_DICT[request_id]
    except KeyError:
        pass
    resp, _ = val
    return resp


def move_until(char: str, count: int, include_pattern=False, reverse=False, move=False):
    char = re.escape(char)
    params = {
        "count": count,
        "pattern": char,
        "isPatternInclude": include_pattern,
        "reverse": reverse,
        "isMove": move,
    }
    resp = send_request("SELECT_UNTIL_PATTERN", params=params)


def select_balanced(left: str, right: str, count: int, include_pattern=False, reverse=False, move=False):
    left = re.escape(left)
    right = re.escape(right)
    params = {
        "count": count,
        "left": left,
        "right": right,
        "isPatternInclude": include_pattern,
    }
    send_request("SELECT_IN_SURROUND", params=params)


def go_to_line(line: int):
    send_request("GO_TO_LINE", params={"line": line - 1})


def execute_command(command: str, *args):
    params = {"command": command, "args": args}
    send_request("EXECUTE_COMMAND", params=params)


cmds = {
    "[<digits>] take parentheses": df.Function(lambda **kw: select_balanced("(", ")", count=int(kw["digits"]))),
    "[<digits>] [back] <action> <all_chars>": df.Function(smart_action_text),
    # "[<digits>] pre <all_chars>": df.Function(lambda **kw: move_until(kw["all_chars"], int(kw["digits"]), move=True)),
    # "[<digits>] take pre <all_chars>": df.Function(lambda **kw: move_until(kw["all_chars"], int(kw["digits"]))),
    # "[<digits>] post <all_chars>": df.Function(
    #     lambda **kw: move_until(kw["all_chars"], int(kw["digits"]), include_pattern=True, move=True)
    # ),
    # "[<digits>] take post <all_chars>": df.Function(
    #     lambda **kw: move_until(kw["all_chars"], int(kw["digits"]), include_pattern=True)
    # ),
    # "[<digits>] back post <all_chars>": df.Function(
    #     lambda **kw: move_until(kw["all_chars"], int(kw["digits"]), reverse=True, move=True)
    # ),
    # "[<digits>] take back post <all_chars>": df.Function(
    #     lambda **kw: move_until(kw["all_chars"], int(kw["digits"]), reverse=True)
    # ),
    # "[<digits>] back pre <all_chars>": df.Function(
    #     lambda **kw: move_until(
    #         kw["all_chars"],
    #         int(kw["digits"]),
    #         reverse=True,
    #         include_pattern=True,
    #         move=True,
    #     )
    # ),
    # "[<digits>] take back pre <all_chars>": df.Function(
    #     lambda **kw: move_until(kw["all_chars"], int(kw["digits"]), reverse=True, include_pattern=True)
    # ),
    "go <n>": df.Function(lambda **k: go_to_line(k["n"])),
}

actions = {
    # technically pre and post become move
    "pre": "start",
    "post": "end",
    "take": "select",
    "copy": "copy",
    "cut": "cut",
    "kill": "delete",
}




directions = {
    "previous": "backwards",
    "next": "forwards",
}


def smart_action_with_index_or_slice(kw, index_or_slice: str):
    kw['node'] = kw['format_node'].format(index_or_slice)
    del kw['format_node']
    return smart_action(**kw)


def create_format_map(nodes: Dict[str, str]) -> Dict[str, str]:
    str_formatter = string.Formatter()
    format_map: Dict[str, str] = {}
    for utterance, pattern in nodes.items():
        has_format_field = any((tup[1] == "0" for tup in str_formatter.parse(pattern)))
        pattern_with_format_field = pattern if has_format_field else pattern + "{0}"
        temp = pattern_with_format_field.replace("{0}", "temp-placeholder")
        temp = temp.replace("{", "{{").replace("}", "}}")
        pattern_with_format_field = temp.replace("temp-placeholder", "{0}")
        format_map[utterance] = pattern_with_format_field
    return format_map


def remove_fields(nodes: Dict[str, str]) -> None:
    removed_fields_map: Dict[str, str] = {}
    for utterance, pattern in nodes.items():
        pattern_with_removed_format_field = pattern.replace("{0}", "")
        removed_fields_map[utterance] = pattern_with_removed_format_field
    return removed_fields_map


def load_language_commands(context: df.Context, nodes: Dict[str, str]):
    format_nodes = create_format_map(nodes)
    removed_fields_map = remove_fields(nodes)
    commands = {
        "<action> [<direction>] <node>": smart_action,
        "<action> every [<direction>] <format_node>": df.Function(
            lambda **kw: smart_action_with_index_or_slice(kw, "[]")
        ),
    }
    extras = [
        df.Choice("action", actions),
        df.Choice("node", removed_fields_map),
        df.Choice("direction", directions),
        df.Choice("format_node", format_nodes),
    ]

    utils.load_commands(context, commands=commands, extras=extras)

utils.load_commands(
    contexts.vscode,
    commands=cmds,
    extras=[
        df.Choice("all_chars", {**keyboard.all_chars, **keyboard.digits}),
        df.Choice("digits", keyboard.digits),
        df.Choice("action", actions),
        df.Choice("direction", directions),
    ],
    defaults={"digits": 1},
)