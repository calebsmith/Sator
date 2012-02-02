#!/usr/bin/env python
from unittest import TestCase, main

from core import PPCSetBase, PCSet, PSet
import utils


"""Test PCSet/PSet class overrides"""
class InitTests(TestCase):
    """PCSet and PSet classes initialize correctly given diff. object types"""

    def setUp(self):
        self.l = [3, 0, 9]
        self.l2 = [2, 13, -12]

    def testInitInt(self):
        a = PSet(0, 9)
        b = PCSet(self.l2)        
        self.assertEqual(a, [0, 9])
        self.assertEqual(b._unique_pcs, [0, 1, 2])

    def testInitSet(self):
        s1 = set(['4', 5, '0'])
        s2 = set(self.l)
        a = PSet(s1)
        b = PCSet(s2)
        c = PCSet(s1, s2)
        self.assertEqual(a._unique_pcs, [0, 4, 5])
        self.assertEqual(b._unique_pcs, [0, 3, 9])
        self.assertEqual(c._unique_pcs, [0, 3, 4, 5, 9])

    def testInitList(self):
        a = PSet(self.l)
        b = PCSet(self.l2)
        c = PSet(self.l, self.l2)
        self.assertEqual(a._unique_pcs, [0, 3, 9])
        self.assertEqual(b._unique_pcs, [0, 1, 2])
        self.assertEqual(c._unique_pcs, [0, 1, 2, 3, 9])
    
    def testInitTuple(self):
        a = PSet((0, 1))
        self.assertEqual(a, [0, 1])

    def testInitPCSet(self):
        a = PCSet(self.l)
        b = PSet(self.l2)
        c = PCSet(a)
        d = PCSet(b)
        e = PCSet(c, d)
        self.assertEqual(c._unique_pcs, [0, 3, 9])
        self.assertEqual(d._unique_pcs, [0, 1, 2])
        self.assertEqual(e._unique_pcs, [0, 1, 2, 3, 9])

    def testInitPSet(self):
        a = PSet([0, 15, 6])
        b = PCSet([0, 1, 9])
        c = PSet(a)
        d = PSet(b)
        e = PSet([2, 8], multiset=True, ordered=False)
        e += c + d
        f = PSet([2, 8] + c + d, multiset=True, ordered=False)
        self.assertEqual(c, [0, 15, 6])
        self.assertEqual(d, [0, 1, 9])
        self.assertTrue(e == [0, 15, 6, 0, 1, 9, 2, 8])
        self.assertTrue(f == [0, 15, 6, 0, 1, 9, 2, 8])


class AddTests(TestCase):
    """Adding to PCSet and PSet objects returns expected objects"""

    def setUp(self):
        self.i = 2
        self.l = [0, 3, 6, 9]
        self.s = set(self.l)

    def testaddInt(self):
        a = PPCSetBase() + self.i
        self.assertEqual(a, self.i)

    def testaddList(self):
        a = PSet() + self.l
        self.assertEqual(a, self.l)

    def testaddTuple(self):
        a = PSet()
        a += (0, 1, 4)
        self.assertEqual(a, (0, 1, 4))

    def testaddSet(self):
        a = PCSet() + self.s
        self.assertEqual(a, self.s)

    def testaddPPCSetTypes(self):
        a = PPCSetBase([0, 1])
        b = PPCSetBase([2, 3])
        c = PPCSetBase()
        c = a + b
        self.assertEqual(c, PSet([0, 1, 2, 3]))
        self.assertEqual(c, PCSet([0, 1, 2, 3]))


class SubTests(TestCase):
    """subtraction override for removes all PC's in PCSet"""

    def setUp(self):
        self.l = [6, 5, 0, 1, 2, 3, 2, 6, 2, 4, 4, 5, 6]

    def testsubInt(self):
        a = PCSet(self.l) - 2
        self.assertEqual(a._unique_pcs, [0, 1, 3, 4, 5, 6])

    def testsubList(self):
        a = PCSet(self.l) - [0, 1, 2]
        self.assertEqual(a._unique_pcs, [3, 4, 5, 6])

    def testsubTuple(self):
        a = PCSet(self.l) - (0, 1, 2, 3, 4)
        self.assertEqual(a._unique_pcs, [5, 6])

    def testsubSet(self):
        a = PCSet(self.l) - set([4, 5, 6])  
        self.assertEqual(a._unique_pcs, [0, 1, 2, 3])

    def testsubPSet(self):
        a = PCSet(self.l) - PSet(0, 1, 5, 6)
        self.assertEqual(a._unique_pcs, [2, 3, 4])

    def testsubPCSet(self):
        a = PCSet(self.l) - PCSet(0, 1, 2, 3)
        self.assertEqual(a._unique_pcs, [4, 5, 6])


