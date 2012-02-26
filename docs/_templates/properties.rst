.. _properties:

=============================
Properties and Static Methods
=============================

The properties and methods are grouped into categories below.

Static Methods
--------------

fortename(string)
    Returns a new unordered PCSet instance whose Forte name is equivalent to the first argument, which is a string.

For example::
    a = PCSet.forte_name('3-11')
    print a
    Out: [0, 3, 7]

fromint(integer, [modulus=12])
    Returns a new unordered PCSet instance whose integer representation is equal to the first argument.
    Takes an optional keyword argument modulus, that defaults to 12.

For example::
    a = PCSet.fromint(343)
    print a
    Out: [0, 1, 2, 4, 6, 8]
    print a.setint
    Out: 343

The static or class methods that are generators are described under :ref:`generators`

Properties for TTO rotations

Rotations
---------
* t_rotations - A list of objects representing each possible transposition of the given object
* i_rotations - A list of objects representing each possible transpostiion of the given object after inversion
* m_rotations - A list of objects representing each possible transpostiion of the given object after Mm, where m is the default_m of the given object
* mi_rotations - A list of objects representing each possible transpostiion of the given object after MI, where MI is the inverse operator of Mm, and m is the default_m of the given object.
* all_rotations - A list of objects representing each possible transformation of the given object under a TTO


Set methods
-----------

These property methods have a limited meaning for ToneRow objects and are only available to PSet and PCSet objects.

* cardinality - Returns the cardinality of the set.
* setint - Returns the set's integer representation. An unordered PCSet of the set can be derived from this integer and the fromint static method.
* pcint - Returns the integer representation of the set's prime form.
* invariance_vector - Returns a list of (n, m) pairs in which each is a TnMm operation for which the set is invariant.

These methods take one positional argument, which can be any of PSet, PCSet, list, tuple, or set and return a PCSet or boolean as appropriate.
They mimic the Python built-in set methods of the same name. In the description, A is used to denote the current object, and B is the object that is passed in as an argument.

* union(other) - The union of the two objects. The resulting object has all of the elements of both. (A or B)
* intersection(other) - The intersection of the two objects. The resulting object has only the elements that are in both. (A and B)
* difference(other) - The difference of the two objects. The resulting object has the elements of A, excepting those in B.
* symmetric_difference(other) - The symmetric difference of the two objects. The resulting object has all of the elements of A, excepting those in B, as well as all of the elements of B, excepting those in A.
* issuperset(other) - Returns True if the current object is a superset of the argument object, otherwise False
* issubset(other) - Returns True if the current object is a subset of the argument object, otherwise False
* isdisjoint(other) - Returns True if the current object and argument object are disjoin, otherwise False

It is worthwhile to note that the behavior of some of these methods are duplicated elsewhere and that they are included here for ease of use with other set methods.
The following methods have the same behavior as the method they are listed with:

* union - The + operator
* difference - The - operator


Set-Class
---------

These properties are related to the object's set-class and are therefore not available to ToneRow objects, since all tone rows have the same set-class, which is the aggregate of the given modulus.

* prime - The set in prime form. (Use the canon method to change the canonical operators used.)
* prime_operation - Returns a two tuple in the form of (n, m) which would transform the set into its prime form under TnMm using .t_m(n, m)
* forte - Returns the Forte name of the set.
* icv - Returns the interval class vector of the set. N.B. - The first integer represents the number of occurences of IC 0, which some texts omit.
* ds - Returns the degrees of symmetry of the set. (The number of Tn/TnI operations for which the set is invariant)
* mpartner - Returns an unordered PCSet instance, which is the M-partner of the current set, which is a PSet or PCSet.
* zpartner - Returns an unordered PCSet instance, which is the Z-partner of the current set, which is a PSet or PCSet.
* literal_compliment - Returns an unordered PCSet, which represents the literal compliment of the set
* abstract_compliment - Returns an unordered PCSet, which represents the abstract compliment of the set. This is the same as the literal compliment in prime form.

Non-TTO transformations
-----------------------

The following non-TTO transformations are available for PCSet objects only

* c() - Change the given object in place to its literal compliment
* z() - Change the given object in place to its z-partner

Pitch Set Only Properties and Methods
-------------------------------------

The following properties are only available for PSet objects.

* root - Determine the root(s) of an ordered pitch set using Paul Hindemith's method. Returns a list with one root, or multiple roots if the root is indeterminate. If the set is unordered, ascending order is the assumed voicing.

Neo-Riemannian Transformations
------------------------------

Neo-Riemannian transformations and their related methods are only available for PSet objects.
The following methods return new PSet instances, modified by the appropriate Neo-Riemannian Transformation. If the root, third, and fifth can not be found, or there are more than one, the given set is returned unmodified.
These transformations preserve order and change only one pitch by one or two semitones (depending on the transformation)
N.B. - While all major/minor triads are supported for all transformations, other trichords or sets with other cardinalities may give unexpected results. The only requirements are that the set has a modulus of 12, and a determinate root, third and fifth.

* P() - Parallel (C major becomes C minor)
* R() - Relative (C major becomes A minor)
* L() - Leading-Tone or "Leittonwechsel" (C major becomes E minor)

Composite transformations (i.e. transformations created by performing P, L, or R )

* S() - Slide (C major becomes Db minor) - equivalent to L().P().R()
* N() - Nebenverwandt (C major becomes F minor) - equivalent to R().L().P()
* H() - Hexatonic Pole - from Richard Cohn (C major becomes Ab minor) - equivalent to L().P().L() or P().L().P()

All Neo-Riemannian Transformations are involutions and are equivalent to a TnI operation, though order is preserved.
The following methods are not transformations but are available for working with Neo-Riemannian transformations:
When the argument takes a string as input, the string is not case-sensitive and characters other than p, l, r, n, h, and s are ignored

* transform(string) - Returns a set equal to the given set after each transformation in the string is performed successively. 
* neo(string) - A generator that takes string input and yields the resulting set after each transformation. 
* cycle(string) - A generator that performs neo successively until the original set is reached. In this way .cycle("plr") would generate the PLR cycle.
* paths(object) - Takes another PSet as an argument, and returns a list of strings in which each string lists the transformations that can be applied to the original set to reach the input set. Only P, L, and R are used for the search.

The following examples show the Neo-Riemannian transformation methods in action::

    a = PSet(0, 4, 7, ordered=True)
    b = a.H()
    print a.P().L().P() == a.H() == b
    Out: True
    print a.paths(a)
    Out: ['PP', 'RR', 'LL']
    print a.paths(b)
    Out: ['LPL', 'PLP']
    c = a.transform('prl')
    for each in a.neo('prl'):
        print each
    Out: [0, 3, 7]
         [-2, 3, 7]
         [-2, 2, 7]
    print c
    Out: [-2, 2, 7]
    for each in a.cycle('pl'):
        print each
    Out: [0, 3, 7]
         [0, 3, 8]
         [-1, 3, 8]
         [-1, 4, 8]
         [-1, 4, 7]
         [0, 4, 7]

N.B. - The output for .cycle('pl') is a hexatonic system (Richard Cohn). In the example above, this was the "Northern" cycle.
