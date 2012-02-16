#!/usr/bin/env python
from itertools import count, izip, combinations

import utils
from const import HIGH_PITCH_LIMIT, LOW_PITCH_LIMIT, Z_PARTNERS


class SetRowBase(object):
    """Base class for PC/pitch sets and tone rows"""

    #TODO: limit pitches to within PITCH_LIMIT bounds
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
        self.pitches = []
        if len(args) == 1:
            self.pitches = self.__add__(args[0], internal=True)
        elif len(args) > 1:
            result = []
            for arg in args:
                result += self.__add__(arg, internal=True)
            self.pitches = result
        if not self._multiset:
            self.pitches = self._rm_dupes(self.pitches)

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
        ps = self.pitches[:] + ps
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
        self.pitches[key] = value

    def __iter__(self):
        for p in self.ppc:
            yield p

    def __len__(self):
        return len(self.ppc)

    def __repr__(self):
        return str(self.ppc)

    def copy(self, pitches=None):
        """Use to copy a ToneRow/PSet/PCSet with all data attributes."""
        if pitches is None:
            pitches = self.pitches
        new = self.__class__(pitches, mod=self._mod, ordered=self._ordered,
                             multiset=self._multiset)
        if isinstance(self, PPCSetBase):
            new.canon(self._canon_t, self._canon_i, self._canon_m)
        new._default_m = self._default_m
        return new

    def mod(self, new_mod=None):
        """
        Takes one argument as the new modulus of the system.
        Without an argument, returns the current modulus.
        """
        if new_mod:
            self._mod = new_mod
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
        output = self.pcs[:]
        output.sort()
        return output

    @property
    def _unique_pcs(self):
        """
        Returns the unique, unordered pitch classes in ascending order. These
        are guarnteed to be unique regardless of rather or not the object is a
        multiset.
        """
        output = list(self._pc_set)
        output.sort()
        return output

    @property
    def uo_pitches(self):
        """Returns the unordered pitches in ascending order"""
        output = self.pitches[:]
        output.sort()
        return output

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
        if isinstance(self, PSet):
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
        return self

    @property
    def R(self):
        """Returns the retrograde of the ToneRow"""
        ppc = self.ppc
        ppc.reverse()
        return self.copy(ppc)

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


