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
#    11-Jun-2012 (CT) Continue creation
#    12-Jun-2012 (CT) Continue creation..
#    ««revision-date»»···
#--

from   __future__  import absolute_import, division, print_function, unicode_literals

from   _GTW                     import GTW
from   _TFL                     import TFL

import _GTW._RST.HTTP_Method

from   _TFL._Meta.Once_Property import Once_Property
from   _TFL                     import pyk, sos
from   _TFL.Filename            import Filename
from   _TFL.predicate           import callable

import _TFL._Meta.M_Class
import _TFL._Meta.Object
import _TFL.Accessor
import _TFL.Context
import _TFL.Environment
import _TFL.Record

from   posixpath import join as pjoin, normpath as pnorm, commonprefix

import logging
import time

class _RST_Meta_ (TFL.Meta.M_Class) :

    def __init__ (cls, name, bases, dct) :
        cls.__m_super.__init__ (name, bases, dct)
        cls.SUPPORTED_METHODS = sms = {}
        for k in GTW.RST.HTTP_Method.Table :
            v = getattr (cls, k, None)
            if callable (v) :
                sms [k] = v
    # end def __init__

    def __call__ (cls, * args, ** kw) :
        if cls._needs_parent and kw.get ("parent") is None :
            return (cls, args, kw)
        result = cls.__m_super.__call__ (* args, ** kw)
        kw.pop ("parent", None)
        result._orig_kw = dict (kw)
        if not result.implicit :
            href = result.href
            pid  = result.pid
            try :
                top  = result.top
            except AttributeError :
                TFL.Environment.exec_python_startup (); import pdb; pdb.set_trace ()
            if href is not None :
                Table = top.Table
                Table [href] = result
                try :
                    perma = result.permalink.lstrip ("/")
                except Exception :
                    pass
                else :
                    if perma != href :
                        if perma not in Table or Table [perma].href == href :
                            Table [perma] = result
            if pid is not None :
                setattr (top.SC, pid, result)
        return result
    # end def __call__

# end class _RST_Meta_

class _RST_Base_ (TFL.Meta.Object) :
    """Base class for RESTful resources."""

    __metaclass__              = _RST_Meta_
    _real_name                 = "_Base_"

    hidden                     = False
    implicit                   = False
    input_encoding             = "iso-8859-15"
    pid                        = None

    _exclude_robots            = True
    _needs_parent              = True
    _r_permission              = None             ### read permission
    _w_permission              = None             ### write permission

    DELETE                     = None
    GET                        = GTW.RST.GET      ### needs    to be redefined
    HEAD                       = GTW.RST.HEAD     ### needs    to be redefined
    OPTIONS                    = GTW.RST.OPTIONS  ### unlikely to be redefined
    POST                       = None
    PUT                        = None

    def __init__ (self, ** kw) :
        self.parent = parent = kw.pop ("parent", None)
        self._kw    = dict (kw)
        self.pop_to_self \
            ( kw
            , "exclude_robots", "r_permissions", "w_permissions"
            , prefix = "_"
            )
        encoding = kw.get ("input_encoding") or \
            getattr (parent, "input_encoding", self.input_encoding)
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

    @Once_Property
    def exclude_robots (self) :
        return self.r_permissions or self.hidden or self._exclude_robots
    # end def exclude_robots

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

    @Once_Property
    def permalink (self) :
        return self.abs_href
    # end def permalink

    @Once_Property
    def r_permissions (self) :
        return sorted \
            (self._get_permissions ("r_permission"), key = TFL.Getter.rank)
    # end def r_permissions

    @Once_Property
    def w_permissions (self) :
        return sorted \
            (self._get_permissions ("w_permission"), key = TFL.Getter.rank)
    # end def w_permissions

    @property
    def Type (self) :
        return self.__class__.__name__
    # end def Type

    @Once_Property
    def _effective (self) :
        return self
    # end def _effective

    def allow_method (self, method, user) :
        """Returns True if `self` allows `method` for `user`."""
        if isinstance (method, basestring) :
            method = GTW.RST.HTTP_Method.Table [method]
        if not user.superuser :
            pn = method.mode + "_permissions"
            permissions = getattr (self, pn)
            return all (p (user, self) for p in self.permissions ())
        return True
    # end def allow_method

    def etype_manager (self, obj) :
        etn = getattr (obj, "type_name", None)
        if etn :
            return self.top.ET_Map [etn].manager
    # end def etype

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
                pyk.fprint \
                    ( ">>> Exception"
                    , exc
                    , "when trying to determine the user"
                    , file = sys.stderr
                    )
        return result
    # end def _get_user

    def _handle_method (self, method, handler) :
        self._prepare_handle_method (method, handler)
        return method (self, handler)
    # end def _handle_method

    def _prepare_handle_method (self, method, handler) :
        ### Redefine to setup context for handling `method` for `handler`,
        ### for instance, `self.change_info`
        pass
    # end def _prepare_handle_method

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

    @property
    def entries (self) :
        return ()
    # end def entries

