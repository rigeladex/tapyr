# -*- coding: iso-8859-1 -*-
# Copyright (C) 2009 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
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
#    TFL.CAO
#
# Purpose
#    Command argument and option processor
#
# Features provided
#    - Automatic type conversions for arguments and options
#    - Default values for arguments and options
#    - Support for sub-commands
#    - Sub-commands and options can be abbreviated (as long as the
#      abbreviation is unique)
#    - Bounds checks on number of arguments and options
#    - Help
#
# Revision Dates
#    31-Dec-2009 (CT) Creation (based on TFL.Command_Line)
#    ««revision-date»»···
#--

"""
This module provides classes for defining and processing commands,
arguments, and options. The values for arguments and options can be
parsed from `sys.argv` or supplied by a client via keyword arguments.

A command is defined by creating an instance of the :class:`Command`
with arguments

- a tuple of :class:`Arg` instances defines the possible arguments,

- a tuple of :class:`Opt` instances defines the possible options,

- the minimum number of arguments required `min_args',

- the maximum number of arguments allowed  `max_args'
  (the default -1 means an unlimited number is allowed),

- a description of the command to be included in the `help',

- a callback function `handler` that performs the command,

- a `name` for the command (by default, the name of the module defining
  the `Command` is used).

For `Arg` and `Opt`, a shortcut string notation can be used:

    `<name>:<type-spec><auto-split-spec>=<default>#<max-number>?<help>`

Calling a :class:`Command` instance with an argument array, e.g.,
`sys.argv`, parses the arguments and options in the array, stores
their values in the instance, and calls the `handler`.

Calling a :class:`Command` instance with keyword arguments initializes
the argument and option values from those values and calls the
`handler`.

Alternatively, the methods `parse`, `store`, and `handle` can be
called by a client, if explicit flow control is required.

"""

from   _TFL               import TFL

from   _TFL.Regexp        import Regexp, re

import _TFL.Abbr_Key_Dict
import _TFL._Meta.Object
import _TFL.sos

class Error (StandardError) :

    def __init__ (self, * args) :
        self.args = args
    # end def __init__

    def __str__ (self) :
        return "Command/argument/option error: %s" % (" ".join (self.args), )
    # end def __str__

    __repr__ = __str__

# end class Error



if __name__ != "__main__" :
    TFL._Export_Module ()
### __END__ TFL.CAO
