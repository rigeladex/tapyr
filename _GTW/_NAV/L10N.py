# -*- coding: utf-8 -*-
# Copyright (C) 2010-2012 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# ****************************************************************************
# This module is part of the package GTW.NAV.
#
# This module is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This module is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this module. If not, see <http://www.gnu.org/licenses/>.
# ****************************************************************************
#
#++
# Name
#    GTW.NAV.L10N
#
# Purpose
#    Provide language selection for GTW.NAV
#
# Revision Dates
#    22-Feb-2010 (CT) Creation
#    22-Feb-2010 (CT) `languages` and `flag` added
#    24-Feb-2010 (CT) `_Cmd_`: s/GTW.NAV._Site_Entity_/GTW.NAV.Page/
#     3-May-2012 (CT) Add `flag_dir`, change `flag` to use it
#    ««revision-date»»···
#--

from   _GTW                     import GTW
from   _TFL                     import TFL

import _GTW.Notification
import _GTW._NAV.Base

from   _TFL._Meta.Once_Property import Once_Property
from   _TFL.I18N                import _, _T, _Tn
from   _TFL                     import sos

import itertools

from   posixpath                import join as pjoin

class L10N (GTW.NAV.Dir) :
    """Navigation directory for selecting a language for localization."""

    hidden          = True
    pid             = "L10N"

    country_map     = dict\
        ( en        = "us"
        )

    class _Cmd_ (GTW.NAV.Page) :

        implicit          = True
        SUPPORTED_METHODS = set (("GET", "POST"))

        def rendered (self, handler, template = None) :
            HTTP      = self.top.HTTP
            language  = self.language
            with TFL.I18N.context (language) :
                choice = TFL.I18N.Config.choice
                if language.startswith (choice [0]) :
                    handler.session ["language"] = (language, )
                    handler.session.notifications.append \
                        ( GTW.Notification
                            (_T (u"Language %s selected") % language)
                        )
                next = handler.request.headers.get ("Referer", "/")
                raise HTTP.Redirect_307 (next)
            raise HTTP.Error_404 ()
        # end def rendered

    # end class _Cmd_

    def __init__ (self, src_dir, parent, ** kw) :
        self.country_map = dict \
            (self.country_map, ** kw.pop ("country_map", {}))
        self.__super.__init__ (src_dir = src_dir, parent = parent, ** kw)
    # end def __init__

    def flag (self, lang) :
        if isinstance (lang, basestring) :
            lang = lang.split ("_")
        map = self.country_map
        for l in itertools.chain (reversed (lang), (self.language, "en")) :
            k = (map.get (l) or l).lower ()
            if k :
                f = "%s.png" % (k, )
                if sos.path.exists (sos.path.join (self.flag_dir, f)) :
                    return pjoin ("/media/GTW/icons/flags", f)
    # end def flag

    @Once_Property
    def flag_dir (self) :
        return sos.path.normpath \
            ( sos.path.join
                ( sos.path.dirname (__file__)
                , ".."
                , "media/icons/flags"
                )
            )
    # end def flag_dir

    @Once_Property
    def languages (self) :
        result = {}
        for l in TFL.I18N.Config.Languages :
            if l :
                result [l] = self._Cmd_ \
                    (parent = self, language = l, name = l)
        return result
    # end def languages

    @property
    def own_links (self) :
        return self.languages.itervalues ()
    # end def own_links

    def _get_child (self, child, * grandchildren) :
        if not grandchildren :
            result = self.languages.get (child)
            if result is None :
                result = self.languages.get (child.split ("_") [0])
            if result is not None :
                return result
    # end def _get_child

    def __nonzero__ (self) :
        return bool (self.languages)
    # end def __nonzero__

# end class L10N

if __name__ != "__main__" :
    GTW.NAV._Export ("*")
### __END__ GTW.NAV.L10N
