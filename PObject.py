# Python Implementation: PObject
##
# @file       PObject.py
#
# @version    2.0.1
#
# @par Purpose
#             PObject class and derived classes for PObjects toolbox package.
#
# @par Comments
#
# @par
#             This is Python 3 code!

# Known Bugs: none
#
# @author     W. Ekkehard Blanz <Ekkehard.Blanz@gmail.com> (C) 2018-2026
#
# Copyright
#            Copyright (C) 2018-2022 W. Ekkehard Blanz
#            See NOTICE.md and LICENSE.md files that come with this distribution
#
# File history:
#
#      Date         | Author         | Modification
#   ----------------+----------------+------------------------------------------
#   Mon Feb 12 2018 | Ekkehard Blanz | created
#   Thu Feb 15 2018 | Ekkehard Blanz | now PObject accepts PObject as parameter
#                   |                | and operators return value-type if result
#                   |                | is unitless
#   Sat Feb 17 2018 | Ekkehard Blanz | added valueList() and floatList() and put
#                   |                | constants in Const and its metaclass
#   Tue Aug 28 2018 | Ekkehard Blanz | PObject constructor can now have prefixed
#                   |                | unit argument
#   Wed Aug 29 2018 | Ekkehard Blanz | added standardizedList()
#   Wed Nov 21 2018 | Ekkehard Blanz | improved unit test and documentation
#   Fri Dec 07 2018 | Ekkehard Blanz | can now add and subtract regular numbers
#                   |                | from unitless PObjects
#   Tue Jan 15 2019 | Ekkehard Blanz | added Temperature as PObject subclass
#   Fri Jan 18 2019 | Ekkehard Blanz | added standard printing of different
#                   |                | units to Energy and Temperature
#   Mon Jan 21 2019 | Ekkehard Blanz | harmonized Energy and Temperature and
#                   |                | removed their conversion properties in
#                   |                | favor of a more robust printUnit
#   Tue Feb 12 2019 | Ekkehard Blanz | added ImperialLengthMisfits
#   Wed Feb 13 2019 | Ekkehard Blanz | vastly improved PObject documentation
#   Thu Feb 14 2019 | Ekkehard Blanz | added useYards parameter
#   Mon Feb 18 2019 | Ekkehard Blanz | added in-place arithmetic operators and
#                   |                | fixed various bugs dealing with
#                   |                | interaction with non PObjects
#   Mon Mar 10 2019 | Ekkehard Blanz | fixed problem in multiplying and dividing
#                   |                | derived classes
#   Tue Mar 12 2019 | Ekkehard Blanz | fixed bug in standardizedList() and
#                   |                | allowed comparisons with 0 directly
#   Fri Jan 07 2022 | Ekkehard Blanz | added standardizedTuple property to
#                   |                | PObject and provided setter for digits
#   Mon Jan 10 2022 | Ekkehard Blanz | arithmetic operations no longer return
#                   |                | unitless PObjects but plain numbers
#                   |                | instead
#   Mon Jan 10 2022 | Ekkehard Blanz | cleaned up code and added documentation
#                   |                | for unitless and zero-valued PObjects
#   Wed Feb 02 2022 | Ekkehard Blanz | added __bool__() method to PObject
#   Fri Feb 18 2022 | Ekkehard Blanz | added copy() method to PObject
#   Wed Apr 13 2022 | Ekkehard Blanz | separated Const from this file and made
#                   |                | part of Physics package
#   Mon Jul 18 2022 | Ekkehard Blanz | added __format__ method to PObject
#   Sat Dec 07 2024 | Ekkehard Blanz | fixed bug in __rtruediv__
#   Wed Dec 11 2024 | Ekkehard Blanz | added Time, Mass, and Length
#                   |                | and moved Frequency From EE package
#   Thu Dec 12 2024 | Ekkehard Blanz | made float() work on PObjects
#   Tue Dec 17 2024 | Ekkehard Blanz | renamed package to PObjects
#   Tue Oct 13 2026 | Ekkehard Blanz | now also imports scipy.constants
#   Wed Oct 14 2026 | Ekkehard Blanz | fixed shared kwargs between objects,
#                   |                | valueList(), standardizedList(),
#                   |                | digits setter, __format__(),
#                   |                | __repr__(), arithmetic with Energy and
#                   |                | ImperialLengthMisfits, construction of
#                   |                | subclasses from PObjects, negative
#                   |                | Time, and imperial length rounding;
#                   |                | results of arithmetic operations now
#                   |                | have the smaller number of digits of
#                   |                | the operands; accepts prefixes in all
#                   |                | tokens of composite units and eV, E_h,
#                   |                | and u as input units; added hook
#                   |                | _resultClass() for class of results of
#                   |                | arithmetic operations
#                   |                |

import math
import copy
import numbers
import scipy
import scipy.constants

from PObjects import SI


def sqrt( value ):
    """!
    @brief Provide a sqrt function that, other than the one provided by math,
    can handle PObjects and negative arguments without raising an exception.

    Instead of
    @code
    from math import sqrt
    @endcode
    use
    @code
    from PObjects import sqrt
    @endcode
    to take advantage of this function.
    @param value radicant
    @return square root of radicant
    """
    return value**0.5



