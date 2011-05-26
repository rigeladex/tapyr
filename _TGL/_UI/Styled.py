# -*- coding: iso-8859-15 -*-
# Copyright (C) 2005 Mag. Christian Tanzer. All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
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
#    TGL.UI.Styled
#
# Purpose
#    Model a styled object of the user interface
#
# Revision Dates
#     1-Apr-2005 (CT) Creation
#     2-Apr-2005 (CT) Import fixed
#    20-May-2005 (CT) `override` added
#    ««revision-date»»···
#--

from   _TFL                  import TFL
from   _TGL                  import TGL
import _TFL._Meta.Object

class Styled (TFL.Meta.Object) :
    """Mode styled text object"""

    def __init__ (self, value, style = None, styler = None, ** override) :
        if isinstance (value, Styled) :
            if value.override :
                override = dict (value.override, ** override)
            if value.style :
                style = value.style
                if styler :
                    style = style (** styler.style_dict)
                    if override :
                        style.__dict__.update (override)
            value = value.value
        self.value    = value
        self.style    = style
        self.override = override
    # end def __init__

    def __str__ (self) :
        return self.value
    # end def __str__

# end class Styled

if __name__ != "__main__" :
    TGL.UI._Export ("*")
### __END__ Styled
