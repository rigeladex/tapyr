# -*- coding: utf-8 -*-
# Copyright (C) 2010 Martin Glueck All rights reserved
# Langstrasse 4, A--2244 Spannberg, Austria. martin@mangari.org
# ****************************************************************************
# This module is part of the package GTW.Form.
#
# This module is licensed under the terms of the BSD 3-Clause License
# <http://www.c-tanzer.at/license/bsd_3c.html>.
# ****************************************************************************
#
#++
# Name
#    GTW.Form.Field_Error
#
# Purpose
#    Classes for error handling for forms
#
# Revision Dates
#    15-Jan-2010 (MG) Creation
#    15-Dec-2010 (CT) Use `GTW.Form.Widget_Spec` for `widget`
#    ««revision-date»»···
#--

from   _TFL                    import TFL
import _TFL._Meta.Object

from   _GTW                    import GTW
import _GTW._Form.Widget_Spec

class Error_List (list, TFL.Meta.Object) :
    """A list of errors."""

    widget = GTW.Form.Widget_Spec ("html/field_error.jnj, error_list")

    def add (self, error) :
        if isinstance (error, (list, tuple, self.__class__)) :
            self.extend (error)
        else :
            self.append (error)
        return error
    # end def add

    def copy (self) :
        result = self.__class__ ()
        result.add (self)
        return result
    # end def copy

# end class Error_List

if __name__ != "__main__" :
    GTW.Form._Export ("*")
### __END__ GTW.Form.Field_Error
