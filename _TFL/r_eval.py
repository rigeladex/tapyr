# -*- coding: iso-8859-15 -*-
# Copyright (C) 2012 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# #*** <License> ************************************************************#
# This module is part of the package TFL.
#
# This module is free software; you can redistribute it and/or
# modify it under the terms of the GNU Library General Public
# License as published by the Free Software Foundation; either
# version 2 of the License, or (at your option) any later version.
#
# This module is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# Library General Public License for more details.
#
# You should have received a copy of the GNU Library General Public License
# along with this module; if not, see <http://www.gnu.org/licenses/>.
# #*** </License> ***********************************************************#
#
#++
# Name
#    TFL.r_eval
#
# Purpose
#    Restricted `eval`
#
# Revision Dates
#     7-Jun-2012 (CT) Creation
#    ««revision-date»»···
#--

from   __future__  import absolute_import, division, print_function, unicode_literals

from   _TFL        import TFL

import re

_eval_restrict_pat = re.compile \
    ( r"(?: (?: ^|\W)(?: lambda)(?: \W|$))|\.__|(?: ^|\W)inspect\."
    , re.VERBOSE
    )

def r_eval (source, ** kw) :
    """Evaluate `source`, in a scope with values of `kw`, but nothing else.


    >>> r_eval ("2 * 2")
    4
    >>> r_eval ("dir ()")
    Traceback (most recent call last):
    ...
    NameError: name 'dir' is not defined
    >>> r_eval ("dir ()", dir = dir)
    ['__builtins__', 'dir']
    >>> r_eval ("type (())")
    Traceback (most recent call last):
    ...
    NameError: name 'type' is not defined
    >>> r_eval ("lambda : 5")
    Traceback (most recent call last):
    ...
    ValueError: Cannot safely evaluate u'lambda : 5'
    >>> r_eval ("().__class__")
    Traceback (most recent call last):
    ...
    ValueError: Cannot safely evaluate u'().__class__'
    """
    if source :
        if _eval_restrict_pat.search (source) :
            raise ValueError ("Cannot safely evaluate %r" % source)
        scope = dict (kw, __builtins__ = {})
        return eval (source, scope)
# end def r_eval

if __name__ != "__main__" :
    TFL._Export ("*")
### __END__ TFL.r_eval