class EqualityTest(TestCase):
    """Equality checks between PCSets, PSets, and built ins"""

    def setUp(self):
        self.l = [0, 1, 2, 4, 5, 10 ,1 ,0]
        self.s = set(self.l)
        self.pcset = PCSet(self.l)
        self.pset = PSet(self.l)
        self.pset.ordered(False)

    def testeqPPCSets(self):
        self.assertTrue(self.pcset == self.pcset)
        self.assertTrue(self.pset == self.pset)
        self.assertTrue(self.pcset == self.pset)

    def testeqPPCSet_list(self):
        self.assertTrue(self.pcset == self.l and self.pset == self.l)

    def testeqPPCSet_set(self):
        self.assertTrue(self.pcset == self.s and self.pset == self.s)

    def testeqPPCSet_int(self):
        a = PCSet(3)
        b = PSet(3)
        self.assertTrue(a == 3 and b == 3)


class InEqualityTest(TestCase):
    """Check for != between PCSets, PSets, and built ins"""

    def setUp(self):
        self.l = [0, 1, 2, 4, 5, 10 ,1 ,0]
        self.l2 = [0, 1, 2, 4, 5, 10]
        self.l3 = [0, 2, 4]
        self.s = set(self.l)
        self.s2 = set(self.l2)
        self.pcset = PCSet(self.l)
        self.pset = PSet(self.l)
        self.pcset2 = PCSet(self.l2)
        self.pset2 = PSet(self.l2)

    def testnePPCSets(self):
        pset3 = PSet(self.l3)
        self.assertTrue(self.pcset == self.l2 and self.pset == self.l2)
        self.assertTrue(self.pcset == self.pset and self.pcset != pset3)

    def testnePPCSet_list(self):
        self.assertTrue(self.pcset == self.l2 and self.pset == self.l2)
        self.assertTrue(self.pcset != self.l3 and self.pset != self.l3)

    def testnePPCSet_set(self):
        s = set([0, 1, 2])
        self.assertTrue(self.pcset != s and self.pset != s)

    def testnePPCSet_int(self):
        self.assertTrue(self.pcset != 5 and self.pset != 3)


class GetItemTest(TestCase):
    """[x:y] PCSets and PSets should return pcs and pitches respectively"""
    
    def setUp(self):
        self.l = [0, 1, 2, 5, 7, 9, 35, 4]
        self.pcset = PCSet(self.l)
        self.pset = PSet(self.l)

    def testgetInt(self):
        self.assertEqual(self.pcset[6], [9])
        self.assertEqual(self.pset[6], [9])
        self.pset.ordered(True)
        self.assertEqual(self.pset[6], [35])

    def testgetRange(self):
        self.assertEqual(self.pcset[2:5], [2, 4, 5])

    def testgetNegative(self):
        self.assertEqual(self.pcset[-1], [11])

    def testgetAfter(self):
        try:
            self.pcset[100]
        except IndexError:
            assert True


class SequenceTest(TestCase):
    """PCSets and PSets behave like sequences with iteration and len()"""

    def setUp(self):
        self.l = [0, 1, 2, 4]
        self.pcset = PCSet(self.l)
        self.pset = PSet(self.l)

    def testiterTest(self):
        pcout = [pc for pc in self.pcset]
        pout = [p for p in self.pset]
        self.assertTrue(pcout == self.l and pout == self.l)

    def testlenTest(self):
        self.assertEqual(len(self.pcset), 4)
        self.pset.multiset(False)
        self.assertEqual(len(self.pset + [0, 2, 5]), 5)
        self.pset.multiset(True)
        self.assertEqual(len(self.pset + [0, 2, 5]), 7)


class ReprTest(TestCase):
    """PCSet and PSet repr's vary based on ordered and multiset settings"""

    def setUp(self):
        self.l = [0, 1, -7, 16, 1, 0]
        self.pcset = PCSet(self.l)
        self.pset = PSet(self.l)

    def testreprO(self):
        self.pcset.ordered(True)
        self.pset.ordered(True)
        self.pcset.multiset(False)
        self.pset.multiset(False)
        self.assertEqual(self.pcset.__repr__(), '[0, 1, 5, 4]')
        self.assertEqual(self.pset.__repr__(), '[0, 1, -7, 16]')

    def testreprO_Multi(self):
        pcset = PCSet(self.l, ordered=True, multiset=True)
        pset = PSet(self.l, ordered=True, multiset=True)
        self.assertEqual(pcset.__repr__(), '[0, 1, 5, 4, 1, 0]')
        self.assertEqual(pset.__repr__(), '[0, 1, -7, 16, 1, 0]')

    def testreprUO(self):        
        self.pcset.ordered(False)
        self.pset.ordered(False)
        self.pcset.multiset(False)
        self.pset.multiset(False)
        self.assertEqual(self.pcset.__repr__(), '[0, 1, 4, 5]')
        self.assertEqual(self.pset.__repr__(), '[-7, 0, 1, 16]')

    def testreprUO_Multi(self):
        pcset = PCSet(self.l, ordered=False, multiset=True)
        pset = PSet(self.l, ordered=False, multiset=True)
        self.assertEqual(pcset.__repr__(), '[0, 0, 1, 1, 4, 5]')
        self.assertEqual(pset.__repr__(), '[-7, 0, 0, 1, 1, 16]')


