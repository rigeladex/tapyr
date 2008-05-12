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
#    Extend/Enhance the djnago builtin url resolver/url patterns and
#    integrate url resolving with the navigation
#
# Revision Dates
#    10-May-2008 (MG) Creation
#    ««revision-date»»···
#--

from   _TFL         import TFL
from   _DJO         import DJO
from    django.core import urlresolvers
import  posixpath

class Url_Pattern (urlresolvers.RegexURLPattern) :
    """XXX"""

    def __init__ (self, regex, callback, pattern_name = None, ** kw) :
        super (Url_Pattern, self).__init__ (regex, callback, kw, pattern_name)
    # end def __init__

    def resolve (self, path) :
        result = super (Url_Pattern, self).resolve (path)
        if result and self.nav_element :
            self.nav_element.top.active_page = self.nav_element
            if not "ACTIVE_PAGE" in result [2] :
                result [2] ["ACTIVE_PAGE"]   = self.nav_element
        return result
    # end def resolve

# end class Url_Pattern

class _Url_Resolver_ (urlresolvers.RegexURLResolver) :
    """XXX"""

    _url_pattners = None

    def __init__ (self, regex, name = None, ** kw) :
        regex = posixpath.join (regex, "")
        super (_Url_Resolver_, self).__init__ (regex, name, kw)
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
        if self._url_pattners is None :
            self._url_pattners = \
                ( self._pre_url_patterns
                + self._nav_url_patterns
                + self._post_url_patterns
                )
        return self._url_pattners
    # end def url_patterns
    urlpatterns = url_patterns

    def add_nav_pattern (self, nav_element, * patterns) :
        for p in patterns :
            self._nav_url_patterns.append (p)
            p.nav_element = nav_element
    # end def nav_post_pattern

    def add_post_pattern (self, * patterns) :
        self._post_url_patterns.extend (patterns)
    # end def add_post_pattern

    def add_pre_pattern (self, * patterns) :
        self._pre_url_patterns.extend (patterns)
    # end def add_pre_pattern

# end class _Url_Resolver_

class M_Root_Url_Resolver (_Url_Resolver_.__class__) :

    root_url_reslovers = {}

    def __call__ (meta, regex, name, ** kw) :
        if name not in meta.root_url_reslovers :
            meta.root_url_reslovers [name] = super \
                (M_Root_Url_Resolver, meta).__call__ (regex, name, ** kw)
        return meta.root_url_reslovers [name]
    # end def __call__

# end class M_Root_Url_Resolver

class Root_Url_Resolver (_Url_Resolver_) :
    """The resolver for the whole site (this is the first resolver activated
       by django)
    """

    __metaclass__ = M_Root_Url_Resolver

# end class Root_Url_Resolver

class Url_Resolver (_Url_Resolver_) :
    """XXX"""

    def __init__ (self, * args, ** kw) :
        super (Url_Resolver, self).__init__ (* args, ** kw)
    # end def __init__

# end class Url_Resolver

if not issubclass (urlresolvers.RegexURLResolver, Root_Url_Resolver) :
    urlresolvers.RegexURLResolver = Root_Url_Resolver

if __name__ != "__main__":
    DJO._Export ("*", "_Url_Resolver_")
### __END__ DJO.Url_Resolver
