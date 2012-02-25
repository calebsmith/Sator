#!/usr/bin/env python

from sator.setbase import SetBase, PCBase


class PCSet(SetBase, PCBase):
    """
    A Class for pitch class sets which adds pitch class only methods
    """

    pitchset = False

    def c(self):
        """Change the given object in place to its literal compliment."""
        self[:] = self.literal_compliment.pitches

    def z(self):
        """
        Change the given object in place to its Z-partner if possible.
        Otherwise leave the object unchanged.        
        """
        other = self.zpartner
        if other:
            self[:] = other.pitches
