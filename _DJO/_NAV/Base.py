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
#    DJO.NAV.Base
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

from   _DJO                     import DJO
from   _TFL                     import TFL
import _DJO._Nav

from   _TFL._Meta.Once_Property import Once_Property
from   _TFL.Filename            import *
from   _TFL                     import sos

import _TFL._Meta.M_Class
import _TFL._Meta.Object

from   posixpath import join as pjoin, normpath as pnorm, commonprefix

import time

def _load_view (name) :
    from django.core.exceptions   import ViewDoesNotExist
    from django.core.urlresolvers import get_mod_func
    mod_name, func_name = get_mod_func (name)
    try:
        return getattr (__import__(mod_name, {}, {}, ['']), func_name)
    except (ImportError, AttributeError), e:
        raise ViewDoesNotExist ("Tried %s. Error was: %s" % (name, e))
# end def _load_view

class _Meta_ (TFL.Meta.M_Class) :

    def __call__ (cls, * args, ** kw) :
        result = cls.__m_super.__call__ (* args, ** kw)
        if result.href is not None and not result.implicit :
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
    top             = None

    implicit        = False
    parent          = None

    _dump_type      = "dict"

    def __init__ (self, parent = None, ** kw) :
        self._kw    = kw
        self.parent = parent
        if "input_encoding" in kw :
            encoding = kw ["input_encoding"]
        else :
            encoding = getattr (parent, "input_encoding", self.input_encoding)
        self._login_required = kw.pop ("login_required", False)
        for k, v in kw.iteritems () :
            if isinstance (v, str) :
                v = unicode (v, encoding, "replace")
            try :
                setattr (self, k, v)
            except AttributeError, exc :
                print self.href or "Navigation.Root", k, v, "\n   ", exc
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

    def allow_user (self, user) :
        if self.login_required :
            if not user.is_authenticated () :
                return False
            if not user.is_active :
                return False
            if not user.is_superuser and self._permission :
                return self._permission (user, self)
        return True
    # end def allow_user

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

    @property
    def has_children (self) :
        return bool (getattr (self, "own_links", []))
    # end def has_children

    @Once_Property
    def href (self) :
        href = pjoin (self.prefix, self.name)
        if href :
            return pnorm (href)
        return ""
    # end def href

    @Once_Property
    def login_required (self) :
        ### if a parent requires login, all children do too (even if they
        ### claim otherwise!)
        return \
            (  self._login_required
            or self._permission
            or (self.parent and self.parent.login_required)
            )
    # end def login_required

    @property
    def nav_links (self) :
        yield self
    # end def nav_links

    @Once_Property
    def permalink (self) :
        return self.abs_href
    # end def permalink

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

    def rendered (self, context = None, nav_page = None, template = None) :
        if context is None :
            from django.template import Context
            context = Context ({})
        context ["page"]     = self
        context ["nav_page"] = nav_page or self
        context ["NAV"]      = self.top
        result = self.render_to_string \
            (template or self.template, context, self.encoding)
        if self.translator :
            result = self.translator (result)
        return result
    # end def rendered

    @property
    def Type (self) :
        return self.__class__.__name__
    # end def Type

    def _formatted_attr (self, name) :
        v = getattr (self, name)
        if isinstance (v, unicode) :
            v = 'u"""%s"""' % (v.encode (self.input_encoding))
        return v
    # end def _formatted_attr

    def _get_child (self, child, * grandchildren) :
        if child == self.name and not grandchildren :
            return self
    # end def _get_child

    def _view (self, request) :
        from django.http     import HttpResponse, Http404
        from django.template import RequestContext
        context = RequestContext (request, dict ())
        result  = self.rendered  (context)
        if result is None :
            raise Http404 (request.path [1:])
        if isinstance (result, str) :
            result = unicode (result, self.encoding)
        if not isinstance (result, HttpResponse) :
            result = HttpResponse (result)
        return result
    # end def _view

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

class Alias (Page) :
    """Model an alias for a page of a web site."""

    _target_href = None
    _target_page = None
    _parent_attr = set (("prefix", "src_dir"))

    def __init__ (self, * args, ** kw) :
        target = kw.pop ("target")
        if isinstance (target, basestring) :
            self._target_href = target
        else :
            self._target_page = target
        self.__super.__init__ (* args, ** kw)
    # end def __init__

    def allow_user (self, user) :
        return (not self.target) or self.target.allow_user (user)
    # end def allow_user

    @Once_Property
    def login_required (self) :
        ### if a parent requires login, all children do too (even if they
        ### claim otherwise!)
        return (not self.target) or self.target.login_required
    # end def login_required

    def rendered (self, context = None, nav_page = None) :
        target = self.target
        if target :
            return target.rendered (context, nav_page or self)
    # end def rendered

    @property
    def target (self) :
        result = self._target_page
        if not result :
            href = self._target_href
            if href :
                href = href.lstrip ("/")
                result = self._target_page = self.top.page_from_href (href)
        return result
    # end def target

    def __getattr__ (self, name) :
        if name not in self._parent_attr :
            target = self.target
            if target is not None :
                return getattr (target, name)
        return self.__super.__getattr__ (name)
    # end def __getattr__

