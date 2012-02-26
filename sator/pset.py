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
        ts = ts.lower()
        new = self.copy()
        for t in ts:
            if t == 'p':
                new = new.P()
                yield new
            if t == 'l':
                new = new.L()
                yield new
            if t == 'r':
                new = new.R()
                yield new
            if t == 's':
                new = new.S()
                yield new
            if t == 'n':
                new = new.N()
                yield new
            if t == 'h':
                new = new.H()
                yield new

    def cycle(self, ts):
        """
        Cycle through a list of transformations until the 
        """
        if not isinstance(ts, str):
            raise Exception('Cycle method only accepts a string')
        ts = ts.lower()
        current = self.copy()
        while True:
            for each in self.neo(ts):
                self[:] = each
                yield each
                if each.uo_pcs == current.uo_pcs:
                    self[:] = current
                    break
            if self[:] == current:
                break
