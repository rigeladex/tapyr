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
#    22-May-2012 (RS) Add `A_IP6_Address`, `A_IP6_Network` and common
#                     ancestor `A_IP_Address`, extend syntax checks
#    23-May-2012 (RS) Rename `A_IP6_Address` -> `_A_IP_Address_`
#    ««revision-date»»···
#--

from   __future__  import absolute_import, division, unicode_literals

from   _MOM.import_MOM       import *
from   _MOM.import_MOM       import _A_Composite_

from   _GTW                  import GTW

from   _TFL.I18N             import _
from   _TFL.Regexp           import Regexp, re

import _GTW._OMP._NET

class _A_IP_Address_ (Syntax_Re_Mixin, A_String) :
    """Model abstract address of IP network."""

    def check_syntax (self, obj, val) :
        self.__super.check_syntax (obj, val)
        if val :
            v = val.split ('/')
            self.check_address (obj, v [0])
            if len (v) > 1 :
                self.check_netmask (obj, v [-1])
    # end def check_syntax

    def check_netmask (self, obj, val) :
        if int (val) > self._bits :
            raise MOM.Error.Attribute_Syntax (obj, self, val)
    # end def check_netmask

# end class _A_IP_Address_

class A_IP4_Address (_A_IP_Address_) :
    """Models an address in a IP4 network."""

    _bits             = 32
    example           = "192.168.42.137"
    typ               = "IP4-address"
    max_length        = 15
    P_Type            = str
    syntax            = _ \
        ( u"IP4 address must contain 4 decimal octets separated by `.`."
        )

    _pattern          = "(?: \d{1,3}\.){3} \d{1,3}"
    _syntax_re        = Regexp \
        ( r"^" + _pattern + "$"
        , re.VERBOSE
        )

    def check_address (self, obj, val) :
        if val :
            for octet in val.split ('.') :
                if int (octet) > 255 :
                    raise MOM.Error.Attribute_Syntax (obj, self, val)
    # end def check_address

# end class A_IP4_Address

class A_IP4_Network (A_IP4_Address) :
    """Model a IP4 network in CIDRR notation."""

    _adr_type         = A_IP4_Address
    _mask_len         = len (str (_adr_type._bits - 1))
    example           = "192.168.42.0/28"
    typ               = "IP4-network"
    max_length        = _adr_type.max_length + _mask_len + 1
    P_Type            = str
    syntax            = _ \
        ( u"IP4 network must contain 4 decimal octets separated by `.`, "
          "optionally followed by `/` and a number between 0 and 32."
        )
    _syntax_re        = Regexp \
        ( "^"
        + _adr_type._pattern
        + r"(?: / \d{1,%s})?" % _mask_len
        + "$"
        , re.VERBOSE
        )

# end class A_IP4_Network

class A_IP6_Address (_A_IP_Address_) :
    """Models an address in a IP6 network."""

    _bits             = 128
    example           = "2001:db8:85a3::8a2e:370:7334"
    typ               = "IP6-address"
    max_length        = 39
    P_Type            = str
    syntax            = _ \
        ( u"IP6 address must contain up to 8 hexadecimal "
          u"numbers with up to 4 digits separated by `:`. "
          u"A single empty group `::` can be used."
        )

    _pattern          = "(?: [0-9A-Fa-f]{0,4} :){2,7} [0-9A-Fa-f]{0,4}"
    _syntax_re        = Regexp \
        ( r"^" + _pattern + "$"
        , re.VERBOSE
        )

    def check_address (self, obj, val) :
        """ First check regular expression, then do some more checks on
            the IPv6 Address -- doing it all with a regex will produce
            an unmaintainable regex, see for example
            https://rt.cpan.org/Public/Bug/Display.html?id=50693
            Many Test-cases stolen from link above.
            Note that we currently don't allow mixed ':' and '.' notation.
        """
        if val :
            empty_count = 0
            if val.startswith (':') :
                if not val.startswith ('::') :
                    raise MOM.Error.Attribute_Syntax (obj, self, val)
                if val != '::' and val.endswith (':') :
                    raise MOM.Error.Attribute_Syntax (obj, self, val)
                empty_count = 1
            elif val.endswith (':') :
                if not val.endswith ('::') :
                    raise MOM.Error.Attribute_Syntax (obj, self, val)
                empty_count = 1
            numbers = val.strip (':') or []
            if numbers :
                numbers = numbers.split (':')
            for v in numbers :
                if not v :
                    if empty_count :
                        raise MOM.Error.Attribute_Syntax (obj, self, val)
                    empty_count += 1
            if not empty_count and len (numbers) != 8 :
                raise MOM.Error.Attribute_Syntax (obj, self, val)
    # end def check_address

# end class A_IP6_Address

class A_IP6_Network (A_IP6_Address) :
    """Model a IP6 network in CIDRR notation."""

    _adr_type         = A_IP6_Address
    _mask_len         = len (str (_adr_type._bits - 1))
    example           = "2001:db8::/32"
    typ               = "IP6-network"
    max_length        = _adr_type.max_length + _mask_len + 1
    P_Type            = str
    syntax            = _ \
        ( _adr_type.syntax
        + u" This is optionally followed by `/` and a number between 0 and 128."
        )
    _syntax_re        = Regexp \
        ( "^"
        + _adr_type._pattern
        + r"(?: / \d{1,%s})?" % _mask_len
        + "$"
        , re.VERBOSE
        )
# end class A_IP6_Network

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
          r"$"
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
