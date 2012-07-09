# -*- coding: iso-8859-15 -*-
# Copyright (C) 2012 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# #*** <License> ************************************************************#
# This module is part of the package GTW.RST.
#
# This module is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This module is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this module. If not, see <http://www.gnu.org/licenses/>.
# #*** </License> ***********************************************************#
#
#++
# Name
#    GTW.RST.Resource
#
# Purpose
#    Model a RESTful resource
#
# Revision Dates
#     8-Jun-2012 (CT) Creation
#    22-Jun-2012 (CT) Set `parent` in `_RST_Meta_.__call__` before `.__init__`
#    26-Jun-2012 (CT) Factor `_Dir_Base_`, add `Dir_V`
#    27-Jun-2012 (CT) Add empty `Leaf._get_child`
#    28-Jun-2012 (CT) Fix `url_template`, use `_response_dict`
#    28-Jun-2012 (CT) Use `request.verbose`
#     1-Jul-2012 (CT) Add `href_pat`, use it in `resource_from_href`
#     2-Jul-2012 (CT) Refactor `href_pat_frag`
#     2-Jul-2012 (CT) Change `resource_from_href` to ignore extension
#     3-Jul-2012 (CT) Use `TFL.Context.relaxed` as alternative to `.time_block`
#     5-Jul-2012 (CT) Add `_m_after__init__`
#     8-Jul-2012 (CT) Rename `template` to `page_template`,
#                     add Alias_Property `template`
#     9-Jul-2012 (CT) Factor `get_template`, add `HTTP_Method.template_name`
#     9-Jul-2012 (CT) Factor `_Dir_._get_child` to `_Dir_Base_`
#     9-Jul-2012 (CT) Add `Dir_V._get_child`, use `Dir_V._entry_type_map`
#     9-Jul-2012 (CT) Add `Dir_V.template_iter`
#    ««revision-date»»···
#--

from   __future__  import absolute_import, division, print_function, unicode_literals

from   _GTW                     import GTW
from   _TFL                     import TFL

import _GTW._RST.HTTP_Method

from   _TFL._Meta.Once_Property import Once_Property
from   _TFL._Meta.Property      import Alias_Property
from   _TFL.Filename            import Filename
from   _TFL.predicate           import callable

import _TFL._Meta.M_Class
import _TFL._Meta.Object
import _TFL.Accessor
import _TFL.Context
import _TFL.Environment
import _TFL.Record

from   posixpath import \
    ( join          as pp_join
    , normpath      as pp_norm
    , split         as pp_split
    , splitext      as pp_splitext
    , commonprefix
    )

import logging
import re
import sys
import time
import traceback

class _RST_Meta_ (TFL.Meta.M_Class) :

    def __init__ (cls, name, bases, dct) :
        cls.__m_super.__init__ (name, bases, dct)
        cls.SUPPORTED_METHODS = sms = {}
        for k in GTW.RST.HTTP_Method.Table :
            v = getattr (cls, k, None)
            if callable (v) :
                sms [k] = v
                tn = getattr (v, "template_name", None)
                if tn :
                    cls._template_names.add (tn)
        for k in ("page_template_name", "dir_template_name") :
            tn = dct.get (k)
            if tn :
                cls._template_names.add (tn)
        cls._m_after__init__ (name, bases, dct)
    # end def __init__

    def __call__ (cls, * args, ** kw) :
        parent = kw.get ("parent")
        if cls._needs_parent and parent is None :
            return (cls, args, kw)
        ### set `result.parent` before calling `result.__init__` so
        ### that `result.__getattr__` can use it right from the beginning
        result = cls.__new__   (cls, * args, ** kw)
        result.parent = kw.pop ("parent", None)
        result.__init__        (* args, ** kw)
        result._after__init__  (kw)
        return result
    # end def __call__

# end class _RST_Meta_

