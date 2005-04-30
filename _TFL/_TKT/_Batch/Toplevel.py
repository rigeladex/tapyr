# -*- coding: iso-8859-1 -*-
# Copyright (C) 2005 TTTech Computertechnik AG. All rights reserved
# Schönbrunnerstrasse 7, A 1040 Wien, Austria. office@tttech.com
#
#++
# Name
#    TFL.TKT.Batch.Toplevel
#
# Purpose
#    provide Focused_Toplevel
#
# Revision Dates
#    30-Apr-2005 (MZO) Creation
#    ««revision-date»»···
#--

from _TFL import TFL
import _TFL._TKT._Batch

def Focused_Toplevel () :
    return None
# end def Focused_Toplevel

if __name__ != "__main__" :
    TFL.TKT.Batch._Export ("*")
### __END__ TFL.TKT.Batch.Toplevel
