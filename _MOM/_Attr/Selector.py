# -*- coding: iso-8859-15 -*-
# Copyright (C) 2011 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# #*** <License> ************************************************************#
# This module is part of the package MOM.Attr.
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
#    MOM.Attr.Selector
#
# Purpose
#    Selector for a group of attributes of an essential Entity
#
# Revision Dates
#     5-Jul-2011 (CT) Creation
#    ««revision-date»»···
#--

from   __future__            import absolute_import, division
from   __future__            import print_function, unicode_literals

from   _MOM                  import MOM
from   _TFL                  import TFL

from   _TFL.predicate        import uniq

import _MOM._Attr

import _TFL._Meta.Object
import _TFL._Meta.Once_Property

import itertools

class _Selection_ (TFL.Meta.Object) :
    """Base class for attribute selections."""

    def __init__ (self, E_Type) :
        self.E_Type = E_Type
    # end def __init__

    @TFL.Meta.Once_Property
    def attr_set (self) :
        return set (self.attrs)
    # end def attr_set

    @TFL.Meta.Once_Property
    def names (self) :
        return tuple (a.name for a in self.attrs)
    # end def names

    def __contains__ (self, item) :
        return item in self.attr_set
    # end def __contains__

    def __iter__ (self) :
        return iter (self.attrs)
    # end def __iter__

# end class _Selection_

class _Combo_Selection_ (_Selection_) :
    """Attribute selection assembled from `include` and `exclude` selectors."""

    exclude = None

    def __init__ (self, spec, E_Type) :
        self.__super.__init__ (E_Type)
        self.include = spec.include (E_Type)
        if spec.exclude is not None :
            self.exclude = spec.exclude (E_Type)
    # end def __init__

    @TFL.Meta.Once_Property
    def attrs (self) :
        exclude = self.exclude
        result  = self.include.attrs
        if exclude is not None :
            result = (a for a in result if a not in exclude)
        return tuple (result)
    # end def attrs

# end class _Combo_Selection_

class _Kind_Selection_ (_Selection_) :
    """Attribute selection for a specific kind of attributes."""

    def __init__ (self, spec, E_Type) :
        self.__super.__init__ (E_Type)
        self.kind = spec.kind
    # end def __init__

    @TFL.Meta.Once_Property
    def attrs (self) :
        return tuple (getattr (self.E_Type, self.kind))
    # end def attrs

# end class _Kind_Selection_

class _List_Selection_ (_Selection_) :
    """Attribute selection combined from a list of selectors."""

    def __init__ (self, spec, E_Type) :
        self.__super.__init__ (E_Type)
        self.sels = tuple (s (E_Type) for s in spec.sels)
    # end def __init__

    @TFL.Meta.Once_Property
    def attrs (self) :
        return tuple (uniq (itertools.chain (* (s.attrs for s in self.sels))))
    # end def attrs

# end class _List_Selection_

class _Name_Selection_ (_Selection_) :
    """Attribute selection specifed by a list of names."""

    def __init__ (self, spec, E_Type) :
        self.__super.__init__ (E_Type)
        self._names = tuple (spec.names)
    # end def __init__

    @TFL.Meta.Once_Property
    def attrs (self) :
        return tuple (getattr (self.E_Type, n) for n in self.names)
    # end def attrs

    @property
    def names (self) :
        return self._names
    # end def names

# end class _Name_Selection_

class _Pred_Selection_ (_Selection_) :
    """Attribute selection specifed by a predicate."""

    def __init__ (self, spec, E_Type) :
        self.__super.__init__ (E_Type)
        self.kind = spec.kind
        self.pred = spec.pred
    # end def __init__

    @TFL.Meta.Once_Property
    def attrs (self) :
        pred = self.pred
        return tuple (a for a in getattr (self.E_Type, self.kind) if pred (a))
    # end def attrs

    def __contains__ (self, item) :
        return bool (self.pred (item))
    # end def __contains__

# end class _Pred_Selection_

class _Selector_ (TFL.Meta.Object) :
    """Base class for attributes selectors."""

    def __call__ (self, E_Type) :
        return self.Type (self, E_Type)
    # end def __call__

# end class _Selector_

class Combo (_Selector_) :
    """Selector for a set of attributes assembled from `include` and
       `exclude` selectors.
    """

    Type = _Combo_Selection_

    def __init__ (self, include, exclude = None) :
        self.include = include
        self.exclude = exclude
    # end def __init__

# end class Combo

class Kind (_Selector_) :
    """Selector for a specific kind of attributes."""

    Type = _Kind_Selection_

    def __init__ (self, kind) :
        self.kind = kind
    # end def __init__

# end class Kind

class List (_Selector_) :
    """Selector combined from a list of selectors."""

    Type = _List_Selection_

    def __init__ (self, * sels) :
        assert sels
        self.sels = sels
    # end def __init__

# end class List

class Name (_Selector_) :
    """Selector for a group of attributes specifed by a list of names."""

    Type = _Name_Selection_

    def __init__ (self, * names) :
        assert names
        self.names = names
    # end def __init__

# end class Name

class Pred (_Selector_) :
    """Selector for attributes satisfying a predicate."""

    Type = _Pred_Selection_

    def __init__ (self, pred, kind = "user_attr") :
        self.pred = pred
        self.kind = kind
    # end def __init__

# end class Pred

class Not_Pred (Pred) :
    """Selector for attributes not satisfying a predicate."""

    def __init__ (self, pred, kind = "user_attr") :
        self.__super.__init__ ((lambda x : not pred (x)), kind)
    # end def __init__

# end class Not_Pred

necessary   = Kind ("necessary")
optional    = Kind ("optional")
primary     = Kind ("primary")
required    = Kind ("required")
user        = Kind ("user_attr")

P_optional  = Not_Pred ((lambda x : x.is_required), "user_attr")
P_required  = Pred     ((lambda x : x.is_required), "user_attr")

if __name__ != "__main__" :
    MOM.Attr._Export_Module ()
### __END__ MOM.Attr.Selector
