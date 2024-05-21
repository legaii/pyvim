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


def next_line_callback(app_state):
    app_state.buffer.move_line(1)


def prev_line_callback(app_state):
    app_state.buffer.move_line(-1)


def next_char_callback(app_state):
    app_state.buffer.move_char(1)


def prev_char_callback(app_state):
    app_state.buffer.move_char(-1)


def next_word_callback(app_state):
    app_state.buffer.go_to_next_word()


def prev_word_callback(app_state):
    app_state.buffer.go_to_prev_word()


def line_begin_callback(app_state):
    app_state.buffer.go_to_line_begin()


def line_end_callback(app_state):
    app_state.buffer.go_to_line_end()


def delete_line_callback(app_state):
    app_state.buffer.delete_line()


def delete_word_callback(app_state):
    app_state.buffer.delete_word()


def search_callback(app_state, search_string):
    app_state.search_string = search_string
    app_state.buffer.next_occurrence(search_string)


def next_occurrence_callback(app_state):
    app_state.buffer.next_occurrence(app_state.search_string)


ESCAPE = chr(27)

key_bindings = [
    KeyBinding(Mode.normal_mode(), re.compile('.*' + ESCAPE), lambda _: None),
    KeyBinding(Mode.normal_mode(), re.compile('i'), switch_to_insert_mode),
    KeyBinding(Mode.normal_mode(), re.compile('h'), prev_char_callback),
    KeyBinding(Mode.normal_mode(), re.compile('j'), next_line_callback),
    KeyBinding(Mode.normal_mode(), re.compile('k'), prev_line_callback),
    KeyBinding(Mode.normal_mode(), re.compile('l'), next_char_callback),
    KeyBinding(Mode.normal_mode(), re.compile('w'), next_word_callback),
    KeyBinding(Mode.normal_mode(), re.compile('b'), prev_word_callback),
    KeyBinding(Mode.normal_mode(), re.compile('0'), line_begin_callback),
    KeyBinding(Mode.normal_mode(), re.compile('dd'), delete_line_callback),
    KeyBinding(Mode.normal_mode(), re.compile('daw'), delete_word_callback),
    KeyBinding(Mode.normal_mode(), re.compile(r'\$'), line_end_callback),
    KeyBinding(Mode.normal_mode(), re.compile('/(.*)\n'), search_callback),
    KeyBinding(Mode.normal_mode(), re.compile('n'), next_occurrence_callback),
    KeyBinding(Mode.normal_mode(), re.compile(':q\n'), quit_callback),
    KeyBinding(Mode.normal_mode(), re.compile('\n'), lambda _: None),
    KeyBinding(Mode.insert_mode(), re.compile(ESCAPE), switch_to_normal_mode),
    KeyBinding(Mode.insert_mode(), re.compile('\b'), delete_char_callback),
    KeyBinding(Mode.insert_mode(), re.compile('\n'), insert_new_line_callback),
    KeyBinding(Mode.insert_mode(), re.compile('(.)'), insert_char_callback),
]
