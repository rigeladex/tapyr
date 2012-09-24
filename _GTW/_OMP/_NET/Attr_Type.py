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
#    23-May-2012 (RS) Rename `A_IP_Address` -> `_A_IP_Address_`
#    23-May-2012 (RS) Add `_syntax_re` for `_A_IP_Address_`
#    10-Aug-2012 (RS) make all IP-related types decendants of `_A_Composite_`
#    11-Aug-2012 (MG) Preparation for special SAS query functions
#    13-Aug-2012 (RS) Add `mask_len` to `IP4_Network` and `IP6_Network`,
#                     create common ancestor of all composite ip types
#    23-Sep-2012 (RS) `_A_IP_Address_` and descendants use `rsclib.IP_Address`
#    24-Sep-2012 (RS) fix/add mixins for SAS backend
#    ««revision-date»»···
#--

from   __future__  import absolute_import, division, unicode_literals

from   _MOM.import_MOM       import *
from   _MOM.import_MOM       import _A_Composite_, _A_String_

from   _GTW                  import GTW

from   _TFL.I18N             import _
from   _TFL.Regexp           import Regexp, re

from   rsclib.IP_Address     import IP_Address  as R_IP_Address
from   rsclib.IP_Address     import IP4_Address as R_IP4_Address
from   rsclib.IP_Address     import IP6_Address as R_IP6_Address

import _GTW._OMP._NET

class _A_IP_Address_ (A_Attr_Type) :
    """Model abstract address of IP network."""

    P_Type = R_IP_Address

    class Pickler (TFL.Meta.Object) :

        @classmethod
        def as_cargo (cls, attr_kind, attr_type, value) :
            if value is not None :
                return str (value)
        # end def as_cargo

        @classmethod
        def from_cargo (cls, scope, attr_kind, attr_type, cargo) :
            if cargo is not None :
                return attr_type.P_Type (cargo)
        # end def from_cargo

    # end class Pickler

    @TFL.Meta.Class_and_Instance_Method
    def _from_string (soc, value, obj, glob, locl) :
        if value :
            try :
                return soc.P_Type (value)
            except ValueError, err :
                raise # MOM.Error.Attribute_Syntax (obj, soc, value)
    # end def _from_string

    @TFL.Meta.Class_and_Instance_Method
    def cooked (soc, value) :
        if not isinstance (value, R_IP_Address) :
            raise TypeError, "Invalid type for cooked -- forgot `raw = True`?"
        return value
    # end def cooked

# end class _A_IP_Address_

class _A_IP4_Address_ (_A_IP_Address_) :
    """Models an address in a IP4 network."""
    ### MGL: Use inet type for the _A_IP4_Address_

    P_Type            = R_IP4_Address
    example           = "192.168.42.137"
    typ               = "IP4-address"
    max_length        = 15
    syntax            = _ \
        ( u"IP4 address must contain 4 decimal octets separated by `.`."
        )

    def check_syntax (self, obj, val) :
        if val and val.mask != self.P_Type.bitlen :
            raise ValueError, "Invalid netmask"
            raise MOM.Error.Attribute_Syntax (obj, self, val)
    # end def check_syntax

# end class _A_IP4_Address_

class _A_IP4_Network_ (_A_IP_Address_) :
    """Model a IP4 network in CIDRR notation."""
    ### MGL: Use cidr type for the _A_IP4_Network_

    P_Type            = R_IP4_Address
    _adr_type         = _A_IP4_Address_
    _mask_len         = len (str (P_Type.bitlen))
    example           = "192.168.42.0/28"
    typ               = "IP4-network"
    max_length        = _adr_type.max_length + _mask_len + 1
    syntax            = _ \
        ( u"IP4 network must contain 4 decimal octets separated by `.`, "
          "optionally followed by `/` and a number between 0 and 32."
          " The bits right of the netmask are automatically set to zero."
        )

# end class _A_IP4_Network_

class _A_IP6_Address_ (_A_IP4_Address_) :
    """Models an address in a IP6 network."""
    ### MGL: Use inet type for the _A_IP6_Address_

    P_Type            = R_IP6_Address
    example           = "2001:db8:85a3::8a2e:370:7334"
    typ               = "IP6-address"
    max_length        = 39
    syntax            = _ \
        ( u"IP6 address must contain up to 8 hexadecimal "
          u"numbers with up to 4 digits separated by `:`. "
          u"A single empty group `::` can be used."
        )

