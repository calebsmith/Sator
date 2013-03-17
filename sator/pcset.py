#!/usr/bin/env python

from sator.setbase import SetBase, PCBase


class PCSet(SetBase, PCBase):
    """
    A Class for pitch class sets which adds pitch class only methods
    """

    pitchset = False

    def c(self):
        """
        Return a new instance that represents the literal compliment of the
        current one
        """
        return self.copy(self.literal_compliment.pitches)

    def z(self):
        """
        Return a new instance that represents the the Z-partner of the current
        instance if possible, Otherwise return None
        """
        other = self.zpartner
        if other:
            return self.copy(other.pitches)
