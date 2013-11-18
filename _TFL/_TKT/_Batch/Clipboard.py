# -*- coding: utf-8 -*-
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
#    29-Aug-2006 (ABR) Merged in changes from For_Lin_Plan_22_branch
#    23-Jul-2007 (CED) Activated absolute_import
#    06-Aug-2007 (CED) Future import removed again
#    ««revision-date»»···
#--



from _TFL import TFL
import _TFL._TKT._Batch
import _TFL._TKT.Mixin

class Clipboard (TFL.TKT.Mixin) :

    def copiable (self, *args) :
        """Current content is copiable."""
        return True
    # end def copiable

    def cuttable (self, *args) :
        """Current content is cuttable."""
        return True
    # end def cuttable

    def pastable (self, *args) :
        """Current content is pastable."""
        return True
    # end def pastable

    def menu_copy_cmd (self, event = None) :
        """Copy selection."""
        pass
    # end def menu_cut_cmd

    def menu_cut_cmd (self, event = None) :
        """Cut selection."""
        pass
    # end def menu_cut_cmd

    def menu_paste_cmd (self, event = None) :
        """Paste selection."""
        pass
    # end def menu_cut_cmd

# end class Clipboard

if __name__ != "__main__" :
    TFL.TKT.Batch._Export ("*")
### __END__ TFL.TKT.Batch.Clipboard
