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
#    GTW.Form.MOM.Inline_Description
#
# Purpose
#    Description of the behaviour of an inline editing
#
# Revision Dates
#    19-Jan-2010 (MG) Creation
#     2-Feb-2010 (MG) Default widget media definition added
#                     Once property `Media` added
#    02-Feb-2010 (MG) Location of JS and CSS files changed
#     3-Feb-2010 (MG) `Media` property moved into `Inline`
#     3-Feb-2010 (MG) Made `own_role_name`  optional
#    ««revision-date»»···
#--

from   _TFL                                 import TFL
import _TFL._Meta.Object

from   _GTW                                 import GTW
import _GTW.Media
import _GTW._Form.Widget_Spec
import _GTW._Form._MOM.Inline
import _GTW._Form._MOM.Inline_Instance

class Inline_Description (TFL.Meta.Object) :
    """A Inline_Description `form` inside a real form."""

    widget = GTW.Form.Widget_Spec \
        ( "html/form.jnj, inline_table"
        , Media = GTW.Media
              ( css_links   =
                  ( GTW.CSS_Link ("/media/styles/GTW/jquery-ui-1.7.2.custom.css")
                  , GTW.CSS_Link ("/media/styles/GTW/m2m.css")
                  )
              , scripts     =
                  ( GTW.Script (src  = "http://www.google.com/jsapi")
                  , GTW.Script (body = 'google.load ("jquery", "1");')
          ##        , GTW.Script (body = 'google.load ("jquery", "1", {uncompressed:true});')
                  , GTW.Script (body = 'google.load ("jqueryui", "1");')
                  , GTW.Script (src  = "GTW/model_edit_ui.js") ## XXX
                  )
              , js_on_ready =
                  ( GTW.JS_On_Ready
                        ( '$(".m2m-inline-form-table").many2many ();'
                        , 100
                        )
                  ,
                  )
            )
        )
    css_class    = "inline-object"

    completer    = None
    max_count    = 256 ### seems to be more than enough for a web-app
                       ### and sys.maxint on a 64 bit is machine way to much
    min_count    = 1
    min_empty    = 0
    min_required = 0

    def __init__ (self, et_man, * field_group_descriptions, ** kw) :
        self.e_type_name              = getattr (et_man, "type_name", et_man)
        self.own_role_name            = kw.pop ("own_role_name", None)
        self.field_group_descriptions = field_group_descriptions
        self.__dict__.update (kw)
    # end def __init__

    def __call__ (self, et_man, added_fields, ** kw) :
        scope             = et_man.home_scope
        link_et_man       = getattr (scope, self.e_type_name)
        if not self.own_role_name :
            roles = tuple (et_man.link_map [link_et_man._etype])
            if len (roles) > 1 :
                raise TypeError ("More thanb one role to chhose from ?")
            self.own_role_name = roles [0].role_name
        inline_form       = GTW.Form.MOM.Inline_Instance.New \
            ( link_et_man
            , * self.field_group_descriptions
            , suffix      = et_man.type_base_name
            )
        return (GTW.Form.MOM.Inline (self, inline_form), )
    # end def __call__

# end class Inline_Description

if __name__ != "__main__" :
    GTW.Form.MOM._Export ("*")
### __END__ GTW.Form.MOM.Inline_Description
