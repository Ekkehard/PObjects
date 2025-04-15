# Python Implementation: EEIterators
# -*- coding: utf-8 -*-
##
# @file       EEIterators.py
#
# @version    2.0.0
#
# @par Purpose
#             EEIterators module of Electrical Engineering Toolbox for
#             (I)Python.
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
#   Tue Dec 17 2024 | Ekkehard Blanz | moved to PObjects
#                   |                |

import math

from PObjects import PObject, ESeries, EEObject, Resistor, Capacitor, Inductor

class ErangeIter():
    """!
    @brief Iterator class for Erange-derived objects.
    """
    def __init__( self, start, end, Eclass, *args, **kwargs ):
        """!
        @brief Constructor for iterator class for the EEObject class.

        Since steps are not all that meaningful in a series, the iterator will
        work in reverse order if the provided end value is smaller than the
        start value.
        @param start beginning value for iteration
        @param end ending value for iteration
        @param Eclass class (not its object) to create objects from
        @param series keyword argument for series to use
        """
        if isinstance( start, PObject ):
            start = start.value
        if isinstance( end, PObject ):
            end = end.value
        self.__end = end
        self.__Eclass = Eclass
        self.__args = args
        self.__kwargs = kwargs
        self.__series = self.__kwargs["series"]
        self.__list = ESeries.list( self.__series )

        self.__distance = math.inf

        self.__factor = 10**math.floor( math.log10( start ) )
        self.__last = len( self.__list ) - 1

        self.__forward = start <= self.__end

        # find index and factor for closest value in given series
        error = math.inf
        for i,val in enumerate( self.__list ):
            newError = abs( start - val * self.__factor )
            if newError < error:
                error = newError
                self.__index = i

        # handle boundary cases
        if 0 == self.__index:
            newError = abs( start - self.__list[-1] * self.__factor / 10 )
            if newError < error:
                self.__index = self.__last
                self.__factor /= 10
        elif self.__last == self.__index:
            newError = abs( start - self.__list[0] * self.__factor * 10 )
            if newError < error:
                self.__index = 0
                self.__factor *= 10

        return


    def __iter__( self ):
        """!
        @brief Iterator is iterable too...
        @return self as iterator
        """
        return self


    def __next__( self ):
        """!
        @brief Return next value from series.

        Iteration can be forward or backward depending on whether start is less
        than or greater than end.  The abortion criterion is "closest to target"
        so that the returned values will be the same (albeit in reverse order)
        regardless which value is given as start and which as end value.
        @return next value
        @throws StopIteration exception when end is reached
        """

        # first compute the potential next value
        value = self.__list[self.__index] * self.__factor

        # determine if we are done
        # which is the case if the distance to the end value increases again
        newDistance = abs( self.__end - value )
        if newDistance > self.__distance:
            raise StopIteration()
        self.__distance = newDistance

        # advance self.__index in appropriate direction
        if self.__forward:
            self.__index += 1
            if self.__index > self.__last:
                self.__index = 0
                self.__factor *= 10
        else:
            self.__index -= 1
            if self.__index < 0:
                self.__index = self.__last
                self.__factor /= 10

        return self.__Eclass( value, *self.__args, **self.__kwargs )



class Erange():
    """!
    As an iterator, the class will provide consecutive EObjects with values from
    a given E-series starting at the closest value to the given start value from
    that series and ending with the closest value to the end value from the same
    series,  progressing over several decades as necessary.  If the end value is
    less than the start value, the iteration will be done in reverse order.
    """

    def __init__( self, start, end, *args, **kwargs ):
        """!
        @brief Constructor for iterable class.
        @param start beginning value for iteration
        @param end ending value for iteration
        @param args unit
                    EEObject-derived class to draw values from (defaults to
                    EEObject)
        @param kwargs series=<series> (default: E12)
        """
        self.__start = start
        self.__end = end
        if len( args ) < 1:
            raise ValueError( "Erange needs at lest a unit as parameters")
        elif len( args ) < 2:
            self.__Eclass = EEObject
        else:
            self.__Eclass = args[0]
            self.__args = args[1:]
        self.__args = args
        try:
            dummy = kwargs["series"]
        except KeyError:
            kwargs["series"] = "E12"
        self.__kwargs = kwargs
        return


    def __iter__( self ):
        """!
        @brief Return iterator for Eseries class.
        @return iterator object
        """
        return ErangeIter( self.__start, self.__end, self.__Eclass,
                           *self.__args, **self.__kwargs )



class Rrange( Erange ):
    """!
    As an iterator, the class will provide consecutive Resistor objects with
    values from a given E-series starting at the closest value to the given
    start value from that series and ending with the closest value to the end
    value from the same series,  progressing over several decades as necessary.
    If the end value is less than the start value, the iteration will be done in
    reverse order.
    """

    def __init__( self, start, end, series=None ):
        """!
        @brief Constructor for iterable class.
        @param start beginning value for iteration
        @param end ending value for iteration
        @param series name of seris (defaults to best of start and end)
        """
        if series is None:
            series = ESeries.bestOf( start.series, end.series )
        super().__init__( start, end, Resistor, "Ω", series=series )
        return



class Crange( Erange ):
    """!
    As an iterator, the class will provide consecutive Capacitor objects with
    values from a given E-series starting at the closest value to the given
    start value from that series and ending with the closest value to the end
    value from the same series,  progressing over several decades as necessary.
    If the end value is less than the start value, the iteration will be done in
    reverse order.
    """

    def __init__( self, start, end, series=None ):
        """!
        @brief Constructor for iterable class.
        @param start beginning value for iteration
        @param end ending value for iteration
        @param series name of series (defaults to best of start and end)
        """
        if series is None:
            series = ESeries.bestOf( start.series, end.series )
        super().__init__( start, end, Capacitor, "F", series=series )
        return



class Lrange( Erange ):
    """!
    As an iterator, the class will provide consecutive Capacitor objects with
    values from a given E-series starting at the closest value to the given
    start value from that series and ending with the closest value to the end
    value from the same series,  progressing over several decades as necessary.
    If the end value is less than the start value, the iteration will be done in
    reverse order.
    """

    def __init__( self, start, end, series ):
        """!
        @brief Constructor for iterable class.
        @param start beginning value for iteration
        @param end ending value for iteration
        @param series name of series (defaults to best of start and end)
        """
        if series is None:
            series = ESeries.bestOf( start.series, end.series )
        super().__init__( start, end, Inductor, "H", series=series )
        return