# end class Alias

class _Dir_ (_Site_Entity_) :
    """Model one directory of a web site."""

    Page            = Page

    dir             = ""
    sub_dir         = ""

    def __init__ (self, parent = None, ** kw) :
        self.__super.__init__ (parent, ** kw)
        self._entries = []
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
    def has_children (self) :
        try :
            first (self.own_links)
        except IndexError :
            return False
        else :
            return True
    # end def has_children

    @property
    def href (self) :
        if self.auto_delegate and self._entries :
            try :
                return first (self.own_links).href
            except IndexError :
                pass
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
        src_dir = pjoin  (self.src_dir, sub_dir)
        result  = Type   (src_dir, parent = self, sub_dir = sub_dir, ** kw)
        if entries :
            result.add_entries (entries)
        return result
    # end def new_sub_dir

    def rendered (self, context = None, nav_page = None) :
        try :
            page = first (self.own_links)
        except IndexError :
            if self.empty_template :
                return self.__super.rendered (template = self.empty_template)
        else :
            return page.rendered (context, nav_page)
    # end def rendered

    def _get_child (self, child, * grandchildren) :
        for owl in self.own_links :
            if owl.name in (child, pjoin (child, "/")) :
                if not grandchildren :
                    return owl
                else :
                    return owl._get_child (* grandchildren)
    # end def _get_child

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
        self.prefix  = pjoin \
            (* [p for p in (parent.prefix, sub_dir) if p is not None])
        self.src_dir  = src_dir
        self.__super.__init__ (parent = parent, ** kw)
    # end def __init__

# end class Dir

class Root (_Dir_) :

    auto_delegate           = False  ### useful if not served by Django
    copyright_start         = None
    empty_template          = None
    _login_required         = False
    name                    = "/"
    owner                   = None
    _permission             = None
    src_root                = ""
    translator              = None

    _dump_type              = "DJO.NAV.Root.from_dict_list \\"

    url_patterns            = []
    pre_first_request_hooks = []

    handlers                = \
        { 404               : None
        , 500               : None
        }

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

    @classmethod
    def page_from_href (cls, href, request = None) :
        result = None
        href_s = pjoin (href, u"")
        if href in cls.top.Table :
            result = cls.top.Table [href]
        elif href_s in cls.top.Table :
            result = cls.top.Table [href_s]
        else :
            tail = []
            while href :
                href, _ = sos.path.split (href)
                if href :
                    tail.append (_)
                    try :
                        d = cls.top.Table [pjoin (href, u"")]
                    except KeyError :
                        pass
                    else :
                        result = d._get_child (* reversed (tail))
                if result :
                    break
        ### XXX check permission of request.user vs. result.???
        return result
    # end def page_from_href

    @classmethod
    def universal_view (cls, request) :
        for h in cls.top.pre_first_request_hooks :
            h ()
        cls.top.pre_first_request_hooks = []
        href = request.path [1:]
        ### import pdb; pdb.set_trace ()
        page = cls.page_from_href (href, request)
        if page :
            import _DJO.views
            user = request.user
            if page.login_required :
                if not user.is_authenticated () :
                    return DJO.views.handler_403 \
                        (request, template_name = "403_login.html")
            if page.allow_user (user) :
                return page._view (request)
            else :
                return DJO.views.handler_403 \
                    (request, template_name = "403_permission.html")
        for pattern in cls.top.url_patterns :
            response = pattern.resolve (request)
            if response :
                return response
        from django.http import Http404
        raise Http404 (href)
    # end def universal_view

    ### methods needed to be able to use the root object as a Django URLResolver
    @classmethod
    def resolve (cls, path) :
        return cls.universal_view, (), {}
    # end def resolve

    @classmethod
    def _resolve_special (cls, view_type):
        from django.core.exceptions import ViewDoesNotExist
        try :
            callback = cls.top.handlers [view_type]
            if isinstance (callback, basestring) :
                callback = _load_view (callback)
            if not callable (callback) :
                raise TypeError ("Handler for %s not callable" % (view_type, ))
        except (KeyError, TypeError), e:
            raise ViewDoesNotExist ("Tried %s. Error was: %s" % (view_type, e))
        return callback, {}
    # end def _resolve_special

    @classmethod
    def resolve404 (cls) :
        return cls._resolve_special (404)
    # end def resolve404

    @classmethod
    def resolve500 (cls) :
        return cls._resolve_special (500)
    # end def resolve500

# end class Root

if __name__ != "__main__":
    DJO.NAV._Export ("*", "_load_view", "_Meta_", "_Site_Entity_")
### __END__ DJO.NAV.Base
