# -*- coding: iso-8859-1 -*-
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
#    TFL.Units.Prefix
#
# Purpose
#    Order of magnitude prefixes
#
# Revision Dates
#     8-Aug-2004 (CT) Creation
#    ««revision-date»»···
#--

from   _TFL import TFL
import _TFL._Units

### http://en.wikipedia.org/wiki/SI_prefix

yocto  = 1E-24
zepto  = 1E-21
atto   = 1E-18
femto  = 1E-15
pico   = 1E-12
nano   = 1E-9
micro  = 1E-6
milli  = 1E-3
centi  = 1E-2
deci   = 1E-1
deka   = 1E+1
hecto  = 1E+2
kilo   = 1E+3
mega   = 1E+6
giga   = 1E+9
tera   = 1E+12
peta   = 1E+15
exa    = 1E+18
zetta  = 1E+21
yotta  = 1E+24

prefix_abbreviations = dict \
    ( y              = yocto
    , z              = zepto
    , a              = atto
    , f              = femto
    , p              = pico
    , n              = nano
    , u              = micro
    , m              = milli
    , c              = centi
    , d              = deci
    , da             = deka
    , h              = hecto
    , k              = kilo
    , M              = mega
    , G              = giga
    , T              = tera
    , P              = peta
    , E              = exa
    , Z              = zetta
    , Y              = yotta
    )

if __name__ != "__main__" :
    TFL.Units._Export \
        ( "prefix_abbreviations"
        , "yocto"
        , "zepto"
        , "atto"
        , "femto"
        , "pico"
        , "nano"
        , "micro"
        , "milli"
        , "centi"
        , "deci"
        , "deka"
        , "hecto"
        , "kilo"
        , "mega"
        , "giga"
        , "tera"
        , "peta"
        , "exa"
        , "zetta"
        , "yotta"
        )
### __END__ Prefix
