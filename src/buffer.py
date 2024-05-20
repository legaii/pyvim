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
