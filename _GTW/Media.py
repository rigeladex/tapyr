# -*- coding: iso-8859-15 -*-
# Copyright (C) 2009-2012 Mag. Christian Tanzer. All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# ****************************************************************************
# This module is part of the package GTW.
#
# This module is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This module is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this module. If not, see <http://www.gnu.org/licenses/>.
# ****************************************************************************
#
#++
# Name
#    GTW.Media
#
# Purpose
#    Encapsulate media specific snippets
#
# Revision Dates
#     9-Jul-2009 (CT) Creation
#    10-Jul-2009 (CT) Creation continued
#    10-Jul-2009 (CT) `Script` added and `js_code` removed
#    10-Jul-2009 (CT) `Rel_Link` added
#    13-Jul-2009 (CT) `Rel_Link.attrs` fixed
#    14-Jul-2009 (CT) `Media_List_JSOR` added and used for `js_on_ready`
#    14-Jul-2009 (CT) `__len__` and `__nonzero__` added to `Media_List`
#    21-Aug-2009 (MG) `JS_On_Ready` added and used to support sorting in
#                     `Media_List_JSOR`
#    10-Jan-2010 (MG) Moved into Package `GTW`
#     2-Feb-2010 (MG) `Media_List.add` added
#     4-Feb-2010 (MG) `Media.from_list` added
#    27-Feb-2010 (MG) `sort_key` added to javascript
#     1-May-2010 (MG) Use `M_Unique_If_Named` to support reuse of media
#                     objects
#     7-Dec-2010 (CT) `condition` added to `Script`
#    13-Sep-2011 (MG) `s/sort_key/rank/g`
#    13-Sep-2011 (MG) `Rel_Link`: `__str__` and `__repr__` added
#    14-Oct-2011 (MG) `JS_On_Ready`: parameter `code` can be a `JS_On_Ready`
#                     as well
#     3-Jan-2012 (CT) Factor `_Object_`, add and use `requires` and `objects`
#     4-Jan-2012 (CT) Add `Script.cache_p`
#     5-Jan-2012 (CT) Remove `Script.body`
#     8-Jan-2012 (CT) Use `.pop_to_self` to reduce footprint of media objects
#    ««revision-date»»···
#--

from   _TFL                               import TFL
from   _GTW                               import GTW

import _TFL.predicate
import _TFL._Meta.Object
import _TFL._Meta.M_Unique_If_Named
from   _TFL._Meta.Once_Property           import Once_Property
from   _TFL._Meta.Property                import Alias_Property

from   posixpath import join as pjoin

class _Object_ (TFL.Meta.Object) :
    """Base class for media objects."""

    rank     = 0
    requires = ()

    @Once_Property
    def objects (self) :
        def _gen (s) :
            for r in s.requires :
                for o in r.objects :
                    yield o
            yield s
        return tuple (_gen (self))
    # end def objects

    @classmethod
    def _sanitized (cls, mobs, Mob_Type = None) :
        if Mob_Type is None :
            Mob_Type = cls
        for mob in mobs :
            if not isinstance (mob, Mob_Type) :
                mob = Mob_Type (mob)
            yield mob
    # end def _sanitized

# end class _Object_

class CSS_Link (_Object_) :
    """Model a CSS link object."""

    __metaclass__ = TFL.Meta.M_Unique_If_Named

    condition     = ""
    media_type    = "all"
    name          = None

    def __init__ (self, href, ** kw) :
        self.href = href
        self.pop_to_self (kw, "condition", "media_type", "name", "rank")
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

class Rel_Link (_Object_) :
    """Model a `rel` link object."""

    def __init__ (self, ** kw) :
        self.href = kw ["href"]
        self.pop_to_self (kw, "rank")
        self._kw  = kw
    # end def __init__

    def attrs (self) :
        return " ".join \
            (   '''%s="%s"''' % (k, v)
            for (k, v) in sorted (self._kw.iteritems ())
            )
    # end def attrs

    def __repr__ (self) :
        return self.attrs ()
    # end def __repr__

    def __str__ (self) :
        return self.href
    # end def __str__

