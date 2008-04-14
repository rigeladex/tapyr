# -*- coding: iso-8859-1 -*-
# Copyright (C) 2008 Mag. Christian Tanzer. All rights reserved
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
#    TFL.Context
#
# Purpose
#    Libryr of context manager functions
#
# Revision Dates
#    14-Apr-2008 (CT) Creation
#    ««revision-date»»···
#--

from   _TFL import TFL
import _TFL.Decorator

from contextlib import closing, nested

@TFL.Contextmanager
def attr_let (obj, attr_name, value) :
    """Context manager for temporarily changing obj's attribute `attr_name` to
       `value`.
    """
    old = getattr (obj, attr_name)
    setattr (obj, attr_name, value)
    try :
        yield obj
    finally :
        assert getattr (obj, attr_name) is value
        setattr (obj, attr_name, old)
# end def attr_let

@TFL.Contextmanager
def list_push (list, item) :
    """Context manager for temporarily pushing `item` onto `list`."""
    list.append (item)
    try :
        yield list
    finally :
        assert list [-1] is item
        list.pop ()
# end def list_push

if __name__ != "__main__" :
    TFL._Export_Module ()
### __END__ TFL.Context
