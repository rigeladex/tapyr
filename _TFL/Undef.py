# -*- coding: utf-8 -*-
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
#    TFL.Undef
#
# Purpose
#    Provide a class for defining undefined objects with nice repr
#
# Revision Dates
#     3-Sep-2010 (CT) Creation
#    28-Sep-2010 (CT) `__nonzero__` added
#    22-Feb-2013 (CT) Add doc-tests
#    ««revision-date»»···
#--

from   _TFL               import TFL
from   _TFL.pyk           import pyk

@pyk.adapt__bool__
class Undef (object) :
    """Undefined object with nice repr."""

    def __init__ (self, name = None) :
        self.name = name
    # end def __init__

    def __bool__ (self) :
        return False
    # end def __bool__

    def __repr__ (self) :
        names = [self.__class__.__name__]
        if self.name :
            names.append (self.name)
        return "<%s>" % "/".join (names)
    # end def __repr__

# end class Undef

__doc__ = """
Module `Undef`
==========================

:class:`Undef` provides a way to define undefined objects with a nice
and deterministic `repr`.

Normally, one would define an undefined object like this::

    >>> undefined = object ()
    >>> bool (undefined)
    True
    >>> undefined # doctest:+ELLIPSIS
    <object object at ...>

This works well, as long as `undefined` doesn't appear in any context, where
it's `repr` is taken and as long as nobody applies boolean tests to it.

:class:`Undef` avoids both these problems::

    >>> undef = Undef ()
    >>> bool (undef)
    False
    >>> undef
    <Undef>

    >>> undefined_foo = Undef ("foo")
    >>> bool (undefined_foo)
    False
    >>> undefined_foo
    <Undef/foo>

    >>> undefined_bar = Undef ("bar")
    >>> bool (undefined_bar)
    False
    >>> undefined_bar
    <Undef/bar>

    >>> undefined_foo == undefined_bar
    False
    >>> undefined_foo is undefined_bar
    False

    >>> undefined_foo == Undef ("foo")
    False
    >>> undefined_foo is Undef ("foo")
    False

.. moduleauthor:: Christian Tanzer <tanzer@swing.co.at>

"""

if __name__ != "__main__" :
    TFL._Export ("Undef")
### __END__ TFL.Undef