# end class Rel_Link

class Script (_Object_) :
    """Model a script element"""

    __metaclass__ = TFL.Meta.M_Unique_If_Named

    href          = Alias_Property ("src")

    condition     = ""
    may_cache     = True
    name          = None
    script_type   = "text/javascript"

    def __init__ (self, src, ** kw) :
        assert src
        self.src  = src
        self.pop_to_self \
            ( kw
            , "condition", "may_cache", "name", "rank", "requires"
            , "script_type"
            )
        if self.requires :
            self.requires = tuple (self._sanitized (self.requires))
    # end def __init__

    @Once_Property
    def absolute_p (self) :
        return self.src.startswith (("http://", "https://"))
    # end def absolute_p

    @Once_Property
    def cache_p (self) :
        return self.may_cache and not (self.condition or self.absolute_p)
    # end def cache_p

    def __eq__ (self, rhs) :
        try :
            rhs = (rhs.src, rhs.script_type)
        except AttributeError :
            pass
        return (self.src, self.script_type) == rhs
    # end def __eq__

    def __hash__ (self) :
        return hash ((self.src, self.script_type))
    # end def __hash__

    def __repr__ (self) :
        return "%s: %s" % (self.src, self.script_type)
    # end def __repr__

    def __str__ (self) :
        return self.src
    # end def __str__

# end class Script

class JS_On_Ready (_Object_) :
    """A javascript code which should be executed once the document is loaded"""

    __metaclass__ = TFL.Meta.M_Unique_If_Named

    default_rank  = object ()
    name          = None

    def __init__ (self, code, rank = default_rank, ** kw) :
        if isinstance (code, self.__class__) :
            if rank is self.default_rank :
                rank   = code.rank
            code       = code.code
        elif rank is self.default_rank :
            rank       = 0
        self.code      = code
        if self.rank :
            self.rank  = rank
        self.pop_to_self (kw, "name")
    # end def __init__

    def __str__ (self) :
        return self.code
    # end def __str__

# end class JS_On_Ready

class Media_List (TFL.Meta.Object) :
    """Model a list of media objects"""

    def __init__ (self, name, media, mobs) :
        self.name  = name
        self.media = media
        self.mobs  = list (mobs)
    # end def __init__

    def add (self, * mob) :
        self.mobs.extend (self._sanitized (mob))
    # end def add

    @Once_Property
    def values (self) :
        return tuple (self._gen_all ())
    # end def values

    def _gen_all (self) :
        for mob in self._gen_own () :
            for o in mob.objects :
                yield o
        name = self.name
        for child in self.media.children :
            for mob in getattr (child, name) :
                yield mob
    # end def _gen_all

    def _gen_own (self) :
        for mob in self.mobs :
            yield mob
    # end def _gen_own

    def __len__ (self) :
        return len (self.values)
    # end def __len__

    def __nonzero__ (self) :
        return bool (self.values)
    # end def __nonzero__

    def __iter__ (self) :
        return iter (self.values)
    # end def __iter__

    def __str__ (self) :
        return "\n".join (str (v) for v in self)
    # end def __str__

    def _sanitized (self, mobs) :
        Mob_Type = self.Mob_Type
        if Mob_Type :
            return Mob_Type._sanitized (mobs)
        else :
            return mobs
    # end def _sanitized

# end class Media_List

class Media_List_Unique (Media_List) :
    """Model a list of unique media objects (filters duplicates)."""

    def _gen_all (self) :
        return TFL.uniq (self.__super._gen_all ())
    # end def _gen_all

# end class Media_List_Unique