# end class _A_IP6_Address_

class _A_IP6_Network_ (_A_IP_Address_) :
    """Model a IP6 network in CIDRR notation."""
    ### MGL: Use cidr type for the _A_IP6_Network_

    P_Type            = R_IP6_Address
    _adr_type         = _A_IP6_Address_
    _mask_len         = len (str (P_Type.bitlen))
    example           = "2001:db8::/32"
    typ               = "IP6-network"
    max_length        = _adr_type.max_length + _mask_len + 1
    syntax            = _ \
        ( u"IP6 network must contain up to 8 hexadecimal "
          u"numbers with up to 4 digits separated by `:`. "
          u"A single empty group `::` can be used."
          u" This is optionally followed by `/` and a number between 0 and 128."
          u" The bits right of the netmask are automatically set to zero."
        )

# end class _A_IP6_Network_


_Ancestor_Essence = MOM.An_Entity

class IP_Address (_Ancestor_Essence) :
    """Model an abstract IP Address."""

    class _Attributes (_Ancestor_Essence._Attributes) :

        _Ancestor = _Ancestor_Essence._Attributes

        class address (_A_IP_Address_) :
            """IP Address"""

            kind = Attr.Necessary

        # end class address

    # end class _Attributes

    def __cmp__ (self, rhs) :
        return cmp (self.address, rhs.address)
    # end def cmp

    def __contains__ (self, rhs) :
        return rhs.address in self.address
    # end def __contains__
    
# end class IP_Address

_Ancestor_Essence = IP_Address

class IP4_Address (_Ancestor_Essence) :
    """Model an IPv4 Address (without netmask)."""

    class _Attributes (_Ancestor_Essence._Attributes) :

        _Ancestor = _Ancestor_Essence._Attributes

        class address (_A_IP4_Address_) :
            """IPv4 Address"""

            kind = Attr.Necessary

        # end class address

        class numeric_address (A_Int) :
            """ Numeric IP address. """

            kind            = Attr.Internal
            auto_up_depends = ("address", )
            min_value       = -0x80000000
            max_value       =  0x7FFFFFFF

            def computed (self, obj) :
                """ We must fit the 32 bit IP address into the signed
                    integer range supported by databases. To correctly
                    support comparison (later needed for checking if an
                    address is contained within a network) we subtract
                    0x80000000 -- so we don't use the usual 2-complement
                    here!
                """
                a = obj.address.ip
                return a - 0x80000000
            # end def computed

        # end class numeric_address

    # end class _Attributes

# end class IP4_Address

_Ancestor_Essence = IP4_Address

class IP4_Network (_Ancestor_Essence) :
    """Model an IPv4 Network with netmask."""

    class _Attributes (_Ancestor_Essence._Attributes) :

        _Ancestor = _Ancestor_Essence._Attributes

        class address (_A_IP4_Network_) :
            """IPv4 Network"""

            kind = Attr.Necessary

        # end class address

        class mask_len (A_Int) :
            """ Length of network mask. """

            kind            = Attr.Internal
            auto_up_depends = ("address", )
            min_value       = 0
            max_value       = 32

            def computed (self, obj) :
                return obj.address.mask
            # end def computed

        # end class mask_len

        class upper_bound (A_Int) :
            """ Numeric IP address of upper bound of network range. """

            kind            = Attr.Internal
            auto_up_depends = ("address", )
            min_value       = -0x80000000
            max_value       =  0x7FFFFFFF

            def computed (self, obj) :
                """ We must fit the 32 bit IP address into the signed
                    integer range supported by databases. To correctly
                    support comparison (later needed for checking if an
                    address is contained within a network) we subtract
                    0x80000000 -- so we don't use the usual 2-complement
                    here!
                """
                a = obj.address._broadcast
                return a - 0x80000000
            # end def computed

        # end class upper_bound

    # end class _Attributes

# end class IP4_Network

_Ancestor_Essence = IP_Address

