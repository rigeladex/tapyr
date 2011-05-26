# -*- coding: iso-8859-15 -*-
# Copyright (C) 2007-2009 Mag. Christian Tanzer. All rights reserved
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
#    TFL.Meta.Once_Property
#
# Purpose
#    Define a property which value is computed once per instance
#
# Revision Dates
#     9-Nov-2007 (CT) Creation
#     4-Feb-2009 (CT) Documentation improved
#    24-Sep-2009 (CT) `_del` added to `Once_Property`
#     7-Oct-2009 (CT) `Once_Property` implemented as wrapper around
#                     `Lazy_Property`
#    ««revision-date»»···
#--

from   _TFL             import TFL
import _TFL._Meta.Property

def Once_Property (f) :
    """Decorator returning a `Lazy_Property`."""
    return TFL.Meta.Lazy_Property (f.__name__, f, f.__doc__)
# end def Once_Property

if __name__ != "__main__" :
    TFL.Meta._Export ("Once_Property")
### __END__ TFL.Meta.Once_Property
