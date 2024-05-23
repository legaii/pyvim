import curses
from typing import Callable


def is_not_space(char: str):
    """Функция, проверяющая, является ли символ char пробельным символом"""
    return not char.isspace()


class Buffer:
    """Класс для хранения содержимого буфера и текущего положения курсора"""

    def __init__(self):
        self.content = ['']
        self.current_line = 0
        self.current_char = 0


    def read_from(self, path: str):
        """Считывает содержимое файла с путем path"""
        try:
            with open(path, 'r') as file:
                self.content = file.read().split('\n')
        except FileNotFoundError:
            pass


    def write_to(self, path: str):
        """Записывает (обновляет) содержимое файла с путем path"""
        with open(path, 'w') as file:
            file.write('\n'.join(self.content))


    def adjust_pos(self):
        """Эта функция сдвигает курсор к ближайшему корректному положению"""
        if self.current_line < 0:
            self.current_line = 0
            self.current_char = 0
            return
        if self.current_line >= len(self.content):
            self.current_line = len(self.content) - 1
            self.current_char = len(self.content[-1])
            return
        if self.current_char < 0:
            self.current_char = 0
        elif self.current_char > len(self.content[self.current_line]):
            self.current_char = len(self.content[self.current_line])


    def move_line(self, delta: int):
        """Перемещает курсор по оси y на delta"""
        self.current_line += delta
        self.adjust_pos()


    def move_char(self, delta: int):
        """Перемещает курсор по оси x на delta"""
        self.current_char += delta
        self.adjust_pos()


    def is_end_of_line(self):
        """Функция проверяет, стоит ли курсор на конце строчки"""
        return self.current_char == len(self.content[self.current_line])


    def check_under_cursor(self, predicate: Callable[[str], bool]):
        """Функция проверяет, что символ под курсором существует и удовлетворяет предикату predicate"""
        return (
            not self.is_end_of_line()
            and predicate(self.content[self.current_line][self.current_char])
        )


    def go_forward(self):
        """Функция сдвигает курсор на 1 символ вперед и возвращает False, если курсор достиг конца буфера"""
        if self.is_end_of_line():
            if self.current_line == len(self.content) - 1:
                return False
            self.current_line += 1
            self.current_char = 0
        else:
            self.current_char += 1
        return True


    def go_backward(self):
        """Функция сдвигает курсор на 1 символ назад и возвращает False, если курсор достиг начала буфера"""
        if self.current_char == 0:
            if self.current_line == 0:
                return False
            self.current_line -= 1
            self.current_char = len(self.content[self.current_line])
        else:
            self.current_char -= 1
        return True


    def go_to_next_word(self):
        """Функция перемещает курсор на начало следующего слова"""
        while self.check_under_cursor(is_not_space):
            self.go_forward()
        while not self.check_under_cursor(is_not_space):
            if not self.go_forward():
                break


    def go_to_prev_word(self):
        """Функция перемещает курсор на конец предыдущего слова"""
        while self.check_under_cursor(is_not_space):
            if not self.go_backward():
                break
        while not self.check_under_cursor(is_not_space):
            if not self.go_backward():
                break


    def go_to_line_begin(self):
        """Функция перемещает курсор на начало строчки"""
        self.current_char = 0


    def go_to_line_end(self):
        """Функция перемещает курсор на конец строчки"""
        self.current_char = len(self.content[self.current_line])


    def insert(self, char: str):
        """Функция вставляет под курсор символ char и сдвигает курсор на 1 символ вправо"""
        cur_line = self.content[self.current_line]
        self.content[self.current_line] = (
            cur_line[:self.current_char] + char + cur_line[self.current_char:]
        )
        self.current_char += 1


    def insert_new_line(self):
        """Функция делит текущую строчку на две"""
        cur_line = self.content[self.current_line]
        self.content = self.content[:self.current_line] + [
            cur_line[:self.current_char], cur_line[self.current_char:]
        ] + self.content[self.current_line + 1:]
        self.current_line += 1
        self.current_char = 0


    def delete_char(self):
        """Функция удаляет символ, предшествующий курсору"""
        if self.current_char == 0:
            if self.current_line > 0:
                self.current_line -= 1
                self.current_char = len(self.content[self.current_line])
                self.content = (
                    self.content[:self.current_line] +
                    [self.content[self.current_line] + self.content[self.current_line + 1]] +
                    self.content[self.current_line + 2:]
                )
        else:
            cur_line = self.content[self.current_line]
            self.current_char -= 1
            self.content[self.current_line] = (
                cur_line[:self.current_char] + cur_line[self.current_char + 1:]
            )


    def delete_word(self):
        """Функция удаляет слово под курсором"""
        if not self.check_under_cursor(is_not_space):
            return
        initial_pos = self.current_char
        while self.check_under_cursor(is_not_space):
            self.current_char += 1
        while self.check_under_cursor(str.isspace):
            self.current_char += 1
        right_pos = self.current_char
        self.current_char = initial_pos
        while self.current_char >= 0 and self.check_under_cursor(is_not_space):
            self.current_char -= 1
        self.current_char += 1
        cur_line = self.content[self.current_line]
        self.content[self.current_line] = (
            cur_line[:self.current_char] + cur_line[right_pos:]
        )


    def delete_line(self):
        """Функция удаляет текущую строчку"""
        self.content.pop(self.current_line)
        if len(self.content) == 0:
            self.content = ['']
        self.adjust_pos()


    def next_occurrence(self, search_string: str):
        """Функция перемещает курсор на начало следующего вхождения search_string в содержимое буфера"""
        substr_begin = self.content[self.current_line].find(search_string, self.current_char + 1)
        if substr_begin != -1:
            self.current_char = substr_begin
            return
        indexed_lines = list(enumerate(self.content))
        indexed_lines = indexed_lines[self.current_line + 1:] + indexed_lines[:self.current_line + 1]
        for line_index, line in indexed_lines:
            substr_begin = line.find(search_string)
            if substr_begin != -1:
                self.current_line = line_index
                self.current_char = substr_begin
                return


    def draw(self, window: curses.window, lines_cnt: int, cols_cnt: int):
        """Функция печатает содержимое буфера в текстовое окно высоты lines_cnt и ширины cols_cnt"""
        window_lines = []
        cursor_x = -1
        cursor_y = -1
        for line_index, line in enumerate(self.content):
            for block_begin in range(0, len(line) if len(line) > 0 else 1, cols_cnt):
                block_end = block_begin + cols_cnt
                if self.current_line == line_index and block_begin <= self.current_char < block_end:
                    cursor_x = self.current_char - block_begin
                    cursor_y = len(window_lines)
                window_lines.append(line[block_begin : block_end])
                if len(window_lines) == lines_cnt:
                    break
            if len(window_lines) == lines_cnt:
                break
        window_lines += [''] * (lines_cnt - len(window_lines))
        for y_pos, line in enumerate(window_lines):
            window.addstr(y_pos, 0, line.ljust(cols_cnt))
        if cursor_x >= 0 and cursor_y >= 0:
            window.move(cursor_y, cursor_x)
