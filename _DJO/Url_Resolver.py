# -*- coding: iso-8859-1 -*-
# Copyright (C) 2008 Martin Glück All rights reserved
# Langstrasse 4, 2244 Spannberg, Austria. martin@mangari.org
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
#    DJO.Url_Resolver
#
# Purpose
#    Extend/enhance the django builtin url resolver/url patterns and
#    integrate url resolving with the navigation
#
# Revision Dates
#    10-May-2008 (MG) Creation
#    14-May-2008 (CT) Spelling corrections
#    14-May-2008 (MG) Use `nav_element.name` instead of `nav_element.href`
#    ««revision-date»»···
#--

from   _TFL         import TFL
from   _DJO         import DJO
from    django.core import urlresolvers
import  posixpath

class Url_Pattern (urlresolvers.RegexURLPattern) :
    """Match a path to a distived view.
       This is an extension to the default django RegexURLPattern which adds
       the `active_page_parameter_name` to the parameters passed to the view
       callable.
    """

    def __init__ (self, pattern, view, name = None, ** kw) :
        ### just to make it easier to pass additional context information
        super (Url_Pattern, self).__init__ (pattern, view, kw, name)
    # end def __init__

    active_page_parameter_name = "PAGE"

    def resolve (self, path) :
        result = super (Url_Pattern, self).resolve (path)
        if result and self.nav_element :
            self.nav_element.top.active_page = self.nav_element
            if self.active_page_parameter_name not in result [2] :
                result [2] [self.active_page_parameter_name] = self.nav_element
        return result
    # end def resolve

# end class Url_Pattern

class Url_Resolver (urlresolvers.RegexURLResolver) :
    """Match a path-prefix and tests the remainder of the path to it's own
       url_patterns.
       This url resolver is different to the default django RegexURLResolver
       in that way that the url_platterns don't come from a different file
       but are instead stored in the instance.
    """

    _url_patterns = None

    def __init__ (self, regex, name = None, ** kw) :
        regex = posixpath.join (regex, "")
        super (Url_Resolver, self).__init__ (regex, name, kw)
        self._pre_url_patterns  = []
        self._post_url_patterns = []
        self._nav_url_patterns  = []
    # end def __init__

    @property
    def urlconf_module (self) :
        ### this url resolver acts like an urlresolver and the module
        ### containing the `urlpatterns` list as well
        return self
    # end def urlconf_module

    @property
    def url_patterns (self) :
        if self._url_patterns is None :
            self._url_patterns = \
                ( self._pre_url_patterns
                + self._nav_url_patterns
                + self._post_url_patterns
                )
        return self._url_patterns
    urlpatterns = url_patterns # end def url_patterns

    def add_nav_pattern (self, nav_element, * patterns) :
        for p in patterns :
            if not isinstance (p, Url_Pattern) :
                args = ()
                kw   = {}
                if isinstance (p, dict) :
                    kw = dict
                else :
                    args = p if isinstance (p, (tuple, list)) else (p, )
                href = nav_element.name
                p = Url_Pattern ("^%s$" % (href, ), * args, ** kw)
            self._nav_url_patterns.append (p)
            p.nav_element = nav_element
    # end def add_nav_pattern

    def append_pattern (self, * patterns) :
        self._post_url_patterns.extend (patterns)
    # end def append_pattern

    def prepend_pattern (self, * patterns) :
        self._pre_url_patterns.extend (patterns)
    # end def prepend_pattern

# end class Url_Resolver

class M_Root_Url_Resolver (Url_Resolver.__class__) :
    """Meta class to create only one instance of the root url resolver per
      `name`.
      In real world django sites, the name is defined in the settings module
      and is called `ROOT_URLCONF`
    """

    root_url_resolvers = {}

    def __call__ (meta, regex, name, ** kw) :
        if name not in meta.root_url_resolvers :
            meta.root_url_resolvers [name] = super \
                (M_Root_Url_Resolver, meta).__call__ (regex, name, ** kw)
        return meta.root_url_resolvers [name]
    # end def __call__

# end class M_Root_Url_Resolver

class Root_Url_Resolver (Url_Resolver) :
    """The resolver for the whole site (this is the first resolver activated
       by django)
    """

    __metaclass__ = M_Root_Url_Resolver

# end class Root_Url_Resolver

if not issubclass (urlresolvers.RegexURLResolver, Root_Url_Resolver) :
    urlresolvers.RegexURLResolver = Root_Url_Resolver

if __name__ != "__main__":
    DJO._Export ("*")
### __END__ DJO.Url_Resolver