class _RST_Base_ (TFL.Meta.Object) :
    """Base class for RESTful resources."""

    __metaclass__              = _RST_Meta_
    _real_name                 = "_Base_"

    hidden                     = False
    implicit                   = False
    pid                        = None
    template                   = Alias_Property ("page_template")
    template_name              = Alias_Property ("page_template_name")

    _needs_parent              = True
    _r_permission              = None             ### read permission
    _w_permission              = None             ### write permission
    _page_template             = None
    _template_names            = set ()

    DELETE                     = None             ### redefine if necessary
    GET                        = GTW.RST.GET      ### needs    to be redefined
    HEAD                       = GTW.RST.HEAD     ### needs    to be redefined
    OPTIONS                    = GTW.RST.OPTIONS  ### unlikely to be redefined
    POST                       = None             ### redefine if necessary
    PUT                        = None             ### redefine if necessary

    def __init__ (self, ** kw) :
        parent   = self.parent                    ### set by meta class
        self._kw = dict (kw)
        self.pop_to_self \
            ( kw
            , "exclude_robots", "r_permissions", "w_permissions"
            , prefix = "_"
            )
        encoding = kw.get ("input_encoding") or \
            getattr (parent, "input_encoding", Root.input_encoding)
        for k, v in kw.iteritems () :
            if isinstance (v, str) :
                v = unicode (v, encoding)
            try :
                setattr (self, k, v)
            except AttributeError, exc :
                print (self.href or "/{ROOT}", k, v, "\n   ", exc)
        if self.implicit :
            self.hidden = True
    # end def __init__

    def _after__init__ (self, kw) :
        ### called by meta class after `__init__` has finished
        ### redefine as necessary
        self._orig_kw = dict (kw)
        top = self.top
        if not self.implicit :
            href = self.href
            pid  = self.pid
            if href is not None :
                Table = top.Table
                Table [href] = self
                try :
                    perma = self.permalink.lstrip ("/")
                except Exception :
                    pass
                else :
                    if perma != href :
                        if perma not in Table or Table [perma].href == href :
                            Table [perma] = self
            if pid is not None :
                setattr (top.SC, pid, self)
        for k in ("page_template_name", "dir_template_name") :
            tn = getattr (self, k, None)
            if tn :
                top._template_names.add (tn)
    # end def _after__init__

    @classmethod
    def _m_after__init__ (cls, name, bases, dct) :
        """Called by metaclass's __init__: redefine as necessary."""
        pass
    # end def _m_after__init__

    @Once_Property
    def abs_href (self) :
        result = self.href
        if not result.startswith ("/") :
            return "/%s" % (result, )
        return result
    # end def abs_href

    @Once_Property
    def account_manager (self) :
        scope = self.top.scope
        if scope :
            return scope.GTW.OMP.Auth.Account
    # end def account_manager

    @Once_Property
    def base (self) :
        return Filename (self.name).base
    # end def base

    @property
    def change_info (self) :
        ### Redefine as necessary
        pass
    # end def change_info

    @property
    def email_from (self) :
        result = self._email_from
        if result is None :
            result = self.webmaster
            if isinstance (result, tuple) :
                result = "%s <%s>" % (result [1], result [0])
            self._email_from = result
        return result
    # end def email_from

    @email_from.setter
    def email_from (self, value) :
        self._email_from = value
    # end def email_from

    @property
    def entries (self) :
        return ()
    # end def entries

    @property
    def entries_transitive (self) :
        return ()
    # end def entries_transitive

    @Once_Property
    def exclude_robots (self) :
        return self.r_permissions or self.hidden or self._exclude_robots
    # end def exclude_robots

    @Once_Property
    def file_stem (self) :
        return pp_norm (pp_join (self.prefix, self.base))
    # end def file_stem

    @Once_Property
    def href (self) :
        pp   = self.parent.href if self.parent else self.prefix
        href = pp_join (pp, self.base)
        if href :
            return pp_norm (href)
        return ""
    # end def href

    @property
    def href_pat_frag (self) :
        pass ### redefine as necessary
    # end def href_pat_frag

    @Once_Property
    def injected_templates (self) :
        ### redefine as necessary
        return set ()
    # end def injected_templates

    @property
    def page_template (self) :
        if self._page_template is None :
            t_name = getattr (self, "page_template_name", None)
            if t_name :
                self._page_template = self.get_template \
                    (t_name, self.injected_templates)
        return self._page_template
    # end def page_template

    @page_template.setter
    def page_template (self, value) :
        self._page_template = None
        if isinstance (value, basestring) :
            self.page_template_name = value
        elif not isinstance (value, self.Templateer.Template_Type) :
            self.page_template_name = value.name
        else :
            self.page_template_name = value.name
            self._page_template     = value
    # end def page_template

    @Once_Property
    def permalink (self) :
        return self.abs_href
    # end def permalink

    @Once_Property
    def r_permissions (self) :
        return sorted \
            (self._get_permissions ("r_permission"), key = TFL.Getter.rank)
    # end def r_permissions

    @property
    def Type (self) :
        return self.__class__.__name__
    # end def Type

    @Once_Property
    def w_permissions (self) :
        return sorted \
            (self._get_permissions ("w_permission"), key = TFL.Getter.rank)
    # end def w_permissions

    @Once_Property
    def _effective (self) :
        return self
    # end def _effective

    def allow_method (self, method, user) :
        """Returns True if `self` allows `method` for `user`."""
        if isinstance (method, basestring) :
            method = GTW.RST.HTTP_Method.Table [method]
        if not (user and user.superuser) :
            pn = method.mode + "_permissions"
            permissions = getattr (self, pn)
            return all (p (user, self) for p in permissions)
        return True
    # end def allow_method

    def allow_user (self, user) :
        return self.allow_method ("GET", user)
    # end def allow_user

    def get_template (self, template_name) :
        if self.Templateer is not None :
            return self.Templateer.get_template (template_name)
    # end def get_template

    def send_error_email (self, request, exc, tbi) :
        from _TFL.Formatter import formatted
        email     = self.email_from
        headers   = request.headers
        message   = "Headers:\n    %s\n\nBody:\n    %s\n\n%s" % \
            ( "\n    ".join
                ("%-20s: %s" % (k, v) for k, v in headers.iteritems ())
            , formatted (request.data)
            , tbi
            )
        if not self.Templateer :
            print ("Exception:", exc)
            print ("Request path", request.path)
            print ("Email", email)
            print (message)
            print (request.data)
        else :
            kw = {}
            if self.DEBUG :
                from _TFL.SMTP import SMTP_Logger
                kw = dict (smtp = SMTP_Logger ())
            self.send_email \
                ( self.error_email_template
                , email_from    = email
                , email_to      = email
                , email_subject = ("Error: %s") % (exc, )
                , message       = message
                , NAV           = self.top
                , page          = self
                , request       = request
                , ** kw
                )
    # end def send_error_email

    def send_email (self, template, ** context) :
        email_from = context.get ("email_from")
        if not email_from :
            context ["email_from"] = email_from = self.email_from
        smtp = context.pop ("smtp", self.smtp)
        smtp.charset = self.encoding
        text = self.top.Templateer.render (template, context).encode \
            (self.encoding, "replace")
        try :
            smtp (text)
        except Exception as exc :
            logging.error \
                ( "Exception: %s"
                  "\n  When trying to send email from %s to %s"
                  "\n  %s"
                , exc
                , email_from, context.get ("email_to", "<Unkown>")
                , text
                )
            try :
                kw = dict \
                    ( context
                    , email_from    = self.email_from
                    , email_to      = self.email_from
                    , email_subject =
                        ( "Error when trying to send email from %s: %s"
                        % (email_from, exc)
                        )
                    , message       = text
                    , NAV           = self.top
                    , page          = self
                    )
                self.send_email (self.error_email_template, ** kw)
            except Exception :
                pass
    # end def send_email

    def template_iter (self) :
        t = self.page_template
        if t :
            yield t
    # end def template_iter

    def _get_permissions (self, name) :
        p = getattr (self, "_" + name, None)
        if p is not None :
            yield p
        if self.parent :
            for p in getattr (self.parent, name + "s", ()) :
                yield p
    # end def _get_permissions

    def _get_user (self, username) :
        result = None
        if username :
            try :
                result = self.account_manager.query (name = username).one ()
            except IndexError :
                pass
            except Exception as exc :
                logging.error \
                    ( "Exception %s when trying to determine the user"
                    , exc
                    )
        return result
    # end def _get_user

    def _handle_method (self, method, request) :
        with self._handle_method_context (method, request) :
            result = method (self, request)
            return result
    # end def _handle_method

    @TFL.Contextmanager
    def _handle_method_context (self, method, request) :
        ### Redefine to setup context for handling `method` for `request`,
        ### for instance, `self.change_info`
        yield
    # end def _handle_method_context

    def __getattr__ (self, name) :
        if self.parent is not None :
            return getattr (self.parent, name)
        raise AttributeError (name)
    # end def __getattr__

    def __repr__ (self) :
        return "<%s %s: %s>" % (self.Type, self.name, self.abs_href)
    # end def __repr__

