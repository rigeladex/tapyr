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
#    14-May-2008 (MG) `Page.parents` added
#    14-May-2008 (MG) `rhref` removed and `_Dir_.url_resolver` removed
#    14-May-2008 (MG) `url_patterns` moved up into `_Site_Entity_`
#    16-May-2008 (MG) `_Site_Entity_.__init__`: Move `url_resolver` in here
#                     (from `_Dir_) and added support for `_Site_Entity_`
#                     which don't have there own url resolver
#    16-May-2008 (MG) `url_resolver_pattern` added
#    16-May-2008 (MG) `_Site_Entity_.href` fixed in case of an empfy `href`
#    17-May-2008 (MG) `_Dir_.delegation_view` added
#    18-May-2008 (MG) Check `src_dir` against None to allow an empty `src_dir`
#    19-May-2008 (CT) Missing import for `Url_Resolver` added
#    20-May-2008 (MG) `_Site_Entity_.relative_to` added, url resolver
#                     handling cleanup
#    20-May-2008 (MG) Bug with `delegation_view` fixed
#    21-May-2008 (MG) `url_resolver_pattern` removed
#    21-May-2008 (CT) `copyright` property added
#    22-May-2008 (MG) `_Site_Entity_.view` added,
#                     `_Dir_.default_view_pattern` added
#                     `Url_Pattern` renamed to `Single_Url_Pattern`
#    22-May-2008 (CT) s/class_method/unbound_method/ (Truth in Advertising)
#    22-May-2008 (CT) `_Site_Entity_.__init__` streamlined
#    22-May-2008 (CT) `_formatted_attr` added to `dump`
#    22-May-2008 (CT) `_Dir_.dump` changed to use `_entries` instead of
#                     `own_links`
#    23-May-2008 (CT) `rendered` added
#    23-May-2008 (CT) Semantics of `_Photo_.name` changed (so that `href`
#                     works properly)
#    23-May-2008 (CT) `Page_ReST` and `Page_ReST_F` added
#    23-May-2008 (CT) `Dyn_Slice_ReST_Dir` added
#    27-May-2008 (CT) `translator` added
#    ««revision-date»»···
#--

from   __future__               import with_statement

from   _TFL                     import TFL
from   _DJO                     import DJO

import _DJO.Url_Resolver

from   _TFL.defaultdict         import defaultdict
from   _TFL.Filename            import *
from   _TFL.predicate           import pairwise
from   _TFL.Record              import Record
from   _TFL.Regexp              import *
from   _TFL._Meta.Once_Property import Once_Property
from   _TFL                     import sos

import _TFL._Meta.Object

from   posixpath import join as pjoin, normpath as pnorm, commonprefix

import textwrap
import time


### To-Do:
### - Dyn_Dir

class _Meta_ (TFL.Meta.Object.__class__) :

    def __call__ (cls, * args, ** kw) :
        result = super (_Meta_, cls).__call__ (* args, ** kw)
        if result.href is not None :
            result.top.Table [result.href] = result
        return result
    # end def __call__

# end class _Meta_

