#! /swing/bin/python
# Copyright (C) 2002 Mag. Christian Tanzer. All rights reserved
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
#    Property
#
# Purpose
#    TFL.Meta.Property
#
# Revision Dates
#    13-May-2002 (CT) Creation
#    ««revision-date»»···
#--

class Property (property) :

    _del = None
    _set = None

    def __init__ (self, name, doc = None) :
        self.name = name
        super (Property, self).__init__ \
            (self._get_value, self._set, self._del_value, doc)
    # end def __init__

    def _set_value (self, obj, value) :
        name = obj.__class__._mangled_name (self.name)
        return setattr (obj, name, value)
    # end def _set_value

    def _get_value (self, obj) :
        name = obj.__class__._mangled_name (self.name)
        return getattr (obj, name)
    # end def _get_value

    def _del_value (self, obj) :
        name = obj.__class__._mangled_name (self.name)
        return delattr (obj, name)
    # end def _del_value

# end class Property

class Autoinit (Property) :
    """Property which is automatically initialized for each instance."""

    def __init__ (self, name, init_value = None, doc = None) :
        super (Autoinit, self).__init__ (name, doc)
        self._init_value = init_value
    # end def __init__

    def init_instance (self, obj) :
        self._set_value (obj, self._init_value)
    # end def init_instance

# end class Autoinit

class RW_Property (Autoinit) :
    _set = Autoinit._set_value
# end class Read_Write

from   _TFL import TFL
import _TFL._Meta
TFL.Meta._Export ("*")

if __debug__ :
    import _TFL._Meta.Class
    class T (object) :
        __metaclass__ = TFL.Meta.Class
        _properties_  = \
          ( Autoinit    ("x", 42,  "readonly  property")
          , RW_Property ("y", 137, "writeable property")
          )

### __END__ Property
