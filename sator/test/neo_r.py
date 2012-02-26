#!/usr/bin/env python
import random
from unittest import TestCase, main

from sator.core import PCSet, PSet
import sator.utils


"""Test pc and set methods"""
class NeoRTest(TestCase):
    """Test pcs, _pc_sets, _setify, _unique_pcs and related methods"""

    def setUp(self):
        self.a = PSet(0, 4, 7, ordered=True, multiset=True)

    def testMod12Required(self):
        a = self.a.copy()
        a.mod(11)
        self.assertRaises(a.Mod12Only, a.P)
        self.assertRaises(a.Mod12Only, a.L)
        self.assertRaises(a.Mod12Only, a.R)

    def testP(self):
        a = self.a
        # P() is an involution
        self.assertEqual(a.P().P(), a)
        self.assertEqual(a.P(), [0, 3, 7])
        self.assertEqual((a + [0, 4, 4, 0, 7]).P(), [0, 3, 7, 0, 3, 3, 0, 7])
        a.i(8)
        # a is Db major. a.P is Db minor
        self.assertEqual(a.P(), [8, 5, 1])

    def testR(self):
        a = self.a
        # R() is an involution
        self.assertEqual(a.R().R(), a)
        self.assertEqual(a.R(), [0, 4, 9])
        self.assertEqual((a + [0, 4, 4, 0, 7]).R(), [0, 4, 9, 0, 4, 4, 0, 9])
        a.i(1)
        # a is F# minor, a.R() is A major
        self.assertEqual(a.R(), [1, -3, -8])

    def testL(self):
        a = self.a
        # L() is an involution
        self.assertEqual(a.L().L(), a)
        self.assertEqual(a.L(), [-1, 4, 7])
        self.assertEqual((a + [0, 4, 4, 0, 7]).L(), [-1, 4, 7, -1, 4, 4, -1, 7])
        a.i(5)
        # a is Bb minor, a.L() is Gb major
        self.assertEqual(a.L(), [6, 1, -2])

    def testN(self):
        self.assertEqual(self.a.N(), self.a.R().L().P())
        self.assertEqual(self.a.N().N(), self.a)

    def testS(self):
        self.assertEqual(self.a.S(), self.a.L().P().R())
        self.assertEqual(self.a.S().S(), self.a)

    def testH(self):
        self.assertEqual(self.a.H(), self.a.P().L().P())
        self.assertEqual(self.a.H(), self.a.L().P().L())
        self.assertEqual(self.a.H().H(), self.a)

    def testNeo(self):
        self.assertEqual(list(self.a.neo("PP")), [[0, 3, 7], [0, 4, 7]])
        self.assertEqual(list(self.a.neo("prL")),
                         [[0, 3, 7], [-2, 3, 7], [-2, 2, 7]]
        )
        self.assertEqual(list(self.a.neo("PP")), list(self.a.neo("PP")))

    def testNeoInvalid(self):
        self.assertEqual(list(self.a.neo("am")), [])
        self.assertEqual(list(self.a.neo("AmPl")), list(self.a.neo("pl")))

    def testCycle(self):
        self.assertEqual(list(self.a.cycle("pl")), [
            [0, 3, 7], [0, 3, 8], [-1, 3, 8], [-1, 4, 8], [-1, 4, 7], [0, 4, 7]
        ])
        self.assertEqual(list(self.a.cycle("pLr")), [
            [0, 3, 7], [0, 3, 8], [0, 5, 8], [0, 5, 9], [0, 4, 9], [0, 4, 7]
        ])

    def testCycleInvalid(self):
        self.assertEqual(list(self.a.cycle("foo")), [])
        self.assertEqual(list(self.a.cycle("fooL")), [[-1, 4, 7], [0, 4, 7]])

    def testTransform(self):
        # 'z' Added to make sure invalid names are ignored
        fs = ['p', 'l', 'r', 'h', 's', 'n', 'z']
        opers = ""
        while len(opers) < 10:
            opers += random.choice(fs)
            neos = list(self.a.neo(opers))
            if neos:
                self.assertEqual(neos[-1], self.a.transform(opers))

    def testPaths(self):
        self.assertEqual(set(self.a.paths(self.a)), set(['PP', 'LL', 'RR']))
        fs = ['p', 'l', 'r', 'z']
        opers = ""
        for n in xrange(0, random.randint(0, 10)):
            opers += random.choice(fs)
        paths = self.a.paths(self.a.transform(opers))
        path = random.choice(paths)
        self.assertEqual(self.a.transform(opers)._pc_set, self.a.transform(path)._pc_set)
        b = self.a.copy()
        b.i(random.randint(0, 12))
        self.assertTrue(self.a.paths(b))
        b.i(random.randint(0, 12))
        self.assertTrue(self.a.paths(b))

    def testPathsInvalid(self):
        b = PSet([0, 3, 4, 7]) # Two thirds present
        self.assertRaises(PSet.NotNeoR, self.a.paths, b)
