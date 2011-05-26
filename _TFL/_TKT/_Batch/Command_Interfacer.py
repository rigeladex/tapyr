# -*- coding: iso-8859-15 -*-
# Copyright (C) 2004-2005 Mag. Christian Tanzer. All rights reserved
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
#    Command_Interfacer
#
# Purpose
#    Model command interface for batch toolkit
#
# Revision Dates
#    21-Dec-2004 (CT) Creation
#    11-Jan-2005 (CT) Creation continued
#    24-Feb-2005 (CT) `CI_Button_Box` added
#    14-Mar-2005 (CT) `CI_Button_Box` added to `_Export` call, too
#    14-Mar-2005 (CT) `Boolean_Variable` added
#    26-Apr-2005 (CT) Define CI-classes via `New` (to keep the right name)
#    23-Jul-2007 (CED) Activated absolute_import
#    06-Aug-2007 (CED) Future import removed again
#    ««revision-date»»···
#--



from   _TFL           import TFL
import _TFL._TKT._Batch
import _TFL._TKT.Command_Interfacer

from   Black_Hole     import black_hole

Boolean_Variable = black_hole
CI_Button_Box    = TFL.TKT.Command_Interfacer.New ("CI_Button_Box")
CI_Eventbinder   = TFL.TKT.Command_Interfacer.New ("CI_Eventbinder")
CI_Menu          = TFL.TKT.Command_Interfacer.New ("CI_Menu")
CI_Menubar       = TFL.TKT.Command_Interfacer.New ("CI_Menubar")
CI_Toolbar       = TFL.TKT.Command_Interfacer.New ("CI_Toolbar")

if __name__ != "__main__" :
    TFL.TKT.Batch._Export \
        ( "Boolean_Variable"
        , "CI_Button_Box"
        , "CI_Eventbinder"
        , "CI_Menu"
        , "CI_Menubar"
        , "CI_Toolbar"
        )
### __END__ Command_Interfacer
