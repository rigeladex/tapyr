# -*- coding: utf-8 -*-
# Copyright (C) 2011-2014 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# #*** <License> ************************************************************#
# This module is part of the package MOM.
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
#    MOM.Q_Exp
#
# Purpose
#    Extend TFL.Q_Exp to support MOM-specific query expressions,
#    e.g., for raw values
#
# Revision Dates
#    19-Jul-2011 (CT) Creation
#    19-Jul-2011 (MG) `_name` converted to `Once_Property`
#    13-Sep-2011 (CT) All Q_Exp internal classes renamed to `_«name»_`
#     8-Jul-2013 (CT) Derive `_RAW_DESC_` from `object`, not `property`
#    19-Jul-2013 (CT) Derive `Raw_Attr_Query` from `Attr_Query`;
#                     set `Q_Exp.Base.RAW` to `Raw_Attr_Query ()`;
#                     remove `_RAW_` and `_RAW_DESC_` (nice simplification)
#    30-Aug-2013 (CT) Remove `SET`
#     4-Apr-2014 (CT) Use `TFL.Q_Exp.Base`, not `TFL.Attr_Query ()`
#    26-Aug-2014 (CT) Change `_Get_Raw_._getter` to allow composite `key`
#     9-Sep-2014 (CT) Rename from `MOM.Q_Exp_Raw` to `MOM.Q_Exp`
#     9-Sep-2014 (CT) Redefine `Base`, `_Get_`;
#                     add `_Get_._E_Type_Restriction_`, `_Get_.RAW`
#    11-Sep-2014 (CT) Add `_E_Type_Restriction_.__getitem__`; add doctest
#    ««revision-date»»···
#--

from   __future__               import unicode_literals

from   _MOM                     import MOM
from   _TFL                     import TFL
from   _TFL.pyk                 import pyk

from   _TFL._Meta.Once_Property import Once_Property
from   _TFL.predicate           import rsplit_hst

import _TFL.Decorator
import _TFL.Q_Exp

class _MOM_Base_ (TFL.Q_Exp.Base) :
    """Query generator supporting TFL.Q query expressions plus RAW queries
       and queries with type restrictions.

    >>> Q.RAW.foo.bar.qux
    Q.RAW.foo.bar.qux

    >>> Q.foo.RAW.bar.qux
    Q.RAW.foo.bar.qux

    >>> Q.foo.bar.RAW.qux
    Q.RAW.foo.bar.qux

    >>> Q.foo.bar.qux.RAW
    Q.RAW.foo.bar.qux

    >>> Q.my_node.manager ["PAP.Person"]
    Q.my_node.manager ["PAP.Person"]

    >>> q1 = Q.OR (Q.my_node.manager, Q.my_node.owner) ["PAP.Person"]
    >>> q2 = Q.my_node.OR (Q.manager, Q.owner) [Q.PAP.Person]

    >>> q1
    <_OR_ [Q.my_node.manager ["PAP.Person"], Q.my_node.owner ["PAP.Person"]]>

    >>> q2
    <_OR_ [Q.my_node.manager ["PAP.Person"], Q.my_node.owner ["PAP.Person"]]>

    >>> qh = Q.my_node.OR (Q.manager, Q.owner)
    >>> qh
    <_OR_ [Q.my_node.manager, Q.my_node.owner]>

    >>> qh.OR (Q [Q.PAP.Person], Q [Q.PAP.Company])
    <_OR_ [Q.my_node.manager ["PAP.Person"], Q.my_node.owner ["PAP.Person"], Q.my_node.manager ["PAP.Company"], Q.my_node.owner ["PAP.Company"]]>

    >>> q3 = Q.my_node.manager.OR (Q ["PAP.Association"], Q ["PAP.Company"])
    >>> q3
    <_OR_ [Q.my_node.manager ["PAP.Association"], Q.my_node.manager ["PAP.Company"]]>

    >>> q3 == 23
    <Filter_Or [Q.my_node.manager ["PAP.Association"] == 23, Q.my_node.manager ["PAP.Company"] == 23]>

    >>> q3.name == "ISAF"
    <Filter_Or [Q.my_node.manager ["PAP.Association"].name == ISAF, Q.my_node.manager ["PAP.Company"].name == ISAF]>

    >>> Q.manager [Q.PAP.Company].owner [Q.PAP.Person]
    Q.manager ["PAP.Company"].owner ["PAP.Person"]

    """

    _real_name       = "Base"

