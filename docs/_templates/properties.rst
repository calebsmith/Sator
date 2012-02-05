.. _properties:

==========
Properties
==========

Each property takes no arguments and does not require the () syntax for calling.
The properties are grouped into categories below.

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

Rotations
---------
* t_rotations - A list of objects representing each possible transposition of the given object
* i_rotations - A list of objects representing each possible transpostiion of the given object after inversion
* m_rotations - A list of objects representing each possible transpostiion of the given object after Mm, where m is the default_m of the given object
* mi_rotations - A list of objects representing each possible transpostiion of the given object after MI, where MI is the inverse operator of Mm, and m is the default_m of the given object.
* all_rotations - A list of objects representing each possible transformation of the given object under a TTO


Set methods
-----------

These methods have a limited meaning for ToneRow objects and are only available to PSet and PCSet objects.

* cardinality - Returns the cardinality of the set.
* setint - Returns the set's integer representation. An unordered PCSet of the set can be derived from this integer and the fromint static method.
* pcint - Returns the integer representation of the set's prime form.


Set-Class
---------

These methods are related to the object's set-class and are therefore not available to ToneRow objects.

* prime - The set in prime form. (Use the canon method to change the canonical operators used.)
* prime_operation - Returns a two tuple in the form of (n, m) which would transform the set into its prime form under TnMm using .t_m(n, m)
* forte - Returns the Forte name of the set.
* icv - Returns the interval class vector of the set. N.B. - The first integer represents the number of occurences of IC 0, which some texts omit.
* mpartner - Returns an unordered PCSet instance, which is the M-partner of the current set, which is a PSet or PCSet.
* zpartner - Returns an unordered PCSet instance, which is the Z-partner of the current set, which is a PSet or PCSet.
* literal_compliment - Returns an unordered PCSet, which represents the literal compliment of the set
* abstract_compliment - Returns an unordered PCSet, which represents the abstract compliment of the set. This is the same as the literal compliment in prime form.


Non-TTO transformations
-----------------------

The following non-TTO transformations are available for PCSet objects only

* c - Change the given object in place to its literal compliment
* z - Change the given object in place to its z-partner
