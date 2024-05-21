from .mode import Mode
from .buffer import Buffer


class AppState:
    def __init__(self, file):
        self.mode = Mode.normal_mode()
        self.file = file
        self.buffer = Buffer()
        self.search_string = ''
        self.read()


    def read(self):
        self.buffer.read_from(self.file)


    def write(self):
        self.buffer.write_to(self.file)
