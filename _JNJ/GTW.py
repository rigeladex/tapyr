# -*- coding: iso-8859-1 -*-
# Copyright (C) 2009-2010 Mag. Christian Tanzer All rights reserved
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
#    JNJ.GTW
#
# Purpose
#    Provide additional global functions for Jinja templates
#
# Revision Dates
#    29-Dec-2009 (CT) Creation
#    13-Jan-2010 (CT) Converted to class; `call_macro` added;
#                     `_T` and `_Tn` added to class `GTW`
#    25-Jan-2010 (MG) `_T` and `_Tn` need to be static methods
#    27-Jan-2010 (CT) `Getter`, `now`, and `sorted` added
#    ««revision-date»»···
#--

from   _JNJ import JNJ
from   _TFL import TFL

import _JNJ.Environment

import _TFL._Meta.Object
import _TFL.Accessor
import _TFL.I18N

class GTW (TFL.Meta.Object) :
    """Provide additional global functions for Jinja templates."""

    from jinja2.runtime import Undefined

    def __init__ (self, env) :
        self.env = env
    # end def __init__

    def call_macro (self, macro_name, * _args, ** _kw) :
        """Call macro named by `macro_name` passing `* _args, ** _kw`."""
        templ_name = _kw.pop   ("templ_name", None)
        macro      = self.get_macro (macro_name, templ_name)
        return macro (* _args, ** _kw)
    # end def call_macro

    def firstof (self, * args) :
        if len (args) == 1 and isinstance (args [0], (tuple, list)) :
            args = args [0]
        for a in args :
            if not (a is None or isinstance (a, self.Undefined)) :
                return a
    # end def firstof

    def get_macro (self, macro_name, templ_name = None) :
        """Return macro `macro_name` from template `templ_name`."""
        if not isinstance (macro_name, basestring) :
            macro_name = str (macro_name)
        if templ_name is None :
            templ_name, macro_name = \
                (p.strip () for p in macro_name.split (",", 1))
        template = self.env.get_template (templ_name)
        return getattr (template.module, macro_name)
    # end def get_macro

    Getter = TFL.Getter

    def now (self, format = "%Y/%m/%d") :
        from datetime import datetime
        result = datetime.now ()
        return result.strftime (format)
    # end def now

    sorted = staticmethod (sorted)

    _T  = staticmethod (TFL.I18N._T)
    _Tn = staticmethod (TFL.I18N._Tn)

# end class GTW

if __name__ != "__main__" :
    JNJ._Export ("GTW")
### __END__ JNJ.GTW
