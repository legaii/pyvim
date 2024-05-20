def is_not_space(char):
    return not char.isspace()


class Buffer:
    def __init__(self):
        self.content = ['']
        self.current_line = 0
        self.current_char = 0


    def read_from(self, path):
        with open(path, 'r') as file:
            self.content = file.read().split('\n')


    def write_to(self, path):
        with open(path, 'w') as file:
            file.write('\n'.join(content))


    def adjust_pos(self):
        if self.current_line < 0:
            self.current_line = 0
        elif self.current_line >= len(self.content):
            self.current_line = len(self.content) - 1
        if self.current_char < 0:
            self.current_char = 0
        elif self.current_char > len(self.content[self.current_line]):
            self.current_char = len(self.content[self.current_line])


    def move_line(self, delta):
        self.current_line += delta
        self.adjust_pos()


    def move_char(self, delta):
        self.current_char += delta
        self.adjust_pos()


    def is_end_of_line(self):
        return self.current_char == len(self.content[self.current_line])


    def check_under_cursor(self, predicate):
        return (
            not self.is_end_of_line()
            and predicate(self.content[self.current_line][self.current_char])
        )


    def go_forward(self):
        if self.is_end_of_line():
            if self.current_line == len(self.content) - 1:
                return False
            self.current_line += 1
            self.current_char = 0
        else:
            self.current_char += 1
        return True


    def go_backward(self):
        if self.current_char == 0:
            if self.current_line == 0:
                return False
            self.current_line -= 1
            self.current_char = len(self.content[self.current_line])
        else:
            self.current_char -= 1
        return True


    def go_to_next_word(self):
        while self.check_under_cursor(is_not_space):
            if not self.go_forward():
                break
        while not self.check_under_cursor(is_not_space):
            if not self.go_forward():
                break


    def go_to_prev_word(self):
        while self.check_under_cursor(is_not_space):
            if not self.go_backward():
                break
        while not self.check_under_cursor(is_not_space):
            if not self.go_backward():
                break


    def go_to_line_begin(self):
        self.current_char = 0


    def go_to_line_end(self):
        self.current_char = len(self.content[self.current_line])


    def insert(self, char):
        cur_line = self.content[self.current_line]
        self.content[self.current_line] = (
            cur_line[:self.current_char] + char + cur_line[self.current_char:]
        )
        self.current_char += 1


    def insert_new_line(self):
        cur_line = self.content[self.current_line]
        self.content = self.content[:self.current_line] + [
            cur_line[:self.current_char], cur_line[self.current_char:]
        ] + self.content[self.current_line + 1:]
        self.current_line += 1
        self.current_char = 0


    def delete_char(self):
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


    def draw(self, window, lines_cnt, cols_cnt):
        window_lines = []
        for line in self.content:
            for block_begin in range(0, len(line) if len(line) > 0 else 1, cols_cnt):
                window_lines.append(line[block_begin : block_begin + cols_cnt])
                if len(window_lines) == lines_cnt:
                    break
            if len(window_lines) == lines_cnt:
                break
        window_lines += [''] * (lines_cnt - len(window_lines))
        for y_pos, line in enumerate(window_lines):
            window.addstr(y_pos, 0, line.ljust(cols_cnt))
        window.move(self.current_line, self.current_char)
