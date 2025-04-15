# Python Implementation: ESeries
# -*- coding: utf-8 -*-
##
# @file       ESeries.py
#
# @version    2.0.0
#
# @par Purpose
#             ESeries module of Electrical Engineering Toolbox for (I)Python.
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
#   Thu Feb 23 2023 | Ekkehard Blanz | now closest() accepts None series
#   Wed Dec 11 2024 | Ekkehard Blanz | handles series=None (mostly by raising 
#                   |                | exceptions)
#   Tue Dec 17 2024 | Ekkehard Blanz | moved to PObjects
#                   |                |

import math


class ESeries():
    """!
    @brief Class to handle values in E-series, which is mostly used for resistor
    values but also for capacitors.

    The class contains a few static methods for obtaining the list of values for
    a given series, the tolerance for that series, the closest value, the next
    higher, and the next lower value of a given series to a given target value,
    as well as a method to obtain a decade worth of values from a given series
    around a given value.

    All methods require the name of the series as an argument, which can be one
    of "E3", "E6", "E12", "E24", "E48", "E96", "E192", 3, 6, 12, 24, 48, 96, or
    192.  It always defaults to "E12."  Alternatively, a custom series can be
    supplied as the series argument, which then needs to be a list with
    consecutive values spanning one decade starting with 1.0 and ending with a
    value < 10.0.

    Since this class contains only static methods it does not need to be
    instantiated.
    """

    # Private class constants:
    __eList = []
    __eList.append( [1.0, 2.2, 4.7] )
    __eList.append( [1.0, 1.5, 2.2, 3.3, 4.7, 6.8] )
    __eList.append( [1.0, 1.2, 1.5, 1.8, 2.2, 2.7, 3.3, 3.9, 4.7, 5.6, 6.8,
                     8.2] )
    __eList.append( [1.0, 1.1, 1.2, 1.3, 1.5, 1.6, 1.8, 2.0, 2.2, 2.4, 2.7, 3.0,
                     3.3, 3.6, 3.9, 4.3, 4.7, 5.1, 5.6, 6.2, 6.8, 7.5, 8.2,
                     9.1] )
    __eList.append( [1.00, 1.05, 1.10, 1.15, 1.21, 1.27, 1.33, 1.40, 1.47, 1.54,
                     1.62, 1.69, 1.78, 1.87, 1.96, 2.05, 2.15, 2.26, 2.37, 2.49,
                     2.61, 2.74, 2.87, 3.01, 3.16, 3.32, 3.48, 3.65, 3.83, 4.02,
                     4.22, 4.42, 4.64, 4.87, 5.11, 5.36, 5.62, 5.90, 6.19, 6.49,
                     6.81, 7.15, 7.50, 7.87, 8.25, 8.66, 9.09, 9.53] )
    __eList.append( [1.00, 1.02, 1.05, 1.07, 1.10, 1.13, 1.15, 1.18, 1.21, 1.24,
                     1.27, 1.30, 1.33, 1.37, 1.40, 1.43, 1.47, 1.50, 1.54, 1.58,
                     1.62, 1.65, 1.69, 1.74, 1.78, 1.82, 1.87, 1.91, 1.96, 2.00,
                     2.05, 2.10, 2.15, 2.21, 2.26, 2.32, 2.37, 2.43, 2.49, 2.55,
                     2.61, 2.67, 2.74, 2.80, 2.87, 2.94, 3.01, 3.09, 3.16, 3.24,
                     3.32, 3.40, 3.48, 3.57, 3.65, 3.74, 3.83, 3.92, 4.02, 4.12,
                     4.22, 4.32, 4.42, 4.53, 4.64, 4.75, 4.87, 4.99, 5.11, 5.23,
                     5.36, 5.49, 5.62, 5.76, 5.90, 6.04, 6.19, 6.34, 6.49, 6.65,
                     6.81, 6.98, 7.15, 7.32, 7.50, 7.68, 7.87, 8.06, 8.25, 8.45,
                     8.66, 8.87, 9.09, 9.31, 9.53, 9.76] )
    __eList.append( [1.00, 1.01, 1.02, 1.04, 1.05, 1.06, 1.07, 1.09, 1.10, 1.11,
                     1.13, 1.14, 1.15, 1.17, 1.18, 1.20, 1.21, 1.23, 1.24, 1.26,
                     1.27, 1.29, 1.30, 1.32, 1.33, 1.35, 1.37, 1.38, 1.40, 1.42,
                     1.43, 1.45, 1.47, 1.49, 1.50, 1.52, 1.54, 1.56, 1.58, 1.60,
                     1.62, 1.64, 1.65, 1.67, 1.69, 1.72, 1.74, 1.76, 1.78, 1.80,
                     1.82, 1.84, 1.87, 1.89, 1.91, 1.93, 1.96, 1.98, 2.00, 2.03,
                     2.05, 2.08, 2.10, 2.13, 2.15, 2.18, 2.21, 2.23, 2.26, 2.29,
                     2.32, 2.34, 2.37, 2.40, 2.43, 2.46, 2.49, 2.52, 2.55, 2.58,
                     2.61, 2.64, 2.67, 2.71, 2.74, 2.77, 2.80, 2.84, 2.87, 2.91,
                     2.94, 2.98, 3.01, 3.05, 3.09, 3.12, 3.16, 3.20, 3.24, 3.28,
                     3.32, 3.36, 3.40, 3.44, 3.48, 3.52, 3.57, 3.61, 3.65, 3.70,
                     3.74, 3.79, 3.83, 3.88, 3.92, 3.97, 4.02, 4.07, 4.12, 4.17,
                     4.22, 4.27, 4.32, 4.37, 4.42, 4.48, 4.53, 4.59, 4.64, 4.70,
                     4.75, 4.81, 4.87, 4.93, 4.99, 5.05, 5.11, 5.17, 5.23, 5.30,
                     5.36, 5.42, 5.49, 5.56, 5.62, 5.69, 5.76, 5.83, 5.90, 5.97,
                     6.04, 6.12, 6.19, 6.26, 6.34, 6.43, 6.49, 6.57, 6.65, 6.73,
                     6.81, 6.90, 6.98, 7.06, 7.15, 7.23, 7.32, 7.41, 7.50, 7.59,
                     7.68, 7.77, 7.87, 7.96, 8.06, 8.16, 8.25, 8.35, 8.45, 8.56,
                     8.66, 8.76, 8.87, 8.98, 9.09, 9.20, 9.31, 9.42, 9.53, 9.65,
                     9.76, 9.88] )
    __tolerance = [0.5, 0.2, 0.1, 0.05, 0.02, 0.01, 0.005]


    @staticmethod
    def __getIndex( series ):
        """!
        @brief Return index into __eList for given E-series.
        @param series valstr or integer representing the series
        @return index into __eList for that series
        """
        try:
            if int == type( series ):
                index = series
            else:
                index = int( series )
            index = round( math.log( index / 3 ) / math.log( 2 ) )
        except ValueError:
            series = series.upper()
            if "E3" == series:
                index = 0
            elif "E6" == series:
                index = 1
            elif "E12" == series:
                index = 2
            elif "E24" == series:
                index = 3
            elif "E48" == series:
                index = 4
            elif "E96" == series:
                index = 5
            elif "E192" == series:
                index = 6
            else:
                index = -1

        if index < 0 or index > 6:
            raise ValueError( "wrong series name entered: "
                              "{0}".format( series ) )
        return index


    @staticmethod
    def list( series="E12" ):
        """!
        @brief Return index into __eList from series.
        @param series valstr or integer representing the series or custom list
        @return list with values of one decade for that series
        """
        if series is None:
            raise ValueError( "No E-Series specified - "
                              "cannot compute list" )
        if list == type( series ):
            if series[0] != 1.0 or series[-1] >= 10.0:
                raise ValueError( "Custom series must span exactly one decade" )
            return series

        return ESeries.__eList[ESeries.__getIndex( series )]


    @staticmethod
    def len( series="E12" ):
        """!
        @brief Return the length of the list for a given series.
        @param series valstr or integer representing the series or custom list
        @return the number of values in a decade for the given series
        """
        if series is None:
            raise ValueError( "No E-Series specified - "
                              "cannot compute len" )

        if list == type( series ):
            return len( series )

        return len( ESeries.__eList[ESeries.__getIndex( series )] )


    @staticmethod
    def bestOf( series1, series2 ):
        """!
        @brief Find the best (more accurate) of two series.
        @param series1 valstr or list with first series to check
        @param series2 valstr or list with second series to check
        @return valstr or list of the better of the two supplied series
        """
        if len( series1 ) >= len( series2 ): return series1
        else: return series2


    @staticmethod
    def tolerance( series="E12" ):
        """!
        @brief Return tolerance for values in given series.

        If the series is given as a list of values within a decade, the
        tolerance is computed from the values within that list, otherwise, the
        standardized value for the series is returned.
        @param series name of seris (defaults to "E12")
        @return floating point 0 < tolerance() < 1 (not percent) with tolerance
        """
        if series is None:
            raise ValueError( "No E-Series specified - "
                              "cannot compute tolerance" )

        if list == type( series ):
            sum = 0.
            for i in range( len( series ) - 1 ):
                sum += (series[i+1] - series[i]) / (series[i+1] + series[i])
            return sum / len( series )
        return ESeries.__tolerance[ESeries.__getIndex( series )]


    @staticmethod
    def closest( value, series="E12" ):
        """!
        @brief Return the closest value in a given series to the given value.
        @param value value to approximate
        @param series name of series (defaults to "E12")
        @return float with closest value in series to given value
        """
        
        if series is None:
            return value
            
        elist = ESeries.list( series )
        factor = 10**math.floor( math.log10( value ) )

        error = math.inf
        index = 0
        for i,val in enumerate( elist ):
            newError = abs( value - val * factor )
            if newError < error:
                error = newError
                index = i

        # handle boundary cases
        if 0 == index:
            newError = abs( value - elist[-1] * factor / 10 )
            if newError < error:
                index = len( elist ) - 1
                factor /= 10
        elif len( elist ) - 1 == index:
            newError = abs( value - elist[0] * factor * 10 )
            if newError < error:
                index = 0
                factor *= 10

        return elist[index] * factor


    @staticmethod
    def next( value, series="E12" ):
        """!
        @brief Return the next higher value in a given series to a given value.
        @param value value to approximate
        @param series name or list of series (defaults to "E12")
        @return float with next higher value in series to given value
        """
        if series is None:
            raise ValueError( "No E-Series specified - cannot compute next" )

        elist = ESeries.list( series )
        factor = 10**math.floor( math.log10( value ) )

        for index,val in enumerate( elist ):
            if val * factor > value: break

        # handle boundary case
        if index >= (len( elist ) - 1) and val * factor <= value:
            index = 0
            factor *= 10

        return elist[index] * factor


    @staticmethod
    def previous( value, series="E12" ):
        """!
        @brief Return the next lower value in a given series to the given value.
        @param value value to approximate
        @param series name or list of series (defaults to "E12")
        @return float with next smaller value in series to given value
        """
        if series is None:
            raise ValueError( "No E-Series specified - "
                              "cannot compute previous" )

        elist = ESeries.list( series )
        factor = 10**math.floor( math.log10( value ) )

        error = math.inf
        for i,val in enumerate( elist[::-1] ):
            if val * factor < value: break
        index = len( elist ) - 1 - i

        # handle boundary case
        if index <= 0 and val * factor >= value:
            index = len( elist ) - 1
            factor /= 10

        return elist[index] * factor


    @staticmethod
    def decade( value, series="E12", decades=1, sorted=False, reverse=False ):
        """!
        @brief Return a list with a decade of values around a given value.

        The returned list is not ordered by default but rather contains values
        increasingly further away from the starting value, always starting with
        the lower value.  To get an ordered list, set sorted to True.
        @param value central value for list
        @param series name of series (defaults to "E12")
        @param decades number of decades to return (can be < 1), defaults to 1
        @param sorted set True to obtain the list sorted
        param reverse set True to sort in reverse order (only if sorted is True)
        @return list with a decade worth of float values
        """
        if series is None:
            raise ValueError( "No E-Series specified - "
                              "cannot compute decade" )

        vlist = []
        if value == ESeries.closest( value, series ):
            vlist.append( value )

        steps = round( ESeries.len( series ) * decades )
        lval = value
        hval = value
        while len( vlist ) < steps:
            lval = ESeries.previous( lval, series )
            vlist.append( lval )
            if len( vlist ) == steps: break
            hval = ESeries.next( hval, series )
            vlist.append( hval )

        if sorted: vlist.sort( reverse=reverse )

        return vlist