class PObject():
    """!
    @brief Class representing any physical object consisting of value and unit.

    Can serve as a base class to derive more specific object classes from, but
    all SI units are fully implemented in this class.  PObjects can be used like
    any other numerical objects in Python, i.e. they can be added, subtracted,
    multiplied, divided and compared.  Obviously, only PObjects with the same
    units can be added and subtracted, but PObjects with arbitrary units can be
    multiplied and divided, multiplied with and divided by regular numbers, and
    raised to a given power thereby yielding not only the SI base units m,
    kg, s, A, K, mol and cd but also the derived SI units such as Hz, N, Pa, J,
    W, C, V, F, Ω, S, Wb, T, H, and lx.  For more details on this, see class
    Unit of the module SI.  When raising a PObject to a non-integer power, only
    such operations are legal that yield valid combinations of SI units, i.e.
    usually the only non-integer power that is legal and useful is 0.5, which
    is also obtained by the sqrt function from this module.  For instance, one
    could compute
    @code
        from PObjects import PObject, sqrt
        from math import pi
        ...
        L = PObject( 5, "mH" )
        C = PObject( 4.7, "pF" )
        f = 1 / (2 * pi * sqrt( L * C ))
        print( f )
    @endcode
    which would produce the string "1.03821 MHz".
    
    The built-in functions min() and max() will also work on lists of PObjects.

    PObjects can be converted to strings and then yield human-readable results
    with engineering notation and standard SI prefixes as shown above. Again
    see the module SI for more details on this.  There are both SI units and
    prefixes (i.e. Ω and μ) that may not render correctly in cases where only
    strict ASCII characters are allowed.  The constructor of the PObject class
    accepts a parameter strictAscii, which, when set to True, will instruct the
    string conversion not to use these characters but use Ohm and u instead.
    Since neither Ω nor μ can be typed on regular ASCII keyboards, PObjects
    always accept Ohm and u as input in addition to Ω and μ.

    It is worth noting that the values used to instantiate any PObject can be
    ints, floats, or even complex numbers, the latter being of particular
    interest in electrical engineering.

    It is possible to instantiate a PObject without a unit or a "blank" unit
    string; doing so is discouraged, but, following the philosophy that simpler 
    is better, any value resulting from an arithmetic operation resulting in a
    unitless PObject will automatically be converted into a regular number (or a
    complex number if the value was complex and the unit string blank).  Only
    other unitless PObjects or regular numbers can be added to or subtracted 
    from unitless PObjects.

    At the expense of sounding like a general Python tutorial, it is worth
    noting that PObjects are mutable objects - not immutable ones such as
    integers or floats with the effect that variable names are just references
    (pointers) to existing mutable PObjects.  Therefore,
    @code
    x = PObject( 5, "kg" )
    y = x
    x *= 2
    @endcode
    will not only result in x obtaining the value of 10 kg but also y.  To avoid
    this (especially for C/C++ or Java programmers unexpected) behavior, use
    @code
    x = PObject( 5, "kg" )
    y = x.copy()
    x *= 2
    @endcode
    now only x will have a value of 10 kg and y still the value of 5 kg.
    
    To make PObjects seamlessly work in regular code, the __float__ method has
    been implemented, so that
    @code
    x = float( PObject( 0.005, "s" ) )
    @endcode
    is the same as
    @code
    x = PObject( 0.005, "s" ).value
    @endcode

    PObjects can have a value of 0 and any unit.  This is because real
    physical objects, such as voltages or currents, often can take on positive
    and negative values and exhibit smooth transitions in between.  Of course,
    strictly mathematically speaking, the numerical representation of a
    physical object consists of the product of its value and its unit, and if
    the value is zero the product is zero too.  The representation as PObject
    with a value of 0 and its regular unit was kept for strictly practical
    reasons so that currents undergoing zero-transitions still remain currents
    and the voltage drop across a superconductor is still a voltage, albeit one
    of 0 V.  It is worth noting, however, that the comparison of
    @code
    PObject( 0, "V" ) == 0
    @endcode
    evaluates to True, and the following is True too for any unit
    @code
    not PObject( 0, "A" )
    @endcode

    However, there is a difference between zero-valued PObjects of different
    units and the number 0 when used in arithmetic operations.  Even a
    zero-valued voltage PObject can only be added to or subtracted from other
    voltage PObjects, not, say, a current PObject, not even a zero-valued one.
    At the other hand, the number 0, by definition, can be added to or
    subtracted from anything, including a PObject, without changing its value.
    This becomes important when we have an existing function that, say, sums up
    its arguments in an accumulator that it initialized to zero, and we want
    to give it either a sequence of regular numbers or a sequence of PObjects
    without making changes to the function code.  Lastly, any number, including
    zero, can be multiplied with any PObject without changing the PObject's
    unit.  At the other hand, multiplying e.g. a zero-valued voltage PObject
    with any current PObject will result in a power PObject of 0 W and not in
    any current or voltage PObject.  So while potentially not holding up to
    mathematical rigor, zero-valued PObjects are very useful and implemented
    with strict consistency.

    Without going into the ontology vs. epistemology discussion here, many
    entities in physics and engineering are not known or cannot be known to an
    arbitrary level of detail, i.e. to a precision better than a given number
    of relevant digits. This class allows his number of digits to be specified,
    which will also affect any PObjects that are derived from this
    limited-precision object.  The values of PObjects without digit limitation
    are rendered as ordinary floating point numbers, whereby the Python string
    format specification will always take precedence even if the internal digit
    limitation was specified.  It is important to know that by specifying the
    'digits' parameter, only the string representation of the associated
    PObject and its derivatives are affected - not the internal representation,
    which is always a floating point number.  When two PObjects are combined
    in an arithmetic operation, the result has the smaller number of digits of
    the two, as no operation can make a result more accurate than its least
    accurate operand.  Also, calculating inherent uncertainties internally is
    beyond the scope of this class.

    Every symbol of a composite unit may carry an SI prefix (e.g. "MHz T^-1"
    or "g / cm^3").  Apart from SI units, the units eV (electron volt) and E_h
    (Hartree energy) as well as u (atomic mass unit) are accepted as input
    (with any SI prefix, also as part of composite units); they are converted
    to J and kg, respectively, internally.
    """
        
    @staticmethod
    def valueList( polist ):
        """!
        @brief Convert a list with PObjects into one with values in SI base
               units only - the unit is not returned.

        It is not checked whether all elements in the list have the same SI base
        unit.

        It is worth noting that valueList() is agnostic with respect to the
        values of the PObjects in the list.  That means that it can handle
        PObjects with complex values, but it also means that the resulting list
        may contain elements of different types.
        @param polist list with PObject-derived objects
        @return list with only values of all objects
        """
        return [PObject.__itemValue( item ) for item in polist]


    @staticmethod
    def __itemValue( item ):
        """!
        @brief Private helper for list functions: return the value of a PObject
               or 0 for the number 0, raise ValueError otherwise.
        @param item PObject or 0
        @return value of item
        """
        if isinstance( item, PObject ):
            return item.value
        if isinstance( item, numbers.Number ) and item == 0:
            return 0
        raise ValueError( "elements in list need to be PObjects or 0" )


    @staticmethod
    def floatList( polist ):
        """!
        @brief Convert a list with PObjects into one with floats of values in
               base SI units only - the unit is not returned.

        It is not checked whether all elements in the list have the same SI base
        unit.  The difference to valueList is merely that all returned elements
        are guaranteed to be floats, but passing a list with PObjects that are
        complex will result in an exception.

        The method is mostly used to pass lists of values of PObjects as arrays
        to C library programs which do not understand PObjects.
        @param polist list with PObject-derived objects
        @return list with values of all objects converted to floats
        """
        return [float( PObject.__itemValue( item ) ) for item in polist]


    @staticmethod
    def standardizedList( polist ):
        """!
        @brief Convert a list of PObjects into one with standardized (i.e. not
               necessarily base SI units) floats of values and return a tuple
               with that list and the (potentially not SI base) unit for all of
               them.

        If a conversion of all elements of the list to the same standardized
        unit is not possible, the values are converted to those with base SI
        units.  Of course, it only makes sense to convert objects to
        standardized units if they have the same SI base unit.  If not all
        elements of the list have the same SI unit or are not PObjects, a
        ValueError exception is raised.
        @param polist list with PObject-derived objects
        @return tuple with list of float values and unit for all of them
        """
        unit = None
        for element in polist:
            if isinstance( element, PObject ):
                if unit is None:
                    unit = element.unit
                elif element.unit != unit:
                    raise ValueError( "all elements in list must have same "
                                      "unit" )
            elif not (isinstance( element, numbers.Number ) and element == 0):
                raise ValueError( "elements in list need to be PObjects" )

        if unit is None:
            # only zeros in list
            return ([0] * len( polist ), "")

        # magnitudes of all non-zero elements
        magnitudes = [abs( element.value ) for element in polist
                      if isinstance( element, PObject ) and element != 0]
        if not magnitudes:
            # only zero-valued PObjects in list
            return ([0.] * len( polist ), str( unit ))

        minval = min( magnitudes )
        maxval = max( magnitudes )
        maxstd, maxunit = SI.Prefix.standardizeTuple( (float( maxval ),
                                                        unit) )
        _, minunit = SI.Prefix.standardizeTuple( (float( minval ), unit) )

        if minunit != maxunit:
            # cannot use the same prefix for all - convert to base unit
            return (PObject.floatList( polist ), str( unit ))

        # all elements are scaled with the same power of 10; dividing by an
        # exact integer power of 10 avoids rounding noise such as 1e-3 * 1e3
        exponent = round( math.log10( maxstd / maxval ) )
        if exponent >= 0:
            return ([float( PObject.__itemValue( element ) ) * 10**exponent
                     for element in polist], maxunit)
        return ([float( PObject.__itemValue( element ) ) / 10**(-exponent)
                 for element in polist], maxunit)


    def __init__( self, value, *args, **kwargs ):
        """!
        @brief Constructor - use as
        @code
        PObject( valstring[, digits=<digits>][, strictAscii=<bool>] )
        @endcode
        or
        @code
        PObject( value[, unit][, digits=<digits>][, strictAscii=<bool>] )
        @endcode
        or
        @code
        PObject( valobj[, digits=<digits>][, strictAscii=<bool>] )
        @endcode

        digits and strictAscii are optional parameters in all cases.  If unit
        is not given, a unitless PObject will be created.

        To allow more arguments in derived classes, the constructor can be
        called with more than the required number of arguments, both with and
        without keywords.  All will be stored internally and made available for
        the derived classes via the "protected" properties _args and _kwargs.
        @param value string representing the physical object including
                     numerical value and potentially unit, the numerical value
                     of the physical object, or another instance of PObject
        @param args currently only supported with one element which is then the
                    unit for the physical object either as a string or as an
                    instance of Unit (see SI.Unit)
        @param kwargs can consist of digits=<digits> and/or strictAscii=<bool>
        """

        if isinstance( value, str ):
            # called with value-and-unit string
            vlist = value.split()
            if len( vlist ) <= 2:
                # only one unit item - may contain SI prefix and can
                # be handled by SI.Prefix
                (self.__value, unit) = SI.Prefix.fromString( value )
            else:
                # more than one unit item is a composite unit whose items
                # are resolved by SI.Prefix.convertToSI() below
                self.__value = SI.Prefix.numberFromString( vlist[0] )
                unit = " ".join( vlist[1:] )
            self.__args = args
            self.__kwargs = dict( kwargs )
        elif isinstance( value, PObject ):
            # called with another PObject-derived object
            # value and unit are simply derived from it
            self.__value = value.value
            unit = value.unit
            # args and kwargs are first also derived from it - as copies so
            # that the other object is not affected by changes to ours
            self.__args = value._args
            self.__kwargs = dict( value._kwargs )
            # but supplied keyword arguments override
            self.__kwargs.update( kwargs )
        elif isinstance( value, numbers.Number ) and \
             not isinstance( value, bool ):
            # called with numerical value only, requires unit in args tuple or
            # results in unitless PObject if nothing is given
            if len( args ) < 1:
                self.__value = value
                unit = ""
            elif str == type( args[0] ):
                if len( args[0].split() ) <= 1:
                    # unit is not composite string and can have prefix
                    (self.__value, unit) = SI.Prefix.normalizeTuple(
                                                            (value, args[0]) )
                else:
                    # unit is composite string - resolved below
                    self.__value = value
                    unit = args[0]
            elif SI.Unit == type( args[0] ):
                # first argument is proper SI Unit
                self.__value = value
                unit = args[0]
            else:
                raise ValueError( "PObject not called with proper unit - "
                                  "value = {0}, args[0] = {1}"
                                  .format( value, args[0] ) )

            if len( args ) > 1:
                self.__args = args[1:]
            else:
                self.__args = ()
            self.__kwargs = dict( kwargs )
        else:
            raise ValueError( "value argument is of type {0} "
                              "but must be string, number or PObject"
                              .format( type( value ) ) )

        try:
            self.__digits = self.__kwargs["digits"]
        except KeyError:
            self.__digits = 6
            self.__kwargs["digits"] = self.digits
        try:
            self.__precision = self.__kwargs["precision"]
        except KeyError:
            self.__precision = 0
            self.__kwargs["precision"] = self.precision

        try:
            self.__strictAscii = self.__kwargs["strictAscii"]
        except KeyError:
            self.__strictAscii = False
            self.__kwargs["strictAscii"] = self.__strictAscii

        if str == type( unit ):
            # resolve prefixes in composite units and convert accepted
            # non-SI units (eV, E_h, u) into SI units
            (self.__value, unit) = SI.Prefix.convertToSI( (self.__value,
                                                           unit) )
            self.__unit = SI.Unit( unit )
        elif SI.Unit == type( unit ):
            self.__unit = unit
        else:
            raise ValueError( "unit {0} must be string or SI.Unit object "
                              "but is {1}".format( unit, type( unit ) ) )

        return


    def __str__( self ):
        """!
        @brief Return a pretty string representing the object.
        @return string containing string representation of value and unit
        """
        if self.__isPrefixable():
            return SI.Prefix.toString( (self.__value, self.__unitString()),
                                       digits=self.__digits,
                                       strictAscii=self.__strictAscii )
        if self.__digits is None:
            return self.__joinComposite( "{0}".format( self.__value ) )
        return self.__joinComposite( "{0:.{1}g}".format( self.__value,
                                                         self.__digits ) )


    def __joinComposite( self, numstr ):
        """!
        @brief Private method to join a formatted number with a composite unit;
               "1 / x" units are rendered as "<number> / x".
        @param numstr formatted number
        @return string with number and unit
        """
        unit = self.__unitString()
        if unit.startswith( "1 / " ):
            return numstr + unit[1:]
        return numstr + " " + unit


    def __format__( self, formatSpec ):
        """!
        @brief Return a pretty string representing the object with a given
        format specification.

        This method allows to override the built-in formatting, including the
        (potentially) user-specified number of significant digits.  An empty
        format specification (as in f"{obj}") yields the same result as str().
        @param formatSpec Python format specifier
        @return string containing string representation of value and unit
        """
        if not formatSpec:
            return str( self )
        if self.__isPrefixable():
            return SI.Prefix.toString( (self.__value, self.__unitString()),
                                       formatSpec=formatSpec,
                                       strictAscii=self.__strictAscii )
        return self.__joinComposite( format( self.__value, formatSpec ) )


    def __isPrefixable( self ):
        """!
        @brief Private method to determine whether the value of this object is
               real and its unit is a single symbol to which an SI prefix can be
               attached when converting the object to a string.
        """
        unit = str( self.__unit )
        return isinstance( self.__value, numbers.Real ) and \
               1 == len( unit.split( " " ) ) and -1 == unit.find( "**" )


    def __unitString( self ):
        """!
        @brief Private method to obtain the unit as string honoring strictAscii.
        """
        if self.__strictAscii:
            return str( self.__unit ).replace( "Ω", "Ohm" )
        return str( self.__unit )


    def __repr__( self ):
        """!
        @brief Return string that when evaluated will re-create the object.

        Requires the class name to be in scope, e.g. after
        @code
        from PObjects import *
        @endcode
        @return string that when evaluated will recreate the object
        """
        return "{0}( {1}, {2} )".format( self.__class__.__name__,
                                         repr( self.__value ),
                                         repr( str( self.__unit ) ) )


    def __combinedDigits( self, other ):
        """!
        @brief Private helper: number of relevant digits of the result of an
               arithmetic operation of this object with another PObject.

        No arithmetic operation can make a result more accurate than its least
        accurate operand, so the result has the smaller number of digits of the
        two operands; None means "all digits" and thus counts as infinite.
        @param other other PObject
        @return number of digits for the result
        """
        if self.__digits is None:
            return other.digits
        if other.digits is None:
            return self.__digits
        return min( self.__digits, other.digits )


    @classmethod
    def _resultClass( cls ):
        """!
        @brief "Protected" hook: class of the results of arithmetic operations
               (with other PObjects of the same unit or with numbers).

        Defaults to the class of the object itself.  Classes whose objects
        cannot take on arbitrary values (such as EEObjects, which are confined
        to an E-series) override this to return PObject, so that results of
        arithmetic operations retain full precision.
        @return class for results of arithmetic operations
        """
        return cls


    def copy( self ):
        """!
        @brief Make a (deep) copy of self.

        This is a Python idiosyncrasy - similar to the copy() method in dicts.
        """
        return copy.deepcopy( self )


    def __add__( self, other ):
        """!
        @brief Overload addition operator (self + other)
        @param other other object to add to ourselves
        @return Object of same class with result
        """
        kwargs = dict( self.__kwargs )
        if not isinstance( other, PObject ):
            if other == 0 or self.isUnitless:
                resval = self.__value + other
            else:
                raise ValueError( "can only add 0 to any PObject or any "
                                  "number to a unitless PObject" )
        elif other.unit != self.unit:
            raise ValueError( "only objects with identical units "
                              "can be added to each other" )
        else:
            resval = self.__value + other.value
            kwargs["digits"] = self.__combinedDigits( other )

        if self.isUnitless:
            return resval
        return self._resultClass()( resval, self.__unit,
                                    *self.__args, **kwargs )


    def __radd__( self, other ):
        """!
        @brief Overload addition operator (other + self)
        @param other other object to add to ourselves
        @return Object of same class with result
        """
        return self.__add__( other )


    def __iadd__( self, other ):
        """!
        @brief Overload in-place addition operator (self += other)
        @param other other object to add to ourselves
        @return self now containing result
        """
        if self._resultClass() is not type( self ):
            # objects of this class cannot take on arbitrary values (e.g.
            # EEObjects) - return a new object instead of modifying self
            return self.__add__( other )
        if not isinstance( other, PObject ):
            if other == 0 or self.isUnitless:
                self.__value += other
            else:
                raise ValueError( "can only add 0 to any PObject or any "
                                  "number to a unitless PObject" )
        elif other.unit != self.unit:
            raise ValueError( "only objects with identical units "
                              "can be added to each other" )
        else:
            self.__value += other.value
            self.digits = self.__combinedDigits( other )

        if self.isUnitless:
            return self.__value
        return self


    def __sub__( self, other ):
        """!
        @brief Overload subtraction operator (self - other)
        @param other other object to subtract from ourselves
        @return Object of same class with result
        """
        kwargs = dict( self.__kwargs )
        if not isinstance( other, PObject ):
            if other == 0 or self.isUnitless:
                resval = self.__value - other
            else:
                raise ValueError( "can only subtract 0 from any PObject "
                                  "or any number from a unitless PObject" )
        elif other.unit != self.unit:
            raise ValueError( "only objects with identical units "
                              "can be subtracted from each other" )
        else:
            resval = self.__value - other.value
            kwargs["digits"] = self.__combinedDigits( other )

        if self.isUnitless:
            return resval
        return self._resultClass()( resval, self.__unit,
                                    *self.__args, **kwargs )


    def __rsub__( self, other ):
        """!
        @brief Overload subtraction operator (other - self)
        @param other other object to subtract ourselves from
        @return Object of same class with result
        """
        kwargs = dict( self.__kwargs )
        if not isinstance( other, PObject ):
            if other == 0 or self.isUnitless:
                resval = other - self.__value
            else:
                raise ValueError( "can only subtract any PObject from 0 or "
                                  "a unitless PObject from any number" )
        elif other.unit != self.unit:
            raise ValueError( "only objects with identical units "
                              "can be subtracted from each other" )
        else:
            resval = other.value - self.__value
            kwargs["digits"] = self.__combinedDigits( other )

        if self.isUnitless:
            return resval
        return self._resultClass()( resval, self.__unit,
                                    *self.__args, **kwargs )


    def __isub__( self, other ):
        """!
        @brief Overload in-place subtraction operator (self -= other)
        @param other other object to subtract from ourselves
        @return self now containing result
        """
        if self._resultClass() is not type( self ):
            # objects of this class cannot take on arbitrary values (e.g.
            # EEObjects) - return a new object instead of modifying self
            return self.__sub__( other )
        if not isinstance( other, PObject ):
            if other == 0 or self.isUnitless:
                self.__value -= other
            else:
                raise ValueError( "can only subtract 0 from any PObject or any "
                                  "number from unitless PObject" )
        elif other.unit != self.unit:
            raise ValueError( "only objects with identical units "
                              "can be subtracted from each other" )
        else:
            self.__value -= other.value
            self.digits = self.__combinedDigits( other )

        if self.isUnitless:
            return self.__value
        return self


    def __mul__( self, other ):
        """!
        @brief Overload multiplication operator (self * other)

        If self is a PObject-derived class and other is too, the result will not
        be an object from the derived class but a proper PObject since the unit
        no longer fits the derived class.
        @param other other object to multiply ourselves with
        @return Object of same class or PObject with result
        """
        if isinstance( other, PObject ):
            kwargs = dict( self.__kwargs )
            kwargs["digits"] = self.__combinedDigits( other )
            res = PObject( self.__value * other.value,
                           self.__unit * other.unit,
                           *self.__args, **kwargs )
        else:
            res = self._resultClass()( self.__value * other, self.__unit,
                                       *self.__args, **self.__kwargs )

        if res.isUnitless:
            return res.value
        return res


    def __imul__( self, other ):
        """!
        @brief Overload in-place multiplication operator (self *= other)

        If self is a PObject-derived class and other is too, the result will not
        be an object from the derived class but a proper PObject since the unit
        no longer fits the derived class.
        @param other other object to multiply ourselves with
        @return self or PObject with result
        """
        if self._resultClass() is not type( self ):
            # objects of this class cannot take on arbitrary values (e.g.
            # EEObjects) - return a new object instead of modifying self
            return self.__mul__( other )
        if not isinstance( other, PObject ):
            self.__value *= other
            res = self
        else:
            kwargs = dict( self.__kwargs )
            kwargs["digits"] = self.__combinedDigits( other )
            res = PObject( self.__value * other.value,
                           self.__unit * other.unit,
                           *self.__args, **kwargs )

        if res.isUnitless:
            return res.value
        return res


    def __rmul__( self, other ):
        """!
        @brief Overload multiplication operator (other * self)
        @param other other object to multiply ourselves with
        @return PObject or derived objects with result
        """
        if isinstance( other, PObject ):
            raise ValueError( "We did not expect to get here" )
        res = self._resultClass()( other * self.__value, self.__unit,
                                     *self.__args, **self.__kwargs )

        if res.isUnitless:
            return res.value
        return res


    def __truediv__( self, other ):
        """!
        @brief Overload division operator (self / other)
        @param other other object to divide ourselves by
        @return Object of same class or PObject with result
        """
        if isinstance( other, PObject ):
            kwargs = dict( self.__kwargs )
            kwargs["digits"] = self.__combinedDigits( other )
            res = PObject( self.__value / other.value,
                           self.__unit / other.unit,
                           *self.__args, **kwargs )
        else:
            res = self._resultClass()( self.__value / other, self.__unit,
                                       *self.__args, **self.__kwargs )

        if res.isUnitless:
            return res.value
        return res


    def __itruediv__( self, other ):
        """!
        @brief Overload in-place addition operator (self /= other)
        @param other other object to divide ourselves by
        @return self or PObject with result
        """
        if self._resultClass() is not type( self ):
            # objects of this class cannot take on arbitrary values (e.g.
            # EEObjects) - return a new object instead of modifying self
            return self.__truediv__( other )
        if not isinstance( other, PObject ):
            self.__value /= other
            res = self
        else:
            kwargs = dict( self.__kwargs )
            kwargs["digits"] = self.__combinedDigits( other )
            res = PObject( self.__value / other.value,
                           self.__unit / other.unit,
                           *self.__args, **kwargs )

        if res.isUnitless:
            return res.value
        return res


    def __rtruediv__( self, other ):
        """!
        @brief Overload division operator (other / self)
        @param other other object to divide by ourselves
        @return PObject with result
        """
        if isinstance( other, PObject ):
            raise ValueError( "We did not expect to get here" )

        res = PObject( other / self.__value,
                       1 / self.__unit,
                       *self.__args, **self.__kwargs )

        if res.isUnitless:
            return res.value
        return res


    def __pow__( self, other ):
        """!
        @brief Overload raise to the power operator (self**other)
        @param other other object to which power to raise ourselves to
        @return always a PObject - not one of the derived objects
        """
        if other == 0:
            return 1

        if isinstance( other, PObject ):
            if other.isUnitless:
                other = other.value
            else:
                raise ValueError( "Cannot raise any object to the power "
                                  "of a PObject with non-blank unit" )

        res = PObject( self.__value**other, self.__unit**other,
                       *self.__args, **self.__kwargs )

        if res.isUnitless:
            return res.value
        return res


    def __abs__( self ):
        """!
        @brief Overload absolute value operator (abs( self ))
        @return Object of same class with result
        """
        res = self._resultClass()( abs( self.__value ), self.__unit,
                                   *self.__args, **self.__kwargs )

        if res.isUnitless:
            return res.value
        return res


    def __neg__( self ):
        """!
        @brief Overload negative sign operator (-self)
        @return Object of same class with result
        """
        res = self._resultClass()( -self.__value, self.__unit,
                                   *self.__args, **self.__kwargs )

        if res.isUnitless:
            return res.value
        return res


    def __lt__( self, other ):
        """!
        @brief Overload < operator (self < other)
        @param other other object to compare ourselves to
        """
        if not isinstance( other, PObject ):
            if not (self.isUnitless or other == 0):
                raise ValueError( "can only compare like objects" )
            return self.__value < other
        if self.unit != other.unit:
            raise ValueError( "can only compare objects with like units" )
        return self.__value < other.value


    def __le__( self, other ):
        """!
        @brief Overload <= operator (self <= other)
        @param other other object to compare ourselves to
        @return boolean value as result
        """
        if not isinstance( other, PObject ):
            if not (self.isUnitless or other == 0):
                raise ValueError( "can only compare like objects" )
            return self.__value <= other
        if self.unit != other.unit:
            raise ValueError( "can only compare objects with like units" )
        return self.__value <= other.value


    def __gt__( self, other ):
        """!
        @brief Overload > operator (self > other)
        @param other other object to compare ourselves to
        @return boolean value as result
        """
        if not isinstance( other, PObject ):
            if not (self.isUnitless or other == 0):
                raise ValueError( "can only compare like objects" )
            return self.__value > other
        if self.unit != other.unit:
            raise ValueError( "can only compare objects with like units" )
        return self.__value > other.value


    def __ge__( self, other ):
        """!
        @brief Overload >= operator (self >= other)
        @param other other object to compare ourselves to
        @return boolean value as result
        """
        if not isinstance( other, PObject ):
            if not (self.isUnitless or other == 0):
                raise ValueError( "can only compare like objects" )
            return self.__value >= other
        if self.unit != other.unit:
            raise ValueError( "can only compare objects with like units" )
        return self.__value >= other.value


    def __eq__( self, other ):
        """!
        @brief Overload == operator (self == other)
        @param other other object to compare ourselves to
        @return boolean value as result
        """
        if not isinstance( other, PObject ):
            if not (self.isUnitless or other == 0):
                return False
            return self.__value == other
        return self.__value == other.value and self.__unit == other.unit


    def __ne__( self, other ):
        """!
        @brief Overload != operator (self != other)
        @param other other object to compare ourselves to
        @return boolean value as result
        """
        if not isinstance( other, PObject ):
            if not (self.isUnitless or other == 0):
                return True
            return self.value != other
        return self.__value != other.value or self.__unit != other.unit


    def __bool__( self ):
        """!
        @brief Obtain truth value of the object, which is the truth value of its
               value.
        """
        return bool( self.__value )
    
    
    def __float__(self):
        """!
        @brief Make float work on PObjects.
        """
        return float( self.__value )


    @property
    def value( self ):
        """!
        @brief Obtain the value of a PObject.
        """
        return self.__value


    @property
    def unit( self ):
        """!
        @brief Obtain the SI.Unit of a PObject as (base) SI.Unit.
        """
        return self.__unit


    @property
    def standardizedTuple( self ):
        """!
        @brief Obtain a standardized tuple of value and standard (i.e. not
               necessarily base) SI unit.
        """
        return SI.Prefix.standardizeTuple( (self.__value, self.__unit) )


    @property
    def isUnitless( self ):
        """!
        @brief Test whether object is unitless.
        """
        return self.__unit.isUnitless


    @property
    def digits( self ):
        """!
        @brief Obtain the digits of a PObject.
        """
        return self.__digits


    @digits.setter
    def digits( self, value ):
        """!
        @brief Set the digits of a PObject.

        The setting is also passed on to objects derived from this one.
        """
        self.__digits = value
        self.__kwargs["digits"] = value
        return


    @property
    def precision( self ):
        """!
        @brief Obtain the precision of a PObject (mostly for Constants).
        """
        return self.__precision


    @property
    def _strictAscii( self ):
        """!
        @brief Obtain the strictAscii property of a PObject.
        """
        return self.__strictAscii


    @property
    def _args( self ):
        """!
        @brief Obtain non-keyword arguments we were called with
        """
        return self.__args


    @property
    def _kwargs( self ):
        """!
        @brief Obtain keyword arguments we were called with
        """
        return self.__kwargs



