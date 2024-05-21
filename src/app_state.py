from .mode import Mode
from .buffer import Buffer


class AppState:
    """Класс для хранения всей информации, которая относится к состоянию приложения"""

    def __init__(self, file: str):
        self.mode = Mode.normal_mode()
        self.file = file
        self.buffer = Buffer()
        self.search_string = ''
        self.read()


    def read(self):
        """Считывает текст из текущего файла и записывает этот текст в буфер"""
        self.buffer.read_from(self.file)


    def write(self):
        """Записывает содержимое буфера в текущий файл"""
        self.buffer.write_to(self.file)
