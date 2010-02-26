# -*- coding: iso-8859-1 -*-
# Copyright (C) 2010 Martin Glueck All rights reserved
# Langstrasse 4, A--2244 Spannberg, Austria. martin@mangari.org
# ****************************************************************************
# This module is part of the package GTW.Form.MOM.
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
# ****************************************************************************
#
#++
# Name
#    GTW.Form.MOM.Field_Group_Description
#
# Purpose
#    Field group description for MOM objects
#
# Revision Dates
#    18-Jan-2010 (MG) Creation
#    29-Jan-2010 (CT) `kw` added to `Field_Group_Description.__init__`
#    29-Jan-2010 (MG) Pass `field_group_description` to `field_group`
#     3-Feb-2010 (MG) Return `None` if no field are left for this a group
#     3-Feb-2010 (MG) Allow callables in field list fo `Field_Prefixer`, `
#                     Role_Description` added
#     3-Feb-2010 (MG) Set the `completes` attribute on completer objects
#     4-Feb-2010 (MG) `Role_Description` removed again
#     8-Feb-2010 (MG) Directly access the `_etype` of the `et_man` (An_Entity
#                     etype managers work differently)
#    18-Feb-2010 (MG) `Field.choices` added
#    24-Feb-2010 (MG) `Field_Group_Description.__call__` changed to use an
#                     `Wildcard_Field` if the user has not supplied a field
#                     spec
#    25-Feb-2010 (CT) `Field` moved into a module of its own
#    ««revision-date»»···
#--

from   _TFL                                 import TFL
import _TFL._Meta.Object

from   _MOM                                 import MOM
import _MOM.Link

from   _GTW                                 import GTW
import _GTW._Form.Field_Group
import _GTW._Form.Field_Group_Description
import _GTW._Form._MOM
from   _GTW._Form._MOM.Field                import Field

import  itertools

class Wildcard_Field (TFL.Meta.Object) :
    """A place holder in the field group description which will expand to
       all attributes of the given kinds which have not been added before the
       wildcard.
    """

    def __init__ (self, * kinds , ** kw) :
        self.kinds  = kinds or ("primary", "user_attr")
        self.prefix = kw.pop ("prefix", None)
        assert not kw, sorted (kw.keys ())
    # end def __init__

    def __call__ (self, et_man, added_fields) :
        prefix = ""
        if self.prefix :
            et_man = getattr (et_man, self.prefix).role_type
            prefix = self.prefix + "."
        etype  = et_man._etype
        return \
            [   "%s%s" % (prefix, ak.name)
            for ak in sorted
               ( itertools.chain (* (getattr (etype, k) for k in self.kinds))
               , key = lambda ak : ak.rank
               )
            if ak.name not in added_fields
            ]
    # end def __call__

# end class Wildcard_Field

class Field_Prefixer (TFL.Meta.Object) :
    """Add a common prefix to all fields."""

    def __init__ (self, prefix, * fields, ** kw) :
        self.prefix = prefix
        self.fields = fields
        self.joiner = kw.pop ("joiner", ".")
    # end def __init__

    def __call__ (self, et_man, added_fields) :
        result = []
        join   = self.joiner.join
        for field in self.fields :
            if callable (field) :
                result.extend \
                    (   join ((self.prefix, f))
                    for f in field (et_man, added_fields)
                    )
            else :
                result.append (self.joiner.join ((self.prefix, field)))
        return result
    # end def __call__

# end class Field_Prefixer

class _MOM_Field_Group_Description_ (GTW.Form.Field_Group_Description) :
    """A field group description for an MOM object"""

    _real_name = "Field_Group_Description"
    widget     = GTW.Form.Widget_Spec \
        ( GTW.Form.Field_Group_Description.widget
        , inline_table_th   = "html/form.jnj, inline_table_th"
        , inline_table_td   = "html/form.jnj, inline_table_td"
        )

    def __call__ (self, et_man, added_fields = None, * args, ** kw) :
        if not self.fields :
            self.fields = (Wildcard_Field (), )
        if added_fields is None :
            added_fields = set ()
        fields_spec = self.fields
        fields      = []
        for f in fields_spec :
            if callable (f) :
                new_fields = f  (et_man, added_fields)
                fields.extend   (new_fields)
            else :
                new_fields =    (str (f), )
                fields.append   (f)
            added_fields.update (new_fields)
        if 1 or fields :
            return \
                ( GTW.Form.Field_Group
                    ([Field (et_man, name) for name in fields], self)
                ,
                )
        return (None, )
    # end def __call__

Field_Group_Description = _MOM_Field_Group_Description_ # end class

if __name__ != "__main__" :
    GTW.Form.MOM._Export ("*")
### __END__ GTW.Form.MOM.Field_Group_Description
