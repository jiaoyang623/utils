# encoding=utf-8
from lib.Grep import Grep

grep = Grep()
grep.load('/opt/jenkins/workspace/360Video_trunk/trunk/360Video/project.properties')

grep.replace_regex('^#.*$', '')

grep.save('result.properties')
