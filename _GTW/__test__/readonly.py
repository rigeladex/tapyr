# -*- coding: iso-8859-1 -*-
# Copyright (C) 2010 Martin Glueck All rights reserved
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
#    GTW.__test__.readonly
#
# Purpose
#    «text»···
#
# Revision Dates
#    11-Aug-2010 (MG) Creation
#    ««revision-date»»···
#--

_test_code = r"""

    >>> scope = Scaffold.scope (%(p1)s, %(n1)s) # doctest:+ELLIPSIS
    Creating new scope MOMT__...
    >>> p = scope.PAP.Person ("LN", "FN")
    >>> scope.commit         () ### should work
    >>> scope.destroy        ()

    >>> apt, url = Scaffold.app_type_and_url (%(p1)s, %(n1)s)
    >>> db_man   = MOM.DB_Man.connect   (apt, url)
    >>> db_man.change_readonly          (True)

    >>> scope = Scaffold.scope (%(p1)s, %(n1)s, create = False) # doctest:+ELLIPSIS
    Loading scope MOMT__...

    The scope is now readonly. So commiting a change should raise an error
    >>> p2 = scope.PAP.Person ("LN2", "FN")
    >>> scope.commit          () # create failes
    Traceback (most recent call last):
       ...
    Readonly_DB

    The scope is now readonly. So commiting a change should raise an error
    >>> p = scope.PAP.Person.query ().one ()
    >>> p.set_raw    (title = "Ing.")
    1
    >>> scope.commit () ### update fails
    Traceback (most recent call last):
       ...
    Readonly_DB

    >>> scope.PAP.Person.query ().all ()
     [GTW.OMP.PAP.Person (u'ln', u'fn', u'', u'')]

     Let's change the readonly back to False
    >>> db_man.change_readonly          (False)
    >>> p.set_raw (title = "Ing.")
    1
    >>> scope.commit           ()
    >>> apt.delete_database    (url)
"""

from _GTW.__test__.model import *

Scaffold.Backend_Default_Path ["SQL"] = "'test'"
Scaffold.Backend_Default_Path ["HPS"] = "'test'"

__test__ = Scaffold.create_test_dict (_test_code)
### __END__ GTW.__test__.readonly


