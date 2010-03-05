# -*- coding: iso-8859-1 -*-
# Copyright (C) 2010 Martin Glueck All rights reserved
# Langstrasse 4, A--2244 Spannberg, Austria. martin@mangari.org
# ****************************************************************************
# This module is part of the package GTW.Form.
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
#    GTW.Form._Form_
#
# Purpose
#    Base class for forms
#
# Revision Dates
#    19-Jan-2010 (MG) Creation
#    20-Jan-2010 (MG) `get_id` allow string as parameter as well
#     5-Feb-2010 (MG) `M_Form` added
#    10-Feb-2010 (MG) `prefix_sub` added
#    10-Feb-2010 (MG) `get_raw`: As soon as we have `request_data` use the
#                     values from there or empty string (empty strings are
#                     not part of the request data!)
#    22-Feb-2010 (CT) `kw` added
#    26-Feb-2010 (MG) Javascript handling added
#    26-Feb-2010 (MG) `is_checked` added
#    27-Feb-2010 (MG) `M_Form.__new__` added to introduce `hidden_fields`
#     4-Mar-2010 (MG) `error_code` and `Not_Assigned` added
#     4-Mar-2010 (MG) `Hidden_Fields_List` added and used
#    ««revision-date»»···
#--

from   _TFL               import TFL
import _TFL.I18N
import _TFL._Meta.Object
import _TFL._Meta.Once_Property
import _TFL.defaultdict
import _TFL.Record

from   _GTW              import GTW
import _GTW._Form.Field_Error
import _GTW._Form.Javascript

class Hidden_Fields_List (object) :
    """A kind of list which handles the hidden fields of a form instance to
       support exactly one iteration over the fields
    """

    def __init__ (self, fields) :
        self.fields = fields
    # end def __init__

    def __nonzero__ (self) :
        return bool (self.fields)
    # end def __nonzero__

    def __iter__ (self) :
        fields, self.fields = self.fields, []
        for f in fields :
            yield f
    # end def __iter__

# end class Hidden_Fields_List

class Not_Assigned (object) :
    """Special object which defines `__nonzero__` to support
          instance = self.instance or None
       and expect that `instance` is `None` if self.instance is
       `Not_Assigned`
    """

    def __nonzero__ (self) :
        return False
    # end def __nonzero__

# end class Not_Assigned

class M_Form (TFL.Meta.Object.__class__) :
    """Meta class for forms."""

    parent_form = None

    def __new__ (mcls, name, bases, dct) :
        result = super (M_Form, mcls).__new__ (mcls, name, bases, dct)
        result.hidden_fields = []
        return result
    # end def __new__

    def _setup_fields (cls, field_groups) :
        result = TFL.NO_List ()
        for fg in (  fg for fg in field_groups
                  if isinstance (fg, GTW.Form.Field_Group)
                  ) :
            result.update (fg.fields)
        result.extend (cls.hidden_fields)
        return result
    # end def _setup_fields

    @TFL.Meta.Once_Property
    def Form (cls) :
        return getattr (cls.parent_form, "Form", cls)
    # end def Form

    def form_and_completer (cls, path) :
        form_cls  = cls
        completer = None
        path      = list (path)
        while path :
            sf = path.pop (0)
            if sf in form_cls.sub_forms :
                form_cls      = form_cls.sub_forms [sf]
            else :
                path.insert (0, sf)
                break
        completer = getattr (form_cls, "completer", None)
        while path :
            completer = getattr (completer, path.pop (0), None)
        if completer :
            return form_cls, completer
        return None, None
    # end def form_and_completer

    @TFL.Meta.Once_Property
    def form_path_css (cls) :
        return "__".join (getattr (cls, "form_path", "").split ("/"))
    # end def form_path_css

    @TFL.Meta.Once_Property
    def javascript (cls) :
        if not cls.parent_form :
            return GTW.Form.Javascript.Form (cls)
        return cls.parent_form.javascript
    # end def javascript

# end class M_Form

class _Form_ (TFL.Meta.Object) :
    """Base class for forms"""

    Not_Assigned  = Not_Assigned ()
    prefix        = ""
    __metaclass__ = M_Form
    instance      = Not_Assigned

    def __init__ (self, instance = None, prefix_sub = None, ** kw) :
        if instance != None :
            self.instance  = instance
        self.errors        = GTW.Form.Error_List ()
        self.field_errors  = TFL.defaultdict (GTW.Form.Error_List)
        self.prefix_sub    = prefix_sub
        if prefix_sub :
            self.prefix    = "%s%s" % (self.prefix , prefix_sub)
        self.request_data  = {}
        self.hidden_fields = Hidden_Fields_List (self.hidden_fields)
        self.kw            = TFL.Record (** kw)
    # end def __init__

    @property
    def error_count (self) :
        return len (self.errors) + len (self.field_errors)
    # end def error_count

    def get_errors (self, field = None) :
        if field :
            field = getattr (field, "html_name", field)
            return self.field_errors [field]
        return self.errors
    # end def get_errors

    def get_id (self, field) :
        if isinstance (field, basestring) :
            field = self.fields [field]
        if self.prefix :
            return "-".join ((self.prefix, field.html_name))
        return field.html_name
    # end def get_id

    def get_raw (self, field) :
        if isinstance (field, basestring) :
            field = self.fields [field]
        html_name = self.get_id (field)
        if self.request_data :
            return self.request_data.get (html_name, u"")
        return field.get_raw (self, self.instance)
    # end def get_raw

    def is_checked (self, field) :
        result = dict (value = "yes")
        if isinstance (field, basestring) :
            field = self.fields [field]
        if field.get_cooked (self, self.instance) :
            result ["checked"] = "checked"
        return result
    # end def is_chained

# end class _Form_

if __name__ != "__main__" :
    GTW.Form._Export ("*")
### __END__ GTW.Form._Form_
