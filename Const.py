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
#                   |                |

import math
from PObjects import PObject

# Physical Constants:

class MetaConst( type ):
    """!
    @brief Metaclass for class Const implementing static class properties so
           class Const doesn't need to get instantiated to get to them.
    """
    @property
    def e_0( cls ):
        """!
        @brief elementary charge
        """
        return PObject( 1.6021766208e-19, "C" )

    @property
    def m_e( cls ):
        """!
        @brief electron mass
        """
        return PObject( 9.10938356e-31, "kg" )

    @property
    def amu( cls ):
        """!
        @brief atomic mass unit
        """
        return PObject( 1.6605388628e-27, "kg" )

    @property
    def m_p( cls ):
        """!
        @brief proton mass
        """
        return 1.0072764668 * Const.amu

    @property
    def m_n( cls ):
        """!
        @brief neutron mass
        """
        return 1.0086649156 * Const.amu

    @property
    def c_0( cls ):
        """!
        @brief speed of light in vacuum
        """
        return PObject( 299792458.0, "m / s" )


    @property
    def h( cls ):
        """!
        @brief Planck's constant
        """
        return PObject( 6.626070040e-34, "kg m**2 / s" )

    @property
    def hbar( cls ):
        """!
        @brief Planck's constant divided by 2 pi
        """
        return Const.h / (2. * math.pi)

    @property
    def N_A( cls ):
        """!
        @brief Avogadro's number
        """
        return PObject( 6.02214076e23, "1 / mol" )

    @property
    def R( cls ):
        """!
        @brief general gas constant
        """
        return PObject( 8.3144598, "kg m**2 / (s**2 K mol)" )

    @property
    def k_B( cls ):
        """!
        @brief Boltzmann constant
        """
        return Const.R / Const.N_A

    @property
    def G( cls ):
        """!
        @brief gravitational constant
        """
        return PObject( 6.6408e-11, "m**3 / (kg s**2)" )

    @property
    def g( cls ):
        """!
        @brief acceleration at equator and sea level due to gravity
               this is not really a "constant" but often needed anyway
        """
        return PObject( 9.80665, "m / s**2" )

    @property
    def mu_0( cls ):
        """!
        @brief Vacuum permeability
        """
        return PObject( math.pi * 4.0e-07, "kg m / (s**2 A**2)" )

    @property
    def epsilon_0( cls ):
        """!
        @brief Vacuum permitivity
        """
        return PObject( 8.854187817e-12, "s**4 A**2 / (m**3 kg)" )


class Const( metaclass=MetaConst ):
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

    The constants currently supported are ("g" isn't really a constant
    but used often):
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
    - epsilon   vacuum permitivity

    All physical constants are returned as PObjects with proper units, i.e. they
    can be subjected to any arithmetic operation with themselves and other
    PObjects and yield correct results (including units) and the statement
    @code
    print( Const.hbar )
    @endcode
    will produce the string "1.05457e-34 m**2 kg / s".
    """
    # pylint: disable=unnecessary-pass
    pass