_Base_ = _RST_Base_ # end class

class RST_Leaf (_Base_) :
    """Base class for RESTful leaves."""

    _real_name                 = "Leaf"

    def _get_child (self, child, * grandchildren) :
        pass
    # end def _get_child

Leaf = RST_Leaf # end class

_Ancestor = _Base_

class _RST_Dir_Base_ (_Ancestor) :
    """Base class for RESTful directories (resources with children)."""

    _real_name                 = "_Dir_Base_"

    _dir_template              = None
    _href_pat_frag             = None

    template                   = Alias_Property ("dir_template")
    template_name              = Alias_Property ("dir_template_name")

    class RST__Dir_Base__GET (_Ancestor.GET) :

        _real_name             = "GET"

        def _response_body (self, resource, request, response) :
            result = self._response_dict (resource, request, response)
            add    = result ["entries"].append
            for e in self._resource_entries (resource, request, response) :
                add (self._response_entry (resource, request, response, e))
            return result
        # end def _response_body

        def _response_dict (self, resource, request, response, ** kw) :
            result = dict \
                ( entries = []
                , ** kw
                )
            if not request.verbose :
                result ["url_template"] = pp_join (resource.abs_href, "{entry}")
            return result
        # end def _response_dict

        def _response_entry (self, resource, request, response, entry) :
            return entry.name
        # end def _response_entry

        def _response_entry (self, resource, request, response, entry) :
            if request.verbose :
                result = pp_join (resource.abs_href, entry.name)
            else :
                result = entry.name
            return result
        # end def _response_entry

        def _resource_entries (self, resource, request, response) :
            raise NotImplementedError
        # end def _resource_entries

    GET = RST__Dir_Base__GET # end class

    def __init__ (self, ** kw) :
        self._entry_map = {}
        for k in ("template", "template_name") :
            if k in kw :
                kw ["page_" + k] = kw.pop (k)
        self.__super.__init__ (** kw)
    # end def __init__

    @property
    def dir_template (self) :
        if self._dir_template is None :
            t_name = getattr (self, "dir_template_name", None)
            if t_name :
                self._dir_template = self.get_template \
                    (t_name, self.injected_dir_templates)
        return self._dir_template
    # end def dir_template

    @dir_template.setter
    def dir_template (self, value) :
        self._dir_template = None
        if isinstance (value, basestring) :
            self.dir_template_name = value
        elif not isinstance (value, self.Templateer.Template_Type) :
            self.dir_template_name = value.name
        else :
            self.dir_template_name = value.name
            self._dir_template     = value
    # end def dir_template

    @property
    def href_pat_frag (self) :
        result = self._href_pat_frag
        if result is None :
            result = self._href_pat_frag = self._add_href_pat_frag_tail \
                (re.escape (self.base))
        return result
    # end def href_pat_frag

    @Once_Property
    def injected_dir_templates (self) :
        ### redefine as necessary
        return set ()
    # end def injected_dir_templates

    def template_iter (self) :
        for t in self.__super.template_iter () :
            yield t
        t = self.dir_template
        if t :
            yield t
    # end def template_iter

    def _get_child (self, child, * grandchildren) :
        try :
            result = self._entry_map [child]
        except KeyError :
            pass
        else :
            if not grandchildren :
                return result
            else :
                return result._get_child (* grandchildren)
    # end def _get_child

