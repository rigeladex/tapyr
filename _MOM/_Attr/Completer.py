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
#    ««revision-date»»···
#--

from   __future__            import absolute_import, division
from   __future__            import print_function, unicode_literals

from   _MOM                  import MOM
from   _TFL                  import TFL

import _MOM._Attr

import _TFL._Meta.Object

class _Completer_ (TFL.Meta.Object) :
    """Root class for attribute completers"""

# end class _Completer_

class Entity_Completer (_Completer_) :
    """Model an entity completer for a MOM attribute."""

    selection_treshold = 1

    def __init__ (self, selection_treshold = None, filter_treshold = None) :
        if selection_treshold is not None :
            self.selection_treshold = selection_treshold
        self.filter_treshold    =
            (    filter_treshold if filter_treshold is not None
            else self.selection_treshold
            )
    # end def __init__

# end class Entity_Completer

class Field_Completer (_Completer_) :
    """Model a field completer for a MOM attribute."""

    exclude  = ()
    include  = ()
    treshold = 1

    def __init__ (self, treshold = None, include = None, exclude = None) :
        if treshold is not None :
            self.treshold = treshold
        if include is not None :
            self.include  = include
        if exclude is not None :
            self.exclude  = exclude
    # end def __init__

# end class Field_Completer

if __name__ != "__main__" :
    MOM.Attr._Export ("*")
### __END__ MOM.Attr.Completer
