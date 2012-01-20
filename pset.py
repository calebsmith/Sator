#!/usr/bin/env python
from itertools import count, izip

import utils
from const import HIGH_PITCH_LIMIT, LOW_PITCH_LIMIT, Z_PARTNERS


def transpose(pitches, sub_n=0):
    return [pitch + sub_n for pitch in pitches]

def invert(pitches, sub_n=0):
    return transpose(multiply(pitches, -1), sub_n)

def multiply(pitches, sub_m):
    return [pitch * sub_m for pitch in pitches]

def transpose_multiply(pitches, sub_n, sub_m):
    result = multiply(pitches, sub_m)
    return transpose(result, sub_n)

class SetRowBase():
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
            self.__add__(args[0])
        elif len(args) > 1:
            for arg in args:
                self.__add__(arg)

    def __add__(self, other):
        ps = other        
        if isinstance(other, (int, long)):
            ps = [other]
        if isinstance(other, set):
            ps = [int(num) for num in other]
        self.pitches.extend(ps)
        if not self._multiset:
            self.pitches = self._rm_dupes(self.pitches)
        return self

    def __eq__(self, other):
        """Compare equality between a PSet/PCSet and another object"""

        #Are we comparing pitches as ordered lists or set membership?
        if not self._ordered and isinstance(other, (tuple, list)):
            other = set(other)
        #Is the other a PSet/PCSet or builtin ?
        if isinstance(other, (SetRowBase, PSet, PCSet)):
            return self.ppc == other.ppc
        if isinstance(other, (int, long)):
            return self.ppc == [other]
        if isinstance(other, (tuple, list)):
            return self.ppc == list(other)
        if isinstance(other, set):
            return set(self.ppc) == other
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
        except IndexError:
            return None

    def __setitem__(self, key, value):
        self.pitches[key] = value

    def __iter__(self):
        for p in self.ppc:
            yield p

    def __repr__(self):
        return str(self.ppc)

    def copy(self, pitches=None):
        if pitches is None:
            pitches = self.pitches
        new = self.__class__(pitches, mod=self._mod, ordered=self._ordered,
                             multiset=self._multiset)
        if isinstance(self, PSetBase):
            new.canon(self._canon_t, self._canon_i, self._canon_m)
        new._default_m = self._default_m
        return new

    def insert(self, place, pitch):
        try:
            pitches = self.pitches[:place]
            pitches.append(pitch)
            pitches.extend(self.pitches[place:])
            self[:] = pitches
        except IndexError:
            self.pitches.append(pitch)

    def clear(self):
        self[:] = []

    def mod(self, new_mod):
        self._mod = new_mod

    def default_m(self, new_m):
        self._default_m = new_m

    def multiset(self, value):
        self._multiset = True if value else False

    def ordered(self, value):
        self._ordered = True if value else False

    @property
    def pcs(self):
        return [pitch % self._mod for pitch in self.pitches]

    @property
    def pc_set(self):
        return set(self.pcs)

    @property
    def pitch_set(self):
        return set(self.pitches)

    @property
    def uo_pcs(self):
        output = self.pcs[:]
        output.sort()
        return output

    @property
    def unique_pcs(self):
        output = list(self.pc_set)
        output.sort()
        return output

    @property
    def uo_pitches(self):
        output = self.pitches[:]
        output.sort()
        return output

    @property
    def ppc(self):
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
        new = []
        [new.insert(ps.index(num), num) for num in ps[:] if num not in new]
        return new

    def each_n(self):
        for num in xrange(0, self._mod):
            yield num

    def _transpose(self, sub_n=0):
        return self.copy(transpose(self.pitches, sub_n))

    def _invert(self, sub_n=0):
        return self.copy(invert(self.pitches, sub_n))

    def _transpose_multiply(self, sub_n=0, sub_m=0):
        if not sub_m:
            sub_m = self._default_m
        result = [pc % self._mod for pc in \
                  transpose_multiply(self.pitches, sub_n, sub_m)]
        return self.copy(result)

    def t(self, sub_n):
        self[:] = (self._transpose(sub_n)).pitches

    def i(self, sub_n=0):
        self[:] = (self._invert(sub_n)).pitches

    @property
    def t_rotations(self):
        return [self.copy(rot) for rot in [self._transpose(n) \
                                           for n in self.each_n()]]

    @property
    def i_rotations(self):
        return [self.copy(rot) for rot in [self._invert(n) \
                                           for n in self.each_n()]]

    @property
    def m_rotations(self):
        return [self.copy(rot) for rot in [self._transpose_multiply(n) \
                                           for n in self.each_n()]]

    @property
    def mi_rotations(self):
        return [self.copy(rot) for rot in [self._transpose_multiply(n, self._default_m * -1) \
                                           for n in self.each_n()]]
    @property
    def all_rotations(self):
        result = []
        result.extend(self._t_rotations())
        result.extend(self._i_rotations())
        result.extend(self._m_rotations())
        result.extend(self._mi_rotations())
        return result

    @property
    def literal_compliment(self):
        return self.copy([n for n in self.each_n() if n not in self.pcs])

    def c(self):
        self[:] = self.literal_compliment.pitches


class PCBase():
    """Base class for Tone rows and PC sets"""

    def m(self, sub_n=0):
        self[:] = (self._transpose_multiply(sub_n, self._default_m)).pitches

    def mi(self, sub_n=0):
        sub_m = self._mod - self._default_m
        self[:] = (self._transpose_multiply(sub_n, sub_m)).pitches
        
    def t_m(self, sub_n=0, sub_m=0):
        if not sub_m:
            sub_m = self._default_m
        self[:] = (self._transpose_multiply(sub_n, sub_m)).pitches


