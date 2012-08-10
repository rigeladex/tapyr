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
#    ««revision-date»»···
#--

from   __future__  import unicode_literals

from   _MOM.import_MOM          import *
from   _GTW._OMP._NET.Attr_Type import *
from   _TFL.Package_Namespace   import Derived_Package_Namespace

Namespace = Derived_Package_Namespace (parent = MOM, name = "_GTW._OMP._NET")

_Ancestor_Essence = MOM.Object

class IP4_Address (_Ancestor_Essence) :

    PNS = Namespace

    class _Attributes (_Ancestor_Essence._Attributes) :

        class address (A_IP4_Address) :

            kind = Attr.Primary

        # end class address

    # end class _Attributes

# end class IP4_Address

_Ancestor_Essence = MOM.Object

class IP4_Network (_Ancestor_Essence) :

    PNS = Namespace

    class _Attributes (_Ancestor_Essence._Attributes) :

        class address (A_IP4_Network) :

            kind = Attr.Primary

        # end class address

    # end class _Attributes

# end class IP4_Network

_Ancestor_Essence = MOM.Object

class IP6_Address (_Ancestor_Essence) :

    PNS = Namespace

    class _Attributes (_Ancestor_Essence._Attributes) :

        class address (A_IP6_Address) :

            kind = Attr.Primary

        # end class address

    # end class _Attributes

# end class IP6_Address

_Ancestor_Essence = MOM.Object

class IP6_Network (_Ancestor_Essence) :

    PNS = Namespace

    class _Attributes (_Ancestor_Essence._Attributes) :

        class address (A_IP6_Network) :

            kind = Attr.Primary

        # end class address

    # end class _Attributes

