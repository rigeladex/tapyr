# -*- coding: iso-8859-1 -*-
# Copyright (C) 2005 Mag. Christian Tanzer. All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.cluster
# ****************************************************************************
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Library General Public
# License as published by the Free Software Foundation; either
# version 2 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Library General Public License for more details.
#
# You should have received a copy of the GNU Library General Public
# License along with this library; if not, write to the Free
# Software Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
# ****************************************************************************
#
#++
# Name
#    Style
#
# Purpose
#    Provide style objects for abstract UI
#
# Revision Dates
#    25-Jan-2005 (CT) Creation
#    ««revision-date»»···
#--

from   _TFL                    import TFL
import _TFL._Meta.M_Data_Class
import _TFL._UI

class M_Style (TFL.Meta.M_Data_Class) :
    """Meta class used for generating style objects (which are implemented by
       real classes).
    """

    class _allowed (type) :
        ### this class must define the names of all valid style attributes

        # colors
        background     = None
        foreground     = None

        # font attributes
        font           = None
        fontsize       = None

    # end class _allowed

# end class M_Style

def Style (name, * parents, ** kw) :
    """Define new style with `name` derived from `parents` with attributes
       given by `kw`.
    """
    return M_Style (name, parents, kw)
# end def Style

if __name__ != "__main__" :
    TFL.UI._Export ("*")
### __END__ Style
