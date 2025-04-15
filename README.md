PObjects - set of Python classes encapsulating physical objects
---------------------------------------------------------------

Physical objects, other than many other objects in mathematics or computer
science, are characterized by not only their numerical value but also their
physical unit.  Combined pairs of values and units, when viewed as a
multiplication of one with the other, obey much of the same rules when used in
numerical computations as regular values do.  In particular, only physical
objects with like units can be added or subtracted yielding a new physical
object with the same unit; physical objects of arbitrary units can be
multiplied or divided yielding physical objects with different units for the
result.

This package understands the SI base units m, kg, s, A, K, and cd but also all
of the common derived units, such as Hz, N, and so on.  On top of that, all
standard SI prefixes, such as k, m, M, and so on are also supported.

PObjects are instantiated with a constructor that takes a numerical value and
a unit string including standard prefix as an argument or with strings
containing both.  When they are printed, "sensible" unit prefixes are chosen (as
in standard engineering notation).

Apart from the class PObject for the standard physical objects and several
convenience classes for the most common physical objects, this package contains
a few classes to facilitate the use of its benefits for electronic components,
honoring the commonly used "E-series" in electrical engineering.
                                                                   
For more details please see the documentation of PObject and that of EEObjects.
