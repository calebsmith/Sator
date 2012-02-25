#!/usr/bin/env python

import sator.utils as utils

from sator.tonerow import ToneRow
from sator.pset import PSet
from sator.pcset import PCSet


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