Leaf = RST_Leaf # end class

class _RST_Node_ (_Base_) :
    """Base class for RESTful nodes (resources with children)."""

    _real_name                 = "_Node_"

    class RST__Node__GET (_Base_.GET) :

        _real_name             = "GET"

        def _response (self, resource, handler) :
            entries = []
            result  = dict \
                ( entries      = entries
                , url_template = "%s/{entry}"
                )
            for e in resource.entries :
                entries.append (e.name)
            return result
        # end def _response

    GET = RST__Node__GET # end class

    def __init__ (self, ** kw) :
        entries = kw.pop ("entries", [])
        self.__super.__init__ (** kw)
        self._entries = []
        if entries :
            self._init_add_entries (entries)
    # end def __init__

    @property
    def entries (self) :
        return tuple (self._entries)
    # end def entries

    @property
    def entries_transitive (self) :
        for e in self.entries :
            yield e
            if isinstance (e, _Node_) :
                for d in e.entries_transitive :
                    yield d
    # end def entries_transitive

    def add_entries (self, * entries) :
        self._entries.extend (entries)
    # end def add_entries

    def _init_add_entries (self, entries) :
        self.add_entries \
            ( * (   cls (* args, ** dict (kw, parent = self))
                for cls, args, kw in entries
                )
            )
    # end def _init_add_entries

_Node_ = _RST_Node_ # end class

class RST_Node (_Node_) :
    """Base class for RESTful nodes (resources with children)."""

    _real_name                 = "Node"

    def __init__ (self, ** kw) :
        parent      = kw      ["parent"]
        self.name   = kw.pop  ("name")
        self.prefix = pjoin   (parent.prefix, self.name, "")
        self.__super.__init__ (** kw)
    # end def __init__

    @Once_Property
    def href (self) :
        return self.prefix.rstrip ("/")
    # end def href

Node = RST_Node # end class

class RST_Root (_Node_) :
    """Root of tree of RESTful nodes."""

    _real_name                 = "Root"

    Create_Scope               = None
    DEBUG                      = False
    name                       = ""
    prefix                     = ""

    _needs_parent              = False

    def __init__ (self, HTTP, ** kw) :
        if "copyright_start" not in kw :
            kw ["copyright_start"] = time.localtime ().tm_year
        self.HTTP           = HTTP
        self.redirects      = dict (kw.pop ("redirects",     {}))
        self.Run_on_Launch  = list (kw.pop ("Run_on_Launch", []))
        self.SC             = TFL.Record ()
        self.Table          = {}
        self.top            = self
        self.pop_to_self      ("name", "prefix")
        self.__super.__init__ (** kw)
    # end def __init__

    @Once_Property
    def scope (self) :
        CS = self.Create_Scope
        if CS is not None :
            result = CS (self.App_Type, self.DB_Url)
            if self.DEBUG :
                print ("Loaded", result)
            return result
    # end def scope

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

    def handle_request (self, handler) :
        HTTP    = self.HTTP
        request = handler.request
        href    = request.path
        rsrc    = self.resource_from_href (href)
        if rsrc :
            user    = request.user = self._get_user (handler.username)
            auth    = user and user.authenticated
            rsrc    = rsrc._effective
            hrm     = request.method
            if hrm not in rsrc.SUPPORTED_METHODS :
                raise HTTP.Error_405 (valid_methods = rsrc.SUPPORTED_METHODS)
            method  = getattr (rsrc, hrm) ()
            if rsrc.allow_method (user, method) :
                if rsrc.DEBUG :
                    fmt = "[%s] %s %s: execution time = %%s" % \
                        ( time.strftime
                            ("%d-%b-%Y %H:%M:%S", time.localtime (time.time ()))
                        , method.name, href
                        )
                    with TFL.Context.time_block (fmt, sys.stderr) :
                        return rsrc._handle_method (method , handler)
                else :
                    return rsrc._handle_method (method , handler)
            else :
                Exc = HTTP.Error_403 if auth else HTTP.Error_401
                raise Exc ()
        raise HTTP.Error_404 ()
    # end def handle_request

    def resource_from_href (self, href) :
        href       = href.strip (u"/")
        result     = None
        Table      = self.Table
        redirects  = self.redirects
        if redirects :
            try :
                result = redirects [href]
            except KeyError :
                pass
            else :
                raise self.HTTP.Redirect_302 (result)
        if href in Table :
            result = Table [href]
        else :
            head = href
            tail = []
            while head :
                head, _ = sos.path.split (head)
                if head :
                    tail.append (_)
                    try :
                        d = Table [head]
                    except KeyError :
                        pass
                    else :
                        result = d._get_child (* reversed (tail))
                if result :
                    break
        return result
    # end def resource_from_href

Root = RST_Root # end class

__doc__ = """
Each supported http method is defined by a separate class of the same name
(in upper case). To disable support in a descendent class, set the
appropriate name to `None`, e.g., ::

    PUT = None

"""

if __name__ != "__main__" :
    GTW.RST._Export ("*")
### __END__ GTW.RST.Resource
