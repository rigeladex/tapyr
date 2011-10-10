# -*- coding: iso-8859-15 -*-
# Copyright (C) 2010-2011 Martin Glueck All rights reserved
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
#     5-May-2010 (MG) `render_mode_description` added
#     6-May-2010 (MG) `table` render mode added
#     6-May-2010 (MG) `needs_header` added
#     6-May-2010 (MG) `widget` removed
#    12-May-2010 (MG) Automatic `legend` creation added
#    13-May-2010 (MG) `Link_Inline_Description.role_name` added
#    15-May-2010 (MG) Bug in `Link_Inline_Description` fixed
#    20-May-2010 (MG) `Link_Inline_Description`: widget for
#                     `link_ui_display_row` added
#    20-May-2010 (MG) `Attribute_Inline_Description`: `error` for render mode
#                     `table` set
#    28-May-2010 (MG) Render mode names changed
#    28-May-2010 (MG) Ise new `GTW.Form.MOM.Field_List` for `list_display`
#    24-Jun-2010 (MG) `javascript_options` added to `Link_Inline_Description`
#     3-Aug-2010 (MG) Handling of `role_name` changed (is now `role_names`)
#     4-Aug-2010 (MG) `Attribute_Inline_Description` render mode `table`
#                     corrected
#    19-Aug-2010 (MG) `Collection_Inline_Description.list_display` fixed
#     1-Feb-2011 (CT) Changed `src` of GTW-specific js-files
#    22-Sep-2011 (CT) s/Class/P_Type/ for _A_Id_Entity_ attributes
#    ««revision-date»»···
#--

from   _TFL                                 import TFL
import _TFL._Meta.Object

from   _MOM                                 import MOM

from   _GTW                                 import GTW
import _GTW.Media
import _GTW._Form.Render_Mode_Description
import _GTW._Form._MOM.Attribute_Inline
import _GTW.jQuery
import  operator

class _GTW_Inline_Description_ (TFL.Meta.Object) :
    """Base class for all inline editing descriptions (links/attributes/...)."""

    PKNS               = GTW.Form.MOM
    completer          = None
    css_class          = "inline-editing"
    javascript_options = dict ()
    needs_header       = False

    def __init__ (self, link_name, * field_group_descriptions, ** kw) :
        self.link_name = getattr (link_name, "type_name", link_name)
        self.field_group_descriptions = field_group_descriptions
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
          , GTW.Script (src = "/media/GTW/js/GTW/Button.js")
          , GTW.Script (src = "/media/GTW/js/GTW/Form.js")
          , GTW.Script (src = "/media/GTW/js/MOM_Auto_Complete.js")
          )
     )

_Inline_Description_ = _GTW_Inline_Description_ # end class

class GTW_Attribute_Inline_Description (_Inline_Description_) :
    """Edit an attribute which refers to an object inline."""

    _real_name              = "Attribute_Inline_Description"
    css_class               = "inline-attribute"

    render_mode_description = GTW.Form.Render_Mode_Description \
        ( div_seq = GTW.Form.Widget_Spec
            ( "html/rform.jnj, aid_div_seq"
            )
        , table   = GTW.Form.Widget_Spec
            ( "html/rform.jnj, aid_table"
            , field_head        = "html/rform.jnj, aid_th"
            , field_header      = "html/rform.jnj, aid_header"
            , field_body        = "html/rform.jnj, aid_td"
            , help              = "html/form.jnj,  field_help"
            , error             = "html/form.jnj,  field_error"
            )
        )

    def field (self, et_man, parent, ** kw) :
        scope            = et_man.home_scope
        self.attr_kind   = attr_kind = getattr (et_man._etype, self.link_name)
        self.ui_name     = attr_kind.ui_name
        obj_etype        = attr_kind.P_Type
        if isinstance (attr_kind, MOM.Attr._Composite_Mixin_) :
            generic_name = self.link_name
        else :
            generic_name = attr_kind.name
        obj_et_man       = getattr (scope, obj_etype.type_name)
        cls              = self.PKNS.Id_Attribute_Inline
        if isinstance (obj_et_man, MOM.E_Type_Manager.An_Entity) :
            cls          = self.PKNS.An_Attribute_Inline
        form_cls      =  cls.Form_Class.New \
            ( obj_et_man
            , * self.field_group_descriptions
            , completer     = kw.get ("completer", self.completer)
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

    _real_name              = "Link_Inline_Description"
    render_mode             = "popup"
    render_mode_description = GTW.Form.Render_Mode_Description \
        ( table   = GTW.Form.Widget_Spec
            ( "html/rform.jnj, inline_table"
            , Media             = _Inline_Description_.media
            )
        , popup                 = GTW.Form.Widget_Spec
            ( "html/rform.jnj, inline_list_display_table"
            , link_list_display     = "html/rform.jnj, link_list_display"
            , link_list_display_row = "html/rform.jnj, link_list_display_row"
            )
        )
    legend             = None
    role_names         = ()
    css_class          = "inline-link"

    max_count          = 256 ### seems to be more than enough for a web-app
                             ### and sys.maxint on a 64 bit is machine way to
                             ### much
    min_count          = 0
    min_empty          = 0
    min_required       = 0

    field_attrs        = dict ()
    list_display       = None
    popup              = True
    javascript_options = dict (popup = operator.attrgetter ("popup"))

    def __init__ (self, * args, ** kw) :
        self.__super.__init__ (* args, ** kw)
        self.list_display = GTW.Form.MOM.Field_List \
            (* (self.list_display or ()))
    # end def __init__

    def __call__ (self, first_pass, et_man, added_fields, parent, ** kw) :
        if not first_pass :
            scope        = et_man.home_scope
            link_et_man  = getattr (scope, self.link_name)
            if not issubclass (link_et_man._etype, MOM.Link) :
                raise TypeError \
                    ("%r is not a link" % (link_et_man.type_base_name, ))
            roles        = tuple (et_man.link_map [link_et_man._etype])
            if len (roles) > 1 :
                raise TypeError ("More than one role to choose from ?")
            self.own_role_name = roles [0].role_name
            role_attr_kind     = getattr (link_et_man, self.own_role_name)
            self.generic_role  = role_attr_kind.generic_role_name
            inline_form        = GTW.Form.MOM.Link_Inline_Instance.New \
                ( link_et_man
                , * self.field_group_descriptions
                , ignore_fields   = (self.own_role_name, self.generic_role)
                , owner_role_name = self.generic_role
                , completer       = self.completer
                , parent          = parent
                , suffix          = et_man.type_base_name
                , field_attrs     = self.field_attrs
                )
            other_roles = \
                [r for r in link_et_man.Roles if not r is role_attr_kind]
            if not self.role_names :
                self.role_names = \
                    [ r.role_name if r.role_name in inline_form.fields
                                  else r.name
                      for r in other_roles
                    ]
            if not self.legend :
                if len (other_roles) == 1 and other_roles [0].auto_cache :
                    ack = getattr (et_man, other_roles [0].auto_cache.attr_name)
                    self.legend = TFL.I18N._T (ack.ui_name)
                else :
                    self.legend = TFL.I18N._T (link_et_man.ui_name)
            self.list_display.both_runs \
                (link_et_man, self.generic_role, self.own_role_name)
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
            self.list_display.both_runs (coll_e_type)
            return (self.PKNS.Collection_Inline (self, inline_form), )
    # end def __call__

Collection_Inline_Description = GTW_Collection_Inline_Description # end class

if __name__ != "__main__" :
    GTW.Form.MOM._Export ("*")
### __END__ GTW.Form.MOM.Inline_Description

