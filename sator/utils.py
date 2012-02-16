#!/usr/bin/env python
from const import FORTE_NAMES, FORTE_INTS

def transpose(pitches, sub_n=0):
    """
    Given a list of pitches and n, returns an object of the same type after Tn
    """
    return [pitch + sub_n for pitch in pitches]

def invert(pitches, sub_n=0):
    """
    Given an object and n, returns an object of the same type after TnI.
    If n is not provided, n is assumed to be 0
    """
    return transpose(multiply(pitches, -1), sub_n)

def multiply(pitches, sub_m):
    """
    Given an object and n, returns an object of the same type after TnMm,
    where m is required. (For mod 12, m is usually 5.)
    """
    return [pitch * sub_m for pitch in pitches]

def transpose_multiply(pitches, sub_n, sub_m):
    """
    Given an object, n, and m, returns an object of the same type after TnMm.
    All arguments are required.
    """
    result = multiply(pitches, sub_m)
    return transpose(result, sub_n)

def setint(pcs):
    """Find the integer representation of an unordered PC set"""
    return sum([2 ** pc for pc in pcs])

def fromint(integer):
        result = []
        limit = len(bin(integer)) - 2
        each_digit = [2 ** n for n in xrange(limit, -1, -1)]
        for index, digit in enumerate(each_digit):
            if integer >= digit:
                integer -= digit
                result.append(limit - index)
        result.sort()
        return result

def forte_name(setint):
	return FORTE_NAMES.get(setint)

def forte_int(fname):
    return FORTE_INTS.get(fname)       

def from_forte(fname):
    try:
        return fromint(forte_int(fname))
    except:
        return None

def icv(pcs, mod=12):
    icv_length = (mod / 2) + 1;
    result = [0 for num in xrange(0, icv_length)]
    icvs = xrange(0, icv_length)
    for pc in pcs:
        for cv in icvs:
            if (pc + cv) % mod in pcs:
                result[cv] += 1
    if icv_length - 1 == mod / 2.0:
        result[icv_length - 1] = result[icv_length - 1] / 2
    return result

def _supers_n_plus_1(pcs, mod):
    for index in xrange(0, mod):
        if index not in pcs:
            result = pcs[:]
            result.append(index)
            yield result

def _subs_n_minus_1(pcs):
    for index in xrange(0, len(pcs)):
        yield [pc for i, pc in enumerate(pcs) if i != index]

def supersets(pcs, mod, limit=0):
    if not limit:
        limit = mod
    # FIXME: Raise a useful exception rather than just yielding None
    if limit <= len(pcs):
        yield
    else:
        for sup in _supers_n_plus_1(pcs, mod):
            current = sup
            yield current
            if len(current) < mod and len(current) < limit:
                for pcs in supersets(current, mod, limit):
                    yield pcs

def subsets(pcs, limit=0):
    # FIXME: Raise a useful exception rather than just yielding None
    if limit >= len(pcs):
        yield
    else:
        for sub in _subs_n_minus_1(pcs):
            current = sub
            yield current
            if len(current) > limit:
                for pcs in subsets(current, limit):
                    yield pcs
