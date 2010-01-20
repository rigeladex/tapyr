# -*- coding: iso-8859-1 -*-
# Copyright (C) 2010 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# ****************************************************************************
# This module is part of the package GTW.NAV.E_Type.
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
#    GTW.NAV.E_Type.Admin
#
# Purpose
#    Navigation page for managing the instances of a specific E_Type
#
# Revision Dates
#    20-Jan-2010 (CT) Creation
#    ««revision-date»»···
#--

from   _GTW                     import GTW
from   _TFL                     import TFL

import _GTW._NAV.Base
import _GTW._NAV._E_Type._Mgr_Base_
import _GTW._Form._MOM.Instance

import _TFL._Meta.Object
from   _TFL._Meta.Once_Property import Once_Property

from   _TFL.I18N                import _, _T, _Tn

from   itertools                import chain as ichain
from   posixpath                import join as pjoin, normpath as pnorm

class Admin (GTW.NAV.E_Type._Mgr_Base_, GTW.NAV.Page) :
    """Navigation page for managing the instances of a specific E_Type."""

    std_template    = "e_type_admin"

    def __init__ (self, ETM, ** kw) :
        if "Form" not in kw :
            kw ["Form"] = GTW.Form.MOM.Instance.New (ETM._etype)
        if "list_display" not in kw :
            kw ["list_display"] = self._auto_list_display (ETM, kw)
        self.__super.__init__ (ETM = ETM, ** kw)
        self.prefix = pjoin (self.parent.prefix, self.name)
    # end def __init__

    @Once_Property
    def manager (self) :
        return self.top.E_Types.get ((self.E_Type.type_name, self.kind_name))
    # end def manager

    @Once_Property
    def href (self) :
        return pjoin (self.prefix, u"")
    # end def href

    def href_create (self) :
        return pjoin (self.abs_href, "create")
    # end def href_create

    def href_change (self, obj) :
        return pjoin (self.abs_href, "change", str (obj.id))
    # end def href_change

    def href_delete (self, obj) :
        return pjoin (self.abs_href, "delete", str (obj.id))
    # end def href_delete

    @property
    def h_title (self) :
        return u"::".join ((self.name, self.parent.h_title))
    # end def h_title

    def rendered (self, context = None, nav_page = None) :
        if context is None :
            context = dict (page = self)
        context.update \
            ( fields  = self.list_display
            , objects = self._entries
            )
        return self.__super.rendered (context, nav_page)
    # end def rendered

    def _auto_list_display (self, E_Type, kw) :
        return list (ichain (E_Type.primary, E_Type.user_attr))
    # end def _auto_list_display

    _child_name_map = dict \
        ( change    = (Changer,   "pid")
        , complete  = (Completer, "field_name")
        , completed = (Completed, "field_name")
        )

    def _get_child (self, child, * grandchildren) :
        if child in self._child_name_map :
            T, attr = self._child_name_map [child]
            return T \
                ( parent = self
                , name   = "%s/%s" % (child, grandchildren [0])
                , ** {attr : grandchildren [0]}
                )
        if child == "create" and not grandchildren :
            return self.Changer (parent = self)
        if child == "delete" and len (grandchildren) == 1 :
            return self.Deleter (parent = self, pid = grandchildren [0])
    # end def _get_child

# end class Admin

"""
   1.    Erzeugen der E-Type spezifischen Form-Klasse:

der einfachst Weg:
form_cls =  GTW.Form.MOM.Instance.New (scope.PAP.Person)
erzeugt 2 Field-Groups: eine mit den primary Attributen, die andere mit
den User Attributen

oder User-Controlled:

form_cls =  GTW.Form.MOM.Instance.New \
    ( scope.PAP.Person
    , GTW.Form.MOM.Field_Group_Description ()
    , GTW.Form.MOM.Inline_Description
        ( "PAP.Person_has_Address", "person"
        , GTW.Form.MOM.Field_Group_Description
              ( GTW.Form.MOM.Field_Prefixer
                  ("address", "street", "zip", "city", "country", "desc")
              )
        , min_empty = 1
        )
    )

wobei es bei den "Fields" folgende Möglichkeiten gibt:

GTW.Form.MOM.Wildcard_Field (* kinds, ** kw)

    * kinds gibt an aus welchen kinds die Felder genommen werden sollen:
      Default: primary, user_attr
    * in den KW kann ein prefix sein

Damit ist folgendes möglich (vorallen für die Inlines interessant):

GTW.Form.MOM.Wildcard_Field ("primary") -> alle primary attribute
GTW.Form.MOM.Wildcard_Field ("primary", prefix = "address") -> alle
primary der Rolle "address"
GTW.Form.MOM.Wildcard_Field (prefix = "address") -> alle primary und
user_attr der Rolle "address"

Wobei "alle" immer für "alle die nicht vorher explizit angeführt wurden"
steht...

und dann gibt es noch den Field_Prefixer... ich denke da ist klar was
der macht (1. Parameter is der prefix, 2...n Namen der Felder...)

Die Inline_Desciption kann folgende "Parameter":

    * min_required (default 0)
    * min_empty (default 1)
    * max_count (default 100)
    * widget (default "html/form.jnj, inline")

Soweit zur Form Klassen-Erzeugung. Im rendered gehts dann so:

form = form_cls (action_url, [instance]) (default für instance its None)

und im POST Fall danach:
error_count = form (request_data)

"""

if __name__ != "__main__" :
    GTW.NAV.E_Type._Export ("*")
### __END__ GTW.NAV.E_Type.Admin