class Energy( PObject ):
    """!
    @brief Convenience class to represent an energy PObject.

    Because of their widespread use, this class also accepts the non-SI units
    eV, E_h, cal, and erg in its constructor.  In addition, the class can be
    instructed to use any one of the energy units eV, cal, and erg whenever an
    object is converted to a string.  The internal representation, as always,
    is strictly in the (mksA) SI system, i.e. in this case a PObject with "J" as
    unit.
    """


    # Avoid circular dependencies - define physical constants here so as not to
    # include Const
    __e_0 = scipy.constants.physical_constants['elementary charge'][0]
    # International Steam Table calorie (4.1868 J); the thermochemical calorie
    # would be scipy.constants.calorie (4.184 J)
    __calConv = scipy.constants.calorie_IT
    __ergConv = 1.0e-07
    __printUnits = ("J", "eV", "cal", "erg")

    def __init__( self, value, *args, **kwargs ):
        """!
        @brief Constructor - use as
        @code
        Energy( valstring[, printUnit=<Unit}]
                [, digits=<digits>][, strictAscii=<truth>] )
        @endcode
        or
        @code
        Energy( value, unit[, printUnit=<Unit}]
                [, digits=<digits>][, strictAscii=<truth>] )
        @endcode
        or
        @code
        Energy( object[, printUnit=<Unit}]
                [, digits=<digits>][, strictAscii=<truth>] )
        @endcode

        printUnit, digits, and strictAscii are optional parameters in all cases;
        printUnit specifies which energy unit shall be used when converting the
        object to a string.
        To allow more arguments in derived classes, the constructor can be
        called with more than the required number of arguments, both with and
        without keywords.  All will be stored internally and made available for
        the derived classes via the "protected" properties _args and _kwargs.
        @param value string representing the energy object including
                     numerical value and unit, the numerical value of the
                     energy object (unit needs to be given as first element
                     in in args), or another instance of PObject with unit J
        @param args currently only supported with one element which is then the
                    unit for the physical object either as a string or as an
                    instance of Unit (see SI.Unit)
        @param kwargs can consist of printUnit=<Unit and/or digits=<digits>
                      and/or strictAscii=<bool>
        """
        try:
            if kwargs["printUnit"] not in Energy.__printUnits:
                raise ValueError( "Wrong Energy unit specified: " +
                                  str( kwargs["printUnit"] ) )
        except KeyError:
            pass

        if isinstance( value, PObject ):
            if value.unit != "J":
                raise ValueError( "Energy can only be initialized with "
                                  "a string, a value unit pair or a PObject "
                                  "with unit J" )
            super().__init__( value, *args, **kwargs )
        else:
            if isinstance( value, str ):
                value, unit = SI.Prefix.fromString( value )
            elif len( args ) > 0:
                # unit may also be an SI.Unit object (from arithmetic
                # operations) and may contain an SI prefix
                value, unit = SI.Prefix.normalizeTuple( (value,
                                                         str( args[0] )) )
                args = args[1:]
            else:
                raise ValueError( "Energy: initialized without required unit" )

            # convert to J as needed
            if "cal" == unit:
                value *= Energy.__calConv
                unit = "J"
            elif "erg" == unit:
                value *= Energy.__ergConv
                unit = "J"
            else:
                # handles eV and E_h
                value, unit = SI.Prefix.convertToSI( (value, unit) )
            if "J" != unit:
                raise ValueError( "Wrong energy unit specified: " + unit )

            super().__init__( value, "J", *args, **kwargs )

        try:
            self.__printUnit = self._kwargs["printUnit"]
        except KeyError:
            self.__printUnit = "J"

        return


    def __str__( self ):
        """!
        @brief Return a pretty string representing the object.
        @return string containing string representation of value and unit
        """
        return self.__render( None )


    def __format__( self, formatSpec ):
        """!
        @brief Return a string representing the object in its printUnit with a
               given format specification.
        @param formatSpec Python format specifier
        @return string containing string representation of value and unit
        """
        if not formatSpec:
            return str( self )
        return self.__render( formatSpec )


    def __render( self, formatSpec ):
        """!
        @brief Private method to convert the object to a string in its
               printUnit.
        @param formatSpec Python format specifier or None
        @return string containing string representation of value and unit
        """
        if "eV" == self.__printUnit:
            value = self.value / Energy.__e_0
        elif "cal" == self.__printUnit:
            value = self.value / Energy.__calConv
        elif "erg" == self.__printUnit:
            value = self.value / Energy.__ergConv
        elif formatSpec:
            return super().__format__( formatSpec )
        else:
            return super().__str__()
        return SI.Prefix.toString( (value, self.__printUnit),
                                   self.digits, formatSpec=formatSpec,
                                   strictAscii=self._strictAscii )


    @property
    def printUnit( self ):
        """!
        @brief Obtain the default unit for __str__.

        It is important to note that this property only affects the unit with
        which this object is printed.  Internally it is always strictly stored
        mksA SI units.
        """
        return self.__printUnit


    @printUnit.setter
    def printUnit( self, unit ):
        """!
        @brief Set the default unit for __str__.

        It is important to note that this property only affects the unit with
        which this object is printed.  Internally it is always strictly stored
        mksA SI units.
        """
        if not unit in ("J", "eV", "cal", "erg"):
            raise ValueError( "Wrong Energy unit specified: " + unit )
        self.__printUnit = unit
        self._kwargs["printUnit"] = self.__printUnit
        return



