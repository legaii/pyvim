import re
from typing import Callable

from .mode import Mode
from .app_state import AppState


class KeyBinding:
    """Класс для хранения обработчика комбинации клавиш и условий, при котором этот обработчик вызывается"""

    def __init__(self, mode: Mode, pattern: re.Pattern, callback: Callable[[AppState, ...], None]):
        self.mode = mode
        self.pattern = pattern
        self.callback = callback


    def check(self, string: str, app_state: AppState):
        """Функция пытается обработать комбинацию клавиш string с помощью обработчика callback"""
        if app_state.mode != self.mode:
            return False
        pattern_match = self.pattern.match(string)
        if pattern_match is not None:
            self.callback(app_state, *pattern_match.groups())
            return True
        return False


def quit_callback(app_state: AppState):
    """Обработчки для выхода из приложения"""
    app_state.mode = Mode.quit_mode()


def read_file_callback(app_state: AppState, file: str):
    """Обработчик для чтения содержимого файла file"""
    app_state.file = file
    app_state.read()


def write_file_callback(app_state: AppState, file: str):
    """Обработчик для записи нового содержимого в файл file"""
    app_state.file = file
    app_state.write()


def switch_to_normal_mode(app_state: AppState):
    """Обработчик для перехода в режим NORMAL"""
    app_state.mode = Mode.normal_mode()


def switch_to_insert_mode(app_state: AppState):
    """Обработчик для перехода в режим INSERT"""
    app_state.mode = Mode.insert_mode()


def delete_char_callback(app_state: AppState):
    """Обработчик для удаления символа под курсором"""
    app_state.buffer.delete_char()


def insert_new_line_callback(app_state: AppState):
    """Обработчик для разделения текущей строчки на две"""
    app_state.buffer.insert_new_line()


def insert_char_callback(app_state: AppState, char: str):
    """Обработчик для вставки символа char"""
    app_state.buffer.insert(char)


def next_line_callback(app_state: AppState):
    """Обработчик для перемещения курсора на следующую строчку"""
    app_state.buffer.move_line(1)


def prev_line_callback(app_state: AppState):
    """Обработчик для перемещения курсора на предыдущую строчку"""
    app_state.buffer.move_line(-1)


def next_char_callback(app_state: AppState):
    """Обработчик для перемещения курсора на следующий символ"""
    app_state.buffer.move_char(1)


def prev_char_callback(app_state: AppState):
    """Обработчик для перемещения курсора на предыдущий символ"""
    app_state.buffer.move_char(-1)


def next_word_callback(app_state: AppState):
    """Обработчик для перемещения курсора на следующее слово"""
    app_state.buffer.go_to_next_word()


def prev_word_callback(app_state: AppState):
    """Обработчик для перемещения курсора на предыдущее слово"""
    app_state.buffer.go_to_prev_word()


def line_begin_callback(app_state: AppState):
    """Обработчик для перемещения курсора на начало текущей строчки"""
    app_state.buffer.go_to_line_begin()


def line_end_callback(app_state: AppState):
    """Обработчик для перемещения курсора на конец текущей строчки"""
    app_state.buffer.go_to_line_end()


def delete_line_callback(app_state: AppState):
    """Обработчик для удаления текущей строчки"""
    app_state.buffer.delete_line()


def delete_word_callback(app_state: AppState):
    """Обработчик для удаления текущего слова"""
    app_state.buffer.delete_word()


def search_callback(app_state: AppState, search_string: str):
    """Обработчик для поиска search_string в содержимом буфера"""
    app_state.search_string = search_string
    app_state.buffer.next_occurrence(search_string)


def next_occurrence_callback(app_state: AppState):
    """Обработчик для поиска следующего вхождения строки, которую пользователь искал в предыдущий раз"""
    app_state.buffer.next_occurrence(app_state.search_string)


ESCAPE = chr(27)

key_bindings = [
    KeyBinding(Mode.normal_mode(), re.compile('.*' + ESCAPE, re.DOTALL), lambda _: None),
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
    KeyBinding(Mode.normal_mode(), re.compile(':e (.*)\n'), read_file_callback),
    KeyBinding(Mode.normal_mode(), re.compile(':w\n'), AppState.write),
    KeyBinding(Mode.normal_mode(), re.compile(':w (.*)\n'), write_file_callback),
    KeyBinding(Mode.normal_mode(), re.compile('\b'), lambda _: None),
    KeyBinding(Mode.normal_mode(), re.compile('\n'), lambda _: None),
    KeyBinding(Mode.insert_mode(), re.compile(ESCAPE), switch_to_normal_mode),
    KeyBinding(Mode.insert_mode(), re.compile('\b'), delete_char_callback),
    KeyBinding(Mode.insert_mode(), re.compile('\n'), insert_new_line_callback),
    KeyBinding(Mode.insert_mode(), re.compile('(.)'), insert_char_callback),
]
