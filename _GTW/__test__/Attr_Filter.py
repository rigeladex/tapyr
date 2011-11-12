# -*- coding: iso-8859-15 -*-
# Copyright (C) 2011 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# #*** <License> ************************************************************#
# This module is part of the package GTW.__test__.
#
# This module is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This module is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this module. If not, see <http://www.gnu.org/licenses/>.
# #*** </License> ***********************************************************#
#
#++
# Name
#    GTW.__test__.Attr_Filter
#
# Purpose
#    Test cases for MOM.Attr.Filter
#
# Revision Dates
#    11-Nov-2011 (CT) Creation
#    ««revision-date»»···
#--

from   __future__  import unicode_literals

_test_code = """
    >>> scope = Scaffold.scope (%(p1)s, %(n1)s) # doctest:+ELLIPSIS
    Creating new scope MOMT__...
    >>> PAP = scope.PAP

    >>> person_attrs = MOM.Attr.Selector.all (PAP.Person.E_Type)
    >>> person_attrs.names
    ('last_name', 'first_name', 'middle_name', 'title', 'lifetime', 'salutation', 'sex')

    >>> for attr in person_attrs :
    ...     print attr.typ, attr.Q
    String <last_name.Q [Attr.Filter.Filter_String_FL]>
    String <first_name.Q [Attr.Filter.Filter_String_FL]>
    String <middle_name.Q [Attr.Filter.String]>
    String <title.Q [Attr.Filter.String]>
    Date_Interval <lifetime.Q [Attr.Filter.Composite]>
    String <salutation.Q [Attr.Filter.String]>
    Sex <sex.Q [Attr.Filter.Ckd]>

    >>> for attr in person_attrs :
    ...     print attr.typ, attr.Q.AC
    String <Attr.Auto_Complete_PN last_name.STARTSWITH [auto-complete]>
    String <Attr.Auto_Complete_PN first_name.STARTSWITH [auto-complete]>
    String <Attr.Auto_Complete_S middle_name.STARTSWITH [auto-complete]>
    String <Attr.Auto_Complete_S title.STARTSWITH [auto-complete]>
    Date_Interval <Attr.Composite_Auto_Complete lifetime.EQ [auto-complete]>
    String <Attr.Auto_Complete_S salutation.STARTSWITH [auto-complete]>
    Sex <Attr.Auto_Complete sex.EQ [auto-complete]>

    >>> for attr in person_attrs :
    ...     print attr.typ, attr.Q.GE
    String <Attr.Greater_Equal last_name.GE [>=]>
    String <Attr.Greater_Equal first_name.GE [>=]>
    String <Attr.Greater_Equal middle_name.GE [>=]>
    String <Attr.Greater_Equal title.GE [>=]>
    Date_Interval <Attr.Composite_Greater_Equal lifetime.GE [>=]>
    String <Attr.Greater_Equal salutation.GE [>=]>
    Sex <Attr.Greater_Equal sex.GE [>=]>

    >>> for attr in person_attrs :
    ...     print attr.typ, getattr (attr.Q, "CONTAINS", "** CONTAINS undefined **")
    String <Attr.Contains last_name.CONTAINS [contains]>
    String <Attr.Contains first_name.CONTAINS [contains]>
    String <Attr.Contains middle_name.CONTAINS [contains]>
    String <Attr.Contains title.CONTAINS [contains]>
    Date_Interval ** CONTAINS undefined **
    String <Attr.Contains salutation.CONTAINS [contains]>
    Sex ** CONTAINS undefined **

    >>> lifetime_attrs = MOM.Attr.Selector.all (PAP.Person.E_Type.lifetime)
    >>> lifetime_attrs.names
    ('start', 'finish')

    >>> for attr in lifetime_attrs :
    ...     print attr.typ, attr.Q.AC
    Date <Attr.Date_Auto_Complete start.EQ [auto-complete]>
    Date <Attr.Date_Auto_Complete finish.EQ [auto-complete]>

    >>> for attr in lifetime_attrs :
    ...     print attr, getattr (PAP.Person.E_Type.lifetime.Q, attr.name).AC
    Date `start` <Attr.Date_Auto_Complete start.EQ [auto-complete]>
    Date `finish` <Attr.Date_Auto_Complete finish.EQ [auto-complete]>

    >>> scope.destroy ()

"""

from _GTW.__test__.model import *

__test__ = Scaffold.create_test_dict (_test_code)

### __END__ GTW.__test__.Attr_Filter
