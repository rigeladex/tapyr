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
#    GTW.AFS.Value
#
# Purpose
#    Model the value of an element of a AFS form
#
# Revision Dates
#     1-Mar-2011 (CT) Creation
#    ««revision-date»»···
#--

from   _GTW                     import GTW
from   _TFL                     import TFL

import _GTW._AFS.Element

import _TFL._Meta.Object
from   _TFL._Meta.Once_Property import Once_Property

import json

class Value (TFL.Meta.Object) :
    """Model the value of an AFS form element."""

    def __init__ (self, form, id, json_cargo) :
        self.form        = form
        self.id          = id
        self.jc          = json_cargo
        self.anchor_id   = json_cargo.get ("$anchor_id")
        self.init = init = json_cargo.get ("init", "")
        self.user        = json_cargo.get ("user", init)
        self.elem        = form [id]
        self.children    = children = []
        for c_id in sorted (json_cargo.get ("$child_ids", ())) :
            children.append (self.__class__ (form, c_id, json_cargo [c_id]))
    # end def __init__

    @classmethod
    def from_json (cls, json_data) :
        cargo = json.loads (json_data)
        id    = cargo ["$id"]
        form  = GTW.AFS.Element.Form [id]
        return cls (form, id, cargo)
    # end def from_json

    @Once_Property
    def changes (self) :
        return (self.init != self.user) + sum (c.changes for c in self.children)
    # end def changes

# end class Value

if __name__ != "__main__" :
    GTW.AFS._Export ("Value")
### __END__ GTW.AFS.Value
