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
#    20-May-2008 (MG) `s/nav_element/nav/g`
#    20-May-2008 (MG) `Proxy_Url_Resolver` and `_Url_Pattern_Creation_Mixin_`
#                     dumped and `nav.relative_to` used instead
#    22-May-2008 (MG) `delegate_directory_root` changed
#                     `Single_Url_Pattern` and `Multi_Page_Url_Pattern` added
#                     `Url_Resolver.try_patterns` added
#                     Support for `default_view_pattern` and `view` added
#    22-May-2008 (CT) s/class_method/unbound_method/ (Truth in Advertising)
#    ««revision-date»»···
#--
### ToDO
### - rework `add_nav_pattern` and friends because since we added the `view`
###   functions the meaning of `DJO.Navigation._Site_Entity_.url_patterns`
###   can be changed to: ( ("pattern", view)
###                      , ("pattern", view, name)
###                      , ("pattern", view, name, kw)
###                      )
###   (Just like normal url patterns in django)

from   _TFL                   import TFL
from   _TFL.defaultdict       import defaultdict
from   _DJO                   import DJO
from    django.core           import urlresolvers
from    django.utils.encoding import smart_str
import  posixpath
import  re

class Url_Pattern (urlresolvers.RegexURLPattern) :
    """Base class for all self defined url patterns."""

    active_page_parameter_name = "PAGE"

    def __init__ (self, pattern, view, name = None, ** kw) :
        self.view_is_unbound = kw.pop ("unbound_method", False)
        super (Url_Pattern, self).__init__ (pattern, view, kw, name)
    # end def __init__

# end class Url_Pattern

class Single_Url_Pattern (Url_Pattern) :
    """Extend the default jango url pattern function by the ability to tie
       the pattern to a signle navigation element which will be added to the
       parameters of the view if this pattern matches the requested url.
    """

    def __init__ (self, pattern, view, name = None, ** kw) :
        self.nav             = kw.pop ("nav", None)
        super (Single_Url_Pattern, self).__init__ (pattern, view, name, ** kw)
    # end def __init__

    def resolve (self, path) :
        result = super (Single_Url_Pattern, self).resolve (path)
        if result and self.nav :
            ### because we have a match `result` now is a tupple containing:
            ###      view, args, kw
            if self.active_page_parameter_name not in result [2] :
                result [2] [self.active_page_parameter_name] = self.nav
        return result
    # end def resolve

# end class Single_Url_Pattern

class Multi_Page_Url_Pattern (Url_Pattern) :
    """A url pattern which handles multiple pages with one pattern."""

    def __init__ (self, pattern, view, name = None, ** kw) :
        self.url2nav = kw.pop ("url2nav", {})
        super (Multi_Page_Url_Pattern, self).__init__ \
            (pattern, view, name, ** kw)
    # end def __init__

    def resolve (self, path) :
        result = super (Multi_Page_Url_Pattern, self).resolve (path)
        if result :
            ### because this pattern handles multiple nav entities we need to
            ### find out which out is the correct one
            try :
                nav = self.url2nav [path]
            except KeyError :
                ### if this path does not match to any nav-elements we behave
                ### as if the pattern has not matched at all
                return None
            if self.active_page_parameter_name not in result [2] :
                result [2] [self.active_page_parameter_name] = nav
            if self.view_is_unbound :
                return \
                    ( lambda * args, ** kw : result [0] (nav, * args, ** kw)
                    , result [1], result [2]
                    )
        return result
    # end def resolve

# end class Multi_Page_Url_Pattern

