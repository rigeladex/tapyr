# -*- coding: iso-8859-15 -*-
# Copyright (C) 2012 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# #*** <License> ************************************************************#
# This module is part of the package GTW.RST.TOP.
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
#    GTW.RST.TOP.Base
#
# Purpose
#    Basic classes for Tree-of-Page framework
#
# Revision Dates
#     5-Jul-2012 (CT) Creation (based on GTW.NAV.Base)
#     9-Jul-2012 (CT) Add and use `HTTP_Method_Mixin.template_name`
#     9-Jul-2012 (CT) Add `RST_TOP_HTML`, define `.rendered`
#    ««revision-date»»···
#--

from   __future__  import absolute_import, division, print_function, unicode_literals

from   _GTW                     import GTW
from   _TFL                     import TFL

import _GTW.Media
import _GTW._RST.Mime_Type
import _GTW._RST.Resource
import _GTW._RST._TOP

from   _TFL._Meta.Once_Property import Once_Property
from   _TFL                     import sos
from   _TFL.predicate           import uniq

import _TFL.I18N

class RST_TOP_HTML (GTW.RST.Mime_Type.HTML) :

    _real_name                 = "HTML"

    def rendered (self, request, response, body) :
        ### `body` is already rendered as HTML
        return body
    # end def rendered

HTML = RST_TOP_HTML # end class

class HTTP_Method_Mixin (GTW.RST.HTTP_Method) :

    _renderers             = (HTML, )

    template_name          = None

    def _render_context (self, resource, request, response, ** kw) :
        return dict \
            ( request       = request
            , notifications = response.session.notifications
            , ** kw
            )
    # end def _render_context

    def _response_body (self, resource, request, response) :
        template = None
        if self.template_name :
            template = resource.get_template (self.template_name)
        context  = resource.render_context \
            (** self._render_context (resource, request, response))
        result = resource.rendered (context, template = template)
        if result is None :
            raise resource.HTTP.Error_404 ()
        return result
    # end def _response_body

# end class HTTP_Method_Mixin

_Ancestor = GTW.RST._Base_

class _TOP_Base_ (_Ancestor) :
    """Base class for TOP."""

    _real_name                 = "_Base_"

    own_links                  = []
    short_title                = ""
    title                      = ""

    _login_required            = False
    _Media                     = GTW.Media ()

    class _TOP_Base_GET_ (HTTP_Method_Mixin, _Ancestor.GET) :

        _real_name             = "GET"

    GET = _TOP_Base_GET_ # end class

    def __init__ (self, ** kw) :
        self.pop_to_self \
            ( kw
            , "login_required", "Media"
            , prefix = "_"
            )
        self.__super.__init__ (** kw)
    # end def __init__

    @Once_Property
    def copyright (self) :
        year  = time.localtime ().tm_year
        start = int (self.copyright_start)
        yr    = str (year) if year == start else "%4.4d-%4.4d" % (start, year)
        return dict \
            ( holder = self.owner
            , url    = self.copyright_url or "/"
            , year   = yr
            )
    # end def copyright

    @property
    def has_children (self) :
        return bool (getattr (self, "own_links", []))
    # end def has_children

    @property
    def h_title (self) :
        name = self.short_title or self.name or self.href
        if self.parent :
            return "/".join ((name, self.parent.h_title))
        else :
            if self is self.top.home :
                return self.top.h_title
            else :
                return "%s [%s]" % (name, self.top.h_title)
    # end def h_title

    @Once_Property
    def login_required (self) :
        ### if a parent requires login, all children do too (even if they
        ### claim otherwise!)
        return \
            (  self._login_required
            or self.r_permissions
            or (self.parent and self.parent.login_required)
            )
    # end def login_required

    @Once_Property
    def Media (self) :
        return self._get_media ()
    # end def Media

    @Once_Property
    def permalink (self) :
        return self.abs_href
    # end def permalink

    @property
    def q_href (self) :
        return pjoin (self.abs_href, self.q_prefix)
    # end def q_href

    def allow_method (self, method, user) :
        """Returns True if `self` allows `method` for `user`."""
        if self.login_required and not \
               (user and user.authenticated and user.active) :
            return False
        return self.__super.allow_method (method, user)
    # end def allow_method

    def etype_manager (self, obj) :
        etn = getattr (obj, "type_name", None)
        if etn :
            return self.top.ET_Map [etn].manager
    # end def etype_manager

    def formatted (self, sep = "\n    ") :
        kvs = ("%s : %r" % (k, v) for (k, v) in sorted (self._kw.iteritems ()))
        return "<%s %s\n    %s\n  >" % (self.Type, self.name, sep.join (kvs))
    # end def formatted

    def is_current_dir (self, page) :
        return False
    # end def is_current_dir

    def is_current_page (self, page) :
        return \
            (  (self.permalink == page.permalink)
            or (self.href      == page.href)
            )
    # end def is_current_page

    def obj_href (self, obj) :
        man = self.etype_manager (obj)
        if man :
            return man.href_display (obj)
    # end def obj_href

    def page_from_obj (self, obj) :
        result = None
        href   = self.obj_href (obj)
        if href :
            top    = self.top
            result = top.Table.get (href)
            if result is None :
                man = self.etype_manager (obj)
                if man :
                    result = man.page_from_obj (obj)
        return result
    # end def page_from_obj

    def render_context (self, nav_page = None, ** kw) :
        return self.top.Templateer.Context \
            ( NAV           = self.top
            , lang          = "_".join (uniq (TFL.I18N.Config.choice))
            , nav_page      = nav_page or self
            , page          = self
            , ** kw
            )
    # end def render_context

    def rendered (self, context, template = None) :
        result = self.top.Templateer.render \
            (template or self.template, context)
        if self.translator :
            result = self.translator (result)
        return result
    # end def rendered

    def _get_media (self, head = None) :
        medias   = []
        parent   = self.parent
        template = getattr (self, "template")
        if head is not None :
            medias.append (head)
        if self._Media is not _Site_Entity_._Media :
            medias.append (self._Media)
        if getattr (template, "Media", None) :
            medias.append (template.Media)
        if parent and parent.Media is not _Site_Entity_._Media :
            medias.append (parent.Media)
        if medias :
            return GTW.Media (children = medias)
        return self._Media
    # end def _get_media

    def _new_edit_session (self, request, ttl = None) :
        dbmd = self.top.scope.db_meta_data
        user = request.user
        if user is None :
            u_hash = request.username = uuid.uuid1 ().hex
        else :
            u_hash = user.password
        return request.session.new_edit_session \
            ((u_hash, dbmd.dbv_hash, dbmd.dbid, sos.getpid ()), ttl)
    # end def _new_edit_session

_Base_ = _TOP_Base_ # end class

if __name__ != "__main__" :
    GTW.RST.TOP._Export ("*", "_Base_")
### __END__ GTW.RST.TOP.Base
