#!/usr/bin/python

import getopt
import sys

from lib.ApkUtils import ApkUtils
from lib.BuildUtils import BuildUtils
from lib.ConfigExecutor import ConfigExecutor


class Player:
    builder = BuildUtils()
    config = ConfigExecutor()
    apkutils = ApkUtils

    def __init__(self):
        self.actions = {
            'update': self.builder.update,
            'genbuild': self.builder.generate_build,
            'release': self.builder.release,
            'clean': self.builder.clean,
            'config': self.config.parse_option,
            'sign': self.apkutils.options,
            'zipalign': self.apkutils.options,
            'jiagu': self.apkutils.options
        }
        return

    def play(self):
        opts, args = getopt.getopt(sys.argv[1:], 'a:p:c:s:d:')
        print opts
        if len(opts) == 0:
            self.help()

        for op, value in opts:
            if op == "-a":
                if ',' in value:
                    actions = value.split(',')
                else:
                    actions = [value]
                for a in actions:
                    if a in self.actions:
                        self.actions[a](opts)

    @staticmethod
    def help():
        print 'Play manual:'
        print '-a actions: '
        print ' update: update project with project.properties'
        print ' genbuild: generate build.xml with project.properties'
        print ' release: build release app'
        print ' clean: clean project'
        print '-p project path'
        print '-c path of configuration.json'


player = Player()
player.play()