class Temperature( PObject ):
    """!
    @brief Convenience class to represent a temperature PObject.

    Because of their widespread use, this class also accepts the non-SI unit ºC,
    and, grudgingly, the unit ºF in its constructor.  In addition, the class can
    be instructed to use any one of these temperature units whenever an object
    is converted to a string.  The internal representation, as always, is
    strictly in the (mksA) SI system, i.e. in this case a PObject with "K" as
    unit.  Since regular keyboards don't allow typing º, the string "deg" can be
    used as input instead, which will also be used as an output if strictAscii
    is set to True.

    It is worth noting that this class is not without inherent practical
    problems, as it will always use the internal representation of K in all
    arithmetic operations and comparisons.  For instance, multiplying a
    Temperature object with 0 will result in 0 K or -273.15 ºC, likewise any
    Temperature object will always be >= 0, regardless of which temperature
    unit the Temperature object was initialized with (or instructed to print).
    """

    __absZeroC = -273.15 # absolute zero in ºC
    __freezingF = 32     # temperature of freezing water in ºF
    __boilingF = 212     # temperature of boiling water in ºF

    __convFactor = (__boilingF - __freezingF) / 100.

    def __init__( self, value, *args, **kwargs ):
        """!
        @brief Constructor - use as
        @code
        Temperature( valstring[, printUnit=<uint>]
                     [, digits=<digits>][, strictAscii=<truth>] )
        @endcode
        or
        @code
        Temperature( value, unit[, printUnit=<uint>]
                     [, digits=<digits>][, strictAscii=<truth>] )
        @endcode
        or
        @code
        Temperature( object[, printUnit=<uint>]
                     [, digits=<digits>][, strictAscii=<truth>] )
        @endcode

        printUnit, digits, and strictAscii are optional parameters in all cases;
        printUnit specifies which energy unit shall be used when converting the
        object to a string.
        @param value string representing the temperature object including
                     numerical value and unit, the numerical value of the
                     temperature object (unit needs to be given as first element
                     in in args), or another instance of PObject with unit K
        @param args currently only supported with one element which is then the
                    unit for the physical object either as a string or as an
                    instance of Unit (see SI.Unit)
        @param kwargs can consist of printUnit=<Unit and/or digits=<digits>
                      and/or strictAscii=<bool>
        """
        try:
            kwargs["printUnit"] = \
                Temperature.__normalizePrintUnit( kwargs["printUnit"] )
        except KeyError:
            pass

        if isinstance( value, PObject ):
            if value.unit != "K":
                raise ValueError( "Temperature can only be initialized with "
                                  "a string, a value unit pair, or an object "
                                  "inheriting from PObject with unit K" )
            super().__init__( value, *args, **kwargs )
            try:
                self.__printUnit = self._kwargs["printUnit"]
            except KeyError:
                self.__printUnit = "K"
            return
        if isinstance( value, str ):
            try:
                value, unit = SI.Prefix.fromString( value )
            except ValueError as e:
                # if blank found in unit (deg C or deg F)
                tokenList = value.split( " " )
                if len( tokenList ) != 3 or tokenList[1] != "deg":
                    raise ValueError( "Temperature: malformed string: " +
                                      value ) from e
                value = float( tokenList[0] )
                unit = "º" + tokenList[2]
        elif len( args ) > 0:
            unit = str( args[0] )
            if unit.startswith( "deg " ):
                unit = unit.replace( "deg ", "º" )
            args = args[1:]
        else:
            raise ValueError( "Temperature: initialized without required unit" )


        # convert to Kelvin
        if "ºC" == unit:
            value -= Temperature.__absZeroC
        elif "ºF" == unit:
            value = (value - Temperature.__freezingF) / \
                    Temperature.__convFactor  -  Temperature.__absZeroC
        elif "K" != unit:
            raise ValueError( "Temperature: Wrong temperature unit "
                              "specified: " + unit )

        if value < 0:
            if value > -1e-9:
                # rounding error from unit conversion at absolute zero
                value = 0.
            else:
                raise ValueError( "Temperature cannot go below absolute zero" )

        super().__init__( value, "K", *args, **kwargs )

        try:
            self.__printUnit = self._kwargs["printUnit"]
        except KeyError:
            self.__printUnit = "K"

        return

    def __str__( self ):
        """!
        @brief Return a pretty string representing the object.
        @return string containing string representation of value and unit
        """
        return self.__render( None )


    def __format__( self, formatSpec ):
        """!
        @brief Return a string representing the object in its printUnit with a
               given format specification.
        @param formatSpec Python format specifier
        @return string containing string representation of value and unit
        """
        if not formatSpec:
            return str( self )
        return self.__render( formatSpec )


    def __render( self, formatSpec ):
        """!
        @brief Private method to convert the object to a string in its
               printUnit.

        In ºC and ºF, the number of digits is interpreted as significant digits
        (as everywhere else); SI prefixes are not used for these units.
        @param formatSpec Python format specifier or None
        @return string containing string representation of value and unit
        """
        if "K" == self.__printUnit:
            if formatSpec:
                return super().__format__( formatSpec )
            return super().__str__()
        if "ºC" == self.__printUnit:
            value = self.value + Temperature.__absZeroC
        else:
            value = (self.value + Temperature.__absZeroC) * \
                    Temperature.__convFactor + Temperature.__freezingF

        if self._strictAscii:
            unit = self.__printUnit.replace( "º", "deg " )
        else:
            unit = self.__printUnit

        if formatSpec:
            return format( value, formatSpec ) + " " + unit
        if self.digits is None:
            return "{0:g} {1}".format( value, unit )
        # avoid "-0" and rounding noise such as 19.999999999999996
        value = float( "{0:.{1}g}".format( value, self.digits ) ) + 0.
        return "{0:.{1}g} {2}".format( value, self.digits, unit )


    @staticmethod
    def __normalizePrintUnit( unit ):
        """!
        @brief Private method to check and normalize a temperature printUnit.
        @param unit one of "K", "ºC", "deg C", "ºF", or "deg F"
        @return normalized printUnit ("K", "ºC", or "ºF")
        """
        if "K" == unit:
            return unit
        if unit in ("ºC", "deg C"):
            return "ºC"
        if unit in ("ºF", "deg F"):
            return "ºF"
        raise ValueError( "Wrong Temperature unit specified: " + str( unit ) )


    @property
    def printUnit( self ):
        """!
        @brief Obtain the default unit for __str__.

        It is important to note that this property only affects the unit with
        which this object is printed.  Internally it is always strictly stored
        mksA SI units.
        """
        return self.__printUnit


    @printUnit.setter
    def printUnit( self, unit ):
        """!
        @brief Set the default unit for __str__.

        It is important to note that this property only affects the unit with
        which this object is printed.  Internally it is always strictly stored
        mksA SI units.
        """
        self.__printUnit = Temperature.__normalizePrintUnit( unit )
        self._kwargs["printUnit"] = self.__printUnit
        return