_Dir_Base_ = _RST_Dir_Base_ # end class

_Ancestor = _Dir_Base_

class _RST_Dir_ (_Ancestor) :
    """Base class for RESTful directories (resources with children)."""

    _real_name                 = "_Dir_"

    class RST__Dir__GET (_Ancestor.GET) :

        _real_name             = "GET"

        def _resource_entries (self, resource, request, response) :
            return resource.entries
        # end def _resource_entries

    GET = RST__Dir__GET # end class

    def __init__ (self, ** kw) :
        entries = kw.pop ("entries", [])
        self.__super.__init__ (** kw)
        self._entries   = []
        if entries :
            self._init_add_entries (entries)
    # end def __init__

    @property
    def entries (self) :
        return self._entries
    # end def entries

    @property
    def entries_transitive (self) :
        for e in self.entries :
            yield e
            if isinstance (e, _Dir_) :
                for d in e.entries_transitive :
                    yield d
    # end def entries_transitive

    def add_entries (self, * entries) :
        self._entries.extend (entries)
        self._entry_map.update ((e.name, e) for e in entries)
    # end def add_entries

    def sub_dir_iter (self) :
        for owl in self.entries :
            if isinstance (owl, _Dir_) :
                yield owl
    # end def sub_dir_iter

    def template_iter (self) :
        for t in self.__super.template_iter () :
            yield t
        eff = self._effective
        if eff is not self :
            for t in eff.template_iter () :
                yield t
        for d in self.sub_dir_iter () :
            for t in d.template_iter () :
                yield t
    # end def template_iter

    def _add_href_pat_frag_tail \
            (self, head, getter = TFL.Getter.href_pat_frag) :
        result  = head
        entries = sorted \
            (self.entries, key = lambda x : x.name, reverse = True)
        e_hpfs = tuple (x for x in (getter (e) for e in entries) if x)
        if e_hpfs :
            e_result   = "|".join (e_hpfs)
            if head :
                result = "%s(?:/(?:%s))?" % (head, e_result)
            else :
                result = e_result
        return result
    # end def _add_href_pat_frag_tail

    def _init_add_entries (self, entries) :
        self.add_entries \
            ( * (   cls (* args, ** dict (kw, parent = self))
                for cls, args, kw in entries
                )
            )
    # end def _init_add_entries