class Url_Resolver (urlresolvers.RegexURLResolver) :
    """Match a path-prefix and tests the remainder of the path to it's own
       url_patterns.
       This url resolver is different to the default django RegexURLResolver
       in that way that the url_platterns don't come from a different file
       but are instead stored in the instance.
    """

    _url_patterns = None

    def __init__ (self, regex, name = None, ** kw) :
        regex                     = posixpath.join (regex, "")
        self.set_nav                        (kw.pop ("nav", None))
        self.default_view_pattern = dict \
            (   (v, re.compile (p, re.UNICODE))
              for (v, p) in kw.pop  ("default_view_pattern", {}).iteritems ()
            )
        super (Url_Resolver, self).__init__ (regex, name, kw)
        self._pre_url_patterns      = []
        self._post_url_patterns     = []
        self._nav_url_patterns      = []
        self._view_patterns         = defaultdict (list)
        self._default_patterns_used = defaultdict (list)
        self._urlconf_module        = self
    # end def __init__

    def add_nav_pattern (self, nav, * patterns) :
        patterns = self.create_url_patterns (nav, patterns)
        for p in patterns :
            self._nav_url_patterns.append (p)
            p.nav = nav
    # end def add_nav_pattern

    def add_view_function (self, nav, view, unbound_method = False) :
        ### first, we need to reduct the full url to the url which will be
        ### matched by the url resolver
        url_part        = nav.relative_to (self.nav_href)
        default_pattern = self.default_view_pattern.get (view, None)
        if default_pattern and default_pattern.match (url_part) :
            ### this view function has a default_pattern and the url part
            ### matches this pattern -> this default pattern has to be part
            ### of the url resolver
            d    = self._default_patterns_used
        else :
            ## looks like we need an own pattern for this view/nav combination
            d    = self._view_patterns
        d [view].append ((nav, url_part, unbound_method))
    # end def add_view_function

    def append_pattern (self, * patterns) :
        self._post_url_patterns.extend (patterns)
    # end def append_pattern

    def create_url_patterns (self, nav, patterns) :
        result = []
        for p in patterns :
            if not isinstance (p, Url_Pattern) :
                args     = ()
                kw       = {}
                if isinstance (p, dict) :
                    kw   = p
                else :
                    args = p if isinstance (p, (tuple, list)) else (p, )
                href     = nav.name
                if href.startswith (posixpath.sep) :
                    href = href [1:]
                if (    isinstance (nav, DJO.Navigation.Page)
                   and (nav.url_resolver is not nav.parent.url_resolver)
                   ) :
                    resolver = nav.parent.url_resolver
                    href     = nav.relative_to (resolver.nav_href)
                    p        = Single_Url_Pattern \
                        ("^%s$" % (href, ), nav = nav, * args, ** kw)
                    resolver.add_nav_pattern (nav, p)
                    continue
                href = nav.relative_to (nav.url_resolver.nav_href)
                p    = Single_Url_Pattern \
                    ("^%s$" % (href, ), nav = nav, * args, ** kw)
            result.append (p)
        return result
    # end def create_url_patterns

    def prepend_pattern (self, * patterns) :
        self._pre_url_patterns.extend (patterns)
    # end def prepend_pattern

    def set_nav (self, nav) :
        self.nav_href = posixpath.join (nav.prefix, "") if nav else ""
    # end def set_nav

    def try_patterns (self, new_path, kw = {}) :
        ### this is almost a copy of the inner code of
        ### django.core.urlresolvers.RegexURLResolver.resolve. We need this
        ### function in the `delegate_directory_root` view function (see
        ### below why)
        tried = []
        for pattern in self._urlconf_module.urlpatterns :
            try:
                sub_match = pattern.resolve (new_path)
            except urlpatterns.Resolver404, e:
                tried.extend \
                    ( [ (pattern.regex.pattern + '   ' + t)
                      for t in e.args [0] ['tried']
                      ]
                    )
            else:
                if sub_match :
                    sub_match_dict = dict \
                        ((smart_str (k), v) for k, v in kw.iteritems ())
                    sub_match_dict.update (self.default_kwargs)
                    for k, v in sub_match [2].iteritems ():
                        sub_match_dict [smart_str (k)] = v
                    return sub_match[0], sub_match[1], sub_match_dict
                tried.append (pattern.regex.pattern)
        raise urlpatterns.Resolver404, dict (tried = tried, path = new_path)
    # end def try_patterns

    @property
    def url_patterns (self) :
        if self._url_patterns is None :
            view_patterns    = []
            default_patterns = []
            for l, spec in ( (view_patterns,    self._view_patterns)
                           , (default_patterns, self._default_patterns_used)
                           ) :
                for view, entities in spec.iteritems () :
                    if len (entities) > 1 :
                        p = Multi_Page_Url_Pattern \
                            ( "^(?:%s)$" % ("|".join (e [1] for e in entities), )
                            , view
                            , unbound_method = entities [0] [2]
                            , url2nav        = dict
                                ((u, n) for (n, u, _) in entities)
                            )
                    else :
                        nav, url_part, unbound_method = entities [0]
                        p = Single_Url_Pattern \
                            ("^%s$" % (url_part, ), view
                            , nav            = nav
                            , unbound_method = unbound_method
                            )
                    l.append (p)
            self._url_patterns = \
                ( self._pre_url_patterns
                + view_patterns
                + self._nav_url_patterns
                + self._post_url_patterns
                + default_patterns
                )
        return self._url_patterns
    urlpatterns = url_patterns # end def url_patterns

# end class Url_Resolver

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
    page     = kw.get (DJO.Url_Pattern.active_page_parameter_name)
    entry    = page._entries [0]
    rel_path = entry.relative_to (page.url_resolver.nav_href)
    print "In %s -> delegate to %s (%s)" % \
        (page.title, entry.abs_href, rel_path)
    ### this wouldn't need to duplicate part of the code of
    ### django.core.urlresolvers.RegexURLResolver (the duplicated code is in
    ### DJO.Url_Resolver.try_patterns) but on the other hand this version
    ### will always start at the top level again (which is a waist since we
    ### know already in which `sub-tree` of the resolver we are)
    # callable, args, kw = urlresolvers.get_resolver (None).resolve \
    #    (page._entries [0].abs_href)
    callable, args, kw = page.url_resolver.try_patterns (rel_path, kw)
    return callable (request, * args, ** kw)
# end def delegate_directory_root

if urlresolvers.RegexURLResolver is not SingletonRegexURLResolver :
    urlresolvers.RegexURLResolver = SingletonRegexURLResolver

if __name__ != "__main__":
    DJO._Export ("*")
### __END__ DJO.Url_Resolver
