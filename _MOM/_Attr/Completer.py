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
#    ««revision-date»»···
#--

from   __future__            import absolute_import, division
from   __future__            import print_function, unicode_literals

from   _MOM                  import MOM
from   _TFL                  import TFL

from   _TFL.predicate        import uniq

import _MOM._Attr

import _TFL._Meta.Object

class _ACI_ (TFL.Meta.Object) :
    """Root class for attribute completer instances."""

    dependents = ()

    def __init__ (self, acs, attr, E_Type) :
        self.name = attr.name
    # end def __init__

    @TFL.Meta.Once_Property
    def names (self) :
        return tuple (uniq ((self.name, ) + self.dependents))
    # end def names

# end class _ACI_

class _ACI_E_ (_ACI_) :
    """Attribute completer instance for an `Entity_Completer`."""

    def __init__ (self, acs, attr, E_Type) :
        self.__super.__init__ (acs, attr, E_Type)
        self.selection_treshold = acs.selection_treshold
        self.filter_treshold    = acs.filter_treshold
    # end def __init__

# end class _ACI_E_

class _ACI_F_ (_ACI_) :
    """Attribute completer instance for a `Field_Completer`."""

    def __init__ (self, acs, attr, E_Type) :
        self.__super.__init__ (acs, attr, E_Type)
        self.treshold = acs.treshold
        if acs.dependents :
            self.dependents = acs.dependents (E_Type).names
    # end def __init__

# end class _ACI_F_

class _Completer_ (TFL.Meta.Object) :
    """Root class for attribute completers"""

    def __call__ (self, attr, E_Type) :
        return self.Type (self, attr, E_Type)
    # end def __call__

# end class _Completer_

class Entity_Completer (_Completer_) :
    """Model an entity completer for a MOM attribute."""

    selection_treshold = 1
    Type               = _ACI_E_

    def __init__ (self, selection_treshold = None, filter_treshold = None) :
        if selection_treshold is not None :
            self.selection_treshold = selection_treshold
        self.filter_treshold    = \
            (    filter_treshold if filter_treshold is not None
            else self.selection_treshold
            )
        assert self.filter_treshold <= self.selection_treshold
    # end def __init__

# end class Entity_Completer

class Field_Completer (_Completer_) :
    """Model a field completer for a MOM attribute."""

    dependents = ()
    treshold   = 1
    Type       = _ACI_F_

    def __init__ (self, treshold = None, dependents = None) :
        if treshold is not None :
            self.treshold = treshold
        if dependents is not None :
            self.dependents = dependents
    # end def __init__

# end class Field_Completer

if __name__ != "__main__" :
    MOM.Attr._Export ("*")
### __END__ MOM.Attr.Completer
