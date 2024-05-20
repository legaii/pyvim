from .mode import Mode
from .buffer import Buffer


class AppState:
    def __init__(self):
        self.mode = Mode.normal_mode()
        self.buffer = Buffer()
