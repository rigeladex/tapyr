# -*- coding: utf-8 -*-
# Copyright (C) 2010-2011 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# ****************************************************************************
# This module is part of the package GTW.Form.
#
# This module is licensed under the terms of the BSD 3-Clause License
# <http://www.c-tanzer.at/license/bsd_3c.html>.
# ****************************************************************************
#
#++
# Name
#    GTW.Form.Widget_Spec
#
# Purpose
#    Specification of widget to be used to render a form, field-group, or field
#
# Revision Dates
#    13-Jan-2010 (CT) Creation
#     2-Feb-2010 (MG) `Media` added
#     5-Feb-2010 (MG) Allow a `Widget_Spec` instance as `default`
#     5-May-2010 (MG) `__getitem__` added
#    18-Mar-2011 (CT) Guard for names starting with `__` added to `__getattr__`
#    ««revision-date»»···
#--

from   _GTW                               import GTW
from   _TFL                               import TFL

import _TFL._Meta.Object
import _GTW._Form

class Widget_Spec (TFL.Meta.Object) :
    """Specification of a widget to be used to render a form, field-group, or
       field.
    """

    default = None
    Media   = None

    def __init__ (self, default = "html/form.jnj, undefinded", ** kw) :
        if isinstance (default, self.__class__) :
            self.__dict__.update (default.__dict__)
        else :
            assert isinstance (default, basestring)
            self.default = default
        self.Media   = kw.pop ("Media", self.Media)
        self.__dict__.update (kw)
    # end def __init__

    def __getattr__ (self, name) :
        if not name.startswith ("__") :
            return self.default
        raise AttributeError (name)
    # end def __getattr__

    def __getitem__ (self, key) :
        try :
            return getattr (self, key)
        except AttributeError :
            raise KeyError (key)
    # end def __getitem__

    def __str__ (self) :
        return self.default
    # end def __str__

# end class Widget_Spec

if __name__ != "__main__" :
    GTW.Form._Export ("*")
### __END__ GTW.Form.Widget_Spec
