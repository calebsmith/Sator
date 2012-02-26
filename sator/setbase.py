#!/usr/bin/env python
from itertools import count, izip, combinations

import sator.utils as utils
from sator.const import Z_PARTNERS

from sator.setrowbase import SetRowBase, PCBase


class SetBase(SetRowBase):
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
            self[:].append(pitch)

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
        from sator.pcset import PCSet
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
        return(cls(utils.fromint(integer), mod=mod) for integer in xrange(0, 2 ** mod))

    @classmethod
    def each_prime_in_mod(cls, mod):
        return(each for each in cls.each_set_in_mod(mod) if each.prime == each)

    @classmethod
    def each_card_in_mod(cls, card, mod):
        """
        Same as the instance method but takes two args for cardinality and
        modulus respectively
        """
        return (cls(each, mod=mod) for each in combinations(cls.each_n_in_mod(mod), card))

    @classmethod
    def each_prime_in_card_mod(cls, card, mod):
        """
        Yields every unique prime form with a given cardinality in the given
        modulus
        """
        for each in combinations(cls.each_n_in_mod(mod), card):
            new = cls(each, mod=mod)
            if new.prime == new:
                yield new

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
        from sator.pcset import PCSet
        return (PCSet(self.copy(rot)) for rot in [self._transpose(n) \
                                                  for n in self.each_n()])

    def _i_rotations(self):
        """
        Same as the public method, but enforces that the returned objects are
        PCSets for use with the prime method.
        """
        from sator.pcset import PCSet
        return (PCSet(self.copy(rot)) for rot in [self._invert(n) \
                                                  for n in self.each_n()])

    def _m_rotations(self):
        """
        Same as the public method, but enforces that the returned objects are
        PCSets for use with the prime method.
        """
        from sator.pcset import PCSet
        return (PCSet(self.copy(rot)) for rot in [self._transpose_multiply(n) \
                                                  for n in self.each_n()])

    def _mi_rotations(self):
        """
        Same as the public method, but enforces that the returned objects are
        PCSets for use with the prime method.
        """
        from sator.pcset import PCSet
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
        from sator.pcset import PCSet
        n, m = self.prime_operation
        return PCSet(self.copy(utils.transpose_multiply(self.pitches, n, m)))

    @property
    def mpartner(self):
        """
        Return a PCSet for the M-partner of the given object.
        """
        from sator.pcset import PCSet
        return PCSet(self._transpose_multiply().prime)

    @staticmethod
    def forte_name(fname):
        """
        A static method that returns a PCSet object with the fort-name provided
        as a string argument.
        Returns an empty PCSet if the argument is not a string with a valid
        Forte name.
        """
        from sator.pcset import PCSet
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
        from sator.pcset import PCSet
        return PCSet(self.copy([n for n in self.each_n() if n not in self.pcs]))

    @property
    def abstract_compliment(self):
        """Returns a PCSet of the abstract compliment of the given object."""
        from sator.pcset import PCSet
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

    @property
    def ds(self):
        """
        Degrees of symmetry (number of Tn/TnI operations for which this set is
        invariant)
        """
        total = 0
        for m in (1, -1):
            for n in self.each_n():
                if self._transpose_multiply(n, m) == self:
                    total += 1
        return total

    def m_vector(self, m):
        """
        Find David Lewin's M-vector.
        (Also described in Composition with Pitch Classes - Robert Morris)
        Finds the number of each set-class with cardinality m which are
        subsets of a given pitch class. The ICV is equivalent to the m-vector
        of a pitch class when m is 2.
        """
        if m > self._mod:
            return
        from sator.pcset import PCSet
        pc_set = self._pc_set
        vectors = {}
        for index, each in enumerate(self.__class__.each_card_in_mod(m, self._mod)):
            e_prime = each.pcint
            old_value = vectors.get(e_prime, 0)
            to_add = 1 if pc_set.issuperset(each._pc_set) else 0
            vectors[e_prime] = old_value + to_add
        return sorted([(PCSet.fromint(pcint), total) \
                       for pcint, total in vectors.items()],
                       key = lambda x: x[0].pcint)

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
        from sator.pcset import PCSet
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
        from sator.pcset import PCSet
        for sub in self.subsets(limit):
            yield PCSet(self.copy(utils.fromint(sub.pcint)))

    class OnlySetableMethod(Exception):
        """
        Exception to raise if the argument used can not be made into a set
        """
        pass

    def args_are_sets(f, *args, **kwargs):
        """ Decorator to help with set methods. Ensures that args are sets"""
        def _(*args, **kwargs):
            from sator.pcset import PCSet
            from sator.pset import PSet
            ints = set()
            for arg in args[1:]:
                if isinstance(arg, (PCSet, PSet)):
                    arg = arg._pc_set
                    continue
                if isinstance(arg, (list, tuple)):
                    arg = set(arg)
                    continue
                if isinstance(arg, set):
                    continue
                err_msg = 'Only lists, tuples, sets, PSet, and PCSet objects can be used as arguments for this method'
                raise args[0].OnlySetableMethod(err_msg)
            return f(*args, **kwargs)
        _.__doc__ = f.__doc__
        _.__name__ = f.__name__
        return _

    @args_are_sets
    def union(self, other):
        """
        Return an instance that represents the union of the current PSet
        or PCSet and another as the first and only positional argument.
        """
        return self.copy(self._pc_set.union(other))

    @args_are_sets
    def intersection(self, other):
        """
        Return an instance that represents the intersection of the current
        PSet or PCSet and another as the first and only positional argument.
        """
        return self.copy(self._pc_set.intersection(other))

    @args_are_sets
    def difference(self, other):
        """
        Return an instance that represents the difference of the current
        PSet or PCSet and another as the first and only positional argument.
        """
        return self.copy(self._pc_set.difference(other))

    @args_are_sets
    def symmetric_difference(self, other):
        """
        Return an instance that represents the symmetric_difference of the
        current PSet or PCSet and another as the first and only positional
        argument.
        """
        return self.copy(self._pc_set.symmetric_difference(other))

    @args_are_sets
    def issubset(self, other):
        """
        Return True if the current PSet or PCSet is a subset of another object
        taken as the first and only positional argument, otherwise False.
        """
        return self._pc_set.issubset(other)

    @args_are_sets
    def issuperset(self, other):
        """
        Return True if the current PSet or PCSet is a superset of another
        object taken as the first and only positional argument, otherwise False
        """
        return self._pc_set.issuperset(other)

    @args_are_sets
    def isdisjoint(self, other):
        """
        Return True if the current PSet or PCSet is disjoint with another
        object taken as the first and only positional argument, otherwise False
        """
        return self._pc_set.isdisjoint(other)
