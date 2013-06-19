#!/usr/bin/env python
"""
Module for similarity relations/functions between two pitch or pitch class sets
"""

from __future__ import division


"""Helper Functions and Exceptions"""


class DifferentModuliException(Exception):
    pass


def _check_mod(a, b):
    """
    Raise an exception if the sets do not have the same modulus. Most
    functions are undefined if the input sets have different moduli.
    """
    err_msg = 'Similarity relations between sets of different moduli are undefined'
    if a.mod() != b.mod():
        raise DifferentModuliException(err_msg)


def require_same_modulus(f):

    def _(a, b, *args, **kwargs):
        _check_mod(a, b)
        return f(a, b, *args, **kwargs)
    return _


"""Functions for determining if the two sets are m, z, or c partners"""


@require_same_modulus
def z(a, b):
    return a.zpartner == b.prime


@require_same_modulus
def c(a, b):
    return a.abstract_compliment == b.prime


@require_same_modulus
def m(a, b):
    return a.mpartner == b.prime


@require_same_modulus
def zc(a, b):
    return z(a, b) and c(a, b)


""" Similarity Functions """


@require_same_modulus
def iv(a, b):
    """
    How many of each ordered interval is expressed from the PC's of a to those
    of b. -Robert Morris' IV(a, b) as described in
    "Composition with Pitch Classes" 1987
    """
    ivect = dict((n, 0) for n in a.each_n())
    for pc in a.uo_pcs:
        for n in a.each_n():
            lookfor = (pc + n) % a.mod()
            if lookfor in b.pcs:
                ivect[n] += 1
    return list(ivect.values())


@require_same_modulus
def sim(a, b):
    """
    The sum of differences between the icvs of sets a and b (excluding icv0
    which represents the cardinality of each set)
    - Robert Morris SIM(a, b)
    """
    return sum(abs(ic_a - ic_b) for ic_a, ic_b in zip(a.icv[1:], b.icv[1:]))


@require_same_modulus
def asim(a, b, rational=False):
    """
    The sum of differences between the icvs of sets a and b (excluding icv0)
    divided by the total icvs in both sets, which is equal to the highest
    possible difference.

    Takes 'rational', which returns a rational number in the form of a two
    tuple when True. Defaults to rational=False

    - Robert Morris ASIM(a, b)
    """
    sim = 0
    asim = 0
    for ic_a, ic_b in zip(a.icv[1:], b.icv[1:]):
        sim += abs(ic_a - ic_b)
        asim += ic_a + ic_b
    return (sim, asim) if rational else sim / asim
