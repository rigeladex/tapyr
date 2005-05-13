# -*- coding: iso-8859-1 -*-
# Copyright (C) 2005 TTTech Computertechnik AG. All rights reserved
# Schönbrunnerstrasse 7, A 1040 Wien, Austria. office@tttech.com
#
#++
# Name
#    TFL.TKT.Tk.Clipboard
#
# Purpose
#    Clipboard for Tk
#
# Revision Dates
#    13-May-2005 (MZO) Creation
#    ««revision-date»»···
#--

from _TFL import TFL
import _TFL._TKT.Mixin

class Clipboard (TFL.TKT.Mixin) :

    def __init__ (self, AC = None) : 
        self.AC = AC
        self.__super.__init__ (AC = self.AC)
    # end def __init__

    def copyable (self, *args) :
        """Current content is copyable.
        """
        return True
    # end def copyable
    # copyable.evaluate_eagerly = True
    
    def cutable (self, *args) :
        """Current content is cutable.
        """
        return True
    # end def cutable
    # cutable.evaluate_eagerly = True
    
    def pasteable (self, *args) :
        """Current content is pasteable.
        """
        return True
    # end def pasteable
    #pasteable.evaluate_eagerly = True

    def menu_copy_cmd (self, event = None) :
        """Copy selection.
        """
        pass   # XXX implement for Tk
    # end def menu_cut_cmd

    def menu_cut_cmd (self, event = None) :
        """Cut selection.
        """
        pass   # XXX implement for Tk
    # end def menu_cut_cmd

    def menu_paste_cmd (self, event = None) :
        """Paste selection.
        """
        pass   # XXX implement for Tk
    # end def menu_cut_cmd

# end class Clipboard

if __name__ != "__main__" :
    TFL.TKT.Tk._Export ("*")
### __END__ of TFL.TKT.Tk.Clipboard
