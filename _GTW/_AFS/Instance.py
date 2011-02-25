# -*- coding: iso-8859-1 -*-
# Copyright (C) 2011 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# #*** <License> ************************************************************#
# This module is part of the package GTW.AFS.
#
# This module is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This module is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this module. If not, see <http://www.gnu.org/licenses/>.
# #*** </License> ***********************************************************#
#
#++
# Name
#    GTW.AFS.Instance
#
# Purpose
#    Model a AFS form instance plus the data for the form's entities and fields
#
# Revision Dates
#    25-Feb-2011 (CT) Creation
#    ««revision-date»»···
#--

from   _GTW                     import GTW
from   _TFL                     import TFL

import _GTW._AFS

import _TFL._Meta.Object
from   _TFL._Meta.Once_Property import Once_Property

import json

class Element (TFL.Meta.Object) :
    """Model a AFS form element plus it's data."""

    def __init__ (self, elem, data) :
        self.elem = elem
        self.data = data
    # end def __init__

    def __iter__ (self) :
        data = self.data
        for c in self.elem.children :
            yield Element (c, data [c.id])
    # end def __iter__

    if 0 :
        ### alternate implementation
        def __init__ (self, elem, data, top = None) :
            self.elem = elem
            self.data = data
            self.top  = top or self
        # end def __init__

        def __iter__ (self) :
            data = self.data
            elem = self.elem
            top  = self.top
            for id in data.get ("child_ids", ()) :
                yield Element (top.elem [id], data [id], top)
        # end def __iter__

    def transitive_iter (self) :
        yield self
        for c in self :
            for x in c.transitive_iter () :
                yield x
    # end def transitive_iter

# end class Element

class Form (Element) :
    """Model a AFS form instance plus the data for the form's entities and
       fields.
    """

    @Once_Property
    def as_js (self) :
        return "new $GTW.AFS.Form (%s, %s)" % \
            (self.elem.as_json, json.dumps (self.data))
    # end def as_js

# end class Form

if __name__ != "__main__" :
    GTW.AFS._Export_Module ()
### __END__ GTW.AFS.Instance
