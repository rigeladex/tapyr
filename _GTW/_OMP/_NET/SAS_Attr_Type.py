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
#    GTW.OMP.NET.SAS_Attr_Type
#
# Purpose
#    Define SAS-specific attribute types for package GTW.OMP.NET
#
# Revision Dates
#    24-Sep-2012 (RS) Creation, factored from `GTW.OMP.NET.Attr_Type`
#    ««revision-date»»···
#--

from   __future__  import absolute_import, division, unicode_literals

from    sqlalchemy              import sql
from   _MOM.import_MOM          import *
from   _GTW                     import GTW

import _GTW._OMP._NET
from   _GTW._OMP._NET.Attr_Type import *

from   _MOM._DBW._SAS.Attr_Type import Add_Classmethod, _sa_string

class _SAS_IP_Address_Query_Mixin_ (TFL.Meta.Object) :

    def __ne__ (self, rhs) :
        return sql.not_ (self.__eq__ (rhs))
    # end def __ne__

# end class _SAS_IP_Address_Query_Mixin_

class _SAS_IP4_Address_Query_Mixin_ (_SAS_IP_Address_Query_Mixin_) :
    """Special query code for IP4 address objects"""

    def in_ (self, rhs) :
        return sql.and_ \
            ( rhs .numeric_address <= self.numeric_address
            , self.numeric_address <= rhs .upper_bound
            )
    # end def in_

    # explicit definition of comparisons, otherwise inheritance (and
    # consequently the _Net_Cmp_Mixin_) won't work.

    def __eq__ (self, rhs) :
        return sql.and_ (self.numeric_address == rhs.numeric_address)
    # end def __eq__
    adr_eq = __eq__ # this is used in network comparison

    def __ge__ (self, rhs) :
        return sql.and_ (self.numeric_address >= rhs.numeric_address)
    # end def __ge__

    def __gt__ (self, rhs) :
        return sql.and_ (self.numeric_address >  rhs.numeric_address)
    # end def __ge__

    def __le__ (self, rhs) :
        return sql.and_ (self.numeric_address <= rhs.numeric_address)
    # end def __ge__

    def __lt__ (self, rhs) :
        return sql.and_ (self.numeric_address <  rhs.numeric_address)
    # end def __ge__

# end class _SAS_IP4_Address_Query_Mixin_

class _SAS_IP6_Address_Query_Mixin_ (_SAS_IP_Address_Query_Mixin_) :
    """Special query code for IP6 address objects"""

    def in_ (self, rhs) :
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
        return sql.and_ \
            ( self.numeric_address_high == rhs.numeric_address_high
            , self.numeric_address_low  == rhs.numeric_address_low
            )
    # end def __eq__
    adr_eq = __eq__ # this is used in network comparison

    def __ge__ (self, rhs) :
        return sql.or_ \
            ( self.numeric_address_high > rhs.numeric_address_high
            , sql.and_
                ( self.numeric_address_high == rhs.numeric_address_high
                , self.numeric_address_low  >= rhs.numeric_address_low
                )
            )
    # end def __ge__

    def __gt__ (self, rhs) :
        return sql.or_ \
            ( self.numeric_address_high > rhs.numeric_address_high
            , sql.and_
                ( self.numeric_address_high == rhs.numeric_address_high
                , self.numeric_address_low  >  rhs.numeric_address_low
                )
            )
    # end def __gt__

    def __le__ (self, rhs) :
        return sql.or_ \
            ( self.numeric_address_high < rhs.numeric_address_high
            , sql.and_
                ( self.numeric_address_high == rhs.numeric_address_high
                , self.numeric_address_low  <= rhs.numeric_address_low
                )
            )
    # end def __le__

    def __lt__ (self, rhs) :
        return sql.or_ \
            ( self.numeric_address_high < rhs.numeric_address_high
            , sql.and_
                ( self.numeric_address_high == rhs.numeric_address_high
                , self.numeric_address_low  <  rhs.numeric_address_low
                )
            )
    # end def __lt__

# end class _SAS_IP6_Address_Query_Mixin_

class _Net_Cmp_Mixin_ (TFL.Meta.Object) :

    def in_ (self, rhs) :
        return sql.and_ \
            ( self.__super.in_ (rhs)
            , rhs.mask_len <= self.mask_len
            )
    # end def in_

    def __eq__ (self, rhs) :
        return sql.and_ \
            ( self.__super.__eq__ (rhs)
            , self.mask_len == rhs.mask_len
            )
    # end def __eq__

    def __ge__ (self, rhs) :
        return sql.or_ \
            ( self.__super.__gt__ (rhs) # yes, really __gt__
            , sql.and_
                ( self.mask_len <= rhs.mask_len
                , self.adr_eq (rhs)
                )
            )
    # end def __ge__

    def __gt__ (self, rhs) :
        return sql.or_ \
            ( self.__super.__gt__ (rhs)
            , sql.and_
                ( self.mask_len < rhs.mask_len
                , self.adr_eq (rhs)
                )
            )
    # end def __gt__

    def __le__ (self, rhs) :
        return sql.or_ \
            ( self.__super.__lt__ (rhs) # yes, really __lt__
            , sql.and_
                ( self.mask_len >= rhs.mask_len
                , self.adr_eq (rhs)
                )
            )
    # end def __le__

    def __lt__ (self, rhs) :
        return sql.or_ \
            ( self.__super.__lt__ (rhs)
            , sql.and_
                ( self.mask_len > rhs.mask_len
                , self.adr_eq (rhs)
                )
            )
    # end def __lt__

# end class _Net_Cmp_Mixin_

class _SAS_IP6_Network_Query_Mixin_ (_Net_Cmp_Mixin_, _SAS_IP6_Address_Query_Mixin_) :
    pass
# end class _SAS_IP6_Network_Query_Mixin_

class _SAS_IP4_Network_Query_Mixin_ (_Net_Cmp_Mixin_, _SAS_IP4_Address_Query_Mixin_) :
    pass
# end class _SAS_IP4_Network_Query_Mixin_


A2C = TFL.Add_To_Class
A2C ("SAS_Query_Mixin", A_IP4_Address) (_SAS_IP4_Address_Query_Mixin_)
A2C ("SAS_Query_Mixin", A_IP4_Network) (_SAS_IP4_Network_Query_Mixin_)
A2C ("SAS_Query_Mixin", A_IP6_Address) (_SAS_IP6_Address_Query_Mixin_)
A2C ("SAS_Query_Mixin", A_IP6_Network) (_SAS_IP6_Network_Query_Mixin_)


@Add_Classmethod ("_sa_columns", _A_IP_Address_)
def _sa_col_ip (cls, attr, kind, unique, owner_etype, ** kw) :
    sa_type = _sa_string (cls, attr, kind, ** kw)
    col     = cls.SAS_Column_Class (attr._sa_col_name, sa_type, **kw)
    col.mom_kind = kind
    return (col, )
# end def _sa_col_ip

__all__ = tuple \
    (  k for (k, v) in globals ().iteritems ()
    if isinstance (v, MOM.Meta.M_Attr_Type)
    )

if __name__ != "__main__" :
    GTW.OMP.NET._Export ("*")
### __END__ GTW.OMP.NET.Attr_Type
