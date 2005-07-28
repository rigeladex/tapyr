# -*- coding: iso-8859-1 -*-
# Copyright (C) 2005 Mag. Christian Tanzer. All rights reserved
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
#    PMA.TKT.GTK.Eventname
#
# Purpose
#    Define PMA specific eventnames for GTK
#    ««text»»···
#
# Revision Dates
#    28-Jul-2005 (CT) Creation
#    ««revision-date»»···
#--

from   _PMA                        import PMA
from   _TGL                        import TGL
import _TGL._TKT._GTK
import _TGL._TKT._GTK.Eventname

Eventname = TGL.TKT.GTK.Eventname

Eventname.add \
    ( next_message = TGL.TKT.GTK.Key_Binder ("n")
    , next_unseen  = TGL.TKT.GTK.Key_Binder ("<Shift>n")
    , prev_message = TGL.TKT.GTK.Key_Binder ("p")
    , prev_unseen  = TGL.TKT.GTK.Key_Binder ("<Shift>p")
    )

if __name__ != "__main__" :
    PMA.TKT.GTK._Export ("Eventname")
### __END__ PMA.TKT.GTK.Eventname
