# -*- coding: iso-8859-1 -*-
# Copyright (C) 2005  Philipp Gortan <gortan@tttech.com>
# ****************************************************************************
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
# ****************************************************************************
#
#++
# Name
#    TFL.Traceback_Printer
#
# Purpose
#    Pretty-Print Traceback Information
#
# Revision Dates
#     9-Aug-2005 (PGO) Creation
#     8-Mar-2006 (CT)  `* args` added to `__call__`
#    ««revision-date»»···
#--

from    _TFL                 import  TFL
import  _TFL._Meta.Object

import  sys
import  traceback

class _Traceback_Printer_ (TFL.Meta.Object) :
    """Traceback Pretty-Printer"""

    _default_format_str = \
        (   __debug__
        and "%(fn)s:%(number)d in '%(function)s':\n\t%(text)s"
        or  "%(fn)s:%(number)d"
        )

    def __init__ (self, format_str = None, cutter = None) :
        """`format_str` defines format of 1 traceback line,
           `cutter` has to be a compiled re pattern
        """
        self.format_str = format_str or self._default_format_str
        self.cutter     = cutter
    # end def __init__

    def __call__ (self, * args) :
        print self.as_string ()
        for a in args :
            print a
    # end def __call__

    def as_string (self) :
        """Extracts exception and traceback information and perform
           pretty-printing. Returns a string.
        """
        exc_type, exc_value, exc_tb = sys.exc_info ()
        if not (exc_type and exc_tb) :
            return
        res = []
        for tb_line in traceback.extract_tb (exc_tb) :
            res.append (self._one_tb_line (tb_line))
        res.append ("\n%s: %s\n" % (exc_type.__name__, exc_value))
        return "\n".join (res)
    # end def as_string

    def _cut (self, s) :
        """returns `s`, reduced by the first match of the cutter"""
        if self.cutter :
            s = self.cutter.sub ("", s)
        return s
    # end def _cut

    def _one_tb_line (self, line) :
        """generate one traceback line (apply format string)"""
        fn, number, function, text = line
        fn = self._cut (fn)
        return self.format_str % locals ()
    # end def _one_tb_line

# end class _Traceback_Printer_

Traceback_Printer = _Traceback_Printer_ ()

if __name__ != "__main__" :
    TFL._Export ("_Traceback_Printer_", "Traceback_Printer")
### __END__ TFL.Traceback_Printer
