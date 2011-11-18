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
#    12-Nov-2011 (CT) Creation continued
#    18-Nov-2011 (CT) Creation continued..
#    ««revision-date»»···
#--

from   __future__  import unicode_literals

_test_code = """
    >>> scope = Scaffold.scope (%(p1)s, %(n1)s) # doctest:+ELLIPSIS
    Creating new scope MOMT__...
    >>> PAP = scope.PAP

    >>> person_attrs   = MOM.Attr.Selector.all (PAP.Person.E_Type)
    >>> php_attrs      = MOM.Attr.Selector.all (PAP.Person_has_Phone.E_Type)
    >>> lifetime_attrs = MOM.Attr.Selector.all (PAP.Person.E_Type.lifetime)

    >>> person_attrs.names
    ('last_name', 'first_name', 'middle_name', 'title', 'lifetime', 'salutation', 'sex')
    >>> php_attrs.names
    ('left', 'right', 'extension', 'desc')
    >>> lifetime_attrs.names
    ('start', 'finish')

    >>> for attr in person_attrs :
    ...     print attr.typ, attr.Q
    String <last_name.Q [Attr.Type.Filter String_FL]>
    String <first_name.Q [Attr.Type.Filter String_FL]>
    String <middle_name.Q [Attr.Type.Filter String]>
    String <title.Q [Attr.Type.Filter String]>
    Date_Interval <lifetime.Q [Attr.Type.Filter Composite]>
    String <salutation.Q [Attr.Type.Filter String]>
    Sex <sex.Q [Attr.Type.Filter Ckd]>

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

    >>> for attr in lifetime_attrs :
    ...     print attr.typ, attr.Q.AC
    Date <Attr.Date_Auto_Complete start.EQ [auto-complete]>
    Date <Attr.Date_Auto_Complete finish.EQ [auto-complete]>

    >>> for attr in lifetime_attrs :
    ...     print attr, getattr (PAP.Person.E_Type.lifetime.Q, attr.name).AC
    Date `start` <Attr.Date_Auto_Complete start.EQ [auto-complete]>
    Date `finish` <Attr.Date_Auto_Complete finish.EQ [auto-complete]>

    >>> for attr in person_attrs :
    ...     print attr.typ, attr.Q.__class__
    String <Attr.Type.Filter String_FL ('CONTAINS', 'ENDSWITH', 'EQ', 'GE', 'GT', 'LE', 'LT', 'NE', 'STARTSWITH')>
    String <Attr.Type.Filter String_FL ('CONTAINS', 'ENDSWITH', 'EQ', 'GE', 'GT', 'LE', 'LT', 'NE', 'STARTSWITH')>
    String <Attr.Type.Filter String ('CONTAINS', 'ENDSWITH', 'EQ', 'GE', 'GT', 'LE', 'LT', 'NE', 'STARTSWITH')>
    String <Attr.Type.Filter String ('CONTAINS', 'ENDSWITH', 'EQ', 'GE', 'GT', 'LE', 'LT', 'NE', 'STARTSWITH')>
    Date_Interval <Attr.Type.Filter Composite ()>
    String <Attr.Type.Filter String ('CONTAINS', 'ENDSWITH', 'EQ', 'GE', 'GT', 'LE', 'LT', 'NE', 'STARTSWITH')>
    Sex <Attr.Type.Filter Ckd ('EQ', 'GE', 'GT', 'LE', 'LT', 'NE')>
    >>> for attr in php_attrs :
    ...     print attr.typ, attr.Q.__class__
    Person <Attr.Type.Filter Id_Entity ()>
    Phone <Attr.Type.Filter Id_Entity ()>
    Numeric_String <Attr.Type.Filter String ('CONTAINS', 'ENDSWITH', 'EQ', 'GE', 'GT', 'LE', 'LT', 'NE', 'STARTSWITH')>
    String <Attr.Type.Filter String ('CONTAINS', 'ENDSWITH', 'EQ', 'GE', 'GT', 'LE', 'LT', 'NE', 'STARTSWITH')>
    >>> for attr in lifetime_attrs :
    ...     print attr.typ, attr.Q.__class__
    Date <Attr.Type.Filter Date ('EQ', 'GE', 'GT', 'LE', 'LT', 'NE')>
    Date <Attr.Type.Filter Date ('EQ', 'GE', 'GT', 'LE', 'LT', 'NE')>

    >>> print PAP.Person_has_Phone.E_Type.person.Q
    <left.Q [Attr.Type.Filter Id_Entity]>
    >>> print PAP.Person_has_Phone.E_Type.person.Q.lifetime
    <lifetime.Q [Attr.Type.Filter Composite]>
    >>> print PAP.Person_has_Phone.E_Type.person.Q.lifetime.start
    <start.Q [Attr.Type.Filter Date]>

    >>> print PAP.Person_has_Phone.E_Type.AQ.person
    <left.Q [Attr.Type.Filter Id_Entity]>
    >>> print PAP.Person_has_Phone.E_Type.AQ.person.lifetime
    <lifetime.Q [Attr.Type.Filter Composite]>
    >>> print PAP.Person_has_Phone.E_Type.AQ.person.lifetime.start
    <start.Q [Attr.Type.Filter Date]>

    >>> seen = set ()
    >>> for at in sorted (scope.attribute_types, key = TFL.Getter.typ) :
    ...     k = at.typ, at.needs_raw_value
    ...     if k not in seen :
    ...         print at.typ, at.Q.__class__
    ...         seen.add (k)
    Account <Attr.Type.Filter Id_Entity ()>
    Address <Attr.Type.Filter Id_Entity ()>
    Boat <Attr.Type.Filter Id_Entity ()>
    Boat_Class <Attr.Type.Filter Id_Entity ()>
    Boat_in_Regatta <Attr.Type.Filter Id_Entity ()>
    Boolean <Attr.Type.Filter Ckd ('EQ', 'GE', 'GT', 'LE', 'LT', 'NE')>
    Date <Attr.Type.Filter Date ('EQ', 'GE', 'GT', 'LE', 'LT', 'NE')>
    Date-Slug <Attr.Type.Filter String ('CONTAINS', 'ENDSWITH', 'EQ', 'GE', 'GT', 'LE', 'LT', 'NE', 'STARTSWITH')>
    Date-Time <Attr.Type.Filter Ckd ('EQ', 'GE', 'GT', 'LE', 'LT', 'NE')>
    Date_Interval <Attr.Type.Filter Composite ()>
    Date_List <Attr.Type.Filter Ckd ('EQ', 'GE', 'GT', 'LE', 'LT', 'NE')>
    Directory <Attr.Type.Filter String ('CONTAINS', 'ENDSWITH', 'EQ', 'GE', 'GT', 'LE', 'LT', 'NE', 'STARTSWITH')>
    Email <Attr.Type.Filter Id_Entity ()>
    Email <Attr.Type.Filter String ('CONTAINS', 'ENDSWITH', 'EQ', 'GE', 'GT', 'LE', 'LT', 'NE', 'STARTSWITH')>
    Entity <Attr.Type.Filter Id_Entity ()>
    Event <Attr.Type.Filter Id_Entity ()>
    Float <Attr.Type.Filter Ckd ('EQ', 'GE', 'GT', 'LE', 'LT', 'NE')>
    Format <Attr.Type.Filter Ckd ('EQ', 'GE', 'GT', 'LE', 'LT', 'NE')>
    Gallery <Attr.Type.Filter Id_Entity ()>
    Group <Attr.Type.Filter Id_Entity ()>
    Id_Entity <Attr.Type.Filter Id_Entity ()>
    Int <Attr.Type.Filter Ckd ('EQ', 'GE', 'GT', 'LE', 'LT', 'NE')>
    Int <Attr.Type.Filter Raw ('CONTAINS', 'ENDSWITH', 'EQ', 'GE', 'GT', 'LE', 'LT', 'NE', 'STARTSWITH')>
    Int_List <Attr.Type.Filter Ckd ('EQ', 'GE', 'GT', 'LE', 'LT', 'NE')>
    Name <Attr.Type.Filter String ('CONTAINS', 'ENDSWITH', 'EQ', 'GE', 'GT', 'LE', 'LT', 'NE', 'STARTSWITH')>
    Nation <Attr.Type.Filter Ckd ('EQ', 'GE', 'GT', 'LE', 'LT', 'NE')>
    Numeric_String <Attr.Type.Filter String ('CONTAINS', 'ENDSWITH', 'EQ', 'GE', 'GT', 'LE', 'LT', 'NE', 'STARTSWITH')>
    Object_PN <Attr.Type.Filter Id_Entity ()>
    Page <Attr.Type.Filter Id_Entity ()>
    Person <Attr.Type.Filter Id_Entity ()>
    Phone <Attr.Type.Filter Id_Entity ()>
    Picture <Attr.Type.Filter Composite ()>
    Position <Attr.Type.Filter Composite ()>
    Recurrence_Spec <Attr.Type.Filter Id_Entity ()>
    Regatta <Attr.Type.Filter Id_Entity ()>
    Regatta_C <Attr.Type.Filter Id_Entity ()>
    Regatta_Event <Attr.Type.Filter Id_Entity ()>
    Regatta_Result <Attr.Type.Filter Composite ()>
    Sailor <Attr.Type.Filter Id_Entity ()>
    Sex <Attr.Type.Filter Ckd ('EQ', 'GE', 'GT', 'LE', 'LT', 'NE')>
    String <Attr.Type.Filter String ('CONTAINS', 'ENDSWITH', 'EQ', 'GE', 'GT', 'LE', 'LT', 'NE', 'STARTSWITH')>
    String <Attr.Type.Filter String ('CONTAINS', 'ENDSWITH', 'EQ', 'GE', 'GT', 'LE', 'LT', 'NE', 'STARTSWITH')>
    Team <Attr.Type.Filter Id_Entity ()>
    Text <Attr.Type.Filter String ('CONTAINS', 'ENDSWITH', 'EQ', 'GE', 'GT', 'LE', 'LT', 'NE', 'STARTSWITH')>
    Thumbnail <Attr.Type.Filter Composite ()>
    Time <Attr.Type.Filter Ckd ('EQ', 'GE', 'GT', 'LE', 'LT', 'NE')>
    Time_Interval <Attr.Type.Filter Composite ()>
    Unit <Attr.Type.Filter Ckd ('EQ', 'GE', 'GT', 'LE', 'LT', 'NE')>
    Url <Attr.Type.Filter String ('CONTAINS', 'ENDSWITH', 'EQ', 'GE', 'GT', 'LE', 'LT', 'NE', 'STARTSWITH')>
    Weekday_RR_List <Attr.Type.Filter Ckd ('EQ', 'GE', 'GT', 'LE', 'LT', 'NE')>
    X <Attr.Type.Filter Ckd ('EQ', 'GE', 'GT', 'LE', 'LT', 'NE')>
    Y <Attr.Type.Filter Ckd ('EQ', 'GE', 'GT', 'LE', 'LT', 'NE')>

    >>> scope.destroy ()

"""

from _GTW.__test__.model import *

__test__ = Scaffold.create_test_dict (_test_code)

### __END__ GTW.__test__.Attr_Filter
