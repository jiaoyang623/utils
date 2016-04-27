# encoding=utf-8


class Base:
    content = ''

    def __init__(self):
        return

    def load(self, path):
        with open(path, 'r') as f:
            self.content = f.read().decode('utf-8')
        return

    def save(self, path):
        with open(path, 'w') as f:
            f.write(self.content.encode('utf-8'))
        return
