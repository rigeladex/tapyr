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
#     3-May-2008 (CT) `Dir.__init__` refactored
#     5-May-2008 (CT) Changed `add_entries` and `from_nav_list_file` to keep
#                     `Type` and `Dir_Type` separate
#     5-May-2008 (CT) Changed `add_entries` to leave `sub_dir` in `d` (and
#                     not pass it positionally to `new_sub_dir`)
#     5-May-2008 (CT) Fixed typo in `new_page` (s/h/href/)
#     6-May-2008 (CT) Changed `new_sub_dir` to keep `src_dir` and `sub_dir`
#                     separate
#     8-May-2008 (CT) `Gallery`, `Photo`, and `Thumbnail` added
#     8-May-2008 (CT) `from_nav_list_file` changed to pass `globals` to
#                     `execfile` (too allow tings like `Type = Gallery` there)
#     9-May-2008 (CT) `_Meta_` and `Table` added
#     9-May-2008 (CT) `top` made into class variable
#    10-May-2008 (MG) `add_page` and `add_sub_dir` fixed
#    10-May-2008 (MG) Use `posixpath` instead of `os.path` (we deal with urls
#                     here not with a files system)
#    12-May-2008 (MG) `url_resolver` and `url_patterns` added
#    12-May-2008 (MG) Context processor `populate_naviagtion_root` added
#    12-May-2008 (MG) `new_sub_dir` and `new_page`: don't normpath `src_dir`
#                     and `href`
#    12-May-2008 (MG) `rhref` added
#    14-May-2008 (CT) `file_stem` fixed
#    14-May-2008 (CT) `Page.__init__` changed to use `self.url_resolver`
#                     instead of `self.parent.url_resolver`
#    14-May-2008 (CT) `dump` added
#    14-May-2008 (CT) `href` converted to property based on new attribute `name`
#    14-May-2008 (CT) `Page.dir` and `Page.level` converted from attributes
#                     to properties
#    14-May-2008 (CT) `Root` and `_Dir_` factored from `Dir`
#    14-May-2008 (CT) `from_dict_list` added
#    14-May-2008 (CT) Bug fixes in `add_entries` and `from_dict_list`
#    ««revision-date»»···
#--

from   _TFL import TFL
from   _DJO                     import DJO

from   _TFL.defaultdict         import defaultdict
from   _TFL.Filename            import *
from   _TFL.predicate           import pairwise
from   _TFL.Record              import Record
from   _TFL._Meta.Once_Property import Once_Property
from   _TFL                     import sos

import _TFL._Meta.Object

from   posixpath                import join as pjoin, normpath as pnorm

### To-Do:
### - Root class: factor from Dir
###   * dump: dump navigation tree into string that's executable python code
###     (using new classmethod `from_list_of_dicts`)
### - Dyn_Dir
###

class _Meta_ (TFL.Meta.Object.__class__) :

    def __call__ (cls, * args, ** kw) :
        result = super (_Meta_, cls).__call__ (* args, ** kw)
        result.top.Table [result.href] = result
        return result
    # end def __call__

# end class _Meta_

class _Site_Entity_ (TFL.Meta.Object) :
    """Model one entity that is part of a web site."""

    __metaclass__   = _Meta_

    desc            = ""
    href            = ""
    rhref           = None
    input_encoding  = "iso-8859-15"
    title           = ""

    parent          = None

    _dump_type      = "dict"

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
    def abs_href (self) :
        result = self.href
        if not result.startswith ("/") :
            return "/%s" % (result, )
        return result
    # end def abs_href

    @Once_Property
    def base (self) :
        return Filename (self.name).base
    # end def base

    @Once_Property
    def file_stem (self) :
        return pnorm (pjoin (self.prefix, self.base))
    # end def file_stem

    @Once_Property
    def href (self) :
        return pnorm (pjoin (self.prefix, self.name))
    # end def file_stem

    def above (self, link) :
        return (not self.level) or \
            (   self.level <= link.level
            and ((not self.prefix) or link.prefix.startswith (self.prefix))
            )
    # end def above

    def dump (self, tail = None) :
        level  = self.level
        indent = "  " * (level + 3)
        sep    = "\n%s, " % (indent, )
        lines  = sep.join \
            ("%s = %r" % (k, v) for (k, v) in sorted (self._kw.iteritems ()))
        if tail :
            lines = "%s%s%s" % (lines, sep, tail)
        return "%s\n%s( Type = %s%s%s\n%s)" % \
            ( self._dump_type
            , indent, self.__class__.__name__, sep, lines, indent
            )
    # end def dump

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
    url_patterns    = ()

    def __init__ (self, * args, ** kw) :
        self.__super.__init__ (* args, ** kw)
        if self.url_resolver and self.url_patterns :
            self.url_resolver.add_nav_pattern (self, * self.url_patterns)
    # end def __init__

    @property
    def dir (self) :
        return self.parent.title
    # end def dir

    @property
    def level (self) :
        return self.parent.level + 1
    # end def dir

