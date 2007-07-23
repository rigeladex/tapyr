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
#    TFL.primes_1
#
# Purpose
#    Provide list of prime numbers up to 10
#
# Revision Dates
#    25-Mar-2001 (CT) Creation
#    11-Feb-2006 (CT) Moved into package `TFL`
#    23-Jul-2007 (CED) Activated absolute_import
#    ��revision-date�����
#--
from __future__ import absolute_import


from _TFL.Primes        import Primes

primes = Primes ((2, 3, 5, 7))

### __END__ TFL.primes_1
