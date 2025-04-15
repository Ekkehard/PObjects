# Python Implementation: SI
# -*- coding: utf-8 -*-
##
# @file       SI.py
#
# @version    2.0.0
#
# @par Purpose
#             Implement the International System of Units (SI Units) for Physics
#             toolbox package for Python.
#
# @par Comments
#             This code replaces the module SIPrefix from the same author.  It
#             combines the functions from this module into a Prefix class and
#             adds a Unit class.  The code in this module is the "secret sauce"
#             behind the PObject class.
# @par
#             Since this code uses "μ" to represent the e-06 prefix and "Ω" to
#             represent Ohms, this file must be utf-8 encoded.  In input
#             strings, both "μ" and "u"  as well as "Ohm" and "Ω" are accepted.
#             In output strings "μ" and "Ω" are used unless the parameter
#             strictAscii is set to True.
# @par
#             This is Python 3 code!

# Known Bugs: none
#
# @author     W. Ekkehard Blanz <Ekkehard.Blanz@gmail.com>
#
# @copyright
#            Copyright (C) 2018-2022 W. Ekkehard Blanz
#            See NOTICE.md and LICENSE.md files that come with this distribution
#

# File history:
#
#      Date         | Author         | Modification
#   ----------------+----------------+------------------------------------------
#   Tue Feb 13 2018 | Ekkehard Blanz | created
#   Thu Feb 15 2018 | Ekkehard Blanz | added unitless to Unit and changed SI
#                   |                | class name to Prefix
#   Sat Feb 17 2018 | Ekkehard Blanz | changed unitless to isUnitless and
#                   |                | fromString to toTuple; added toObject
#   Sun Feb 18 2018 | Ekkehard Blanz | made independent of other Toolbox modules
#   Wed Aug 08 2018 | Ekkehard Blanz | made standardizeTuple and normalizeTuple
#                   |                | public methods
#   Tue Jan 15 2019 | Ekkehard Blanz | now also works with "cm"
#   Wed Jan 16 2019 | Ekkehard Blanz | fixed a few bugs related to mass units
#   Thu Jan 17 2019 | Ekkehard Blanz | fixed a bug printing values without
#                   |                | prefixes
#   Fri Jan 18 2019 | Ekkehard Blanz | fixed a bug of mistaken prefix
#   Wed Feb 13 2019 | Ekkehard Blanz | vastly improved documentation
#   Tue Mar 12 2019 | Ekkehard Blanz | made __pow__() more flexible
#   Wed Apr 13 2022 | Ekkehard Blanz | made Part of the Physics package
#   Mon Jul 18 2022 | Ekkehard Blanz | added formatSpec parameter to
#                   |                | Prefix.toString()
#                   |                |


import math


