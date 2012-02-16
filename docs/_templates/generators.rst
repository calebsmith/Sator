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




    def each_n_in_mod(cls, mod):

    each set in mod
    each prime in mod
    def each_card_in_mod(cls, card, mod):
    def each_prime_in_card_mod(cls, card, mod):