_Dir_ = _RST_Dir_ # end class

_Ancestor = _Dir_

class RST_Dir (_Ancestor) :
    """Base class for RESTful directories (resources with children)."""

    _real_name                 = "Dir"

    def __init__ (self, ** kw) :
        self.prefix = pp_join (self.parent.prefix, kw ["name"], "")
        self.__super.__init__ (** kw)
    # end def __init__

    @Once_Property
    def href (self) :
        return self.prefix.rstrip ("/")
    # end def href

Dir = RST_Dir # end class

_Ancestor = _Dir_Base_

class RST_Dir_V (_Ancestor) :
    """Base class for RESTful volatile directories (resources with children,
       without permanent `_entries`).
    """

    _entry_type_map = None

    def template_iter (self) :
        for t in self.__super.template_iter () :
            yield t
        if self._entry_type_map :
            for e in self._entry_type_map.itervalues () :
                for t in e.template_iter () :
                    yield t
    # end def template_iter

    def _add_href_pat_frag_tail (self, head, getter = None) :
        return head
    # end def _add_href_pat_frag_tail

    def _get_child (self, child, * grandchildren) :
        result = self.__super._get_child (child, * grandchildren)
        if result is None and self._entry_type_map :
            try :
                T = self._entry_type_map [child]
            except KeyError :
                pass
            else :
                return self._new_child (T, child, grandchildren)
    # end def _get_child

    def _new_child (self, T, child, grandchildren) :
        result = T (name = child, parent = self)
        if not grandchildren :
            return result
        else :
            return result._get_child (* grandchildren)
    # end def _new_child

