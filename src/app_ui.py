from app_state import AppState


class AppUI:
    def __init__(self, window, lines_cnt, cols_cnt):
        self.window = window
        self.lines_cnt = lines_cnt
        self.cols_cnt = cols_cnt
        self.state = AppState()
        self.key_binding_prefix = ""
        self.key_bindings = []


    def run(self):
        running = True
        y = 0
        while running:
            key = self.window.getkey()
            if len(key) == 1:
                self.read_char(key)
                if not self.state.running:
                    running = False


    def read_char(self, char):
        if char == 'q':
            self.state.running = False
        self.redraw()


    def redraw(self):
        lines, cursor_y, cursor_x = self.state.draw(self.lines_cnt, self.cols_cnt)
        for i, line in enumerate(lines):
            self.window.addstr(i, 0, line)
        self.window.move(cursor_y, cursor_x)
        self.window.refresh()
