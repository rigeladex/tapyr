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
#     2-Dec-2011 (CT) Creation continued...
#    13-Dec-2011 (CT) Creation continued.... (`.Atoms`)
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
    String <last_name.Q [Attr.Type.Querier String_FL]>
    String <first_name.Q [Attr.Type.Querier String_FL]>
    String <middle_name.Q [Attr.Type.Querier String]>
    String <title.Q [Attr.Type.Querier String]>
    Date_Interval <lifetime.Q [Attr.Type.Querier Composite]>
    String <salutation.Q [Attr.Type.Querier String]>
    Sex <sex.Q [Attr.Type.Querier Ckd]>

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
    ...     print attr.typ, attr.Q
    Date <start.Q [Attr.Type.Querier Date]>
    Date <finish.Q [Attr.Type.Querier Date]>

    >>> for attr in lifetime_attrs :
    ...     print attr.typ, getattr (PAP.Person.E_Type.AQ.lifetime, attr.name)
    Date <lifetime.start.Q [Attr.Type.Querier Date]>
    Date <lifetime.finish.Q [Attr.Type.Querier Date]>

    >>> for attr in lifetime_attrs :
    ...     print attr, getattr (PAP.Person.E_Type.lifetime.Q, attr.name)
    Date `start` <lifetime.start.Q [Attr.Type.Querier Date]>
    Date `finish` <lifetime.finish.Q [Attr.Type.Querier Date]>

    >>> for attr in person_attrs :
    ...     print attr.typ, attr.Q.__class__
    String <Attr.Type.Querier String_FL ('CONTAINS', 'ENDSWITH', 'EQ', 'GE', 'GT', 'LE', 'LT', 'NE', 'STARTSWITH')>
    String <Attr.Type.Querier String_FL ('CONTAINS', 'ENDSWITH', 'EQ', 'GE', 'GT', 'LE', 'LT', 'NE', 'STARTSWITH')>
    String <Attr.Type.Querier String ('CONTAINS', 'ENDSWITH', 'EQ', 'GE', 'GT', 'LE', 'LT', 'NE', 'STARTSWITH')>
    String <Attr.Type.Querier String ('CONTAINS', 'ENDSWITH', 'EQ', 'GE', 'GT', 'LE', 'LT', 'NE', 'STARTSWITH')>
    Date_Interval <Attr.Type.Querier Composite ()>
    String <Attr.Type.Querier String ('CONTAINS', 'ENDSWITH', 'EQ', 'GE', 'GT', 'LE', 'LT', 'NE', 'STARTSWITH')>
    Sex <Attr.Type.Querier Ckd ('EQ', 'GE', 'GT', 'LE', 'LT', 'NE')>
    >>> for attr in php_attrs :
    ...     print attr.typ, attr.Q.__class__
    Person <Attr.Type.Querier Id_Entity ('EQ', 'NE')>
    Phone <Attr.Type.Querier Id_Entity ('EQ', 'NE')>
    Numeric_String <Attr.Type.Querier String ('CONTAINS', 'ENDSWITH', 'EQ', 'GE', 'GT', 'LE', 'LT', 'NE', 'STARTSWITH')>
    String <Attr.Type.Querier String ('CONTAINS', 'ENDSWITH', 'EQ', 'GE', 'GT', 'LE', 'LT', 'NE', 'STARTSWITH')>
    >>> for attr in lifetime_attrs :
    ...     print attr.typ, attr.Q.__class__
    Date <Attr.Type.Querier Date ('EQ', 'GE', 'GT', 'LE', 'LT', 'NE')>
    Date <Attr.Type.Querier Date ('EQ', 'GE', 'GT', 'LE', 'LT', 'NE')>

    >>> print PAP.Person_has_Phone.E_Type.person.Q
    <left.Q [Attr.Type.Querier Id_Entity]>
    >>> print PAP.Person_has_Phone.E_Type.person.Q.lifetime
    <left.lifetime.Q [Attr.Type.Querier Composite]>
    >>> print PAP.Person_has_Phone.E_Type.person.Q.lifetime.start
    <left.lifetime.start.Q [Attr.Type.Querier Date]>

    >>> print PAP.Person_has_Phone.E_Type.AQ.person
    <left.Q [Attr.Type.Querier Id_Entity]>
    >>> print PAP.Person_has_Phone.E_Type.AQ.person.lifetime
    <left.lifetime.Q [Attr.Type.Querier Composite]>
    >>> print PAP.Person_has_Phone.E_Type.AQ.person.lifetime.start
    <left.lifetime.start.Q [Attr.Type.Querier Date]>

    >>> def show_Q (a, level = 0) :
    ...     print "%%s%%-20s%%s" %% ("  " * level, a._attr_name, a.Sig_Key)
    ...     for c in a.Children :
    ...         show_Q (c, level + 1)
    >>> for pka in PAP.Person_has_Phone.E_Type.primary :
    ...     show_Q (pka.Q)
    left                2
      last_name           3
      first_name          3
      middle_name         3
      title               3
    right               2
      country_code        3
      area_code           3
      number              3
    extension           3

    >>> for pka in MOM.Attr.Selector.all (scope.SRM.Boat_in_Regatta.E_Type) :
    ...     show_Q (pka.Q)
    left                2
      left                2
        name                3
      nation              0
      __raw_sail_number   3
      sail_number_x       3
    right               2
      left                2
        name                3
        date                None
          start               0
          finish              0
    skipper             2
      left                2
        last_name           3
        first_name          3
        middle_name         3
        title               3
      nation              0
      mna_number          3
      club                2
        name                3
    place               0
    points              0

    >>> def show_QA (a) :
    ...     print repr (a._attr)
    ...     for c in a.Atoms :
    ...         print "   ", repr (c._attr), c._full_name
    >>> def show_QUA (a) :
    ...     print repr (a._attr), "unwrapped"
    ...     for c in a.Unwrapped_Atoms :
    ...         print "   ", repr (c._attr), c._full_name
    >>> for pka in MOM.Attr.Selector.all (scope.SRM.Boat_in_Regatta.E_Type) :
    ...     show_QA (pka.Q)
    ...     show_QUA (pka.Q)
    Boat `left`
        String `name` left.left.name
        Nation `nation` left.nation
        Int `sail_number` left.sail_number
        String `sail_number_x` left.sail_number_x
    Boat `left` unwrapped
        String `name` left.name
        Nation `nation` nation
        Int `sail_number` sail_number
        String `sail_number_x` sail_number_x
    Regatta `right`
        String `name` right.left.name
        Date `start` right.left.date.start
        Date `finish` right.left.date.finish
    Regatta `right` unwrapped
        String `name` left.name
        Date `start` left.date.start
        Date `finish` left.date.finish
    Entity `skipper`
        String `last_name` skipper.left.last_name
        String `first_name` skipper.left.first_name
        String `middle_name` skipper.left.middle_name
        String `title` skipper.left.title
        Nation `nation` skipper.nation
        String `mna_number` skipper.mna_number
        String `name` skipper.club.name
    Entity `skipper` unwrapped
        String `last_name` left.last_name
        String `first_name` left.first_name
        String `middle_name` left.middle_name
        String `title` left.title
        Nation `nation` nation
        String `mna_number` mna_number
        String `name` club.name
    Int `place`
        Int `place` place
    Int `place` unwrapped
        Int `place` place
    Int `points`
        Int `points` points
    Int `points` unwrapped
        Int `points` points

    >>> seen = set ()
    >>> for at in sorted (scope.attribute_types, key = TFL.Getter.typ) :
    ...     k = at.typ, at.needs_raw_value
    ...     if k not in seen :
    ...         print at.typ, at.Q.__class__, at.Q.Sig_Key
    ...         seen.add (k)
    Account <Attr.Type.Querier Id_Entity ('EQ', 'NE')> 2
    Address <Attr.Type.Querier Id_Entity ('EQ', 'NE')> 2
    Boat <Attr.Type.Querier Id_Entity ('EQ', 'NE')> 2
    Boat_Class <Attr.Type.Querier Id_Entity ('EQ', 'NE')> 2
    Boat_in_Regatta <Attr.Type.Querier Id_Entity ('EQ', 'NE')> 2
    Boolean <Attr.Type.Querier Boolean ('EQ',)> 1
    Date <Attr.Type.Querier Date ('EQ', 'GE', 'GT', 'LE', 'LT', 'NE')> 0
    Date-Slug <Attr.Type.Querier String ('CONTAINS', 'ENDSWITH', 'EQ', 'GE', 'GT', 'LE', 'LT', 'NE', 'STARTSWITH')> 3
    Date-Time <Attr.Type.Querier Ckd ('EQ', 'GE', 'GT', 'LE', 'LT', 'NE')> 0
    Date_Interval <Attr.Type.Querier Composite ()> None
    Date_List <Attr.Type.Querier Ckd ('EQ', 'GE', 'GT', 'LE', 'LT', 'NE')> 0
    Directory <Attr.Type.Querier String ('CONTAINS', 'ENDSWITH', 'EQ', 'GE', 'GT', 'LE', 'LT', 'NE', 'STARTSWITH')> 3
    Email <Attr.Type.Querier Id_Entity ('EQ', 'NE')> 2
    Email <Attr.Type.Querier String ('CONTAINS', 'ENDSWITH', 'EQ', 'GE', 'GT', 'LE', 'LT', 'NE', 'STARTSWITH')> 3
    Entity <Attr.Type.Querier Id_Entity ('EQ', 'NE')> 2
    Event <Attr.Type.Querier Id_Entity ('EQ', 'NE')> 2
    Float <Attr.Type.Querier Ckd ('EQ', 'GE', 'GT', 'LE', 'LT', 'NE')> 0
    Format <Attr.Type.Querier Ckd ('EQ', 'GE', 'GT', 'LE', 'LT', 'NE')> 0
    Gallery <Attr.Type.Querier Id_Entity ('EQ', 'NE')> 2
    Group <Attr.Type.Querier Id_Entity ('EQ', 'NE')> 2
    Id_Entity <Attr.Type.Querier Id_Entity ('EQ', 'NE')> 2
    Int <Attr.Type.Querier Ckd ('EQ', 'GE', 'GT', 'LE', 'LT', 'NE')> 0
    Int <Attr.Type.Querier Raw ('CONTAINS', 'ENDSWITH', 'EQ', 'GE', 'GT', 'LE', 'LT', 'NE', 'STARTSWITH')> 3
    Int_List <Attr.Type.Querier Ckd ('EQ', 'GE', 'GT', 'LE', 'LT', 'NE')> 0
    Name <Attr.Type.Querier String ('CONTAINS', 'ENDSWITH', 'EQ', 'GE', 'GT', 'LE', 'LT', 'NE', 'STARTSWITH')> 3
    Nation <Attr.Type.Querier Ckd ('EQ', 'GE', 'GT', 'LE', 'LT', 'NE')> 0
    Numeric_String <Attr.Type.Querier String ('CONTAINS', 'ENDSWITH', 'EQ', 'GE', 'GT', 'LE', 'LT', 'NE', 'STARTSWITH')> 3
    Object_PN <Attr.Type.Querier Id_Entity ('EQ', 'NE')> 2
    Page <Attr.Type.Querier Id_Entity ('EQ', 'NE')> 2
    Person <Attr.Type.Querier Id_Entity ('EQ', 'NE')> 2
    Phone <Attr.Type.Querier Id_Entity ('EQ', 'NE')> 2
    Picture <Attr.Type.Querier Composite ()> None
    Position <Attr.Type.Querier Composite ()> None
    Recurrence_Spec <Attr.Type.Querier Id_Entity ('EQ', 'NE')> 2
    Regatta <Attr.Type.Querier Id_Entity ('EQ', 'NE')> 2
    Regatta_C <Attr.Type.Querier Id_Entity ('EQ', 'NE')> 2
    Regatta_Event <Attr.Type.Querier Id_Entity ('EQ', 'NE')> 2
    Regatta_Result <Attr.Type.Querier Composite ()> None
    Sailor <Attr.Type.Querier Id_Entity ('EQ', 'NE')> 2
    Sex <Attr.Type.Querier Ckd ('EQ', 'GE', 'GT', 'LE', 'LT', 'NE')> 0
    String <Attr.Type.Querier String ('CONTAINS', 'ENDSWITH', 'EQ', 'GE', 'GT', 'LE', 'LT', 'NE', 'STARTSWITH')> 3
    String <Attr.Type.Querier String ('CONTAINS', 'ENDSWITH', 'EQ', 'GE', 'GT', 'LE', 'LT', 'NE', 'STARTSWITH')> 3
    Team <Attr.Type.Querier Id_Entity ('EQ', 'NE')> 2
    Text <Attr.Type.Querier String ('CONTAINS', 'ENDSWITH', 'EQ', 'GE', 'GT', 'LE', 'LT', 'NE', 'STARTSWITH')> 3
    Thumbnail <Attr.Type.Querier Composite ()> None
    Time <Attr.Type.Querier Ckd ('EQ', 'GE', 'GT', 'LE', 'LT', 'NE')> 0
    Time_Interval <Attr.Type.Querier Composite ()> None
    Unit <Attr.Type.Querier Ckd ('EQ', 'GE', 'GT', 'LE', 'LT', 'NE')> 0
    Url <Attr.Type.Querier String ('CONTAINS', 'ENDSWITH', 'EQ', 'GE', 'GT', 'LE', 'LT', 'NE', 'STARTSWITH')> 3
    Weekday_RR_List <Attr.Type.Querier Ckd ('EQ', 'GE', 'GT', 'LE', 'LT', 'NE')> 0
    X <Attr.Type.Querier Ckd ('EQ', 'GE', 'GT', 'LE', 'LT', 'NE')> 0
    Y <Attr.Type.Querier Ckd ('EQ', 'GE', 'GT', 'LE', 'LT', 'NE')> 0

    >>> for sig, Sig_Key in sorted (at.Q.Signatures.iteritems (), key = TFL.Getter [1]) :
    ...     print Sig_Key, sig
    0 ('EQ', 'GE', 'GT', 'LE', 'LT', 'NE')
    1 ('EQ',)
    2 ('EQ', 'NE')
    3 ('CONTAINS', 'ENDSWITH', 'EQ', 'GE', 'GT', 'LE', 'LT', 'NE', 'STARTSWITH')

    >>> for k, v in sorted (at.Q.Base_Op_Table.iteritems ()) :
    ...     print "%%-12s %%s" %% (k, v)
    CONTAINS     <Attr.Filter CONTAINS [contains]>
    ENDSWITH     <Attr.Filter ENDSWITH [ends-with]>
    EQ           <Attr.Filter EQ [==]>
    GE           <Attr.Filter GE [>=]>
    GT           <Attr.Filter GT [>]>
    LE           <Attr.Filter LE [<=]>
    LT           <Attr.Filter LT [<]>
    NE           <Attr.Filter NE [!=]>
    STARTSWITH   <Attr.Filter STARTSWITH [starts-with]>

    >>> scope.destroy ()

"""

from _GTW.__test__.model import *

__test__ = Scaffold.create_test_dict (_test_code)

### __END__ GTW.__test__.Attr_Filter
