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
#    21-Feb-2005 (CT) `check_names` and doc-test added
#     3-Feb-2005 (ABR, Factored out `add`
#                 MGL)
#    ««revision-date»»···
#--

"""
Consistency check:

>>> import _TFL._TKT._Tk.Eventname
>>> import _TFL._TKT._Batch.Eventname
>>> TFL.TKT._Eventname.check_names (TFL.TKT.Batch.Eventname, TFL.TKT.Tk.Eventname)
_TFL._TKT._Tk.Eventname defines all names that _TFL._TKT._Batch.Eventname defines
_TFL._TKT._Batch.Eventname defines all names that _TFL._TKT._Tk.Eventname defines
"""

from   _TFL                 import TFL
import _TFL.Caller
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

    def __init__ (self, AC = None, _name = None, ** kw) :
        self.__super.__init__ (AC = AC)
        self._name = _name or TFL.Caller.globals ().get ("__name__")
        self._map  = dict (kw)
        self._pam  = {}
        self.add (**kw)
    # end def __init__

    def add (self, **kw) :
        pam = self._pam
        for k, v in kw.iteritems () :
            if v is not None and v in pam :
                raise ValueError, \
                    ( "Eventnames `%s` and `%s` point to same event: `%s`"
                    % (k, pam [v], v)
                    )
            pam [v] = k
    # end def add

    def check_names (cls, evn_1, evn_2) :
        """Checks if `evn_1` and `evn_2` define the same event names"""
        try :
            set
        except NameError :
            ### legacy lifter (`set` was added as builtin in 2.4)
            ### XXX remove me, please after 2.3 is history
            from sets import Set as set
        s1 = set (evn_1._map.iterkeys ())
        s2 = set (evn_2._map.iterkeys ())
        cls._check_difference (evn_1, evn_2, s1 - s2)
        cls._check_difference (evn_2, evn_1, s2 - s1)
    check_names = classmethod (check_names)

    def _check_difference (cls, evn_1, evn_2, diff) :
        if diff :
            for n in diff :
                print "%s defines %s, while %s doesn't"  % (evn_1, n, evn_2)
        else :
            print "%s defines all names that %s defines" % (evn_2, evn_1)
    _check_difference = classmethod (_check_difference)

    def __getattr__ (self, name) :
        try :
            return self._map [name]
        except KeyError :
            raise AttributeError, \
                "'Eventname' object has no attribute '%s'" % (name, )
    # end def __getattr__

    def __repr__ (self) :
        return self._name
    # end def __repr__

# end class _Eventname

if __name__ != "__main__" :
    TFL.TKT._Export ("_Eventname")
### __END__ Eventname
