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
#    TGW/_Eventname
#
# Purpose
#    Provides a mechanism for accessing the keyboard accelerators and other
#    kinds of actions in a toolkit-independent way
#
# Revision Dates
#    10-Jan-2005 (ABR, Creation
#                 GZA)
#    ««revision-date»»···
#--

from _TFL import TFL
import _TFL._TKT
import _TFL._Meta.Object

class _Eventname (TFL.Meta.Object) :
    """
    >>> Eventname = _Eventname (copy = "Strg-C", paste = "Strg-V")
    >>> print Eventname.copy
    Strg-C
    >>> print Eventname.paste
    Strg-V
    >>> print Eventname.undefined
    Traceback (most recent call last):
      File "/usr/local/lib/python2.3/doctest.py", line 442, in _run_examples_inner
        compileflags, 1) in globs
      File "<string>", line 1, in ?
      File "./_Eventname.py", line 40, in __getattr__
        raise AttributeError, e
    AttributeError: 'undefined'

    """
    def __init__ (self, **kw) :
        self.key_dict = dict (**kw)
    # end def __init__

    def __getattr__ (self, name) :
        try :
            return self.key_dict [name]
        except KeyError, e :
            raise AttributeError, e
    # end def __getattr__
# end class _Eventname

if __name__ != "__main__" :
    from _TFL._TKT import TKT
    TKT._Export ("_Eventname")

### __END__ _TFL/_TKT/_Eventname

