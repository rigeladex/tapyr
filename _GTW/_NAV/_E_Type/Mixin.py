# -*- coding: iso-8859-15 -*-
# Copyright (C) 2010-2011 Mag. Christian Tanzer All rights reserved
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
#    GTW.NAV.E_Type.Mixin
#
# Purpose
#    Mixin for classes of GTW.NAV.E_Type
#
# Revision Dates
#    17-Mar-2010 (CT) Creation
#    12-Apr-2010 (CT) `_get_entries` factored in here
#    30-Apr-2010 (CT) `Instance_Mixin` added (factored from
#                     `GTW.NAV.E_Type.Instance_Mixin`)
#     7-May-2010 (CT) `Instance_Mixin.__init__` changed to take `parent` from
#                     `kw`, if possible
#    12-May-2010 (CT) `lid_query` removed
#    21-Dec-2010 (CT) `h_title` removed
#    22-Dec-2010 (CT) `permalink` changed to use `self.manager` instead of
#                     home-grown code
#     9-Apr-2011 (MG) Use getattr for accessing `perma_name`
#                     `Mixin._get_objects` support for dict style `Page`
#                     added
#    10-May-2011 (CT) `hidden` added
#    11-May-2011 (MG) `Mixin`: `Page` handling changed
#    ««revision-date»»···
#--

from   _GTW                     import GTW
from   _TFL                     import TFL

import _GTW._NAV._E_Type

import _TFL._Meta.Object
from   _TFL._Meta.Once_Property import Once_Property

from   posixpath                import join  as pjoin

class Mixin (TFL.Meta.Object) :
    """Mixin for classes of GTW.NAV.E_Type."""

    objects         = property (lambda s : s._objects)
    page_args       = {}
    sort_key        = None

    def __init__ (self, parent, ** kw) :
        Page_Args = kw.get ("Page")
        if isinstance (Page_Args, dict) :
            kw ["page_args"] = Page_Args.copy ()
            kw ["Page"]      = kw ["page_args"].pop ("Type")
        self.__super.__init__ (parent = parent, ** kw)
        self._objects = []
        self._old_cid = -1
    # end def __init__

    def query (self) :
        raise NotImplementedError \
            ("%s.query isn't implemented" % self.__class__.__name)
    # end def query

    @Once_Property
    def query_filters (self) :
        return tuple ()
    # end def query_filters

    def _get_entries (self) :
        scope = self.top.scope
        cid   = scope.ems.max_cid
        if self._old_cid != cid :
            self._old_cid = cid
            self._objects = self._get_objects ()
        return self._objects
    # end def _get_entries

    _entries = property (lambda s : s._get_entries (), lambda s, v : True)

    def _get_objects (self) :
        T  = self.Page
        kw = self.page_args
        return [T (self, o, ** kw) for o in self.query ()]
    # end def _get_objects

# end class Mixin

class Instance_Mixin (Mixin) :

    attr_mapper     = None

    def __init__ (self, manager, obj, ** kw) :
        name = getattr (obj, "name", None)
        if name is None :
            name = str (getattr (obj, "perma_name", obj.pid))
        else :
            name = TFL.Ascii.sanitized_filename (name)
        self.__super.__init__ \
            ( obj        = obj
            , manager    = manager
            , name       = name
            , parent     = kw.pop ("parent", manager)
            , ** kw
            )
        self.hidden      = getattr (obj, "hidden", False)
        self.short_title = self.__getattr__ ("short_title")
        self.title       = self.__getattr__ ("title")
    # end def __init__

    @property
    def admin (self) :
        return self.manager.admin
    # end def admin

    @Once_Property
    def permalink (self) :
        return self.manager.href_display (self.obj)
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

# end class Instance_Mixin

if __name__ != "__main__" :
    GTW.NAV.E_Type._Export ("*")
### __END__ GTW.NAV.E_Type.Mixin
