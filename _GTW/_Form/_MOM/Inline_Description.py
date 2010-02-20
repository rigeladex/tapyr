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
#     3-Feb-2010 (MG) Set `parent_et_man` in inline form classes
#     5-Feb-2010 (MG) `Attribute_Inline_Description` and
#                     `Link_Inline_Description` factored
#     5-Feb-2010 (MG) Pass `parent_form` ot sub form creation, set the
#                     completer as attribute of the sub form class
#     8-Feb-2010 (MG) Default widget for `Attribute_Inline_Description` fixed
#     8-Feb-2010 (MG) Directly access the `_etype` of the `et_man` (An_Entity
#                     etype managers work differently)
#    10-Feb-2010 (MG) Link javascript setup moved form `Media` to
#                     `Link_Inline_Description.js_on_ready` to be able to
#                     create link specific code
#    20-Feb-2010 (MG) Locations of javascript and style sheets changed
#    ««revision-date»»···
#--

from   _TFL                                 import TFL
import _TFL._Meta.Object

from   _MOM                                 import MOM

from   _GTW                                 import GTW
import _GTW.Media
import _GTW._Form.Widget_Spec
import _GTW._Form._MOM.Inline
import _GTW._Form._MOM.Inline_Instance

class _Inline_Description_ (TFL.Meta.Object) :
    """Base class for all inline editing descriptions (links/attributes/...)."""

    completer    = None
    js_on_ready  = ()
    css_class    = "inline-editing"

    def __init__ (self, link_name, * field_group_descriptions, ** kw) :
        self.link_name  = getattr (link_name, "type_name", link_name)
        self.field_group_descriptions = field_group_descriptions
        self.__dict__.update (kw)
    # end def __init__

# end class _Inline_Description_

class Attribute_Inline_Description (_Inline_Description_) :
    """Edit an attribute which refers to an object inline."""

    css_class               = "inline-attribute"
    widget                  = GTW.Form.Widget_Spec \
        ( "html/form.jnj, aid_div_seq"
        , inline_table_th   = "html/form.jnj, inline_table_aid_th"
        , inline_table_td   = "html/form.jnj, inline_table_aid_td"
        )

    def __call__ (self, et_man, added_fields, parent_form, ** kw) :
        scope      = et_man.home_scope
        attr_kind  = et_man._etype._Attributes._attr_dict.get \
            (self.link_name, getattr (et_man._etype, self.link_name))
        if isinstance (attr_kind, MOM.Attr._Composite_Mixin_) :
            obj_etype = attr_kind.C_Type
        else :
            obj_etype = attr_kind.role_type
        obj_et_man = getattr (scope, obj_etype.type_name)
        self.generic_name = getattr \
            (attr_kind, "generic_role_name", self.link_name)
        inline_form       = GTW.Form.MOM.Attribute_Inline_Instance.New \
            ( obj_et_man
            , * self.field_group_descriptions
            , suffix        = et_man.type_base_name
            , parent_form   = parent_form
            , completer     = self.completer
            )
        return (GTW.Form.MOM.Attribute_Inline (self, inline_form), )
    # end def __call__

# end class Attribute_Inline_Description

class Link_Inline_Description (_Inline_Description_) :
    """Edit a link inline in a form."""

    widget = GTW.Form.Widget_Spec \
        ( "html/form.jnj, inline_table"
        , Media = GTW.Media
              ( css_links   =
                  ( GTW.CSS_Link ("/media/GTW/css/jquery-ui-1.7.2.custom.css")
                  , GTW.CSS_Link ("/media/GTW/css/m2m.css")
                  )
              , scripts     =
                  ( GTW.Script (src  = "http://www.google.com/jsapi")
                  , GTW.Script (body = 'google.load ("jquery", "1");')
          ##        , GTW.Script (body = 'google.load ("jquery", "1", {uncompressed:true});')
                  , GTW.Script (body = 'google.load ("jqueryui", "1");')
                  , GTW.Script (src  = "/media/GTW/js/model_edit_ui.js") ## XXX
                  )
            )
        )
    js_on_ready  = \
        ( ( '$(".m2m-inline-form-table").many2many '
              '({link_prefix : "%(form_cls.prefix)s"});\n'
          , 100
          )
        ,
        )
    css_class    = "inline-link"

    max_count    = 256 ### seems to be more than enough for a web-app
                       ### and sys.maxint on a 64 bit is machine way to much
    min_count    = 1
    min_empty    = 0
    min_required = 0

    def __init__ (self, et_man, * field_group_descriptions, ** kw) :
        self.own_role_name = kw.pop ("own_role_name", None)
        self.__super.__init__ (et_man, * field_group_descriptions, ** kw)
    # end def __init__

    def __call__ (self, et_man, added_fields, parent_form, ** kw) :
        scope             = et_man.home_scope
        link_et_man       = getattr (scope, self.link_name)
        if not self.own_role_name :
            roles = tuple (et_man.link_map [link_et_man._etype])
            if len (roles) > 1 :
                raise TypeError ("More thanb one role to chhose from ?")
            self.own_role_name = roles [0].role_name
        self.genric_role  = getattr \
            (link_et_man, self.own_role_name).generic_role_name
        inline_form       = GTW.Form.MOM.Link_Inline_Instance.New \
            ( link_et_man
            , * self.field_group_descriptions
            , suffix        = et_man.type_base_name
            , parent_form   = parent_form
            , completer     = self.completer
            )
        return (GTW.Form.MOM.Link_Inline (self, inline_form), )
    # end def __call__

# end class Link_Inline_Description

if __name__ != "__main__" :
    GTW.Form.MOM._Export ("*")
### __END__ GTW.Form.MOM.Inline_Description
