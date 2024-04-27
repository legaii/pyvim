from mode import Mode
from buffer import Buffer


class AppState:
    def __init__(self):
        self.running = True
        self.mode = Mode.normal_mode()
        self.buffer = Buffer()


    def draw(self, lines_cnt, cols_cnt):
        lines, cursor_y, cursor_x = self.buffer.draw(lines_cnt - 1, cols_cnt)
        lines.append(self.mode.draw())
        return lines, cursor_y, cursor_x
