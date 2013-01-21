# -*- coding: iso-8859-15 -*-
# Copyright (C) 2012-2013 Martin Glueck All rights reserved
# Langstrasse 4, A--2244 Spannberg, Austria. martin@mangari.org
# #*** <License> ************************************************************#
# This module is part of the package GTW.__test__.
#
# This module is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This module is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this module. If not, see <http://www.gnu.org/licenses/>.
# #*** </License> ***********************************************************#
#
#++
# Name
#    GTW.__test__.SAS_DB_Features
#
# Purpose
#    Test special features only present in SAS backend
#
# Revision Dates
#    13-Aug-2012 (MG) Creation
#    ««revision-date»»···
#--

from   __future__ import absolute_import, division, print_function, unicode_literals

_test_code = r"""
    >>> scope = Scaffold.scope ("sqlite:///test.sqlite", %(n1)s) # doctest:+ELLIPSIS
    Creating new scope MOMT__...

    >>> scope.destroy ()
"""

from   _GTW.__test__.model      import *
from   _MOM.import_MOM          import Q

GTW.OMP.PAP.Person.use_indices = ( ("first_name", "last_name"), )
__test__ = Scaffold.create_test_dict (_test_code)

### __END__ SAS_DB_Features