# end class Page

class Gallery (Page) :
    """Model a photo gallery that's part of a web site."""

    template = "gallery.html"

    def __init__ (self, pic_dir, parent = None, ** kw) :
        self.im_dir   = pjoin (pic_dir, "im")
        self.th_dir   = pjoin (pic_dir, "th")
        self._photos  = []
        self._thumbs  = []
        base          = Filename (pic_dir).base
        self.name     = "%s.html" % (base, )
        self.__super.__init__ (parent, pic_dir = pic_dir, ** kw)
        self.src_dir  = pjoin (getattr (self, "prefix", ""), base)
    # end def __init__

    @property
    def photos (self) :
        if not self._photos :
            self._read_entries ()
        return self._photos
    # end def photos

    @property
    def thumbnails (self) :
        if not self._thumbs :
            self._read_entries ()
        return self._thumbs
    # end def thumbnails

    def _read_entries (self) :
        photos = self._photos
        thumbs = self._thumbs
        images = sorted \
            (sos.expanded_globs (pjoin (self.im_dir, "*.jpg")))
        i = 0
        for im in images :
            name = Filename (im).base
            th   = pjoin (self.th_dir, "%s.jpg" % name)
            if sos.path.exists (th) :
                i     += 1
                title  = "%s %d/%d" % (self.title, i, len (images))
                desc   = "%s %d/%d" % (self.desc,  i, len (images))
                photo  = Photo     \
                    ( im
                    , parent = self
                    , desc   = desc
                    , title  = title
                    )
                thumb  = Thumbnail \
                    ( th, photo
                    , parent = self
                    , desc   = desc
                    , title  = title
                    )
                photos.append (photo)
                thumbs.append (thumb)
        prev  = None
        for curr, next in pairwise (photos + [None]) :
            curr.prev = prev
            curr.next = next
            prev      = curr
    # end def _read_entries

# end class Gallery

class _Photo_ (Page) :

    _size     = None

    def __init__ (self, name, parent, ** kw) :
        self.__super.__init__ (name = name, src = name, parent = parent, ** kw)
    # end def __init__

    @property
    def height (self) :
        size = self.size
        if size is not None :
            return size [1]
    # end def height

    @property
    def size (self) :
        if self._size is None :
            from PIL import Image
            img = Image.open (self.name)
            self._size = img.size
        return self._size
    # end def size

    @property
    def width (self) :
        size = self.size
        if size is not None :
            return size [0]
    # end def width

# end class _Photo_

class Photo (_Photo_) :
    """Model one page of a web site displaying a single photo of a gallery."""

    next      = None
    prev      = None
    template  = "photo.html"
    thumb     = None

# end class Photo

class Thumbnail (_Photo_) :
    """Model a thumbnail of a photo."""

    def __init__ (self, name, photo, parent, ** kw) :
        self.__super.__init__ (name, parent, ** kw)
        self.photo  = photo
        photo.thumb = self
    # end def __init__

# end class Thumbnail

