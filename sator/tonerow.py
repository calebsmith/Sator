#!/usr/bin/env python

from sator.setrowbase import SetRowBase, PCBase

class ToneRow(SetRowBase, PCBase):
    _modulus = 12

    class IncompleteToneRow(Exception):
        pass

    def __init__(self, *args, **kwargs):
        kwargs.update({'multiset': False, 'ordered': True})
        SetRowBase.__init__(self, *args, **kwargs)
        if len(self.ppc) < self._mod:
            msg = 'Tone rows must be instantiated with a number of ' + \
                  'pitches or pcs equal to their modulus'
            raise self.IncompleteToneRow(msg)

    def swap(self, a, b):
        """
        Given two arguments, swap the PC's in the ToneRow that are at these
        positions. 
        """
        c = self.pitches[a]
        self.pitches[a] = self.pitches[b]
        self.pitches[b] = c

    @property
    def P(self):
        """Returns the prime of the ToneRow"""
        return self.copy()

    @property
    def R(self):
        """Returns the retrograde of the ToneRow"""
        return self.copy(list(reversed(self.ppc)))

    @property
    def I(self):
        """Returns the inversion of the ToneRow"""
        return self._invert()

    @property
    def RI(self):
        """Returns the retrograde inversion of the ToneRow"""
        return self.R.I

    @property
    def M(self):
        """
        Returns the Mm of the ToneRow, where m = the default_m of the ToneRow
        """
        return self._transpose_multiply()

    @property
    def MI(self):
        """
        Returns the MmI of the ToneRow, where m = the default_m of the ToneRow
        """
        return self._transpose_multiply(0, self._mod - self._default_m)

    @property
    def RM(self):
        """Returns the retrograde of the M of the ToneRow."""
        return self.R.M

    @property
    def RMI(self):
        """Returns the retrograde of the MI of the ToneRow."""
        return self.R.MI

    def ordered(self, order):
        """Overridden so that ToneRows are always ordered."""
        self._ordered = True

    def multiset(self, multi):
        """Overridden so that ToneRows are never multisets."""
        self._multiset = False
