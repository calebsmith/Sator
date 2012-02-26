#!/usr/bin/env python
from unittest import TestCase, main

from sator.core import PCSet, PSet
import sator.utils as utils


"""Test pc and set methods"""
class PCSetifyTests(TestCase):
    """Test pcs, _pc_sets, _setify, _unique_pcs and related methods"""

    def setUp(self):        
        self.pcset = PCSet(22, 3, 5, -7, 0, 10)

    def testPc(self):
        pcs = [pitch % self.pcset._mod for pitch in self.pcset.pitches]
        self.assertEqual(self.pcset.pcs, pcs)

    def testPc_set(self):
        self.assertEqual(self.pcset._pc_set, set([0, 3, 5, 10]))

    def testCardinality(self):
        self.assertEqual(self.pcset.cardinality, 4)

    def testPitch_set(self):
        self.assertEqual(self.pcset._pitch_set, set([22, 3, 5, -7, 0, 10]))

    def testUo_pcs(self):
        self.assertEqual(self.pcset.uo_pcs, [0, 3, 5, 5, 10, 10])

    def testUnique_pcs(self):
        self.assertEqual(self.pcset._unique_pcs, [0, 3, 5, 10])


"""Test Tn TnI TnMm operations"""
class VarEqualsTnTm(TestCase):
    """operations that return a PCSet or PSet"""

    def setUp(self):
        self.l = [0, 2, 5, 20, -1]
        self.pcset = PCSet(self.l)
        self.pset = PSet(self.l)

    def testTranspose(self):
        a = self.pcset._transpose(5)
        self.assertEqual(a.pitches, [5, 7, 10, 25, 4])
        self.assertEqual(a.uo_pcs, [1, 4, 5, 7, 10])
        self.assertEqual(a.__class__, PCSet)
        b = self.pset._transpose(5)
        self.assertEqual(b.pitches, [5, 7, 10, 25, 4])
        self.assertEqual(b.__class__, PSet)

    def testInvert(self):
        a = self.pcset._invert()
        self.assertEqual(a.pitches, [0, -2, -5, -20, 1])
        self.assertEqual(a.uo_pcs, [0, 1, 4, 7, 10])
        self.assertEqual(a.__class__, PCSet)
        b = self.pset._invert(3)
        self.assertEqual(b.pitches, [3, 1, -2, -17, 4])
        self.assertEqual(b.__class__, PSet)

    def testTranspose_multiply(self):
        a = self.pcset._transpose_multiply(1, 11)
        b = self.pset._transpose_multiply(5, 5)
        c = self.pset._transpose_multiply(0, 5)
        d = self.pcset._transpose_multiply(1, 1)
        self.assertEqual(a, a._transpose_multiply(0, 1))
        self.assertEqual(a.pcs, [1, 11, 8, 5, 2])
        self.assertEqual(b.pcs, [5, 3, 6, 9, 0])
        self.assertEqual(c.pcs, self.pcset._transpose_multiply())
        self.assertEqual(d, self.pcset._transpose(1))


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
        self.assertEqual(a._unique_pcs, [0, 4, 8, 9, 10])
        self.assertEqual(b._unique_pcs, [0, 1, 3, 7, 11])

    def testMi(self):
        a = self.a
        b = self.b
        c = self.c
        a.mi()
        b.m()
        b.i()
        c.mi(5)
        self.assertEqual(a._unique_pcs, [0, 2, 3, 4, 8])
        self.assertEqual(a, b)
        self.assertEqual(c._unique_pcs, [1, 5, 7, 8, 9])

    def testTm(self):
        a = self.a
        b = a.copy()
        c = b.copy()
        a.t_m(0, 1)
        b.t_m(1, 5)
        c.t_m(5, -1)
        self.assertEqual(a._unique_pcs, [0, 2, 4, 8, 9])
        self.assertEqual(b._unique_pcs, [1, 5, 9, 10, 11])
        self.assertEqual(c._unique_pcs, [1, 3, 5, 8, 9])


class BinIntTest(TestCase):
    """Functions that convert PCSets to integers and vice versa"""

    def setUp(self):
        self.pcset = PCSet(1, 4)
        self.pcset2 = PCSet(0, 3, 4, 6)

    def testSetInt(self):
        self.assertEqual(self.pcset.setint, 18)
        self.assertEqual(self.pcset2.setint, 89)

    def testFromInt(self):
        self.assertEqual(utils.fromint(18), self.pcset._unique_pcs)
        self.assertEqual(utils.fromint(89), self.pcset2._unique_pcs)

    def testNewFromInt(self):
        """Using fromint staticmethod to create new PCSets"""
        a = PCSet.fromint(5)
        self.assertEqual(a, [0, 2])
        b = PCSet.fromint(630, 7)
        self.assertEqual(b, [1, 2, 4, 5, 6])


class VectorPropertyTest(TestCase):
    def testInvarianceVector(self):
        a = PCSet(0, 2, 4, 6, 8, 10)
        inv_vector = a.invariance_vector
        for m in (1, -1, 5, 7):
            for n in (0, 2, 4, 6, 8, 10):
                inv_vector.remove((n, m))
        self.assertEqual(inv_vector, [])
        self.assertEqual(PCSet(0, 6, 7, 8).invariance_vector, [(0, 1)])

    def testDS(self):
        self.assertEqual([tri.ds for tri in PCSet.each_prime_in_card_mod(3, 12)], [
            2, 1, 1, 1, 1, 2, 1, 1, 2, 2, 1, 6
        ])

    def testMVector(self):
        for each in PCSet.each_prime_in_card_mod(3, 12):
            m_vector = each.m_vector(2)
            m_vector = [vect[1] for vect in m_vector]
            self.assertEqual(each.icv[1:], m_vector)


