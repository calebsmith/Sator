.. _ttos:

=====
TTO's
=====

TTO is an acronym for "Twelve Tone Operators."

Using TTO's in place
--------------------

To modify a ToneRow, PCSet, or PSet by TTO in place, use the t, i, m, mi, and t_m methods.
The table below shows each method's associated TTO, arguments and defaults. Arguments enclosed in brackets are optional, and use the default if not provided.

======  =====  ===========  =========
Name    TTO    Arguments    Defaults
======  =====  ===========  =========
t       Tn     n            NA
i       TnI    [n]          n=0
m       TnM    [n]          n=0
mi      TnMI   [n]          n=0
t_m     TnMm   n, m         NA

======  =====  ===========  =========

* m, mi, and t_m are not possible for pitch sets. Therefore, these methods are only available for ToneRow and PCSet instances.

Below are some examples::

    a = PCSet(0, 4, 9)
    a.t(1)
    print a
    Out: [1, 5, 10]
    a.i()
    print a
    Out: [2, 7, 11]
    a.m()
    print a
    Out: [7, 10, 11]
    a.mi()
    print a
    Out: [1, 5, 10]
    a.t_m(1, 11)
    print a
    Out: [0, 3, 8]

Returning new instances via a TTO
---------------------------------

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
====================  ==============  =============  ========

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

* Multiply and transpose_multiply will raise an InvalidTTO exception if they are called with a PSet
