# -*- coding: iso-8859-15 -*-
# Copyright (C) 2005 Mag. Christian Tanzer. All rights reserved
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
#    TFL.PMPP
#
# Purpose
#    Poor-Man's Pre-Processor
#
# Revision Dates
#     6-Feb-2005 (CT) Creation
#    25-Mar-2005 (MG) Import of `Filename` changed
#    23-Jul-2007 (CED) Activated absolute_import
#    06-Aug-2007 (CED) Future import removed again
#    ««revision-date»»···
#--



from   _TFL              import TFL
import _TFL._Meta.Object

from   _TFL.Filename     import Filename
from   _TFL.Regexp       import Regexp, re

class PMPP (TFL.Meta.Object) :
    """Poor-Man's Pre-Processor: rewrite a file according to preprocessor
       comments.

       >>> from   StringIO import StringIO
       >>> pp     = PMPP ("TESTTAG")
       >>> source = '''Line before start-tag
       ...    Indented line before start-tag
       ...    # _TESTTAG_LINE_ single tagged line
       ...    Another indented line before start-tag
       ...    # _TESTTAG_START_
       ...    # First tagged line
       ...    #     Second tagged line
       ...    # Third tagged line
       ...    # _TESTTAG_ELSE_
       ...    # First line to be removed by PMPP
       ...    #     Second line to be removed by PMPP
       ...    # _TESTTAG_END_
       ...    Line after end-tag
       ... Last line
       ... '''
       >>> for l in pp (StringIO (source)) :
       ...     print l,
       ...
       Line before start-tag
          Indented line before start-tag
          single tagged line
          Another indented line before start-tag
          First tagged line
              Second tagged line
          Third tagged line
          Line after end-tag
       Last line

    """

    comment_pat   = Regexp (r"\s+ (?P<comment> \# \s*)", re.X)
    pattern_pat   = r"^(?P<indent> \s*) \# \s* _%s_%s_ \s*"

    def __init__ (self, tag) :
        pattern_pat   = self.pattern_pat
        self.head_tag = Regexp (pattern_pat % (tag, "START"), re.X)
        self.else_tag = Regexp (pattern_pat % (tag, "ELSE"),  re.X)
        self.tail_tag = Regexp (pattern_pat % (tag, "END"),   re.X)
        self.line_tag = Regexp (pattern_pat % (tag, "LINE"),  re.X)
    # end def __init__

    def rewrite (self, fname, target_dir) :
        target = Filename (target_dir, fname).name
        f      = open     (fname,  "r")
        o      = open     (target, "w")
        print "Processing %s" % (target, )
        for l in self (f) :
            o.write (l)
    # end def rewrite

    def __call__ (self, source) :
        head_tag    = self.head_tag
        else_tag    = self.else_tag
        tail_tag    = self.tail_tag
        line_tag    = self.line_tag
        comment_pat = self.comment_pat
        comment     = "# "
        for l in source :
            if not head_tag.match (l) :
                if line_tag.match (l) :
                    ### return text without line-tag
                    yield line_tag.sub (r"\g<indent>", l, 1)
                else :
                    ### return untagged text unchanged
                    yield l
            else :
                l = source.next ()
                if comment_pat.match (l) :
                    comment = comment_pat.comment
                while not (else_tag.match (l) or tail_tag.match (l)) :
                    ### return text between start-tag and else- or tail-tag
                    ### without the leading comment
                    yield l.replace (comment, "", 1)
                    l = source.next ()
                if else_tag.match (l) :
                    ### skip over text between else- and tail-tag
                    while not tail_tag.match (l) :
                        l = source.next ()
    # end def __call__

# end class PMPP

"""
Usage examples:
    Demoize  = PMPP ("DEMOVERSION")
    makedemo = Demoize.rewrite

    TMCoize  = PMPP ("TMCVERSION")
"""

if __name__ != "__main__" :
    TFL._Export ("*")
### __END__ TFL.PMPP
