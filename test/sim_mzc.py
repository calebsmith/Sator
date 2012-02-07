#!/usr/bin/env python
from unittest import TestCase, main

from core import PCSet, PSet
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

    def testIV(self):
        a = self.pcset
        b = self.pcset_z
        self.assertEqual(iv(a, b), [2, 2, 2, 2, 1, 2, 1, 3, 2, 1, 2, 4])

    def testSIM(self):
        a = self.pcset
        b = self.pcset_z
        self.assertEqual(sim(a, b), 9)

    def testASIM(self):
        a = self.pcset
        b = self.pcset_z
        self.assertEqual(asim(a, b, rational=True), (9, 21))

    def testcheckmod(self):
        a = self.pcset
        b = PCSet(0, 3, mod=7)
        self.assertEqual(iv(a, b), NotImplemented)
        self.assertEqual(sim(a, b), NotImplemented)
        self.assertEqual(asim(a, b), NotImplemented)
