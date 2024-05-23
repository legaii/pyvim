class Mode:
    """Класс-enum с 3 режимами: NORMAL, INSERT и служебный режим QUIT"""

    def __init__(self, mode_id: int):
        self.mode_id = mode_id


    def draw(self):
        """Возвращает текстовое описание режима. Это описание можно отображать, например, в status line"""
        if self.mode_id == 1:
            return '-- INSERT --'
        else:
            return ''


    def __eq__(self, other):
        """Проверяет два режима на равенство"""
        return self.mode_id == other.mode_id


    @classmethod
    def normal_mode(cls):
        """Режим NORMAL"""
        return cls(0)


    @classmethod
    def insert_mode(cls):
        """Режим INSERT"""
        return cls(1)


    @classmethod
    def quit_mode(cls):
        """Служебный режим, во время которого приложение находится в процессе завершения"""
        return cls(2)
