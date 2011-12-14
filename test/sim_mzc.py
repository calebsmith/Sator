#!/usr/bin/env python
from unittest import TestCase, main

from pset import PCSet, PSet
from sim import *

class SimMZCTests(TestCase):        
    def setUp(self):
        self.l = [0, 1, 2, 4, 5, 8]
        self.pcset = PCSet(self.l)
        self.pcset_z = PCSet([0, 1, 3, 7])

    def testM(self):
        a = self.pcset
        b = a.mpartner
        self.assertTrue(m(a, b))
        b.t_m(3, -1)
        self.assertTrue(m(a, b))

    def testZ(self):
        a = self.pcset_z
        b = a.zpartner
        self.assertTrue(z(a, b))

    def testC(self):
        a = self.pcset
        b = a.abstract_compliment
        self.assertTrue(c(a, b))   


