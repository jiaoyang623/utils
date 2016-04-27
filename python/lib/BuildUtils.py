import os
import re

from Utils import get_path


class BuildUtils:
    def __init__(self):
        return

    @staticmethod
    def get_projects(config_path):
        with open(config_path) as f:
            content = f.read()
        libs = re.findall(r'^android\.library\.reference\.\d+=(.+)$', content, re.MULTILINE)
        libs.append('../' + os.path.split(os.path.dirname(os.path.abspath(config_path)))[1])
        pwd = os.path.split(os.path.abspath(config_path))[0]
        libs = [os.path.abspath(pwd + '/' + p) for p in libs]
        return libs

    def update(self, opts):
        path = get_path(opts) + '/project.properties'
        if len(path) > 0:
            libs = self.get_projects(path)
            for lib in libs:
                os.system('svn up ' + lib)
        else:
            print 'need to specify the path of project.properties'
        return

    def generate_build(self, opts):
        path = get_path(opts) + '/project.properties'
        if len(path) > 0:
            libs = self.get_projects(path)
            for lib in libs:
                os.system('android update project -p %s -t android-22 -n %s --subprojects'
                          % (lib, lib[lib.rindex('/') + 1:]))
        else:
            print 'need to specify the path of project.properties'
        return

    @staticmethod
    def release(opts):
        path = get_path(opts)
        os.system('ant -f %s release' % path)
        return

    @staticmethod
    def clean(opts):
        path = get_path(opts)
        os.system('ant -f %s clean' % path)
