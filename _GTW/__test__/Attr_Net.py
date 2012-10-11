# -*- coding: iso-8859-15 -*-
# Copyright (C) 2012 Dr. Ralf Schlatterbeck All rights reserved
# Reichergasse 131, A--3411 Weidling, Austria. rsc@runtux.com
# #*** <License> ************************************************************#
# This module is part of the package GTW.__test__.
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
#    GTW.__test__.Attr_Net
#
# Purpose
#    Test cases for GTW.OMP.Net.Attr_Type
#
# Revision Dates
#    22-May-2012 (RS) Creation
#    10-Aug-2012 (RS) IP addresses are now composite. Fix tests for new
#                     check of subnet mask (bits right of mask must be 0)
#    11-Aug-2012 (MG) New tests for query functions added
#    13-Aug-2012 (RS) Test `IP6_Network` with default mask_len 128
#    13-Sep-2012 (RS) Comment doctest for unimplemented feature
#    24-Sep-2012 (RS) Fix doctest for `in`, add relational operators
#                     fix error messages now coming from rsclib
#    24-Sep-2012 (CT) Adapt tests
#    10-Oct-2012 (CT) Rename test classes to `Test_...`
#    10-Oct-2012 (CT) Add test for `raw_query_attrs`
#    ««revision-date»»···
#--

from   __future__  import unicode_literals

from   _MOM.import_MOM          import *
from   _GTW._OMP._NET.Attr_Type import *
from   _TFL.Package_Namespace   import Derived_Package_Namespace

Namespace = Derived_Package_Namespace (parent = MOM, name = "_GTW._OMP._NET")

_Ancestor_Essence = MOM.Object

class Test_IP4_Address (_Ancestor_Essence) :

    PNS = Namespace

    class _Attributes (_Ancestor_Essence._Attributes) :

        class address (A_IP4_Address) :

            kind = Attr.Primary

        # end class address

    # end class _Attributes

# end class Test_IP4_Address

_Ancestor_Essence = MOM.Object

class Test_IP4_Network (_Ancestor_Essence) :

    PNS = Namespace

    class _Attributes (_Ancestor_Essence._Attributes) :

        class address (A_IP4_Network) :

            kind = Attr.Primary

        # end class address

    # end class _Attributes

# end class Test_IP4_Network

_Ancestor_Essence = MOM.Object

class Test_IP6_Address (_Ancestor_Essence) :

    PNS = Namespace

    class _Attributes (_Ancestor_Essence._Attributes) :

        class address (A_IP6_Address) :

            kind = Attr.Primary

        # end class address

    # end class _Attributes

# end class Test_IP6_Address

_Ancestor_Essence = MOM.Object

class Test_IP6_Network (_Ancestor_Essence) :

    PNS = Namespace

    class _Attributes (_Ancestor_Essence._Attributes) :

        class address (A_IP6_Network) :

            kind = Attr.Primary

        # end class address

    # end class _Attributes

# end class Test_IP6_Network

_Ancestor_Essence = MOM.Object

class MAC_Address (_Ancestor_Essence) :

    PNS = Namespace

    class _Attributes (_Ancestor_Essence._Attributes) :

        class address (A_MAC_Address) :

            kind = Attr.Primary

        # end class address

    # end class _Attributes

# end class MAC_Address