class IP6_Address (_Ancestor_Essence) :
    """Model an IPv6 Address (without netmask)."""

    class _Attributes (_Ancestor_Essence._Attributes) :

        _Ancestor = _Ancestor_Essence._Attributes

        class address (_A_IP6_Address_) :
            """IPv6 Address"""

            kind = Attr.Necessary

        # end class address

        class numeric_address_low (A_Int) :
            """ Numeric IP address -- low 64 bit.
                We must fit the 64 bit part into the signed integer
                range supported by databases. To correctly support
                comparison (later needed for checking if an address is
                contained within a network) we subtract the minimum
                bigint -- so we don't use the usual 2-complement here!
            """

            kind            = Attr.Internal
            auto_up_depends = ("address", )
            min_value       = 0x8000000000000000
            max_value       = 0x7FFFFFFFFFFFFFFF

            def computed (self, obj) :
                adr = obj.address.ip
                return (adr & 0xFFFFFFFFFFFFFFFF) - 0x8000000000000000
            # end def computed

        # end class numeric_address_low

        class numeric_address_high (A_Int) :
            """ Numeric IP address -- high 64 bit.
                We must fit the 64 bit part into the signed integer
                range supported by databases. To correctly support
                comparison (later needed for checking if an address is
                contained within a network) we subtract the minimum
                bigint -- so we don't use the usual 2-complement here!
            """

            kind            = Attr.Internal
            auto_up_depends = ("address", )
            min_value       = 0x8000000000000000
            max_value       = 0x7FFFFFFFFFFFFFFF

            def computed (self, obj) :
                adr = obj.address.ip
                return (adr >> 64) - 0x8000000000000000
            # end def computed

        # end class numeric_address_high

    # end class _Attributes

# end class IP6_Address

_Ancestor_Essence = IP6_Address

class IP6_Network (_Ancestor_Essence) :
    """Model an IPv6 Network with netmask."""

    class _Attributes (_Ancestor_Essence._Attributes) :

        _Ancestor = _Ancestor_Essence._Attributes

        class address (_A_IP6_Network_) :
            """IPv6 Network"""

            kind = Attr.Necessary

        # end class address

        class mask_len (A_Int) :
            """ Length of network mask. """

            kind            = Attr.Internal
            auto_up_depends = ("address", )
            min_value       = 0
            max_value       = 128

            def computed (self, obj) :
                return obj.address.mask
            # end def computed

        # end class mask_len

        class upper_bound_low (A_Int) :
            """ Numeric IP address of upper bound of network range low 64 bit.
                We must fit the 64 bit part into the signed integer
                range supported by databases. To correctly support
                comparison (later needed for checking if an address is
                contained within a network) we subtract the minimum
                bigint -- so we don't use the usual 2-complement here!
            """

            kind            = Attr.Internal
            auto_up_depends = ("address", )
            min_value       = 0x8000000000000000
            max_value       = 0x7FFFFFFFFFFFFFFF

            def computed (self, obj) :
                a = obj.address._broadcast
                return (a & 0xFFFFFFFFFFFFFFFF) - 0x8000000000000000
            # end def computed

        # end class numeric_address_high

        class upper_bound_high (A_Int) :
            """ Numeric IP address of upper bound of network range high 64 bit.
                We must fit the 64 bit part into the signed integer
                range supported by databases. To correctly support
                comparison (later needed for checking if an address is
                contained within a network) we subtract the minimum
                bigint -- so we don't use the usual 2-complement here!
            """

            kind            = Attr.Internal
            auto_up_depends = ("address", )
            min_value       = 0x8000000000000000
            max_value       = 0x7FFFFFFFFFFFFFFF

            def computed (self, obj) :
                a = obj.address._broadcast
                return (a >> 64) - 0x8000000000000000
            # end def computed

        # end class numeric_address_high

    # end class _Attributes

# end class IP6_Network

class _A_Composite_IP_Address_ (_A_Composite_) :

    P_Type = IP_Address
    typ    = "IP_Address"

# end class _A_Composite_IP_Address_

class A_IP4_Address (_A_Composite_IP_Address_) :
    """IPv4 Address (without netmask)."""

    P_Type = IP4_Address
    typ    = "IP4_Address"

