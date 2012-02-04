.. _data_inspection:

===============
Data Inspection
===============

ToneRow, PCSet and PSet instances store all of their data in the pitches field, while other data such as pitch classes are handled as properties, which dervive from pitches.
For example, a PCSet may have the pitches [0, 13, -1] and it's pcs property would output [0, 1, 11].

The following table shows the available properties/fields along with a description for each.

===========  =============
Property     Description
===========  =============
pitches      An ordered list of pitches
pcs          An ordered list of pitch classes
uo_pitches   An unordered list of pitches
uo_pcs       An unordered list of pitch classes
ppc          The ordered or unordered pitches or pitch classes, determined by the class and the ordered attribute

The following rules are used to determine what the ppc property should output:

 * Output pitches for PSets, pitch classes for everthing else
 * Output the pitches or pitch classes in order if the ordered attribute is set to True
 * Output the pitches or pitch classes in ascending order if the ordered attribute is set to False (Default)

Each class uses str(ppc) for its __repr__, so ppc is used to output an object's basic representation.
Unless another property is used explicitly, an object's pitches field is used for copying or instantiating another object. For example::

    a = PSet(0, -1, 18)
    b = PCSet(a)
    c = PSet(b)
    print c
    Out: [0, -1, 18)
    print c == a
    Out: True

However, if a pitch collection contains different pitches of the same pitch class, data can be lost in conversion as in the following example::

    a = PSet(0, 6, 18)
    b = PCSet(a)
    c = PSet(b)
    print c
    Out: [0, 6]
    print c == a
    Out: False

ToneRows can also be instantiated from PSet or PCSet instances, but they must have each possible pitch class given the modulus of the object.
When instantiating a new ToneRow with a modulus other than 12, it must be specified as a kwarg as in the following example::

    a = PSet(0, 2, 5, 3, 4, 1, 6)
    b = ToneRow(a, mod=7)

The following are important considerations when instantiating and working with tone rows:

* ToneRows must have each possible pitch class. If instantiating with fewer, an IncompleteException is raised.
* ToneRows are ordered by definition and can not have their ordered field set to False
* ToneRows can not be multisets.