class Time( PObject ):
    """!
    @brief Convenience class to represent a time PObject.

    Other than a PObject with unit "s", this class returns its value in seconds, 
    minutes, hours, days, and years.  The internal represention is of course in
    seconds only.
    """

    def __init__( self, value, *args, **kwargs ):
        """!
        @brief Constructor - use as
        @code
        Time( val[, printUnit=<uint>]
              [, digits=<digits>][, strictAscii=<truth>] )
        @endcode
        or
        @code
        Time( value, unit[, printUnit=<uint>]
              [, digits=<digits>][, strictAscii=<truth>] )
        @endcode
        or
        @code
        Time( object[, printUnit=<uint>]
              [, digits=<digits>][, strictAscii=<truth>] )
        @endcode

        digits, and strictAscii are optional parameters in all cases.
        @param val  string representing the time object including
                    numerical value and unit (which must be "s") or the 
                    numerical value of the time object in seconds
        @param args currently only supported with one element which is then the
                    unit for the physical object either as a string which can be
                    "s", "min" or "minutes", "d" or "days or "y" or "years" or 
                    as an instance of Unit (see SI.Unit)
        @param kwargs can consist of printUnit=<Unit and/or digits=<digits>
                      and/or strictAscii=<bool>
        """
        if isinstance( value, PObject ):
            super().__init__( value, *args, **kwargs )
        else:
            unit = None
            if isinstance( value, str ):
                tokens = value.split()
                if 2 == len( tokens ):
                    value = SI.Prefix.numberFromString( tokens[0] )
                    unit = tokens[1]
                else:
                    value, unit = SI.Prefix.fromString( value )
                    if not unit:
                        unit = "s"
            elif len( args ) > 0:
                unit = str( args[0] )
                args = args[1:]
            else:
                unit = "s"
            if unit in ("min", "minutes"):
                value *= 60
                unit = "s"
            elif unit in ("h", "hours"):
                value *= 3600
                unit = "s"
            elif unit in ("d", "days"):
                value *= 86400
                unit = "s"
            elif unit in ("y", "years"):
                value *= Time.__SECONDS_PER_YEAR
                unit = "s"
            elif not unit.endswith( "s" ):
                raise ValueError( "Time: initialized with wrong unit: {0}"
                                  .format( unit ) )
            super().__init__( value, unit, *args, **kwargs )
        if self.unit != "s":
            raise ValueError( "Time can only be initialized with a string, a "
                              "value in seconds, a value and a unit, or an "
                              "object inheriting from PObject with unit s" )
        return

    # average Gregorian year
    __SECONDS_PER_YEAR = 31556952

    def __str__( self ):
        """!
        @brief Return a pretty string representing the object.

        Times of a minute or more are broken down into years, days, hours,
        minutes ("min"), and seconds; negative times are preceded by a minus
        sign.
        @return string containing string representation of value and unit
        """
        if not isinstance( self.value, numbers.Real ) or \
           not math.isfinite( self.value ):
            return super().__str__()

        sign = "-" if self.value < 0 else ""
        total = abs( self.value )
        if self.digits is not None:
            # round to the resolution of the seconds field (two digits before
            # the decimal point) first so that e.g. 119.9999999 s becomes
            # 2 min 0 s and not 1 min 60 s
            total = round( total, max( 0, self.digits - 2 ) )
        if total < 60:
            return super().__str__()

        years, rest = divmod( total, Time.__SECONDS_PER_YEAR )
        days, rest = divmod( rest, 86400 )
        hours, rest = divmod( rest, 3600 )
        minutes, seconds = divmod( rest, 60 )
        years, days, hours, minutes = \
            int( years ), int( days ), int( hours ), int( minutes )

        retstr = sign
        if years > 0:
            retstr += "{0:d} y ".format( years )
        if not (years == 0 and days == 0):
            retstr += "{0:d} d ".format( days )
        if not (years == 0 and days == 0 and hours == 0):
            retstr += "{0:d} h ".format( hours )
        retstr += "{0:d} min ".format( minutes )
        retstr += SI.Prefix.toString( (seconds, "s"), self.digits,
                                      strictAscii=self._strictAscii )
        return retstr


