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
#    GTW.NAV.E_Type.Gallery
#
# Purpose
#    Navigation page modelling a single instance of a GTW.OMP.SWP.Gallery
#
# Revision Dates
#    23-Mar-2010 (CT) Creation
#    24-Mar-2010 (CT) `name` passed to `Picture`
#    24-Mar-2010 (CT) `Gallery.permalink` and `.prefix` corrected
#    ««revision-date»»···
#--

from   _GTW                     import GTW
from   _TFL                     import TFL

import _GTW.FO
import _GTW._NAV.Base
import _GTW._NAV._E_Type.Instance

import _TFL.Accessor
import _TFL._Meta.Object

from   _TFL._Meta.Once_Property import Once_Property
from   _TFL.I18N                import _, _T, _Tn
from   _TFL.predicate           import pairwise

from   posixpath                import join  as pjoin

class Gallery (GTW.NAV.E_Type.Instance) :
    """Navigation page modelling a single instance of a Gallery."""

    allows_children = True

    template        = "gallery.html"

    class _Cmd_ (GTW.NAV.E_Type.Mixin, GTW.NAV.Page) :

        implicit          = True

    # end class _Cmd_

    class Picture (_Cmd_) :

        template  = "photo.html"

        def __init__ (self, * args, ** kw) :
            self.__super.__init__ (* args, ** kw)
            self.photo   = self.obj.photo
            self.thumb   = self.obj.thumb
        # end def __init__

        @Once_Property
        def next (self) :
            return self.obj.next
        # end def next

        @Once_Property
        def permalink (self) :
            return self.parent.href_photo (self)
        # end def permalink

        @Once_Property
        def prev (self) :
            return self.obj.prev
        # end def prev

        @Once_Property
        def title (self) :
            return "%s: %s %s/%s" % \
                ( self.parent.obj.title
                , _T ("picture")
                , self.obj.name
                , len (self.obj.gallery.pictures)
                )
        # end def title

    # end class Picture

    def __init__ (self, * args, ** kw) :
        self.__super.__init__ (* args, ** kw)
        self.prefix   = self.href
        self.pictures = pics = list \
            ( self.Picture
                ( parent = self
                , obj    = p
                , name   = "%s.html" % p.name
                )
            for p in sorted (self.obj.pictures, key = TFL.Getter.number)
            )
        prev = None
        for curr, next in pairwise (pics + [None]) :
            curr.prev = prev
            curr.next = next
            prev      = curr
    # end def __init__

    def href_photo (self, pic) :
        return pjoin (self.permalink, pic.name)
    # end def href_photo

    @Once_Property
    def permalink (self) :
        return pjoin (self.__super.permalink, "")
    # end def permalink

    def _get_child (self, child, * grandchildren) :
        if not grandchildren :
            n = int (child.split (".") [0])
            return self.pictures [n-1]
    # end def _get_child

# end class Gallery

if __name__ != "__main__" :
    GTW.NAV.E_Type._Export ("*")
### __END__ GTW.NAV.E_Type.Gallery
