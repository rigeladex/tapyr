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
#    11-Mar-2005 (CT)  `destroy` added and used
#    11-Mar-2005 (CT)  `pack` changed to pass on its `kw` arguments
#    11-Mar-2005 (CT)  `pack` changed to map True/False to values grokable by
#                      Tk
#    13-Apr-2005 (MZO) implemented new_menubar
#    20-Apr-2005 (MZO) Focused_Toplevel return none - like TGW.Focused_Toplevel
#    25-Apr-2005 (CT)  `new_context_menu` removed (wrong name, wrong place)
#    30-Aug-2005 (MZO) [14421] - renamed win_expl_cb
#    19-Jul-2006 (MZO) [18758] `new_menubar` implemented
#    ««revision-date»»···
#--

from _TFL import TFL
from CTK  import *

import _TFL._TKT.Mixin
import _TFL._TKT._Tk
import _TFL._TKT._Tk.Command_Interfacer

class Toplevel (TFL.TKT.Mixin) :
    """A toplevel window -- no optional toolbar etc. yet"""

    Widget_Type = CTK.Toplevel

    _padx = 5
    _pady = 5

    def __init__ \
        ( self
        , menu            = None
        , statusbar       = None
        , title           = ""
        , toolbar         = None
        , name            = ""
        , cb_delete       = None  # callback for destroy event
        , cb_win_explorer = None  # callback (file_uri) if dnd received
        , maximize        = False
        , AC              = None
        , *args
        , **kw
        ) :
        self.__super.__init__ (AC = AC)
        self.cb_delete = cb_delete
        self.wtk_widget = CTK.C_Toplevel \
            (destroy_cmd = self.destroy)
        self._bb        = None
        self.exposed_widget = self.button_box = CTK.Buttongrid   \
            ( self.wtk_widget
            , name        = "button_box"
            , padx        = self._padx
            , pady        = self._pady
            , columns     = 6
            )
        self.button_box.pack (side = BOTTOM)
    # end def __init__

    def destroy (self) :
        if callable (self.cb_delete) :
            self.cb_delete ()
        self.wtk_widget.destroy ()
    # end def destroy

    def pack (self, widget, fill = None, ** kw) :
        if fill == True :
            fill = BOTH
        elif fill == False :
            fill = None
        widget.pack \
            ( fill      = fill
            , side      = BOTTOM
            , padx      = self._padx
            , pady      = self._pady
            , ** kw
            )
    # end def pack

    def show (self) :
        pass
    # end def pack

    def new_menubar (self) :
        if self._bb is None :
            self._bb = self.TNS.CI_Button_Box \
                (self.AC, self.button_box, name = "mb")
            self._bb.wtk_widget.pack \
                ( fill      = X
                , side      = BOTTOM
                , padx      = self._padx
                , pady      = self._pady
                )
        return self._bb
    # end def new_menubar

    def __getattr__ (self, name) :
        res = getattr (self.wtk_widget, name)
        setattr (self, name, res)
        return res
    # end def __getattr__

# end class Toplevel

def Focused_Toplevel () :
    # return focused widget of current active toplevel
    return None
# end def Focused_Toplevel

if __name__ != "__main__" :
    TFL.TKT.Tk._Export ("Toplevel", "Focused_Toplevel")
### __END__ TOM.TKT.TGW.Toplevel
