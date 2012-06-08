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

import logging

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
        result = cls.__m_super.__call__ (* args, ** kw)
        result._orig_kw = dict (kw)
        if not result.implicit :
            href = result.href
            pid  = result.pid
            top  = result.top
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

    error_email_template       = "error_email"
    hidden                     = False
    href                       = ""
    implicit                   = False
    input_encoding             = "iso-8859-15"
    nick                       = ""
    parent                     = None
    pid                        = None
    top                        = None

    _email                     = None   ### default from address
    _exclude_robots            = True
    _r_permission              = None   ### read permission
    _w_permission              = None   ### write permission

    DELETE                     = None
    GET                        = None
    HEAD                       = None
    OPTIONS                    = None
    POST                       = None
    PUT                        = None

    class OPTIONS (GTW.RST.OPTIONS) :

        def __call__ (self, page, handler) :
            methods = sorted \
                (  k for k, m in page.SUPPORTED_METHODS.iteritems ()
                if page.allow_method (m, handler.request)
                )
            handler.set_header ("Allow", ", ".join (methods))
            return ""
        # end def __call__

    # end class OPTIONS

    def __init__ (self, parent = None, ** kw) :
        self._kw    = dict (kw)
        self.parent = parent
        self.pop_to_self (kw, "r_permissions", "w_permissions", prefix = "_")
        if "input_encoding" in kw :
            encoding = kw ["input_encoding"]
        else :
            encoding = getattr (parent, "input_encoding", self.input_encoding)
        for k, v in kw.iteritems () :
            if isinstance (v, str) :
                v = unicode (v, encoding, "replace")
            try :
                setattr (self, k, v)
            except AttributeError, exc :
                print (self.href or "Navigation.Root", k, v, "\n   ", exc)
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
    def email (self) :
        result = self._email
        if result is None :
            result = self.webmaster
            if isinstance (result, tuple) :
                result = "%s <%s>" % (result [1], result [0])
            self._email = result
        return result
    # end def email

    @email.setter
    def email (self, value) :
        self._email = value
    # end def email

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
        return tuple (self._get_permissions ("r_permission"))
    # end def r_permissions

    @Once_Property
    def w_permissions (self) :
        return tuple (self._get_permissions ("w_permission"))
    # end def w_permissions

    @property
    def Type (self) :
        return self.__class__.__name__
    # end def Type

    @Once_Property
    def _effective (self) :
        return self
    # end def _effective

    def allow_method (self, method, request) :
        """Returns True if `self` allows `method` for `request.user`"""
        user = request.user
        if not user.superuser :
            pn = method.mode + "_permissions"
            permissions = getattr (self, pn)
            for p in self.permissions () :
                if not p (user, self) :
                    return False
        return True
    # end def allow_method

    def etype_manager (self, obj) :
        etn = getattr (obj, "type_name", None)
        if etn :
            return self.top.ET_Map [etn].manager
    # end def etype

    def send_email (self, template, ** context) :
        email_from = context.get ("email_from")
        if not email_from :
            context ["email_from"] = self.email
        if self.smtp :
            text = self.top.Templateer.render (template, context).encode \
                (self.encoding, "replace")
            self.smtp (text)
        else :
            print ("*** Cannot send email because `smtp` is undefined ***")
            print (text)
    # end def send_email

    def _get_permissions (self, name) :
        p = getattr (self, "_" + name, None)
        if p is not None :
            yield p
        if self.parent :
            for p in getattr (self.parent, name + "s", ()) :
                yield p
    # end def _get_permissions

    def _get_user (self, username) :
        result = self.anonymous_account
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

    def _send_error_email (self, handler, exc, tbi) :
        email     = self.email
        request   = handler.request
        headers   = request.headers
        message   = "Headers:\n    %s\n\nBody:\n    %s\n\n%s" % \
            ( "\n    ".join
                ("%-20s: %s" % (k, v) for k, v in headers.iteritems ())
            , formatted (handler.body)
            , tbi
            )
        if self.DEBUG :
            print ("Exception:", exc)
            print ("Request path", request.path)
            print (message)
            print (handler.body)
        else :
            self.send_email \
                ( self.error_email_template
                , email_from    = email
                , email_to      = email
                , email_subject = ("Error: %s") % (exc, )
                , message       = message
                , NAV           = self.top
                , page          = self
                , request       = request
                )
    # end def _send_error_email

    def __getattr__ (self, name) :
        if self.parent is not None :
            return getattr (self.parent, name)
        raise AttributeError (name)
    # end def __getattr__

    def __repr__ (self) :
        return "<%s %s    %s>" % (self.Type, self.name, self.abs_href)
    # end def __repr__

_Base_ = _RST_Base_ # end class


__doc__ = """
Each supported http method is defined by a separate class of the same name
(in upper case). To disable support in a descendent class, set the
appropriate name to `None`::

    PUT = None

"""

if __name__ != "__main__" :
    GTW.RST._Export ("*")
### __END__ GTW.RST.Resource
