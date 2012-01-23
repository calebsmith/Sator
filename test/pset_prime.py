#!/usr/bin/env python
from unittest import TestCase, main

from core import PCSet, PSet
import utils
from const import Z_PARTNERS

class PrimeTestCase(TestCase):        
    def setUp(self):
        self.l = [0, 1, 2, 3, 4, 6]
        self.set_ints = [0, 4095, 392, 661, 583, 203, 2741, 584, 394, 858]
        self.sets = [PCSet(utils.fromint(each)) for each in self.set_ints]
        self.pcset = PCSet(self.l)
        self.t_rots = list(self.pcset._t_rotations())
        self.i_rots = list(self.pcset._i_rotations())
        self.m_rots = list(self.pcset._m_rotations())
        self.mi_rots = list(self.pcset._mi_rotations())

"""Test prime and related subfunctions"""
class PrimeAndRotationsTest(PrimeTestCase):
    """Methods that generate lists of PCSets after TnTm operations"""

    def make_rotations(self):
        """Helper for checking ._rotations and ._rotation_ints"""
        self.t_only = [[self.pcset.uo_pcs]]
        self.m_only = self.t_only + [[self.pcset._transpose_multiply().uo_pcs]]
        self.i_only = self.t_only + [[self.pcset._invert().uo_pcs]]
        self.im_only = self.t_only + [[self.pcset._invert().uo_pcs]] + \
            [[self.pcset._transpose_multiply().uo_pcs]]
        self.ti_rots = [self.t_rots] + [self.i_rots]
        self.tm_rots = [self.t_rots] + [self.m_rots]
        self.im_rots = [self.i_rots] + [self.m_rots]
        self.all_rots = [self.t_rots] + [self.i_rots] + [self.m_rots] + \
            [self.mi_rots]

    def make_canons(self):    
        for canon_t in [True, False]:
            for canon_i in [True, False]:
                for canon_m in [True, False]:
                    yield canon_t, canon_i, canon_m

    def make_rotation_ints(self):
        """Helper for making setints from rotations"""
        result = []
        for rotation in self.pcset._rotations():
            result.append([utils.setint(pcs) for pcs in rotation])
        return result

    def make_prime_operation(self):
        """Helper for listing operations that make rotation_ints"""
        tto_ints = []
        for index_m, operation in enumerate(self.pcset._rotation_ints):
            for index_t, num in enumerate(operation):
                tto_ints.append((num, index_t, index_m))
        tto_ints.sort()
        tto = tto_ints[0]
        oper = tto[2]
        if oper == 0:
            m = 1
        elif oper == 1:
            m = self.pcset._mod - 1
        elif oper == 2:
            m = self.pcset._default_m
        elif oper == 3:
            m = self.pcset._mod - self.pcset._default_m
        return (tto[1], m)


    def testT_rotations(self):
        self.assertEqual(self.t_rots[0], self.pcset.uo_pcs)
        self.assertEqual(self.t_rots[-1], [0, 1, 2, 3, 5, 11])

    def testI_rotations(self):
        self.assertEqual(self.i_rots[0], self.pcset._invert().uo_pcs)
        self.assertEqual(self.i_rots[-1], [5, 7, 8, 9, 10, 11])

    def testM_rotations(self):
        self.assertEqual(self.m_rots[0], self.pcset._transpose_multiply().uo_pcs)
        self.assertEqual(self.m_rots[-1], [2, 4, 5, 7, 9, 11])

    def testMi_rotations(self):
        self.assertEqual(self.mi_rots[0],
                         self.pcset._transpose_multiply()._invert().uo_pcs)
        self.assertEqual(self.mi_rots[-1], [1, 3, 5, 6, 8, 11])

    def testAll_rotations(self):
        all_rots = self.t_rots + self.i_rots + self.m_rots + self.mi_rots
        self.assertEqual(all_rots, self.pcset.all_rotations)

    def testRotations(self):
        self.make_rotations()
        def unpack_rotations():
            """unpack the generator of generators to a list of lists"""
            return [list(rot) for rot in self.pcset._rotations()]
        self.pcset.canon(True, True, True)
        self.assertEqual(self.all_rots, unpack_rotations())
        self.pcset.canon(True, True, False) # Default setting. Tn/TnI-type
        self.assertEqual(self.ti_rots, unpack_rotations())
        self.pcset.canon(True, False, True)
        self.assertEqual(self.tm_rots, unpack_rotations())
        self.pcset.canon(True, False, False)
        self.assertEqual([self.t_rots], unpack_rotations())
        self.pcset.canon(False, True, True)
        self.assertEqual(self.im_only, unpack_rotations())
        self.pcset.canon(False, True, False)
        self.assertEqual(self.i_only, unpack_rotations())
        self.pcset.canon(False, False, True)
        self.assertEqual(self.m_only, unpack_rotations())
        self.pcset.canon(False, False, False)
        self.assertEqual(self.t_only, unpack_rotations())

    def testAllRotations(self):
        all_rots = []
        all_rots.extend(self.t_rots)
        all_rots.extend(self.i_rots)
        all_rots.extend(self.m_rots)
        all_rots.extend(self.mi_rots)
        self.assertEqual(all_rots, self.pcset.all_rotations)

    def testRotationInts(self):
        self.make_rotations()
        for t, i, m in self.make_canons():
            self.pcset.canon(t, i, m)
            self.assertEqual(self.make_rotation_ints(),
                             self.pcset._rotation_ints)

    def testPrimeOperation(self):
        self.pcset.clear()
        l = [3, 5, 6, 11, 0, -2, 2, -4, 7, 9, 13, -8]
        for pc in l:
            self.pcset + pc
            for t, i, m in self.make_canons():
                self.pcset.canon(t, i, m)
                self.assertEqual(self.pcset.prime_operation,
                                 self.make_prime_operation())

    def testPrime(self):
        primes = []
        set_ints = [0, 4095, 420, 2224]
        sets = [PCSet(utils.fromint(each)) for each in set_ints]
        for t, i, m in self.make_canons():
            for each in sets:
                each.canon(t, i, m)
                primes.append(each.prime)
        self.assertEqual(primes, [
                         [],
                         [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
                         [0, 1, 3, 6],
                         [0, 1, 4, 6],
                         [],
                         [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
                         [0, 1, 3, 6],
                         [0, 1, 3, 7],
                         [],
                         [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
                         [0, 6, 7, 9],
                         [0, 1, 6, 10],
                         [],
                         [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
                         [0, 3, 5, 6],
                         [0, 1, 3, 7],
                         [],
                         [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
                         [2, 5, 7, 8],
                         [1, 5, 7, 8],
                         [],
                         [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
                         [2, 5, 7, 8],
                         [1, 5, 7, 8],
                         [],
                         [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
                         [2, 5, 7, 8],
                         [4, 5, 7, 11],
                         [],
                         [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
                         [2, 5, 7, 8],
                         [4, 5, 7, 11]                            
        ])


class PrimeReliantTests(PrimeTestCase):

    def testPCInt(self):
        for each in self.sets:
            self.assertEqual(utils.setint(each.prime), each.pcint)

    def testForteName(self):
        for each in self.sets:
            self.assertTrue(each.forte != None)

    def testForteInt(self):
        for each in self.sets:
            self.assertEqual(each.pcint,
                             utils.setint(utils.from_forte(each.forte)))

    def testForteSet(self):
        a = PCSet()
        fnames = [each.forte for each in self.sets]
        new_sets = []
        for fname in fnames:
            a.clear()
            a = PCSet.forte_name(fname)
            new_sets.append(a.copy())
        new_fnames = [each.forte for each in new_sets]
        self.assertEqual(fnames, new_fnames)

    def testMPartner(self):
        for each in self.sets:
            self.assertEqual(each.mpartner, each._transpose_multiply().prime)

    def testLiteralCompliment(self):
        self.assertEqual(self.pcset.literal_compliment, [5, 7, 8, 9, 10, 11])

    def testCompliment(self):
        for each in self.sets:
            other = each.copy()
            other.c()
            self.assertEqual(each.literal_compliment, other)

    def testAbstractCompliment(self):
        for each in self.sets:
            self.assertEqual(each.literal_compliment.prime,
                             each.abstract_compliment)

    def testicv(self):
        icvs = [each.icv for each in self.sets]
        self.assertEqual(icvs, [
            [0, 0, 0, 0, 0, 0, 0],
            [12, 12, 12, 12, 12, 12, 6],
            [3, 1, 0, 0, 1, 1, 0],
            [5, 0, 3, 2, 1, 4, 0],
            [5, 2, 1, 2, 2, 2, 1],
            [5, 2, 1, 2, 1, 2, 2],
            [7, 2, 5, 4, 3, 6, 1],
            [3, 0, 0, 2, 0, 0, 1],
            [4, 1, 1, 0, 1, 2, 1],
            [6, 2, 3, 3, 2, 4, 1],
        ])

    def make_z_sets(self):
        zints = Z_PARTNERS.keys()
        return [PCSet(utils.fromint(zint)) for zint in zints]

    def testZPartner(self):
        for each in self.make_z_sets():
            self.assertTrue(each.zpartner.pcint in Z_PARTNERS.values())

    def testZ(self):
        for each in self.make_z_sets():
            each.z()
            self.assertTrue(each.pcint in Z_PARTNERS.values())

    def testEachPrime(self):
        a = PCSet()
        for prime in a.each_prime():
            self.assertEqual(prime.prime, prime._unique_pcs)

class SubsetsTest(TestCase):

    def setUp(self):
        self.l = [0, 3, 4]
        self.pcset = PCSet(self.l)

    def testSubsets(self):
        subs = [sub for sub in self.pcset.subsets()]
        self.assertEqual(subs, [
                         [3, 4], [4], [], [3], [],
                         [0, 4], [4], [], [0], [],
                         [0, 3], [3], [], [0], []
        ])
        self.assertTrue(isinstance(subs[0], PCSet))

    def testSubPrimes(self):
        subprimes = [subprime for subprime in self.pcset.subprimes()]
        self.assertEqual(subprimes, [
                         [0, 1], [0], [], [0], [],
                         [0, 4], [0], [], [0], [],
                         [0, 3], [0], [], [0], []
        ])

class SupersetsTest(TestCase):

    def setUp(self):
        self.l = [0, 1, 2, 3, 5, 6, 8, 10, 11]
        self.pcset = PCSet(self.l)

    def testSupersets(self):
        supers = [sup for sup in self.pcset.supersets()]
        self.assertEqual(supers, [
                         [0, 1, 2, 3, 4, 5, 6, 8, 10, 11],
                         [0, 1, 2, 3, 4, 5, 6, 7, 8, 10, 11],
                         [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
                         [0, 1, 2, 3, 4, 5, 6, 8, 9, 10, 11],
                         [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
                         [0, 1, 2, 3, 5, 6, 7, 8, 10, 11],
                         [0, 1, 2, 3, 4, 5, 6, 7, 8, 10, 11],
                         [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
                         [0, 1, 2, 3, 5, 6, 7, 8, 9, 10, 11],
                         [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
                         [0, 1, 2, 3, 5, 6, 8, 9, 10, 11],
                         [0, 1, 2, 3, 4, 5, 6, 8, 9, 10, 11],
                         [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
                         [0, 1, 2, 3, 5, 6, 7, 8, 9, 10, 11],
                         [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
        ])

    def testSuperPrimes(self):
        superprimes = [superprime for superprime in self.pcset.superprimes()]
        self.assertEqual(superprimes, [
                         [0, 1, 2, 3, 4, 5, 6, 7, 8, 10],
                         [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                         [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
                         [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                         [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
                         [0, 1, 2, 3, 4, 5, 7, 8, 9, 10],
                         [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                         [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
                         [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                         [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
                         [0, 1, 2, 3, 4, 5, 6, 7, 9, 10],
                         [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                         [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
                         [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                         [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
        ])
"""
TODO: Add tests for PPCSet methods below

    Finish prime test - pass doesn't count as a unit test

Untested methods:
each_card #FIXME: Implementation of this method sucks anyways

Add test for similarity relations

Add tests for Tone rows

"""
