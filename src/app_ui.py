import curses

from .key_bindings import KeyBinding, ESCAPE
from .app_state import AppState
from .mode import Mode


class AppUI:
    """Класс для взаимодействия между пользователем и AppState"""

    def __init__(self,
        window: curses.window, lines_cnt: int, cols_cnt: int,
        file: int, key_bindings: list[KeyBinding]
    ):
        self.window = window
        self.lines_cnt = lines_cnt
        self.cols_cnt = cols_cnt
        self.state = AppState(file)
        self.key_binding_prefix = ""
        self.key_bindings = key_bindings


    @staticmethod
    def transform_key(key: str):
        """Функция, преобразующая нестандартный ввод от пользователя в более удобный вид"""
        return {
            curses.KEY_ENTER: '\n',
            curses.KEY_BREAK: '\n',
            curses.KEY_BACKSPACE: '\b',
            curses.KEY_LEFT: 'h',
            curses.KEY_DOWN: 'j',
            curses.KEY_UP: 'k',
            curses.KEY_RIGHT: 'l',
            'KEY_ENTER': '\n',
            'KEY_BREAK': '\n',
            'KEY_BACKSPACE': '\b',
            'KEY_LEFT': 'h',
            'KEY_DOWN': 'j',
            'KEY_UP': 'k',
            'KEY_RIGHT': 'l',
            '\r': '\n',
        }.get(key, key)


    def run(self):
        """Функция отлавливает нажатия по клавиатуре и обновляет окно приложения"""
        while self.state.mode != Mode.quit_mode():
            self.redraw()
            key = self.transform_key(self.window.getkey())
            if key.isprintable() or key in ('\n', '\b', ESCAPE):
                self.read_char(key)


    def read_char(self, char: str):
        """Функция обрабатывает символ char, введенный с клавиатуры"""
        self.key_binding_prefix += char
        for key_binding in self.key_bindings:
            if key_binding.check(self.key_binding_prefix, self.state):
                self.key_binding_prefix = ""
                break


    def redraw(self):
        """Функция с нуля перерисовывает текстовое окно приложения"""
        status_line = self.key_binding_prefix
        mode_line = self.state.mode.draw()
        status_line += ' ' * (self.cols_cnt - len(status_line) - len(mode_line))
        status_line += mode_line
        status_line = status_line.replace('\n', '')
        self.window.addstr(self.lines_cnt - 1, 0, status_line, curses.A_BOLD)
        self.state.buffer.draw(self.window, self.lines_cnt - 1, self.cols_cnt)
        self.window.refresh()
