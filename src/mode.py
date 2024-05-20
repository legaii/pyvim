class Mode:
    def __init__(self, mode_id):
        self.mode_id = mode_id


    def draw(self):
        if self.mode_id == 1:
            return '-- INSERT --'
        else:
            return ''


    def __eq__(self, other):
        return self.mode_id == other.mode_id


    @classmethod
    def normal_mode(cls):
        return cls(0)


    @classmethod
    def insert_mode(cls):
        return cls(1)


    @classmethod
    def quit_mode(cls):
        return cls(2)
