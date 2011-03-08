# -*- coding: iso-8859-1 -*-
# Copyright (C) 2011 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# #*** <License> ************************************************************#
# This module is part of the package GTW.AFS.
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
#    GTW.AFS.Error
#
# Purpose
#    Provide exception classes for errors in AFS form processing
#
# Revision Dates
#     2-Mar-2011 (CT) Creation
#     8-Mar-2011 (CT) `Corrupted` added
#    ««revision-date»»···
#--

from   _GTW                     import GTW
from   _TFL                     import TFL

import _GTW._AFS

import _TFL._Meta.Object

from   _TFL.I18N                import _

class Base (Exception) :
    """Base class for AFS exceptions"""

    __metaclass__             = TFL.Meta.M_Class

    message = None
    status  = 400

    def __init__ (self, message = None, status = None, ** kw) :
        if message is not None :
            self.message = message
        if status is not None :
            self.status = status
        assert self.message
        args = (self.message, self.status) + ((kw, ) if kw else ())
        self.__super.__init__ (* args)
        self.__dict__.update  (kw)
    # end def __init__

# end class Base

class Conflict (Base) :

    message = _ \
        ( """Edit conflict: at least one value was changed asynchronously """
          """by another request."""
        )
    status  = 409

# end class Conflict

class Corrupted (Base) :

    message = _ \
        ( """The form values were corrupted somewhere or are too old.""")
    status  = 404

# end class Corrupted

class Timeout (Base) :

    message = _ ("""The edit session has expired.""")
    status  = 408

# end class Timeout

class Unknown (Base) :
    """Used for unknown forms, form elements, ..."""

    status = 404

# end class Unknown

if __name__ != "__main__" :
    GTW.AFS._Export_Module ()
### __END__ GTW.AFS.Error
