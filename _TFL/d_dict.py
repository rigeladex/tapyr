#! /usr/bin/python
# -*- coding: iso-8859-1 -*-
# Copyright (C) 1999-2001 Mag. Christian Tanzer. All rights reserved
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
#    d_dict
#
# Purpose
#    Function returning a dictionary allowing
#    - to derive a new dictionary from any number of existing dictionaries
#    - to initialize a new dictionary with keyword syntax (no quotes
#      necessary around keys)
#
# Revision Dates
#    11-Sep-2001 (CT) Creation (factored from `D_Dict`)
#    16-Jan-2003 (CT) Aesthetics
#    ««revision-date»»···
#--

def d_dict (* ancestors, ** kw) :
    """Returns a dictionary,

       `d_dict` adds just a bit of syntactic sugar for the initialization of
       dictionary objects:

       - a new dictionary can be initialized with the contents of any number
         of existing dictionaries (the values from the existing dictionaries
         are copied during the construction of the new dictionary)

       - values for the new dictionary can be specified with keyword notation
         -- this saves the quotes for string-valued keys

       For instance, given two dictionaries `d1` and `d2` as

           d1 = {"spam" : 2, "eggs" : 3}
           d2 = d_dict (ham = 1, brunch = "Bacon")

       `d3` can be defined as

           d3 = d_dict (d1, d2, foo = "bar", spam = 0)

       instead of

           d3 = {"foo" : "bar", "spam" : 0}
           d3.update (d2)
           d3.update (d1)

       or even (more verbose, but probably with the intended effect):

           d3 = {}
           d3.update (d2)
           d3.update (d1)
           d3.update ({"foo" : "bar", "spam" : 0})
    """
    result = {}
    if ancestors :
        ancestors = list  (ancestors)
        ancestors.reverse ()
        map               (result.update, ancestors)
    result.update (kw)
    return result
# end def d_dict

from _TFL import TFL
TFL._Export ("*")

### __END__ d_dict
