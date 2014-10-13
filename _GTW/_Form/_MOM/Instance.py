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
#    GTW.Form.MOM.Instance
#
# Purpose
#    A form which creates or changes a MOM object
#
# Revision Dates
#    18-Jan-2010 (MG) Creation
#    29-Jan-2010 (MG) Use `Widget_Spec` instead of plain text
#    22-Feb-2010 (CT) `Instance.__init__` changed to pass `** kw` to `super`
#     3-May-2010 (MG) New form handling implemented
#    15-May-2010 (MG) `css_class`, `widget`, and `default_render_mode` removed
#    ««revision-date»»···
#--

from   _MOM               import MOM

from   _TFL                                 import TFL
import _TFL._Meta.Object
import _TFL.defaultdict
import _GTW._Form.Field_Error

from   _GTW                                 import GTW
import _GTW._Form._MOM
import _GTW._Form._MOM._Instance_

class Instance (GTW.Form.MOM._Instance_) :
    """A form which creates or changes a MOM object.

       Instance of this class are always the top level form and can never be
       used as inlines.
    """

    def __init__ (self, action, instance = None, ** kw) :
        self.action       = action
        self.__super.__init__ (instance, ** kw)
    # end def __init__

# end class Instance

if __name__ != "__main__" :
    GTW.Form.MOM._Export ("*")
### __END__ GTW.Form.MOM.Instance
