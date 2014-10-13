# -*- coding: utf-8 -*-
# Copyright (C) 2010 Martin Glueck All rights reserved
# Langstrasse 4, A--2244 Spannberg, Austria. martin@mangari.org
# ****************************************************************************
# This module is part of the package GTW.Form.MOM.
#
# This module is licensed under the terms of the BSD 3-Clause License
# <http://www.c-tanzer.at/license/bsd_3c.html>.
# ****************************************************************************
#
#++
# Name
#    GTW.Form.MOM.Scope_Mockup
#
# Purpose
#    Act like a scope but don't modify the real scope.
#    This mockup is used to validate the inline link changes in forms.
#
# Revision Dates
#     6-Aug-2010 (MG) Creation
#    ««revision-date»»···
#--

from   _TFL              import TFL
import _TFL._Meta.Object
from   _GTW              import GTW
import _GTW._Form._MOM

class Scope_Mockup (TFL.Meta.Object) :
    """A mockup of a real scope."""

    def __init__ (self, scope) :
        self.app_type = scope.app_type
    # end def __init__

    def record_change (self, * args, ** kw) :
        pass
    # end def record_change

    def rename (self, entity, new_epk, renamer) :
        renamer ()
    # end def rename

    def __getattr__ (self, name) :
        return getattr (self.app_type, name)
    # end def __getattr__

    def __getitem__ (self, key) :
        return self.app_type [key]
    # end def __getitem__

# end class Scope_Mockup

if __name__ != "__main__" :
    GTW.Form.MOM._Export ("*")
### __END__ Scope_Mockup


