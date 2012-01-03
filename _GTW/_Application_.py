# -*- coding: iso-8859-15 -*-
# Copyright (C) 2010-2012 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# ****************************************************************************
# This module is part of the package GTW.
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
#    GTW._Application_
#
# Purpose
#    Base class for web applications
#
# Revision Dates
#    28-Jun-2010 (CT) Creation
#    29-Jun-2010 (CT) `_init_handlers` corrected (use `_init_static_handler`)
#    ««revision-date»»···
#--

from   _TFL                import TFL
from   _GTW                import GTW

import _TFL._Meta.Object

class _Application_ (TFL.Meta.Object) :
    """Base class for web applications."""

    def _init_handlers (self, handlers, kw) :
        static_handler = kw.pop ("static_handler", None)
        result = []
        if static_handler :
            result.append (self._init_static_handler (static_handler))
        for handler_spec in handlers :
            result.append (self._init_handler (handler_spec))
        return result, kw
    # end def _init_handlers

    def _init_handler (self, handler_spec) :
        hkw = {}
        if len (handler_spec) > 2 :
            prefix, handler, hkw = handler_spec
        else :
            prefix, handler      = handler_spec
        return (self._handler_pattern (prefix), handler, hkw)
    # end def _init_handler

# end class _Application_

if __name__ != "__main__" :
    GTW._Export ("_Application_")
### __END__ GTW._Application_
