# -*- coding: iso-8859-15 -*-
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
#    TFL.primes_2
#
# Purpose
#    Provide list of prime numbers up to 100
#
# Revision Dates
#    25-Mar-2001 (CT) Creation
#    11-Feb-2006 (CT) Moved into package `TFL`
#    23-Jul-2007 (CED) Activated absolute_import
#    06-Aug-2007 (CED) Future import removed again
#    ««revision-date»»···
#--



from _TFL.Primes        import Primes

primes = Primes \
    ( (       2,       3,       5,       7,      11,      13,      17,      19
      ,      23,      29,      31,      37,      41,      43,      47,      53
      ,      59,      61,      67,      71,      73,      79,      83,      89
      ,      97
      )
    )

### __END__ TFL.primes_2
