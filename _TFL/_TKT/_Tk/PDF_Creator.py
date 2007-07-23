# -*- coding: iso-8859-1 -*-
# Copyright (C) 2005 TTTech Computertechnik AG. All rights reserved
# Schönbrunnerstrasse 7, A 1040 Wien, Austria. office@tttech.com
#
#++
# Name
#    TFL.TKT.Tk.PDF_Creator.py
#
# Purpose
#    Currently do nothing if TK-Toolkit
#
# Revision Dates
#    12-Apr-2005 (MZO) Creation
#    23-Jul-2007 (CED) Activated absolute_import
#    ««revision-date»»···
#--
from __future__ import absolute_import


from _TFL import TFL
import _TFL._Meta.Object

class PDF_Creator (TFL.Meta.Object) :
    def __init__ (self, source, gui, filename = None) :
        pass
    # end def __init__

    def open_pdf (self) :
        pass
    # end def open_pdf
# end class PDF_Creator

if __name__ != "__main__" :
    import _TFL._TKT._Tk
    TFL.TKT.Tk._Export ("*")
### __END__ TFL.TKT.Tk.PDF_Creator.py
