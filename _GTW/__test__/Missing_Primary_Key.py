# -*- coding: iso-8859-1 -*-
# Copyright (C) 2010 Martin Glueck All rights reserved
# Langstrasse 4, A--2244 Spannberg. martin@mangari.org
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
#    GTW.__test__.Missing_Primary_Key
#
# Purpose
#    Test what happens if one tries to create an object where a primary key
#    is correctly specified durign object creation
#
# Revision Dates
#    22-Jun-2010 (MG) Creation
#    ««revision-date»»···
#--
_test_code = r"""
    >>> scope = Scaffold.scope (%(p1)s, %(n1)s) # doctest:+ELLIPSIS
    Creating new scope MOMT__...
    >>> PAP = scope.PAP
    >>> PAP.Person.count
    0
    >>> PAP.Person (last_name = u"last_name", first_name = u"", raw = True)
    Traceback (most recent call last):
      ...
    Invariant_Errors: Condition `AC_check_first_name_0` :  (first_name is not None and first_name != '')
        first_name = u''
    >>> PAP.Person.count
    0
    >>> errors = []
    >>> PAP.Person \
    ...     ( last_name  = u"last_name"
    ...     , first_name = u""
    ...     , raw        = True
    ...     , on_error   = errors.append
    ...     )
    ...
    >>> errors
    [Invariant_Errors([Invariant_Error(GTW.OMP.PAP.Person (u'last_name', u'', u'', u''), Condition `AC_check_first_name_0` :  (first_name is not None and first_name != '')
        first_name = u'', (), ())],)]
    >>> PAP.Person.count
    0

"""

from _GTW.__test__.model import *

__test__ = Scaffold.create_test_dict (_test_code)


### __END__ GTW.__test__.Missing_Primary_Key


