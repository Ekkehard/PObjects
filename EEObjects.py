# Python Implementation: EEObjects
# -*- coding: utf-8 -*-
##
# @file       EEObjects.py
#
# @version    2.0.0
#
# @par Purpose
#             EEObjects module of PObjects Toolbox for (I)Python.
#
# @par Comments
#             This code is modeled after the Matlab/Octave Electrical
#             Engineering Toolbox from the same author.
# @par
#             This is Python 3 code!

# Known Bugs: none
#
# @author     Ekkehard Blanz <Ekkehard.Blanz@gmail.com> (C) 2022-2024
#
# @copyright  See COPYING file that comes with this distribution
#
# File history:
#
#      Date         | Author         | Modification
#  -----------------+----------------+------------------------------------------
#   Thu Apr 14 2022 | Ekkehard Blanz | extracted from ElectricalEngineering.py
#   Wed Dec 11 2022 | Ekkehard Blanz | eliminated need for series in Inductor
#                   |                | and moved Frequency to PObjects package
#   Tue Dec 17 2024 | Ekkehard Blanz | moved to PObjects
#                   |                |

import sys
import os.path

from PObjects import PObject, SI, ESeries


class EEObject( PObject ):
    """!
    @brief PObject-derived class that allows objects to only take on values out
    of a given E-series or an arbitrary (non-E) series provided in a list.

    This class is particularly useful for Resistors and Capacitors.  But since
    the series argument also takes lists of values in a decade that do not
    correspond to an E-series, it can also be used for inductors.  Since only
    distinct values are allowed, the class also provides a next() and previous()
    method.  For more general computations, only PObjects should be used, as 
    their values are not restricted and allow full precision computations.
    """

    def __init__( self, value, *args, **kwargs ):
        """!
        @brief Constructor.  Can be called as
        @code
            EEObject( <valueString>[, series=<series>] )
        @endcode
        or
        @code
            EEObject( <value>, <unit>[, series=<series>] )
        @endcode
        or
        @code
            EEObject( <objet>[, series=<series>] )
        @endcode
        where valueString can be any valstr consisting of a value and an SI
        unit, and the object can be any PObject-derived object.  <value> and
        <unit> are self explanatory, and <series> can be a valstr specifying an
        E-series or a list with values covering one decade.  In addition, this
        constructor will also accept the keyword arguments digits for the
        number of significant digits to be printed (defaults to 3), and
        strictAscii as a boolean value (defaults to False) to allow restriction
        of output to strict ASCII characters only.
        @param value valstr with value and unit or float with value or PObject
                     with unit "Ω"
        @param args unit if value was int, float, or complex
        @param kwargs series=<series> (default: "E12"),
                      digits=<digits> (default: 3),
                      strictAscii=<bool> (default: False)
        """
        try:
            self.__series = kwargs["series"]
        except KeyError:
            self.__series = "E12"
        try:
            _ = kwargs["digits"]
        except KeyError:
            kwargs["digits"] = 3
            
        if isinstance( value, str ):
            if len( args ) != 0:
                raise ValueError( "Too many arguments" )
            value, unit = SI.Prefix.fromString( value )
            args = unit,
        elif isinstance( value, PObject ):
            unit = value.unit
            value = value.value
            args = unit,
        elif isinstance( value, (int, float, complex) ):
            if len( args ) < 1:
                raise ValueError( "Unit argument missing" )
        super().__init__( ESeries.closest( value, self.__series ),
                          *args,
                          **kwargs )
        return


    def next( self ):
        """!
        @brief Obtain an object with the next higher value to the one of this
        object.
        @return object with next higher value from same series
        """
        return self.__class__( ESeries.next( self.value, self.series ),
                               *self._args,
                               **self._kwargs )


    def previous( self ):
        """!
        @brief Obtain an object with the next lower value to the one of this
        object.
        @return object with next lower value from same series
        """
        return self.__class__( ESeries.previous( self.value, self.series ),
                               *self._args, **self._kwargs )


    def decade( self, decades=1, sorted=False, reverse=False ):
        """!
        @brief Obtain a list with objects spanning one decade around the value
        of this object.
        @param sorted set True to obtain the list sorted
        param reverse set True to sort in reverse order (only if sorted is True)
        @return list of objects with values spanning one decade around this one
        """
        vlist = ESeries.decade( self.value, self.series, decades=decades,
                                sorted=sorted, reverse=reverse )
        olist = []
        for value in vlist:
            olist.append( self.__class__( value, *self._args, **self._kwargs ) )
        return olist


    # inherits value and unit property from PObject
    # inherits _args and _kwargs properties from PObject


    @property
    def series( self ):
        """!
        @brief Obtain the series values of this object are confined to.
        """
        return self.__series


class Voltage( PObject ):
    """!
    @brief Convenience class to create a PObject-derived object with unit V.
    """

    def __init__( self, value, *args, **kwargs ):
        """!
        @brief Constructor.
        @param value valstr with value and unit or float with value or PObject
                     with unit "V"
        @param args unit "V" if value was float
        @param kwargs digits=<digits> (default: 3),
                      strictAscii=<bool> (default: False)
        """
        try:
            _ = kwargs["digits"]
        except KeyError:
            kwargs["digits"] = 3

        if isinstance( value, PObject ):
            super().__init__( value, *args, **kwargs )
        else:
            if str == type( value ):
                value, unit = SI.Prefix.fromString( value )
            elif len( args ) > 0:
                unit = args[0]
                args = args[1:]
            else:
                unit = "V"
            super().__init__( value, unit, *args, **kwargs )
        if self.unit != "V":
            raise ValueError( "Voltage can only be initialized with a "
                              "string, a value in V, a value and a unit, "
                              "or an object inheriting from PObject with "
                              "unit V" )
        return


