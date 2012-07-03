# -*- coding: iso-8859-15 -*-
# Copyright (C) 2010-2012 Martin Glueck All rights reserved
# Langstrasse 4, A--2244 Spannberg, Austria. martin@mangari.org
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
#    GTW.Request_Data
#
# Purpose
#    Wrapper around ddict like data where the values are lists but should not
#    be lists
#
# Revision Dates
#    19-Jan-2010 (MG) Creation
#    20-Jan-2010 (MG) Check's added to make sure the values in the original
#                     data dict contains exactly one element
#    20-Jan-2010 (MG) Support dict's which don't have lists as value's
#    29-Jan-2010 (MG) `__getitem__` and `get` fixed
#     3-Feb-2010 (MG) `iteritems` added
#    10-Feb-2010 (MG) Convert the data into unicode
#    21-Feb-2010 (MG) `pop` added
#    20-Mar-2010 (MG) Moved into `GTW` package
#    28-Jun-2010 (MG) `iterkeys` added
#    14-Nov-2011 (CT) Change `iteritems` to `_convert_element`
#    14-Nov-2011 (CT) Add `__nonzero__`
#    21-Nov-2011 (CT) Change `_convert_element` to `logging` instead of `assert`
#    20-Jun-2012 (CT) Add `Request_Data_List`; factor/rewrite `_normalized`
#     2-Jul-2012 (CT) Add `has_option`
#     3-Jul-2012 (CT) Redefine `Request_Data_List.get` to fix `default`
#    ��revision-date�����
#--

from   _TFL              import TFL
import _TFL._Meta.Object

from   _GTW              import GTW

import  logging

class _GTW_Request_Data_ (TFL.Meta.Object) :
    """Convert the list values into no lists during access."""

    _real_name = "Request_Data"

    def __init__ (self, data) :
        self.data = data
    # end def __init__

    def get (self, key, default = None) :
        return self._convert_element (key, self.data.get (key, default))
    # end def get

    def has_option (self, key) :
        """Return value of `key` or True, if `key` was specified with empty
           value.
        """
        result = self.get (key)
        if result == "" :
            result = True
        elif result and result.lower () in ("no", "false", "0") :
            result = False
        return result
    # end def has_option

    def iteritems (self) :
        convert = self._convert_element
        for key in self.data.iterkeys () :
            yield key, convert (key, self [key])
    # end def iteritems

    def iterkeys (self) :
        return self.data.iterkeys ()
    # end def iterkeys

    def pop (self, key, default = None) :
        return self._convert_element (key, self.data.pop (key, default))
    # end def pop

    def _convert_element (self, key, value) :
        if isinstance (value, (list, tuple)) :
            if len (value) != 1 :
                logging.warning \
                    ( "Got multiple values for '%s', using '%s', ignoring: %s"
                    , key, value [0], value [1:]
                    )
            value = value [0]
        return self._normalized (value)
    # end def _convert_element

    def _normalized (self, value) :
        if isinstance (value, (str, bytes)) :
            return unicode (value, "utf8", "replace")
        return value
    # end def _normalized

    def __contains__ (self, item) :
        return item in self.data
    # end def __contains__

    def __getitem__ (self, key) :
        return self._convert_element (key, self.data [key])
    # end def __getitem__

    def __iter__ (self) :
        return iter (self.data)
    # end def __iter__

    def __nonzero__ (self) :
        return bool (self.data)
    # end def __nonzero__

    def __repr__ (self) :
        return repr (self.data)
    # end def __repr__

Request_Data = _GTW_Request_Data_ # end class

class _GTW_Request_Data_List_ (_GTW_Request_Data_) :
    """Convert all values into lists during access."""

    _real_name = "Request_Data_List"

    def get (self, key, default = []) :
        return self.__super.get (key, default)
    # end def get

    def _convert_element (self, key, value) :
        normalized = self._normalized
        if isinstance (value, (list, tuple)) :
            return list (normalized (x) for x in value)
        return [normalized (value)]
    # end def _convert_element

Request_Data_List = _GTW_Request_Data_List_ # end class

if __name__ != "__main__" :
    GTW._Export ("*")
### __END__ GTW.Request_Data
