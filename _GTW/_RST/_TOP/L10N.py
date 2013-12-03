# -*- coding: utf-8 -*-
# Copyright (C) 2012-2013 Mag. Christian Tanzer All rights reserved
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
#    GTW.RST.TOP.L10N
#
# Purpose
#    Language selection for tree of pages
#
# Revision Dates
#     9-Jul-2012 (CT) Creation
#    23-Jul-2012 (CT) Add argument `response` to `_Language_.GET.__call__`
#    24-Jul-2012 (CT) Fix `_Language_.GET.__call__`
#    26-Nov-2013 (CT) Use cookie, not session, to store `language`
#    26-Nov-2013 (CT) Add `_Language_.skip_etag`
#    ««revision-date»»···
#--

from   __future__ import absolute_import, division, print_function, unicode_literals

from   _GTW                     import GTW
from   _TFL                     import TFL

import _GTW.Notification
import _GTW._RST.HTTP_Method
import _GTW._RST._TOP.Dir
import _GTW._RST._TOP.Page

from   _TFL._Meta.Once_Property import Once_Property

from   _TFL.Decorator           import getattr_safe
from   _TFL.I18N                import _, _T, _Tn

from   posixpath                import join  as pp_join

import itertools

_Ancestor = GTW.RST.TOP.Page

class _Language_ (_Ancestor) :

    implicit  = True
    skip_etag = True

    class _Language__GET_ (_Ancestor.GET) :

        _real_name             = "GET"

        def __call__ (self, resource, request, response) :
            Status   = resource.Status
            language = resource.language
            with TFL.I18N.context (language) :
                next   = request.req_data.get ("next", request.referrer)
                choice = TFL.I18N.Config.choice
                if language.startswith (choice [0]) :
                    response.set_cookie ("language", language, max_age = 1<<31)
                    response.add_notification \
                        ( GTW.Notification
                            (_T (u"Language %s selected") % language)
                        )
                raise Status.Temporary_Redirect (next)
            raise Status.Not_Found ()
        # end def __call__

    GET = _Language__GET_ # end class _Language__GET_

# end class _Language_

class L10N (GTW.RST.TOP.Dir) :
    """Navigation directory supporting language selection."""

    hidden          = True
    pid             = "L10N"

    country_map     = dict\
        ( en        = "us"
        )

    _flag_map       = {}
    _flag_prefix    = "/media/GTW/icons/flags"

    def __init__ (self, ** kw) :
        self.country_map = dict \
            (self.country_map, ** kw.pop ("country_map", {}))
        kw ["entries"] = tuple \
            (   _Language_ (language = l, name = l)
            for l in sorted (TFL.I18N.Config.Languages) if l
            )
        self.__super.__init__ (** kw)
    # end def __init__

    @Once_Property
    @getattr_safe
    def languages (self) :
        return self._entry_map
    # end def languages

    def flag (self, lang) :
        key    = tuple (lang)
        result = self._flag_map.get (key)
        if result is None :
            if isinstance (lang, basestring) :
                lang = lang.split ("_")
            check    = self.static_handler.get_path
            map      = self.country_map
            prefix   = self._flag_prefix
            for l in itertools.chain (reversed (lang), (self.language, "en")) :
                k = (map.get (l) or l).lower ()
                if k :
                    r = pp_join (prefix, "%s.png" % (k, ))
                    if check (r) :
                        result = self._flag_map [key] = r
                        break
        return result
    # end def flag

    def _get_child (self, child, * grandchildren) :
        if not grandchildren :
            result = self.__super._get_child (child)
            if result is None and child :
                result = self.languages.get (child.split ("_") [0])
            return result
    # end def _get_child

    def __nonzero__ (self) :
        return bool (self.languages)
    # end def __nonzero__

# end class L10N

if __name__ != "__main__" :
    GTW.RST.TOP._Export ("*")
### __END__ GTW.RST.TOP.L10N
