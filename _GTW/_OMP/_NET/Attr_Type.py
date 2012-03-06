# -*- coding: iso-8859-15 -*-
# Copyright (C) 2012 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# #*** <License> ************************************************************#
# This module is part of the package GTW.OMP.NET.
#
# This module is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This module is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this module. If not, see <http://www.gnu.org/licenses/>.
# #*** </License> ***********************************************************#
#
#++
# Name
#    GTW.OMP.NET.Attr_Type
#
# Purpose
#    Define attribute types for package GTW.OMP.NET
#
# Revision Dates
#     6-Mar-2012 (CT) Creation
#    ««revision-date»»···
#--

from   __future__  import absolute_import, division, print_function, unicode_literals

from   _MOM.import_MOM       import *
from   _MOM.import_MOM       import _A_Composite_

from   _GTW                  import GTW

from   _TFL.I18N             import _
from   _TFL.Regexp           import Regexp, re

import _GTW._OMP._NET

class A_IP4_Address (Syntax_Re_Mixin, A_String) :
    """Models an address in a IP4 network."""

    example           = "192.168.42.137"
    typ               = "IP4-address"
    max_length        = 15
    P_Type            = str
    syntax            = _ \
        ( u"A IP4 address must contain 4 decimal octets separated by `.`."
        )

    _ip4_pat          = "(?: \d{1,3}\.){3} \d{1,3}"
    _syntax_re        = Regexp \
        ( r"^" + _ip4_pat + "$"
        , re.VERBOSE
        )

# end class A_IP4_Address

class A_IP4_Network (Syntax_Re_Mixin, A_String) :
    """Model a IP4 network in CIDRR notation."""

    example           = "192.168.42.0/28"
    typ               = "IP4-network"
    max_length        = 18
    P_Type            = str
    syntax            = _ \
        ( u"A IP4 network must contain 4 decimal octets separated by `.`, "
          "optionally followed by `/` and a number between 0 and 32."
        )

    _syntax_re        = Regexp \
        ( "^"
        + A_IP4_Address._ip4_pat
        + r"(?: / \d{1,2})?"
        + "$"
        , re.VERBOSE
        )

# end class A_IP4_Network

class A_MAC_Address (Syntax_Re_Mixin, A_String) :
    """Model a MAC address."""

    example           = "00:18:71:69:0b:c8"
    typ               = "MAC-address"
    max_length        = 17
    P_Type            = str
    syntax            = _ \
        ( "A MAC address must contain 6 hexadecimal octets separated by `:`."
        )

    _syntax_re        = Regexp \
        ( r"^"
          r"(?: [0-9A-F]{2} :){5} [0-9A-F]{2}"
        , r"$"
        , re.VERBOSE | re.IGNORECASE
        )

# end class A_MAC_Address

__all__ = tuple \
    (  k for (k, v) in globals ().iteritems ()
    if isinstance (v, MOM.Meta.M_Attr_Type)
    )

if __name__ != "__main__" :
    GTW.OMP.NET._Export ("*")
### __END__ GTW.OMP.NET.Attr_Type
