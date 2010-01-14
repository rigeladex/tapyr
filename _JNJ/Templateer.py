# -*- coding: iso-8859-1 -*-
# Copyright (C) 2010 Martin Glueck All rights reserved
# Langstrasse 4, A--2244 Spannberg. martin@mangari.org
# ****************************************************************************
#
# This module is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This module is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this module. If not, see <http://www.gnu.org/licenses/>.
# ****************************************************************************
#
#++
# Name
#    JNJ.Templateer
#
# Purpose
#    Provide the interface require by GTW.NAV to load and render templates
#
# Revision Dates
#    13-Jan-2010 (MG) Creation
#    14-Jan-2010 (CT) s/Templeteer/Templateer/g
#    14-Jan-2010 (CT) Esthetics
#    ««revision-date»»···
#--

from   _JNJ             import JNJ
import _JNJ.Environment

def Templateer (* args, ** kw) :
    result         = JNJ.HTML (* args, ** kw)
    result.Context = dict
    return result
# end def Templateer

if __name__ != "__main__" :
    JNJ._Export ("Templateer")
### __END__ JNJ.Templateer


