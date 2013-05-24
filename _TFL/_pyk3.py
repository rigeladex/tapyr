# -*- coding: iso-8859-15 -*-
# Copyright (C) 2010-2013 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# ****************************************************************************
# This module is part of the package TFL.
#
# This module is free software; you can redistribute it and/or
# modify it under the terms of the GNU Library General Public
# License as published by the Free Software Foundation; either
# version 2 of the License, or (at your option) any later version.
#
# This module is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Library General Public License for more details.
#
# You should have received a copy of the GNU Library General Public License
# icense along with this module; if not, see <http://www.gnu.org/licenses/>.
# ****************************************************************************
#
#++
# Name
#    TFL._pyk3
#
# Purpose
#    Python3 specific implementation of TFL.pyk
#
# Revision Dates
#    16-Jun-2010 (CT) Creation
#     5-Jan-2011 (CT) `pickle` added
#    23-May-2013 (CT) Add `string_types`, `text_type`, `Classic_Class_Type`
#    23-May-2013 (CT) Add class decorator `adapt__bool__`
#    24-May-2013 (CT) Add `adapt__div__`, `adapt__str__`
#    24-May-2013 (CT) Add `iteritems`, `iterkeys`, `itervalues`, `xrange`
#    24-May-2013 (CT) Add `int_types`
#    ««revision-date»»···
#--

from   io     import StringIO

import pickle

Classic_Class_Type = None

fprint             = print

int_types          = (int, )
string_types       = (str, )
text_type          = str

def adapt__bool__ (cls) :
    dct = cls.__dict__
    if "__bool__" not in dct and "__nonzero__" in dct :
        setattr (cls, "__bool__", dct ["__nonzero__"])
    return cls
# end def adapt__bool__

def adapt__div__ (cls) :
    """Nothing to be done here"""
    return cls
# end def adapt__div__

def adapt__str__ (cls) :
    """Nothing to be done here"""
    return cls
# end def adapt__str__

def iteritems (dct) :
    return dct.items ()
# end def iteritems

def iterkeys (dct) :
    return dct.keys ()
# end def iterkeys

def itervalues (dct) :
    return dct.values ()
# end def itervalues

xrange = range

### __END__ TFL._pyk3
