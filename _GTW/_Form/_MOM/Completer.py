# -*- coding: iso-8859-1 -*-
# Copyright (C) 2009-2010 Mag. Christian Tanzer. All rights reserved
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
#    GTW.Form.MOM.Completer
#
# Purpose
#    Helper class for completion in nested forms
#
# Revision Dates
#    19-Aug-2009 (CT) Creation
#    20-Aug-2009 (CT) `template` added
#    20-Aug-2009 (CT) `jsor_form` and `js_on_ready` changed to include `triggers`
#    21-Aug-2009 (CT) `options` factored
#    21-Aug-2009 (CT) `min_chars` added to `options`
#    21-Aug-2009 (CT) Use meta class `M_Unique_If_Named`
#    21-Aug-2009 (CT) `_ignore_options` added and used
#     2-Feb-2010 (MG) Moved into `GTW.Form.MOM` packages
#    ««revision-date»»···
#--

from   _TFL                               import TFL
from   _GTW                               import GTW

import _TFL._Meta.Object
import _TFL._Meta.M_Unique_If_Named
import _TFL.Caller

import _GTW._Form._MOM
import  json

class Completer (TFL.Meta.Object) :
    """Helper class for completion in nested forms."""

    __metaclass__ = TFL.Meta.M_Unique_If_Named

    jsor_form = "\n".join \
        ( ("""$(".%(mname)s").completer"""
          , """  ({ "list_url" : "%(list_url)s" """
          , """   , "obj_url"  : "%(obj_url)s" """
          , """   , "prefix"   : "%(mname)s" """
          , """   , "triggers" :  %(triggers)s """
          , """  }); """
          , ""
          )
        )

    ### Can be overriden by `__init__` arguments
    options   = dict \
        ( fields    = ()
        , min_chars = 3
        , prefix    = "/Admin"
        , template  = "model_completion_list.html"
        )
    _ignore_options = set (["name", "prefix", "template"])

    def __init__ (self, triggers, ** kw) :
        self._triggers = triggers
        self.role      = kw.pop ("role", None)
        self.options   = dict (self.options, ** kw)
    # end def __init__

    def js_on_ready (self, inline) :
        base_et  = et = inline.inline_form_cls.et_man._etype
        if self.role :
            et = getattr (et, self.role).role_type
        fname    = self.role or "XXX"
        mname    = et.type_base_name
        base_tbn = base_et.type_base_name
        list_url = "%s/%s/complete/%s"  % (self.prefix, base_tbn, fname)
        obj_url  = "%s/%s/completed/%s" % (self.prefix, base_tbn, fname)
        triggers = json.dumps (self.triggers)
        result   = self.jsor_form % TFL.Caller.Object_Scope (self)
        return (result, )
    # end def js_on_ready

    @property
    def triggers (self) :
        result = {}
        for k, v in self._triggers.iteritems () :
            result [k] = d = v.copy ()
            for k, v in self.options.iteritems () :
                if k not in self._ignore_options :
                    d.setdefault (k, v)
        return result
    # end def triggers

    def __getattr__ (self, name) :
        try :
            return self.options [name]
        except KeyError :
            raise AttributeError, name
    # end def __getattr__

# end class Completer

if __name__ != "__main__":
    GTW.Form.MOM._Export ("*")
### __END__ GTW.Form.MOM.Completer
