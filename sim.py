#!/usr/bin/env python
"""
Module for similarity relations/functions between two pitch or pitch class sets
"""

"""Functions for determining if the two sets are m, z, or c partners"""

def z(a, b):
    return a.zpartner == b.prime

def c(a, b):
    return a.abstract_compliment == b.prime

def m(a, b):
    return a.mpartner == b.prime

def zc(a, b):
    return z(a, b) and c(a, b)
