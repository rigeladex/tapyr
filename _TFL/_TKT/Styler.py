# -*- coding: iso-8859-1 -*-
# Copyright (C) 2005 Mag. Christian Tanzer. All rights reserved
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
#    TFL.TKT.Styler
#
# Purpose
#    Map a UI.Style object to a toolkit specific dictionary of options
#
# Revision Dates
#    18-Feb-2005 (CT) Creation
#    21-Feb-2005 (CT) `__init__` changed to pass `self` to `_opt_mappers`
#    ««revision-date»»···
#--

from   _TFL                 import TFL
import _TFL._TKT.Mixin
import _TFL._Meta.M_Auto_Combine

import weakref

class _TKT_Styler_ (TFL.TKT.Mixin) :
    """Map a UI.Style object to a toolkit specific dictionary of options


       >>> from _TFL._UI.Style import *
       >>> from predicate import *
       >>> class Test_Styler (Styler) :
       ...     Opts = dict_from_list (
       ...         ("background", "foreground", "underline"))
       ...     _opt_mappers = dict (
       ...           underline = lambda v : (False, True) [v != "none"]
       ...         )
       ...
       ...
       >>> s1 = Style ("s1", foreground = "yellow")
       >>> s2 = Style ("s2", background = "red")
       >>> s3 = Style ("s3", s1, s2)
       >>> s4 = Style ("s4", s1, underline = "double")
       >>> s5 = Style ("s5", s4, underline = "none")
       >>> for s in s1, s2, s3, s4, s5 :
       ...     print s, sorted (Test_Styler (s).option_dict.iteritems ())
       ...
       <Style s1> [('foreground', 'yellow')]
       <Style s2> [('background', 'red')]
       <Style s3> [('background', 'red'), ('foreground', 'yellow')]
       <Style s4> [('foreground', 'yellow'), ('underline', True)]
       <Style s5> [('foreground', 'yellow'), ('underline', False)]
    """

    _real_name           = "Styler"
    __metaclass__        = TFL.Meta.M_Auto_Combine
    _dicts_to_combine    = ("Opts", "_opt_mappers")

    Opts                 = {} ### contains all options of interest to a
                              ### specific TKT specific widget type
    _opt_mappers         = {} ### maps option names to functions transforming
                              ### option values into a toolkit specific form

    def __init__ (self, style) :
        self.style       = weakref.proxy (style)
        self.option_dict = d = {}
        _opt_mappers     = self._opt_mappers
        for o in self.Opts :
            v = getattr (style, o, None)
            if v is not None :
                if o in _opt_mappers :
                    v = _opt_mappers [o] (self, v)
                d [o] = v
    # end def __init__

Styler = _TKT_Styler_ # end class _TKT_Styler_

if __name__ != "__main__" :
    TFL.TKT._Export ("*")
### __END__ TFL.TKT.Styler
