# -*- coding: utf-8 -*-
# Copyright (C) 2011-2013 Mag. Christian Tanzer All rights reserved
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
#    MOM.Attr.Completer
#
# Purpose
#    Model field and entity completers for MOM attributes
#
# Revision Dates
#     5-Jul-2011 (CT) Creation
#     6-Jul-2011 (CT) Creation continued
#    17-Jul-2011 (CT) Creation continued.. (major surgery)
#    22-Jul-2011 (CT) `__call__` changed to use `E_Type.ac_query_attrs`
#                     instead of `attr_completion`
#    22-Jul-2011 (CT) `all_names` added
#    27-Jul-2011 (CT) `entity_p` added
#    15-Sep-2011 (CT) `Completer.__init__` changed to save `spec`
#    20-Sep-2011 (CT) `all_names` and `dependents` removed
#    20-Sep-2011 (CT) `C_Completer` and `E_Completer` (plus their `_Spec`) added
#     7-Nov-2011 (CT) Change `Completer.__call__` to query results for
#                     `treshold == 0` without `fs`
#    13-Dec-2012 (CT) Add arguments `ETM_R`, `AQ` to `Completer.__call__`
#    25-Apr-2013 (CT) Add optional arg `xtra_filter` to `Completer.__call__`
#    ««revision-date»»···
#--

from   __future__            import absolute_import, division
from   __future__            import print_function, unicode_literals

from   _MOM                  import MOM
from   _TFL                  import TFL

from   _TFL.predicate        import uniq

import _MOM._Attr.Selector

import _TFL._Meta.Object

class Completer (TFL.Meta.Object) :
    """Attribute completer instance for a specific E_Type."""

    buddies    = ()
    embedded_p = False

    def __init__ (self, acs, attr, E_Type) :
        self.etn      = E_Type.type_name
        self.name     = name = attr.name
        self.spec     = acs
        self.treshold = acs.treshold
        if acs.buddies :
            self.buddies = acs.buddies (E_Type, name).names
        self.entity_p = set (self.names) == set (E_Type.epk_sig)
    # end def __init__

    def copy (self) :
        cls    = self.__class__
        result = cls.__new__   (cls)
        result.__dict__.update (self.__dict__)
        return result
    # end def copy

    def __call__ \
            ( self, scope, val_dict
            , ETM_R       = None
            , AQ          = None
            , xtra_filter = None
            ) :
        ETM = scope [self.etn]
        if ETM_R is None :
            ETM_R = ETM
        vd  = dict  ((k, v) for k, v in val_dict.iteritems () if v != "")
        fs  = tuple (ETM.ac_query_attrs (self.names, vd, AQ))
        if fs or self.treshold == 0 :
            q = ETM_R.query_s (* fs)
            if xtra_filter is not None :
                q = q.filter (xtra_filter)
            return q.distinct ()
        return TFL.Q_Result (())
    # end def __call__

    @property
    def as_json_cargo (self) :
        result = dict \
            ( entity_p = self.entity_p
            , names    = list (self.names)
            , treshold = self.treshold
            )
        if self.embedded_p :
            result ["embedded_p"] = True
        return result
    # end def as_json_cargo

    @TFL.Meta.Once_Property
    def names (self) :
        return tuple (uniq ((self.name, ) + self.buddies))
    # end def names

    def embedded (self, spec) :
        result = self.copy ()
        result.__dict__.update (spec or {})
        result.embedded_p = True
        return result
    # end def embedded

# end class Completer

class _Nested_Completer_ (Completer) :

    def __init__ (self, acs, attr, E_Type) :
        self.__super.__init__ (acs, attr, E_Type)
        self.nested_specs = acs.nested_specs
        self.nested = []
    # end def __init__

    def derived (self, nested) :
        if nested is not None :
            name   = nested.name
            result = nested.embedded (self.nested_specs.get (name, {}))
            self.nested.append (result)
            return result
    # end def derived

# end class _Nested_Completer_

class C_Completer (_Nested_Completer_) :
    """A_Composite completer instance for a specific E_Type."""

# end class C_Completer

class E_Completer (_Nested_Completer_) :
    """A_Id_Entity completer instance for a specific E_Type."""

# end class E_Completer

class Completer_Spec (TFL.Meta.Object) :
    """Attribute completer specification for a MOM attribute."""

    buddies    = None
    treshold   = 1
    Type       = Completer

    def __init__ (self, treshold = None, buddies = None) :
        if treshold is not None :
            self.treshold = treshold
        if buddies is not None :
            assert isinstance (buddies, MOM.Attr.Selector._Selector_), \
                "Expected Attr.Selector for `buddies`, got `%s`" % (buddies, )
            self.buddies = buddies
    # end def __init__

    def __call__ (self, attr, E_Type) :
        return self.Type (self, attr, E_Type)
    # end def __call__

# end class Completer_Spec

class _Nested_Completer_Spec_ (Completer_Spec) :

    def __init__ (self, buddies = None, ** kw) :
        self.__super.__init__ (buddies = buddies)
        self.nested_specs = kw
    # end def __init__

# end class _Nested_Completer_Spec_

class C_Completer_Spec (_Nested_Completer_Spec_) :
    """Attribute completer specification for A_Composite."""

    Type       = C_Completer

# end class C_Completer_Spec

class E_Completer_Spec (_Nested_Completer_Spec_) :
    """Attribute completer specification for A_Id_Entity."""

    Type       = E_Completer

# end class E_Completer_Spec

if __name__ != "__main__" :
    MOM.Attr._Export ("*")
### __END__ MOM.Attr.Completer
