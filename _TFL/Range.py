# -*- coding: iso-8859-1 -*-
# Copyright (C) 2001 Mag. Christian Tanzer. All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
#
#++
# Name
#    Range
#
# Purpose
#    Implement range generator
#
#    Blatantly stolen from a posting by "Andrew Dalke" <dalke@acm.org> in
#    comp.lang.python on Wed, 9 May 2001 12:20:56 -0600,
#    Message-id: <9dc1se$tdn$1@nntp9.atl.mindspring.net>
#    References: <mailman.989424256.5933.python-list@python.org>
#
# Revision Dates
#    10-May-2001 (CT) Creation
#    21-Feb-2002 (CT) `Range_` renamed to `_Range_`
#    ««revision-date»»···
#--

import types

class _Range_ :
    """Range generator: takes integers and slices as arguments to
       `[]' and returns a list of indices as specified by the arguments.

       For instance,

       >>> Range [1]
       [0]
       >>> Range [5]
       [0, 1, 2, 3, 4]
       >>> Range [4:8]
       [4, 5, 6, 7]
       >>> Range [4:8:2]
       [4, 6]
       >>> Range [1:3, 7:9]
       [1, 2, 7, 8]
       >>> Range [0:10:2, 10:100:10]
       [0, 2, 4, 6, 8, 10, 20, 30, 40, 50, 60, 70, 80, 90]
    """

    def __getitem__ (self, indices) :
        if type (indices) != type (()) :
            indices = (indices, )
        result = []
        for i in indices :
            if type (i) == types.SliceType :
                result.extend (range (i.start, i.stop, i.step or 1))
            else :
                result.extend (range (i))
        return result
    # end def __getitem__

# end class _Range_

Range = _Range_ ()

### unit-test code ############################################################

if __debug__ :
    import U_Test

    def _doc_test () :
        import Range
        return U_Test.run_module_doc_tests (Range)
    # end def _doc_test

    if __name__ == "__main__" :
        _doc_test ()
# end if __debug__

### end unit-test code ########################################################

from _TFL import TFL

if __name__ != "__main__" :
    TFL._Export ("*")

### __END__ Range
