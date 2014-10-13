# -*- coding: utf-8 -*-
# Copyright (C) 2010 Martin Glueck All rights reserved
# Langstrasse 4, A--2244 Spannberg, Austria. martin@mangari.org
# ****************************************************************************
# This module is part of the package GTW.Form.
#
# This module is licensed under the terms of the BSD 3-Clause License
# <http://www.c-tanzer.at/license/bsd_3c.html>.
# ****************************************************************************
#
#++
# Name
#    GTW.Form.__Test
#
# Purpose
#    Simple test for plain forms
#
# Revision Dates
#    19-Jan-2010 (MG) Creation
#    ««revision-date»»···
#--

from   _GTW._Form                         import Form
import _GTW._Form.Auth

form = Form.Auth.Login (None, "/login.html")
#import pdb; pdb.set_trace ()
print form (dict (username = "user1", password = "passwd1"))
### __END__ GTW.Form.__Test


