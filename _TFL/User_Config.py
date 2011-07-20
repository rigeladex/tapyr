# -*- coding: iso-8859-15 -*-
# Copyright (C) 2011 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# #*** <License> ************************************************************#
# This module is part of the package TFL.
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
#    TFL.User_Config
#
# Purpose
#    Provide thread-local user configuration
#
# Revision Dates
#    19-Jul-2011 (CT) Creation
#    20-Jul-2011 (CT) `get_tz` and `set_defaults` added
#    ««revision-date»»···
#--

from   __future__  import unicode_literals

from   _MOM        import MOM
from   _TFL        import TFL

import _TFL._Meta.Property
import _TFL.Context

from   dateutil    import tz
import locale
import threading
import sys

class User_Config (threading.local) :
    """Provide thread-local user configuration."""

    _initialzed          = False

    file_system_encoding = sys.getfilesystemencoding ()
    input_encoding       = locale.getpreferredencoding ()
    language             = "en"
    output_encoding      = input_encoding
    time_zone            = tz.tzutc ()
    user                 = None

    def __init__ (self, ** kw) :
        if self._initialzed :
            raise SystemError \
                ( "TFL.User_Config must not be called more than "
                  "once per thread"
                )
        self._initialzed = True
        self.__dict__.update (kw)
    # end def __init__

    def get_tz (self, name = None) :
        """Return tz-info for `name` (default taken from environment).

           For instance::

               tz.gettz ("Europe/Vienna") -->
                   tzfile ('/usr/share/zoneinfo/Europe/Vienna')

        """
        return tz.gettz (name)
    # end def get_tz

    LET = TFL.Meta.Class_and_Instance_Method (TFL.Context.attr_let)

    def set_default (self, name, value) :
        """Set default of attribute `name` to `value`."""
        setattr (self.__class__, name, value)
    # end def set_default

    def set_defaults (self, ** kw) :
        cls = self.__class__
        for k, v in kw.iteritems () :
            setattr (cls, k, v)
    # end def set_defaults

# end class User_Config

user_config = User_Config ()

if __name__ != "__main__" :
    TFL._Export ("*")
### __END__ TFL.User_Config
