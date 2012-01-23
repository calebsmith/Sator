Core module
===========

The core module in sator contains the three essential classes for instantiating
and manipulating tone rows, pitch, and pitch class sets.

To construct rows and sets, import the ToneRow, PCSet, and PSet classes from
this module.

>>> from sator.core import ToneRow, PCSet, PSet

To return new set or row instances modified by a TTO, import and use the following:

>>> from sator.core import transpose, invert, multiply, transpose_multiply

.. automodule:: core
    :members:

.. autofunction:: transpose
.. autofunction:: invert
.. autofunction:: multiply
.. autofunction:: transpose_multiply
