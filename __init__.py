# Python Implementation: PObjects
# -*- coding: utf-8 -*-
##
# @file       __init__.py
#
# @mainpage   PObjects - set of Python classes encapsulating physical objects
#
# Physical objects, other than many other objects in mathematics or computer
# science, are characterized by not only their numerical value but also their
# physical unit.  Combined pairs of values and units, when viewed as a
# multiplication of one with the other, obey much of the same rules when used in
# numerical computations as regular values do.  In particular, only physical
# objects with like units can be added or subtracted yielding a new physical
# object with the same unit; physical objects of arbitrary units can be
# multiplied or divided yielding physical objects with different units for the
# result.
#
# This package understands the SI base units m, kg, s, A, K, and cd but also all 
# of the common derived units, such as Hz, N, and so on.  On top of that, all
# standard SI prefixes, such as k, m, M, and so on are also supported.
#
# PObjects are instantiated with a constructor that takes a numerical value and
# a unit including standard prefix as an argument or with strings containing
# both.  When they are printed, "sensible" unit prefixes are chosen (as in
# standard engineering notation).
#
# Apart from the class PObject for the standard physical objects and several
# convenience classes for the most common physical objects, this package
# contains a few classes to facilitate the use of its benefits for electronic
# components, honoring the commonly used "E-series" in electrical engineering.
# 
# For more details please see the documentation of \link PObject.PObject PObject
# \endlink and that of \link EEObjects.EEObject EEObjects \endlink.
#
# @version    2.0.0
#
# @par Comments
# This is Python 3 code!  However, PEP 8 guidelines are decidedly NOT followed
# in some instances, and guidelines provided by "Coding Style Guidelines" a
# "Process Guidelines" document from WEB Design are used instead where the two
# differ, as the latter span several programming languages and are therefore
# also applicable to projects that require more than one programming language;
# it also provides consistency across hundreds of thousands of lines of legacy
# code.  Doing so, ironically, is following PEP 8, which speaks highly of the
# wisdom of the authors of PEP 8.
#
# @par Known Bugs
# None
#
# @author
# W. Ekkehard Blanz <Ekkehard.Blanz@gmail.com>
#
# @copyright
# Copyright (C) 2022 - 2025 W. Ekkehard Blanz\n

#
# File history:
#
#      Date         | Author         | Modification
#   ----------------+----------------+------------------------------------------
#   Wed Apr 13 2022 | Ekkehard Blanz | created
#   Wed Dec 11 2024 | Ekkehard Blanz | added Time, Mass, and Length
#                   |                | and moved Frequency to Physics package
#   Tue Dec 17 2024 | Ekkehard Blanz | brought PObjects-related packages from
#                   |                | ElectricalEngineering into this package
#   Tue Jan 28 2025 | Ekkehard Blanz | added __version__ and __all__
#                   |                |

from .SI import Unit, Prefix
from .PObject import sqrt, PObject, Energy, Temperature, Time, Mass, Length, \
                     Frequency, ImperialLengthMisfits
from .ESeries import ESeries
from .EEObjects import EEObject, Voltage, Current, \
                       Resistor, Capacitor, Inductor
from .EEIterators import Erange, Rrange, Crange, Lrange
from .Const import Const



__version__ = '2.0.0'
#__all__ = ['Const', 'Unit', 'Prefix', 'sqrt', 'PObject', 'Energy',
#           'Temperature', 'Time', 'Mass', 'Length', 'Frequency',
#           'ImperialLengthMisfits', 'ESeries', 'EEObject', 'Voltage', 'Current',
#           'Resistor', 'Capacitor', 'Inductor', 'Erange', 'Rrange', 'Crange',
#           'Lrange']
