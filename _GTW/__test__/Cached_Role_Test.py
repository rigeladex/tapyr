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
#    GTW.__test__.Cached_Role_Test
#
# Purpose
#    Test cases for cached role behavior.
#
# Revision Dates
#    21-Apr-2010 (MG) Creation
#    ««revision-date»»···
#--

_test_code = """
    >>> scope = Scope (%s) # doctest:+ELLIPSIS
    Creating new scope MOMT__... in memory
    >>> PAP      = scope.PAP
    >>> person   = PAP.Person  (u"Test", u"Person")
    >>> address1 = PAP.Address (u"Street 1", u"Zip", u"City", u"Country")
    >>> address2 = PAP.Address (u"Street 2", u"Zip", u"City", u"Country")
    >>> sorted (person.addresses)
    []
    >>> link = PAP.Person_has_Address (person, address1)
    >>> sorted (person.addresses)
    [GTW.OMP.PAP.Address (u'street 1', u'zip', u'city', u'country', u'')]
    >>> sorted (PAP.Person_has_Address.query ().all ())
    [GTW.OMP.PAP.Person_has_Address ((u'test', u'person', u'', u''), (u'street 1', u'zip', u'city', u'country', u''))]
    >>> link.set (address = address2)
    1
    >>> sorted (person.addresses)
    [GTW.OMP.PAP.Address (u'street 2', u'zip', u'city', u'country', u'')]
    >>> link
    GTW.OMP.PAP.Person_has_Address ((u'test', u'person', u'', u''), (u'street 2', u'zip', u'city', u'country', u''))
    >>> sorted (PAP.Person_has_Address.query ().all ())
    [GTW.OMP.PAP.Person_has_Address ((u'test', u'person', u'', u''), (u'street 2', u'zip', u'city', u'country', u''))]
"""

from _GTW.__test__.model import MOM, GTW, Scope

__test__ = dict \
    ( HPS = _test_code % ("", )
    , SAS = _test_code % ("'sqlite://'", )
    )
### __END__ GTW.__test__.Cached_Role_Test


