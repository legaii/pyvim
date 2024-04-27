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


    def current_pos(self):
        return (self.current_line, self.current_char)


    def last_pos(self):
        return (len(self.content) - 1, len(self.content[-1]))


    def adjust_pos(self):
        if self.current_char < 0:
            self.current_char = 0


    def move_line(self, delta):
        self.current_line += delta
        self.adjust_pos()
