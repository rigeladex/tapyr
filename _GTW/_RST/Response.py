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
#    GTW.RST.Response
#
# Purpose
#    Wrap and extend wsgi-specific Response class
#
# Revision Dates
#    20-Jun-2012 (CT) Creation
#    ««revision-date»»···
#--

from   __future__  import absolute_import, division, print_function, unicode_literals

from   _GTW                     import GTW
from   _TFL                     import TFL

import _GTW._RST

from   _TFL._Meta.Once_Property import Once_Property

import _TFL._Meta.M_Auto_Combine_Sets
import _TFL._Meta.M_Class
import _TFL._Meta.Object

class _M_Response_ (TFL.Meta.M_Auto_Combine_Sets, TFL.Meta.M_Class) :
    """Meta class for Response"""

# end class _M_Response_

class _RST_Response_ (TFL.Meta.Object) :
    """Wrap and extend wsgi-specific Response class."""

    __metaclass__     = _M_Response_

    _own_vars         = ("root", "_request", "_response")
    _sets_to_combine  = ("_own_vars", )

    def __init__ (self, _root, _request, * args, ** kw) :
        self.root      = _root
        self._request  = _request
        self._response = _root.HTTP.Response (* args, ** kw)
    # end def __init__

    def __call__ (self, * args, ** kw) :
        return self._response.__call__ (* args, ** kw)
    # end def __call__

    def __getattr__ (self, name) :
        if name not in self._own_vars :
            return getattr (self._response, name)
        raise AttributeError (name)
    # end def __getattr__

    def __setattr__ (self, name, value) :
        if name in self._own_vars :
            return self.__super.__setattr__ (name, value)
        else :
            return setattr  (self._response, name, value)
    # end def __setattr__

Response = _RST_Response_ # end class

if __name__ != "__main__" :
    GTW.RST._Export ("Response")
### __END__ GTW.RST.Response