Base = _MOM_Base_ # end class

Q = Base (Ignore_Exception = AttributeError)

@TFL.Override_Method (Base)
class _MOM_Get_ (Base._Get_) :
    """Query getter with support for E_Type restriction"""

    _real_name       = "_Get_"

    @property
    def RAW (self) :
        """Get raw value for attribute specified by getter `self`."""
        prefix, _, postfix = rsplit_hst (self._name, ".")
        Q = self.Q
        return Q.RAW._Get_Raw_ (Q, prefix = prefix, postfix = postfix)
    # end def RAW

    def __getitem__ (self, type_name) :
        """Restrict result of getter `self` to instances of E_Type with name
           `type_name`.
        """
        return self._E_Type_Restriction_ (self, type_name)
    # end def __getitem__

_Get_ = _MOM_Get_ # end class

@TFL.Add_Method (_Get_)
class _E_Type_Restriction_ (TFL.Q_Exp._Get_) :

    def __init__ (self, head_getter, type_name, tail_getter = None) :
        self.Q            = head_getter.Q
        self._head_getter = head_getter
        self._tail_getter = tail_getter
        if isinstance (type_name, _Get_) :
            type_name = type_name._name
        self._type_name   = type_name
    # end def __init__

    def predicate (self, obj) :
        Q  = self.Q
        tg = self._tail_getter
        try :
            result   = self._head_getter (obj)
            app_type = obj.E_Type.app_type
            E_Type   = app_type.entity_type (self._type_name)
            if E_Type is None :
                raise TypeError \
                    ( "App-type %s doesn't have E-Type with name %s"
                    % (app_type, type_name)
                    )
        except Q.Ignore_Exception as exc :
            result = Q.undef
        else :
            if isinstance (result, E_Type) :
                if tg is not None :
                    result = tg (result)
            elif isinstance (result, pyk.string_types + (dict, )) :
                result = Q.undef
            else :
                try :
                    _ = iter (result)
                except TypeError :
                    result = Q.undef
                else :
                    result = result.__class__ \
                        (v for v in result if isinstance (v, E_Type))
                    if tg is not None :
                        result = result.__class__ (tg (r) for r in result)
        return result
    # end def predicate

    def __getattr__ (self, name) :
        tg = self._tail_getter
        return self.__class__ \
            ( self._head_getter
            , self._type_name
            , getattr (tg if tg is not None else self.Q, name)
            )
    # end def __getattr__

    def __getitem__ (self, type_name) :
        return self.__class__ (self, type_name)
    # end def __getitem__

    def __repr__ (self) :
        result = """%r ["%s"]""" % (self._head_getter, self._type_name)
        tg     = self._tail_getter
        if tg is not None :
            result += repr (tg) [1:] ### skip leading `Q`
        return result
    # end def __repr__

# end class _E_Type_Restriction_

class Raw_Attr_Query (Base) :
    """Syntactic sugar for creating Filter objects based on raw attribute
       queries.
    """

    def __getattr__ (self, name) :
        return self._Get_Raw_ (self, name)
    # end def __getattr__

# end class Raw_Attr_Query

Base.RAW = Raw_Attr_Query ()

@TFL.Add_New_Method (Raw_Attr_Query)
class _Get_Raw_ (TFL.Q_Exp._Get_) :
    """Query getter for raw values."""

    def __init__ (self, Q, postfix, prefix = "") :
        self.Q        = Q
        self._postfix = postfix
        self._prefix  = prefix
    # end def __init__

    def _getter (self, obj) :
        if self._prefix :
            obj = getattr (TFL.Getter, self._prefix) (obj)
        key = self._postfix
        if hasattr (obj, "raw_attr") and key in obj.attributes :
            return obj.raw_attr (key)
        else :
            getter = getattr (TFL.Getter, key)
            result = getter  (obj)
            if isinstance (obj, MOM.Entity) :
                result = unicode (result)
            return result
    # end def _getter

    @Once_Property
    def _name (self) :
        if self._prefix :
            return ".".join ((self._prefix, self._postfix))
        return self._postfix
    # end def _name

    def __getattr__ (self, name) :
        return self.__class__ (self.Q, name, self._name)
    # end def __getattr__

    def __repr__ (self) :
        return "Q.RAW.%s" % (self._name, )
    # end def __repr__

# end class _Get_Raw_

if __name__ != "__main__" :
    MOM._Export ("Q")
    MOM._Export_Module ()
### __END__ MOM.Q_Exp