_test_code = """
    >>> scope = Scaffold.scope (%(p1)s, %(n1)s) # doctest:+ELLIPSIS
    Creating new scope MOMT__...
    >>> NET = scope.GTW.OMP.NET
    >>> Test_IP4_Address = NET.Test_IP4_Address
    >>> Test_IP4_Network = NET.Test_IP4_Network
    >>> Test_IP6_Address = NET.Test_IP6_Address
    >>> Test_IP6_Network = NET.Test_IP6_Network
    >>> MAC_Address = NET.MAC_Address
    >>> MAC_Address ("00:11:22:33:44:55")
    GTW.OMP.NET.MAC_Address (u'00:11:22:33:44:55')
    >>> MAC_Address ("000:11:22:33:44:55")
    Traceback (most recent call last):
     ...
    Invariants: Condition `AC_check_address_length` : Value for address must not be longer than 17 (length <= 17)
        address = '000:11:22:33:44:55'
        length = 18 << len (address)
      `Syntax error` for : `MAC-address `address``
         expected type  : `MAC-address`
         got      value : `000:11:22:33:44:55`
    A MAC address must contain 6 hexadecimal octets separated by `:`.
    >>> MAC_Address ("00:11:22:33:44")
    Traceback (most recent call last):
     ...
    Invariants: `Syntax error` for : `MAC-address `address``
         expected type  : `MAC-address`
         got      value : `00:11:22:33:44`
    A MAC address must contain 6 hexadecimal octets separated by `:`.
    >>> MAC_Address ("00:11:22:33:44:55:66")
    Traceback (most recent call last):
     ...
    Invariants: Condition `AC_check_address_length` : Value for address must not be longer than 17 (length <= 17)
        address = '00:11:22:33:44:55:66'
        length = 20 << len (address)
      `Syntax error` for : `MAC-address `address``
         expected type  : `MAC-address`
         got      value : `00:11:22:33:44:55:66`
    A MAC address must contain 6 hexadecimal octets separated by `:`.
    >>> Test_IP4_Address (dict (address = '1.2.3.4'), raw = True)
    GTW.OMP.NET.Test_IP4_Address (dict (address = 1.2.3.4))
    >>> Test_IP4_Address (dict (address = '111.222.233.244'), raw = True)
    GTW.OMP.NET.Test_IP4_Address (dict (address = 111.222.233.244))
    >>> Test_IP4_Address (dict (address = '111.222.233.244/22'), raw = True)
    Traceback (most recent call last):
     ...
    Attribute_Value: Can't set IP4-address `address` attribute IP4_Address.address to `111.222.232.0/22`
        Invalid netmask: 22; must be empty or 32
    >>> Test_IP4_Address (dict (address = '1.2.3.4/22'), raw = True)
    Traceback (most recent call last):
     ...
    Attribute_Value: Can't set IP4-address `address` attribute IP4_Address.address to `1.2.0.0/22`
        Invalid netmask: 22; must be empty or 32
    >>> Test_IP4_Address (dict (address = '256.255.255.2'), raw = True)
    Traceback (most recent call last):
     ...
    Attribute_Value: Can't set necessary attribute IP4_Address.address to `u'256.255.255.2'`
        `Invalid octet: 256` for : `IP4-address `address``
         expected type  : `IP4-address`
         got      value : `256.255.255.2`
    IP4 address must contain 4 decimal octets separated by `.`.
    >>> Test_IP4_Address (dict (address = '2560.255.2.2'), raw = True)
    Traceback (most recent call last):
     ...
    Attribute_Value: Can't set necessary attribute IP4_Address.address to `u'2560.255.2.2'`
        `Invalid octet: 2560` for : `IP4-address `address``
        expected type  : `IP4-address`
        got      value : `2560.255.2.2`
    IP4 address must contain 4 decimal octets separated by `.`.
    >>> Test_IP4_Network (dict (address = '111.222.233.244/31'), raw = True)
    GTW.OMP.NET.Test_IP4_Network (dict (address = 111.222.233.244/31))
    >>> Test_IP4_Network (dict (address = '1.2.3.4/30'), raw = True)
    GTW.OMP.NET.Test_IP4_Network (dict (address = 1.2.3.4/30))
    >>> Test_IP4_Network (dict (address = '1.2.3.4/32'), raw = True)
    GTW.OMP.NET.Test_IP4_Network (dict (address = 1.2.3.4))
    >>> Test_IP4_Network (dict (address = '0.0.0.0/0'), raw = True)
    GTW.OMP.NET.Test_IP4_Network (dict (address = 0.0.0.0/0))
    >>> Test_IP4_Network (dict (address = '1.2.3.4/22'), raw = True)
    GTW.OMP.NET.Test_IP4_Network (dict (address = 1.2.0.0/22))
    >>> Test_IP4_Network (dict (address = '1.2.3.4/33'), raw = True)
    Traceback (most recent call last):
     ...
    Attribute_Value: Can't set necessary attribute IP4_Network.address to `u'1.2.3.4/33'`
        `Invalid netmask: 33` for : `IP4-network `address``
         expected type  : `IP4-network`
         got      value : `1.2.3.4/33`
    IP4 network must contain 4 decimal octets separated by `.`, optionally followed by `/` and a number between 0 and 32. The bits right of the netmask are automatically set to zero.
    >>> Test_IP4_Network (dict (address = '1.2.3.4/333'), raw = True)
    Traceback (most recent call last):
     ...
    Attribute_Value: Can't set necessary attribute IP4_Network.address to `u'1.2.3.4/333'`
        `Invalid netmask: 333` for : `IP4-network `address``
         expected type  : `IP4-network`
         got      value : `1.2.3.4/333`
    IP4 network must contain 4 decimal octets separated by `.`, optionally followed by `/` and a number between 0 and 32. The bits right of the netmask are automatically set to zero.
    >>> Test_IP6_Address \\
    ...     ( dict (address = '2001:0db8:85a3:0000:0000:8a2e:0370:7334')
    ...     , raw = True
    ...     )
    GTW.OMP.NET.Test_IP6_Address (dict (address = 2001:db8:85a3::8a2e:370:7334))
    >>> Test_IP6_Address \\
    ...     ( dict (address = '2001:db8:85a3:0:0:8a2e:370:7335')
    ...     , raw = True
    ...     )
    GTW.OMP.NET.Test_IP6_Address (dict (address = 2001:db8:85a3::8a2e:370:7335))
    >>> Test_IP6_Address \\
    ...     ( dict (address = '2001:db8:85a3::8a2e:370:7336')
    ...     , raw = True
    ...     )
    GTW.OMP.NET.Test_IP6_Address (dict (address = 2001:db8:85a3::8a2e:370:7336))
    >>> Test_IP6_Address \\
    ...     ( dict (address = '2001:0db8:0000:0000:0000:0000:1428:57ab')
    ...     , raw = True
    ...     )
    GTW.OMP.NET.Test_IP6_Address (dict (address = 2001:db8::1428:57ab))
    >>> Test_IP6_Address \\
    ...     ( dict (address = '2001:0db8:0000:0000:0000::1428:57ac')
    ...     , raw = True
    ...     )
    GTW.OMP.NET.Test_IP6_Address (dict (address = 2001:db8::1428:57ac))
    >>> Test_IP6_Address (dict (address = '2001:0db8:0:0:0:0:1428:57ad'), raw = True)
    GTW.OMP.NET.Test_IP6_Address (dict (address = 2001:db8::1428:57ad))
    >>> Test_IP6_Address (dict (address = '2001:0db8:0:0::1428:57ae'), raw = True)
    GTW.OMP.NET.Test_IP6_Address (dict (address = 2001:db8::1428:57ae))
    >>> Test_IP6_Address (dict (address = '2001:0db8::1428:57af', raw = True))
    GTW.OMP.NET.Test_IP6_Address (dict (address = 2001:db8::1428:57af))
    >>> Test_IP6_Address (dict (address = '2001:db8::1428:57b0'), raw = True)
    GTW.OMP.NET.Test_IP6_Address (dict (address = 2001:db8::1428:57b0))
    >>> Test_IP6_Address \\
    ...     ( dict (address = '0000:0000:0000:0000:0000:0000:0000:0001')
    ...     , raw = True
    ...     )
    GTW.OMP.NET.Test_IP6_Address (dict (address = ::1))
    >>> Test_IP6_Address (dict (address = '::2'), raw = True)
    GTW.OMP.NET.Test_IP6_Address (dict (address = ::2))
    >>> Test_IP6_Address (dict (address = '::ffff:0c22:384e'), raw = True)
    GTW.OMP.NET.Test_IP6_Address (dict (address = ::ffff:c22:384e))
    >>> Test_IP6_Address \\
    ...     ( dict (address = '2001:0db8:1234:0000:0000:0000:0000:0000')
    ...     , raw = True
    ...     )
    GTW.OMP.NET.Test_IP6_Address (dict (address = 2001:db8:1234::))
    >>> Test_IP6_Address \\
    ...     ( dict (address = '2001:0db8:1234:ffff:ffff:ffff:ffff:ffff')
    ...     , raw = True
    ...     )
    GTW.OMP.NET.Test_IP6_Address (dict (address = 2001:db8:1234:ffff:ffff:ffff:ffff:ffff))
    >>> Test_IP6_Address (dict (address = '2001:db8:a::123'), raw = True)
    GTW.OMP.NET.Test_IP6_Address (dict (address = 2001:db8:a::123))
    >>> Test_IP6_Address (dict (address = 'fe80::'), raw = True)
    GTW.OMP.NET.Test_IP6_Address (dict (address = fe80::))
    >>> Test_IP6_Address (dict (address = '::ffff:c000:280'), raw = True)
    GTW.OMP.NET.Test_IP6_Address (dict (address = ::ffff:c000:280))
    >>> Test_IP6_Address (dict (address = '::'), raw = True)
    GTW.OMP.NET.Test_IP6_Address (dict (address = ::))
    >>> Test_IP6_Address (dict (address = '::ffff:12.34.56.78'), raw = True)
    Traceback (most recent call last):
     ...
    Attribute_Value: Can't set necessary attribute IP6_Address.address to `u'::ffff:12.34.56.78'`
        `Hex value too long: 12.34.56.78` for : `IP6-address `address``
         expected type  : `IP6-address`
         got      value : `::ffff:12.34.56.78`
    IP6 address must contain up to 8 hexadecimal numbers with up to 4 digits separated by `:`. A single empty group `::` can be used.
    >>> Test_IP6_Address (dict (address = '::ffff:192.0.2.128'), raw = True)
    Traceback (most recent call last):
     ...
    Attribute_Value: Can't set necessary attribute IP6_Address.address to `u'::ffff:192.0.2.128'`
        `Hex value too long: 192.0.2.128` for : `IP6-address `address``
         expected type  : `IP6-address`
         got      value : `::ffff:192.0.2.128`
    IP6 address must contain up to 8 hexadecimal numbers with up to 4 digits separated by `:`. A single empty group `::` can be used.
    >>> Test_IP6_Address (dict (address = '123'), raw = True)
    Traceback (most recent call last):
     ...
    Attribute_Value: Can't set necessary attribute IP6_Address.address to `u'123'`
        `Not enough hex parts in address: 123` for : `IP6-address `address``
         expected type  : `IP6-address`
         got      value : `123`
    IP6 address must contain up to 8 hexadecimal numbers with up to 4 digits separated by `:`. A single empty group `::` can be used.
    >>> Test_IP6_Address (dict (address = 'ldkfj'), raw = True)
    Traceback (most recent call last):
     ...
    Attribute_Value: Can't set necessary attribute IP6_Address.address to `u'ldkfj'`
        `Hex value too long: ldkfj` for : `IP6-address `address``
         expected type  : `IP6-address`
         got      value : `ldkfj`
    IP6 address must contain up to 8 hexadecimal numbers with up to 4 digits separated by `:`. A single empty group `::` can be used.
    >>> Test_IP6_Address (dict (address = '2001::FFD3::57ab'), raw = True)
    Traceback (most recent call last):
     ...
    Attribute_Value: Can't set necessary attribute IP6_Address.address to `u'2001::FFD3::57ab'`
        `Only one '::' allowed` for : `IP6-address `address``
         expected type  : `IP6-address`
         got      value : `2001::FFD3::57ab`
    IP6 address must contain up to 8 hexadecimal numbers with up to 4 digits separated by `:`. A single empty group `::` can be used.
    >>> Test_IP6_Address \\
    ...     ( dict (address = '2001:db8:85a3::8a2e:37023:7334')
    ...     , raw = True
    ...     )
    Traceback (most recent call last):
     ...
    Attribute_Value: Can't set necessary attribute IP6_Address.address to `u'2001:db8:85a3::8a2e:37023:7334'`
        `Hex value too long: 37023` for : `IP6-address `address``
         expected type  : `IP6-address`
         got      value : `2001:db8:85a3::8a2e:37023:7334`
    IP6 address must contain up to 8 hexadecimal numbers with up to 4 digits separated by `:`. A single empty group `::` can be used.
    >>> Test_IP6_Address \\
    ...     ( dict (address = '2001:db8:85a3::8a2e:370k:7334')
    ...     , raw = True
    ...     )
    Traceback (most recent call last):
     ...
    Attribute_Value: Can't set necessary attribute IP6_Address.address to `u'2001:db8:85a3::8a2e:370k:7334'`
        `invalid literal for long() with base 16: '370k'` for : `IP6-address `address``
         expected type  : `IP6-address`
         got      value : `2001:db8:85a3::8a2e:370k:7334`
    IP6 address must contain up to 8 hexadecimal numbers with up to 4 digits separated by `:`. A single empty group `::` can be used.
    >>> Test_IP6_Address (dict (address = '1:2:3:4:5:6:7:8:9'), raw = True)
    Traceback (most recent call last):
     ...
    Attribute_Value: Can't set necessary attribute IP6_Address.address to `u'1:2:3:4:5:6:7:8:9'`
        `Too many hex parts in address: 1:2:3:4:5:6:7:8:9` for : `IP6-address `address``
         expected type  : `IP6-address`
         got      value : `1:2:3:4:5:6:7:8:9`
    IP6 address must contain up to 8 hexadecimal numbers with up to 4 digits separated by `:`. A single empty group `::` can be used.
    >>> Test_IP6_Address (dict (address = '1::2::3'), raw = True)
    Traceback (most recent call last):
     ...
    Attribute_Value: Can't set necessary attribute IP6_Address.address to `u'1::2::3'`
        `Only one '::' allowed` for : `IP6-address `address``
         expected type  : `IP6-address`
         got      value : `1::2::3`
    IP6 address must contain up to 8 hexadecimal numbers with up to 4 digits separated by `:`. A single empty group `::` can be used.
    >>> Test_IP6_Address (dict (address = '1:::3:4:5'), raw = True)
    Traceback (most recent call last):
     ...
    Attribute_Value: Can't set necessary attribute IP6_Address.address to `u'1:::3:4:5'`
        `Too many ':': 1:::3:4:5` for : `IP6-address `address``
         expected type  : `IP6-address`
         got      value : `1:::3:4:5`
    IP6 address must contain up to 8 hexadecimal numbers with up to 4 digits separated by `:`. A single empty group `::` can be used.
    >>> Test_IP6_Address (dict (address = '1:2:3::4:5:6:7:8:9'), raw = True)
    Traceback (most recent call last):
     ...
    Attribute_Value: Can't set necessary attribute IP6_Address.address to `u'1:2:3::4:5:6:7:8:9'`
        `Too many hex parts in address: 1:2:3::4:5:6:7:8:9` for : `IP6-address `address``
         expected type  : `IP6-address`
         got      value : `1:2:3::4:5:6:7:8:9`
    IP6 address must contain up to 8 hexadecimal numbers with up to 4 digits separated by `:`. A single empty group `::` can be used.
    >>> Test_IP6_Address (dict (address = '::ffff:2.3.4'), raw = True)
    Traceback (most recent call last):
     ...
    Attribute_Value: Can't set necessary attribute IP6_Address.address to `u'::ffff:2.3.4'`
        `Hex value too long: 2.3.4` for : `IP6-address `address``
         expected type  : `IP6-address`
         got      value : `::ffff:2.3.4`
    IP6 address must contain up to 8 hexadecimal numbers with up to 4 digits separated by `:`. A single empty group `::` can be used.
    >>> Test_IP6_Address (dict (address = '::ffff:257.1.2.3'), raw = True)
    Traceback (most recent call last):
     ...
    Attribute_Value: Can't set necessary attribute IP6_Address.address to `u'::ffff:257.1.2.3'`
        `Hex value too long: 257.1.2.3` for : `IP6-address `address``
         expected type  : `IP6-address`
         got      value : `::ffff:257.1.2.3`
    IP6 address must contain up to 8 hexadecimal numbers with up to 4 digits separated by `:`. A single empty group `::` can be used.
    >>> Test_IP6_Address (dict (address = '1.2.3.4'), raw = True)
    Traceback (most recent call last):
     ...
    Attribute_Value: Can't set necessary attribute IP6_Address.address to `u'1.2.3.4'`
        `Hex value too long: 1.2.3.4` for : `IP6-address `address``
         expected type  : `IP6-address`
         got      value : `1.2.3.4`
    IP6 address must contain up to 8 hexadecimal numbers with up to 4 digits separated by `:`. A single empty group `::` can be used.
    >>> Test_IP6_Address (dict (address = ':aa:aa:aa'), raw = True)
    Traceback (most recent call last):
     ...
    Attribute_Value: Can't set necessary attribute IP6_Address.address to `u':aa:aa:aa'`
        `No single ':' at start allowed` for : `IP6-address `address``
         expected type  : `IP6-address`
         got      value : `:aa:aa:aa`
    IP6 address must contain up to 8 hexadecimal numbers with up to 4 digits separated by `:`. A single empty group `::` can be used.
    >>> Test_IP6_Address (dict (address = 'aa:aa:aa:'), raw = True)
    Traceback (most recent call last):
     ...
    Attribute_Value: Can't set necessary attribute IP6_Address.address to `u'aa:aa:aa:'`
        `No single ':' at end allowed` for : `IP6-address `address``
         expected type  : `IP6-address`
         got      value : `aa:aa:aa:`
    IP6 address must contain up to 8 hexadecimal numbers with up to 4 digits separated by `:`. A single empty group `::` can be used.
    >>> Test_IP6_Address (dict (address = '1:2:3:4:5:6:7'), raw = True)
    Traceback (most recent call last):
     ...
    Attribute_Value: Can't set necessary attribute IP6_Address.address to `u'1:2:3:4:5:6:7'`
        `Not enough hex parts in address: 1:2:3:4:5:6:7` for : `IP6-address `address``
         expected type  : `IP6-address`
         got      value : `1:2:3:4:5:6:7`
    IP6 address must contain up to 8 hexadecimal numbers with up to 4 digits separated by `:`. A single empty group `::` can be used.
    >>> Test_IP6_Address (dict (address = ':::'), raw = True)
    Traceback (most recent call last):
     ...
    Attribute_Value: Can't set necessary attribute IP6_Address.address to `u':::'`
        `No ':' at start and end` for : `IP6-address `address``
         expected type  : `IP6-address`
         got      value : `:::`
    IP6 address must contain up to 8 hexadecimal numbers with up to 4 digits separated by `:`. A single empty group `::` can be used.
    >>> Test_IP6_Address (dict (address = '1:2:3::/127'), raw = True)
    Traceback (most recent call last):
     ...
    Attribute_Value: Can't set IP6-address `address` attribute IP6_Address.address to `1:2:3::/127`
        Invalid netmask: 127; must be empty or 128

    >>> Test_IP6_Network (dict (address = '1:2:3::/48'), raw = True)
    GTW.OMP.NET.Test_IP6_Network (dict (address = 1:2:3::/48))
    >>> Test_IP6_Network (dict (address = '1:2:3::/128'), raw = True)
    GTW.OMP.NET.Test_IP6_Network (dict (address = 1:2:3::))
    >>> n = Test_IP6_Network (dict (address = '2001:db8:a::123'), raw = True)
    >>> n
    GTW.OMP.NET.Test_IP6_Network (dict (address = 2001:db8:a::123))
    >>> n.address.mask_len
    128
    >>> Test_IP6_Network (dict (address = '::/0'), raw = True)
    GTW.OMP.NET.Test_IP6_Network (dict (address = ::/0))
    >>> Test_IP6_Network (dict (address = '1:2:3::/1'), raw = True)
    GTW.OMP.NET.Test_IP6_Network (dict (address = ::/1))
    >>> Test_IP6_Network (dict (address = '1:2:3::/129'), raw = True)
    Traceback (most recent call last):
     ...
    Attribute_Value: Can't set necessary attribute IP6_Network.address to `u'1:2:3::/129'`
        `Invalid netmask: 129` for : `IP6-network `address``
         expected type  : `IP6-network`
         got      value : `1:2:3::/129`
    IP6 network must contain up to 8 hexadecimal numbers with up to 4 digits separated by `:`. A single empty group `::` can be used. This is optionally followed by `/` and a number between 0 and 128. The bits right of the netmask are automatically set to zero.
    >>> Test_IP6_Network (dict (address = '1:2:3::/1290'), raw = True)
    Traceback (most recent call last):
     ...
    Attribute_Value: Can't set necessary attribute IP6_Network.address to `u'1:2:3::/1290'`
        `Invalid netmask: 1290` for : `IP6-network `address``
         expected type  : `IP6-network`
         got      value : `1:2:3::/1290`
    IP6 network must contain up to 8 hexadecimal numbers with up to 4 digits separated by `:`. A single empty group `::` can be used. This is optionally followed by `/` and a number between 0 and 128. The bits right of the netmask are automatically set to zero.
    >>> scope.destroy ()
"""

