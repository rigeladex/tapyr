# -*- coding: iso-8859-15 -*-
# Copyright (C) 2008-2012 Mag. Christian Tanzer. All rights reserved
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
#    Library of context manager functions
#
# Revision Dates
#    14-Apr-2008 (CT) Creation
#    10-Dec-2009 (CT) `attr_let` changed to accept `** kw` instead of a
#                     single name and value
#    17-Dec-2010 (CT) `time_block` added
#    28-Jun-2012 (CT) Add `relaxed`
#    17-Jul-2012 (CT) Augment `AttributeError` info in `attr_let`
#    ««revision-date»»···
#--

from   _TFL import TFL
import _TFL.Decorator

from   contextlib import closing, nested
from   timeit     import default_timer as _timer

@TFL.Contextmanager
def attr_let (obj, ** kw) :
    """Provide context with attributes of `obj` temporary bound to
       values in `kw`.
    """
    store = {}
    undef = object ()
    for k, v in kw.iteritems () :
        store [k] = getattr (obj, k, undef)
    try :
        for k, v in kw.iteritems () :
            try :
                setattr (obj, k, v)
            except AttributeError as exc :
                raise AttributeError ("%s: [%s = %r]" % (exc, k, v))
        yield
    finally :
        for k, v in store.iteritems () :
            if v is undef :
                delattr (obj, k)
            else :
                try :
                    setattr (obj, k, v)
                except AttributeError as exc :
                    raise AttributeError ("%s: [%s = %r]" % (exc, k, v))
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

@TFL.Contextmanager
def relaxed (* args, ** kw) :
    """Context manager doing nothing."""
    yield None
# end def relaxed

@TFL.Contextmanager
def time_block (fmt = "Execution time: %s", out = None, cb = None) :
    """Context manager measuring the execution time for a block.

       After finishing the block, `cb` will be called with the arguments
       `start` and `finish`, if specified. Otherwise, `time_block` will use
       `fmt` to write the execution time to sys.stdout.
    """
    start  = _timer ()
    yield
    finish = _timer ()
    if cb is not None :
        cb (start, finish)
    else :
        import pyk
        pyk.fprint (fmt % (finish - start, ), file = out)
# end def time_block

if __name__ != "__main__" :
    TFL._Export_Module ()
### __END__ TFL.Context
