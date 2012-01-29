.. _constructor_options:

===================
Constructor Options
===================

The PCSet and PSet classes take the following keyword arguments:

==================   ============  ==================================  ==============  ===============================
Key                  Type          Description                         Example         Default
==================   ============  ==================================  ==============  ===============================
mod                  int           Set the object's modulus            mod=7           12
ordered              boolean       Is the set ordered or unordered?    ordered=True    False for PCSet, True for PSet
multiset             boolean       Is the set a multiset?              multiset=True   False
==================   ============  ==================================  ==============  ===============================

* Tone rows are ordered by definition, and can not be multisets, these kwargs have no affect when constructing ToneRow objects.
* Constructing a tone row with fewer pitch classes than its modulus is by definition a pitch class set, and not a tone row. As a result, you must use the mod= kwarg when constructing a tone row with a modulus less than 12.