"""Test methods pitch/pc manipulation methods such as insert, copy, clear"""
class InsertTest(TestCase):
    """
    Insert method inserts a pitch/pc in place or appends it for index errors
    """

    def setUp(self):
        self.l = [1, 4, 23, 5, -9]

    def testinsertBegin(self):
        a = PCSet(self.l)
        b = PSet(self.l)
        a.insert(0, 10)
        b.insert(0, 11)
        self.assertEqual(a.pitches, [10] + self.l)
        self.assertEqual(b.pitches, [11] + self.l)

    def testinsertMiddle(self):
        a = PCSet(self.l)
        b = PSet(self.l)
        a.insert(3, 15)
        b.insert(4, 8)
        self.assertEqual(a.pitches, [1, 4, 23, 15, 5, -9])
        self.assertEqual(b.pitches, [1, 4, 23, 5, 8, -9])

    def testinsertEnd(self):
        a = PCSet(self.l)
        b = PSet(self.l)
        a.insert(6, 10)
        b.insert(6, 99)
        self.assertEqual(a.pitches, self.l + [10])
        self.assertEqual(b.pitches, self.l + [99])

    def testinsertAfter(self):
        a = PCSet(self.l)
        b = PSet(self.l)
        a.insert(100, 1)
        b.insert(100, 0)
        self.assertEqual(a.pitches, self.l + [1])
        self.assertEqual(b.pitches, self.l + [0])

    def testinsertNegative(self):
        a = PCSet(self.l, multiset=True)
        b = PSet(self.l, multiset=True)
        a.insert(-2, 2)
        b.insert(-3, 12)
        self.assertEqual(a.pitches, [1, 4, 23, 2, 5, -9])
        self.assertEqual(b.pitches, [1, 4, 12, 23, 5, -9])


class ClearTest(TestCase):
    """The clear method removes all pitches/pcs from a PCSet or PSet"""

    def setUp(self):
        self.l = [9, 3, 4, 5, 6, 1]

    def testclearPCSet(self):
        a = PCSet(self.l)
        a.clear()
        self.assertTrue(a.pcs == [] and a.pitches == [])

    def testclearPSet(self):
        a = PSet(self.l)
        a.clear()
        self.assertTrue(a.pcs == [] and a.pitches == [])


class CopyTest(TestCase):
    """
    Create a new instance with the pitches, settings and class of the original
    """

    def setUp(self):
        self.l = [0, 3, 16, 1]

    def testcopyPitches(self):
        a = PCSet(self.l)
        b = PSet(self.l)
        c = a.copy()
        d = b.copy()
        self.assertTrue(c.pitches == self.l and d.pitches == self.l)

    def testcopySettings(self):
        def verify(current):
            self.assertEqual(current.__class__, PCSet)
            self.assertTrue(current._ordered == False and current._multiset == False)
            self.assertEqual(current._mod, 7)
            self.assertTrue(current._canon_t, True)
            self.assertEqual(current._canon_i, False)
            self.assertEqual(current._canon_m, True)
            self.assertEqual(current.pitches, self.l)

        a = PCSet(self.l)
        a.mod(7)
        a.ordered(False)
        a.multiset(False)
        a.canon(True, False, True)
        a2 = a.copy()
        verify(a2)    
        b = PSet(self.l)
        self.assertEqual(b.__class__, PSet)
        b = a.copy()
        verify(b)


"""Test settings attributes and their methods"""
class SettingsTest(TestCase):
    """PCSet and PSet instances have various methods to change settings"""

    def setUp(self):
        self.l = [0, 4, 9, 11]
        self.pcset = PCSet(self.l)
        self.pset = PSet(self.l)

    def testMod(self):
        self.pcset.mod(7)
        self.pset.mod(13)
        self.assertEqual(self.pcset._mod, 7)
        self.assertEqual(self.pset._mod, 13)

    def testCanon(self):
        a = self.pcset
        b = self.pset
        a.canon(True, False, False)
        b.canon(False, True, True)        
        self.assertTrue(
            a._canon_t == True and a._canon_i == False and a._canon_m == False
        )
        self.assertTrue(
            b._canon_t == False and b._canon_i == True and b._canon_m == True
        )

    def testDefault_m(self):
        self.pcset.default_m(7)
        self.assertEqual(self.pcset._default_m, 7)

    def testOrdered(self):
        self.pcset.ordered(True)
        self.pset.ordered(True)
        self.assertTrue(
            self.pcset._ordered == True and self.pset._ordered == True
        )
        self.pcset.ordered(False)
        self.pset.ordered(False)
        self.assertTrue(
            self.pcset._ordered == False and self.pset._ordered == False
        )

    def testMultiset(self):
        self.pcset.multiset(True)
        self.pset.multiset(True)
        self.assertTrue(
            self.pcset._multiset == True and self.pset._multiset == True
        )
        self.pcset.multiset(False)
        self.pset.multiset(False)
        self.assertTrue(
            self.pcset._multiset == False and self.pset._multiset == False
        )
