# -*- coding: iso-8859-1 -*-
# Copyright (C) 2007 Mag. Christian Tanzer. All rights reserved
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
#    DJO.expand_CSS
#
# Purpose
#    Expand a CSS template via the Python `%s` operator
#
# Revision Dates
#    14-Dec-2007 (CT) Creation
#    ««revision-date»»···
#--

from   _TFL                   import TFL
from   _TFL.Filename          import Filename
from   _TFL.Caller            import Scope

def command_spec (arg_array = None) :
    from   _TFL.Command_Line import Command_Line
    return Command_Line \
        ( arg_spec         =
            ( "template:S"
            ,
            )
        , option_spec      = ()
        , min_args         = 1
        , process_keywords = True
        , arg_array        = arg_array
        )
# end def command_spec

def main (cmd) :
    for f in cmd.argv :
        fn = Filename (f, ".css_template")
        pn = Filename (".parameters", fn)
        pd = {}
        execfile    (pn.name, pd)
        ct   = open (fn.name).read ()
        outf = open (Filename (".css", fn).name, "wb")
        outf.write  (ct % Scope (globs = pd, locls = cmd.keywords))
        outf.close  ()
# end def main

if __name__ == "__main__":
    main (command_spec ())
### __END__ expand_CSS
