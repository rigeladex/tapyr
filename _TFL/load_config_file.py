# -*- coding: utf-8 -*-
# Copyright (C) 2006-2010 Mag. Christian Tanzer. All rights reserved
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
#    TFL.load_config_file
#
# Purpose
#    Load config file
#
# Revision Dates
#     5-Jan-2006 (CT) Creation
#    10-Nov-2009 (CT) s/execfile/exec/ to avoid `-3` warning
#    30-Jul-2010 (CT) Moved from `TGL` to `TFL`
#    ««revision-date»»···
#--

from _TFL import TFL
from _TFL import sos

def load_config_file (file_name, globals, locals = None) :
    if locals is None :
        locals = globals
    fname = sos.expanded_path (file_name)
    try :
        with open (fname) as f :
            config = f.read ()
    except IOError :
        pass
    else :
        exec (config, globals, locals)
    return locals
# end def load_config_file

if __name__ != "__main__" :
    TFL._Export ("*")
### __END__ TFL.load_config_file
