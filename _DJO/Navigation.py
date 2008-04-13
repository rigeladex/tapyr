# -*- coding: iso-8859-1 -*-
# Copyright (C) 2008 Mag. Christian Tanzer. All rights reserved
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
#    DJO.Navigation
#
# Purpose
#    Model navigation for web site
#
# Revision Dates
#    27-Feb-2008 (CT) Creation
#    28-Feb-2008 (CT) `encoding` added and used
#    13-Apr-2008 (CT) `own_links_transitive` corrected (needs to call
#                     `own_links_transitive`, not `own_links`, for sub_dirs)
#    ««revision-date»»···
#--

from   _TFL import TFL
from   _DJO import DJO

from   _TFL.defaultdict         import defaultdict
from   _TFL.Filename            import *
from   _TFL.Record              import Record
from   _TFL._Meta.Once_Property import Once_Property
from   _TFL                     import sos

import _TFL._Meta.Object

class _Site_Entity_ (TFL.Meta.Object) :
    """Model one entity that is part of a web site."""

    desc           = ""
    href           = ""
    title          = ""

    parent         = None

    def __init__ (self, parent = None, ** kw) :
        self.parent = parent
        encoding    = kw.get \
            ("input_encoding", getattr (parent, "input_encoding", "iso-8859-1"))
        for k, v in kw.iteritems () :
            if isinstance (v, str) :
                v = unicode (v, encoding, "replace")
            setattr (self, k, v)
    # end def __init__

    @Once_Property
    def base (self) :
        return Filename (self.href).base
    # end def base

    @Once_Property
    def file_stem (self) :
        return sos.path.normpath (sos.path.join (self.prefix, self.base))
    # end def file_stem

    def above (self, link) :
        return (not self.level) or \
            (   self.level <= link.level
            and ((not self.prefix) or link.prefix.startswith (self.prefix))
            )
    # end def above

    def __getattr__ (self, name) :
        if self.parent is not None :
            return getattr (self.parent, name)
        raise AttributeError, name
    # end def __getattr__

# end class _Site_Entity_

class Page (_Site_Entity_) :
    """Model one page of a web site."""

    own_links = []

# end class Page

class Dir (_Site_Entity_) :
    """Model one directory of a web site."""

    dir       = ""
    sub_dir   = ""

    def __init__ (self, src_dir, parent = None, ** kw) :
        self.__super.__init__ (parent, ** kw)
        self.src_dir  = src_dir
        self.parents  = []
        self.prefix   = prefix = ""
        if parent :
            self.parents = parent.parents + [parent]
            if self.sub_dir :
                self.prefix = prefix = sos.path.join \
                    (* [p for p in (parent.prefix, self.sub_dir) if p])
        self.context  = context = dict ()
        self.level    = level   = 1 + getattr (parent, "level", -2)
        self._entries = entries = []
        nl            = sos.path.join (src_dir, "navigation.list")
        execfile (nl, context)
        for d in context ["own_links"] :
            s = d.get ("sub_dir")
            if s :
                sub_dir = sos.path.normpath (sos.path.join (src_dir, s))
                entry   = self.__class__ (sub_dir, parent = self, ** d)
            else :
                h = d.get ("href")
                if h and prefix :
                    d ["href"] = sos.path.normpath (sos.path.join (prefix, h))
                entry = Page \
                    (parent = self, level = level + 1, dir = self.title, ** d)
            entries.append (entry)
        if entries :
            self.href = entries [0].href
    # end def __new__

    @property
    def own_links (self) :
        for e in self._entries :
            if isinstance (e, Dir) :
                if e.href :
                    yield e
            else :
                yield e
    # end def own_links

    @property
    def own_links_transitive (self) :
        for e in self._entries :
            if isinstance (e, Dir) :
                if e.href :
                    yield e
                for ee in e.own_links_transitive :
                    yield ee
            else :
                yield e
    # end def own_links_transitive

    @property
    def top (self) :
        if self.parents :
            return self.parents [0]
        return self
    # end def top

# end class Dir

if __name__ != "__main__":
    DJO._Export_Module ()
### __END__ Navigation
