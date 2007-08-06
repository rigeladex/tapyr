# -*- coding: iso-8859-1 -*-
# Copyright (C) 2001-2006 Mag. Christian Tanzer. All rights reserved
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
#    TFL.Primes
#
# Purpose
#    Provide list of prime numbers up to a certain boundary
#
# Revision Dates
#    25-Mar-2001 (CT)  Creation
#    11-Feb-2006 (CT)  Moved into package `TFL`
#     8-Nov-2006 (PGO) Primes are immutable
#    23-Jul-2007 (CED) Activated absolute_import
#    06-Aug-2007 (CED) Future import removed again
#    ««revision-date»»···
#--



from   _TFL               import TFL
import _TFL.Ordered_Set

from math               import sqrt

class Primes (TFL.Immutable_Ordered_Set) :
    """List of primes up to a certain boundary"""

    Factors      = {}
    U_Factors    = {}

    def is_prime (self, p) :
        return self.index_dict.has_key (p)
    # end def is_prime

    def factors (self, number, _i = 0) :
        """Returns list of all prime factors of `number'."""
        try :
            return self.Factors [number]
        except KeyError :
            last_p = int (sqrt (number))
            for p in self [_i:] :
                if p > last_p :
                    ### if we didn't find any prime factor yet, `number' must
                    ### be prime itself
                    result = [number]
                    break
                div, mod = divmod (number, p)
                if mod == 0 :
                    result = [p] + self.factors (div, _i)
                    break
                _i = _i + 1
            else :
                raise ValueError, (str (number), "Needs bigger prime table")
            self.Factors [number] = result
            return result
    # end def factors

    def u_factors (self, number, _i = 0) :
        """Returns list of all unique prime factors of `number' (i.e.,
           `result' contains each factor only once).
        """
        try :
            return self.U_Factors [number]
        except KeyError :
            last_p = int (sqrt (number))
            for p in self [_i:] :
                if p > last_p :
                    ### if we didn't find any prime factor yet, `number' must
                    ### be prime itself
                    result = [number]
                    break
                div, mod = divmod (number, p)
                if mod == 0 :
                    result = self.u_factors (div, _i) [:]
                    if [p] != result [0:1] :
                        result [0:0] = [p]
                    break
                _i = _i + 1
            else :
                raise ValueError, (str (number), "Needs bigger prime table")
            self.U_Factors [number] = result
            return result
    # end def u_factors

    def __contains__ (self, item) :
        return item in self.index_dict
    # end def __contains__

# end class Primes

if __name__ != "__main__" :
    TFL._Export ("*")
### __END__ TFL.Primes
