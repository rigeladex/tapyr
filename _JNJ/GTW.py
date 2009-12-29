# -*- coding: iso-8859-1 -*-
# Copyright (C) 2009 Mag. Christian Tanzer All rights reserved
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
#    ««revision-date»»···
#--

from   _JNJ import JNJ
from   _TFL import TFL

import _JNJ.Environment

from   jinja2.runtime import Undefined

def firstof (* args) :
    if len (args) == 1 and isinstance (args [0], (tuple, list)) :
        args = args [0]
    for a in args :
        if not (a is None or isinstance (a, Undefined)) :
            return a
# end def firstof

def get_macro (macro_name, templ_name = None) :
    """Return macro `macro_name` from template `templ_name`."""
    if templ_name is None :
        templ_name, macro_name = (p.strip () for p in macro_name.split (",", 1))
    env      = JNJ.Environment.active
    template = env.get_template (templ_name)
    return getattr (template.module, macro_name)
# end def get_macro

if __name__ != "__main__" :
    JNJ._Export_Module ()
### __END__ JNJ.GTW
