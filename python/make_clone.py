#!/usr/bin/python

from lib.ConfigExecutor import ConfigExecutor
import sys

if len(sys.argv) != 2:
    print 'Configuration file is in need!'
    exit(1)

executor = ConfigExecutor()
executor.parse(sys.argv[1])
