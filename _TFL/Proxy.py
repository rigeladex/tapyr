# -*- coding: iso-8859-1 -*-
# Copyright (C) 2004 Mag. Christian Tanzer. All rights reserved
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
#    Proxy
#
# Purpose
#    Generic proxy
#
# Revision Dates
#    19-Apr-2004 (CT) Creation
#    20-Apr-2004 (CT) Magic name check removed from `__getattr__` (for
#                     new-style classes, Python doesn't look at instance for
#                     magic methods)
#    23-Jul-2007 (CED) Activated absolute_import
#    06-Aug-2007 (CED) Future import removed again
#    ««revision-date»»···
#--



from   _TFL              import TFL
import _TFL._Meta.Object

class Proxy (TFL.Meta.Object) :
    """Proxy for some other object. All attributes not found in proxy will
       by taken from proxied object.
    """

    def __init__ (self, proxied, ** kw) :
        self.__dict__.update (kw)
        self._proxied = proxied
    # end def __init__

    def __getattr__ (self, name) :
        return getattr (self._proxied, name)
    # end def __getattr__

# end class Proxy

if __name__ != "__main__" :
    TFL._Export ("*")
### __END__ Proxy