class Frequency( PObject ):
    """!
    @brief Convenience class to represent a frequency PObject.

    The only difference to instantiating a PObject with the same value and unit 
    Hz is that here we can drop the "Hz" as parameter during initialization. 
    """

    def __init__( self, value, *args, **kwargs ):
        """!
        @brief Constructor.
        @param value valstr with value and unit or float with value or PObject
                     with unit "Hz"
        @param args currently only supported with at most one element which is 
                    then the unit for the physical object either as a string 
                    which must be "Hz" (with an appropriate SI prefix), or as an
                    instance of Unit (see SI.Unit)
        @param kwargs can consist of digits=<digits> and/or strictAscii=<bool>
        """
        if isinstance( value, PObject ):
            super().__init__( value, *args, **kwargs )
        else:
            if isinstance( value, str ):
                value, unit = SI.Prefix.fromString( value )
            elif len( args ) > 0:
                unit = args[0]
                args = args[1:]
            elif 0 == len( args ):
                unit = "Hz"
            super().__init__( value, unit, *args, **kwargs )
        if self.unit != "Hz":
            raise ValueError( "Frequency can only be initialized with a "
                              "string, a value in Hz, a value unit pair, "
                              "or an object inheriting from PObject with "
                              "unit Hz" )
        return



class Mass( PObject ):
    """!
    @brief Convenience class to represent a mass PObject.
    
    The only difference to instantiating a PObject with the same value and unit 
    kg is that here we can drop the "kg" as parameter during initialization. 
    """

    def __init__( self, value, *args, **kwargs ):
        """!
        @brief Constructor - use as
        @code
        Mass( val[, printUnit=<uint>]
              [, digits=<digits>][, strictAscii=<truth>] )
        @endcode
        or
        @code
        Mass( value, unit[, printUnit=<uint>]
              [, digits=<digits>][, strictAscii=<truth>] )
        @endcode
        or
        @code
        Mass( object[, printUnit=<uint>]
              [, digits=<digits>][, strictAscii=<truth>] )
        @endcode

        digits, and strictAscii are optional parameters in all cases.
        @param val  string representing the mass object including
                    numerical value and unit, or the numerical value of the
                    mass object in kg
        @param args currently only supported with one element which is then the
                    unit for the physical object either as a string or as an
                    instance of Unit (see SI.Unit)
        @param kwargs can consist of printUnit=<Unit and/or digits=<digits>
                      and/or strictAscii=<bool>
        """
        if isinstance( value, PObject ):
            super().__init__( value, *args, **kwargs )
        else:
            if isinstance( value, str ):
                value, unit = SI.Prefix.fromString( value )
            elif len( args ) > 0:
                unit = args[0]
                args = args[1:]
            else:
                unit = "kg"
            super().__init__( value, unit, *args, **kwargs )
        if self.unit != "kg":
            raise ValueError( "Mass can only be initialized with a string, a "
                              "value in kg, a value unit pair, or an object "
                              "inheriting from PObject with unit kg" )
        return


