# -*- coding: iso-8859-15 -*-
# Copyright (C) 2012 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# #*** <License> ************************************************************#
# This module is part of the package GTW.RST.TOP.
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
#    GTW.RST.TOP.Page
#
# Purpose
#    Model a leaf in tree of pages
#
# Revision Dates
#     5-Jul-2012 (CT) Creation
#    ««revision-date»»···
#--

from   __future__  import absolute_import, division, print_function, unicode_literals

from   _GTW                     import GTW
from   _TFL                     import TFL

import _GTW._RST.Resource
import _GTW._RST._TOP.Base

from   _TFL._Meta.Once_Property import Once_Property

class TOP_Page (GTW.RST.TOP._Base_, GTW.RST.Leaf) :
    """Leaf of tree of pages."""

    _real_name                 = "Page"

    dir_template_name    = None
    own_links            = []

Page = TOP_Page # end class

class _Page_O_ (Page) :
    """Page relying on an object for some of its properties."""

    def __getattr__ (self, name) :
        try :
            return self.__super.__getattr__ (name)
        except AttributeError :
            if name != "obj" :
                try :
                    obj = self.obj
                except Exception :
                    raise AttributeError (name)
                else :
                    return getattr (obj, name)
            raise
    # end def __getattr__

# end class _Page_O_

class Page_O (_Page_O_) :
    """Page relying on an object for some of its properties."""

    def __init__ (self, * args, ** kw) :
        self.ETM_name = kw.pop ("ETM")
        self.epk      = kw.pop ("epk")
        self.__super.__init__ (* args, ** kw)
    # end def __init__

    @property
    def obj (self) :
        return self.top.scope [self.ETM_name].instance (* self.epk)
    # end def obj

# end class Page_O

class Page_P (_Page_O_) :
    """Page relying on an object stored by another page for some of its properties."""

    def __init__ (self, * args, ** kw) :
        self.base_href = kw.pop ("base_href")
        self.__super.__init__ (* args, ** kw)
    # end def __init__

    @property
    def obj (self) :
        base_page = self.top.resource_from_href (self.base_href)
        if base_page is not None :
            return base_page.obj
    # end def obj

# end class Page_P

if __name__ != "__main__" :
    GTW.RST.TOP._Export ("*")
### __END__ GTW.RST.TOP.Page