class Current( PObject ):
    """!
    @brief Convenience class to create a PObject-derived object with unit A.
    """

    def __init__( self, value, *args, **kwargs ):
        """!
        @brief Constructor.
        @param value valstr with value and unit or float with value or PObject
                     with unit "A"
        @param args unit "A" if value was float
        @param kwargs digits=<digits> (default: 3),
                      strictAscii=<bool> (default: False)
        """
        try:
            _ = kwargs["digits"]
        except KeyError:
            kwargs["digits"] = 3

        if isinstance( value, PObject ):
            super().__init__( value, *args, **kwargs )
        else:
            if str == type( value ):
                value, unit = SI.Prefix.fromString( value )
            elif len( args ) > 0:
                unit = args[0]
                args = args[1:]
            else:
                unit = "A"
            super().__init__( value, unit, *args, **kwargs )
        if self.unit != "A":
            raise ValueError( "Current can only be initialized with a "
                              "string, a value in A, a value and a unit, "
                              "or an object inheriting from PObject with "
                              "unit A" )
        return

class Resistor( EEObject ):
    """!
    @brief Convenience class for an EEObject initialized as resistor using E12
    series by default.
    """

    def __init__( self, value, *args, **kwargs ):
        """!
        @brief Constructor.
        @param value valstr with value and unit or float with value or PObject
                     with unit "Ω"
        @param args unit "Ω" if value was float
        @param kwargs series=<series> (default: "E12"),
                      digits=<digits> (default: 3),
                      strictAscii=<bool> (default: False)
        """
        try:
            _ = kwargs["digits"]
        except KeyError:
            kwargs["digits"] = 3
        try:
            series = kwargs["series"]
        except KeyError:
            series = None

        if isinstance( value, PObject ):
            if isinstance( value, EEObject ):
                if series is None:
                    series = value.series
            else:
                if series is None:
                    series = "E12"
            kwargs["series"] = series
            super().__init__( value, *args, **kwargs )
        else:
            if series is None:
                kwargs["series"] = "E12"
            if str == type( value ):
                value, unit = SI.Prefix.fromString( value )
            elif len( args ) > 0:
                unit = args[0]
                args = args[1:]
            elif 0 == len( args ):
                unit = "Ω"
            super().__init__( value, unit, *args, **kwargs )
        if self.unit != "Ω":
            raise ValueError( "Unit for Resistor must be Ohm" )
        return


class Capacitor( EEObject ):
    """!
    @brief Convenience class for an EEObject initialized as capacitor using E6
    series.  @see also the companion class Crange.
    """

    def __init__( self, value, *args, **kwargs ):
        """!
        @brief Constructor.
        @param value valstr with value and unit or float with value or PObject
                     with unit "F"
        @param args unit "F" if value was float
        @param kwargs series=<series> (default: "E6"),
                    digits=<digits> (default: 3),
                    strictAscii=<bool> (default: False)
        """
        try:
            _ = kwargs["digits"]
        except KeyError:
            kwargs["digits"] = 3
        try:
            series = kwargs["series"]
        except KeyError:
            series = None

        if isinstance( value, PObject ):
            if isinstance( value, EEObject ):
                if series is None:
                    series = value.series
            else:
                if series is None:
                    series = "E6"
            kwargs["series"] = series
            super().__init__( value, *args, **kwargs )
        else:
            if series is None:
                kwargs["series"] = "E6"
            if str == type( value ):
                value, unit = SI.Prefix.fromString( value )
            elif len( args ) > 0:
                unit = args[0]
                args = args[1:]
            elif 0 == len( args ):
                unit = "F"
            super().__init__( value, unit, *args, **kwargs )
        if self.unit != "F":
            raise ValueError( "Unit for Capacitor must be Farad" )
        return


class Inductor( EEObject ):
    """!
    @brief Convenience class for EEObject initialized as inductor.  Since it is
    derived from EEObject and not PObject, objects are usually confined to a 
    series that was supplied when initializing it - there is no default series 
    for inductors.  To create an inductor object with values not bound to a
    particular series, use a PObject with unit "H".
    """

    def __init__( self, value, *args, **kwargs ):
        """!
        @brief Constructor.
        @param value valstr with value and unit or float with value or PObject
                     with unit "H"
        @param args unit "H" if value was float
        @param kwargs series=<series> (default: None),
                      digits=<digits> (default: 3),
                      strictAscii=<bool> (default: False)
        """
        try:
            _ = kwargs["series"]
        except KeyError:
            kwargs["series"] = None

        if isinstance( value, PObject ):
            super().__init__( value, *args, **kwargs )
        else:
            if str == type( value ):
                value, unit = SI.Prefix.fromString( value )
            elif len( args ) > 0:
                unit = args[0]
                args = args[1:]
            elif 0 == len( args ):
                unit = "H"
            super().__init__( value, unit, *args, **kwargs )
        if self.unit != "H":
            raise ValueError( "Unit for Inductor must be Henry" )
        return
