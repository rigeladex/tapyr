# -*- coding: iso-8859-15 -*-
# Copyright (C) 2011 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# #*** <License> ************************************************************#
# This module is part of the package GTW.CSS.
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
# #*** </License> ***********************************************************#
#
#++
# Name
#    GTW.CSS.Border
#
# Purpose
#    Model a CSS border specification
#
# Revision Dates
#    21-Feb-2011 (CT) Creation
#    23-Mar-2011 (CT) `P_Border` added
#    ««revision-date»»···
#--

from   __future__  import absolute_import, division
from   __future__  import print_function, unicode_literals

from   _GTW                       import GTW
from   _TFL                       import TFL

from   _GTW.Parameters            import P_dict
import _GTW._CSS

_prefix_map = dict \
    ( radius     = ("-moz", "-webkit")
    )

def Border (** declarations) :
    """Model a CSS border specification.

    >>> print (sorted (Border (color = "red", width = "2px").items ()))
    [(u'border-color', u'red'), (u'border-width', u'2px')]
    >>> print (sorted (Border (color = "red", width = "2px", radius = "2px").items ()))
    [(u'-moz-border-radius', u'2px'), (u'-webkit-border-radius', u'2px'), (u'border-color', u'red'), (u'border-radius', u'2px'), (u'border-width', u'2px')]
    """
    result = {}
    for k, v in declarations.iteritems () :
        k = k.replace ("_", "-")
        n = "-".join (("border", k))
        result [n] = v
        t = k.split ("-") [-1]
        for p in _prefix_map.get (t, ()) :
            result ["-".join ((p, n))] = v
    return result
# end def Border

class P_Border (P_dict) :
    """Border parameter dict: supports lazy evaluation of dict arguments."""

    def __call__ (self, P) :
        return Border (** self.__super.__call__ (P))
    # end def __call__

# end class P_Border

if __name__ != "__main__" :
    GTW.CSS._Export ("*")
### __END__ GTW.CSS.Border