class Length( PObject ):
    """!
    @brief Convenience class to represent a length PObject.

    In addition to the regular unit "m" this class also handles light years with
    the unit "ly".
    """

    __lyConv = 9460730472580800

    def __init__( self, value, *args, **kwargs ):
        """!
        @brief Constructor - use as
        @code
        Length( val[, printUnit=<uint>]
              [, digits=<digits>][, strictAscii=<truth>] )
        @endcode
        or
        @code
        Length( value, unit[, printUnit=<uint>]
              [, digits=<digits>][, strictAscii=<truth>] )
        @endcode
        or
        @code
        Length( object[, printUnit=<uint>]
              [, digits=<digits>][, strictAscii=<truth>] )
        @endcode

        digits, and strictAscii are optional parameters in all cases.
        @param val  string representing the length object including
                    numerical value and unit, or the numerical value of the
                    length object in m
        @param args currently only supported with one element which is then the
                    unit for the physical object either as a string or as an
                    instance of Unit (see SI.Unit).  As a string, it can be "ly"
                    representing a light year.
        @param kwargs can consist of printUnit=<Unit and/or digits=<digits>
                      and/or strictAscii=<bool>
        """
        if isinstance( value, PObject ):
            super().__init__( value, *args, **kwargs )
        else:
            if isinstance( value, str ):
                value, unit = SI.Prefix.fromString( value )
            elif len( args ) > 0:
                unit = args[0]
                if isinstance( unit, str ):
                    # resolve prefixes so that e.g. "kly" works too
                    value, unit = SI.Prefix.normalizeTuple( (value, unit) )
                args = args[1:]
            else:
                unit = "m"
            if unit == "ly":
                value *= self.__lyConv
                unit = "m"
            super().__init__( value, unit, *args, **kwargs )
        if self.unit != "m":
            raise ValueError( "Length can only be initialized with a string, a "
                              "value in m, a value and a unit, or an object "
                              "inheriting from PObject with unit m" )
        return

    def __str__( self ):
        """!
        @brief Return a pretty string representing the object.
        @return string containing string representation of value and unit
        """
        return self.__render( None )


    def __format__( self, formatSpec ):
        """!
        @brief Return a string representing the object with a given format
               specification (in light years for lengths > 1 ly).
        @param formatSpec Python format specifier
        @return string containing string representation of value and unit
        """
        if not formatSpec:
            return str( self )
        return self.__render( formatSpec )


    def __render( self, formatSpec ):
        """!
        @brief Private method to convert the object to a string.
        @param formatSpec Python format specifier or None
        @return string containing string representation of value and unit
        """
        if isinstance( self.value, numbers.Real ) and \
           abs( self.value ) > self.__lyConv:
            return SI.Prefix.toString( (self.value / self.__lyConv, "ly"),
                                       self.digits, formatSpec=formatSpec,
                                       strictAscii=self._strictAscii )
        if formatSpec:
            return super().__format__( formatSpec )
        return super().__str__()



