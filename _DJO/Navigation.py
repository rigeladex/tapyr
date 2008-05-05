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
#    29-Apr-2008 (CT) Default for `input_encoding` defined as class variable
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

    desc            = ""
    href            = ""
    input_encoding  = "iso-8859-15"
    title           = ""

    parent          = None

    def __init__ (self, parent = None, ** kw) :
        self._kw    = kw
        self.parent = parent
        if "input_encoding" in kw :
            self.input_encoding = encoding = kw.pop ("input_encoding")
        else :
            encoding = getattr (parent, "input_encoding", self.input_encoding)
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

    def __str__ (self) :
        return ", ".join \
            ( "%s : %r" % (k, v) for (k, v) in sorted (self._kw.iteritems ()))
    # end def __str__

# end class _Site_Entity_

class Page (_Site_Entity_) :
    """Model one page of a web site."""

    own_links       = []

# end class Page

class Dir (_Site_Entity_) :
    """Model one directory of a web site."""

    Page            = Page

    dir             = ""
    sub_dir         = ""

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
    # end def __init__

    @classmethod
    def from_nav_list_file (cls, src_dir, parent = None, ** kw) :
        """Return a new `Dir` filled with information read from the file
           `navigation.list` in `src_dir`.
        """
        result = cls           (src_dir, parent = parent, ** kw)
        nl     = sos.path.join (src_dir, "navigation.list")
        execfile               (nl, result.context)
        result.add_entries \
            (result.context ["own_links"], Type = cls.from_nav_list_file)
        return result
    # end def from_nav_list_file

    @property
    def href (self) :
        if self._entries :
            return self._entries [0].href
    # end def href

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

    def add_entries (self, list_of_dicts, ** kw) :
        entries = self._entries
        for d in list_of_dicts :
            s = d.pop ("sub_dir", None)
            if kw :
                d = dict (kw, ** d)
            if s :
                entry = self.new_sub_dir (s, ** d)
            else :
                entry = self.new_page    (** d)
            entries.append (entry)
    # end def add_entries

    def add_page (self, ** kw) :
        """Add a page with the attributes passed as keyword arguments."""
        result = self.new_page (** kw)
        self.entries.append (result)
        return result
    # end def add_page

    def add_sub_dir (self, sub_dir, ** kw) :
        result = self.new_sub_dir (sub_dir, ** kw)
        self.entries.append (result)
        return result
    # end def add_sub_dir

    def new_page (self, ** kw) :
        Type   = kw.pop ("Type", self.Page)
        href   = kw.get ("href")
        prefix = self.prefix
        if href and prefix :
            kw ["href"] = sos.path.normpath (sos.path.join (prefix, h))
        result = Type \
            (parent = self, level = self.level + 1, dir = self.title, ** kw)
        return result
    # end def new_page

    def new_sub_dir (self, sub_dir, ** kw) :
        Type    = kw.pop ("Type", self.__class__)
        sub_dir = sos.path.normpath (sos.path.join (self.src_dir, sub_dir))
        result  = Type (sub_dir, parent = self, ** kw)
        return result
    # end def new_sub_dir

    def __str__ (self) :
        return "%s; href : %r, %s" % \
            (self.src_dir, self.href, self.__super.__str__ ())
    # end def __str__

# end class Dir

if __name__ != "__main__":
    DJO._Export_Module ()
### __END__ Navigation
