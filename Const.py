# Python Implementation: Const
##
# @file       Const.py
#
# @version    2.0.0
#
# @par Purpose
#             Constants for PObjects toolbox package for Python.
#
# @par Comments
#
# @par
#             This is Python 3 code!

# Known Bugs: none
#
# @author     W. Ekkehard Blanz <Ekkehard.Blanz@gmail.com>
#
# Copyright
#            Copyrigh W. Ekkehard Blanzt <Ekkehard.Blanz@gmail.com> (C) 2022-2024
#            See NOTICE.md and LICENSE.md files that come with this distribution
#
# File history:
#
#      Date         | Author         | Modification
#   ----------------+----------------+------------------------------------------
#   Wed Apr 13 2022 | Ekkehard Blanz | extracted from Physics.py and made
#                   |                | part of Physics package
#   Tue Dec 17 2024 | Ekkehard Blanz | renamed package to PObjects
#   Wed Jun 18 2025 | Ekkehard Blanz | now gets all constants from scipy and
#                   |                | added function fromScipy()
#                   |                |

import math
import scipy
from PObjects import PObject
import classutilities

# Physical Constants:

class Const( classutilities.ClassPropertiesMixin ):
    """!
    @brief Physical constants class.

    If this class is included like so
    @code
    from PObjects import Const
    @endcode
    constants can be obtained as
    @code
    x = Const.<constant name>
    @endcode
    without ever instantiating class Const.

    This is an interface class to obtain the physical constants in scipy as 
    PObjects.  Additionally, constants can be accessed more easily using 
    mnemonic names rather than the names (strings) used in scipy.  However, the 
    scipy constants can still be converted to PObjects using the names as 
    strings via the (static) function fromScipy; this function also allows to 
    access all the constants that are not implemented as shortcuts here.  The 
    constants currently supported here are ("g" isn't really a constant but used
    often):
    - e_0       elementary charge
    - m_e       electron mass
    - amu       atomic mass unit
    - m_p       proton mass
    - m_n       neutron mass
    - c_0       speed of light in vacuum
    - h         Planck's constant
    - hbar      Planck's constant divided by 2 pi
    - N_A       Avogadro's number
    - R         general gas constant
    - k_B       Boltzmann constant
    - G         gravitational constant
    - g         acceleration at equator and see level due to gravity
    - mu_0      vacuum permeability
    - epsilon   vacuum permittivity

    All physical constants are returned as PObjects with proper units, i.e. they
    can be subjected to any arithmetic operation with themselves and other
    PObjects and yield correct results (including units) and the statement
    @code
    print( Const.hbar )
    @endcode
    will produce the string "1.05457e-34 m**2 kg / s".
    """
    
    @staticmethod
    def fromScipy( name ):
        """!
        @brief Return a scipy constant with a given name as PObject.
        @param name name of constant as used in scipy.physical_constants
        @return constant as a PObject (including value and unit)
        """
        return PObject( scipy.constants.physical_constants[name][0],
                        scipy.constants.physical_constants[name][1],
                        precision=scipy.constants.physical_constants[name][2] )
                        
    @classutilities.classproperty
    def e_0( cls ):
        """!
        @brief elementary charge
        """
        return Const.fromScipy( 'elementary charge' )

    @classutilities.classproperty
    def m_e( cls ):
        """!
        @brief electron mass
        """
        return Const.fromScipy( 'electron mass' )

    @classutilities.classproperty
    def amu( cls ):
        """!
        @brief atomic mass unit
        """
        return Const.fromScipy( 'atomic mass constant' )

    @classutilities.classproperty
    def m_p( cls ):
        """!
        @brief proton mass
        """
        return Const.fromScipy( 'proton mass' )

    @classutilities.classproperty
    def m_n( cls ):
        """!
        @brief neutron mass
        """
        return Const.fromScipy( 'neutron mass' )

    @classutilities.classproperty
    def c_0( cls ):
        """!
        @brief speed of light in vacuum
        """
        return Const.fromScipy( 'speed of light in vacuum' )

    @classutilities.classproperty
    def h( cls ):
        """!
        @brief Planck's constant
        """
        return Const.fromScipy( 'Planck constant' )

    @classutilities.classproperty
    def hbar( cls ):
        """!
        @brief Planck's constant divided by 2 pi
        """
        return Const.h / (2. * math.pi)

    @classutilities.classproperty
    def N_A( cls ):
        """!
        @brief Avogadro's number
        """
        return Const.fromScipy( 'Avogadro constant' )

    @classutilities.classproperty
    def R( cls ):
        """!
        @brief general gas constant
        """
        return Const.fromScipy( 'molar gas constant' )

    @classutilities.classproperty
    def k_B( cls ):
        """!
        @brief Boltzmann constant
        """
        return Const.R / Const.N_A

    @classutilities.classproperty
    def G( cls ):
        """!
        @brief gravitational constant
        """
        return Const.fromScipy( 'Newton constant of gravitation' )

    @classutilities.classproperty
    def g( cls ):
        """!
        @brief acceleration at equator and sea level due to gravity -
               this is not really a "constant" but often needed anyway
        """
        return Const.fromScipy( 'standard acceleration of gravity' )

    @classutilities.classproperty
    def mu_0( cls ):
        """!
        @brief Vacuum magnetic permeability
        """
        return Const.fromScipy( 'vacuum mag. permeability' )

    @classutilities.classproperty
    def epsilon_0( cls ):
        """!
        @brief Vacuum electric permittivity
        """
        return Const.fromScipy( 'vacuum electric permittivity' )
