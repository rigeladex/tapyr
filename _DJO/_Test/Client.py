# -*- coding: iso-8859-1 -*-
# Copyright (C) 2005-2008 Martin Glück. All rights reserved
# Langstrasse 4, A--2244 Spannberg, Austria. martin@smangari.org
# ****************************************************************************
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Library General Public
# License as published by the Free Software Foundation; either
# version 2 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Library General Public License for more details.
#
# You should have received a copy of the GNU Library General Public
# License along with this library; if not, write to the Free
# Software Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
# ****************************************************************************
#
#++
# Name
#    DJO.Test.Client
#
# Purpose
#    Some extensions to the djnago test client
#
# Revision Dates
#     7-Oct-2008 (MG) Creation
#    ««revision-date»»···
#--

from    django.test.client    import Client as DClient
from    django.test           import utils

from   _DJO                   import DJO
import _DJO._Test.Response

from   _TFL                   import TFL
import _TFL._Meta.Object

### setup the DJANGO test system
utils.setup_test_environment ()

class Client (DClient) :
    """Extend the DJNAGO test client."""

    __metaclass__ = TFL.Meta.Object.__class__

    def get (self, * args, ** kw) :
        status_code = kw.pop ("status_code", DJO.Test.no_default)
        response    = self.__super.get (* args, ** kw)
        if status_code != DJO.Test.no_default :
            assert response.status_code == status_code, "%d != %s" % \
                (response.status_code, status_code)
        return response
    # end def get

    def put (self, * args, ** kw) :
        status_code = kw.pop ("status_code", DJO.Test.no_default)
        response    = self.__super.put (* args, ** kw)
        if status_code != DJO.Test.no_default :
            assert response.status_code == status_code, "%d != %s" % \
                (response.status_code, status_code)
        return response
    # end def put

    def request (self, * args, ** kw) :
        response = self.__super.request (* args, ** kw)
        return DJO.Test.Response (response)
    # end def request

# end class Client

if __name__ != "__main__" :
    DJO.Test._Export ("Client")
### __END__ DJO.Test.Client
