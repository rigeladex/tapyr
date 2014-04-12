# -*- coding: utf-8 -*-
# Copyright (C) 2014 Mag. Christian Tanzer All rights reserved
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
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this module. If not, see <http://www.gnu.org/licenses/>.
# #*** </License> ***********************************************************#
#
#++
# Name
#    GTW.CSS.Property
#
# Purpose
#    CSS property specification with necessary vendor prefixes, if any
#
# Revision Dates
#    12-Apr-2014 (CT) Creation
#    ««revision-date»»···
#--

"""
Specification of CSS properties with automatically generated
vendor prefixes::

    >>> from _TFL.Formatter import formatted_1
    >>> def show (p) :
    ...     print (formatted_1 (p))

    >>> Border    = Property ("border")

    >>> show (Border (color = "red", width = "2px"))
    {'border-color' : 'red', 'border-width' : '2px'}
    >>> show (Border (color = "red", width = "2px", radius = "2px"))
    {'border-color' : 'red', 'border-radius' : '2px', 'border-width' : '2px'}

    >>> Border_pr = Property ("border", radius = ("-moz", "-webkit"))

    >>> show (Border_pr (color = "red", width = "2px"))
    {'border-color' : 'red', 'border-width' : '2px'}
    >>> show (Border_pr (color = "red", width = "2px", radius = "2px"))
    {'-moz-border-radius' : '2px', '-webkit-border-radius' : '2px', 'border-color' : 'red', 'border-radius' : '2px', 'border-width' : '2px'}

    >>> show (Transform (origin = "60% 100%", translate = "100px"))
    {'-ms-transform-origin' : '60% 100%', '-ms-transform-translate' : '100px', '-webkit-transform-origin' : '60% 100%', '-webkit-transform-translate' : '100px', 'transform-origin' : '60% 100%', 'transform-translate' : '100px'}

"""

from   __future__ import division, print_function
from   __future__ import absolute_import, unicode_literals

from   _GTW                       import GTW
from   _TFL                       import TFL

from   _GTW.Parameters            import P_dict
import _GTW._CSS

from   _TFL._Meta.Once_Property   import Once_Property
import _TFL._Meta.Object

from   itertools                  import chain as ichain

class Property (TFL.Meta.Object) :
    """CSS property specification with necessary vendor prefixes, if any."""

    def __init__ (self, _base_name, * _prefixes, ** kw) :
        """`_prefixes` specify the vendor prefixes needed for all values,
           `kw` specify the vendor prefixes needed for the `keys` in `kw`.
        """
        self.base_name = _base_name
        self.prefixes  = _prefixes
        self.vp_map    = dict (kw)
    # end def __init__

    def __call__ (self, ** decls) :
        """Return a dict with `decls` plus any necessary prefixed declarations.
        """
        result    = {}
        base_name = self.base_name
        prefixes  = self.prefixes
        vp_map    = self.vp_map
        for k, v in decls.iteritems () :
            k = k.replace ("_", "-")
            n = "-".join ((base_name, k))
            result [n] = v
            t = k.split ("-") [-1]
            for p in ichain (vp_map.get (t, ()), prefixes) :
                result ["-".join ((p, n))] = v
        return result
    # end def __call__

    @Once_Property
    def P (self) :
        """Property parameter dict: supports lazy evaluation of dict arguments.
        """
        cls = self.__class__
        def _P__call__ (this, P) :
            return self (** P_dict.__call__ (this, P))
        return P_dict.__class__ \
            ( "P_%s" % (cls.__name__)
            , (P_dict, )
            , dict
                ( __call__   = _P__call__
                , __module__ = cls.__module__
                )
            )
    # end def P

# end class Property

Border      = Property ("border")
Box         = Property ("box",                   "-moz",        "-webkit")
Calc        = Property ("calc")
Column      = Property ("column",                "-moz",        "-webkit")
Filter      = Property ("filter",                               "-webkit")
Flex        = Property ("flex",                  "-moz", "-ms", "-webkit")
Font_Feat   = Property ("font-feature-settings", "-moz",        "-webkit")
Gradient    = Property ("gradient",                             "-webkit")
Transform   = Property ("transform",                     "-ms", "-webkit")
Transition  = Property ("transition",                           "-webkit")

if __name__ != "__main__" :
    GTW.CSS._Export ("*")
### __END__ GTW.CSS.Property
