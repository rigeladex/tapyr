# -*- coding: iso-8859-15 -*-
# Copyright (C) 2010-2011 Martin Glueck All rights reserved
# Langstrasse 4, A--2244 Spannberg, Austria. martin@mangari.org
# ****************************************************************************
# This module is part of the package GTW.__test__.
#
# This module is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This module is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this module. If not, see <http://www.gnu.org/licenses/>.
# ****************************************************************************
#
#++
# Name
#    GTW.__test__.Id_Entity_Link
#
# Purpose
#    Test how generic links to object without a relevant root work,
#
# Revision Dates
#    27-Oct-2010 (MG) Creation
#    ««revision-date»»···
#--

test_code = r"""
    >>> scope = Scaffold.scope (%(p1)s, %(n1)s) # doctest:+ELLIPSIS
    Creating new scope MOMT__...

    >>> PAP = scope.PAP
    >>> SWP = scope.SWP
    >>> per = PAP.Person           ("ln", "fn")
    >>> pa1 = SWP.Page             ("title_1", text = "text 1")
    >>> pa2 = SWP.Page             ("title_2", text = "text 2")
    >>> scope.commit               ()

    >>> PAP.Entity_created_by_Person (pa1, per)
    GTW.OMP.PAP.Entity_created_by_Person ((u'title_1', ), (u'ln', u'fn', u'', u''))
    >>> scope.commit ()

    >>> PAP.Entity_created_by_Person (pa2.epk_raw, per.epk_raw, raw = True)
    GTW.OMP.PAP.Entity_created_by_Person ((u'title_2', ), (u'ln', u'fn', u'', u''))
    >>> scope.commit ()
"""

from   _GTW.__test__.model                      import *

__test__ = Scaffold.create_test_dict (test_code)

### __END__ GTW.__test__.Id_Entity_Link
