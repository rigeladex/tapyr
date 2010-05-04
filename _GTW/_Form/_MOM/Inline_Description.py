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
#     2-Feb-2010 (MG) Location of JS and CSS files changed
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
#    24-Feb-2010 (CT) `Attribute_Inline_Description.__call__` changed to use
#                     `Class` (works for `A_Object, too`) instead of
#                     `role_type` (works only for `A_Link_Role`)
#    24-Feb-2010 (MG) Media definition moved into `_Inline_Description_`
#    24-Feb-2010 (MG) Parameter `form_name` added to construction of inline
#                     form classes
#    26-Feb-2010 (MG) `keep_instance` added
#    27-Feb-2010 (MG) `sort_key` added to `jquery` media
#    28-Feb-2010 (MG) `Attribute_Inline_Description.__call__`: add attributes
#                     to `added_fields`
#    11-Mar-2010 (MG) `An_Attribute_Inline/Id_Attribute_Inline` added
#     1-May-2010 (MG) jQuery related media's are now defined in `GTW.jQuery`
#     3-May-2010 (MG) New form handling implemented
#    ««revision-date»»···
#--

from   _TFL                                 import TFL
import _TFL._Meta.Object

from   _MOM                                 import MOM

from   _GTW                                 import GTW
import _GTW.Media
import _GTW._Form.Widget_Spec
import _GTW._Form._MOM.Attribute_Inline
import _GTW.jQuery

class _GTW_Inline_Description_ (TFL.Meta.Object) :
    """Base class for all inline editing descriptions (links/attributes/...)."""

    PKNS         = GTW.Form.MOM
    completer    = None
    css_class    = "inline-editing"

    def __init__ (self, link_name, * field_group_descriptions, ** kw) :
        self.link_name = getattr (link_name, "type_name", link_name)
        self.field_group_descriptions = field_group_descriptions
        widget = kw.pop ("widget", None)
        if widget and not isinstance (widget, dict) :
            widget = dict (default = widget)
        if widget :
            self.widget = GTW.Form.Widget_Spec (self.widget, ** widget)
        self.__dict__.update (kw)
    # end def __init__

    media           = GTW.Media \
      ( css_links   =
          ( GTW.CSS_Link._.jQuery_UI
          , GTW.CSS_Link ("/media/GTW/css/inline_forms.css")
          )
      , scripts     =
          ( GTW.Script._.jQuery
          , GTW.Script._.jQuery_UI
          , GTW.Script (src = "/media/GTW/js/GTW_Form.js")
          , GTW.Script (src = "/media/GTW/js/MOM_Auto_Complete.js")
          )
     )

_Inline_Description_ = _GTW_Inline_Description_ # end class

class GTW_Attribute_Inline_Description (_Inline_Description_) :
    """Edit an attribute which refers to an object inline."""

    _real_name              = "Attribute_Inline_Description"
    css_class               = "inline-attribute"
    widget                  = GTW.Form.Widget_Spec \
        ( "html/form.jnj, aid_div_seq"
        , th_onion          = "html/form.jnj, th_onion_aid"
        , td_onion          = "html/form.jnj, td_onion_aid"
        , Media             = _Inline_Description_.media
        )

    def field (self, et_man, parent, ** kw) :
        scope            = et_man.home_scope
        attr_kind        = getattr (et_man._etype, self.link_name)
        self.ui_name     = attr_kind.ui_name
        if isinstance (attr_kind, MOM.Attr._Composite_Mixin_) :
            obj_etype    = attr_kind.C_Type
            generic_name = self.link_name
        else :
            obj_etype    = attr_kind.Class
            generic_name = attr_kind.name
        obj_et_man       = getattr (scope, obj_etype.type_name)
        cls              = self.PKNS.Id_Attribute_Inline
        if isinstance (obj_et_man, MOM.E_Type_Manager.An_Entity) :
            cls          = self.PKNS.An_Attribute_Inline
        form_cls      =  cls.Form_Class.New \
            ( obj_et_man
            , * self.field_group_descriptions
            , completer     = kw.pop ("completer", self.completer)
            , form_name     = self.link_name
            , generic_name  = generic_name
            , parent        = parent
            , is_link_role  = issubclass (et_man._etype, MOM.Link)
            , suffix        = et_man.type_base_name
            )
        return cls (self.link_name, form_cls, self)
    # end def field

    def __str__ (self) :
        return self.link_name
    # end def __str__

Attribute_Inline_Description = GTW_Attribute_Inline_Description # end class

class GTW_Link_Inline_Description (_Inline_Description_) :
    """Edit a link inline in a form."""

    _real_name   = "Link_Inline_Description"
    widget       = GTW.Form.Widget_Spec \
        ( "html/form.jnj, inlines_as_table"
        , Media             = _Inline_Description_.media
        )
    css_class    = "inline-link"

    max_count    = 256 ### seems to be more than enough for a web-app
                       ### and sys.maxint on a 64 bit is machine way to much
    min_count    = 1
    min_empty    = 0
    min_required = 0

    field_attrs  = dict ()


    def __call__ (self, first_pass, et_man, added_fields, parent, ** kw) :
        if not first_pass :
            scope        = et_man.home_scope
            link_et_man  = getattr (scope, self.link_name)
            roles        = tuple (et_man.link_map [link_et_man._etype])
            if len (roles) > 1 :
                raise TypeError ("More than one role to choose from ?")
            self.own_role_name = roles [0].role_name
            self.generic_role  = getattr \
                (link_et_man, self.own_role_name).generic_role_name
            inline_form       = GTW.Form.MOM.Link_Inline_Instance.New \
                ( link_et_man
                , * self.field_group_descriptions
                , ignore_fields   = (self.own_role_name, self.generic_role)
                , owner_role_name = self.generic_role
                , completer       = self.completer
                , parent          = parent
                , suffix          = et_man.type_base_name
                , field_attrs     = self.field_attrs
                )
            return (self.PKNS.Link_Inline (self, inline_form), )
    # end def __call__

Link_Inline_Description = GTW_Link_Inline_Description # end class

class GTW_Collection_Inline_Description (Link_Inline_Description) :
    """Edit a collection of a certain type inline."""

    _real_name   =  "Collection_Inline_Description"

    def __call__ (self, first_pass, et_man, added_fields, parent, ** kw) :
        if first_pass :
            added_fields.add (self.link_name)
        else :
            scope        = et_man.home_scope
            coll_e_type  = getattr (et_man, self.link_name).C_Type.C_Type
            inline_form       = GTW.Form.MOM.Collection_Inline_Instance.New \
                ( getattr (scope, coll_e_type.type_name)
                , * self.field_group_descriptions
                , completer       = self.completer
                , parent          = parent
                , suffix          = et_man.type_base_name
                , field_attrs     = self.field_attrs
                )
            return (self.PKNS.Collection_Inline (self, inline_form), )
    # end def __call__

Collection_Inline_Description = GTW_Collection_Inline_Description # end class

if __name__ != "__main__" :
    GTW.Form.MOM._Export ("*")
### __END__ GTW.Form.MOM.Inline_Description
