# -*- coding: iso-8859-1 -*-
# Copyright (C) 2006 Mag. Christian Tanzer. All rights reserved
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
#    TGL.Observed_Value
#
# Purpose
#    Encapsulate a value and inform observers about changes of that value
#
# Revision Dates
#     5-Jan-2006 (CT) Creation
#    21-Jan-2006 (MG) Support for `kw` added
#    ««revision-date»»···
#--

from _TFL import TFL
from _TGL import TGL

import _TFL._Meta.Object

class Observed_Value (TFL.Meta.Object) :
    """Value that informs registered observers about changes.

       >>> x = Observed_Value (0)
       >>> def obs (ov, nv) :
       ...     print "%s changed to %s" % (ov, nv)
       ...
       >>> x.register_observer (obs)
       >>> x.value
       0
       >>> x.value = 0
       >>> x.value = 42
       0 changed to 42
       >>> x.value = 0
       42 changed to 0
       >>> x.value = 0
    """

    value = property (lambda s : s._value, lambda s, v : s._set (v))

    def __init__ (self, value = None, ** kw) :
        self._value    = value
        self.observers = []
        self.kw        = kw
    # end def __init__

    def deregister_observer (self, * o) :
        to_remove = set (o)
        self.observers = [o for o in self.observers if o not in to_remove]
    # end def deregister_observer

    def register_observer (self, * o) :
        self.observers.extend (o)
    # end def register_observer

    def _set (self, value) :
        if value != self._value :
            for o in self.observers :
                o (self, value, ** self.kw)
        self._value = value
    # end def _set

    def __getattr__ (self, name) :
        if name not in self.kw :
            return getattr (self._value, name)
        return self.kw [name]
    # end def __getattr__

    def __float__ (self) :
        return float (self._value)
    # end def __float__

    def __int__ (self) :
        return int (self._value)
    # end def __int__

    def __len__ (self) :
        return len (self._value)
    # end def __len__

    def __long__ (self) :
        return long (self._value)
    # end def __long__

    def __nonzero__ (self) :
        return bool (self._value)
    # end def __nonzero__

    def __repr__ (self) :
        return repr (self._value)
    # end def __repr__

    def __str__ (self) :
        return str (self._value)
    # end def __str__

# end class Observed_Value

if __name__ != "__main__" :
    TGL._Export ("*")
### __END__ TGL.Observed_Value