# end class A_IP4_Address

class A_IP4_Network (_A_Composite_IP_Address_) :
    """IPv4 Address with netmask."""

    P_Type = IP4_Network
    typ    = "IP4_Network"

# end class A_IP4_Network

class A_IP6_Address (_A_Composite_IP_Address_) :
    """IPv6 Address (without netmask)."""

    P_Type = IP6_Address
    typ    = "IP6_Address"

# end class A_IP6_Address

class A_IP6_Network (_A_Composite_IP_Address_) :
    """IPv6 Address with netmask."""

    P_Type = IP6_Network
    typ    = "IP6_Network"

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

class _SAS_IP_Address_Query_Mixin_ (TFL.Meta.Object) :

    def __ne__ (self, rhs) :
        from    sqlalchemy              import sql
        return sql.not_ (self.__eq__ (rhs))
    # end def __ne__

# end class _SAS_IP_Address_Query_Mixin_

class _Net_Cmp_Mixin_ (TFL.Meta.Object) :

    def in_ (self, rhs) :
        from    sqlalchemy              import sql
        return sql.and_ \
            ( self.__super.in_ (rhs)
            , rhs.mask_len <= self.mask_len
            )
    # end def in_

    def __eq__ (self, rhs) :
        from    sqlalchemy              import sql
        return sql.and_ \
            ( self.__super.__eq__ (rhs)
            , self.mask_len == rhs.mask_len
            )
    # end def __eq__

    def __ge__ (self, rhs) :
        from    sqlalchemy              import sql
        return sql.or_ \
            ( self.__super.__gt__ (rhs) # yes, really __gt__
            , sql.and_
                ( self.mask_len <= rhs.mask_len
                , self.adr_eq (rhs)
                )
            )
    # end def __ge__

    def __gt__ (self, rhs) :
        from    sqlalchemy              import sql
        return sql.or_ \
            ( self.__super.__gt__ (rhs)
            , sql.and_
                ( self.mask_len < rhs.mask_len
                , self.adr_eq (rhs)
                )
            )
    # end def __gt__

    def __le__ (self, rhs) :
        from    sqlalchemy              import sql
        return sql.or_ \
            ( self.__super.__lt__ (rhs) # yes, really __lt__
            , sql.and_
                ( self.mask_len >= rhs.mask_len
                , self.adr_eq (rhs)
                )
            )
    # end def __le__

    def __lt__ (self, rhs) :
        from    sqlalchemy              import sql
        return sql.or_ \
            ( self.__super.__lt__ (rhs)
            , sql.and_
                ( self.mask_len > rhs.mask_len
                , self.adr_eq (rhs)
                )
            )
    # end def __lt__

# end class _Net_Cmp_Mixin_

class _SAS_IP4_Address_Query_Mixin_ (_SAS_IP_Address_Query_Mixin_) :
    """Special query code for IP4 address objects"""

    def in_ (self, rhs) :
        from    sqlalchemy              import sql
        return sql.and_ \
            ( rhs .numeric_address <= self.numeric_address
            , self.numeric_address <= rhs .upper_bound
            )
    # end def in_

    # explicit definition of comparisons, otherwise inheritance (and
    # consequently the _Net_Cmp_Mixin_) won't work.

    def __eq__ (self, rhs) :
        from    sqlalchemy              import sql
        return sql.and_ (self.numeric_address == rhs.numeric_address)
    # end def __eq__
    adr_eq = __eq__ # this is used in network comparison

    def __ge__ (self, rhs) :
        from    sqlalchemy              import sql
        return sql.and_ (self.numeric_address >= rhs.numeric_address)
    # end def __ge__

    def __gt__ (self, rhs) :
        from    sqlalchemy              import sql
        return sql.and_ (self.numeric_address >  rhs.numeric_address)
    # end def __ge__

    def __le__ (self, rhs) :
        from    sqlalchemy              import sql
        return sql.and_ (self.numeric_address <= rhs.numeric_address)
    # end def __ge__

    def __lt__ (self, rhs) :
        from    sqlalchemy              import sql
        return sql.and_ (self.numeric_address <  rhs.numeric_address)
    # end def __ge__

