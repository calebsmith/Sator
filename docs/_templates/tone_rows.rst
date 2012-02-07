.. _tone_rows:

=========
Tone Rows
=========

Tone rows can be thought of as a very restrictive type of ordered pitch class collection in which all possible elements are present.
As a result, there are many methods for sets that are meaningless, and therefore withheld from the ToneRow class, such as .ordered() and the methods for adding/removing pitch classes.


Inherited Methods and Methods with Different Meanings
-----------------------------------------------------

The following are some methods which ToneRow objects inherit from a parent class common to sets (SetRowBase), but are in no way meaningful to tone rows:
* pitches, pcs, uo_pitches, uo_pcs - Tone rows are always ordered pitch class collections, so these methods are irrelavent to the API and only exist for consistency internally.
* multiset, ordered - These are overridden in ToneRow to do nothing

The following are some methods that have a different meaning or use with ToneRow objects:
* Wheras the x_rotations (where x is t, i, m, or mi) methods are thought of as rotations when used with sets, here they constitue the T, I, M, and MI matrices
* default_m - The prime form is not meaningful in tone rows (they are always the aggregate) but the default_m is used to determine the m used by the M and MI matrices, as well as any TTO operations containing M/MI on the row.


ToneRow Methods
---------------

The following are methods that are unique to ToneRow objects:

    * swap(a, b) - Given indices a and b, swap the PC's in the tone row that are in these positions.
    * P - Prime form of the row
    * I - Inversion of the row
    * R - Retrograde of the row
    * RI - Retrograde inversion of the row
    * M - Mm of the row (m is supplied by default_m)
    * MI - MmI of the row
    * RM - Retrograde of the Mm of the row
    * RMI - Retrograde of the MmI of the row
