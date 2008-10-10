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
#    10-Oct-2008 (MG) `check_form_errors` added
#    ««revision-date»»···
#--

from   _TFL                   import TFL
import _TFL._Meta.Object
import _TFL._Meta.Once_Property
from    urlparse              import urlsplit, urlunsplit
from    django.http           import QueryDict

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
        self.context   = Multi_Dict (name = "Context", * response.context or ())
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

    def check_form_errors (self, * fields_with_errors, ** kw) :
        form_name = kw.pop ("form_name", "form")
        non_field = kw.pop ("non_field_errors", False)
        form      = self.context [form_name]
        errors    = dict (form.errors)
        for field_name in fields_with_errors :
            assert field_name in errors
            del errors [field_name]
        for field_name, error_msg in kw.iteritems () :
            msg = "\n\n".join (unicode (m) for m in errors.pop (field_name))
            assert error_msg in msg
        assert not errors
        assert bool (form.non_field_errors ()) == non_field
    # end def check_form_errors

    def check_redirect ( self, redirect_to
                       , redirect_status_code = 302
                       , status_code          = 200
                       , host                 = None
                       ) :
        assert self.status_code == redirect_status_code
        url = self._response ["Location"]
        scheme,     netloc,   path,   query,   fragment = urlsplit (url)
        e_scheme, e_netloc, e_path, e_query, e_fragment = urlsplit (redirect_to)
        if not (e_scheme or e_netloc):
            redirect_to = urlunsplit \
                (("http", host or "testserver", e_path, e_query, e_fragment))
        assert url == redirect_to

        if status_code is not None :
            # Get the redirection page, using the same client that was used
            # to obtain the original response.
            redirect_response = self._response.client.get \
                (path, QueryDict (query))
            assert redirect_response.status_code == status_code
    # end def check_redirect

# end class Response

if __name__ != "__main__" :
    from _DJO._Test import Test
    Test._Export ("Response", "no_default")
### __END__ DJO.Test.Response
