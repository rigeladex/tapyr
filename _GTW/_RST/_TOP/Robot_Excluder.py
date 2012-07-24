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
#    GTW.RST.TOP.Robot_Excluder
#
# Purpose
#    Page providing a /robots.txt file
#
# Revision Dates
#    24-Jul-2012 (CT) Creation
#    ««revision-date»»···
#--

from   __future__ import absolute_import, division, print_function, unicode_literals

from   _GTW                     import GTW
from   _TFL                     import TFL

import _GTW._RST.Mime_Type
import _GTW._RST._TOP.Page

from   _TFL._Meta.Once_Property import Once_Property

from   itertools                import chain as iter_chain

_Ancestor = GTW.RST.TOP.Page

class Robot_Excluder (_Ancestor) :
    """Page providing a /robots.txt file."""

    exclude_robots             = False
    hidden                     = True
    ignore_picky_accept        = True
    implicit                   = False

    class Robot_Excluder_GET (_Ancestor.GET) :

        _real_name             = "GET"
        _renderers             = (GTW.RST.Mime_Type.TXT, )

        def _response_body (self, resource, request, response) :
            return resource.contents
        # end def _response_body

    GET = Robot_Excluder_GET # end class Robot_Excluder_GET

    def __init__ (self, ** kw) :
        self.__super.__init__ (name = "robots", ** kw)
    # end def __init__

    @Once_Property
    def contents (self) :
        exclude = list \
            (   "Disallow: %s" % (r.abs_href, )
            for r in self.top.own_links if r.exclude_robots
            )
        result = ""
        if exclude :
            result = "\n".join (iter_chain (["User-agent: *"], exclude))
        return result
    # end def contents

# end class Robot_Excluder

if __name__ != "__main__" :
    GTW.RST.TOP._Export ("*")
### __END__ GTW.RST.TOP.Robot_Excluder
