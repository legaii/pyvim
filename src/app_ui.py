import curses

from .app_state import AppState
from .mode import Mode


class AppUI:
    def __init__(self, window, lines_cnt, cols_cnt, key_bindings):
        self.window = window
        self.lines_cnt = lines_cnt
        self.cols_cnt = cols_cnt
        self.state = AppState()
        self.key_binding_prefix = ""
        self.key_bindings = key_bindings


    @staticmethod
    def transform_key(key):
        return {
            'KEY_BACKSPACE': '\b',
            'KEY_LEFT': 'h',
            'KEY_DOWN': 'j',
            'KEY_UP': 'k',
            'KEY_RIGHT': 'l',
        }.get(key, key)


    def run(self):
        while self.state.mode != Mode.quit_mode():
            self.redraw()
            key = self.transform_key(self.window.getkey())
            if len(key) == 1:
                self.read_char(key)


    def read_char(self, char):
        self.key_binding_prefix += char
        for key_binding in self.key_bindings:
            if key_binding.check(self.key_binding_prefix, self.state):
                self.key_binding_prefix = ""
                break


    def redraw(self):
        status_line = self.key_binding_prefix
        mode_line = self.state.mode.draw()
        status_line += ' ' * (self.cols_cnt - len(status_line) - len(mode_line))
        status_line += mode_line
        self.window.addstr(self.lines_cnt - 1, 0, status_line, curses.A_BOLD)
        self.state.buffer.draw(self.window, self.lines_cnt - 1, self.cols_cnt)
        self.window.refresh()
