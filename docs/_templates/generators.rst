.. _generators:

==========
Generators
==========

All of the generator methods are prefaced by each, sub or super. Below is a brief description of all of the instance generator methods:

* each_n - Yields each possible n for the object's modulus. (0 - 11 for mod 12)
* each_tto - Yields a two tuple in the form of (n, m) for every possible TTO that can be performed on an object.
* each_set - Yields each possible unordered set for the object's modulus
* each_card - Yields each unordered set with the same cardinality as the object, for the object's modulus
* each_prime - Yields each unique set-class for the object's modulus

* subsets - Yields each subset of the given object (depth first)
* subprimes - Yields the unique set-classes of the subsets of the given object
* supersets - Yields each superset of the given object (depth first)
* superprimes - Yields the unique set-classes of the supersets of the given object

The each methods do not take any arguments, while the super and sub methods optionally take one argument. If given, the subsets or supersets will terminate recursion after reaching the cardinality specified.

The following generators are class methods, take the arguments listed, and yield results similar to their instance method counterparts.

* each_n_in_mod(modulus) - Yields each possible n where n is 0 <= n < modulus
* each_set_in_mod(modulus) - Yields each possible unordered set for the given modulus
* each_prime_in_mod(modulus) - Yields each unique set-class for the given modulus
* each_card_in_mod(cardinality, modulus) - Yields each unordered set with the given cardinality in the given modulus.
* each_prime_in_card_mod(cardinality, modulus) - Yields each unique set-class with the given cardinality in the given modulus.
