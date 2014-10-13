# -*- coding: utf-8 -*-
# Copyright (C) 2004 Mag. Christian Tanzer. All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# ****************************************************************************
#
# This module is licensed under the terms of the BSD 3-Clause License
# <http://www.c-tanzer.at/license/bsd_3c.html>.
# ****************************************************************************
#
#++
# Name
#    Proxy
#
# Purpose
#    Generic proxy
#
# Revision Dates
#    19-Apr-2004 (CT) Creation
#    20-Apr-2004 (CT) Magic name check removed from `__getattr__` (for
#                     new-style classes, Python doesn't look at instance for
#                     magic methods)
#    23-Jul-2007 (CED) Activated absolute_import
#    06-Aug-2007 (CED) Future import removed again
#    ««revision-date»»···
#--



from   _TFL              import TFL
import _TFL._Meta.Object

class Proxy (TFL.Meta.Object) :
    """Proxy for some other object. All attributes not found in proxy will
       by taken from proxied object.
    """

    def __init__ (self, proxied, ** kw) :
        self.__dict__.update (kw)
        self._proxied = proxied
    # end def __init__

    def __getattr__ (self, name) :
        return getattr (self._proxied, name)
    # end def __getattr__

# end class Proxy

if __name__ != "__main__" :
    TFL._Export ("*")
### __END__ Proxy