class ImperialLengthMisfits( PObject ):
    """!
    @brief Convenience class to represent imperial length misfit units.

    We do not encourage the use of any imperial units, and under no
    circumstances must they EVER be used for internal representation of any
    physical quantities, but sometimes input and output in these units may be
    considered desirable in some remote areas of the world, which then tends to
    lead to catastrophic crashes of spacecrafts manufactured in those remote
    areas on other planets (http://mars.jpl.nasa.gov/msp98/news/mco990930.html).
    The messiness of this code (as compared to the code above) should be enough
    of a deterrent, if any should still have been needed.  You have been warned!

    We also note that unlike the common use of imperial length units, this class
    can produce consistent results using all imperial units.  For instance,
    5 ' 7 " converts to 1 Yd 2 ' 7 " if useYards is set to True.
    """

    # factor representing one inch in meters
    __INCH_FACTOR = 0.0254

    def __init__( self, value, *args, **kwargs ):
        """!
        @brief Constructor - use as
        @code
        ImperialLengthMisfits( valstring[, precision=<precision>]
                               [, useYards=<bool>])
        @endcode
        or
        @code
        ImperialLengthMisfits( value, unit[, precision=<precision>]
                               [, useYards=<bool>])
        @endcode
        or
        @code
        ImperialLengthMisfits( object[, precision=<precision>]
                               [, useYards=<bool>])
        @endcode

        precision and useYards are optional parameters in all cases.

        The valstring is a textual representation of the length with any
        combination of Miles, yards, feet, inches and mils.  Inches can be given
        in decimal or power-of-two fractions.  This code accepts all common
        abbreviations of imperial length units, but it is mandatory that they
        be separated from the numerals by a blank.  Also, inches can be given
        as an optional whole number and a fraction of powers of two.  In this
        case the whole number and the fraction must be separated by a blank.
        The parameter precision determines how the length is represented when a
        ImperialLengthMisfits object is converted to a string.  When given as a
        fraction of 1 over a power of 2, inches will be represented as whole
        numbers plus a fraction - common factors in numerator and denominator
        will be canceled if possible but the fraction will always be rounded to
        the next number given as precision.  If this precision is given as 1
        over a power of 10, inches will be presented as decimal fractions with
        as many digits as indicated by precision, i.e. 1 for 1 / 10, 2 for
        1 / 100, and so on.  If a length is too small to be represented that
        way, it will be represented in mils.  If not given, precision defaults
        to 1 / 64.  Since this class inherits from PObject, the internal
        representation of all lengths will always be in m.  If useYards is
        given and set to True, yards are also used to render the length as a
        string.  If not given or set to False, only miles, feet and inches are
        used, plus mils for very small values.
        @param value string representing the length object including
                     numerical value and unit, the numerical value of the
                     length object (unit needs to be given as first element
                     in in args), or another instance of PObject with unit m
        @param args currently only supported with one element which is then the
                    unit for the physical object either as a string or as an
                    instance of Unit (see SI.Unit)
        @param kwargs can consist of precision=<precision> and
                      useYards=<bool> - both are optional
        """
        if isinstance( value, PObject ):
            if value.unit != "m":
                raise ValueError( "ImperialLengthMisfits can only be "
                                  "initialized with a string, a value unit "
                                  "combination, or an (object inheriting from) "
                                  "PObject with unit m" )
            if isinstance( value, ImperialLengthMisfits ):
                # inherit the formatting settings of the other object unless
                # they are overridden
                merged = dict( value._kwargs )
                if "precision" in kwargs:
                    merged.pop( "inchFraction", None )
                merged.update( kwargs )
                kwargs = merged
            value = value.value
        elif isinstance( value, str ):
            valstr = value
            if valstr.find( "'" ) != -1 and valstr.find( " '" ) == -1:
                valstr = valstr.replace( "'", " '" )
                valstr = valstr.replace( "' '", "''" )
            if valstr.find( "\"" ) != -1 and valstr.find( " \"" ) == -1:
                valstr = valstr.replace( "\"", " \"" )

            value = 0
            # if we were initialized with a string, we need to parse it
            parts = valstr.split()
            i = len( parts ) - 1
            try:
                while i > 0:
                    factor = self.__unit2factor( parts[i] )
                    i -= 1
                    if factor == self.__INCH_FACTOR:
                        # we allow fractions only for inches
                        if parts[i].find( "/" ) != -1:
                            fraction = parts[i].split( "/" )
                            value += float( fraction[0] ) / \
                                     float( fraction[1] ) * factor
                            i -= 1
                            if i >= 0:
                                try:
                                    value += float( parts[i] ) * factor
                                    i -= 1
                                except ValueError:
                                    # there may only be a fraction and no
                                    # number
                                    pass
                        else:
                            value += float( parts[i] ) * factor
                            i -= 1
                    else:
                        # all other units are straightforward
                        value += float( parts[i] ) * factor
                        i -= 1
                if i >= 0:
                    # a number without unit (or a lone unit) is left over
                    raise ValueError( "number or unit missing" )
            except ValueError as e:
                raise ValueError( "Malformed string: " + valstr +
                                  " ("+ str( e ) + ")" ) from e
        elif len( args ) > 0:
            unit = args[0]
            if isinstance( unit, SI.Unit ) or "m" == str( unit ).strip():
                # metres, e.g. from arithmetic operations or repr()
                if unit != "m":
                    raise ValueError( "ImperialLengthMisfits: unit must be "
                                      "a length unit" )
            else:
                value *= self.__unit2factor( str( unit ) )
            args = args[1:]
        else:
            raise ValueError( "ImperialLengthMisfits: initialized without "
                              "required unit" )

        # convert given precision either to internal power-of-2 fraction of an
        # inch or to number of post decimal point digits; the result is kept
        # in the keyword argument inchFraction (None for decimal fractions)
        # so that the keyword argument precision remains available to
        # PObject and objects resulting from arithmetic operations keep it
        if "inchFraction" not in kwargs:
            try:
                precision = kwargs.pop( "precision" )
            except KeyError:
                precision = 1 / 64
            try:
                denominator = int( round( 1 / precision ) )
            except (ZeroDivisionError, TypeError) as e:
                raise ValueError( "ImperialLengthMisfits: precision must be "
                                  "inverse of power of 2 or power of "
                                  "10" ) from e
            if denominator < 1:
                raise ValueError( "ImperialLengthMisfits: precision must be "
                                  "inverse of power of 2 or power of 10" )
            if bool( denominator & (denominator - 1) ):
                # denominator is not power of 2
                digits = math.log10( denominator )
                if round( digits ) != digits:
                    raise ValueError( "ImperialLengthMisfits: precision must "
                                      "be inverse of power of 2 or power of "
                                      "10" )
                kwargs["inchFraction"] = None
                kwargs["digits"] = round( digits )
            else:
                kwargs["inchFraction"] = denominator

        try:
            kwargs["useYards"] = bool( kwargs["useYards"] )
        except KeyError:
            kwargs["useYards"] = False

        super().__init__( value, "m", *args, **kwargs )

        return


    def __unit2factor( self, unit ):
        """!
        @brief Convert imperial misfit unit into metric conversion factor.

        Even the use of the units is not standardized, so we have to check for
        all sorts of common uses.  We note that we do not accept a lower case
        m as an abbreviation for Mile - all other units and their abbreviations
        are case insensitive.
        """
        MILS_IN_INCH = 1000
        INCHES_IN_FOOT = 12
        FEET_IN_YARD = 3
        YARDS_IN_MILE = 1760

        if "m" == unit.strip().rstrip( "." ):
            raise ValueError( "Lower case m is not accepted as abbreviation "
                              "for Mile - use mi" )
        u = unit.strip().upper().rstrip( "." )
        if u in ("''", "\"", "IN", "INCH", "INCHES"):
            return self.__INCH_FACTOR
        if u in ("'", "FT", "FOOT", "FEET"):
            return self.__INCH_FACTOR * INCHES_IN_FOOT
        if u in("YARD", "YARDS", "YD", "Y", "YRD"):
            return self.__INCH_FACTOR * INCHES_IN_FOOT * FEET_IN_YARD
        if u in("MILE", "MILES", "MI", "M"):
            return self.__INCH_FACTOR * INCHES_IN_FOOT * FEET_IN_YARD * \
                   YARDS_IN_MILE
        if u in ("MIL", "MILS"):
            return self.__INCH_FACTOR / MILS_IN_INCH
        raise ValueError( "Wrong unit encountered: " + unit )


    def __str__( self ):
        """!
        @brief Return a pretty string representing the object.

        Fractional parts of inches will also be presented, either as fractions
        with powers of two in the denominator, or as regular decimal fractions,
        depending on what was given for the precision parameter to the
        constructor of this class.
        @return string containing string representation of value and unit
        """
        inchFraction = self._kwargs["inchFraction"]
        digits = self.digits if self.digits is not None else 6
        sign = "-" if self.value < 0 else ""
        inches = abs( self.value ) / self.__INCH_FACTOR

        if (inchFraction and inches < 1 / inchFraction) or \
           (inchFraction is None and inches < 1 / 64):
            # first we take care of really small values that we represent in mil
            if inchFraction:
                digits = 2
            fstring = "{{0:.{0}f}} mil".format( digits )
            return fstring.format( self.value / self.__unit2factor( "mil" ) )

        # count the length in integer steps of the precision (rounded) - this
        # way carries into the next higher unit happen automatically
        if inchFraction:
            steps = inchFraction
        else:
            steps = 10**digits
        count = int( math.floor( inches * steps + 0.5 ) )

        components = []
        miles, count = divmod( count, 63360 * steps )
        if miles > 0:
            components.append( str( miles ) + " mi" )
        if self._kwargs["useYards"]:
            yards, count = divmod( count, 36 * steps )
            if yards > 0:
                components.append( str( yards ) + " yd" )
        feet, count = divmod( count, 12 * steps )
        if feet > 0:
            components.append( str( feet ) + " ft" )

        # inches are "special" as they require fractions
        if count > 0:
            if inchFraction:
                wholes, fraction = divmod( count, steps )
                if fraction > 0:
                    # cancel whatever we can cancel
                    divisor = math.gcd( fraction, steps )
                    fractionString = "{0}/{1}".format( fraction // divisor,
                                                       steps // divisor )
                    if wholes > 0:
                        components.append( "{0} {1} in".format(
                                                    wholes, fractionString ) )
                    else:
                        components.append( fractionString + " in" )
                else:
                    components.append( str( wholes ) + " in" )
            else:
                fstring = "{{0:.{0}f}} in".format( digits )
                components.append( fstring.format( count / steps ) )

        return sign + " ".join( components )



# Unit Test
if "__main__" == __name__:

    import sys
    import os.path
    sys.path.append( os.path.join( os.path.dirname( __file__ ), os.pardir ) )
    from common import enableUnicodeOutput, idTupleFromFile, printCopyright, \
                       ReturnCodes
    from PObjects import Const


    def printUsage():
        """!
        @brief Print usage for unit test.
        """
        helpText = \
"""
Synopsis:
    python3 PObjects.py
This Unit test takes no parameters except the usual -h and -V flags.  It then
prompts the user for inputs for the individual tests.
"""
        print( helpText )
        return


    def main():
        """!
        @brief Main program.
        """

        NAME, REVISION, YEARS, AUTHORS = idTupleFromFile( __file__ )

        enableUnicodeOutput()

        # place arguments in argList and flags in flags
        for i in range( 1, len( sys.argv ) ):
            token = sys.argv[i]
            if token in ("-h", "--help"):
                printUsage()
                printCopyright( NAME, REVISION, YEARS, AUTHORS )
                return ReturnCodes.SUCCESS_RC
            if token in ("-V", "--Version"):
                printCopyright( NAME, REVISION, YEARS, AUTHORS )
                return ReturnCodes.SUCCESS_RC
            print( "Wrong flag or argument encountered" )
            return ReturnCodes.PARAMETER_ERROR_RC

        print( "Each of the subtests in this unit test program can be "
               "terminated by pressing Ctrl-D")

        runLoop = True
        while runLoop:
            try:
                string = input( "Enter 1st component value and unit: " )
            except (KeyboardInterrupt, EOFError):
                print( "\n" )
                runLoop = False
                continue
            try:
                o1 = PObject( string, digits=3 )
                print( "Entered: {0}".format( o1 ) )
            except ValueError as e:
                print( "Error: " + str( e ) )
                continue
            try:
                print( "o1**2 = {0}".format( o1**2 ) )
                print( "o1 * 3 = {0}".format( o1 * 3 ) )
                print( "5 * o1 = {0}".format( 5 * o1 ) )
                o1 *= 2
                print( "o1 *= 2; o1 = {0}".format( o1 ) )
                o1 /= 2
                print( "o1 /= 2; o1 = {0}".format( o1 ) )
            except ValueError as e:
                print( "Error: " + str( e ) )
            try:
                string = input( "Enter 2nd component value and unit: " )
            except (KeyboardInterrupt, EOFError):
                print( "\n" )
                runLoop = False
                continue
            try:
                o2 = PObject( string )
                print( "Entered: {0}".format( o2 ) )
                print( "o1 + o2 = {0}".format( o1 + o2 ) )
                print( "o1 - o2 = {0}".format( o1 - o2 ) )
                o1 += o2
                print( "o1 += o2; o1 = {0}".format( o1 ) )
                o1 -= o2
                print( "o1 -= o2; o1 = {0}".format( o1 ) )
            except ValueError as e:
                print( "Error: " + str( e ) )
            try:
                print( "o1 * o2 = {0}".format( o1 * o2 ) )
                try:
                    print( "o1 / o2 = {0}".format( o1 / o2 ) )
                    print( "sqrt( 1 / (o1 * o2) ) = {0}".format( sqrt (1 /
                                                                  (o1*o2))) )
                    print( "or                      {0}".format( (o1*o2)**-0.5))
                except ZeroDivisionError:
                    print( "Error! Cannot divide by zero" )
            except ValueError as e:
                print( "Error: " + str( e ) )

            try:
                olist = [o1, o2]
                vlist = PObject.valueList( olist )
                print( "As a list in base SI units:" )
                print( "o1.value = {0}, o2.value = {1}".format( vlist[0],
                                                                vlist[1] ) )
                vlist = PObject.floatList( olist )
                print( "As a list of floats in base SI units:" )
                print( "o1.value = {0}, o2.value = {1}".format( vlist[0],
                                                                vlist[1] ) )
                if o1.unit == o2.unit:
                    vlist, unit = PObject.standardizedList( olist )
                    print( "As a list with standardized values:" )
                    print( "o1 : {0} {1}, ".format(vlist[0], unit ), end="" )
                    print( "o2 : {0} {1}, ".format(vlist[1], unit ) )
            except ValueError as e:
                print( "Error: " + str( e ) )

            try:
                if o1.unit == o2.unit:
                    if o1 < o2: print( "o1 < o2" )
                    if o1 <= o2: print( "o1 <= o2" )
                    if o1 > o2: print( "o1 > o2" )
                    if o1 >= o2: print( "o1 >= o2" )
                    if o1 == o2: print( "o1 == o2" )
                if o1 != o2: print( "o1 != o2" )
            except ValueError as e:
                print( "Error: " + str( e ) )

        runLoop = True
        while runLoop:
            try:
                string = input( "Enter energy and unit: " )
            except (KeyboardInterrupt, EOFError):
                print( "\n" )
                runLoop = False
                continue
            try:
                e = Energy( string )
                print( "With base unit: {0}".format( e ) )
                e.printUnit = "eV"
                print( e )
                e.printUnit = "cal"
                print( e )
                e.printUnit = "erg"
                print( e )
            except ValueError as e:
                print( "Error: " + str( e ) )

        runLoop = True
        while runLoop:
            try:
                string = input( "Enter temperature and unit: " )
            except (KeyboardInterrupt, EOFError):
                print( "\n" )
                runLoop = False
                continue
            try:
                temp = Temperature( string )
                print( "With base unit: {0}".format( temp ) )
                temp.printUnit = "ºC"
                print( temp )
                temp.printUnit = "ºF"
                print( temp )
            except ValueError as e:
                print( "Error: " + str( e ) )

        runLoop = True
        while runLoop:
            try:
                string = input( "Enter number and imperial length unit: " )
            except (KeyboardInterrupt, EOFError):
                print( "\n" )
                runLoop = False
                continue
            try:
                length = ImperialLengthMisfits( string )
                print( "This was: {0}".format( length ) )
                length = ImperialLengthMisfits( string, precision=1/1000 )
                print( "or using decimal precision: {0}".format( length ) )
                length = ImperialLengthMisfits( string, useYards=True )
                print( "or using yards: {0}".format( length ) )
                print( "or in SI units: {0}".format( PObject( length ) ) )
            except ValueError as e:
                print( "Error: " + str( e ) )

        print( u"m\u2091 = {0}".format( Const.m_e ) )
        print( u"e\u2080 = {0}".format( Const.e_0 ) )
        print( "ℏ = {0}".format( Const.hbar ) )

        return ReturnCodes.SUCCESS_RC


    sys.exit( int( main() or 0 ) )
