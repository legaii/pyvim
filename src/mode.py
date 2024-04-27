class Mode:
    def __init__(self, mode_id):
        self.mode_id = mode_id


    def draw(self):
        if self.mode_id == 0:
            return ''
        elif self.mode_id == 1:
            return '-- INSERT --'


    @classmethod
    def normal_mode(cls):
        return cls(0)


    @classmethod
    def insert_mode(cls):
        return cls(1)


    @classmethod
    def command_mode(cls):
        return cls(2)
