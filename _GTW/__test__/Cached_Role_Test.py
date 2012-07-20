# -*- coding: iso-8859-15 -*-
# Copyright (C) 2010-2012 Martin Glueck All rights reserved
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
#    GTW.__test__.Cached_Role_Test
#
# Purpose
#    Test cases for cached role behavior.
#
# Revision Dates
#    21-Apr-2010 (MG) Creation
#    20-Jul-2012 (RS) Add several left-sides (more than one `PAP.Person`)
#    ««revision-date»»···
#--

_test_code = """
    >>> scope = Scaffold.scope (%(p1)s, %(n1)s) # doctest:+ELLIPSIS
    Creating new scope MOMT__...
    >>> PAP      = scope.PAP
    >>> person   = PAP.Person  (u"Test", u"Person")
    >>> person2  = PAP.Person  (u"Another", u"Person")
    >>> address1 = PAP.Address (u"Street 1", u"Zip", u"City", u"Country")
    >>> address2 = PAP.Address (u"Street 2", u"Zip", u"City", u"Country")
    >>> email1   = PAP.Email   (u"person@example.com")
    >>> email2   = PAP.Email   (u"person2@example.com")
    >>> elink1   = PAP.Person_has_Email (person, email1)
    >>> elink2   = PAP.Person_has_Email (person2, email2)
    >>> sorted (person.addresses) #1
    []
    >>> link = PAP.Person_has_Address (person, address1)
    >>> sorted (person.addresses) #2
    [GTW.OMP.PAP.Address (u'street 1', u'zip', u'city', u'country')]
    >>> sorted (PAP.Person_has_Address.query ().all ())
    [GTW.OMP.PAP.Person_has_Address ((u'test', u'person', u'', u''), (u'street 1', u'zip', u'city', u'country'))]
    >>> link.set (address = address2)
    1
    >>> sorted (person.addresses) #3
    [GTW.OMP.PAP.Address (u'street 2', u'zip', u'city', u'country')]
    >>> link
    GTW.OMP.PAP.Person_has_Address ((u'test', u'person', u'', u''), (u'street 2', u'zip', u'city', u'country'))
    >>> sorted (PAP.Person_has_Address.query ().all ())
    [GTW.OMP.PAP.Person_has_Address ((u'test', u'person', u'', u''), (u'street 2', u'zip', u'city', u'country'))]
    >>> link.set_raw (right = address1.epk_raw)
    1
    >>> [e.address for e in person.emails]
    [u'person@example.com']
    >>> [e.address for e in person2.emails]
    [u'person2@example.com']
"""

from _GTW.__test__.model import *

__test__ = Scaffold.create_test_dict (_test_code)

### __END__ GTW.__test__.Cached_Role_Test
