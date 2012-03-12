#!/usr/bin/env python
from __future__ import division
from itertools import combinations

from sator.setbase import SetBase


class PSet(SetBase):
    """A class for pitch sets, which adds pitch set only methods."""

    pitchset = True

    class Mod12Only(Exception):
        pass

    class NotNeoR(Exception):
        """Can not be transformed by a Neo-Riemannian operator"""
        pass

    def checkMod12(f):
        def _(*args, **kwargs):
            self = args[0]
            if self._mod != 12:
                raise self.Mod12Only('The modulus must be 12 for this method')
            return f(*args, **kwargs)
        _.__name__ = f.__name__
        _.__module__ = f.__module__
        _.__doc__ = f.__doc__
        return _

    def neo_oper(f):
        def _(*args, **kwargs):
            self = args[0]
            roots = self.root
            unique_roots = set((root % self._mod for root in roots))
            if len(roots) == 0 or len(unique_roots) > 1:
                return f(self)
            try:
                thirds, major = self._thirds(roots[0])
            except self.NotNeoR:
                return f(self)
            try:
                fifths = self._fifths(roots[0])
            except self.NotNeoR:
                return f(self)
            root_indexes = [index for index, p in enumerate(self[:]) if p in roots]
            return f(self, major, root_indexes, thirds, fifths, *args[1:], **kwargs)
        _.__name__ = f.__name__
        _.__module__ = f.__module__
        _.__doc__ = f.__doc__
        return _

    @property
    @checkMod12
    def root(self):
        """
        Find the root(s) of an ordered pitch set, using Paul Hindemith's method
        """
        if not self[:]:
            return []
        totals = {}
        for p in self[:]:
            totals[p] = 0
        for each in combinations(self[:], 2):
            diff = abs(each[1] - each[0]) % self._mod
            # Ignore tritones.
            if diff == 6:
                continue
            rating = diff if diff < self._mod // 2 else self._mod - diff
            # The root of these three is the lower note, otherwise higher
            lower, higher = (0, 1) if each[1] > each[0] else (1, 0)
            key = each[lower] if diff in [7, 4, 3] else each[higher]                
            totals[key] = rating + totals.get(key, 0)
        # Sort by rating descending and truncate
        totals = sorted(totals.items(), key= lambda x: x[1])
        totals.reverse()
        current = totals[0][1]
        for index, total in enumerate(totals):
            if total[1] < current:
                index -= 1
                break
            current = total[1]
        return sorted([total[0] for total in totals[0:index + 1]])

    def _thirds(self, root):
        root_pc = root % self._mod
        thirds = []
        major = None
        for index, pc in enumerate(self.pcs):
            if pc == root_pc + 3 or pc == root_pc - 9:
                major = False
                thirds.append((index, major))
            if pc == root_pc + 4 or pc == root_pc - 8:
                major = True
                thirds.append((index, major))
        if len(thirds) < 1:
            raise self.NotNeoR('There is no identifiable third.')
        majors = [major for third, major in thirds]
        if True in majors and False in majors:
            raise self.NotNeoR('There are major and minor thirds.')
        return([third for third, major in thirds], major)

    def _fifths(self, root):
        root_pc = root % self._mod
        fifths = []
        for index, pc in enumerate(self.pcs):
            if pc == root_pc + 7 or pc == root_pc - 5:
                fifths.append(index)
        if len(fifths) < 1:
            raise self.NotNeoR('There is no identifiable fifth.')
        return fifths

    @checkMod12
    @neo_oper
    def P(self, *args):
        if not args:
            return self.copy()
        major, roots, thirds, fifths = args[:4]
        new = self.copy()
        for third in thirds:
            new[third] = new.pitches[third] - 1 \
                if major else new.pitches[third] + 1
        return new

    @checkMod12
    @neo_oper
    def L(self, *args):
        if not args:
            return self.copy()
        major, roots, thirds, fifths = args[:4]
        new = self.copy()
        if major:
            for root in roots:
                new[root] = new.pitches[root] - 1
        else:
            for fifth in fifths:
                new[fifth] = new.pitches[fifth] + 1
        return new

    @checkMod12
    @neo_oper
    def R(self, *args):
        if not args:
            return self.copy()
        major, roots, thirds, fifths = args[:4]
        new = self.copy()
        if major:
            for fifth in fifths:
                new[fifth] = new.pitches[fifth] + 2
        else:
            for root in roots:
                new[root] = new.pitches[root] - 2
        return new

    def H(self):
        """Hexatonic Pole (Cohn)"""
        return self.P().L().P()

    def N(self):
        """Nebenverwandt"""
        return self.R().L().P()

    def S(self):
        """Slide"""
        return self.L().P().R()

    def neo(self, ts):
        if not isinstance(ts, str):
            raise Exception('Neo method only accepts a string')
        ts = ts.upper()
        new = self.copy()

        def get_funcs(obj):
            fs = [obj.P, obj.L, obj.R, obj.H, obj.N, obj.S]
            return fs, [f.__name__ for f in fs]

        fs, fnames = get_funcs(self)
        for t in ts:
            if t in fnames:
                new = fs[fnames.index(t)]()
                yield new
                fs, fnames = get_funcs(new)

    def transform(self, ts):
        """
        Returns the given object after performing the list of transformations
        given as a string argument.
        If the string is empty, the given object is returned.
        """
        if not isinstance(ts, str):
            raise Exception('Transform method only accepts a string')
        t = None
        for t in self.neo(ts):
            pass
        return t if t is not None else self.copy()

    def cycle(self, ts):
        """
        Cycle through a list of transformations until the original set is
        reached.
        """
        if not isinstance(ts, str):
            raise Exception('Cycle method only accepts a string')
        ts = ts.lower()
        current = self.copy()
        while True:
            for each in self.neo(ts):
                self[:] = each
                yield each
                if each._unique_pcs == current._unique_pcs:
                    self[:] = current
                    break
            if self[:] == current:
                break

    def paths(self, other):
        """
        A breadth first tree search to find the shortest path(s) from the given
        object to another. Takes one argument as the goal set, returns a list
        with one or more strings indicating the transformations between the
        given set and the goal set.
        """
        # Verify that other is a transformation of self
        current = other.copy()
        current.canon(True, True, False)
        if self.prime != current.prime:
            raise self.NotNeoR('Neo Riemannian operations will never transform this set into the goal set.')

        # Make branches from the curret node following P, L and R
        def get_branches(obj):
            return ((f(), f) for f in (obj.P, obj.L, obj.R))

        def prune_append(obj, tree, first=True):
            # return paths when goal is reached, otherwise prune current ones
            # and append the next transformation, then check again
            if not first:
                # Only prune after the first time through
                for name in tree.keys():
                    obj = tree.pop(name)
                    for branch, f in get_branches(obj):
                        tree[name + f.__name__] = branch
            paths = [name for name, obj in tree.items() \
                     if obj._pc_set == other._pc_set]
            return paths if paths else prune_append(other, tree, first=False)

        # Make a tree with keys p, l, and r and values P(), L(), and R()
        tree = {}
        for branch, f in get_branches(self):
            tree[f.__name__] = branch
        return prune_append(self, tree)