class _Site_Entity_ (TFL.Meta.Object) :
    """Model one entity that is part of a web site."""

    __metaclass__   = _Meta_

    desc            = ""
    href            = ""
    input_encoding  = "iso-8859-15"
    title           = ""
    url_patterns    = ()

    parent          = None
    view            = None

    _dump_type      = "dict"

    def __init__ (self, parent = None, ** kw) :
        self._kw    = kw
        self.parent = parent
        if "input_encoding" in kw :
            encoding = kw ["input_encoding"]
        else :
            encoding = getattr (parent, "input_encoding", self.input_encoding)
        for k, v in kw.iteritems () :
            if isinstance (v, str) :
                v = unicode (v, encoding, "replace")
            setattr (self, k, v)
        self._setup_url_resolver (parent, kw)
        view = self.view
        if view :
            unbound_method = "view" not in kw
            if unbound_method :
                ### the view function is an instance method -> we need to
                ### pass the unbound method instead
                view = self.__class__.view
            self.url_resolver.add_view_function (self, view, unbound_method)
        if hasattr (self, "url_resolver") and self.url_patterns :
            self.url_resolver.add_nav_pattern (self, * self.url_patterns)
    # end def __init__

    @Once_Property
    def abs_href (self) :
        result = self.href
        if not result.startswith ("/") :
            return "/%s" % (result, )
        return result
    # end def abs_href

    def above (self, link) :
        return (not self.level) or \
            (   self.level <= link.level
            and ((not self.prefix) or link.prefix.startswith (self.prefix))
            )
    # end def above

    @Once_Property
    def base (self) :
        return Filename (self.name).base
    # end def base

    @Once_Property
    def copyright (self) :
        year  = time.localtime ().tm_year
        start = self.copyright_start
        return dict \
            ( year   = "-".join ("%s" % y for y in (start, year) if y)
            , holder = self.owner
            )
    # end def copyright

    def dump (self, tail = None) :
        level  = self.level
        indent = "  " * (level + 3)
        sep    = "\n%s, " % (indent, )
        lines  = sep.join \
            (   "%s = %s" % (k, self._formatted_attr (k))
            for k in sorted (self._kw)
            )
        if tail :
            lines = "%s%s%s" % (lines, sep, tail)
        return "%s\n%s( Type = %s%s%s\n%s)" % \
            ( self._dump_type
            , indent, self.__class__.__name__, sep, lines, indent
            )
    # end def dump

    @Once_Property
    def file_stem (self) :
        return pnorm (pjoin (self.prefix, self.base))
    # end def file_stem

    @Once_Property
    def href (self) :
        href = pjoin (self.prefix, self.name)
        if href :
            return pnorm (href)
        return ""
    # end def href

    @property
    def nav_links (self) :
        yield self
    # end def nav_links

    def relative_to (self, url, href = None) :
        href          = href or self.href
        common_prefix = commonprefix ((href, url))
        return href.replace (common_prefix, u"")
    # end def relative_to

    @Once_Property
    def render_to_string (self) :
        from _DJO.Render import to_string
        return to_string
    # end def render_to_string

    def rendered (self, context = None) :
        if context is None :
            context = dict (page = self)
        result = self.render_to_string (self.template, context, self.encoding)
        if self.translator :
            result = self.translator (result)
        return result
    # end def rendered

    def _formatted_attr (self, name) :
        v = getattr (self, name)
        if isinstance (v, unicode) :
            v = 'u"""%s"""' % (v.encode (self.input_encoding))
        return v
    # end def _formatted_attr

    def _setup_url_resolver (self, parent, kw) :
        url_resolver = kw.get ("url_resolver")
        if url_resolver :
            ### this entity has it's own url resolver
            if not isinstance (url_resolver, DJO.Url_Resolver) :
                ### looks like it's just a class -> let's convert it to an
                ### instance
                pattern = self.relative_to \
                    (self.parent.url_resolver.nav_href, self.file_stem)
                self.url_resolver = self.url_resolver \
                    ( "^%s" % (pattern, ), pattern
                    , default_view_pattern = kw.get ("default_view_pattern", {})
                    )
            if parent :
                ### this entity has a parent so let's add our own url
                ### resolver to the parents to build the resolve chain
                parent.url_resolver.append_pattern (self.url_resolver)
            self.url_resolver.set_nav (self)
        return url_resolver
    # end def _setup_url_resolver

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

    @Once_Property
    def parents (self) :
        return self.parent.parents + [self.parent]
    # end def parents

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

    def __init__ (self, pic_dir, parent, ** kw) :
        self.im_dir   = pjoin (pic_dir, "im")
        self.th_dir   = pjoin (pic_dir, "th")
        self._photos  = []
        self._thumbs  = []
        base          = Filename (pic_dir).base
        self.name     = "%s.html" % (base, )
        self.__super.__init__ (parent, pic_dir = pic_dir, ** kw)
        self.src_dir  = self.prefix = pjoin (parent.prefix, base)
    # end def __init__

    @Once_Property
    def href (self) :
        href = pjoin (self.parent.prefix, self.name)
        if href :
            return pnorm (href)
        return ""
    # end def href

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
                    ( "%s.html" % (name, ), im
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

    def __init__ (self, name, src, parent, ** kw) :
        self.__super.__init__ (name = name, src = src, parent = parent, ** kw)
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
            img = Image.open (self.src)
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

    def __init__ (self, src, photo, parent, ** kw) :
        self.__super.__init__ (photo.name, src, parent, ** kw)
        self.photo  = photo
        photo.thumb = self
    # end def __init__

# end class Thumbnail

class _Dir_ (_Site_Entity_) :
    """Model one directory of a web site."""

    Page            = Page

    dir             = ""
    sub_dir         = ""
    delegation_view = None

    def __init__ (self, parent = None, ** kw) :
        self.__super.__init__ (parent, ** kw)
        self._entries = []
        if self.delegation_view :
            resolver = self.url_resolver
            resolver.prepend_pattern \
                ( DJO.Single_Url_Pattern
                    ( u"^%s$" % (self.relative_to (resolver.nav_href), )
                    , self.delegation_view
                    , nav = self
                    )
                )
    # end def __init__

    @classmethod
    def from_nav_list_file (cls, src_dir, parent = None, ** kw) :
        """Return a new `Dir` filled with information read from the file
           `navigation.list` in `src_dir`.
        """
        context = {}
        nl      = pjoin (src_dir, "navigation.list")
        result  = cls   (src_dir, parent = parent, ** kw)
        execfile        (nl, globals (), context)
        result.add_entries \
            (context ["own_links"], Dir_Type = Dir.from_nav_list_file)
        return result
    # end def from_nav_list_file

    @property
    def href (self) :
        if not self.delegation_view :
            if self._entries :
                return first (self.own_links).href
        return pjoin (self.prefix, u"")
    # end def href

    @property
    def own_links (self) :
        for e in self._entries :
            for nl in e.nav_links :
                yield nl
    # end def own_links

    @property
    def own_links_transitive (self) :
        for e in self.own_links :
            yield e
            if isinstance (e, Dir) :
                for ee in e.own_links_transitive :
                    yield ee
    # end def own_links_transitive

    def add_entries (self, list_of_dicts, ** kw) :
        entries   = self._entries
        Dir_Type  = kw.pop ("Dir_Type", self.__class__)
        for d in list_of_dicts :
            s     = d.get ("sub_dir", None)
            if kw :
                d = dict (kw, ** d)
            if s is not None :
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
            (   "\n      ".join (e.dump ().split ("\n"))
            for e in self._entries
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
            (* [p for p in (parent.prefix, sub_dir) if p is not None])
        self.src_dir  = src_dir
        self.__super.__init__ (parent = parent, ** kw)
    # end def __init__

# end class Dir

class Root (_Dir_) :

    copyright_start = None
    name            = "/"
    owner           = None
    src_root        = ""
    translator      = None

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

### a django TEMPLATE_CONTEXT_PROCESSORS which adds a variable named
### `NAVIGATION` to all `RequestContext` instances
def populate_naviagtion_root (request) :
    return dict (NAVIGATION = _Site_Entity_.top)
# end def populate_naviagtion_root

class Page_ReST (Page) :
    """Model one page generated from re-structured text."""

    date = ""

    @Once_Property
    def contents (self) :
        return self.markup_to_html (self.src_contents)
    # end def contents

    @Once_Property
    def markup_to_html (self) :
        from django.contrib.markup.templatetags.markup \
            import restructuredtext
        return restructuredtext
    # end def markup_to_html

# end class Page_ReST

class Page_ReST_F (Page_ReST) :
    """Model one page generated from re-structured text stored in file."""

    src_extension = ".txt"

    @Once_Property
    def src_contents (self) :
        with open (self.src_path, "rb") as f :
            result = f.read ()
        return unicode (result.strip (), self.input_encoding, "replace")
    # end def src_contents

    @Once_Property
    def src_path (self) :
        return pjoin (self.src_root, self.file_stem + self.src_extension)
    # end def src_path

# end class Page_ReST_F

class Dyn_Slice_ReST_Dir (_Site_Entity_) :
    """Dynamic slice based on the re-structured files in a directory."""

    href          = None
    nav_info_pat  = Regexp \
        ( r"^\.\. *$"
          "\n"
          r" +<Nav-Info> *$"
          "\n"
            r"(?P<code>"
              r"(?:^ +\w+ *=.*$" "\n" r")+"
            r")"
          r" +</Nav-Info> *$"
        , re.MULTILINE
        )
    own_links     = ()
    src_extension = ".txt"
    _entries      = None

    @property
    def nav_links (self) :
        if self._entries is None :
            self._read_entries ()
        return self._entries
    # end def nav_links

    def _page_info (self, f) :
        result = {}
        with open (f, "rb") as f :
            src = unicode (f.read ().strip (), self.input_encoding, "replace")
        pat = self.nav_info_pat
        if pat.search (src) :
            exec textwrap.dedent (pat.code) in globals (), result
            result ["src_contents"] = pat.sub ("", src).strip ()
        return result
    # end def _page_info

    def _read_entries (self) :
        self._entries = entries = []
        add           = entries.append
        files         = sos.expanded_globs \
            ( pjoin
                (self.src_root, self.prefix, "*%s" % (self.src_extension, ))
            )
        parent        = self.parent
        Page_Type     = getattr (self, "Page_Type", Page_ReST)
        sort_key      = getattr (self, "sort_key", lambda x : (x.date, x.name))
        for f in files :
            info = self._page_info (f)
            if info :
                name = "%s.html" % (Filename (f).base, )
                info ["name"] = name
                add (Page_Type (parent = parent, ** info))
        entries.sort (key = sort_key, reverse = True)
    # end def _read_entries

# end class Dyn_Slice_ReST_Dir

if __name__ != "__main__":
    DJO._Export_Module ()
### __END__ Navigation
