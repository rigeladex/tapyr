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

from   _TFL             import TFL
import _TFL._Meta
import _TFL._Meta.Class

class _Property_ (property) :

    __metaclass__ = TFL.Meta.Class

    def __init__ (self) :
        self.__super.__init__ (self._get, self._set, self._del)
    # end def __init__

    def del_value (self, obj) :
        return delattr (obj, self.mangled_name)
    # end def del_value

    def get_value (self, obj) :
        return getattr (obj, self.mangled_name)
    # end def get_value

    def set_value (self, obj, value) :
        return setattr (obj, self.mangled_name, value)
    # end def set_value

    def set_doc (self, doc) :
        self.__doc__ = doc
    # end def set_doc

    _del = None
    _get = get_value
    _set = None

# end class _Property_

class Property (_Property_) :

    def __init__ (self, name, doc = None) :
        self.name         = name
        self.mangled_name = "__%s" % name
        self.__super.__init__ ()
        if doc :
            self.set_doc (doc)
    # end def __init__

# end class Property

class RO_Property (Property) :
    """Readonly property which is automatically initialized for each
       instance.
    """

    def __init__ (self, name, init_value = None, doc = None) :
        self.init_value = init_value
        self.__super.__init__ (name, doc)
    # end def __init__

    def init_instance (self, obj) :
        self.set_value (obj, self.init_value)
    # end def init_instance

# end class RO_Property

class RW_Property (RO_Property) :
    """Read/write property automatically initialized for each instance"""

    _del = RO_Property.del_value
    _set = RO_Property.set_value

# end class Read_Write

if __name__ == "__main__" :
    if __debug__ :
        class T (object) :
            __metaclass__ = TFL.Meta.Class
            __properties  = \
              ( RO_Property ("x", 42,  "readonly  property")
              , RW_Property ("y", 137, "writeable property")
              )

        class U (T) :
            __properties = \
              ( RW_Property ("x", 3.1415926, "redefined attribute")
              , RO_Property ("z", "fubar")
              )
else :
    TFL.Meta._Export ("*", "_Property_")
### __END__ TFL.Meta.Property
