#!/usr/bin/env python
from itertools import permutations

import sator.utils as utils
from sator.const import MAX_OCTAVE

class SetRowBase(object):
    """Base class for PC/pitch sets and tone rows"""

    pitches = []
    _mod = 12
    _default_m = 5
    _ordered = False
    _multiset = False

    #Overrides
    def __init__(self, *args, **kwargs):
        modulus = kwargs.pop('mod', 12)
        self.mod(modulus)
        ordered = kwargs.pop('ordered', self._ordered)
        self.ordered(ordered)
        multiset = kwargs.pop('multiset', self._multiset)
        self.multiset(multiset)
        self[:] = []
        results = []
        for arg in args:
            results += self.__add__(arg, internal=True)
        # Limit the pitches to within max_octave octaves from 0
        new_results = []
        for result in results:
            new = abs(result) % (MAX_OCTAVE * self.mod())
            if result < 0:
                new = new * -1
            new_results.append(new)
        self.pitches = new_results
        if not self._multiset:
            self[:] = self._rm_dupes(self.pitches)

    def __add__(self, other, **kwargs):
        internal = kwargs.get('internal', False)
        ps = other
        if isinstance(other, SetRowBase):
            ps = other.pitches[:]
        if isinstance(other, (int, long)):
            ps = [other]
        if isinstance(other, (tuple, list)):
            ps = list(other)
        if isinstance(other, set):
            ps = [int(num) for num in other]
        ps = self.pitches + ps
        if not self._multiset:
            ps = self._rm_dupes(ps)
        # If initializing, returning an instance creates infinite recursion
        ps = self.copy(ps) if not internal else ps
        return ps

    def __radd__(self, other):
        return self.__add__(other)

    def __eq__(self, other):
        """Compare equality between a ToneRow/PSet/PCSet and another object"""
        try:
            that = other.copy()
        except AttributeError:
            try:
                that = other[:]
            except TypeError:
                that = [other]
        #Are we comparing pitches as ordered lists or set membership?
        if not self._ordered and isinstance(other, (tuple, list)):
            that = set(that)
        #Is the other a PSet/PCSet or builtin ?
        if isinstance(that, SetRowBase):
            return self.ppc == that.ppc
        if isinstance(that, (tuple, list)):
            return self.ppc == list(that)
        if isinstance(that, set):
            return set(self.ppc) == that
        else:
            return NotImplemented
        return False

    def __ne__(self, other):
        result = self.__eq__(other)
        if result is NotImplemented:
            return result
        return not result

    def __getitem__(self, key):
        try:
            l = []
            l.extend(self.ppc[key])
            return self.copy(l)
        except TypeError:
            l = [self.ppc[key]]
            return self.copy(l)

    def __setitem__(self, key, value):
        if isinstance(value, (int, long)):
            new = abs(value) % (MAX_OCTAVE * self.mod())
            if value < 0:
                new = new * -1
            value = new
        self.pitches[key] = value

    def __iter__(self):
        for p in self.ppc:
            yield p

    def __len__(self):
        return len(self.ppc)

    def __repr__(self):
        return str(self.ppc)

    def __copy__(self):
        return copy(self)

    def copy(self, pitches=None, **kwargs):
        """Use to copy a ToneRow/PSet/PCSet with all data attributes."""
        if pitches is None:
            pitches = self.pitches
        new_kwargs = {
            'mod': self._mod,
            'ordered': self._ordered,
            'multiset': self._multiset,
        }
        new_kwargs.update(kwargs or {})
        new = self.__class__(pitches, **new_kwargs)
        if hasattr(new, 'canon'):
            new.canon(self._canon_t, self._canon_i, self._canon_m)
        new._default_m = self._default_m
        return new

    class InvalidModulus(Exception):
        pass

    def mod(self, new_mod=None):
        """
        Takes one argument as the new modulus of the system.
        Without an argument, returns the current modulus.
        """
        if new_mod is not None:
            if new_mod > 0 and new_mod < 32:
                self._mod = new_mod
            else:
                raise self.InvalidModulus('The modulus must be > 0 and < 32')
        else:
            return self._mod

    def default_m(self, new_m=None):
        """
        Takes one argument as the new default argument for M operations.
        (The default for Mod 12 is 5)
        Without an argument, returns the current default m.
        """
        if new_m:
            self._default_m = new_m
        else:
            return self._default_m

    def multiset(self, value=None):
        """
        Takes one boolean argument and determines if the object is a multiset.
        (The default for all objects is False. ToneRows cannot be multisets)
        Without an argument, returns the current setting.
        """
        if value is not None:        
            self._multiset = True if value else False
        else:
            return self._multiset

    def ordered(self, value=None):
        """
        Takes one boolean argument and determines if the object is ordered.
        (The default for PCSets is False. The default for PSets is True.)
        Without an argument, returns the current setting.
        """
        if value is not None:
            self._ordered = True if value else False
        else:
            return self._ordered

    @property
    def pcs(self):
        """Returns the pitch classes of the current set/row"""
        return [pitch % self._mod for pitch in self.pitches]

    @property
    def _pc_set(self):
        """Returns pitch classes as a Python set for internal use"""
        return set(self.pcs)

    @property
    def _pitch_set(self):
        """Returns pitches as a Python set for internal use"""
        return set(self.pitches)

    @property
    def uo_pcs(self):
        """Returns unordered pitch classes in ascending order"""
        return sorted(self.pcs[:])

    @property
    def _unique_pcs(self):
        """
        Returns the unique, unordered pitch classes in ascending order. These
        are guarnteed to be unique regardless of rather or not the object is a
        multiset.
        """
        return sorted(list(self._pc_set))

    @property
    def uo_pitches(self):
        """Returns the unordered pitches in ascending order"""
        return sorted(self.pitches[:])

    @property
    def ppc(self):
        """
        Returns the pitches or pcs of a ToneRow, PCSet, or PSet taking into
        account the ordered and multiset settings.
        """
        #Ordered?
        if self._ordered:
            pitches = self.pitches
            pcs = self.pcs
        else:
            pitches = self.uo_pitches
            pcs = self.uo_pcs
        #PC/Pitch Set?
        if getattr(self, 'pitchset', False):
            ppc = pitches
        else:
            ppc = pcs
        #Multiset?
        if not self._multiset:
            ppc = self._rm_dupes(ppc)
        return ppc

    def _rm_dupes(self, ps):
        """Remove all duplicates of a given pitch or pitch class from a list"""
        new = []
        [new.insert(ps.index(num), num) for num in ps[:] if num not in new]
        return new

    def each_n(self):
        """
        Yields a number for each possible member in the object considering its
        modulus.
        (An object with a modulus of 12 would return [0, 1, 2...11])
        """
        return self.each_n_in_mod(self._mod)

    @classmethod
    def each_n_in_mod(cls, mod):
        """
        Same as the instance method but takes one positional arg as the modulus
        """
        for num in xrange(0, mod):
            yield num

    def each_tto(self):
        """
        Yields an (n, m) pair for each TTO that can be performed on the given
        object
        """
        for m in [1, -1, self._default_m, self._mod - self._default_m]:
            for n in self.each_n():
                yield (n, m)

    def each_permutation(self):
        """
        A generator that yields ordered objects that represent each
        permutation of the given object.
        """
        for each in permutations(self[:]):
            yield self.copy(each, ordered=True)

    def _transpose(self, sub_n=0):
        return self.copy(utils.transpose(self.pitches, sub_n))

    def _invert(self, sub_n=0):
        return self.copy(utils.invert(self.pitches, sub_n))

    def _transpose_multiply(self, sub_n=0, sub_m=0):
        if not sub_m:
            sub_m = self._default_m
        result = [pc % self._mod for pc in \
                  utils.transpose_multiply(self.pcs, sub_n, sub_m)]
        return self.copy(result)

    def t(self, sub_n):
        """Transpose the object in place by the argument provided."""
        self[:] = (self._transpose(sub_n)).pitches

    def i(self, sub_n=0):
        """
        Invert the object in place. If an argument is provided, also transpose
        the object in place by that amount.
        """
        self[:] = (self._invert(sub_n)).pitches

    @property
    def t_rotations(self):
        """
        Returns a list of objects for each possible transposition of the given
        object.
        """
        return [self.copy(rot) for rot in [self._transpose(n) \
                                           for n in self.each_n()]]

    @property
    def i_rotations(self):
        """
        Returns a list of objects for each possible transposition of the given
        object after inversion.
        """
        return [self.copy(rot) for rot in [self._invert(n) \
                                           for n in self.each_n()]]

    @property
    def m_rotations(self):
        """
        Returns a list of objects for each possible transposition of the given
        object after M.
        """
        return [self.copy(rot) for rot in [self._transpose_multiply(n) \
                                           for n in self.each_n()]]

    @property
    def mi_rotations(self):
        """
        Returns a list of objects for each possible transposition of the given
        object after MI.
        """
        return [self.copy(rot) for rot in [self._transpose_multiply(n, self._default_m * -1) \
                                           for n in self.each_n()]]

    @property
    def all_rotations(self):
        """
        Return a flat list of objects for each possible TTO of the given object
        """
        return [self._transpose_multiply(n, m) for n, m in self.each_tto()]


class PCBase(object):
    """Base class for Tone rows and PC sets"""

    def m(self, sub_n=0):
        """
        Perform M on the object in place. If an argument is provided, also
        transpose the object in place by that amount.
        """
        self[:] = (self._transpose_multiply(sub_n, self._default_m)).pitches

    def mi(self, sub_n=0):
        """
        Perform M and I on the object in place. If an argument is provided,
        also transpose the object in play by that amount.
        """
        sub_m = self._mod - self._default_m
        self[:] = (self._transpose_multiply(sub_n, sub_m)).pitches
        
    def t_m(self, sub_n, sub_m):
        """
        Perform TnMm on the object in place, where n and m are positional
        arguments. If n is not provided, it defaults to 0. If m is not provided
        it defaults to the default_m of the object.
        """
        self[:] = (self._transpose_multiply(sub_n, sub_m)).pitches
