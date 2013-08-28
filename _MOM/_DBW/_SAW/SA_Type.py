# -*- coding: iso-8859-15 -*-
# Copyright (C) 2013 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# #*** <License> ************************************************************#
# This module is part of the package MOM.DBW.SAW.
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
#    MOM.DBW.SAW.SA_Type
#
# Purpose
#    Encapsulate SQLalchemy types
#
# Revision Dates
#     8-Jul-2013 (CT) Creation
#    18-Jul-2013 (CT) Add support for overriding `_Type_Name_`, fix bugs
#    30-Jul-2013 (CT) Change `_Type_Name_Integer_` to allow undefined values;
#                     needed by MD_Change instances not bound to Entities
#     4-Aug-2013 (CT) Fix `_Type_Name_Integer_.process_bind_param`
#    ««revision-date»»···
#--

from   __future__            import division, print_function
from   __future__            import absolute_import, unicode_literals

from   _MOM                  import MOM
from   _TFL                  import TFL
from   _TFL.pyk              import pyk

from   _MOM._DBW._SAW        import SA
import _MOM._Attr.Type

import _TFL._Meta.Object
import _TFL._Meta.Property

import datetime

class _Id_Entity_ (SA.types.TypeDecorator) :
    """Augmented integer type that converts entities to pids"""

    def process_bind_param (self, value, dialect) :
        return getattr (value, "pid", value)
    # end def process_bind_param

# end class _Id_Entity_

class _Type_Name_Integer_ (SA.types.TypeDecorator) :
    """Augmented integer type that converts MOM type_names to/from integers"""

    _MOM_ATW = None
    impl     = SA.types.SmallInteger

    def process_bind_param   (self, value, dialect) :
        tn_map = self._MOM_ATW.tn_map
        if value is None :
            value = -1
        elif isinstance (value, pyk.string_types) :
            value = tn_map [value]
        return value
    # end def process_bind_param

    def process_result_value (self, value, dialect) :
        if isinstance (value, pyk.int_types) :
            tn_map = self._MOM_ATW.tn_map
            return tn_map [value] if value >= 0 else None
        elif value is not None :
            return str (value)
    # end def process_result_value

# end class _Type_Name_Integer_

class M_SA_Type (TFL.Meta.Object.__class__) :
    """Encapsulate SQLalchemy types"""

    @TFL.Meta.Once_Property
    def P_Int_Types (cls) :
        """Map (`min_value`, `max_value`) tuples to SA integer types"""
        _AI = MOM.Attr._A_Int_
        return \
            ( (_AI.min_value_16, _AI.max_value_16, cls.SmallInteger)
            , (_AI.min_value_32, _AI.max_value_32, cls.Integer)
            , (_AI.min_value_64, _AI.max_value_64, cls.BigInteger)
            )
    # end def P_Int_Types

    @TFL.Meta.Once_Property
    def P_Type_Map (cls) :
        """Map python types to SA types"""
        return \
            { bool              : cls.Boolean
            , datetime.date     : cls.Date
            , datetime.datetime : cls.DateTime
            , datetime.time     : cls.Time
            , float             : cls.Float
            }
    # end def P_Type_Map

    def __getattr__ (cls, name) :
        result = getattr (SA.types, name)
        setattr (cls, name, result)
        return result
    # end def __getattr__

# end class M_SA_Type

class SA_Type (TFL.Meta.BaM (TFL.Meta.Object, metaclass = M_SA_Type)) :
    """Encapsulate SQLalchemy types"""

    _Type_Name_ = _Type_Name_Integer_

    def __init__ (self, ATW) :
        self._ATW = ATW
    # end def __init__

    @TFL.Meta.Once_Property
    def Id_Entity (self) :
        """Augmented integer type that converts entities to pids"""
        ATW  = self._ATW
        ET   = ATW.app_type ["MOM.Id_Entity"]
        pid  = ET.pid
        return _Id_Entity_.__class__ \
            ( str ("Id_Entity"), (_Id_Entity_, )
            , dict (impl = self.sized_int_type (pid.Pickled_Type))
            )
    # end def Id_Entity

    def sized_int_type (self, pts) :
        """Return the smallest SA integer type that can hold
           (`pts.min_value`, `pts.max_value`)
        """
        result    = None
        _AI       = MOM.Attr._A_Int_
        max_value = pts.max_value or _AI.max_value_32
        min_value = pts.min_value or _AI.min_value_32
        for tmin, tmax, result in self.P_Int_Types :
            if tmin <= min_value < max_value <= tmax :
                break
        else :
            raise TypeError \
                ( "Cannot map integer type with max-value %d and min-value %d "
                  "to a database type"
                % (max_value, min_value)
                )
        return result
    # end def sized_int_type

    @TFL.Meta.Once_Property
    def Type_Name (self) :
        """Augmented integer type that converts MOM type_names to/from integers"""
        return self._Type_Name_.__class__ \
            ( str ("Type_Name"), (self._Type_Name_, )
            , dict (_MOM_ATW = self._ATW)
            )
    # end def Type_Name

    def __getattr__ (self, name) :
        result = getattr (self.__class__, name)
        setattr (self, name, result)
        return result
    # end def __getattr__

# end class SA_Type

if __name__ != "__main__" :
    MOM.DBW.SAW._Export ("SA_Type")
### __END__ MOM.DBW.SAW.SA_Type
