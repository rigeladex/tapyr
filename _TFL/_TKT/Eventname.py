# -*- coding: iso-8859-1 -*-
# Copyright (C) 2004-2005 Mag. Christian Tanzer. All rights reserved
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
#    TFL.TKT.Eventname
#
# Purpose
#    Provide symbolic names for GUI events (keys, mouse clicks, ...)
#
# Revision Dates
#    12-Jan-2005 (CT) Creation
#    18-Jan-2005 (CT) Derive from `TFL.TKT.Mixin` instead of `TFL.Meta.Object`
#     9-Feb-2005 (CT) `_pam` added
#    14-Feb-2005 (CT) `__init__` changed to accept multiple mappings to `None`
#    ««revision-date»»···
#--

from   _TFL                 import TFL
import _TFL._TKT.Mixin

class _Eventname (TFL.TKT.Mixin) :
    """Provide symbolic names for GUI events (keys, mouse clicks, ...)

       >>> Eventname = _Eventname (copy = "<Control C>", save = "<Control S>")
       >>> Eventname.copy
       '<Control C>'
       >>> Eventname.save
       '<Control S>'
       >>> Eventname.cut
       Traceback (most recent call last):
         ...
       AttributeError: 'Eventname' object has no attribute 'cut'
    """

    def __init__ (self, AC = None, ** kw) :
        self.__super.__init__ (AC = AC)
        self._map = dict (kw)
        self._pam = pam = {}
        for k, v in kw.iteritems () :
            if v is not None and v in pam :
                raise ValueError, \
                    ( "Eventnames `%s` and `%s` point to same event: `%s`"
                    % (k, pam [v], v)
                    )
            pam [v] = k
    # end def __init__

    def __getattr__ (self, name) :
        try :
            return self._map [name]
        except KeyError :
            raise AttributeError, \
                "'Eventname' object has no attribute '%s'" % (name, )
    # end def __getattr__

# end class _Eventname

if __name__ != "__main__" :
    TFL.TKT._Export ("_Eventname")
### __END__ Eventname
