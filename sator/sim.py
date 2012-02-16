#!/usr/bin/env python
"""
Module for similarity relations/functions between two pitch or pitch class sets
"""

from __future__ import division


"""Functions for determining if the two sets are m, z, or c partners"""

def z(a, b):
    return a.zpartner == b.prime

def c(a, b):
    return a.abstract_compliment == b.prime

def m(a, b):
    return a.mpartner == b.prime

def zc(a, b):
    return z(a, b) and c(a, b)


""" Similarity Functions """

def _check_mod(a, b):
    # Verify the sets have the same modulus. Most functions are defined if the
    # input sets are different moduli.
    return False if a.mod() == b.mod() else True

"""Robert Morris"""
def iv(a, b):
    """
    How many of each ordered interval is expressed from the PC's of a to those
    of b. -Robert Morris' IV(a, b) as described in
    "Composition with Pitch Classes" 1987
    """
    if _check_mod(a, b):
        return NotImplemented
    ivect = dict([(n, 0) for n in a.each_n()])
    for pc in a.uo_pcs:
        for n in a.each_n():
            lookfor = (pc + n) % a.mod()
            if lookfor in b.pcs:
                ivect[n] += 1
    return ivect.values()

def sim(a, b):
    """
    The sum of differences between the icvs of sets a and b (excluding icv0)
    - Robert Morris SIM(a, b)
    """
    if _check_mod(a, b):
        return NotImplemented
    # Skip the first interval class, which is the cardinality.
    return sum([abs(ic[0] - ic[1]) for ic in zip(a.icv[1:], b.icv[1:])])

def asim(a, b, rational=False):
    if _check_mod(a, b):
        return NotImplemented
    """
    The sum of differences between the icvs of sets a and b (excluding icv0)
    divided by the total icvs in both sets, which is equal to the highest
    possible difference.

    Takes the kwarg rational. If true, returns a rational number in the form of
    a two tuple.
    Defaults to rational=False

    - Robert Morris ASIM(a, b)
    """
    sim = asim = 0
    for ic in zip(a.icv[1:], b.icv[1:]):
        sim += abs(ic[0] - ic[1])
        asim += ic[0] + ic[1]
    return (sim, asim) if rational else sim / asim
