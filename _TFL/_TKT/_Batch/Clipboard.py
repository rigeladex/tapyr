# -*- coding: iso-8859-1 -*-
# Copyright (C) 2005 TTTech Computertechnik AG. All rights reserved
# Schönbrunnerstrasse 7, A 1040 Wien, Austria. office@tttech.com
#
#++
# Name
#    TFL.TKT.Batch.Clipboard
#
# Purpose
#    Clipboard for api documentation.
#
# Revision Dates
#    29-Aug-2005 (MZO) Creation (i15639)
#    ««revision-date»»···
#--

from _TFL import TFL
import _TFL._TKT._Batch
import _TFL._TKT.Mixin

class Clipboard (TFL.TKT.Mixin) :

    def copyable (self, *args) :
        """Current content is copyable.
        """
        return True
    # end def copyable

    def cutable (self, *args) :
        """Current content is cutable.
        """
        return True
    # end def cutable

    def pasteable (self, *args) :
        """Current content is pasteable.
        """
        return True
    # end def pasteable

    def menu_copy_cmd (self, event = None) :
        """Copy selection.
        """
        pass
    # end def menu_cut_cmd

    def menu_cut_cmd (self, event = None) :
        """Cut selection.
        """
        pass
    # end def menu_cut_cmd

    def menu_paste_cmd (self, event = None) :
        """Paste selection.
        """
        pass
    # end def menu_cut_cmd

# end class Clipboard

if __name__ != "__main__" :
    TFL.TKT.Batch._Export ("*")
### __END__ TFL.TKT.Batch.Clipboard
