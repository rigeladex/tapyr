# -*- coding: iso-8859-1 -*-
# Copyright (C) 2005-2008 Martin Glück. All rights reserved
# Langstrasse 4, A--2244 Spannberg, Austria. martin@smangari.org
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
#    DJO.Test.Response
#
# Purpose
#    A wrapper around the DJANGO response object to more `test` features
#
# Revision Dates
#     7-Oct-2008 (MG) Creation
#    ««revision-date»»···
#--

from   _TFL                   import TFL
import _TFL._Meta.Object
import _TFL._Meta.Once_Property

no_default = object ()

class Multi_Dict (TFL.Meta.Object) :

    def __init__ (self, * dict_list, ** kw) :
        self.name      = kw.pop ("name", self.__class__.__name__)
        self.dict_list = dict_list
    # end def __init__

    def __getitem__ (self, key) :
        for d in self.dict_list :
            if key in d :
                return d [key]
        raise KeyError ("`%s` not in %s" % (key, self.name))
    # end def __getitem__

    def get (self, key, default = no_default) :
        try :
            return self [key]
        except KeyError :
            if default == no_default :
                raise
        return default
    # end def get

# end class Multi_Dict

class Response (TFL.Meta.Object) :
    """Wrapper around a DJANGO response to add test features."""

    def __init__ (self, response) :
        self._response = response
        self.context   = Multi_Dict (name = "Context", * response.context)
    # end def __init__

    @TFL.Meta.Once_Property
    def lxml (self) :
        import  lxml.html
        return lxml.html.document_fromstring (self._response.content)
    # end def lxml

    def check_templates (self, * names) :
        template_names = set (t.name for t in self._response.template)
        result         = True
        for n in names :
            if n.startswith ("!") :
                result &= n [1:].strip () not in template_names
            else :
                result &= n                   in template_names
        return result
    # end def check_templates

    def __getattr__ (self, name) :
        return getattr (self._response, name)
    # end def __getattr__

# end class Response

if __name__ != "__main__" :
    from _DJO._Test import Test
    Test._Export ("Response", "no_default")
### __END__ DJO.Test.Response
