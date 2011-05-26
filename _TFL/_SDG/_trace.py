# -*- coding: iso-8859-15 -*-
# Copyright (C) 2004 Mag. Christian Tanzer. All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# ****************************************************************************
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Library General Public
# License as published by the Free Software Foundation; either
# version 2 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Library General Public License for more details.
#
# You should have received a copy of the GNU Library General Public
# License along with this library; if not, write to the Free
# Software Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
# ****************************************************************************
#
#++
# Name
#    TFL.SDG._trace
#
# Purpose
#    Enable tracing of SDG formatting
#
# Revision Dates
#    22-Sep-2004 (CT) Creation
#    23-Jul-2007 (CED) Activated absolute_import
#    06-Aug-2007 (CED) Future import removed again
#    ««revision-date»»···
#--



from   predicate         import *
from   _TFL              import TFL
import _TFL._SDG.Node
import _TFL._SDG.Formatter
import _TFL._FMW.Tracer
import _TFL.Caller

def _ (self) :
    d = {}
    for a in "indent_anchor", "indent_offset", "ht_width" :
        try :
            d [a] = self [a]
        except KeyError :
            pass
    return ", ".join \
        ([("%s = %s" % (n, v)) for (n, v) in sorted (d.iteritems ())])
TFL.Caller.Object_Scope.__str__ = TFL.Caller.Object_Scope.__repr__ = _

def _ (self) :
    return "%s %s" % (self.__class__.__name__, self.name)
TFL.SDG.Node.__repr__ = _

def _ (self) :
    return "%s %s" % (self.__class__.__name__, self.name)
TFL.SDG.Node.__str__ = _

tracer = TFL.FMW.Tracer \
    (recorder = TFL.FMW.Trace_Recorder_F (open ("/tmp/trace", "w")))

Formatter = TFL.SDG._.Formatter

tracer.add_method (TFL.SDG.Node,                               "formatted")
tracer.add_method (Formatter.Partial_Line_Formatter,           "__call__")
tracer.add_method (Formatter.Single_Line_Formatter,            "__call__")
tracer.add_method (Formatter._Recursive_Formatter_,            "__call__")
tracer.add_method (Formatter._Recursive_Formatter_Method_,     "__iter__")
tracer.add_method (Formatter._Recursive_Formatter_Node_,       "__iter__")
tracer.add_method (Formatter._Recursive_Formatter_Attr_,       "__iter__")
tracer.add_method (Formatter._Recursive_Formatters_,           "__call__")
tracer.add_method (Formatter._Recursive_Formatters_,           "__iter__")
tracer.add_method (Formatter.Multi_Line_Formatter,             "__call__")

### __END__ TFL.SDG.Node
