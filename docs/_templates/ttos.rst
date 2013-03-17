.. _ttos:

=====
TTO's
=====

TTO is an acronym for "Twelve Tone Operators."

Using TTO's in place
--------------------

To obtain a new ToneRow, PCSet, or PSet by TTO, use the t, i, m, mi, and t_m methods.
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
    print a.t(1)
    Out: [1, 5, 10]
    print a.i()
    Out: [0, 3, 8]
    print a.m()
    print a
    Out: [7, 10, 11]
    print a.mi()
    Out: [1, 5, 10]
    print a.t_m(1, 11)
    Out: [0, 3, 8]
