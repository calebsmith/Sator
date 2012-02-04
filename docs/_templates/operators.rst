.. _operators:

=========
Operators
=========

Iteration and Length
--------------------

ToneRow, PCSet, and PSet objects can be iterated over, which returns each pitch or pitch class represented by the object's .ppc property.
The set's ordered property is respected by the iterator, which returns each element in the order given for ordered sets, and in ascending order for unordered sets. For example::

    a = PCSet([0, 3, 5, 6, 9], ordered=False)
    for pc in a:
        print pc

Returns 0, 3, ... 9
However::

    a = PCSet([9, 5, 3, 2], ordered=True)
    for pc in a:
        print pc

Returns 9, 5, ... 2

Similarly the len() property returns the length of the object's .ppc property. The length of the set is not the same as the set's cardinality.
Refer to :func:`cardinality` to see the distinction between :func:`len` and :func:`cardinality`.
This is best illustrated by the following example, as a contains 3 pitches, and only 1 pitch class::

    a = PSet(11, -1, 23)
    print a.cardinality
    Out: 1
    print len(a)
    Out: 3

Evaluation
----------

ToneRow, PCSet and PSet objects can be compared to each other for equality and inequality using the == and != operators.
Use the following list to see the criteria for equality amongst these objects:

* If one object is ordered, the pitches or pitch classes must be in the same order.
* One object can be a list, tuple, or set rather than a ToneRow, PCSet, or PSet object.
* A ToneRow is equal to another object if they contain the same pitch classes in the same order.
* Two PSets are equal if they contain the same pitches.
* Two PCSets are equal if they contain the same pitch classes.
* A PSet and PCSet are equal if they contain the same pitch classes.

Addition and Subtraction
------------------------

Pitches or pitch classes can be added or removed from an existing set with the += or = + idioms.
The addition and subtraction operators each return a new object, so it can also be used to instantiate a new object.
Integers, lists, tuples, sets and instances of sator core objects can all be added or subtracted.
For examle::
    a += [3, 9]
    b = b + [0]
    c = a + b

Addition and subtraction can also be used for evaluation such as::

    a = PSet(0, 1, 11)
    a + [3, 9] == [0, 1, 3, 9, 11]
    Out: True
    a - 1 == [0, 11]
    Out: True

* When subtracting from a multiset, each instance of the pitch or pitch class will be removed.
When adding or subtracting a pitch or pitch class is not possible, because it is already present or not in the instance, no errors are raised.
For example::
    a = PSet(0, 1, 11)
    print a - 3
    Out: [0, 1, 11]


Insert
------

Similarly, pitch and pitch sets, but not tone rows, have an insert method. This method is meaningful only for sets which have their ordered field set to True but still adds the pitch or pitch class nonetheless.
Insert takes an index and a new pitch/pitch class as it's arguments.
This method can be used as follows::

    a = PCSet([0, 4, 8], ordered=True)
    a.insert(1, 2)
    print a
    Out: [0, 2, 4, 8]

Copy
----

Objects are mutable in Python, which may lead to unexpected behavior. For example::

    a = PSet(0, 3, 6, ordered=True)
    b = a
    b += 8
    print a
    Out: [0, 3, 6, 8]

To instantiate a new ToneRow, PCSet or PSet from another use the copy method as shown below::

    a = PSet(0, 3, 6, ordered=True)
    b = a.copy()
    b += 8
    print a
    Out: [0, 3, 6]
    print b
    Out: [0, 3, 6, 8]
    print b.ordered
    out: True
