#!/usr/bin/env python

import unittest, sys

from test import __all__ as alltests

class NoSuchTestError(Exception): pass

def match(name):
    if name not in alltests:
        raise NoSuchTestError, "Test '%s' not found." % name
    else:
        return name

def run(testnames, level=2):
    for name in testnames:
        if name:
            print "Testing Pyset module: %s" % name
            test = 'test.' + name
            suite = unittest.TestLoader().loadTestsFromName(test)
            unittest.TextTestRunner(verbosity=level).run(suite)

if __name__ == '__main__':
    args = sys.argv[1:]
    if args:
        tests = [match(name) for name in args]
        run(tests)
    else:
        run(alltests,level=1)