class Media_List_href (Media_List) :
    """Model a list of media objects with href"""

    prefix   = None
    Mob_Type = None

    def __init__ (self, name, media, mobs) :
        self.__super.__init__ (name, media, tuple (self._sanitized (mobs)))
    # end def __init__

    def _gen_own (self) :
        prefix = self.prefix
        url    = self.media.url
        for mob in self.__super._gen_own () :
            href = mob.href
            if href and not href.startswith (("http://", "https://", "/")) :
                mob.href = pjoin \
                    (* (x for x in (url, prefix, href) if x is not None))
            yield mob
    # end def _gen_own

# end class Media_List_href

class Media_List_CSSL (Media_List_href, Media_List_Unique) :
    """Model a list of CSS_Link objects"""

    prefix   = "styles"
    Mob_Type = CSS_Link

# end class Media_List_CSSL

class Media_List_JSOR (Media_List_Unique) :
    """Model a list of javascript on-ready objects"""

    Mob_Type = JS_On_Ready

    def __init__ (self, name, media, mobs) :
        self.__super.__init__ (name, media, tuple (self._sanitized (mobs)))
    # end def __init__

    @Once_Property
    def values (self) :
        return tuple (sorted (self._gen_all (), key = lambda mob : mob.rank))
    # end def values

# end class Media_List_JSOR

class Media_List_Rell (Media_List_href) :

    prefix   = None
    Mob_Type = Rel_Link

# end class Media_List_Rell

class Media_List_Script (Media_List_href, Media_List_Unique) :
    """Model a list of script objects"""

    prefix   = "js"
    Mob_Type = Script

    @Once_Property
    def values (self) :
        return tuple (sorted (self._gen_all (), key = lambda mob : mob.rank))
    # end def values

# end class Media_List_Script

class Media (TFL.Meta.Object) :
    """
       >>> class Media (Media) :
       ...     url = "/test/"
       ...
       >>> NL = chr (10)

       >>> m = Media (css_links = ("a.css", "/b/c.css"),
       ...       scripts = ("foo.js", "bar.js", "http://baz.js"))
       >>> print NL.join (repr (l) for l in m.css_links)
       all: /test/styles/a.css
       all: /b/c.css
       >>> tuple (str (l) for l in m.scripts)
       ('/test/js/foo.js', '/test/js/bar.js', 'http://baz.js')
       >>> n = Media (("/test/styles/a.css", CSS_Link ("c.css", media_type = "screen")))
       >>> print NL.join (repr (l) for l in n.css_links)
       all: /test/styles/a.css
       screen: /test/styles/c.css
       >>> tuple (str (l) for l in n.scripts)
       ()
       >>> q = Media (scripts = ("qux.js", ), children = (m, n))
       >>> print NL.join (repr (l) for l in q.css_links)
       all: /test/styles/a.css
       all: /b/c.css
       screen: /test/styles/c.css
       >>> "; ".join (str (l) for l in q.scripts)
       '/test/js/qux.js; /test/js/foo.js; /test/js/bar.js; http://baz.js'
    """

    url = "/media"

    def __init__ (self, css_links = (), scripts = (), js_on_ready = (), rel_links = (), children = (), ** kw) :
        self.__dict__.update (kw)
        self.css_links   = Media_List_CSSL   ("css_links",   self, css_links)
        self.scripts     = Media_List_Script ("scripts",     self, scripts)
        self.js_on_ready = Media_List_JSOR   ("js_on_ready", self, js_on_ready)
        self.rel_links   = Media_List_Rell   ("rel_links",   self, rel_links)
        self.children    = list              (children)
    # end def __init__

    @classmethod
    def from_list (cls, medias, ** kw) :
        to_add = dict ((n, v) for n, v in kw.iteritems () if v)
        if len (medias) == 1 and not to_add :
            result = medias [0]
        else :
            result = \
                GTW.Media (children = medias) if (medias or to_add) else None
        for n, v in to_add.iteritems () :
            getattr (result, n).add (* v)
        return result
    # end def from_list

# end class Media

if __name__ != "__main__":
    GTW._Export ("*")
### __END__ GTW.Media
