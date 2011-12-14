#!/usr/bin/env python
from unittest import TestCase, main

from pset import PSetBase, PCSet, PSet
import utils


"""Test pc and set methods"""
class PCSetifyTests(TestCase):
    """Test pcs, pc_sets, _setify, unique_pcs and related methods"""

    def setUp(self):        
        self.pcset = PCSet(22, 3, 5, -7, 0, 10)

    def testPc(self):
        pcs = [pitch % self.pcset._mod for pitch in self.pcset.pitches]
        self.assertEqual(self.pcset.pcs, pcs)

    def testPc_set(self):
        self.assertEqual(self.pcset.pc_set, set([0, 3, 5, 10]))

    def testCardinality(self):
        self.assertEqual(self.pcset.cardinality, 4)

    def testPitch_set(self):
        self.assertEqual(self.pcset.pitch_set, set([22, 3, 5, -7, 0, 10]))

    def testUo_pcs(self):
        self.assertEqual(self.pcset.uo_pcs, [0, 3, 5, 5, 10, 10])

    def testUnique_pcs(self):
        self.assertEqual(self.pcset.unique_pcs, [0, 3, 5, 10])


"""Test Tn TnI TnMm operations"""
class VarEqualsTnTm(TestCase):
    """operations that return a PCSet or PSet"""

    def setUp(self):
        self.l = [0, 2, 5, 20, -1]
        self.pcset = PCSet(self.l)
        self.pset = PSet(self.l)

    def testTranspose(self):
        a = self.pcset.transpose(5)
        self.assertEqual(a.pitches, [5, 7, 10, 25, 4])
        self.assertEqual(a.uo_pcs, [1, 4, 5, 7, 10])
        self.assertEqual(a.__class__, PCSet)
        b = self.pset.transpose(5)
        self.assertEqual(b.pitches, [5, 7, 10, 25, 4])
        self.assertEqual(b.__class__, PSet)

    def testInvert(self):
        a = self.pcset.invert()
        self.assertEqual(a.pitches, [0, -2, -5, -20, 1])
        self.assertEqual(a.uo_pcs, [0, 1, 4, 7, 10])
        self.assertEqual(a.__class__, PCSet)
        b = self.pset.invert(3)
        self.assertEqual(b.pitches, [3, 1, -2, -17, 4])
        self.assertEqual(b.__class__, PSet)

    def testMultiply(self):
        a = self.pcset.multiply()
        b = self.pcset.multiply(7)
        self.assertEqual(a.pcs, [0, 10, 1, 4, 7])
        self.assertEqual(a.__class__, PCSet)
        self.assertEqual(b.pcs, [0, 2, 11, 8, 5])

    def testTranspose_multiply(self):
        a = self.pcset.transpose_multiply(1, 11)
        b = self.pset.transpose_multiply(5, 5)
        c = self.pset.transpose_multiply(0, 5)
        d = self.pcset.transpose_multiply(1, 1)
        self.assertEqual(a, a.transpose_multiply(0, 1))
        self.assertEqual(a.multiply(), a.transpose_multiply())
        self.assertEqual(a.pcs, [1, 11, 8, 5, 2])
        self.assertEqual(b.pcs, [5, 3, 6, 9, 0])
        self.assertEqual(c.pcs, self.pcset.multiply())
        self.assertEqual(d, self.pcset.transpose(1))


class TnTmInPlace(TestCase):
    """operations that change a PCSet/PSet in place via TnTm"""

    def setUp(self):
        self.l = [0, -15, 20, 4, 2, 0]
        self.a = PCSet(self.l, multiset=True)
        self.b = self.a.copy()
        self.c = self.a.copy()

    def testT(self):
        a = self.a
        b = self.b
        a.t(5)
        b.t(-2)
        self.assertEqual(a.pitches, [5, -10, 25, 9, 7, 5])
        self.assertEqual(b.pitches, [-2, -17, 18, 2, 0, -2])

    def testI(self):
        a = self.a
        b = self.b
        c = self.c
        a.i()
        b.i()
        c.i(3)
        self.assertEqual(a.pitches, [0, 15, -20, -4, -2, 0])
        self.assertEqual(a, b.pcs)
        self.assertEqual(b.pitches, a.pitches)
        self.assertEqual(c.pitches, [3, 18, -17, -1, 1, 3])

    def testM(self):
        a = self.a
        b = self.b
        a.m()
        b.m(3)
        self.assertEqual(a.unique_pcs, [0, 4, 8, 9, 10])
        self.assertEqual(b.unique_pcs, [0, 1, 3, 7, 11])

    def testMi(self):
        a = self.a
        b = self.b
        c = self.c
        a.mi()
        b.m()
        b.i()
        c.mi(5)
        self.assertEqual(a.unique_pcs, [0, 2, 3, 4, 8])
        self.assertEqual(a, b)
        self.assertEqual(c.unique_pcs, [1, 5, 7, 8, 9])

    def testTm(self):
        a = self.a
        b = a.copy()
        c = b.copy()
        a.t_m(0, 1)
        b.t_m(1, 5)
        c.t_m(5, -1)
        self.assertEqual(a.unique_pcs, [0, 2, 4, 8, 9])
        self.assertEqual(b.unique_pcs, [1, 5, 9, 10, 11])
        self.assertEqual(c.unique_pcs, [1, 3, 5, 8, 9])


class BinIntTest(TestCase):
    """Functions that convert PCSets to integers and vice versa"""

    def setUp(self):
        self.pcset = PCSet(1, 4)
        self.pcset2 = PCSet(0, 3, 4, 6)

    def testSetInt(self):
        self.assertEqual(self.pcset.setint(), 18)
        self.assertEqual(self.pcset2.setint(), 89)

    def testMaxDigit(self):
        self.assertEqual(utils._max_digit(4095), 12)
        self.assertEqual(utils._max_digit(0), 1)
        self.assertEqual(utils._max_digit(25), 5)

    def testFromInt(self):
        self.assertEqual(utils.fromint(18), self.pcset.unique_pcs)
        self.assertEqual(utils.fromint(89), self.pcset2.unique_pcs)


class EachTest(TestCase):
    """Methods that provide each n in the modulus or each set in the modulus"""

    def setUp(self):
        self.pcset = PCSet()

    def testEach_n(self):
        self.pcset.mod(12)
        self.assertEqual(list(self.pcset.each_n()),
                         [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11])
        self.pcset.mod(6)
        self.assertEqual(list(self.pcset.each_n()),[0, 1, 2, 3, 4, 5])

    def testEach_set(self):
        self.pcset.mod(12)
        each_set = list(self.pcset.each_set())
        self.assertEqual(each_set[0:6], [[], [0], [1], [0, 1], [2], [0, 2]])
        self.assertEqual(each_set[-1],
                         [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11])
        for index, each in enumerate(each_set):
            self.assertEqual(utils.setint(each), index)
        self.pcset.mod(4)
        each_set = list(self.pcset.each_set())
        self.assertEqual(each_set[0:3], [[], [0], [1]])
        self.assertEqual(each_set[-1], [0, 1, 2, 3])
