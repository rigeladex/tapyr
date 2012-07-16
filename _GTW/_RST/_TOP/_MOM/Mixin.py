# -*- coding: iso-8859-15 -*-
# Copyright (C) 2012 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# #*** <License> ************************************************************#
# This module is part of the package GTW.RST.TOP.MOM.
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
#    GTW.RST.TOP.MOM.Mixin
#
# Purpose
#    Define mixin classes for GTW.RST.TOP.MOM
#
# Revision Dates
#    15-Jul-2012 (CT) Creation
#    ««revision-date»»···
#--

from   __future__ import absolute_import, division, print_function, unicode_literals

from   _GTW                     import GTW
from   _TFL                     import TFL

import _GTW._RST._MOM.Mixin
import _GTW._RST._TOP._MOM

from   _TFL._Meta.Once_Property import Once_Property
from   _TFL.I18N                import _, _T, _Tn

import _TFL.Ascii
import _TFL.Attr_Mapper

class TOP_MOM_Entity_Mixin (GTW.RST.MOM.RST_Mixin) :
    """Mixin for RST.TOP classes displaying MOM instances."""

    _real_name      = "Entity_Mixin"

    attr_mapper     = TFL.Attr_Mapper ()

    def __init__ (self, ** kw) :
        obj = kw ["obj"]
        if "name" not in kw :
            name = getattr (obj, "name", None)
            if name is None :
                name = unicode (getattr (obj, "perma_name", obj.pid))
            kw ["name"] = TFL.Ascii.sanitized_filename (name)
        kw.setdefault ("manager", self.parent)
        kw.setdefault ("hidden",  getattr (obj, "hidden", False))
        self.__super.__init__ (** kw)
        ### Get `short_title` and `title` from `obj`
        self.short_title = self.__getattr__ ("short_title")
        self.title       = self.__getattr__ ("title")
    # end def __init__

    @property
    def admin (self) :
        return self.manager.admin
    # end def admin

    @Once_Property
    def FO (self) :
        return GTW.FO (self.obj, self.top.encoding)
    # end def FO

    @Once_Property
    def permalink (self) :
        return self.manager.href_display (self.obj)
    # end def permalink

    def __getattr__ (self, name) :
        if self.attr_mapper :
            try :
                return self.attr_mapper (self.obj.FO, name)
            except AttributeError :
                pass
        return self.__super.__getattr__  (name)
    # end def __getattr__

Entity_Mixin = TOP_MOM_Entity_Mixin # end class

class TOP_MOM_E_Type_Mixin (GTW.RST.MOM.RST_E_Type_Mixin) :

    _real_name      = "E_Type_Mixin"

    attr_mapper     = None

    def __init__ (self, ** kw) :
        self.pop_to_self (kw, "ETM", prefix = "_")
        E_Type      = self.E_Type
        name        = kw.pop  ("name",        E_Type.ui_name)
        short_title = kw.pop  \
            ( "short_title"
            , _T (name.capitalize () if name [0] >= "a" else name)
            )
        title       = kw.pop  ("title",       _T (E_Type.__doc__))
        self.__super.__init__ \
            ( name          = TFL.Ascii.sanitized_filename (unicode (name))
            , short_title   = short_title
            , title         = title
            , ** kw
            )
    # end def __init__

    def __getattr__ (self, name) :
        if self.attr_mapper :
            try :
                return self.attr_mapper (self.obj, name)
            except AttributeError :
                pass
        return self.__super.__getattr__  (name)
    # end def __getattr__

E_Type_Mixin = TOP_MOM_E_Type_Mixin # end class

if __name__ != "__main__" :
    GTW.RST.TOP.MOM._Export ("*")
### __END__ GTW.RST.TOP.MOM.Mixin