class Unit():
    """!
    @brief Class for objects to represent SI units.

    These objects can be multiplied and divided like real SI units using paper
    and pencil.  Apart from the SI base units
    - m   meter
    - kg  kilogram
    - s   second
    - A   Ampere
    - K   Kelvin
    - mol mol
    - cd  candela

    this class also supports the derived units
     - Hz Hertz
     - N  Newton
     - Pa Pascal
     - J  Joule
     - W  Watt
     - C  Coulomb
     - V  Volt
     - F  Farad
     - Ω  Ohm (Ohm as input and as output if strictAscii was set to True)
     - S  Siemens
     - Wb Weber
     - T  Tesla
     - H  Henry
     - lx lux

    All these derived units are created from the base units by multiplying and
    dividing two or more of them.

    There is the SI unit Ω that may not render correctly in cases where only
    strict ASCII characters are supported.  The constructor of the Unit class
    accepts a parameter strictAscii, which, when set to True, will instruct the
    string conversion not to use this character but use Ohm instead. Since Ω
    cannot be typed on regular ASCII keyboards, Unit always accept Ohm as input
    in addition to Ω.
    """

    # each of the SI base units is represented by a unique prime.
    __baseDict = {2:"m", 3:"kg", 5:"s", 7: "A", 11:"K", 13:"mol", 17:"cd"}

    # Below, the full representation consists of a rational number with these
    # primes in numerator and denominator implemented as a tuple. Combined SI
    # units are represented as compound numbers using the prime factors of their
    # constituents, again, as rational numbers.  This way, the units can be
    # easily canceled in numerator and denominator.  The tuple representing the
    # rational number serves as a key into the names dictionary.
    __namesDict = {
        (1, 1): "",
        (2, 1): "m",
        (3, 1): "kg",
        (5, 1): "s",
        (7, 1): "A",
        (11, 1): "K",
        (13, 1): "mol",
        (17, 1): "cd",
        (1, 5): "Hz",
        (6, 25): "N",
        (3, 50): "Pa",
        (12, 25): "J",
        (12, 125): "W",
        (35, 1): "C",
        (12, 875): "V",
        (30625, 12): "F",
        (12, 6125): "Ω",
        (6125, 12): "S",
        (12, 175): "Wb",
        (3, 175): "T",
        (12, 1225): "H",
        (17, 4): "lx"
        }

    def __init__( self, unit, strictAscii=False ):
        """!
        @brief Constructor, takes a string (or a rational number tuple)
        representing an SI unit as an argument.

        The tuple is mostly for internal use when overloading operators.
        @param unit base unit to be represented by this object
        @param strictAscii set to True to print "Ω" as "Ohm"
        """
        if str != type( unit ) and tuple != type( unit ):
            raise ValueError( "SI.Unit only takes strings and tuples "
                              "as arguments" )

        self.__strictAscii = strictAscii

        if tuple == type( unit ):
            num, den = unit
            self.__numerator = num // math.gcd( num, den )
            self.__denominator = den // math.gcd( num, den )
        else:
            if "Ohm" == unit: unit = "Ω"
            if unit.count( "/" ) > 1:
                raise ValueError( "Can only use one '/' - use parentheses "
                                  "for numerator and denominator" )
            unit = unit.replace( "(", "" ).replace( ")", "" )
            self.__numerator = 1
            self.__denominator = 1
            numerator = True
            for token in unit.split( " " ):
                if "1" == token: continue
                if "/" == token:
                    numerator = False
                    continue
                pos = token.find( "**" )
                if -1 == pos:
                    power = 1
                else:
                    power = int( token[pos+2:] )
                    token = token[:pos]

                found = False
                for (tup, name) in Unit.__namesDict.items():
                    if name == token:
                        num, den = tup
                        if numerator:
                            self.__numerator *= num**power
                            self.__denominator *= den**power
                        else:
                            self.__numerator *= den**power
                            self.__denominator *= num**power
                        found = True
                if not found:
                    raise ValueError( "Unknown unit name specified: " + token )
        return



    def __str__( self ):
        """!
        @brief Return a pretty string representing the object.
        @return string containing string representation of units
        """
        if 1 == self.__numerator and 1 == self.__denominator: return ""
        try:
            return Unit.__namesDict[(self.__numerator, self.__denominator)]
        except KeyError:
            try:
                retstrNum = "1"
                retstrDen = Unit.__namesDict[(self.__denominator,
                                               self.__numerator)]
            except KeyError:
                retstrNum = self.__components( self.__numerator )
                if not retstrNum: retstrNum = "1"
                retstrDen = self.__components( self.__denominator )

        if retstrDen:
            if 1 == len( retstrDen.split( " " ) ):
                retstr = retstrNum + " / " + retstrDen
            else:
                retstr = retstrNum + " / (" + retstrDen + ")"
        else:
            retstr = retstrNum

        if self.__strictAscii:
            retstr = retstr.replace( "Ω", "Ohm" )

        return retstr



    def __repr__( self ):
        """!
        @brief Return technical representation of the object.
        @return Evaluable string recreating the object
        """
        return "Unit( (" + str( self.__numerator ) + ", " + \
                           str( self.__denominator ) + ") )"



    def __components( self, n ):
        """!
        @brief Private method to obtain components of a composite "unit."

        Uses Euler's algorithm to compute prime factorization and then collects
        equal elements to represent them as units raised to some power.
        @param n integer representing composite SI unit
        @return string with all components
        """
        i = 2
        components = ""
        while i * i <= n:
            if n % i:
                i += 1
            else:
                n //= i
                components += Unit.__baseDict[i] + " "
        if n > 1:
            components += Unit.__baseDict[n] + " "
        components = components.strip()

        l = components.split( " " )
        index = 0
        while index < len( l ) - 1:
            if l[index+1] != l[index]:
                index += 1
                continue
            item = l[index]
            count = 1
            index += 1
            while l[index] == item:
                count += 1
                index += 1
                if index >= len( l ): break
            rs = ((item + " ") * count).strip()
            components = components.replace( rs,
                                             "{0}**{1}".format( item, count ) )
        return components



    @property
    def _numerator( self ):
        """!
        @brief Obtain numerator of this object.
        For internal use in operator overloading.
        """
        return self.__numerator



    @property
    def _denominator( self ):
        """!
        @brief Obtain denominator of this object.
        For internal use in operator overloading.
        """
        return self.__denominator



    @property
    def isUnitless( self ):
        """!
        @brief Test whether unit is 1 / 1.
        """
        return 1 == self.__numerator and 1 == self.__denominator



    def __mul__( self, other ):
        """!
        @brief Overloading multiplication.
        @param other other SI.Unit object to multiply with
        @return SI.Unit object with multiplied units
        """
        if Unit != type( other ):
            raise ValueError( "can only multiply SI.Units with each other" )
        num = self.__numerator * other._numerator
        den = self.__denominator * other._denominator
        return Unit( (num, den) )



    def __truediv__( self, other ):
        """!
        @brief Overloading division (self / other).
        @param other other SI.Unit object to divide this unit by
        @return SI.Unit object with divided units
        """
        if Unit != type( other ):
            raise ValueError( "can only divide SI.Units by each other" )
        num = self.__numerator * other._denominator
        den = self.__denominator * other._numerator
        return Unit( (num, den) )



    def __rtruediv__( self, other ):
        """!
        @brief Overloading right hand side division (other / self).
        @param other other SI.Unit object to be divided by this unit
        @return SI.Unit object with divided units
        """
        if Unit != type( other ) and other != 1:
            raise ValueError( "can only divide SI.Units by each other" )
        if 1 == other:
            den = int( self.__numerator )
            num = int( self.__denominator )
        else:
            den = self.__numerator * other._denominator
            num = self.__denominator * other._numerator
        return Unit( (num, den) )



    def __pow__( self, power ):
        """!
        @brief Raise unit to the power-th power.

        If power is any integer, the method will succeed.  If power is +/- 0.5,
        the method may succeed; in all other cases the method will likely not
        succeed as it will probably not result in a quotient of SI base units.
        If that cannot be achieved, a ValueError will be raised.
        @param power power unit should be raised to
        @return SI.Unit object with raised to the power-th power
        """
        if 1 == self.__numerator and 1 == self.__denominator: return self

        if power >= 1 and int( power ) == power:
            num = self.__numerator**int( power )
            den = self.__denominator**int( power )
        elif power <= -1 and int( power ) == power:
            den = self.__numerator**int( power )
            num = self.__denominator**int( power )
        elif power == 0:
            return (1, 1)
        elif power > 0:
            num = self.__numerator**power
            den = self.__denominator**power
            if int( num ) != num or int( den ) != den:
                if power == 0.5:
                    raise ValueError( "Cannot compute square root of "
                                      "unit {0}".format( self ) )
                raise ValueError( "Cannot compute {0}-th power of "
                                  "unit {1}".format( power, self ) )
        elif power < 0:
            den = self.__numerator**(-power)
            num = self.__denominator**(-power)
            if int( num ) != num or int( den ) != den:
                raise ValueError( "Cannot compute {0}-th power of "
                                  "unit {1}".format( power, self ) )

        return Unit( (int( num ), int( den )) )



    def __eq__( self, other ):
        """!
        @brief Overloading equality check.
        @param other other SI.Unit object to be checked against
        @return True or False
        """
        if isinstance( other, Unit ):
            pass
        elif str == type( other ):
            other = Unit( other )
        else:
            raise ValueError( "can only compare Unit with other Unit" )
        return self.__numerator == other._numerator and \
               self.__denominator == other._denominator




    def __ne__( self, other ):
        """!
        @brief Overloading inequality check.
        @param other other SI.Unit object to be checked against
        @return True or False
        """
        if isinstance( other, Unit ):
            pass
        elif str == type( other ):
            other = Unit( other )
        else:
            raise ValueError( "can only compare Unit with other Unit" )
        return self.__numerator != other._numerator or \
               self.__denominator != other._denominator



