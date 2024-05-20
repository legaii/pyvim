import re

from .mode import Mode


class KeyBinding:
    def __init__(self, mode, pattern, callback):
        self.mode = mode
        self.pattern = pattern
        self.callback = callback


    def check(self, string, app_state):
        if app_state.mode != self.mode:
            return False
        pattern_match = self.pattern.match(string)
        if pattern_match is not None:
            self.callback(app_state, *pattern_match.groups())
            return True
        return False


def quit_callback(app_state):
    app_state.mode = Mode.quit_mode()


def switch_to_normal_mode(app_state):
    app_state.mode = Mode.normal_mode()


def switch_to_insert_mode(app_state):
    app_state.mode = Mode.insert_mode()


def delete_char_callback(app_state):
    app_state.buffer.delete_char()


def insert_new_line_callback(app_state):
    app_state.buffer.insert_new_line()


def insert_char_callback(app_state, char):
    app_state.buffer.insert(char)


ESCAPE = chr(27)

key_bindings = [
    KeyBinding(Mode.normal_mode(), re.compile('.*' + ESCAPE), lambda _: None),
    KeyBinding(Mode.normal_mode(), re.compile('i'), switch_to_insert_mode),
    KeyBinding(Mode.normal_mode(), re.compile(':q\n'), quit_callback),
    KeyBinding(Mode.normal_mode(), re.compile('\n'), lambda _: None),
    KeyBinding(Mode.insert_mode(), re.compile(ESCAPE), switch_to_normal_mode),
    KeyBinding(Mode.insert_mode(), re.compile('\b'), delete_char_callback),
    KeyBinding(Mode.insert_mode(), re.compile('\n'), insert_new_line_callback),
    KeyBinding(Mode.insert_mode(), re.compile('(.)'), insert_char_callback),
]