_query_test = r"""
    >>> scope = Scaffold.scope (%(p1)s, %(n1)s) # doctest:+ELLIPSIS
    Creating new scope MOMT__...
    >>> NET = scope.GTW.OMP.NET
    >>> Test_IP4_Address = NET.Test_IP4_Address
    >>> Test_IP4_Network = NET.Test_IP4_Network
    >>> Test_IP6_Address = NET.Test_IP6_Address
    >>> Test_IP6_Network = NET.Test_IP6_Network

    >>> i40 = Test_IP4_Address (dict (address = '192.168.0.1'),    raw = True)
    >>> i41 = Test_IP4_Address (dict (address = '192.168.1.1'),    raw = True)
    >>> i42 = Test_IP4_Address (dict (address = '192.168.1.2'),    raw = True)
    >>> i43 = Test_IP4_Address (dict (address = '192.168.1.20'),   raw = True)
    >>> i40.address.address
    192.168.0.1
    >>> i41.address.address
    192.168.1.1
    >>> i42.address.address
    192.168.1.2
    >>> i43.address.address
    192.168.1.20

    >>> n41 = Test_IP4_Network (dict (address = '192.168.1.0/28'), raw = True)
    >>> n42 = Test_IP4_Network (dict (address = '192.168.1.0/29'), raw = True)
    >>> n43 = Test_IP4_Network (dict (address = '192.168.1.8/29'), raw = True)
    >>> n44 = Test_IP4_Network (dict (address = '192.168.2.0/28'), raw = True)
    >>> n45 = Test_IP4_Network (dict (address = '192.168.1.0/27'), raw = True)
    >>> n46 = Test_IP4_Network (dict (address = '192.168.0.0/27'), raw = True)
    >>> n41.address.address
    192.168.1.0/28
    >>> n42.address.address
    192.168.1.0/29
    >>> n43.address.address
    192.168.1.8/29
    >>> n44.address.address
    192.168.2.0/28
    >>> n45.address.address
    192.168.1.0/27
    >>> n46.address.address
    192.168.0.0/27
    >>> scope.commit ()

    >>> address = i41.address
    >>> network = n41.address
    >>> Test_IP4_Address.query (Q.address == address).count ()
    1
    >>> Test_IP4_Address.query (Q.address != address).count ()
    3
    >>> Test_IP4_Address.query (Q.address >= address).count ()
    3
    >>> Test_IP4_Address.query (Q.address >  address).count ()
    2
    >>> Test_IP4_Address.query (Q.address <  address).count ()
    1
    >>> Test_IP4_Address.query (Q.address <= address).count ()
    2

    >>> Test_IP4_Address.query (Q.address.IN (network)).count ()
    2

    >>> Test_IP4_Network.query (Q.address.IN (network)).count ()
    3
    >>> r = Test_IP4_Network.query (Q.address.IN (network)).all ()
    >>> list (sorted (x.address.address for x in r))
    [192.168.1.0/29, 192.168.1.0/28, 192.168.1.8/29]

    >>> Test_IP4_Network.query (Q.address == network).count ()
    1
    >>> Test_IP4_Network.query (Q.address != network).count ()
    5
    >>> Test_IP4_Network.query (Q.address >= network).count ()
    4
    >>> Test_IP4_Network.query (Q.address >  network).count ()
    3
    >>> Test_IP4_Network.query (Q.address <  network).count ()
    2
    >>> Test_IP4_Network.query (Q.address <= network).count ()
    3

    >>> i60 = Test_IP6_Address (dict (address = '2001:db7::1'),      raw = True)
    >>> i61 = Test_IP6_Address (dict (address = '2001:db8::1'),      raw = True)
    >>> i62 = Test_IP6_Address (dict (address = '2001:db8::2'),      raw = True)
    >>> i63 = Test_IP6_Address (dict (address = '2001:db8::20'),     raw = True)
    >>> i60.address.address
    2001:db7::1
    >>> i61.address.address
    2001:db8::1
    >>> i62.address.address
    2001:db8::2
    >>> i63.address.address
    2001:db8::20

    >>> n61 = Test_IP6_Network (dict (address = '2001:db8::/124'),   raw = True)
    >>> n62 = Test_IP6_Network (dict (address = '2001:db8::/125'),   raw = True)
    >>> n63 = Test_IP6_Network (dict (address = '2001:db8::8/125'),  raw = True)
    >>> n64 = Test_IP6_Network (dict (address = '2001:db8::10/124'), raw = True)
    >>> n65 = Test_IP6_Network (dict (address = '2001:db8::/123'),   raw = True)
    >>> n66 = Test_IP6_Network (dict (address = '2001:db7::/123'),   raw = True)
    >>> n61.address.address
    2001:db8::/124
    >>> n62.address.address
    2001:db8::/125
    >>> n63.address.address
    2001:db8::8/125
    >>> n64.address.address
    2001:db8::10/124
    >>> n65.address.address
    2001:db8::/123
    >>> n66.address.address
    2001:db7::/123
    >>> scope.commit ()

    >>> address = i61.address
    >>> network = n61.address
    >>> Test_IP6_Address.query (Q.address == address).count ()
    1
    >>> Test_IP6_Address.query (Q.address != address).count ()
    3
    >>> Test_IP6_Address.query (Q.address >= address).count ()
    3
    >>> Test_IP6_Address.query (Q.address >  address).count ()
    2
    >>> Test_IP6_Address.query (Q.address <  address).count ()
    1
    >>> Test_IP6_Address.query (Q.address <= address).count ()
    2

    >>> Test_IP6_Address.query (Q.address.IN (network)).count ()
    2

    >>> Test_IP6_Network.query (Q.address.IN (network)).count ()
    3
    >>> r = Test_IP6_Network.query (Q.address.IN (network)).all ()
    >>> list (sorted (x.address.address for x in r))
    [2001:db8::/125, 2001:db8::/124, 2001:db8::8/125]

    >>> Test_IP6_Network.query (Q.address == network).count ()
    1
    >>> Test_IP6_Network.query (Q.address != network).count ()
    5
    >>> Test_IP6_Network.query (Q.address >= network).count ()
    4
    >>> Test_IP6_Network.query (Q.address >  network).count ()
    3
    >>> Test_IP6_Network.query (Q.address <  network).count ()
    2
    >>> Test_IP6_Network.query (Q.address <= network).count ()
    3

    >>> qd  = dict (address = dict (address = '192.168.1.8/29'))
    >>> rqs = Test_IP4_Network.raw_query_attrs (qd, qd)
    >>> rqs
    (Q.address.address == 192.168.1.8/29,)
    >>> matches = Test_IP4_Network.query_s (* rqs).all ()
    >>> print "\n".join (repr (x) for x in matches)
    GTW.OMP.NET.Test_IP4_Network (dict (address = 192.168.1.8/29))

    >>> matches2 = Test_IP4_Network.query_s (Q.address.address == n43.address.address).all ()
    >>> print "\n".join (repr (x) for x in matches2)
    GTW.OMP.NET.Test_IP4_Network (dict (address = 192.168.1.8/29))

    >>> scope.destroy ()
"""
from _GTW.__test__.model import *

__test__ = Scaffold.create_test_dict \
    ( dict (test_code = _test_code, query_test = _query_test))

### __END__ GTW.__test__.Attr_Net
