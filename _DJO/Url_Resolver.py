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
#    16-May-2008 (MG) `_Url_Pattern_Creation_Mixin_` factored,
#                     `Proxy_Url_Resolver` added
#    16-May-2008 (MG) `Url_Resolver.urlconf_name` replaced by settings
#                     `_urlconf_module` to `self`
#    16-May-2008 (MG) Support for url resolver less directories added
#    16-May-2008 (MG) Support for `Page`s with `url_resolver`s added
#    16-May-2008 (MG) `Singleton_Url_Resolver` and
#                     `SingletonRegexURLResolver` added
#    18-May-2008 (MG) `Proxy_Url_Resolver.prepend_pattern` and
#                     `delegate_directory_root` added
#    18-May-2008 (MG) Optional parameter `nav_element` added to
#                     `Url_Pattern.__init__`
#    ««revision-date»»···
#--

from   _TFL         import TFL
from   _DJO         import DJO
from    django.core import urlresolvers
import  posixpath
import  re

class Url_Pattern (urlresolvers.RegexURLPattern) :
    """Match a path to a distived view.
       This is an extension to the default django RegexURLPattern which adds
       the `active_page_parameter_name` to the parameters passed to the view
       callable.
    """

    active_page_parameter_name = "PAGE"

    def __init__ (self, pattern, view, name = None, ** kw) :
        self.nav_element = kw.pop ("nav_element", None)
        ### just to make it easier to pass additional context information
        super (Url_Pattern, self).__init__ (pattern, view, kw, name)
    # end def __init__

    def resolve (self, path) :
        result = super (Url_Pattern, self).resolve (path)
        if result and self.nav_element :
            self.nav_element.top.active_page = self.nav_element
            if self.active_page_parameter_name not in result [2] :
                result [2] [self.active_page_parameter_name] = self.nav_element
        return result
    # end def resolve

# end class Url_Pattern

class _Url_Pattern_Creation_Mixin_ (object) :
    """Mixin for creating/modifing url patterns out of the user spec."""

    def create_url_patterns (self, nav_element, prefix, patterns) :
        result = []
        for p in patterns :
            if not isinstance (p, (Url_Pattern, Url_Resolver)) :
                args     = ()
                kw       = {}
                if isinstance (p, dict) :
                    kw   = p
                else :
                    args = p if isinstance (p, (tuple, list)) else (p, )
                href     = nav_element.name
                if href.startswith (posixpath.sep) :
                    href = href [1:]
                p    = Url_Pattern \
                    ("^%s$" % (posixpath.join (prefix, href), ), * args, ** kw)
            elif prefix :
                old_pattern = p.regex.pattern [1:]
                p.regex = re.compile \
                    ( "^%s" % ( posixpath.join (prefix, old_pattern), )
                    , p.regex.flags
                    )
            result.append (p)
        return result
    # end def create_url_patterns

# end class _Url_Pattern_Creation_Mixin_

class Url_Resolver ( _Url_Pattern_Creation_Mixin_
                   , urlresolvers.RegexURLResolver
                   ) :
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
        self._urlconf_module    = self
    # end def __init__

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
        patterns = self.create_url_patterns (nav_element, "", patterns)
        if (   isinstance (nav_element, DJO.Navigation.Page)
           and nav_element.has_own_url_resolver
           and self is nav_element.url_resolver
           ) :
            return nav_element.parent.url_resolver.add_nav_pattern \
                (nav_element, * patterns)
        for p in patterns :
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

class Proxy_Url_Resolver (_Url_Pattern_Creation_Mixin_) :
    """Add a prefix (proxied_nav.sub_dir) to all patterns added to this
       resolver and than append the pattners/resolvers to the url resolver of
       the parent of the proxied_nav
    """

    def __init__ (self, proxied_nav) :
        self.proxied_nav = proxied_nav
    # end def __init__

    def add_nav_pattern (self, nav_element, * patterns) :
        patterns = self.create_url_patterns \
            (nav_element, self.proxied_nav.sub_dir, patterns)
        return self.proxied_nav.parent.url_resolver.add_nav_pattern \
            (nav_element, * patterns)
    # end def add_nav_pattern

    def append_pattern (self, * patterns) :
        patterns = self.create_url_patterns \
                (None, self.proxied_nav.sub_dir, patterns)
        return self.proxied_nav.parent.url_resolver.append_pattern \
            (* patterns)
    # end def append_pattern

    def prepend_pattern (self, * patterns) :
        patterns = self.create_url_patterns \
                (None, self.proxied_nav.sub_dir, patterns)
        return self.proxied_nav.parent.url_resolver.prepend_pattern \
            (* patterns)
    # end def prepend_pattern

# end class Proxy_Url_Resolver

class M_Url_Resolver (Url_Resolver.__class__) :
    """Meta class to create only one instance of the root url resolver per
      `name`.
      In real world django sites, the name is defined in the settings module
      and is called `ROOT_URLCONF`
    """

    url_resolvers = {}

    def __call__ (meta, regex, urlconf_name, * args, ** kw) :
        if urlconf_name not in meta.url_resolvers :
            meta.url_resolvers [urlconf_name] = result = super \
                (M_Url_Resolver, meta).__call__ \
                    (regex, urlconf_name, * args, ** kw)
        return meta.url_resolvers [urlconf_name]
    # end def __call__

# end class M_Url_Resolver

class Singleton_Url_Resolver (Url_Resolver) :
    """Adds the singleton behavior to the Url_Resolver."""

    __metaclass__ = M_Url_Resolver

# end class Singleton_Url_Resolver

class SingletonRegexURLResolver (urlresolvers.RegexURLResolver) :
    """Extend the default RegexURLResolver of django to add the
       `singleton` function to the django url resolvers as well.
    """

    __metaclass__ = M_Url_Resolver

# end class SingletonRegexURLResolver

def delegate_directory_root (request, ** kw) :
    page               = kw.get (DJO.Url_Pattern.active_page_parameter_name)
    callable, args, kw = urlresolvers.get_resolver (None).resolve \
        (page._entries [0].abs_href)
    return callable (request, * args, ** kw)
# end def delegate_directory_root

if urlresolvers.RegexURLResolver is not SingletonRegexURLResolver :
    urlresolvers.RegexURLResolver = SingletonRegexURLResolver

if __name__ != "__main__":
    DJO._Export ("*")
### __END__ DJO.Url_Resolver