class ToneRow(SetRowBase, PCBase):
    _modulus = 12

    class IncompleteException(Exception):
        pass

    def __init__(self, *args, **kwargs):
        kwargs.update({'multiset': False, 'ordered': True})
        SetRowBase.__init__(self, *args, **kwargs)
        if len(self.ppc) < self._mod:
            msg = 'Tone rows must be instantiated with a number of ' + \
                  'pitches or pcs equal to their modulus'
            raise self.IncompleteException(msg)

    @property
    def P(self):
        return self

    @property
    def R(self):
        ppc = self.ppc
        ppc.reverse()
        return self.copy(ppc)

    @property
    def I(self):
        return self._invert()

    @property
    def RI(self):
        return self.R.I

    def ordered(self, order):
        self._ordered = True

    def multiset(self, multi):
        self._multiset = False


class PSetBase(SetRowBase):
    """Base class for PCSet and PSet"""

    _canon_t = True
    _canon_i = True
    _canon_m = False

    def __len__(self):
        return len(self.ppc)

    def canon(self, t, i, m):
        self._canon_t = 1 if t else 0
        self._canon_i = 1 if i else 0
        self._canon_m = 1 if m else 0

    def setint(self, integer=None):
        if integer:
            self[:] = utils.fromint(integer)
        else:
            return utils.setint(self.unique_pcs)

    @property
    def pcint(self):
        return utils.setint(self.prime)

    def each_card(self):
        bins = []
        for num in range(0, self._mod):
            bins.append(1) if num < self.cardinality else bins.append(0)
        maxint = 0
        minint = 0
        for index, bin in enumerate(bins):
            if bin:
                minint += 2 ** index
                maxint += 2 ** (self._mod - index - 1)
        other = self.copy()
        for num in range(minint, maxint + 1):
            other = other.fromint(num)
            if other.cardinality == self.cardinality:
                yield other

    def each_set(self):
        return (self.copy(utils.fromint(integer)) \
                for integer in xrange(0, 2 ** self._mod))

    def each_prime(self):
        return (each for each in self.each_set() if each.prime == each)

    @property
    def cardinality(self):
        return len(self.pc_set)

    def _t_rotations(self):
        return (PCSet.copy(rot) for rot in [self._transpose(n) \
                                            for n in self.each_n()])

    def _i_rotations(self):
        return (PCSet.copy(rot) for rot in [self._invert(n) \
                                            for n in self.each_n()])
    def _m_rotations(self):
        return (PCSet.copy(rot) for rot in [self._transpose_multiply(n) \
                                            for n in self.each_n()])

    def _mi_rotations(self):
        return (PCSet.copy(rot) for rot in [self._transpose_multiply(n, self._default_m * -1) \
                                            for n in self.each_n()])

    @property
    def rotation_ints(self):
        return [[utils.setint(pcs) for pcs in rotation] \
            for rotation in self._rotations()]

    def _rotations(self):
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
        The (n, m) pair to perform on this set in order to obtain the prime
        """
        low_vals =[min(izip(operation, count())) \
            for operation in self.rotation_ints]
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
        n, m = self.prime_operation
        return PCSet(self.copy(transpose_multiply(self.pitches, n, m)))

    @property
    def mpartner(self):
        return PCSet(self._transpose_multiply().prime)

    def forte(self, fname=None):
        if fname:
            fset = utils.from_forte(fname)
            if fset:
                self[:] = fset
        else:
            return utils.forte_name(self.pcint)

    @property
    def icv(self):
        return utils.icv(self.unique_pcs, self._mod)

    @property
    def zpartner(self):
        if self._mod > 12:
            return None
        if self._mod == 12:
            zint = Z_PARTNERS.get(self.pcint, None)
            if zint:
                return self.copy(utils.fromint(zint))
            else:
                return
        for each in self.each_card():
            p = each.prime.unique_pcs
            if each.icv == self.icv and p != self.prime.unique_pcs:
                return self.copy(p)

    def supersets(self, limit=0):
        for sup in utils.supersets(self.ppc, self._mod, limit):
            yield self.copy(sup)

    def superprimes(self, limit=0):
        for sup in self.supersets(limit):
            yield PCSet(self.copy(utils.fromint(sup.pcint)))

    def subsets(self, limit=0):
        for sub in utils.subsets(self.ppc, limit):
            yield self.copy(sub)

    def subprimes(self, limit=0):
        for sub in self.subsets(limit):
            yield PCSet(self.copy(utils.fromint(sub.pcint)))


class PCSet(PSetBase, PCBase):
    """
    A pitch class set which adds pitch class only methos
    """

    def __sub__(self, other):
        """Remove all instances of a given pc from a pcset"""
        rm_pcs = other
        if isinstance(other, (int, long)):
            rm_pcs = [other]
        if isinstance(other, set):
            rm_pcs = [int(num) for num in other]
        for pc in rm_pcs:
            self._rm_pc(pc)
        return self

    def _rm_pc(self, pc):
        while pc in self.pitches:
            self.pitches.remove(pc)

    def z(self):
        other = self.zpartner
        if other:
            self = other.copy()

    @property
    def abstract_compliment(self):
        return self.literal_compliment.prime


class PSet(PSetBase):
    """A pitch set, which adds pitch set only methods."""

    _ordered = True

    def remove(self, key):
        try:
            self[:] = self[:key] + self[key + 1:]
        except IndexError:
            pass
