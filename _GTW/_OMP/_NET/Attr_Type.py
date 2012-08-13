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
#    ««revision-date»»···
#--

from   __future__  import absolute_import, division, unicode_literals

from   _MOM.import_MOM       import *
from   _MOM.import_MOM       import _A_Composite_

from   _GTW                  import GTW

from   _TFL.I18N             import _
from   _TFL.Regexp           import Regexp, re

import _GTW._OMP._NET

def _inverted_mask_ (adrlen, mask) :
    return (2 ** (adrlen - mask)) - 1
# end def _inverted_mask_

def _masklen_ (adrlen, adr) :
    masklen = adrlen
    adr = adr.split ('/', 1)
    if len (adr) > 1 :
        masklen = int (adr [-1], 10)
    return masklen
# end def _masklen_

def _numeric_ip4_address_ (adr) :
    val = 0
    for a in adr.split ('.') :
        val <<= 8
        val |=  int (a, 10)
    return val
# end def _numeric_ip4_address_

def _numeric_ip6_address_ (adr) :
    """ Compute numeric ipv6 address from adr without netmask.
        We assume the address is well-formed.
        >>> n = _numeric_ip6_address_
        >>> print "%X" % n ("::")
        0
        >>> print "%X" % n ("::1")
        1
        >>> print "%X" % n ("2001:0db8:85a3:0000:0000:8a2e:0370:7334")
        20010DB885A3000000008A2E03707334
        >>> print "%X" % n ("2001:db8:85a3:0:0:8a2e:370:7334")
        20010DB885A3000000008A2E03707334
        >>> print "%X" % n ("2001:db8:85a3::8a2e:370:7334")
        20010DB885A3000000008A2E03707334
        >>> print "%X" % n ("2001:db8:85a3::")
        20010DB885A300000000000000000000
        >>> print "%X" % n ("::8a2e:370:7334")
        8A2E03707334
    """
    lower = ''
    upper = adr.split ('::', 1)
    if len (upper) > 1 :
        upper, lower = upper
    else :
        upper = upper [0]

    value = 0L
    shift = 128 - 16

    if upper :
        for v in upper.split (':') :
            assert (v)
            v = long (v, 16)
            value |= v << shift
            shift -= 16
    if lower :
        lv = 0L
        for v in lower.split (':') :
            assert (v)
            v = long (v, 16)
            lv <<= 16
            lv |=  v
        value |= lv
    return value
# end def _numeric_ip6_address_

class _A_IP_Address_ (Syntax_Re_Mixin, A_String) :
    """Model abstract address of IP network."""

    def check_syntax (self, obj, val) :
        self.__super.check_syntax (obj, val)
        if val :
            v = val.split ('/')
            mask = ''
            if len (v) > 1 :
                mask = v [-1]
                self.check_netmask (obj, mask)
            self.check_address (obj, v [0], mask)
    # end def check_syntax

    def check_netmask (self, obj, val) :
        if int (val) > self._bits :
            raise MOM.Error.Attribute_Syntax (obj, self, val)
    # end def check_netmask

    _syntax_re = Regexp (r"^[0-9a-fA-F.:/]+$")

# end class _A_IP_Address_

class _A_IP4_Address_ (_A_IP_Address_) :
    """Models an address in a IP4 network."""
    ### MGL: Use inet type for the _A_IP4_Address_

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

    def check_address (self, obj, val, mask) :
        if val :
            for octet in val.split ('.') :
                if int (octet) > 255 :
                    raise MOM.Error.Attribute_Syntax (obj, self, val)
    # end def check_address

# end class _A_IP4_Address_

class _A_IP4_Network_ (_A_IP4_Address_) :
    """Model a IP4 network in CIDRR notation."""
    ### MGL: Use cidr type for the _A_IP4_Network_

    _adr_type         = _A_IP4_Address_
    _mask_len         = len (str (_adr_type._bits - 1))
    example           = "192.168.42.0/28"
    typ               = "IP4-network"
    max_length        = _adr_type.max_length + _mask_len + 1
    P_Type            = str
    syntax            = _ \
        ( u"IP4 network must contain 4 decimal octets separated by `.`, "
          "optionally followed by `/` and a number between 0 and 32."
          " The bits right of the netmask must be zero."
        )
    _syntax_re        = Regexp \
        ( "^"
        + _adr_type._pattern
        + r"(?: / \d{1,%s})?" % _mask_len
        + "$"
        , re.VERBOSE
        )

    def check_address (self, obj, val, mask) :
        self.__super.check_address (obj, val, mask)
        # mask check (bits not included in mask must be 0)
        if val and mask :
            i = _numeric_ip4_address_ (val)
            m = _inverted_mask_ (32, int (mask, 10))
            r = i & m
            if r :
                v = '/'.join ((val, mask))
                raise MOM.Error.Attribute_Syntax (obj, self, v)
    # end def check_address

