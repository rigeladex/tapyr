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
#    DJO.NAV
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
#    25-May-2008 (MG) `_setup_url_resolver` fixed to work without a parent as
#                     well
#    27-May-2008 (CT) `translator` added
#     8-Jul-2008 (CT) `implicit` added
#     8-Jul-2008 (CT) `Root.universal_view` and `Root.page_from_href` added
#     9-Jul-2008 (CT) `_get_child` added to `_Site_Entity_`, `Gallery`, and
#                     `Dir`
#     9-Jul-2008 (CT) `Gallery` changed to consider `delegation_view`
#     9-Jul-2008 (CT) `_Dir_.rendered` added
#     9-Jul-2008 (CT) Default for `delegation_view` moved from `Dir` to `Root`
#                     (and handling changed to allow `True` for
#                     `delegation_view`, too)
#    10-Jul-2008 (CT) `_view` factored from `universal_view`
#    10-Jul-2008 (CT) `Model_Admin` started
#    11-Jul-2008 (CT) `Model_Admin` continued
#    15-Jul-2008 (CT) Use `DJO.Model_Form` instead of plain old
#                     newsforms.Model_Form
#    15-Jul-2008 (CT) `Site_Admin` added
#    29-Aug-2008 (CT) s/super(...)/__m_super/
#    23-Sep-2008 (CT) `_Site_Entity_.rendered` changed to always put
#                     `page = self` into context (otherwise delegation from
#                     `Dir` to `Page` doesn't work properly)
#    25-Sep-2008 (CT) `Alias` added
#    26-Sep-2008 (CT) Optional argument `nav_page` added to `rendered`
#     3-Oct-2008 (CT) Properties `has_children` and `Type` added
#     3-Oct-2008 (CT) `context ["NAV"]` added to `rendered`
#     3-Oct-2008 (CT) `Alias` changed to inherit from `Page`,
#                     `Alias.__getattr__` added
#     3-Oct-2008 (MG) `populate_naviagtion_root`, `url_pattern`, and
#                     `delegation_view` removed (not needed anymore)
#     5-Oct-2008 (MG) `Bypass_URL_Resolver` added
#     5-Oct-2008 (MG) `none_result` and `no_entries_template` added
#     6-Oct-2008 (MG) `none_result` and` no_entries_template` replaced by
#                     `empty_template`
#                     `_Site_Entity_._view` raise `Http404` in case
#                     `rendered` returns `None`
#                     `Root.url_pattern` and friends added
#     7-Oct-2008 (CT) Esthetics (and spelling)
#     7-Oct-2008 (CT) Gallery changed to use a directory-style `href`
#     7-Oct-2008 (CT) `empty_template` moved from `_Dir_` to `Root`
#     7-Oct-2008 (CT) `auto_delegate` added to support statically generated
#                     files
#     7-Oct-2008 (CT) `page_from_href` changed to try `href` with a trailing
#                     slash, too
#     9-Oct-2008 (CT) Use `.top` to access class variables like
#                     `url_patterns` and `handlers` that might be redefined
#                     for the instance of `Root`
#     9-Oct-2008 (MG) `Root.pre_first_request_hooks` added and used in
#                     `universal_view`
#     9-Oct-2008 (MG) `Site_Admin.__init__` allow models without `admin_args`
#                     set
#    10-Oct-2008 (CT) Esthetics
#                     (and use `.top` to access `pre_first_request_hooks`)
#    10-Oct-2008 (CT) Guard for `DoesNotExist` added to `Changer.rendered`
#                     and `Deleter._view`
#    10-Oct-2008 (MG)  `Site_Admin.__init__` use `unicode
#                      (m._meta.verbose_name_plural)` to resolve the
#                      translation proxy
#    14-Oct-2008 (CT) `_load_view` factored and used in `Url_Pattern.resolve`
#    15-Oct-2008 (CT) `Model_Admin.has_children` and `Model_Admin.prefix` added
#    15-Oct-2008 (CT) `Model_Admin.Field.formatted` changed to not apply
#                     `str` to values of type `unicode`
#    15-Oct-2008 (CT) `Site_Admin.rendered` simplified and then commented out
#    16-Oct-2008 (CT) `Model_Admin._get_child` changed to set proper `name`
#                     for `Changer`
#    17-Oct-2008 (CT) `login_required` added
#    18-Oct-2008 (CT) Factored from monolithic `DJO.Navigation`
#    ««revision-date»»···
#--

from   __future__               import with_statement

from   _DJO                     import DJO
from   _TFL                     import TFL
import _DJO._NAV.Base

from   _TFL.Filename            import *
from   _TFL.Regexp              import *
from   _TFL._Meta.Once_Property import Once_Property
from   _TFL                     import sos

from   posixpath import join as pjoin, normpath as pnorm

import textwrap

class Page_ReST (DJO.NAV.Page) :
    """Model one page generated from re-structured text."""

    date = ""

    @Once_Property
    def contents (self) :
        return self.markup_to_html (unicode (self.src_contents))
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

class Dyn_Slice_ReST_Dir (DJO.NAV._Site_Entity_) :
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
    DJO.NAV._Export ("*")
### __END__ DJO.NAV.ReST
