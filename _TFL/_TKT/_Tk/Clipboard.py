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
#    13-Jun-2005 (CT)  Some ballast removed
#    13-Jun-2005 (CT)  Tk-exploring prints added
#    ««revision-date»»···
#--

from _TFL import TFL
import _TFL._TKT.Mixin

from CTK import *

class Clipboard (TFL.TKT.Mixin) :

    def copyable (self, *args) :
        """Current content is copyable.
        """
        #w = CTK.root; print "copyable", w, w.focus_get ()
        return True
    # end def copyable
    copyable.evaluate_eagerly = True

    def cutable (self, *args) :
        """Current content is cutable.
        """
        #w = CTK.root; print "cutable", w, w.focus_get ()
        return True
    # end def cutable
    cutable.evaluate_eagerly = True

    def pasteable (self, *args) :
        """Current content is pasteable.
        """
        #w = CTK.root; print "pasteable", w, w.focus_get ()
        return True
    # end def pasteable
    pasteable.evaluate_eagerly = True

    def menu_copy_cmd (self, event = None) :
        """Copy selection.
        """
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
        """Cut selection.
        """
        w = getattr (event, "widget", CTK.root)
        #print "cut", w, w.focus_get ()
        pass   # XXX implement for Tk
    # end def menu_cut_cmd

    def menu_paste_cmd (self, event = None) :
        """Paste selection.
        """
        w = getattr (event, "widget", CTK.root)
        #print "paste", w, w.focus_get ()
        pass   # XXX implement for Tk
    # end def menu_cut_cmd

# end class Clipboard

if __name__ != "__main__" :
    TFL.TKT.Tk._Export ("*")
### __END__ of TFL.TKT.Tk.Clipboard