class Prefix():
    """!
    @brief Convert raw numbers and units of PObjects to SI prefix format and
    vice versa.

    The code in this class is very straightforward and does not convert one SI
    prefix into another - it strictly converts an internal representation of a
    physical entity into the most compact ("standard"") representation using SI
    prefixes on the one hand, and a string representation of arbitrary base unit
    and SI prefixes into an internal presentation using strictly mksA SI base
    units only.  It is assumed that the internal representation (as returned by
    fromString()) is always in SI units.

    When it comes to the representation of masses, the code does the intuitively
    "right thing" and uses the mass units "g", "kg", and "t" in the obvious ways
    for both formatted input and output.  The internal representation, i.e. the
    return value from fromString(), is still always in kg.

    This class uses the following prefixes:
     - y (yocto) for e-24
     - z (zepto) for e-21
     - a (atto)  for e-18
     - f (femto) for e-15
     - p (pico)  for e-12
     - n (nano)  for e-09
     - μ (micro) for e-06 (u as input and as output if strictAscii was set True)
     - m (milli) for e-03
     - c (centi) for e-02 (only used if the unit is m)
     - k (kilo)  for e+03
     - M (Mega)  for e+06
     - G (Giga)  for e+09
     - T (Tera)  for e+12
     - P (Peta)  for e+15
     - E (Exa)   for e+18
     - Z (Zetta) for e+21
     - Y (Yotta) for e+24

    There is the prefix μ that may not render correctly in cases where only
    strict ASCII characters are allowed.  All methods of the Prefix class
    accept a parameter strictAscii, which, when set to True, will instruct the
    string conversion not to use this character but use u instead.  Since μ can
    not be typed on regular keyboards, Prefix always accepts u as input in
    addition to μ.

    This class has only class methods (static methods) and does not need to be
    instantiated.
    """


    @staticmethod
    def toString( valueTuple, precision=3, formatSpec=None, strictAscii=False ):
        """!
        @brief Convert a number and base unit to an SI-prefix formatted string.
        @param valueTuple with number to be formatted and its SI base unit
        @param precision total number of digits to print (if set to None, all
        relevant digits are printed - defaults to 3)
        @param formatSpec Python format spec, if not None (default),
        precision will be ignored
        @param strictAscii if set to True, only strict ASCII characters are
        returned
        @return formatted string containing number and unit with SI prefix
        """

        if not tuple == type( valueTuple ):
            raise ValueError( "toString() requires (value, unit) tuple "
                              "as argument" )

        (newval, unit) = Prefix.standardizeTuple( valueTuple, strictAscii )

        if formatSpec:
            return format( newval, formatSpec ) + " " + unit
        else:
            if precision is not None and newval != 0:
                # difference to next integer
                delta = abs( round( newval ) - newval )
                predigits = max( 0,
                                 math.floor( math.log10( abs( newval ) ) ) + 1 )
                postdigits = max( 0, precision - predigits )

                if abs( newval ) > 1 and delta <= 5 * 10**(-postdigits - 1):
                    # we've got something close enough to an integer
                    newval = round( newval )
                    fstring = "{0} {1}"
                else:
                    if abs( newval ) > 1.e27 or abs( newval ) < 1.e-24:
                        fstring = "{{0:.{0}g}} {{1}}".format( postdigits )
                    else:
                        fstring = "{{0:.{0}f}} {{1}}".format( postdigits )
            else:
                fstring = "{0:g} {1}"

            return fstring.format( newval, unit )


    @staticmethod
    def fromString( string, strictAscii=False ):
        """!
        @brief Convert a string with a number plus SI prefix and unit to a
        number and unit tuple.

        The function allows both "μ" and "u" to indicate the 10**-6 SI prefix.
        @param string string with number, prefix, and unit
        @param strictAscii if set to True, only strict ASCII characters are
        returned
        @return tuple with number and base unit
        """

        try:
            tokenList = string.split( " " )
        except ValueError:
            tokenList = [string]

        if len( tokenList ) == 1:
            number = float( string )
            return (number, "")
        if len( tokenList ) != 2:
            raise ValueError( "SI.fromString: malformed string: " + string )

        return Prefix.normalizeTuple( (float( tokenList[0] ), tokenList[1]),
                                      strictAscii )



    @staticmethod
    def normalizeTuple( valueTuple, strictAscii=False ):
        """!
        @brief Normalize a (value, unit) tuple to one with base unit without
               prefix.
        The function allows both "μ" and "u" to indicate the 10**-6 SI prefix.
        Moreover, the function converts "Ohm" to "Ω" when strictAscii is False
        and "Ω" to "Ohm" when strictAscii is true.
        @param valueTuple (value, unit) tuple where unit may or may not be an
                          SI base unit
        @param strictAscii set True to get only 8-bit ASCII characters
        @return (value, baseUnit) tuple where baseUnit is an SI base unit
        """
        prefixes = {"y":-24, "z":-21, "a":-18, "f":-15, "p":-12, "n":-9, "u":-6,
                    "μ":-6, "m":-3, "c":-2, "":0, "k":3, "M":6, "G":9, "T":12,
                    "P":15, "E":18, "Z":21, "Y":24}

        (value, unit) = valueTuple

        if int == type( value ):
            value = float( value )

        if Unit == type( unit ):
            unit = str( unit )

        if not isinstance( value, float ) or not isinstance( unit, str ):
            raise ValueError( "wrong data types supplied in valueTuple" )

        unit = unit.strip()
        if len( unit ) > 1 and \
           "kg" != unit and "cal" != unit and "mol" != unit and "cd" != unit:
            baseUnit = unit[1:]
            prefix = unit[0]
        else:
            baseUnit = unit
            prefix = ""

        try:
            power = prefixes[prefix]
        except KeyError:
            # likely mistaken unit for prefix - then there is no prefix
            baseUnit = unit
            power = 0

        number = float( value ) * 10**power

        if baseUnit:
            # internally, all units are strictly mksA SI units,
            # i.e. g and t are converted to kg
            if "t" == baseUnit:
                baseUnit = "kg"
                number *= 1000.
            elif "g" == baseUnit:
                baseUnit = "kg"
                number /= 1000.

            # whether we allow "Ω" as base unit depends on the setting of
            # strictAscii
            if "Ω" == baseUnit and strictAscii:
                baseUnit = "Ohm"
            elif "Ohm" == baseUnit and not strictAscii:
                baseUnit = "Ω"

        return (number, baseUnit)



    @staticmethod
    def standardizeTuple( valueTuple, strictAscii=False, integerBits=None ):
        """!
        @brief Standardize a (value, baseUnit) tuple to one with optimally SI-
               prefixed unit.

        For lengths, the prefix "c" is used as appropriate.  For masses, values
        less than 1 kg will be returned in grams (with the appropriate prefix),
        and those >= 1000 kg will be returned as tons (again with the
        appropriate prefix).
        @param (value, baseUnit) tuple where unit may or may not be an SI base
        @param strictAscii set True to get only 8-bit ASCII characters
        @param integerBits if not None, returned value will be integer and unit
        will be adjusted to allow as precise a representation as possible in the
        given number of bits; if that number is negative, a signed integer is
        assumed.
        @return (value, unit) tuple where unit is an SI-prefixed unit string
        """

        if strictAscii:
            prefixes = {-24:"y", -21:"z", -18:"a", -15:"f", -12:"p", -9:"n",
                        -6:"u", -3:"m", -2:"c", 0:"", 3:"k", 6:"M", 9:"G",
                        12:"T", 15:"P", 18:"E", 21:"Z", 24:"Y"}
        else:
            prefixes = {-24:"y", -21:"z", -18:"a", -15:"f", -12:"p", -9:"n",
                        -6:"μ", -3:"m", -2:"c", 0:"", 3:"k", 6:"M", 9:"G",
                        12:"T", 15:"P", 18:"E", 21:"Z", 24:"Y"}

        (number, baseUnit) = Prefix.normalizeTuple( valueTuple, strictAscii )

        if not baseUnit:
            return (number, baseUnit)

        absval = abs( number )
        sign = math.copysign( 1, number )

        try:
            power10 = math.floor( math.log10( absval ) )
        except ValueError:
            # fall back to "g-formatting" in case the number is close enough to
            # 0 to cause a ValueError exception here
            return (number, baseUnit)

        if "m" == baseUnit and power10 in (-1, -2) and not integerBits:
            # cm are different as the exponent is not evenly divisible by 3
            # but we use the "c"-prefix only for length units;
            # we also don't use it when we represent the number as a strict
            # integer so as not to break the computational logic below
            prefixIndex = -2
        else:
            prefixIndex = (power10 // 3) * 3

        if "kg" == baseUnit:
            # deal with the g, kg, t mess for masses
            if prefixIndex >= 3 and prefixIndex <= 27:
                baseUnit = "t"
                absval /= 1000.
                prefixIndex -= 3
            elif prefixIndex < 0 and prefixIndex >= -27:
                baseUnit = "g"
                absval *= 1000.
                prefixIndex += 3
            # if we cannot represent the mass with standard prefixes, we resort
            # to representing it as "kg" and powers of 10

        newval = absval / 10**prefixIndex * sign

        if integerBits is not None:
            if integerBits < 0:
                maxval = 2**(1 - integerBits - 2) - 1
            else:
                maxval = 2**integerBits - 1

            while abs( newval ) * 1000 < maxval:
                newval *= 1000
                prefixIndex -= 3
            newval = round( newval )

        try:
            prefix = prefixes[prefixIndex]
        except KeyError:
            # fall back to "g-formatting" in the relatively rare cases where the
            # number is outside the range covered by SI prefixes
            newval = number
            prefix = ""

        return (newval, prefix + baseUnit)





# Unit Test
if "__main__" == __name__:

    import sys
    import os.path
    sys.path.append( os.join( os.path.dirname( __file__ ), os.pardir ) )
    from common import idTupleFromFile, enableUnicodeOutput, printCopyright, \
                       ReturnCodes


    def printUsage():
        """!
        @brief Print simple usage statement.
        """
        helpText = \
"""
Synopsis:
    python3 SI.py
This Unit test takes no parameters except the usual -h and -V flags.  It then
prompts the user for inputs for the individual tests.
"""
        print( helpText )
        return


    def main():
        """!
        @brief Main program
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

        print( "\nTo skip or end SI test type Ctrl-D" )
        runLoop = True
        while runLoop:
            try:
                string = input( "Enter number, an SI prefix, and an SI unit " +
                                "(no blank between the latter two)\n" )
            except (KeyboardInterrupt, EOFError):
                print( "\n" )
                runLoop = False
                continue
            try:
                (number, unit) = Prefix.fromString( string )
            except ValueError as e:
                print( "Error: " + str( e ) )
                continue
            print( "Number:    {0:g}".format( number ) )
            print( "Base Unit: {0:s}".format( unit ) )
            string = Prefix.toString( (number, unit) )
            print( "Formatted string:  {0:s}".format( string ) )

        runLoop = True
        while runLoop:
            try:
                string = input( "Enter 1st SI unit: ")
            except (KeyboardInterrupt, EOFError):
                print( "\n" )
                runLoop = False
                continue
            unit1 = Unit( string )
            print( "Entered: {0}".format( unit1 ) )
            newUnit = 1 / unit1
            print( "Inverse unit: {0}".format( newUnit ) )
            try:
                string = input( "Enter 2nd SI unit: ")
            except (KeyboardInterrupt, EOFError):
                print( "\n" )
                runLoop = False
                continue
            unit2 = Unit( string )
            print( "Entered: {0}".format( unit2 ) )
            newUnit = unit1 * unit2
            print( "unit1 * unit2: {0}".format( newUnit ) )
            newUnit = unit1 / unit2
            print( "unit1 / unit2: {0}".format( newUnit ) )
            print( "unit1 == unit2: {0}".format( unit1 == unit2 ) )

        unit1 = Unit( "H" )
        unit2 = Unit( "F" )
        newUnit = (unit1 * unit2)**(-0.5)
        print( "That should show Hz: {0}".format( newUnit ) )

        return ReturnCodes.SUCCESS_RC


    sys.exit( int( main() or 0 ) )
