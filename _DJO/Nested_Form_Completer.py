# -*- coding: iso-8859-1 -*-
# Copyright (C) 2009 Mag. Christian Tanzer. All rights reserved
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
#    DJO.Nested_Form_Completer
#
# Purpose
#    Helper class for completion in nested forms
#
# Revision Dates
#    19-Aug-2009 (CT) Creation
#    ««revision-date»»···
#--

from   _TFL                               import TFL
from   _DJO                               import DJO

import _TFL._Meta.Object
import _TFL.Caller

class Nested_Form_Completer (TFL.Meta.Object) :
    """Helper class for completion in nested forms."""

    jsor_form = "\n".join \
        ( ("""$(".%(mname)s").completer"""
          , """  ({ "url": "%(url)s" """
          , """   , "prefix": "%(mname)s" """
          , """  }); """
          , ""
          )
        )

    def __init__ (self, triggers, fields = ()) :
        self.triggers = triggers
        self.fields   = fields
    # end def __init__

    def js_on_ready (self, nested_form_group) :
        model  = nested_form_group.model
        fname  = nested_form_group.field_name
        mname  = nested_form_group.Name
        url    = "/Admin/%s/complete/%s" % (model.__name__, fname)
        result =  self.jsor_form % TFL.Caller.Object_Scope (self)
        return (result, )
    # end def js_on_ready

# end class Nested_Form_Completer

if __name__ != "__main__":
    DJO._Export ("*")
### __END__ DJO.Nested_Form_Completer
