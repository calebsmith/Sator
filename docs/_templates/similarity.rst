.. _similarity_relations:

====================
Similarity Relations
====================

Similarity relations take two sator core objects as input and are imported from the sator.sim module.
The following is a list of general similarity functions and their descriptions:

* m(a, b) - Returns True if the sets are M-partners, otherwise False
* c(a, b) - Returns True if the sets are abstract compliments, otherwise False
* z(a, b) - Returns True if the sets are Z-partners, otherwise False
* zc(a, b) - Returns True if the sets are abstract compliments and Z-partners, otherwise False

Each of these return a boolean.

The following is a list of similarity functions invented by Robert Morris:

* iv(a, b) - Returns a list of totals of each ordered pitch interval that can be expressed from a pc in a to a pc in b. -Morris' IV(a, b)
* sim(a, b) - Returns the sum of absolute value differences between the icv's of a and b (excluding icv0) -Morris' SIM(a, b)
* asim(a, b) - Returns the sim(a, b) divided by the total of possible differences in the icv's of a and b. Takes a boolean kwarg rational, which changes the return to a two tuple representing a rational number -Morris' ASIM(a, b)
