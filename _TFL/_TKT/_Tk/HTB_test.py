from   CT_TK                import root, YES, BOTH
from   _TFL                 import TFL
import _TFL._UI.HTB
from   _TFL._UI.App_Context import App_Context

import _TFL._TKT._Tk
import _TFL._TKT._Tk.Text
import _TFL._TKT._Tk.Butcon

if __name__ == "__main__" :
    AC = App_Context (TFL)
    def mknode (tb, name) :
        n = TFL.UI.HTB.Node \
            (tb, name, "1. test line\n2. test line\n3. test line")
        n.insert (tb.current_pos, "nowrap")
        return n

    def mkchild (tn, name) :
        n = tn.new_child (name, "1. test line\n2. test line")
        return n

    tb  = TFL.UI.HTB.Browser (AC, name = 'huhu')
    tb.text.exposed_widget.pack  (expand = YES, fill = BOTH)

    tb.insert            (tb.current_pos, "**           Test me           **\n")
    tn = TFL.UI.HTB.help (tb)
    tn.insert            (tb.current_pos, "rindent")
    tn = mknode          (tb, "n1")
    x = mkchild          (tn, "s1")
    mkchild              (tn, "s2")
    nn = mkchild         (tn, "s3")
    mkchild              (nn, "ss1")
    nnn = mkchild        (nn, "ss2")
    tn = mknode          (tb, "n2")
    mkchild              (tn, "s-a")
    mkchild              (tn, "s-b")
    tn.open              ()
    tn = mknode          (tb, "n3")
    mkchild              (tn, "s-x")
    mkchild              (tn, "s-y")
    tn = mknode          (tb, "n4")

    tb.text.exposed_widget.mainloop ()

