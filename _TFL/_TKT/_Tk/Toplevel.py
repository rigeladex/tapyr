# -*- coding: iso-8859-1 -*-
# Copyright (C) 2005 TTTech Computertechnik AG. All rights reserved
# Schönbrunnerstrasse 7, A 1040 Wien, Austria. office@tttech.com
#
#++
# Name
#    TFL.TKT.Tk.Toplevel
#
# Purpose
#    A toplevel window with optional toolbar, menu and statusbar.
#
# Revision Dates
#     3-Mar-2005 (RSC) Creation
#     3-Mar-2005 (RSC) added show
#    10-Mar-2005 (CT)  Don't drop `cb_destroy` on the floor
#    10-Mar-2005 (CT)  s/cb_destroy/cb_delete/
#    10-Mar-2005 (CT)  Use `CTK.C_Toplevel` instead of `CTK.Toplevel`
#    ««revision-date»»···
#--

from _TFL import TFL
from CTK  import *

import _TFL._TKT.Mixin

class Toplevel (TFL.TKT.Mixin) :
    """A toplevel window -- no optional toolbar etc. yet"""

    Widget_Type = CTK.Toplevel

    def __init__ \
        ( self
        , menu        = None
        , statusbar   = None
        , title       = ""
        , toolbar     = None
        , name        = ""
        , cb_delete   = None  # callback for destroy event
        , win_expl_cb = None # callback (file_uri) if dnd received
        , maximize    = False
        , AC          = None
        , *args
        , **kw
        ) :
        self.__super.__init__ (AC = AC)
        self.wtk_widget = self.exposed_widget = CTK.C_Toplevel \
            (destroy_cmd = cb_delete)
    # end def __init__

    def pack (self, widget, ** kw) :
        widget.pack ()
    # end def pack

    def show (self) :
        pass
    # end def pack

    def __getattr__ (self, name) :
        res = getattr (self.wtk_widget, name)
        setattr (self, name, res)
        return res
    # end def __getattr__

# end class Toplevel

Focused_Toplevel = Toplevel

if __name__ != "__main__" :
    TFL.TKT.Tk._Export ("Toplevel", "Focused_Toplevel")
### __END__ TOM.TKT.TGW.Toplevel
