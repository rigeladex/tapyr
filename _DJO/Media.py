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
#    10-Jul-2009 (CT) Creation continued
#    ««revision-date»»···
#--

from   _TFL                               import TFL
from   _DJO                               import DJO

import _TFL.predicate
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

    def __repr__ (self) :
        return "%s: %s" % (self.media_type, self.href)
    # end def __repr__

    def __str__ (self) :
        return self.href
    # end def __str__

# end class CSS_Link

class Media_List (TFL.Meta.Object) :
    """Model a list of media objects"""

    def __init__ (self, name, media, mobs) :
        self.name  = name
        self.media = media
        self.mobs  = mobs
    # end def __init__

    @Once_Property
    def values (self) :
        return tuple (self._gen_all ())
    # end def values

    def _gen_all (self) :
        for mob in self._gen_own () :
            yield mob
        name = self.name
        for child in self.media.children :
            for mob in getattr (child, name) :
                yield mob
    # end def _gen_all

    def _gen_own (self) :
        for mob in self.mobs :
            yield mob
    # end def _gen_own

    def __iter__ (self) :
        return iter (self.values)
    # end def __iter__

# end class Media_List

class Media_List_Unique (Media_List) :
    """Model a list of unique media objects (filters duplicates)."""

    def _gen_all (self) :
        return TFL.uniq (self.__super._gen_all ())
    # end def _gen_all

# end class Media_List_Unique

class Media_List_CSSL (Media_List_Unique) :
    """Model a list of CSS_Link objects"""

    prefix = "styles"

    def __init__ (self, name, media, mobs) :
        self.__super.__init__ (name, media, tuple (self._sanitized (mobs)))
    # end def __init__

    def _gen_own (self) :
        prefix = self.prefix
        url    = self.media.url
        for mob in self.__super._gen_own () :
            if not mob.href.startswith (("http://", "https://", "/")) :
                mob.href = pjoin (url, prefix, mob.href)
            yield mob
    # end def _gen_own

    def _sanitized (self, mobs) :
        for mob in mobs :
            if not isinstance (mob, CSS_Link) :
                mob = CSS_Link (mob)
            yield mob
    # end def _sanitized

# end class Media_List_CSSL

class Media_List_JSL (Media_List_Unique) :
    """Model a list of Javascript link objects"""

    prefix = "js"

    def _gen_own (self) :
        prefix = self.prefix
        url    = self.media.url
        for mob in self.__super._gen_own () :
            if not mob.startswith (("http://", "https://", "/")) :
                mob = pjoin (url, prefix, mob)
            yield mob
    # end def _gen_own

# end class Media_List_JSL

class Media (TFL.Meta.Object) :
    """
       >>> class Media (Media) :
       ...     url = "/test/"
       ...
       >>> NL = chr (10)

       >>> m = Media (css_links = ("a.css", "/b/c.css"),
       ...       js_links = ("foo.js", "bar.js", "http://baz.js"))
       >>> print NL.join (repr (l) for l in m.css_links)
       all: /test/styles/a.css
       all: /b/c.css
       >>> tuple (m.js_links)
       ('/test/js/foo.js', '/test/js/bar.js', 'http://baz.js')
       >>> n = Media (("/test/styles/a.css", CSS_Link ("c.css", "screen")))
       >>> print NL.join (repr (l) for l in n.css_links)
       all: /test/styles/a.css
       screen: /test/styles/c.css
       >>> tuple (n.js_links)
       ()
       >>> q = Media (js_links = ("qux.js", ), children = (m, n))
       >>> print NL.join (repr (l) for l in q.css_links)
       all: /test/styles/a.css
       all: /b/c.css
       screen: /test/styles/c.css
       >>> "; ".join (q.js_links)
       '/test/js/qux.js; /test/js/foo.js; /test/js/bar.js; http://baz.js'
    """

    @Once_Property
    def url (self) :
        from django.conf import settings
        return settings.MEDIA_URL
    # end def url

    def __init__ (self, css_links = (), js_links = (), js_on_ready = (), js_code = (), children = ()) :
        self.css_links   = Media_List_CSSL ("css_links",   self, css_links)
        self.js_links    = Media_List_JSL  ("js_links",    self, js_links)
        self.js_on_ready = Media_List      ("js_on_ready", self, js_on_ready)
        self.js_code     = Media_List      ("js_code",     self, js_code)
        self.children    = list            (children)
    # end def __init__

# end class Media

if __name__ != "__main__":
    DJO._Export ("*")
### __END__ DJO.Media
