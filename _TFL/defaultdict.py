# -*- coding: iso-8859-1 -*-
# Copyright (C) 2006 Mag. Christian Tanzer. All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.cluster
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
#    TFL.defaultdict
#
# Purpose
#    dict with default value for missing entries
#
# Revision Dates
#    13-Mar-2006 (CT) Creation
#    ««revision-date»»···
#--

"""
Python 2.5 is going to add a `defaultdict`. This module is meant to be
used in the meantime.
"""

from _TFL import TFL

class _defaultdict_ (dict) :

    def __getitem__ (self, key) :
        try :
            return super (_defaultdict_, self).__getitem__ (key)
        except KeyError :
            return self.__missing__ (key)
    # end def __getitem__

    def __missing__ (self, key) :
        if self.default_factory is None :
            raise KeyError (key)
        result = self [key] = self.default_factory ()
        return result
    # end def __missing__

# end class _defaultdict_

class defaultdict (_defaultdict_) :
    """defaultdict(_default_factory) --> dict with default factory

       The default factory is called without arguments to produce
       a new value when a key is not present, in __getitem__ only.
       A defaultdict compares equal to a dict with the same items.
    """

    def __init__ (self, _default_factory, * args, ** kw) :
        self.default_factory = _default_factory
        super (defaultdict, self).__init__ (* args, ** kw)
    # end def __init__

# end class defaultdict

if __name__ != "__main__" :
    TFL._Export ("*", "_defaultdict_")
### __END__ TFL.defaultdict
