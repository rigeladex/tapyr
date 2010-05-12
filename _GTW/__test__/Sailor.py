# -*- coding: iso-8859-1 -*-
# Copyright (C) 2010 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# ****************************************************************************
# This module is part of the package MOM.__test__.
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
#    MOM.__test__.Sailor
#
# Purpose
#    Test SRM.Sailor creation and querying
#
# Revision Dates
#    27-Apr-2010 (CT) Creation
#    ««revision-date»»···
#--

_test_code = """
    >>> scope = Scaffold.scope (%s, %s) # doctest:+ELLIPSIS
    Creating new scope MOMT__...
    >>> PAP = scope.PAP
    >>> SRM = scope.SRM
    >>> p = PAP.Person.instance_or_new ("Tanzer", "Christian")
    >>> s = SRM.Sailor.instance_or_new (p.epk_raw, nation = "AUT", mna_number = "29676", raw = True) ### 1
    >>> s
    GTW.OMP.SRM.Sailor ((u'tanzer', u'christian', u'', u''), u'AUT', u'29676')
    >>> SRM.Sailor.instance (p.epk_raw, nation = "AUT", mna_number = "29676", raw = True)
    GTW.OMP.SRM.Sailor ((u'tanzer', u'christian', u'', u''), u'AUT', u'29676')
    >>> SRM.Sailor.instance_or_new (p.epk_raw, nation = "AUT", mna_number = "29676", raw = True)
    GTW.OMP.SRM.Sailor ((u'tanzer', u'christian', u'', u''), u'AUT', u'29676')
    >>> SRM.Sailor.instance_or_new (p.epk_raw, s.nation, s.mna_number)
    GTW.OMP.SRM.Sailor ((u'tanzer', u'christian', u'', u''), u'AUT', u'29676')

"""

from _GTW.__test__.model import *

__test__ = Scaffold.create_test_dict (_test_code)

### __END__ MOM.__test__.Sailor
