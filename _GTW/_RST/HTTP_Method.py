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
#    GTW.RST.HTTP_Method
#
# Purpose
#    Base classes for HTTP methods
#
# Revision Dates
#     8-Jun-2012 (CT) Creation
#    ««revision-date»»···
#--

from   __future__  import absolute_import, division, print_function, unicode_literals

from   _GTW                     import GTW
from   _TFL                     import TFL

import _GTW._RST

import _TFL._Meta.M_Class
import _TFL._Meta.Object

class _Meta_ (TFL.Meta.M_Class) :

    Table = {}

    def __init__ (cls, name, bases, dct) :
        cls.__m_super.__init__ (name, bases, dct)
        if name != "HTTP_Method" :
            cls.name = name = cls.__name__
            cls.Table [name] = cls
    # end def __init__

# end class _Meta_

class HTTP_Method (TFL.Meta.Object) :
    """Base class for HTTP methods."""

    __metaclass__              = _Meta_

# end class HTTP_Method

class _HTTP_DELETE_ (HTTP_Method) :
    """Implement HTTP method DELETE."""

    _real_name                 = "DELETE"
    mode                       = "w"

DELETE = _HTTP_DELETE_ # end class

class _HTTP_GET_ (HTTP_Method) :
    """Implement HTTP method GET."""

    _real_name                 = "GET"
    mode                       = "r"

GET = _HTTP_GET_ # end class

class _HTTP_HEAD_ (HTTP_Method) :
    """Implement HTTP method HEAD."""

    _real_name                 = "HEAD"
    mode                       = "r"

HEAD = _HTTP_HEAD_ # end class

class _HTTP_OPTIONS_ (HTTP_Method) :
    """Implement HTTP method OPTIONS."""

    _real_name                 = "OPTIONS"
    mode                       = "r"

OPTIONS = _HTTP_OPTIONS_ # end class

class _HTTP_POST_ (HTTP_Method) :
    """Implement HTTP method POST."""

    _real_name                 = "POST"
    mode                       = "w"

POST = _HTTP_POST_ # end class

class _HTTP_PUT_ (HTTP_Method) :
    """Implement HTTP method PUT."""

    _real_name                 = "PUT"
    mode                       = "w"

PUT = _HTTP_PUT_ # end class

if __name__ != "__main__" :
    GTW.RST._Export ("*")
### __END__ GTW.RST.HTTP_Method
