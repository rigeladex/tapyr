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
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
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
#     2-Mar-2011 (CT) Creation continued
#    ««revision-date»»···
#--

from   _GTW                     import GTW
from   _TFL                     import TFL

import _GTW._AFS.Element
import _GTW._AFS.Error
from   _GTW._AFS.Instance       import _Base_

import _TFL._Meta.Property
from   _TFL._Meta.Once_Property import Once_Property

from   _TFL.I18N                import _

import json

class Value (_Base_) :
    """Model the value of an AFS form element."""

    anchor_id = None
    init      = ""
    _edit     = None

    def __init__ (self, form, id, json_cargo) :
        self.form     = form
        self.id       = id
        self.jc       = json_cargo
        self.elem     = self._get_elem (form, id)
        self.children = children = []
        self.pop_to_self (json_cargo, "$anchor_id", "init", "edit")
        for c_id in sorted (json_cargo.get ("$child_ids", ())) :
            children.append (self.__class__ (form, c_id, json_cargo [c_id]))
    # end def __init__

    @classmethod
    def from_json (cls, json_data) :
        cargo = json.loads (json_data)
        id    = cargo ["$id"]
        form  = cls._get_elem (GTW.AFS.Element.Form, id)
        return cls (form, id, cargo)
    # end def from_json

    @Once_Property
    def changes (self) :
        return (self.init != self.edit) + sum (c.changes for c in self.children)
    # end def changes

    @property
    def edit (self) :
        return self._edit or self.init
    # end def edit

    @edit.setter
    def edit (self, value) :
        self._edit = value
    # end def edit

    @TFL.Meta.Class_and_Instance_Method
    def _get_elem (soc, form, id) :
        try :
            return form [id]
        except KeyError :
            raise GTW.AFS.Error.Unknown \
                (_ ("Form/element is unknown"), unknown_id = id)
    # end def _get_elem

    def _v_repr (self, v, name) :
        if isinstance (v, dict) :
            result = "%r" % (sorted (v.iteritems ()), )
        else :
            result = "%r" % (v, )
            if result.startswith (("u'", 'u"')) :
                result = result [1:]
        return "%s-v = %s" % (name, result)
    # end def _v_repr

    def __str__ (self) :
        result = [str (self.elem), self._v_repr (self.init, "init")]
        if self.init != self.edit :
            result.append (self._v_repr (self.edit, "edit"))
        result.append (str (self.changes))
        return " ".join (result)
    # end def __str__

# end class Value

if __name__ != "__main__" :
    GTW.AFS._Export ("Value")
### __END__ GTW.AFS.Value
