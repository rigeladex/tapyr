from   CT_TK                import root, NORMAL, YES, BOTH, INSERT
from   _TFL                 import TFL
from   _TFL._UI.HTB         import Node, Browser, help
from   _TFL._UI.App_Context import App_Context

import _TFL._TKT._Tk
import _TFL._TKT._Tk.HTB


if __name__ == "__main__" :
    AC = App_Context (TFL)
    def mknode (tb, name) :
        n = Node (tb, name, "1. test line\n2. test line\n3. test line")
        n.insert   (INSERT, "nowrap")
        return n

    def mkchild (tn, name) :
        n = tn.new_child (name, "head", "1. test line\n2. test line")
        return n

    tb  = Browser (AC, root, 'huhu', state = NORMAL)
    tb.ui.browser.pack (expand = YES, fill = BOTH)
    tb.insert          (INSERT, "**             Test me             **\n")
    tn = help          (tb)
    tn.insert          (INSERT, "rindent")
    tn = mknode        (tb,     "n1")
    print "1", tn
    x = mkchild        (tn,     "s1")
    y = tn.new_child ("huhu", "haha", "hihi")
    print "2", tn, x, y
    mkchild            (tn,     "s2")
    nn = mkchild       (tn,     "s3")
    mkchild            (nn,     "ss1")
    nnn = mkchild      (nn,     "ss2")
    tn = mknode        (tb,     "n2")
    mkchild            (tn,     "s-a")
    mkchild            (tn,     "s-b")
    tn.open            ()
    tn = mknode        (tb,     "n3")
    mkchild            (tn,     "s-x")
    mkchild            (tn,     "s-y")
    tn = mknode        (tb,     "n4")
    tb.ui.browser.mainloop ()