# end class IP6_Network

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
    >>> IP4_Address = NET.IP4_Address
    >>> IP4_Network = NET.IP4_Network
    >>> IP6_Address = NET.IP6_Address
    >>> IP6_Network = NET.IP6_Network
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
    >>> IP4_Address (dict (address = '1.2.3.4'))
    GTW.OMP.NET.IP4_Address (dict (address = u'1.2.3.4'))
    >>> IP4_Address (dict (address = '111.222.233.244'))
    GTW.OMP.NET.IP4_Address (dict (address = u'111.222.233.244'))
    >>> IP4_Address (dict (address = '111.222.233.244/22'))
    Traceback (most recent call last):
     ...
    Invariants: Condition `AC_check_address_length` : Value for address must not be longer than 15 (length <= 15)
        address = '111.222.233.244/22'
        length = 18 << len (address)
      `Syntax error` for : `IP4-address `address``
         expected type  : `IP4-address`
         got      value : `111.222.233.244/22`
    IP4 address must contain 4 decimal octets separated by `.`.
    >>> IP4_Address (dict (address = '1.2.3.4/22'))
    Traceback (most recent call last):
     ...
    Invariants: `Syntax error` for : `IP4-address `address``
         expected type  : `IP4-address`
         got      value : `1.2.3.4/22`
    IP4 address must contain 4 decimal octets separated by `.`.
    >>> IP4_Address (dict (address = '256.255.255.2'))
    Traceback (most recent call last):
     ...
    Invariants: `Syntax error` for : `IP4-address `address``
         expected type  : `IP4-address`
         got      value : `256.255.255.2`
    IP4 address must contain 4 decimal octets separated by `.`.
    >>> IP4_Address (dict (address = '2560.255.2.2'))
    Traceback (most recent call last):
     ...
    Invariants: `Syntax error` for : `IP4-address `address``
         expected type  : `IP4-address`
         got      value : `2560.255.2.2`
    IP4 address must contain 4 decimal octets separated by `.`.
    >>> IP4_Network (dict (address = '111.222.233.244/31'))
    GTW.OMP.NET.IP4_Network (dict (address = u'111.222.233.244/31'))
    >>> IP4_Network (dict (address = '1.2.3.4/30'))
    GTW.OMP.NET.IP4_Network (dict (address = u'1.2.3.4/30'))
    >>> IP4_Network (dict (address = '1.2.3.4/32'))
    GTW.OMP.NET.IP4_Network (dict (address = u'1.2.3.4/32'))
    >>> IP4_Network (dict (address = '0.0.0.0/0'))
    GTW.OMP.NET.IP4_Network (dict (address = u'0.0.0.0/0'))
    >>> IP4_Network (dict (address = '1.2.3.4/22'))
    Traceback (most recent call last):
     ...
    Invariants: `Syntax error` for : `IP4-network `address``
         expected type  : `IP4-network`
         got      value : `1.2.3.4/22`
    IP4 network must contain 4 decimal octets separated by `.`, optionally followed by `/` and a number between 0 and 32. The bits right of the netmask must be zero.
    >>> IP4_Network (dict (address = '1.2.3.4/33'))
    Traceback (most recent call last):
     ...
    Invariants: `Syntax error` for : `IP4-network `address``
         expected type  : `IP4-network`
         got      value : `33`
    IP4 network must contain 4 decimal octets separated by `.`, optionally followed by `/` and a number between 0 and 32. The bits right of the netmask must be zero.
    >>> IP4_Network (dict (address = '1.2.3.4/333'))
    Traceback (most recent call last):
     ...
    Invariants: `Syntax error` for : `IP4-network `address``
         expected type  : `IP4-network`
         got      value : `1.2.3.4/333`
    IP4 network must contain 4 decimal octets separated by `.`, optionally followed by `/` and a number between 0 and 32. The bits right of the netmask must be zero.
    >>> IP6_Address (dict (address = '2001:0db8:85a3:0000:0000:8a2e:0370:7334'))
    GTW.OMP.NET.IP6_Address (dict (address = u'2001:0db8:85a3:0000:0000:8a2e:0370:7334'))
    >>> IP6_Address (dict (address = '2001:db8:85a3:0:0:8a2e:370:7334'))
    GTW.OMP.NET.IP6_Address (dict (address = u'2001:db8:85a3:0:0:8a2e:370:7334'))
    >>> IP6_Address (dict (address = '2001:db8:85a3::8a2e:370:7334'))
    GTW.OMP.NET.IP6_Address (dict (address = u'2001:db8:85a3::8a2e:370:7334'))
    >>> IP6_Address (dict (address = '2001:0db8:0000:0000:0000:0000:1428:57ab'))
    GTW.OMP.NET.IP6_Address (dict (address = u'2001:0db8:0000:0000:0000:0000:1428:57ab'))
    >>> IP6_Address (dict (address = '2001:0db8:0000:0000:0000::1428:57ab'))
    GTW.OMP.NET.IP6_Address (dict (address = u'2001:0db8:0000:0000:0000::1428:57ab'))
    >>> IP6_Address (dict (address = '2001:0db8:0:0:0:0:1428:57ab'))
    GTW.OMP.NET.IP6_Address (dict (address = u'2001:0db8:0:0:0:0:1428:57ab'))
    >>> IP6_Address (dict (address = '2001:0db8:0:0::1428:57ab'))
    GTW.OMP.NET.IP6_Address (dict (address = u'2001:0db8:0:0::1428:57ab'))
    >>> IP6_Address (dict (address = '2001:0db8::1428:57ab'))
    GTW.OMP.NET.IP6_Address (dict (address = u'2001:0db8::1428:57ab'))
    >>> IP6_Address (dict (address = '2001:db8::1428:57ab'))
    GTW.OMP.NET.IP6_Address (dict (address = u'2001:db8::1428:57ab'))
    >>> IP6_Address (dict (address = '0000:0000:0000:0000:0000:0000:0000:0001'))
    GTW.OMP.NET.IP6_Address (dict (address = u'0000:0000:0000:0000:0000:0000:0000:0001'))
    >>> IP6_Address (dict (address = '::1'))
    GTW.OMP.NET.IP6_Address (dict (address = u'::1'))
    >>> IP6_Address (dict (address = '::ffff:0c22:384e'))
    GTW.OMP.NET.IP6_Address (dict (address = u'::ffff:0c22:384e'))
    >>> IP6_Address (dict (address = '2001:0db8:1234:0000:0000:0000:0000:0000'))
    GTW.OMP.NET.IP6_Address (dict (address = u'2001:0db8:1234:0000:0000:0000:0000:0000'))
    >>> IP6_Address (dict (address = '2001:0db8:1234:ffff:ffff:ffff:ffff:ffff'))
    GTW.OMP.NET.IP6_Address (dict (address = u'2001:0db8:1234:ffff:ffff:ffff:ffff:ffff'))
    >>> IP6_Address (dict (address = '2001:db8:a::123'))
    GTW.OMP.NET.IP6_Address (dict (address = u'2001:db8:a::123'))
    >>> IP6_Address (dict (address = 'fe80::'))
    GTW.OMP.NET.IP6_Address (dict (address = u'fe80::'))
    >>> IP6_Address (dict (address = '::ffff:c000:280'))
    GTW.OMP.NET.IP6_Address (dict (address = u'::ffff:c000:280'))
    >>> IP6_Address (dict (address = '::'))
    GTW.OMP.NET.IP6_Address (dict (address = u'::'))
    >>> IP6_Address (dict (address = '::ffff:12.34.56.78'))
    Traceback (most recent call last):
     ...
    Invariants: `Syntax error` for : `IP6-address `address``
         expected type  : `IP6-address`
         got      value : `::ffff:12.34.56.78`
    IP6 address must contain up to 8 hexadecimal numbers with up to 4 digits separated by `:`. A single empty group `::` can be used.
    >>> IP6_Address (dict (address = '::ffff:192.0.2.128'))
    Traceback (most recent call last):
     ...
    Invariants: `Syntax error` for : `IP6-address `address``
         expected type  : `IP6-address`
         got      value : `::ffff:192.0.2.128`
    IP6 address must contain up to 8 hexadecimal numbers with up to 4 digits separated by `:`. A single empty group `::` can be used.
    >>> IP6_Address (dict (address = '123'))
    Traceback (most recent call last):
     ...
    Invariants: `Syntax error` for : `IP6-address `address``
         expected type  : `IP6-address`
         got      value : `123`
    IP6 address must contain up to 8 hexadecimal numbers with up to 4 digits separated by `:`. A single empty group `::` can be used.
    >>> IP6_Address (dict (address = 'ldkfj'))
    Traceback (most recent call last):
     ...
    Invariants: `Syntax error` for : `IP6-address `address``
         expected type  : `IP6-address`
         got      value : `ldkfj`
    IP6 address must contain up to 8 hexadecimal numbers with up to 4 digits separated by `:`. A single empty group `::` can be used.
    >>> IP6_Address (dict (address = '2001::FFD3::57ab'))
    Traceback (most recent call last):
     ...
    Invariants: `Syntax error` for : `IP6-address `address``
         expected type  : `IP6-address`
         got      value : `2001::FFD3::57ab`
    IP6 address must contain up to 8 hexadecimal numbers with up to 4 digits separated by `:`. A single empty group `::` can be used.
    >>> IP6_Address (dict (address = '2001:db8:85a3::8a2e:37023:7334'))
    Traceback (most recent call last):
     ...
    Invariants: `Syntax error` for : `IP6-address `address``
         expected type  : `IP6-address`
         got      value : `2001:db8:85a3::8a2e:37023:7334`
    IP6 address must contain up to 8 hexadecimal numbers with up to 4 digits separated by `:`. A single empty group `::` can be used.
    >>> IP6_Address (dict (address = '2001:db8:85a3::8a2e:370k:7334'))
    Traceback (most recent call last):
     ...
    Invariants: `Syntax error` for : `IP6-address `address``
         expected type  : `IP6-address`
         got      value : `2001:db8:85a3::8a2e:370k:7334`
    IP6 address must contain up to 8 hexadecimal numbers with up to 4 digits separated by `:`. A single empty group `::` can be used.
    >>> IP6_Address (dict (address = '1:2:3:4:5:6:7:8:9'))
    Traceback (most recent call last):
     ...
    Invariants: `Syntax error` for : `IP6-address `address``
         expected type  : `IP6-address`
         got      value : `1:2:3:4:5:6:7:8:9`
    IP6 address must contain up to 8 hexadecimal numbers with up to 4 digits separated by `:`. A single empty group `::` can be used.
    >>> IP6_Address (dict (address = '1::2::3'))
    Traceback (most recent call last):
     ...
    Invariants: `Syntax error` for : `IP6-address `address``
         expected type  : `IP6-address`
         got      value : `1::2::3`
    IP6 address must contain up to 8 hexadecimal numbers with up to 4 digits separated by `:`. A single empty group `::` can be used.
    >>> IP6_Address (dict (address = '1:::3:4:5'))
    Traceback (most recent call last):
     ...
    Invariants: `Syntax error` for : `IP6-address `address``
         expected type  : `IP6-address`
         got      value : `1:::3:4:5`
    IP6 address must contain up to 8 hexadecimal numbers with up to 4 digits separated by `:`. A single empty group `::` can be used.
    >>> IP6_Address (dict (address = '1:2:3::4:5:6:7:8:9'))
    Traceback (most recent call last):
     ...
    Invariants: `Syntax error` for : `IP6-address `address``
         expected type  : `IP6-address`
         got      value : `1:2:3::4:5:6:7:8:9`
    IP6 address must contain up to 8 hexadecimal numbers with up to 4 digits separated by `:`. A single empty group `::` can be used.
    >>> IP6_Address (dict (address = '::ffff:2.3.4'))
    Traceback (most recent call last):
     ...
    Invariants: `Syntax error` for : `IP6-address `address``
         expected type  : `IP6-address`
         got      value : `::ffff:2.3.4`
    IP6 address must contain up to 8 hexadecimal numbers with up to 4 digits separated by `:`. A single empty group `::` can be used.
    >>> IP6_Address (dict (address = '::ffff:257.1.2.3'))
    Traceback (most recent call last):
     ...
    Invariants: `Syntax error` for : `IP6-address `address``
         expected type  : `IP6-address`
         got      value : `::ffff:257.1.2.3`
    IP6 address must contain up to 8 hexadecimal numbers with up to 4 digits separated by `:`. A single empty group `::` can be used.
    >>> IP6_Address (dict (address = '1.2.3.4'))
    Traceback (most recent call last):
     ...
    Invariants: `Syntax error` for : `IP6-address `address``
         expected type  : `IP6-address`
         got      value : `1.2.3.4`
    IP6 address must contain up to 8 hexadecimal numbers with up to 4 digits separated by `:`. A single empty group `::` can be used.
    >>> IP6_Address (dict (address = ':aa:aa:aa'))
    Traceback (most recent call last):
     ...
    Invariants: `Syntax error` for : `IP6-address `address``
         expected type  : `IP6-address`
         got      value : `:aa:aa:aa`
    IP6 address must contain up to 8 hexadecimal numbers with up to 4 digits separated by `:`. A single empty group `::` can be used.
    >>> IP6_Address (dict (address = 'aa:aa:aa:'))
    Traceback (most recent call last):
     ...
    Invariants: `Syntax error` for : `IP6-address `address``
         expected type  : `IP6-address`
         got      value : `aa:aa:aa:`
    IP6 address must contain up to 8 hexadecimal numbers with up to 4 digits separated by `:`. A single empty group `::` can be used.
    >>> IP6_Address (dict (address = '1:2:3:4:5:6:7'))
    Traceback (most recent call last):
     ...
    Invariants: `Syntax error` for : `IP6-address `address``
         expected type  : `IP6-address`
         got      value : `1:2:3:4:5:6:7`
    IP6 address must contain up to 8 hexadecimal numbers with up to 4 digits separated by `:`. A single empty group `::` can be used.
    >>> IP6_Address (dict (address = ':::'))
    Traceback (most recent call last):
     ...
    Invariants: `Syntax error` for : `IP6-address `address``
         expected type  : `IP6-address`
         got      value : `:::`
    IP6 address must contain up to 8 hexadecimal numbers with up to 4 digits separated by `:`. A single empty group `::` can be used.
    >>> IP6_Network (dict (address = '1:2:3::/48'))
    GTW.OMP.NET.IP6_Network (dict (address = u'1:2:3::/48'))
    >>> IP6_Network (dict (address = '1:2:3::/128'))
    GTW.OMP.NET.IP6_Network (dict (address = u'1:2:3::/128'))
    >>> IP6_Network (dict (address = '::/0'))
    GTW.OMP.NET.IP6_Network (dict (address = u'::/0'))
    >>> IP6_Network (dict (address = '1:2:3::/0'))
    Traceback (most recent call last):
     ...
    Invariants: `Syntax error` for : `IP6-network `address``
         expected type  : `IP6-network`
         got      value : `1:2:3::/0`
    IP6 network must contain up to 8 hexadecimal numbers with up to 4 digits separated by `:`. A single empty group `::` can be used. This is optionally followed by `/` and a number between 0 and 128. The bits right of the netmask must be zero.
    >>> IP6_Network (dict (address = '1:2:3::/129'))
    Traceback (most recent call last):
     ...
    Invariants: `Syntax error` for : `IP6-network `address``
         expected type  : `IP6-network`
         got      value : `129`
    IP6 network must contain up to 8 hexadecimal numbers with up to 4 digits separated by `:`. A single empty group `::` can be used. This is optionally followed by `/` and a number between 0 and 128. The bits right of the netmask must be zero.
    >>> IP6_Network (dict (address = '1:2:3::/1290'))
    Traceback (most recent call last):
     ...
    Invariants: `Syntax error` for : `IP6-network `address``
         expected type  : `IP6-network`
         got      value : `1:2:3::/1290`
    IP6 network must contain up to 8 hexadecimal numbers with up to 4 digits separated by `:`. A single empty group `::` can be used. This is optionally followed by `/` and a number between 0 and 128. The bits right of the netmask must be zero.
"""

from _GTW.__test__.model import *

__test__ = Scaffold.create_test_dict (_test_code)

### __END__ GTW.__test__.Attr_Net
