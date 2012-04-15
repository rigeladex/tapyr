# -*- coding: iso-8859-15 -*-
# Copyright (C) 2005-2012 Mag. Christian Tanzer. All rights reserved
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
#    TFL.TKT.Styler
#
# Purpose
#    Map a UI.Style object to a toolkit specific dictionary of options
#
# Revision Dates
#    18-Feb-2005 (CT) Creation
#    21-Feb-2005 (CT) `__init__` changed to pass `self` to `_opt_mappers`
#     1-Apr-2005 (CT) `style_dict` added
#     1-Apr-2005 (CT) `__new__` and `_cache` added
#     2-Apr-2005 (MG) `__init__` changed to allow renaming of a `style`
#                     property
#    ««revision-date»»···
#--

from   _TFL                 import TFL
import _TFL._TKT.Mixin
import _TFL._Meta.M_Auto_Combine
import _TFL._Meta.Object

import weakref

class _TKT_Styler_ (TFL.Meta.Object) :
    """Map a UI.Style object to a toolkit specific dictionary of options


       >>> from _TFL._UI.Style import *
       >>> from _TFL.predicate import *
       >>> class Test_Styler (Styler) :
       ...     Opts = dict_from_list (
       ...         ("background", "foreground", "underline"))
       ...     _opt_mappers = dict (
       ...           underline = lambda s, v : (False, True) [v != "none"]
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

    _cache               = {} ### indexed by `self.__class__` and `style`

    def __new__ (cls, style) :
        if cls not in cls._cache :
            cls._cache [cls] = weakref.WeakKeyDictionary ()
        _cache = cls._cache [cls]
        if style in _cache :
            return _cache [style]
        result = _cache [style] \
               = super (_TKT_Styler_, cls).__new__ (cls, style)
        result._init_ (style)
        return result
    # end def __new__

    def _init_ (self, style) :
        self.style       = weakref.proxy (style)
        self.style_dict  = s = {}
        self.option_dict = d = {}
        _opt_mappers     = self._opt_mappers
        for style_name, tkt_name in self.Opts.iteritems () :
            v        = getattr (style, style_name, None)
            if v is not None :
                s [style_name] = v
                if style_name in _opt_mappers :
                    v = _opt_mappers [style_name] (self, v)
                d [tkt_name or style_name] = v
    # end def __init__

Styler = _TKT_Styler_ # end class _TKT_Styler_

if __name__ != "__main__" :
    TFL.TKT._Export ("*")
### __END__ TFL.TKT.Styler
