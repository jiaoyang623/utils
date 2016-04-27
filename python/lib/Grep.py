# encoding=utf-8

import re
from lib.Base import Base


class Grep(Base):
    def replace(self, src, dst):
        self.content = self.content.replace(src, dst)
        return

    def replace_regex(self, src, dst):
        content_array = re.split(src, self.content, 65536, re.MULTILINE)
        self.content = dst.join(content_array)
        return

    def find(self, pattern):
        return re.findall(pattern, self.content, re.MULTILINE)

    def find(self, pattern, callback):
        content_array = self.content.split('\n')
        p = re.compile(pattern)
        for i in range(len(content_array)):
            line = content_array[i]
            result = p.findall(line)
            if len(result) > 0:
                content_array[i] = callback(line, result)
        self.content = '\n'.join(content_array)
