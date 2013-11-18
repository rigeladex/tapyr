# -*- coding: utf-8 -*-
# Copyright (C) 2005 Mag. Christian Tanzer. All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# ****************************************************************************
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
# ****************************************************************************
#
#++
# Name
#    PMA
#
# Purpose
#    Main program for Pythonic Mail Agent
#
# Revision Dates
#    20-May-2005 (CT) Creation
#    29-Jul-2005 (CT) Call to `load_user_config` added
#    ««revision-date»»···
#--

from   _PMA import PMA
import _PMA._UI.Starter

def main () :
    PMA.load_user_config ()
    cmd = PMA.UI.Starter.command_spec ()
    PMA.UI.Starter (PMA, cmd)
# end def main

if __name__ == "__main__" :
    main ()
### __END__ PMA
