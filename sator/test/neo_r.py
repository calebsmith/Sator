#!/usr/bin/env python
from unittest import TestCase, main

from sator.core import PCSet, PSet
import sator.utils


"""Test pc and set methods"""
class NeoRTest(TestCase):
    """Test pcs, _pc_sets, _setify, _unique_pcs and related methods"""

    def setUp(self):
        self.a = PSet(0, 4, 7, ordered=True, multiset=True)

    def testP(self):
        a = self.a
        # P() is an involution
        self.assertEqual(a.P().P(), a)
        # Mod 12 required
        try:
            a.mod(11)
            a.P()
        except a.Mod12Only:
            pass
        else:
            self.assertTrue(False)
        a.mod(12)
        self.assertEqual(a.P(), [0, 3, 7])
        self.assertEqual((a + [0, 4, 4, 0, 7]).P(), [0, 3, 7, 0, 3, 3, 0, 7])
        a.i(8)
        # a is Db major. a.P is Db minor
        self.assertEqual(a.P(), [8, 5, 1])

    def testR(self):
        a = self.a
        # R() is an involution
        self.assertEqual(a.R().R(), a)
        # Mod 12 required
        try:
            a.mod(11)
            a.R()
        except a.Mod12Only:
            pass
        else:
            self.assertTrue(False)
        a.mod(12)
        self.assertEqual(a.R(), [0, 4, 9])
        self.assertEqual((a + [0, 4, 4, 0, 7]).R(), [0, 4, 9, 0, 4, 4, 0, 9])
        a.i(1)
        # a is F# minor, a.R() is A major
        self.assertEqual(a.R(), [1, -3, -8])

    def testL(self):
        a = self.a
        # L() is an involution
        self.assertEqual(a.L().L(), a)
        # mod 12 required
        try:
            a.mod(11)
            a.L()
        except a.Mod12Only:
            pass
        else:
            self.assertTrue(False)
        a.mod(12)
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
