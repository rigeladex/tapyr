# -*- coding: iso-8859-15 -*-
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
#    13-Jun-2005 (CT)  Some ballast removed
#    13-Jun-2005 (CT)  Tk-exploring prints added
#    28-Aug-2006 (ABR) Merged in changes from For_Lin_Plan_22_branch
#    23-Jul-2007 (CED) Activated absolute_import
#    06-Aug-2007 (CED) Future import removed again
#    ««revision-date»»···
#--



from _TFL import TFL
import _TFL._TKT.Mixin

from CTK import *

class Clipboard (TFL.TKT.Mixin) :

    def copiable (self, *args) :
        """Current content is copiable."""
        #w = CTK.root; print "copyable", w, w.focus_get ()
        return True
    # end def copiable
    #copiable.evaluate_eagerly = True

    def cuttable (self, *args) :
        """Current content is cuttable."""
        #w = CTK.root; print "cutable", w, w.focus_get ()
        return True
    # end def cuttable
    #cuttable.evaluate_eagerly = True

    def pastable (self, *args) :
        """Current content is pastable."""
        #w = CTK.root; print "pastable", w, w.focus_get ()
        return True
    # end def pastable
    #pastable.evaluate_eagerly = True

    def menu_copy_cmd (self, event = None) :
        """Copy selection."""
        w = getattr (event, "widget", CTK.root)
        #print "copy", w, w.focus_get ()
        try :
            s = w.selection_get (selection = "PRIMARY")
        except CTK.TclError:
            pass
        else :
            w.clipboard_clear  ()
            w.clipboard_append (s)
            #print "   ", s
        pass   # XXX implement for Tk
    # end def menu_cut_cmd

    def menu_cut_cmd (self, event = None) :
        """Cut selection."""
        w = getattr (event, "widget", CTK.root)
        #print "cut", w, w.focus_get ()
        pass   # XXX implement for Tk
    # end def menu_cut_cmd

    def menu_paste_cmd (self, event = None) :
        """Paste selection."""
        w = getattr (event, "widget", CTK.root)
        #print "paste", w, w.focus_get ()
        pass   # XXX implement for Tk
    # end def menu_cut_cmd

# end class Clipboard

if __name__ != "__main__" :
    TFL.TKT.Tk._Export ("*")
### __END__ TFL.TKT.Tk.Clipboard
