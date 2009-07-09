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
#    DJO.Media
#
# Purpose
#    Encapsulate media specific snippets
#
# Revision Dates
#     9-Jul-2009 (CT) Creation
#    ««revision-date»»···
#--

from   _TFL                               import TFL
from   _DJO                               import DJO

import _TFL._Meta.Object
from   _TFL._Meta.Once_Property           import Once_Property

from   posixpath import join as pjoin

class CSS_Link (TFL.Meta.Object) :
    """Model a CSS link object."""

    def __init__ (self, href, media_type = "all") :
        self.href       = href
        self.media_type = media_type
    # end def __init__

    def __eq__ (self, rhs) :
        try :
            rhs = rhs.href, rhs.media_type
        except AttributeError :
            pass
        return (self.href, self.media_type) == rhs
    # end def __eq__

    def __hash__ (self) :
        return hash ((self.href, self.media_type))
    # end def __hash__

# end class CSS_Link

class Media (TFL.Meta.Object) :

    css_prefix = "styles"
    js_prefix  = "js"

    @Once_Property
    def media_url (self) :
        from django.conf import settings
        return settings.MEDIA_URL
    # end def media_url

    def __init__ (self, css_links = (), js_links = (), js_on_ready = (), js_code = (), children = ()) :
        self._css_links   = tuple (self._sanitized_css_links (css_links))
        self._js_links    = js_links
        self._js_on_ready = js_on_ready
        self._js_code     = js_code
        self.children     = list (children)
    # end def __init__

    @Once_Property
    def css_links (self) :
        return tuple (self._filter (self._gen ("css_link", self._css_massage)))
    # end def css_links

    @Once_Property
    def js_code (self) :
        return tuple (self._gen ("js_code"))
    # end def js_code

    @Once_Property
    def js_links (self) :
        return tuple (self._filter (self._gen ("js_link", self._js_massage)))
    # end def js_links

    @Once_Property
    def js_on_ready (self) :
        return tuple (self._gen ("js_on_ready"))
    # end def js_on_ready

    def _css_massage (self, l) :
        if not l.href.startswith (("http://", "https://", "/")) :
            l.href = pjoin (self.media_url, self.css_prefix, l.href)
        return l
    # end def _css_link_gen

    def _filter (links) :
        seen = set ()
        for l in links :
            if l not in seen :
                yield l
                seen.add (l)
    # end def _filter

    def _gen (self, attr, massage = None) :
        _attr = "_" + attr
        for l in getattr (self, _attr) :
            if massage :
                l = massage (l)
            yield l
        for c in self.children :
            for l in getattr (c, attr) :
                yield l
    # end def _js_code_gen

    def _js_massage (self, l) :
        if not l.startswith (("http://", "https://", "/")) :
            l = pjoin (self.media_url, self.js_prefix, l)
        return l
    # end def _js_massage

    def _sanitized_css_links (self, css_links) :
        for l in css_links :
            if not isinstance (l, CSS_Link) :
                l = CSS_Link (l)
            yield l
    # end def _sanitized_css_links

# end class Media

### __END__ DJO.Media
