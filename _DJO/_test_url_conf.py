# -*- coding: iso-8859-1 -*-
# Copyright (C) 2008 Martin Glück All rights reserved
# Langstrasse 4, 2244 Spannberg, Austria. martin@mangari.org
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
#    DJO._test_url_conf
#
# Purpose
#    A url confif for test purposes
#
# Revision Dates
#    14-Mar-2008 (MG) Creation
#    ««revision-date»»···
#--

from django.conf.urls.defaults   import *
from django.contrib              import admin

def _test_view (request, arg, kw = None) :
    return ""
# end def _test_view


urlpatterns  = patterns \
    ( ""
    ### the following patter is for the test of the `Path_Starts_With`
    ### template tag
    , url (r"^this/is/nice/$", _test_view, name = "test-path-starts-with")
    )

### __END__ DJO._test_url_conf


