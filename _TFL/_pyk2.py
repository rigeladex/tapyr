# -*- coding: iso-8859-15 -*-
# Copyright (C) 2010-2012 Mag. Christian Tanzer All rights reserved
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
#    TFL._pyk2
#
# Purpose
#    Python2 specific implementation of TFL.pyk
#
# Revision Dates
#    16-Jun-2010 (CT) Creation
#     5-Jan-2011 (CT) `pickle` added
#    18-Apr-2012 (CT) Change `fprint` to encode `sep` and `end`, too
#    ««revision-date»»···
#--

from   _TFL             import TFL

from   _TFL.User_Config import user_config

import cPickle as pickle
import sys

def fprint (* values, ** kw) :
    """print(value, ..., sep=' ', end='\\n', file=sys.stdout)

       Prints the values to a stream, or to sys.stdout by default.
       Optional keyword arguments:
       file: a file-like object (stream); defaults to the current sys.stdout.
       sep:  string inserted between values, default a space.
       end:  string appended after the last value, default a newline.
    """
    def _convert (v, encoding) :
        if not isinstance (v, basestring) :
            v = unicode (v)
        if isinstance (v, unicode) :
            v = v.encode (encoding, "replace")
        return v
    file = kw.pop ("file", None)
    if file is None :
        file = sys.stdout
    enc  = user_config.output_encoding
    sep  = _convert (kw.pop ("sep",  " "),  enc)
    end  = _convert (kw.pop ("end",  "\n"), enc)
    txt  = sep.join (_convert (v, enc) for v in values)
    file.write (txt + end)
# end def fprint

### __END__ TFL._pyk2
