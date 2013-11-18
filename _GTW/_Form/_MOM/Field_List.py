# -*- coding: utf-8 -*-
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
#    GTW.Form.MOM.Field_List
#
# Purpose
#    Handling of field specification for forms
#
# Revision Dates
#    28-May-2010 (MG) Creation
#    01-Jun-2010 (MG) Handling of `role_name` added
#     2-Jun-2010 (CT) `prefixed` added to `Wildcard_Field.__call__`
#    24-Jul-2010 (MG) `Wildcard_Field.`exclude` added
#     4-Aug-2010 (MG) `exclude` added to `Field_List.both_runs`
#    ««revision-date»»···
#--

from   _TFL                import TFL
from   _GTW                import GTW
import _GTW._Form._MOM
import _TFL._Meta.Object

import  itertools

class Wildcard_Field (TFL.Meta.Object) :
    """A place holder in the field group description which will expand to
       all attributes of the given kinds which have not been added explicitly.
    """

    def __init__ (self, * kinds , ** kw) :
        self.kinds   = kinds or ("primary", "user_attr")
        self.prefix  = kw.pop ("prefix", None)
        self.exclude = kw.pop ("exclude", set ())
        assert not kw, sorted (kw.keys ())
    # end def __init__

    def __call__ (self, first_pass, et_man, added_fields) :
        if first_pass :
            ### the wildcard file can only evalue which fields have to be
            ### added after all other fields have been precessed in the first
            ### pass
            return (self, )
        added_fields.update (self.exclude)
        prefixed = lambda x : x
        if self.prefix :
            et_man   = getattr (et_man, self.prefix).role_type
            prefixed = lambda x : ".".join ((self.prefix, x))
        etype  = getattr (et_man, "_etype", et_man)
        result = []
        for ak in sorted \
               ( itertools.chain (* (getattr (etype, k) for k in self.kinds))
               , key = lambda ak : ak.rank
               ) :
            name      = ak.name
            role_name = getattr (ak, "role_name", name)
            if (name not in added_fields) and (role_name not in added_fields) :
                result.append (prefixed (name))
        return result
    # end def __call__

# end class Wildcard_Field

class Field_Prefixer (TFL.Meta.Object) :
    """Add a common prefix to all fields."""

    def __init__ (self, prefix, * fields, ** kw) :
        self.prefix = prefix
        self.fields = fields
        self.joiner = kw.pop ("joiner", ".")
    # end def __init__

    def __call__ (self, first_pass, et_man, added_fields) :
        ### the first_pass can be igbore because the `Field_Prefixer`
        ### replaces itself with the field names and therefore will not be
        ### called in the second pass anymore
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

class Field_List (TFL.Meta.Object) :
    """List of fields for forms in various contexts which support wildcards,
       prefixes, ...
    """

    def __init__ (self, * fields) :
        if not fields :
            fields      = (Wildcard_Field (), )
        self.fields     = fields
        self.first_pass = True
    # end def __init__

    def both_runs (self, et_man, * exclude) :
        added_fields = set (exclude)
        self (et_man, added_fields)
        self (et_man, added_fields)
    # end def both_runs

    def __call__ (self, et_man, added_fields) :
        if added_fields is None :
            added_fields = set ()
        fields           = []
        for f in self.fields :
            if callable (f) :
                new_fields = f  (self.first_pass, et_man, added_fields)
                fields.extend   (new_fields)
            else :
                new_fields =    (str (f), )
                fields.append   (f)
            added_fields.update (new_fields)
        self.fields        = fields
        self.first_pass    = False
        return fields
    # end def __call__

    def __nonzero__ (self) :
        return len (self.fields)
    # end def __nonzero__

    def __iter__ (self) :
        return iter (self.fields)
    # end def __iter__

# end class Field_List

if __name__ != "__main__" :
    GTW.Form.MOM._Export ("*")
### __END__ GTW.Form.MOM.Field_List