class _Dir_ (_Site_Entity_) :
    """Model one directory of a web site."""

    Page            = Page
    url_resolver    = None

    dir             = ""
    sub_dir         = ""

    def __init__ (self, parent = None, ** kw) :
        self.__super.__init__ (parent, ** kw)
        self.context  = dict ()
        self._entries = []
        if (   self.url_resolver
           and not isinstance (self.url_resolver, DJO.Url_Resolver)
           ) :
            self.url_resolver = self.url_resolver \
                ("^%s" % (self.sub_dir, ), self.sub_dir)
    # end def __init__

    @classmethod
    def from_nav_list_file (cls, src_dir, parent = None, ** kw) :
        """Return a new `Dir` filled with information read from the file
           `navigation.list` in `src_dir`.
        """
        result = cls   (src_dir, parent = parent, ** kw)
        nl     = pjoin (src_dir, "navigation.list")
        execfile       (nl, globals (), result.context)
        result.add_entries \
            (result.context ["own_links"], Dir_Type = Dir.from_nav_list_file)
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

    def add_entries (self, list_of_dicts, ** kw) :
        entries   = self._entries
        Dir_Type  = kw.pop ("Dir_Type", self.__class__)
        for d in list_of_dicts :
            s     = d.get ("sub_dir", None)
            if kw :
                d = dict (kw, ** d)
            if s :
                Type  = d.pop ("Type", Dir_Type)
                entry = self.new_sub_dir (Type = Type, ** d)
            else :
                entry = self.new_page    (** d)
            entries.append (entry)
    # end def add_entries

    def add_page (self, ** kw) :
        """Add a page with the attributes passed as keyword arguments."""
        result = self.new_page (** kw)
        self._entries.append (result)
        return result
    # end def add_page

    def add_sub_dir (self, sub_dir, ** kw) :
        result = self.new_sub_dir (sub_dir, ** kw)
        self._entries.append (result)
        return result
    # end def add_sub_dir

    def dump (self) :
        level  = self.level
        indent = "  " * (level + 5)
        sep    = "\n%s" % (indent, )
        sep_c  = "%s, " % sep
        tail = sep_c.join \
            (   "\n      ".join (owl.dump ().split ("\n"))
            for owl in self.own_links
            )
        return self.__super.dump \
            (tail = "_entries =%s[ %s%s]" % (sep, tail, sep))
    # end def dump

    def new_page (self, ** kw) :
        Type         = kw.pop ("Type", self.Page)
        href         = kw.pop ("href", None)
        if href is not None :
            ### legacy lifting
            assert not "name" in kw
            kw ["name"] = href
        result = Type (parent = self, ** kw)
        return result
    # end def new_page

    def new_sub_dir (self, sub_dir, ** kw) :
        Type    = kw.pop ("Type", self.__class__)
        entries = kw.pop ("_entries", None)
        src_dir = pjoin (self.src_dir, sub_dir)
        result  = Type (src_dir, parent = self, sub_dir = sub_dir, ** kw)
        if entries :
            result.add_entries (entries)
        return result
    # end def new_sub_dir

    def __str__ (self) :
        return "%s; href : %r, %s" % \
            (self.src_dir, self.href, self.__super.__str__ ())
    # end def __str__

# end class _Dir_

class Dir (_Dir_) :
    """Model one directory of a web site."""

    def __init__ (self, src_dir, parent, ** kw) :
        sub_dir      = kw.get ("sub_dir", "")
        self.level   = parent.level + 1
        self.parents = parent.parents + [parent]
        self.prefix  = sos.path.join \
            (* [p for p in (parent.prefix, sub_dir) if p])
        self.src_dir  = src_dir
        self.__super.__init__ (parent = parent, ** kw)
        if parent.url_resolver and parent.url_resolver != self.url_resolver :
            parent.url_resolver.append_pattern (self.url_resolver)
    # end def __init__

# end class Dir

class Root (_Dir_) :

    name       = "/"

    _dump_type = "DJO.Navigation.Root.from_dict_list \\"

    def __init__ (self, src_dir, ** kw) :
        _Site_Entity_.top = self
        self.parents      = []
        self.prefix       = ""
        self.Table        = {}
        self.level        = -1
        self.__super.__init__ (src_dir = src_dir, ** kw)
    # end def __init__

    @classmethod
    def from_dict_list (cls, ** kw) :
        Dir_Type = kw.pop ("Dir_Type", Dir)
        Type     = kw.pop ("Type",     cls)
        entries  = kw.pop ("_entries", None)
        result   = Type (** kw)
        if entries :
            result.add_entries (entries, Dir_Type = Dir_Type)
        return result
    # end def from_dict_list

# end class Root

def populate_naviagtion_root (request) :
    return dict (NAVIGATION = _Site_Entity_.top)
# end def populate_naviagtion_root

if __name__ != "__main__":
    DJO._Export_Module ()
### __END__ Navigation
