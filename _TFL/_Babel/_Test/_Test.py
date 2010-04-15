# -*- coding: iso-8859-1 -*-
# Copyright (C) 2010 Martin Glueck All rights reserved
# Langstrasse 4, A--2244 Spannberg, Austria. martin@mangari.org
# ****************************************************************************
# This module is part of the package TFL.Babel.
#
# This module is free software; you can redistribute it and/or
# modify it under the terms of the GNU Library General Public
# License as published by the Free Software Foundation; either
# version 2 of the License, or (at your option) any later version.
#
# This module is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Library General Public License for more details.
#
# You should have received a copy of the GNU Library General Public License
# icense along with this module; if not, see <http://www.gnu.org/licenses/>.
# ****************************************************************************
#
#++
# Name
#    TFL.Babel._Test
#
# Purpose
#    Test file which will be parsed.
#
# Revision Dates
#    15-Apr-2010 (MG) Creation
#    ««revision-date»»···
#--

from   _TFL.I18N import _, _T, _Tn, Translations, Config
import  os

_ ("Just markup")
print _T  ("Markup and translation")
print _Tn ("Singular", "Plural", 2)

path  = os.path.join (os.path.dirname (__file__), "-I18N", "de.mo")
Config.current = Translations (open (path), "messages")

print "_T tests"
print _T  ("Just markup")
print _T  ("Markup and translation")
print _T  ("Singular")
print _T  ("Plural")
print "_Tn tests"
print _Tn ("Singular", "Plural", 0)
print _Tn ("Singular", "Plural", 1)
print _Tn ("Singular", "Plural", 2)
### __END__ TFL.Babel._Test


