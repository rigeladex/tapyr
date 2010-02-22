# -*- coding: iso-8859-1 -*-
# Copyright (C) 2010 Mag. Christian Tanzer All rights reserved
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
#    ««revision-date»»···
#--

from   _GTW                     import GTW
from   _TFL                     import TFL

import _GTW.Notification
import _GTW._NAV.Base

from   _TFL.I18N                import _, _T, _Tn

class L10N (GTW.NAV.Dir) :
    """Navigation directory for selecting a language for localization."""

    hidden          = True
    pid             = "L10N"

    class _Cmd_ (GTW.NAV._Site_Entity_) :

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

    def _get_child (self, child, * grandchildren) :
        if not grandchildren :
            return self._Cmd_ (parent = self, language = child, name = child)
    # end def _get_child

# end class L10N

if __name__ != "__main__" :
    GTW.NAV._Export ("*")
### __END__ GTW.NAV.L10N