# end class _A_IP4_Network_

class _A_IP6_Address_ (_A_IP_Address_) :
    """Models an address in a IP6 network."""
    ### MGL: Use inet type for the _A_IP6_Address_

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

    def check_address (self, obj, val, mask) :
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

# end class _A_IP6_Address_

class _A_IP6_Network_ (_A_IP6_Address_) :
    """Model a IP6 network in CIDRR notation."""
    ### MGL: Use cidr type for the _A_IP6_Network_

    _adr_type         = _A_IP6_Address_
    _mask_len         = len (str (_adr_type._bits - 1))
    example           = "2001:db8::/32"
    typ               = "IP6-network"
    max_length        = _adr_type.max_length + _mask_len + 1
    P_Type            = str
    syntax            = _ \
        ( u"IP6 network must contain up to 8 hexadecimal "
          u"numbers with up to 4 digits separated by `:`. "
          u"A single empty group `::` can be used."
          u" This is optionally followed by `/` and a number between 0 and 128."
          u" The bits right of the netmask must be zero."
        )
    _syntax_re        = Regexp \
        ( "^"
        + _adr_type._pattern
        + r"(?: / \d{1,%s})?" % _mask_len
        + "$"
        , re.VERBOSE
        )

    def check_address (self, obj, val, mask) :
        self.__super.check_address (obj, val, mask)
        # mask check (bits not included in mask must be 0)
        if val and mask :
            i = _numeric_ip6_address_ (val)
            m = _inverted_mask_ (128, int (mask, 10))
            r = i & m
            if r :
                v = '/'.join ((val, mask))
                raise MOM.Error.Attribute_Syntax (obj, self, v)
    # end def check_address

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

# end class IP4_Address

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
                a = _numeric_ip4_address_ (obj.address.split ('/', 1) [0])
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
                return _masklen_ (self.max_value, obj.address)
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
                i = obj.address.split ('/', 1)
                if len (i) > 1 :
                    i, m = i
                else :
                    i = i [0]
                    m = None
                a = _numeric_ip4_address_ (i)
                if m :
                    a += _inverted_mask_ (32, long (m, 10))
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
                adr = _numeric_ip6_address_ (obj.address.split ('/') [0])
                return (adr & 0xFFFFFFFFFFFFFFFF) - 0x8000000000000000
            # end def computed

        # end class numeric_address_high

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
                adr = _numeric_ip6_address_ (obj.address.split ('/') [0])
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
                return _masklen_ (self.max_value, obj.address)
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
                i = obj.address.split ('/', 1)
                if len (i) > 1 :
                    i, m = i
                else :
                    i = i [0]
                    m = None
                a = _numeric_ip6_address_ (i)
                if m :
                    a += _inverted_mask_ (128, long (m, 10))
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
                i = obj.address.split ('/', 1)
                if len (i) > 1 :
                    i, m = i
                else :
                    i = i [0]
                    m = None
                a = _numeric_ip6_address_ (i)
                if m :
                    a += _inverted_mask_ (128, long (m, 10))
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

class _SAS_IP4_Address_Query_Mixin_ (TFL.Meta.Object) :
    """Special quey code for IP4 address objects"""

    _Handled_Compare_Operations = set (("eq", "ne"))

    @TFL.Meta.Once_Property
    def _QUERY_ATTRIBUTES (self) :
        return ("numeric_address", )
    # end def _QUERY_ATTRIBUTES

    def in_ (self, rhs) :
        from    sqlalchemy              import sql
        return sql.func.IP4_Address_IN ()
    # end def in_

# end class _SAS_IP4_Address_Query_Mixin_

def _add_query_mixins (module) :
    A2C = TFL.Add_To_Class
    A2C ("SAS_Query_Mixin", A_IP4_Address) (_SAS_IP4_Address_Query_Mixin_)
# end def _add_query_mixins

GTW.OMP.NET._Add_Import_Callback ("_MOM._DBW._SAS.Query", _add_query_mixins)

__all__ = tuple \
    (  k for (k, v) in globals ().iteritems ()
    if isinstance (v, MOM.Meta.M_Attr_Type)
    )

if __name__ != "__main__" :
    GTW.OMP.NET._Export ("*")
### __END__ GTW.OMP.NET.Attr_Type
