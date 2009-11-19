# -*- coding: iso-8859-1 -*-
# Copyright (C) 2009 Martin Glueck. All rights reserved
# Langstrasse 4, 2244 Spannberg, Austria. martin@mangari.org
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
#    MOM.DBW.Session
#
# Purpose
#    Base class for database backend specific session classes
#
# Revision Dates
#    19-Oct-2009 (MG) Creation
#    ««revision-date»»···
#--

from   _TFL       import TFL
from   _MOM       import MOM
import _MOM._DBW
import _TFL._Meta.Object

class _M_Session_ (TFL.Meta.Object.__class__) :
    """Base meta class for all session"""

    def etype_decorator (cls, e_type) :
        return e_type
    # end def etype_decorator

# end class _M_Session_

class _DBW_Session_ (TFL.Meta.Object) :
    """Base class for database backend specific session classes"""

    __metaclass__ = _M_Session_
    _real_name    = "Session"

    type_name     = "<Unspecified>"

Session = _DBW_Session_ # end class Session

if __name__ != '__main__':
    MOM.DBW._Export ("*")
### __END__ MOM.DBW.Session
