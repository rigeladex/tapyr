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
#    ««revision-date»»···
#--

from   __future__            import absolute_import, division
from   __future__            import print_function, unicode_literals

from   _MOM                  import MOM
from   _TFL                  import TFL

from   _TFL.predicate        import uniq

import _MOM._Attr

import _TFL._Meta.Object

class Completer (TFL.Meta.Object) :
    """Attribute completer instance for a specific E_Type."""

    buddies    = ()
    dependents = ()

    def __init__ (self, acs, attr, E_Type) :
        self.name     = attr.name
        self.etn      = E_Type.type_name
        self.treshold = acs.treshold
        if acs.buddies :
            self.buddies = acs.buddies (E_Type).names
        if acs.dependents :
            self.dependents = acs.dependents (E_Type).names
    # end def __init__

    def __call__ (self, scope, val_dict) :
        ETM    = scope [self.etn]
        vd     = dict  ((k, v) for k, v in val_dict.iteritems () if v != "")
        fs     = tuple (ETM.ac_query_attrs (self.names, vd))
        if fs :
            return ETM.query (* fs).distinct ()
        return TFL.Q_Result (())
    # end def __call__

    @property
    def as_json_cargo (self) :
        return dict \
            ( names    = list (self.names)
            , treshold = self.treshold
            )
    # end def as_json_cargo

    @TFL.Meta.Once_Property
    def names (self) :
        return tuple (uniq ((self.name, ) + self.buddies))
    # end def names

    @TFL.Meta.Once_Property
    def all_names (self) :
        return tuple (uniq (self.names + self.dependents))
    # end def all_names

# end class Completer

class Completer_Spec (TFL.Meta.Object) :
    """Attribute completer specification for a MOM attribute."""

    buddies    = ()
    dependents = ()
    treshold   = 1
    Type       = Completer

    def __init__ (self, treshold = None, buddies = (), dependents = None) :
        if treshold is not None :
            self.treshold = treshold
        if buddies is not None :
            self.buddies = buddies
        if dependents is not None :
            self.dependents = dependents
    # end def __init__

    def __call__ (self, attr, E_Type) :
        return self.Type (self, attr, E_Type)
    # end def __call__

# end class Completer_Spec

if __name__ != "__main__" :
    MOM.Attr._Export ("*")
### __END__ MOM.Attr.Completer
