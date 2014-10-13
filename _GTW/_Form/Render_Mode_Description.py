# -*- coding: utf-8 -*-
# Copyright (C) 2010 Martin Glueck All rights reserved
# Langstrasse 4, A--2244 Spannberg. martin@mangari.org
# ****************************************************************************
# This module is part of the package GTW.Form.
#
# This module is licensed under the terms of the BSD 3-Clause License
# <http://www.c-tanzer.at/license/bsd_3c.html>.
# ****************************************************************************
#
#++
# Name
#    GTW.Form.Render_Mode_Description
#
# Purpose
#    Description of the different render modes for objects used during
#    rendering. Example render modes are `div_seq`, `table`,  ...
#
# Revision Dates
#     5-May-2010 (MG) Creation
#     5-May-2010 (MG) `widget_spec` instance of `default_mode` added
#    ««revision-date»»···
#--

from   _GTW                               import GTW
from   _TFL                               import TFL

import _TFL._Meta.Object
import _GTW._Form.Widget_Spec

class Render_Mode_Description (TFL.Meta.Object) :
    """Render mode description for objects used durign form rendering."""

    def __init__ (self, parent = None, ** modes) :
        if parent :
            raise NotImplementedError ("Inheritance not yet impl")
        self.__dict__.update (modes)
        self.__modes = modes.keys ()
    # end def __init__

    def __getitem__ (self, key) :
        try :
            return getattr (self, key)
        except AttributeError:
            raise ValueError ("No render mode %r defined" % (key, ))
    # end def __getitem__

# end class Render_Mode_Description

if __name__ != "__main__" :
    GTW.Form._Export ("*")
### __END__ GTW.Form.Render_Mode_Description
