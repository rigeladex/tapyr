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
#    GTW.NAV.E_Type.Instance
#
# Purpose
#    Navigation page modelling a single instance of a E_Type
#
# Revision Dates
#    19-Jan-2010 (CT) Creation
#    20-Jan-2010 (CT) `FO` factored to GTW
#    25-Jan-2010 (CT) `rendered` changed to take `handler` instead of `context`
#     5-Mar-2010 (CT) `__init__` fixed
#     5-Mar-2010 (CT) `attr_mapper` and `__getattr__` using it added
#    17-Mar-2010 (CT) `permalink` added
#    17-Mar-2010 (CT) `GTW.NAV.E_Type.Mixin` added as ancestor
#    19-Mar-2010 (CT) `permalink` changed to use the real `E_Type.Manager`
#    24-Mar-2010 (CT) `Instance_Y` added
#    29-Apr-2010 (CT) `Instance.permalink` changed to use `man.href_display`
#                     instead of home-grown code
#    29-Apr-2010 (CT) `Instance_Y` removed
#    ««revision-date»»···
#--

from   _GTW                     import GTW
from   _TFL                     import TFL

import _GTW.FO
import _GTW._NAV.Base
import _GTW._NAV._E_Type.Mixin

import _TFL._Meta.Object
from   _TFL._Meta.Once_Property import Once_Property

from   _TFL.I18N                import _, _T, _Tn

from   posixpath                import join  as pjoin

class Instance (GTW.NAV.E_Type.Mixin, GTW.NAV.Page) :
    """Navigation page modelling a single instance of a E_Type."""

    allows_children = False
    attr_mapper     = None

    def __init__ (self, manager, obj, ** kw) :
        name = getattr (obj, "name", str (obj.perma_name))
        self.__super.__init__ \
            ( obj      = obj
            , manager  = manager
            , name     = name
            , parent   = manager
            , ** kw
            )
        self.desc  = self.__getattr__ ("desc")
        self.title = self.__getattr__ ("title")
    # end def __init__

    @property
    def admin (self) :
        return self.manager.admin
    # end def admin

    @property
    def contents (self) :
        return self.obj.contents
    # end def contents

    @property
    def changer (self) :
        admin = self.admin
        if admin :
            return admin._get_child ("change", self.obj.lid)
    # end def changer

    @property
    def h_title (self) :
        return u"::".join \
            ((self.obj.short_title or self.name, self.parent.h_title))
    # end def h_title

    def href_change (self) :
        admin = self.admin
        if admin :
            return admin.href_change (self.obj)
    # end def href_change

    def href_delete (self) :
        admin = self.admin
        if admin :
            return admin.href_delete (self.obj)
    # end def href

    @Once_Property
    def permalink (self) :
        man = self.top.E_Types [self.E_Type.type_name]
        return man.href_display (self.obj)
    # end def permalink

    def rendered (self, handler, template = None) :
        with self.LET (FO = GTW.FO (self.obj, self.top.encoding)) :
            return self.__super.rendered (handler, template)
    # end def rendered

    def __getattr__ (self, name) :
        if self.attr_mapper :
            try :
                return self.attr_mapper (self.obj.FO, name)
            except AttributeError :
                pass
        return self.__super.__getattr__  (name)
    # end def __getattr__

# end class Instance

if __name__ != "__main__" :
    GTW.NAV.E_Type._Export ("*")
### __END__ GTW.NAV.E_Type.Instance