class PSetPropertyTest(TestCase):

    def setUp(self):
        self.a = PSet(0, 4, 7, ordered=True, multiset=True)

    def testroot_obvious(self):
        a = PSet(0, 3, 7)
        for tn in a.t_rotations:
            self.assertEqual(tn.root, [tn[0]])
        a = PSet(0, 4, 7)
        for tn in a.t_rotations:
            self.assertEqual(tn.root, [tn[0]])

    def testroot_many(self):
        self.assertEqual(PSet(0, 3, 6, 9).root, [0, 3, 6, 9])
        self.assertEqual(PSet(-4, 0, 4).root, [-4, 0, 4])
        self.assertEqual(PSet(0, 2, 7).root, [0, 7])

    def testroot_order_invariant(self):
        # With major/minor triads, order is irrelavant
        for perm in PSet(0, 3, 7).each_permutation():
            self.assertEqual(perm.root, [0])
        for perm in PSet(0, 4, 7).each_permutation():
            self.assertEqual(perm.root, [0])
        # Voicing should also be irrelavent
        self.assertEqual(PSet(4, 7, 12, ordered=True).root, [12])
        self.assertEqual(PSet(7, 0, -9, ordered=True).root, [0])
        self.assertEqual(PSet(-8, 12, -5, ordered=True).root, [12])

    def testroot_order_variance(self):
        self.assertEqual(PSet(0, 7, 9, 14, ordered=True).root, [14])
        self.assertEqual(PSet(2, 9, 12, 19, ordered=True).root, [12, 19])


class PCSetPropertyTest(TestCase):

    def setUp(self):
        self.a = PCSet([0, 2, 5, 7])
        self.b = PCSet([5, 7, 8])
        self.c = PCSet([1, 3, 4])

    def testUnion(self):
        self.assertEqual(self.a + self.c, self.a.union(self.c))

    def testDifference(self):
        self.assertEqual(self.a - self.b, self.a.difference(self.b))

    def testSymmetricDifference(self):
        self.assertEqual(self.a.symmetric_difference(self.b), PCSet([0, 2, 8]))

    def testIntersection(self):
        self.assertEqual(PCSet([5, 7]), self.a.intersection(self.b))

    def testSymDiffIntersectionUnion(self):
        sym_diff = self.a.symmetric_difference(self.b)
        intersection = self.a.intersection(self.b)
        self.assertEqual(sym_diff + intersection, self.a.union(self.b))

    def testIsSubset(self):
        self.assertTrue(self.a.issubset([0,2,5,7,8,9]))
        self.assertFalse(self.a.issubset([0, 2]))

    def testIsSuperset(self):
        self.assertTrue(self.a.issuperset([5,7]))
        self.assertFalse(self.a.issuperset(self.c))

    def testIsDisjoint(self):
        self.assertTrue(self.a.isdisjoint(self.a.literal_compliment))
        self.assertTrue(self.a.isdisjoint(self.c))
        self.assertFalse(self.a.isdisjoint(self.b))


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
        self.assertEqual(list(self.pcset.each_n()),
                         list(PCSet.each_n_in_mod(6)))

    def testEach_set(self):
        self.pcset.mod(12)
        each_set = list(self.pcset.each_set())
        self.assertEqual(each_set[0:6], [[], [0], [1], [0, 1], [2], [0, 2]])
        self.assertEqual(each_set[-1],
                         [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11])
        self.assertEqual(each_set, list(PCSet.each_set_in_mod(12)))
        for index, each in enumerate(each_set):
            self.assertEqual(utils.setint(each), index)
        self.pcset.mod(4)
        each_set = list(self.pcset.each_set())
        self.assertEqual(each_set[0:3], [[], [0], [1]])
        self.assertEqual(each_set[-1], [0, 1, 2, 3])

    def testEach_set_in_mod(self):
        for each in PCSet.each_set_in_mod(10):
            self.assertEqual(each.mod(), 10)
        self.assertEqual(each, list(xrange(0, 10)))

    def testEach_tto(self):
        def check_each_tto(mod):
            a = PCSet(0, 3, mod=mod)
            ttos = list(a.each_tto())
            index = 0
            for m in (1, -1, 5, mod - 5):
                for n in xrange(0, mod):
                    self.assertEqual(ttos[index], (n, m))
                    index += 1  
        check_each_tto(12)
        check_each_tto(7)
        check_each_tto(15)

    def testEach_card(self):
        card = 2
        mod = 13
        a = PCSet(range(0, card), mod=mod)
        aggregate = PCSet(range(0, mod), mod=mod)
        for each, each_static in zip(a.each_card(), PCSet.each_card_in_mod(card, mod)):
            self.assertEqual(each.cardinality, card)
            self.assertEqual(each.mod(), mod)
            self.assertEqual(each._pc_set.issubset(aggregate), True)

    def testEach_prime_in_card_mod(self):
        trichords = [
            [0, 1, 2],
            [0, 1, 3],
            [0, 1, 4],
            [0, 1, 5],
            [0, 1, 6],
            [0, 2, 4],
            [0, 2, 5],
            [0, 2, 6],
            [0, 2, 7],
            [0, 3, 6],
            [0, 3, 7],
            [0, 4, 8],
        ]
        for each in PCSet.each_prime_in_card_mod(3, 13):
            self.assertEqual(each.mod(), 13)
            trichords.remove(each)
        self.assertEqual(trichords, [])