Dir_V = RST_Dir_V # end class

_Ancestor = Leaf

class RST_Raiser (_Ancestor) :
    """Resource that raises an error 500."""

    _real_name                 = "Raiser"

    hidden                     = True

    class RST_Raiser_GET (_Ancestor.GET) :

        _real_name             = "GET"

        def _response_body (self, resource, request, response) :
            raise RuntimeError ("Wilful raisement")
        # end def _response_body

    GET = RST_Raiser_GET # end class

Raiser = RST_Raiser # end class

_Ancestor = _Dir_

class RST_Root (_Ancestor) :
    """Root of tree of RESTful resources."""

    _real_name                 = "Root"

    Cacher                     = None # XXX GTW.RST.Template_Media_Cache
    Create_Scope               = None
    DEBUG                      = False
    Templateer                 = None

    default_locale_code        = "en"
    domain                     = ""
    encoding                   = "utf-8"    ### output encoding
    error_email_template       = "error_email"
    ignore_picky_accept        = False
    input_encoding             = "iso-8859-15"
    language                   = "en"
    languages                  = set (("en", ))
    name                       = ""
    prefix                     = ""
    site_url                   = ""

    _exclude_robots            = True
    _href_pat                  = None
    _needs_parent              = False

    _email_from                = None   ### default from address
    _smtp                      = None
    _webmaster                 = None

    from _GTW._RST.Request  import Request  as Request_Type
    from _GTW._RST.Response import Response as Response_Type

    def __init__ (self, HTTP, ** kw) :
        if "copyright_start" not in kw :
            kw ["copyright_start"] = time.localtime ().tm_year
        self.pop_to_self      (kw, "name", "prefix")
        self.pop_to_self      (kw, "smtp", prefix = "_")
        self.HTTP           = HTTP
        self.redirects      = dict (kw.pop ("redirects", {}))
        self.SC             = TFL.Record ()
        self.Table          = {}
        self.top            = self
        self.__super.__init__ (** kw)
    # end def __init__

    def __call__ (self, environ, start_response) :
        return self.wsgi_app (environ, start_response)
    # end def __call__

    @property
    def href_pat (self) :
        result = self._href_pat
        if result is None :
            hpf = self.href_pat_frag
            if hpf :
                try :
                    result = self._href_pat = re.compile (hpf)
                except Exception as exc :
                    logging.error \
                        ("Exception in href_pat for %s: %s", self, exc)
        return result
    # end def href_pat

    @property
    def smtp (self) :
        if self._smtp is None :
            from _TFL.SMTP import SMTP_Logger
            self._smtp = SMTP_Logger ()
        return self._smtp
    # end def smtp

    @Once_Property
    def scope (self) :
        CS = self.Create_Scope
        if CS is not None :
            result = CS (self.App_Type, self.DB_Url)
            if self.DEBUG :
                print ("Loaded", result)
            return result
    # end def scope

    @property
    def webmaster (self) :
        result = self._webmaster
        if result is None :
            domain = self.domain or self.site_url
            if domain.startswith ("www.") :
                domain = domain [4:]
            result = self._webmaster = "webmaster@%s" % (domain, )
        return result
    # end def webmaster

    @webmaster.setter
    def webmaster (self, value) :
        self._webmaster = value
    # end def webmaster

    def allow (self, resource, user, method = "GET") :
        if isinstance (resource, basestring) :
            resource = self.resource_from_href (resource)
        if resource :
            try :
                allow_method = resource.allow_method
            except Exception :
                return True
            else :
                return allow_method (method, user)
    # end def allow

    def Request (self, environ) :
        result = self.Request_Type  (self, environ)
        result.charset = self.encoding
        return result
    # end def Request

    def Response (self, request, * args, ** kw) :
        result = self.Response_Type (self, request, * args, ** kw)
        result.charset = self.encoding
        return result
    # end def Response

    def resource_from_href (self, req_href) :
        Table        = self.Table
        req_href     = req_href.strip ("/")
        href, ext    = pp_splitext (req_href)
        match        = None
        redirects    = self.redirects
        result       = None
        if redirects :
            try :
                result = redirects [href]
            except KeyError :
                pass
            else :
                raise self.HTTP.Redirect_302 (result)
        if result is None :
            result = Table.get (href)
        if result is None :
            href_pat = self.href_pat
            if href_pat :
                match = href_pat.match (href)
                if match :
                    head = match.group (0)
                    tail = href [len (head):].lstrip ("/").split ("/")
                    resource = Table.get (head)
                    if resource :
                        result = resource._get_child (* tail)
        if result is None and not match :
            head = href
            tail = []
            while head :
                head, _ = pp_split (head)
                if head or not tail : ### `not tail` covers root's entries
                    tail.append (_)
                    try :
                        d = Table [head]
                    except KeyError :
                        pass
                    else :
                        if self.DEBUG :
                            print \
                                ( "*" * 3, href, d
                                , "not in `Table`, not matched by `href_pat`"
                                )
                        result = d._get_child (* reversed (tail))
                if result :
                    break
        return result
    # end def resource_from_href

    def template_iter (self) :
        seen = set ()
        gett = self.get_template
        def _gen () :
            for tn in self.template_names :
                yield gett (tn)
            for tn in self.Templateer.error_template_names :
                yield gett (tn)
            for t in self.__super.template_iter () :
                yield t
        for t in _gen () :
            if t.id not in seen :
                yield t
                seen.add (t.id)
    # end def template_iter

    def wsgi_app (self, environ, start_response) :
        """WSGI application responding to http[s] requests."""
        HTTP    = self.HTTP
        request = self.Request (environ)
        try :
            result = self._http_response (request)
        except HTTP.Status as status :
            result = status (request)
        except HTTP.HTTP_Exception as exc :
            ### works for werkzeug.exceptions.HTTPException
            return exc
        except Exception as exc :
            tbi    = traceback.format_exc ()
            result = self._http_response_error (request, exc, tbi)
        if not result :
            result = self._http_response_error \
                (request, ValueError ("No result"))
        return result (environ, start_response)
    # end def wsgi_app

    def _http_response (self, request) :
        HTTP     = self.HTTP
        href     = request.path
        resource = self.resource_from_href (href)
        if resource  :
            user       = request.user = self._get_user (request.username)
            auth       = user and user.authenticated
            resource   = resource._effective
            meth_name  = request.method
            if meth_name not in resource.SUPPORTED_METHODS :
                raise HTTP.Error_405 \
                    (valid_methods = resource.SUPPORTED_METHODS)
            method   = getattr (resource, meth_name) ()
            if resource.allow_method (method, user) :
                if resource.DEBUG :
                    context = TFL.Context.time_block
                    fmt     = "[%s] %s %s: execution time = %%s" % \
                        ( time.strftime
                            ("%d-%b-%Y %H:%M:%S", time.localtime (time.time ()))
                        , method.name, href
                        )
                else :
                    context = TFL.Context.relaxed
                    fmt     = None
                with context (fmt, sys.stderr) :
                    return resource._handle_method (method, request)
            else :
                raise (HTTP.Error_403 if auth else HTTP.Error_401)
        raise HTTP.Error_404
    # end def _http_response

    def _http_response_error (self, request, exc, tbi = None) :
        self.send_error_email (request, exc, tbi)
        return self.HTTP.Error_500 (exc) (request)
    # end def _http_response_error

Root = RST_Root # end class

__doc__ = """
Each supported http method is defined by a separate class of the same name
(in upper case). To disable support in a descendent class, set the
appropriate name to `None`, e.g., ::

    PUT = None

"""

if __name__ != "__main__" :
    GTW.RST._Export ("*", "_Base_", "_Dir_Base_", "_Dir_")
### __END__ GTW.RST.Resource
