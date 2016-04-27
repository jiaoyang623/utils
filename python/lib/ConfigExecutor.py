# encoding=utf-8
import json
import os

from Utils import get_path
from lib.Grep import Grep


class ConfigExecutor(Grep):
    actions = []
    actions_replace = []
    groups = []
    seq = 1

    def __init__(self):
        self.actions = {
            'replace': self.action_replace,
            'delete': self.action_delete
        }

        self.actions_replace = {
            'replace': self.replace,
            'replace_regex': self.replace_regex,
            'replace_group': self.replace_group
        }
        return

    def make_group(self, line, groups):
        in_group = groups[0]
        output = ''
        for x in self.groups:
            if type(x) == int:
                output += in_group[x - 1]
            elif x == 'seq':
                output += str(self.seq)
            else:
                output += str(x)

        self.seq += 1
        return output

    def replace_group(self, src, dst):
        self.seq = 1
        self.groups = dst
        self.find(src, self.make_group)
        self.seq = 1
        return

    def action_replace(self, item):
        self.load(item['src'])

        [[self.actions_replace[key](obj['from'], obj['to']) for obj in item[key]]
         for key in item if key in self.actions_replace]

        self.save(item['dst'])
        return

    @staticmethod
    def action_delete(item):
        path = item['src']
        if os.path.exists(path):
            if os.path.isdir(path):
                os.rmdir(path)
            else:
                os.remove(path)
        return

    def action_change_script(self, item):
        self.load(item['src'])
        # clean comment

        self.save(item['dst'])

    # config need to be json string
    def parse(self, path):
        with open(path) as f:
            config_str = f.read()

        config = json.loads(config_str)

        for item in config:
            self.actions[item['action']](item)
        return

    def parse_option(self, opts):
        for op, value in opts:
            if '-c' == op:
                config_path = os.path.abspath(value)
        pwd = get_path(opts)

        if len(pwd) > 0:
            os.chdir(pwd)
        self.parse(config_path)
