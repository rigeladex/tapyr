# -*- coding: utf-8 -*-
# Copyright (C) 2005 Martin Glück. All rights reserved
# Langstrasse 4, A--2244 Spannberg, Austria. office@spannberg.com
# ****************************************************************************
#
# This module is licensed under the terms of the BSD 3-Clause License
# <http://www.c-tanzer.at/license/bsd_3c.html>.
# ****************************************************************************
#
#++
# Name
#    TGL.TKT.HILD.%(name)s
#
# Purpose
#    Wrapper for the hildon widget %(gtk_widget)s (Nokia 770 gtk+ extensions)
#
# Revision Dates
#    %(date)s (%(user)s) Automated creation
#    ««revision-date»»···
#--

from   _TGL._TKT._HILD         import HILD
from   _TGL._TKT._GTK          import GTK
import _TGL._TKT._HILD.%(base)s

class %(name)s (HILD.%(base)s) :
    """Wrapper for the hildon widget %(gtk_widget)s"""

    GTK_Class        = HILD.hildon.%(gtk_widget)s
    __gtk_properties = \\
        ( %(properties)s
        )

# end class %(name)s

if __name__ != "__main__" :
    HILD._Export ("%(name)s")
### __END__ TGL.TKT.HILD.%(name)s
'''

def find_properties (cls) :
    prop   = []
    for p in gobject.list_properties (cls) :
        if p.owner_type == cls.__gtype__ :
            pn   = p.name.replace ("-", "_")
            mode = 0
            opt  = ""
            if hasattr (cls, "set_%s" % pn) :
                mode += 2
            if hasattr (cls, "get_%s" % pn) :
                mode += 1
            prop.append ((pn, p, mode))
    prop.sort ()
    result     = []
    gtk_object = gobject.type_from_name ("GtkObject")
    for name, p, mode in prop :
        if gobject.type_is_a (p.value_type, gtk_object) :
            cls = "GTK.SG_Object_Property "
        elif mode == (p.flags & 0x03) :
            cls = "GTK.SG_Property        "
        else :
            cls = "GTK.Property           "
        opt  = [""]
        if not p.flags & 0x01 :
            opt.append ("get = None")
        if not p.flags & 0x02 :
            opt.append ("set = None")
        element = '%s ("%s"%s)' % (cls, name, ", ".join (opt))
        result.append (element)
    return "\n        , ".join (result)
# end def find_properties

cmd = Command_Line \
    ( arg_spec    = ( "name:S?Name of the new wrapper class"
                    )
    , option_spec = ( "user:S=MG?Username"
                    , "gtk_widget:S?Name of the wrapped GTK widget"
                    , "base:S?Name of the wrapper base class"
                    , "path:S=_TGL/_TKT/_HILD"
                    )
    , help_on_err = True
    , max_args    = 1
    , min_args    = 1
    )
base       = cmd.base
gtk_widget = cmd.gtk_widget or cmd.name.replace ("_", "")
cls        = getattr (hildon, gtk_widget)
if not base :
    pat  = Regexp ("([A-Z])")
    base = pat.subn ("_\\1", cls.mro () [1].__name__) [0] [1:]

d = dict \
    ( name       = cmd.name
    , gtk_widget = gtk_widget
    , date       = time.strftime ("%d-%b-%Y")
    , user       = cmd.user
    , base       = base
    , properties = find_properties (cls)
    )
filename = os.path.join (cmd.path, "%s.py" % (cmd.name, ))
print "%s: class %s (%s) wraps %s" % (filename, cmd.name, base, gtk_widget)
open (filename, "w").write (template % d)