# end class _SAS_IP4_Address_Query_Mixin_

class _SAS_IP4_Network_Query_Mixin_ (_Net_Cmp_Mixin_, _SAS_IP4_Address_Query_Mixin_) :
    pass
# end class _SAS_IP4_Network_Query_Mixin_

class _SAS_IP6_Address_Query_Mixin_ (_SAS_IP_Address_Query_Mixin_) :
    """Special query code for IP6 address objects"""

    def in_ (self, rhs) :
        from    sqlalchemy              import sql
        return sql.or_ \
            ( sql.and_
                ( rhs .numeric_address_high <  self.numeric_address_high
                , self.numeric_address_high <  rhs .upper_bound_high
                )
            , sql.and_
                ( rhs .numeric_address_high == self.numeric_address_high
                , rhs .numeric_address_low  <= self.numeric_address_low
                , self.numeric_address_low  <= rhs .upper_bound_low
                )
            , sql.and_
                ( self.numeric_address_high == rhs .upper_bound_high
                , rhs .numeric_address_low  <= self.numeric_address_low
                , self.numeric_address_low  <= rhs .upper_bound_low
                )
            )
    # end def in_

    def __eq__ (self, rhs) :
        from    sqlalchemy              import sql
        return sql.and_ \
            ( self.numeric_address_high == rhs.numeric_address_high
            , self.numeric_address_low  == rhs.numeric_address_low
            )
    # end def __eq__
    adr_eq = __eq__ # this is used in network comparison

    def __ge__ (self, rhs) :
        from    sqlalchemy              import sql
        return sql.or_ \
            ( self.numeric_address_high > rhs.numeric_address_high
            , sql.and_
                ( self.numeric_address_high == rhs.numeric_address_high
                , self.numeric_address_low  >= rhs.numeric_address_low
                )
            )
    # end def __ge__

    def __gt__ (self, rhs) :
        from    sqlalchemy              import sql
        return sql.or_ \
            ( self.numeric_address_high > rhs.numeric_address_high
            , sql.and_
                ( self.numeric_address_high == rhs.numeric_address_high
                , self.numeric_address_low  >  rhs.numeric_address_low
                )
            )
    # end def __gt__

    def __le__ (self, rhs) :
        from    sqlalchemy              import sql
        return sql.or_ \
            ( self.numeric_address_high < rhs.numeric_address_high
            , sql.and_
                ( self.numeric_address_high == rhs.numeric_address_high
                , self.numeric_address_low  <= rhs.numeric_address_low
                )
            )
    # end def __le__

    def __lt__ (self, rhs) :
        from    sqlalchemy              import sql
        return sql.or_ \
            ( self.numeric_address_high < rhs.numeric_address_high
            , sql.and_
                ( self.numeric_address_high == rhs.numeric_address_high
                , self.numeric_address_low  <  rhs.numeric_address_low
                )
            )
    # end def __lt__

# end class _SAS_IP6_Address_Query_Mixin_

class _SAS_IP6_Network_Query_Mixin_ (_Net_Cmp_Mixin_, _SAS_IP6_Address_Query_Mixin_) :
    pass
# end class _SAS_IP6_Network_Query_Mixin_


def _add_query_mixins (module) :
    A2C = TFL.Add_To_Class
    A2C ("SAS_Query_Mixin", A_IP4_Address) (_SAS_IP4_Address_Query_Mixin_)
    A2C ("SAS_Query_Mixin", A_IP4_Network) (_SAS_IP4_Network_Query_Mixin_)
    A2C ("SAS_Query_Mixin", A_IP6_Address) (_SAS_IP6_Address_Query_Mixin_)
    A2C ("SAS_Query_Mixin", A_IP6_Network) (_SAS_IP6_Network_Query_Mixin_)
# end def _add_query_mixins

GTW.OMP.NET._Add_Import_Callback ("_MOM._DBW._SAS.Query", _add_query_mixins)

__all__ = tuple \
    (  k for (k, v) in globals ().iteritems ()
    if isinstance (v, MOM.Meta.M_Attr_Type)
    )

if __name__ != "__main__" :
    GTW.OMP.NET._Export ("*")
### __END__ GTW.OMP.NET.Attr_Type
