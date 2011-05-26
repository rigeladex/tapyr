# -*- coding: iso-8859-15 -*-
# Copyright (C) 2009-2010 Martin Glueck All rights reserved
# Langstrasse 4, A--2244 Spannberg, Austria. martin@mangari.org
# ****************************************************************************
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Library General Public
# License as published by the Free Software Foundation; either
# version 2 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Library General Public License for more details.
#
# You should have received a copy of the GNU Library General Public
# License along with this library; if not, write to the Free
# Software Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
# ****************************************************************************
#
#++
# Name
#    GTW.Form.Field_Group_Description
#
# Purpose
#    Abstract definition of a field group
#
# Revision Dates
#    18-Jan-2010 (MG) Creation
#    29-Jan-2010 (MG) Pass `field_group_description` to `field_group`
#     2-Feb-2010 (MG) Use `GTW.Form.Widget_Spec`
#     2-Feb-2010 (MG) Once property `Media` added
#     5-Feb-2010 (MG) Convert `widget` to `Widget_Spec`
#    15-Apr-2010 (MG) `Media` moved to `GTW.Form.Field_Group`
#     3-May-2010 (MG) New form handling implemented
#     6-May-2010 (MG) `widget` replace by `render_mode_description`
#    29-Jun-2010 (MG) Legacy `widget` re-added
#    ««revision-date»»···
#--

from   _TFL               import TFL
import _TFL._Meta.Object
import _TFL._Meta.Once_Property

from   _GTW               import GTW
import _GTW._Form.Render_Mode_Description
import _GTW._Form.Field_Group

class _Form_Field_Group_Description_ (TFL.Meta.Object) :
    """Abstract definition of a field group."""

    _real_name              = "Field_Group_Description"
    completer               = None
    media                   = None

    default_render_mode     = "div_seq"
    render_mode_description = GTW.Form.Render_Mode_Description \
        (div_seq = GTW.Form.Widget_Spec ("html/form.jnj, fg_div_seq"))
    widget                  = render_mode_description ["div_seq"]

    def __init__ (self, * fields, ** kw) :
        self.fields = fields
        self.__dict__.update (kw)
    # end def __init__

    def prepare_request_data (self, form, request_data) :
        pass
    # end def prepare_request_data

    def update_object (self, form) :
        pass
    # end def update_object

    def update_raw_attr_dict (self, form) :
        pass
    # end def update_raw_attr_dict

    def __call__ (self) :
        return (GTW.Form.Field_Group (self.fields, self), )
    # end def __call__

Field_Group_Description = _Form_Field_Group_Description_ # end class Field_Group_Description

if __name__ != "__main__" :
    GTW.Form._Export ("*")
### __END__ GTW.Form.Field_Group_Description
