.. _attributes:

==========
Attributes
==========

PCSet and PSet instances have attributes which can be set via the methods listed below.
ToneRow instances have some but not all of these methods and exceptions are noted after the method's description.

Mod
---

mod([modulus])

Sets the modulus of the object to modulus. Without a modulus, the current modulus is returned

Default_m
---------

default_m([m])

Sets the default m that is used for Mm (and MI) for TTO's and for determining the prime form if Mm is canonical (Refer to canon below for more).
Without an argument, the current default_m is returned

Multiset
--------

multiset([boolean])

If boolean is True, the object is now a multiset and will accept new pitches or pitch classes that are duplicates of existing set members.
If boolean is False, the object is not a multiset and will not accept new pitches or pitch classes that are duplicates of existing members.
Without an argument, the current multiset status is returned.

* ToneRow instances have multiset set to False and it can not be multisets.

Ordered
-------

ordered([boolean])

If boolean is True, the object will be considered an ordered set, and its __repr__ will show the pitches or pitch classes in the order they were added. Equivalence tests will consider the order of the set.
If boolean is False, the object will be considered an unordered set, and its __repr__ will show the pitches or pitch classes in ascending numerical order regardless of the order in which they were added. Equivalence tests will not consider the order of the set, only its members. Unordered sets maintain order internally, so they do not loose the order of pitches/pitch classes when ordered is set to True.

* ToneRow instances have ordered set to True and can not be unordered.

Canon
-----

canon(t, i, m) where t, i, and m are booleans.

Set the status of Tn, TnI, and TnM as canonical operators. These operators are used for determining set-class membership.
The default is to use Tn/TnI, which would result from calling .canon(True, True, False).
As an example, to use only Tn, as some theorists propose, use canon(True, False, False). To use Tn/TnI/TnM use .canon(True, True, True)

* Set-class membership is irrelevant for tone rows since they are all members of the aggregate. ToneRow instances do not have a canon method.

get_canon()

Returns a three tuple with the current status of canonical operators.
If the canonical operators are Tn/TnM, the return would be (True, False, True)

* ToneRow instances do not have this method.
