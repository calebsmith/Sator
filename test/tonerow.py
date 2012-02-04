#!/usr/bin/env python
from unittest import TestCase, main

from core import ToneRow


class ToneRowTests(TestCase):        
    def setUp(self):
        self.l = [0, 4, 5, 8, 9, 1, 10, 3, 6, 2, 7, 11]
        self.tonerow = ToneRow(self.l)

    def testInit(self):
        # Make sure exception is thrown if args < mod
        try:
            tonerow = ToneRow([0])
        except ToneRow.IncompleteToneRow:
            self.assertTrue(True)
        else:
            self.assertTrue(False)
        valid_tr = ToneRow(0, 1, 2, mod=3)
        self.assertTrue(valid_tr)

    def testMultiset_fails(self):
        self.tonerow.multiset(True)
        self.assertEqual(self.tonerow._multiset, False)

    def testP(self):
        self.assertEqual(self.tonerow.P, self.l)

    def testR(self):
        r = self.l
        r.reverse()
        self.assertEqual(self.tonerow.R, r)

    def testI(self):
        i = self.tonerow._invert()
        self.assertEqual(self.tonerow.I, i)

    def testRI(self):
        i = self.tonerow._invert()
        ri = i.ppc
        ri.reverse()
        self.assertEqual(self.tonerow.RI, ri)       
