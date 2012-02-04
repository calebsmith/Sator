.. _ttos:

=====
TTO's
=====

TTO is an acronym for "Twelve Tone Operators."

To return new set or row instances modified by a TTO, import and use the following functions:

>>> from sator.core import transpose, invert, multiply, transpose_multiply

The table below shows each function's assocatied TTO, arguments and defaults. Arguments enclosed in brackets are optional, and use the default if not provided.

====================  ==============  =============  ========
Name                  TTO             Arguments      Defaults
====================  ==============  =============  ========
transpose             Tn              object, n      NA
invert                TnI             object, [n]    n=0
multiply              T0Mm            object, [m]    m=5
transpose_multiply    TnMm            object, n, m   NA
=============================================================

The following are some examples of each::

    a = PCSet(0, 4, 9)
    b = transpose(a, 1)
    print b
    Out: [1, 5, 10]
    c = invert(a)
    print c
    Out: [0, 3, 8]
    d = transpose_multiply(a, 3, 7)
    print d
    Out: [3, 6, 7]

* Multiply and transpose_multiply will raise a InvalidTTO exception if they are called with a PSet
