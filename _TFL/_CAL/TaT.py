# -*- coding: iso-8859-1 -*-
# Copyright (C) 2004 Mag. Christian Tanzer. All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.cluster
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
#    TaT
#
# Purpose
#    Model a recurrence (i.e., something happening Time-after-Time)
#
# Revision Dates
#    23-Oct-2004 (CT) Creation
#    ««revision-date»»···
#--

from   _TFL                    import TFL
import _TFL._CAL
import _TFL._Meta.Object

from   predicate               import identity

class TaT_Exception_Handler (TFL.Meta.Object) :
    """Model a TaT exception handler"""

    def __init__ (self, condition, delta, alternate = False, max_pos = None, max_neg = None) :
        self.condition = condition
        self.delta     = delta
        self.alternate = alternate
        self.max_pos   = max_pos
        self.max_neg   = max_neg
    # end def __init__

    def __call__ (self, date) :
        result         = date
        condition      = self.condition
        delta          = self.delta
        alternate      = alternate
        max_pos        = self.max_pos
        max_neg        = self.max_neg
        while condition (result) :
            result     = result + delta
            if alternate :
                delta = - delta
            if (  (max_pos and result - date   > max_pos)
               or (max_neg and date   - result > max_neg)
               ) :
                raise StopIteration
        return result
    # end def __call__

# end class TaT_Exception_Handler

class TaT (TFL.Meta.Object) :
    """Model a recurrence (i.e., something happening Time-after-Time)

       >>> from _TFL._CAL.Date  import *
       >>> from _TFL._CAL.Delta import *
       >>> upper = Date (2004, 12, 31)
       >>> start = Date (2004, 10, 23)
       >>> [str (t) for t in TaT (start, Month_Delta (1), upper)]
       ['2004-10-23', '2004-11-23', '2004-12-23']
       >>> [str (t) for t in TaT (start, Month_Delta (2), upper)]
       ['2004-10-23', '2004-12-23']
    """

    def __init__ (self, start, delta, upper, exc_handler = identity) :
        self.start         = start
        self.delta         = delta
        self.upper         = upper
        self.exc_handler   = exc_handler
    # end def __init__

    def __iter__ (self) :
        delta         = self.delta
        upper         = self.upper
        exc_handler   = self.exc_handler
        next          = self.start
        while True :
            n = exc_handler (next)
            if n > upper :
                break
            yield n
            next = next + delta
    # end def __iter__

# end class TaT

if __name__ != "__main__" :
    TFL.CAL._Export ("*")
### __END__ TaT
