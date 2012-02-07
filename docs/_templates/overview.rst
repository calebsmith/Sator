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
These arguments can be integers, lists, tuples, or another ToneRow, PCSet, or PSet object.
Any of the following are both valid and equivalent::

    a = PSet([0, 2, 4, 6, 8])
    a = PSet(0, 2, 4, 6, 8)
    a = PSet(0, [2, 4], 6, 8)
    b = PSet(a)

The constructors also take several optional keyword arguments. For further details, refer to :ref:`constructor_options`

For more information about how pitch/pitch class data is stored and retrieved and how to instantiate objects from objects of other classes refer to :ref:`data_inspection`

Operating on Tone Row and Pitch/Pitch Class objects
---------------------------------------------------

Each of these objects can be iterated over, has a length, and with the exception of tone rows, can have additional pitches or pitch classes added or removed from them.
Each class also supports an insert and copy method.
The following example introduces an overview of the supported operators:: 

    a = PCSet([0, 3, 9], ordered=True)
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
    a.insert(0, 10)
    print a
    Out: [10, 0, 9, 11]
    b = a.copy()
    print b
    Out: [10, 0, 9, 11]

Refer to :ref:`operators` for more specifics on these operators.

TTO's
-----

At the heart of atonal music are the twelve tone operators, or TTO's. Each of sator's classes have methods for these, which are detailed at :ref:`ttos`

Below is a simple example of using each to modify a PCSet in place::

    a = PCSet(0, 1, 3)
    a.i()
    print a
    Out: [0, 9, 11]
    a.t(6)
    print a
    Out: [3, 5, 6]
    a.m()
    Out: [1, 3, 6]
    a.t_m(6, 7)
    print a
    Out: [0, 1, 3]

Attributes, Generators, and Properties
--------------------------------------

Sator core class objects have various boolean attributes such as ordered and multiset. They also have several property and generator methods. For more information on each topic, refer to the relevant links below:

:ref:`attributes`

:ref:`generators`

:ref:`properties`

Tone Rows
---------

ToneRow objects share many of the same methods as PCSet and PSet methods, but sometimes these methods have different or limited meaning.
ToneRow objects also have many unique methods such as: P, R, I, RI, M, MI, RM, RMI, and swap.

Refer to :ref:`tone_rows` for more information

Similarity Relations
--------------------

Similarity relations are imported from sator.sim and are used to make various kinds of comparisons between pitch or pitch class sets. For example::

    from sator.core import PCSet
    from sator.sim import m, c, z
    a = PCSet(0, 1, 2, 4, 7, 9)
    b = PCSet(0, 1, 3, 5, 6, 8)    
    print c(a, b)
    Out: True
    print z(a, b)
    Out: True
    print m(a, b)
    Out: False

Refer to :ref:`similarity_relations` for more information.
