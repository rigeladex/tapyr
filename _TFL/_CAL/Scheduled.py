# -*- coding: iso-8859-1 -*-
# Copyright (C) 2004 Mag. Christian Tanzer. All rights reserved
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
#    TFL.CAL.Scheduled
#
# Purpose
#    Model a scheduled item (appointment, to-do, ...)
#
# Revision Dates
#    30-Oct-2004 (CT) Creation
#     2-Nov-2004 (CT) Creation continued
#    ««revision-date»»···
#--

from   _TFL                    import TFL
import _TFL._CAL
import _TFL._Meta.Object
import _TFL.Caller

class Scheduled (TFL.Meta.Object) :
    """Root class for all types of scheduled items"""

    prototype         = None
    attr_defaults     = dict \
        ( alarm       = None
        , deadline    = None
        , description = None
        , duration    = None
        , format      = None
        , kind        = None
        , location    = None
        , priority    = None
        , reminder    = None
        , time        = None
        , title       = None
        , x_attrs     = None
        )

    def __init__ (self, ** kw) :
        for k, v in kw.iteritems () :
            if v is not None :
                setattr (self, k, v)
    # end def __init__

    def derived (self, ** kw) :
        return self.__class__ (prototype = self, ** kw)
    # end def derived

    def formatted (self, format = None) :
        if format is None :
            format = self.format
        if format is not None :
            return format % TFL.Caller.Object_Scope (self)
    # end def formatted

    def __getattr__ (self, name) :
        if self.prototype is not None :
            return getattr (self.prototype, name)
        elif name in self.attr_defaults :
            return self.attr_defaults [name]
        raise AttributeError, name
    # end def __getattr__

# end class Scheduled

if __name__ != "__main__" :
    TFL.CAL._Export ("*")
### __END__ TFL.CAL.Scheduled