class PPCSetBase(SetRowBase):
    """Base class for PCSet and PSet"""

    _canon_t = True
    _canon_i = True
    _canon_m = False

    def __sub__(self, other):
        """Remove all instances of a given pc from a pcset"""
        rm_pcs = other
        if isinstance(other, (int, long)):
            rm_pcs = [other]
        if isinstance(other, set):
            rm_pcs = [int(num) for num in other]
        results = self.pitches[:]
        for pc in rm_pcs:
            while pc in results:
                results.remove(pc)
        return self.copy(results)

    def insert(self, place, pitch):
        """
        Given arguments (place, pitch) insert the pitch at the place position.
        Take care to inspect the object's pitches attribute rather than it's
        __repr__, which uses the ppc attribute and may truncate duplicates.
        If the position is too great, the pitch will be appended at the end.
        """
        try:
            pitches = self.pitches[:place]
            pitches.append(pitch)
            pitches.extend(self.pitches[place:])
            self[:] = pitches
        except IndexError:
            self.pitches.append(pitch)

    def clear(self):
        """Remove all pitches/pitch classes from the object."""
        self[:] = []

    def canon(self, t, i, m):
        """
        Takes arguments in the form of (T, I, M) where each is a boolean.
        These arguments determine which TTO's are canonical. These TTO's are
        used to determine an object's set-class.
        (The default canonical operators are T and I, hence the common name
        Tn/TnI type).
        Ex:
            a.canon(True, False, False)

            a.prime would now give the Tn-type, and ignore inversion as an
            operation for determining set-class membership.
        """
        self._canon_t = True if t else False
        self._canon_i = True if i else False
        self._canon_m = True if m else False

    @property
    def get_canon(self):
        """
        Returns a three tuple showing which TTO's are canonical for the given
        object. These are in the order (T, I, M). Refer to canon() for details
        on how these settings are used.
        """
        return (self._canon_t, self._canon_i, self._canon_m)

    @staticmethod
    def fromint(integer, modulus=12):
        """
        Static method that returns a PCSet object with pc's generated from
        their integer representation.
            Ex:
                0 = [], 1 = [0], 2 = [1], 3 = [0, 1], 4 = [2], 5 = [0, 2]
                PCSet.fromint(5) returns PCSet([0, 2])
        """
        new_set = PCSet(mod=modulus)
        new_set.pitches = utils.fromint(integer)
        return new_set

    @property
    def setint(self):
        """
        Returns the integer representation for the unique PC's in a given
        object
        """
        return utils.setint(self._unique_pcs)

    @property
    def pcint(self):
        """
        Returns the integer representation of a given object in prime form.
        """
        return utils.setint(self.prime)

    def each_set(self):
        """
        Yields every possible set in the modulus of the given object.
        """
        return self.each_set_in_mod(self._mod)

    def each_prime(self):
        """
        Yields each unique set-class in the modulus of the given object.
        """
        return self.each_prime_in_mod(self._mod)

    def each_card(self):
        """
        Yields every set with the same cardinality as the given object, taking
        into account the object's modulus.
        """
        return self.each_card_in_mod(self.cardinality, self._mod)

    @classmethod
    def each_set_in_mod(cls, mod):
        return(cls(utils.fromint(integer)) for integer in xrange(0, 2 ** mod))

    @classmethod
    def each_prime_in_mod(cls, mod):
        return(each for each in cls.each_set_in_mod(mod) if each.prime == each)

    @classmethod
    def each_card_in_mod(cls, card, mod):
        """
        Same as the instance method but takes two args for cardinality and
        modulus respectively
        """
        return (cls(each) for each in combinations(cls.each_n_in_mod(mod), card))

    @classmethod
    def each_prime_in_card_mod(cls, card, mod):
        """
        Yields every unique prime form with a given cardinality in the given
        modulus
        """
        for each in combinations(cls.each_n_in_mod(mod), card):
            if cls(each).prime == cls(each):
                yield cls(each)

    @property
    def cardinality(self):
        """Returns the cardinality of the given object."""
        return len(self._pc_set)

    # Helper functions for prime()
    def _t_rotations(self):
        """
        Same as the public method, but enforces that the returned objects are
        PCSets for use with the prime method.
        """
        return (PCSet(self.copy(rot)) for rot in [self._transpose(n) \
                                                  for n in self.each_n()])

    def _i_rotations(self):
        """
        Same as the public method, but enforces that the returned objects are
        PCSets for use with the prime method.
        """
        return (PCSet(self.copy(rot)) for rot in [self._invert(n) \
                                                  for n in self.each_n()])

    def _m_rotations(self):
        """
        Same as the public method, but enforces that the returned objects are
        PCSets for use with the prime method.
        """
        return (PCSet(self.copy(rot)) for rot in [self._transpose_multiply(n) \
                                                  for n in self.each_n()])

    def _mi_rotations(self):
        """
        Same as the public method, but enforces that the returned objects are
        PCSets for use with the prime method.
        """
        return (PCSet(self.copy(rot)) for rot in [self._transpose_multiply(n, self._default_m * -1) \
                                                  for n in self.each_n()])

    @property
    def _rotation_ints(self):
        """
        Returns a nested list with the interger representation for each object
        returned from _rotations()
        """
        return [[utils.setint(pcs) for pcs in rotation] \
            for rotation in self._rotations()]

    def _rotations(self):
        """
        Returns a nested list of PCSet objects for each canonical TTO for a
        given object.
        """
        def setify(pitches):
            pcs = [pitch % self._mod for pitch in pitches]
            result = list(set(pitches))
            result.sort()
            return result

        result = []
        if self._canon_t:
            result.append(self._t_rotations())
            if self._canon_i:
                result.append(self._i_rotations())
            if self._canon_m:
                result.append(self._m_rotations())
            if self._canon_i and self._canon_m:
                result.append(self._mi_rotations())
        else:
            result.append([setify(self.pcs)])
            if self._canon_i:
                result.append([setify(self._invert())])
            if self._canon_m:
                result.append([setify(self._transpose_multiply(0))])
        return result

    @property
    def prime_operation(self):
        """
        A property that returns (n, m) to perform on the given object via TnMm
        in order to obtain its prime form.
        """
        low_vals =[min(izip(operation, count())) \
            for operation in self._rotation_ints]
        min_val = min(izip(low_vals, count()))
        n = min_val[0][1]
        oper = min_val[1]
        if oper == 0:
            m = 1
        elif oper == 1:
            m = self._mod - 1
        elif oper == 2:
            m = self._default_m
        elif oper == 3:
            m = self._mod - self._default_m
        return (n, m)

    @property
    def prime(self):
        """
        Return a PCSet that represents the given object in prime form, taking
        into account its canonical TTO's (set these with .canon(T, I, M)).
        """
        n, m = self.prime_operation
        return PCSet(self.copy(utils.transpose_multiply(self.pitches, n, m)))

    @property
    def mpartner(self):
        """
        Return a PCSet for the M-partner of the given object.
        """
        return PCSet(self._transpose_multiply().prime)

    @staticmethod
    def forte_name(fname):
        """
        A static method that returns a PCSet object with the fort-name provided
        as a string argument.
        Returns an empty PCSet if the argument is not a string with a valid
        Forte name.
        """
        fset = utils.from_forte(fname)
        new_set = PCSet()
        if fset:
            new_set.pitches = fset
        return new_set

    @property
    def forte(self):
        """
        Returns the Forte name for the given object.
        """
        return utils.forte_name(self.pcint)

    @property
    def literal_compliment(self):
        """Returns a PCSet of the literal compliment of the given object."""
        return PCSet(self.copy([n for n in self.each_n() if n not in self.pcs]))

    @property
    def abstract_compliment(self):
        """Returns a PCSet of the abstract compliment of the given object."""
        return PCSet(self.literal_compliment.prime)

    @property
    def icv(self):
        """Returns the interval class vector of the given object."""
        return utils.icv(self._unique_pcs, self._mod)

    @property
    def zpartner(self):
        """
        Property that returns the Z-partner of the given object if it exists,
        otherwise returns None.
        """
        if self._mod > 12:
            return None
        if self._mod == 12:
            zint = Z_PARTNERS.get(self.pcint, None)
            if zint:
                return self.copy(utils.fromint(zint))
            else:
                return
        for each in self.each_card():
            if each.icv == self.icv:
                if each.prime._unique_pcs != self.prime._unique_pcs:
                    return self.copy(p)

    @property
    def invariance_vector(self):
        """
        A property that returns the list of (n, m) pairs that produce an
        invariant set via TnMm
        """
        return [(n, m) for n, m in self.each_tto() if self._transpose_multiply(n, m) == self]

    def supersets(self, limit=0):
        """
        Yields the supersets of the given object. Takes an optional argument,
        which limits the supersets to those with a cardinality <= the limit.
        With no argument, returns all supersets.
        """
        for sup in utils.supersets(self.ppc, self._mod, limit):
            yield self.copy(sup)

    def superprimes(self, limit=0):
        """
        Yields the supersets of the given object which have a unique set-class.
        Takes an optional limit argument with the same behavior as supersets()
        """
        for sup in self.supersets(limit):
            yield PCSet(self.copy(utils.fromint(sup.pcint)))

    def subsets(self, limit=0):
        """
        Yields the subsets of the given object. Takes an optional argument,
        which limits the subsets to those with a cardinality >= the limit.
        With no argument, returns all subsets.
        """
        for sub in utils.subsets(self.ppc, limit):
            yield self.copy(sub)

    def subprimes(self, limit=0):
        """
        Yields the subsets of the given object which have a unique set-class.
        Takes an optional limit argument with the same behavior as subsets().
        """
        for sub in self.subsets(limit):
            yield PCSet(self.copy(utils.fromint(sub.pcint)))


class PCSet(PPCSetBase, PCBase):
    """
    A Class for pitch class sets which adds pitch class only methods
    """

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
            self.pitches = other.pitches


class PSet(PPCSetBase):
    """A class for pitch sets, which adds pitch set only methods."""
    pass


class InvalidTTO(Exception):
    pass


def transpose(a, n):
    return a.copy(utils.transpose(a.pitches, n))

def invert(a, n=0):
    return a.copy(utils.invert(a.pitches, n))

def multiply(a, m=5):
    if a.__class__ == PSet:
        raise InvalidTTO('Pitch sets can not be operated on with TnMm')
    return a.copy(utils.multiply(a.pcs, m))

def transpose_multiply(a, n, m=5):
    if a.__class__ == PSet:
        raise InvalidTTO('Pitch sets can not be operated on with TnMm')
    return a.copy(utils.transpose_multiply(a.pcs, n, m))
