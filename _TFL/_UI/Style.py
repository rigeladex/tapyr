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
#    26-Jan-2005 (CT) `Style` converted from function to object to allow
#                     `add` and `Style.xxx`
#    ««revision-date»»···
#--

from   _TFL                    import TFL
import _TFL._Meta.M_Data_Class
import _TFL._Meta.Object
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

class Style (TFL.Meta.Object) :

    def __call__ (self, name, * parents, ** kw) :
        """Returns new style with `name` derived from `parents` with attributes
           given by `kw`.
        """
        return M_Style (name, parents, kw)
    # end def __call__

    def add (self, name, * parents, ** kw) :
        """Add new style with `name` derived from `parents` with attributes
           given by `kw`.
        """
        if hasattr (self, name) :
            raise NameError, "Style %s already defined" % name
        result = self (name, * parents, ** kw)
        setattr (self, name, result)
        return result
    # end def add

# end class Style

Style = Style ()

if __name__ != "__main__" :
    TFL.UI._Export ("*", "Style")
### __END__ Style
