.. _overview:

========
Overview
========

In this overview, we will discuss the most essential parts of sator, but it is assumed that the reader is well versed in atonal theory.

Constructing Tone Rows and Pitch/Pitch Class Sets
-------------------------------------------------

The core module in sator contains the three essential classes for instantiating
and manipulating tone rows, pitch sets, and pitch class sets.

To construct rows and sets, import the ToneRow, PCSet, and PSet classes from
the core module as follows::

    from sator.core import ToneRow, PCSet, PSet

To instantiate an empty pitch set, or pitch class set, use::

    a = PSet()
    b = PCSet()

* ToneRow objects are excluded from the above example because by definition, they cannot be empty.

The classes' constructors take an optional number of positional arguments as pitches or pc's.
These arguments can be integers, lists, tuples, or another tone row, pitch class set, or pitch set object.
Any of the following are both valid and equivalent::

    a = PSet([0, 2, 4, 6, 8])
    a = PSet(0, 2, 4, 6, 8)
    a = PSet(0, [2, 4], 6, 8)
    b = PCSet(a)

The constructors also take several optional keyword arguments. For further details, refer to :ref:`constructor_options`

When constructing a pitch set from a pitch class set and converting back to a pitch set, care must be taken so that the the pitch data remains unmolested.
In this example, pitch set c will contain the pitch classes of b, rather than the pitches from a::

    a = PSet(0, 25, -1)
    b = PCSet(a)
    c = PSet(b)
    print c
    Out: [0, 1, 11]

To maintain pitch data, use the .pitches property of the PCSet explicitly::

    c = PSet(b.pitches)
    print c
    Out: [0, 25, -1]

To understand this distinction and the importance of the .ppc property refer to :ref:`data_inspection`

Operating on Tone Row and Pitch/Pitch Class objects
---------------------------------------------------

Each of these objects can be iterated over, has a length, and with the exception of tone rows, can have additional pitches or pitch classes added or removed from them.
The following example introduces an overview of the supported operators:: 

    a = PCSet([0, 3, 9])
    a = a + 11
    a = a - 3
    print a
    Out: [0, 9, 11]
    for pc in a:
        print pc
    Out: 0
    Out: 9
    Out: 11
    print len(a)
    Out: 3

Similarly, pitch and pitch sets, but not tone rows, have an insert method. This is meaningful only for sets which have their ordered field set to True. Insert takes an index and a new pitch/pitch class as it's arguments.
This method can be used as follows::

    a = PCSet([0, 4, 8], ordered=True)
    a.insert(1, 2)
    print a
    Out: [0, 2, 4, 8]

Refer to :ref:`operators` for more specifics on these operators, including some gotchas.
