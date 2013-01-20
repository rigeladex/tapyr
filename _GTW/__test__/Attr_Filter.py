# -*- coding: iso-8859-15 -*-
# Copyright (C) 2011-2013 Mag. Christian Tanzer All rights reserved
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
#    19-Mar-2012 (CT) Adapt to reification of `SRM.Handicap`
#    14-May-2012 (CT) Add test showing `P_Type` of `scope.attribute_types`
#    31-Jul-2012 (CT) Add `Angle` to test output
#    11-Oct-2012 (CT) Change duplicate removal for `Sig_Key` test
#     6-Dec-2012 (CT) Remove `Entity_created_by_Person`
#    20-Jan-2013 (CT) Add `AIS`
#    ««revision-date»»···
#--

from   __future__  import unicode_literals

_test_code = """
    >>> scope = Scaffold.scope (%(p1)s, %(n1)s) # doctest:+ELLIPSIS
    Creating new scope MOMT__...
    >>> PAP = scope.PAP

    >>> for aq in PAP.Person.E_Type.AQ.Attrs :
    ...     print aq
    <last_name.AQ [Attr.Type.Querier String_FL]>
    <first_name.AQ [Attr.Type.Querier String_FL]>
    <middle_name.AQ [Attr.Type.Querier String]>
    <title.AQ [Attr.Type.Querier String]>
    <lifetime.AQ [Attr.Type.Querier Composite]>
    <salutation.AQ [Attr.Type.Querier String]>
    <sex.AQ [Attr.Type.Querier Ckd]>

    >>> paq = MOM.Attr.Querier.E_Type (PAP.Person.E_Type, MOM.Attr.Selector.all)
    >>> for aq in paq.Attrs :
    ...     print aq
    <last_name.AQ [Attr.Type.Querier String_FL]>
    <first_name.AQ [Attr.Type.Querier String_FL]>
    <middle_name.AQ [Attr.Type.Querier String]>
    <title.AQ [Attr.Type.Querier String]>
    <lifetime.AQ [Attr.Type.Querier Composite]>
    <salutation.AQ [Attr.Type.Querier String]>
    <sex.AQ [Attr.Type.Querier Ckd]>

    >>> for aq in paq.Attrs_Transitive :
    ...     print aq
    <last_name.AQ [Attr.Type.Querier String_FL]>
    <first_name.AQ [Attr.Type.Querier String_FL]>
    <middle_name.AQ [Attr.Type.Querier String]>
    <title.AQ [Attr.Type.Querier String]>
    <lifetime.AQ [Attr.Type.Querier Composite]>
    <lifetime.start.AQ [Attr.Type.Querier Date]>
    <lifetime.finish.AQ [Attr.Type.Querier Date]>
    <lifetime.alive.AQ [Attr.Type.Querier Boolean]>
    <salutation.AQ [Attr.Type.Querier String]>
    <sex.AQ [Attr.Type.Querier Ckd]>

    >>> for aq in paq.Atoms :
    ...     print aq
    <last_name.AQ [Attr.Type.Querier String_FL]>
    <first_name.AQ [Attr.Type.Querier String_FL]>
    <middle_name.AQ [Attr.Type.Querier String]>
    <title.AQ [Attr.Type.Querier String]>
    <lifetime.start.AQ [Attr.Type.Querier Date]>
    <lifetime.finish.AQ [Attr.Type.Querier Date]>
    <lifetime.alive.AQ [Attr.Type.Querier Boolean]>
    <salutation.AQ [Attr.Type.Querier String]>
    <sex.AQ [Attr.Type.Querier Ckd]>

    >>> for aq in PAP.Person_has_Phone.E_Type.AQ.Atoms :
    ...     print aq
    <left.last_name.AQ [Attr.Type.Querier String_FL]>
    <left.first_name.AQ [Attr.Type.Querier String_FL]>
    <left.middle_name.AQ [Attr.Type.Querier String]>
    <left.title.AQ [Attr.Type.Querier String]>
    <left.lifetime.start.AQ [Attr.Type.Querier Date]>
    <left.lifetime.finish.AQ [Attr.Type.Querier Date]>
    <left.lifetime.alive.AQ [Attr.Type.Querier Boolean]>
    <left.salutation.AQ [Attr.Type.Querier String]>
    <left.sex.AQ [Attr.Type.Querier Ckd]>
    <right.country_code.AQ [Attr.Type.Querier String]>
    <right.area_code.AQ [Attr.Type.Querier String]>
    <right.number.AQ [Attr.Type.Querier String]>
    <right.desc.AQ [Attr.Type.Querier String]>
    <extension.AQ [Attr.Type.Querier String]>
    <desc.AQ [Attr.Type.Querier String]>

    >>> for aq in PAP.Person_has_Phone.E_Type.AQ.left.Atoms :
    ...     print aq
    <left.last_name.AQ [Attr.Type.Querier String_FL]>
    <left.first_name.AQ [Attr.Type.Querier String_FL]>
    <left.middle_name.AQ [Attr.Type.Querier String]>
    <left.title.AQ [Attr.Type.Querier String]>
    <left.lifetime.start.AQ [Attr.Type.Querier Date]>
    <left.lifetime.finish.AQ [Attr.Type.Querier Date]>
    <left.lifetime.alive.AQ [Attr.Type.Querier Boolean]>
    <left.salutation.AQ [Attr.Type.Querier String]>
    <left.sex.AQ [Attr.Type.Querier Ckd]>

    >>> for aq in PAP.Person_has_Phone.E_Type.AQ.left.Unwrapped_Atoms :
    ...     print aq
    <last_name.AQ [Attr.Type.Querier String_FL]>
    <first_name.AQ [Attr.Type.Querier String_FL]>
    <middle_name.AQ [Attr.Type.Querier String]>
    <title.AQ [Attr.Type.Querier String]>
    <lifetime.start.AQ [Attr.Type.Querier Date]>
    <lifetime.finish.AQ [Attr.Type.Querier Date]>
    <salutation.AQ [Attr.Type.Querier String]>
    <sex.AQ [Attr.Type.Querier Ckd]>

    >>> person_attrs   = MOM.Attr.Selector.all (PAP.Person.E_Type)
    >>> php_attrs      = MOM.Attr.Selector.all (PAP.Person_has_Phone.E_Type)
    >>> lifetime_attrs = MOM.Attr.Selector.all (PAP.Person.E_Type.lifetime)

    >>> person_attrs.names
    ('last_name', 'first_name', 'middle_name', 'title', 'lifetime', 'salutation', 'sex')
    >>> php_attrs.names
    ('left', 'right', 'extension', 'desc')
    >>> lifetime_attrs.names
    ('start', 'finish', 'alive')

    >>> for attr in person_attrs :
    ...     print attr.typ, attr.AQ
    String <last_name.AQ [Attr.Type.Querier String_FL]>
    String <first_name.AQ [Attr.Type.Querier String_FL]>
    String <middle_name.AQ [Attr.Type.Querier String]>
    String <title.AQ [Attr.Type.Querier String]>
    Date_Interval <lifetime.AQ [Attr.Type.Querier Composite]>
    String <salutation.AQ [Attr.Type.Querier String]>
    Sex <sex.AQ [Attr.Type.Querier Ckd]>

    >>> for attr in person_attrs :
    ...     print attr.typ, attr.AQ.AC
    String <Attr.Auto_Complete_PN last_name.STARTSWITH [auto-complete]>
    String <Attr.Auto_Complete_PN first_name.STARTSWITH [auto-complete]>
    String <Attr.Auto_Complete_S middle_name.STARTSWITH [auto-complete]>
    String <Attr.Auto_Complete_S title.STARTSWITH [auto-complete]>
    Date_Interval <Attr.Composite_Auto_Complete lifetime.EQ [auto-complete]>
    String <Attr.Auto_Complete_S salutation.STARTSWITH [auto-complete]>
    Sex <Attr.Auto_Complete sex.EQ [auto-complete]>

    >>> for attr in person_attrs :
    ...     print attr.typ, attr.AQ.GE
    String <Attr.Greater_Equal last_name.GE [>=]>
    String <Attr.Greater_Equal first_name.GE [>=]>
    String <Attr.Greater_Equal middle_name.GE [>=]>
    String <Attr.Greater_Equal title.GE [>=]>
    Date_Interval <Attr.Composite_Greater_Equal lifetime.GE [>=]>
    String <Attr.Greater_Equal salutation.GE [>=]>
    Sex <Attr.Greater_Equal sex.GE [>=]>

    >>> for attr in person_attrs :
    ...     print attr.typ, getattr (attr.AQ, "CONTAINS", "** CONTAINS undefined **")
    String <Attr.Contains last_name.CONTAINS [contains]>
    String <Attr.Contains first_name.CONTAINS [contains]>
    String <Attr.Contains middle_name.CONTAINS [contains]>
    String <Attr.Contains title.CONTAINS [contains]>
    Date_Interval ** CONTAINS undefined **
    String <Attr.Contains salutation.CONTAINS [contains]>
    Sex ** CONTAINS undefined **

    >>> for attr in lifetime_attrs :
    ...     print attr.typ, attr.AQ
    Date <start.AQ [Attr.Type.Querier Date]>
    Date <finish.AQ [Attr.Type.Querier Date]>
    Boolean <alive.AQ [Attr.Type.Querier Boolean]>

    >>> for attr in lifetime_attrs :
    ...     print attr.typ, getattr (PAP.Person.E_Type.AQ.lifetime, attr.name)
    Date <lifetime.start.AQ [Attr.Type.Querier Date]>
    Date <lifetime.finish.AQ [Attr.Type.Querier Date]>
    Boolean <lifetime.alive.AQ [Attr.Type.Querier Boolean]>

    >>> for attr in lifetime_attrs :
    ...     print attr, getattr (PAP.Person.E_Type.lifetime.AQ, attr.name)
    Date `start` <lifetime.start.AQ [Attr.Type.Querier Date]>
    Date `finish` <lifetime.finish.AQ [Attr.Type.Querier Date]>
    Boolean `alive` <lifetime.alive.AQ [Attr.Type.Querier Boolean]>

    >>> for attr in person_attrs :
    ...     print attr.typ, attr.AQ.__class__
    String <Attr.Type.Querier String_FL ('CONTAINS', 'ENDSWITH', 'EQ', 'GE', 'GT', 'IN', 'LE', 'LT', 'NE', 'STARTSWITH')>
    String <Attr.Type.Querier String_FL ('CONTAINS', 'ENDSWITH', 'EQ', 'GE', 'GT', 'IN', 'LE', 'LT', 'NE', 'STARTSWITH')>
    String <Attr.Type.Querier String ('CONTAINS', 'ENDSWITH', 'EQ', 'GE', 'GT', 'IN', 'LE', 'LT', 'NE', 'STARTSWITH')>
    String <Attr.Type.Querier String ('CONTAINS', 'ENDSWITH', 'EQ', 'GE', 'GT', 'IN', 'LE', 'LT', 'NE', 'STARTSWITH')>
    Date_Interval <Attr.Type.Querier Composite ()>
    String <Attr.Type.Querier String ('CONTAINS', 'ENDSWITH', 'EQ', 'GE', 'GT', 'IN', 'LE', 'LT', 'NE', 'STARTSWITH')>
    Sex <Attr.Type.Querier Ckd ('EQ', 'GE', 'GT', 'IN', 'LE', 'LT', 'NE')>

    >>> for attr in php_attrs :
    ...     print attr.typ, attr.AQ.__class__
    Person <Attr.Type.Querier Id_Entity ('EQ', 'IN', 'NE')>
    Phone <Attr.Type.Querier Id_Entity ('EQ', 'IN', 'NE')>
    Numeric_String <Attr.Type.Querier String ('CONTAINS', 'ENDSWITH', 'EQ', 'GE', 'GT', 'IN', 'LE', 'LT', 'NE', 'STARTSWITH')>
    String <Attr.Type.Querier String ('CONTAINS', 'ENDSWITH', 'EQ', 'GE', 'GT', 'IN', 'LE', 'LT', 'NE', 'STARTSWITH')>

    >>> for attr in lifetime_attrs :
    ...     print attr.typ, attr.AQ.__class__
    Date <Attr.Type.Querier Date ('EQ', 'GE', 'GT', 'IN', 'LE', 'LT', 'NE')>
    Date <Attr.Type.Querier Date ('EQ', 'GE', 'GT', 'IN', 'LE', 'LT', 'NE')>
    Boolean <Attr.Type.Querier Boolean ('EQ',)>

    >>> print PAP.Person_has_Phone.E_Type.person.AQ
    <left.AQ [Attr.Type.Querier Id_Entity]>
    >>> print PAP.Person_has_Phone.E_Type.person.AQ.lifetime
    <left.lifetime.AQ [Attr.Type.Querier Composite]>
    >>> print PAP.Person_has_Phone.E_Type.person.AQ.lifetime.start
    <left.lifetime.start.AQ [Attr.Type.Querier Date]>

    >>> print PAP.Person_has_Phone.E_Type.AQ.person
    <left.AQ [Attr.Type.Querier Id_Entity]>
    >>> print PAP.Person_has_Phone.E_Type.AQ.person.lifetime
    <left.lifetime.AQ [Attr.Type.Querier Composite]>
    >>> print PAP.Person_has_Phone.E_Type.AQ.person.lifetime.start
    <left.lifetime.start.AQ [Attr.Type.Querier Date]>

    >>> def show_Q (a, level = 0) :
    ...     print "%%s%%-20s%%s" %% ("  " * level, a._attr_name, a.Sig_Key)
    ...     for c in a.Attrs :
    ...         show_Q (c, level + 1)
    >>> AQ = PAP.Person_has_Phone.AQ
    >>> for pka in PAP.Person_has_Phone.E_Type.primary :
    ...     show_Q (getattr (AQ, pka.name))
    left                2
      last_name           3
      first_name          3
      middle_name         3
      title               3
      lifetime            None
        start               0
        finish              0
        alive               1
      salutation          3
      sex                 0
    right               2
      country_code        3
      area_code           3
      number              3
      desc                3
    extension           3

    >>> for pka in scope.SRM.Boat_in_Regatta.E_Type.AQ.Attrs :
    ...     show_Q (pka)
    left                2
      left                2
        name                3
        max_crew            0
        beam                0
        loa                 0
        sail_area           0
      nation              0
      __raw_sail_number   3
      sail_number_x       3
      name                3
    right               2
      left                2
        name                3
        date                None
          start               0
          finish              0
          alive               1
        club                2
          name                3
          long_name           3
        desc                3
        is_cancelled        1
      boat_class          2
        name                3
      discards            0
      is_cancelled        1
      kind                3
      races               0
      result              None
        date                0
        software            3
        status              3
    skipper             2
      left                2
        last_name           3
        first_name          3
        middle_name         3
        title               3
        lifetime            None
          start               0
          finish              0
          alive               1
        salutation          3
        sex                 0
      nation              0
      __raw_mna_number    3
      club                2
        name                3
        long_name           3
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
    >>> for pka in scope.SRM.Boat_in_Regatta.E_Type.AQ.Attrs :
    ...     show_QA (pka)
    ...     show_QUA (pka)
    Boat `left`
        String `name` left.left.name
        Int `max_crew` left.left.max_crew
        Float `beam` left.left.beam
        Float `loa` left.left.loa
        Float `sail_area` left.left.sail_area
        Nation `nation` left.nation
        Int `sail_number` left.sail_number
        String `sail_number_x` left.sail_number_x
        String `name` left.name
    Boat `left` unwrapped
        String `name` left.name
        Nation `nation` nation
        Int `sail_number` sail_number
        String `sail_number_x` sail_number_x
        String `name` name
    Regatta `right`
        String `name` right.left.name
        Date `start` right.left.date.start
        Date `finish` right.left.date.finish
        Boolean `alive` right.left.date.alive
        String `name` right.left.club.name
        String `long_name` right.left.club.long_name
        String `desc` right.left.desc
        Boolean `is_cancelled` right.left.is_cancelled
        String `name` right.boat_class.name
        Int `discards` right.discards
        Boolean `is_cancelled` right.is_cancelled
        String `kind` right.kind
        Int `races` right.races
        Date-Time `date` right.result.date
        String `software` right.result.software
        String `status` right.result.status
    Regatta `right` unwrapped
        String `name` left.name
        Date `start` left.date.start
        Date `finish` left.date.finish
        String `name` boat_class.name
        Int `discards` discards
        Boolean `is_cancelled` is_cancelled
        String `kind` kind
        Int `races` races
        Date-Time `date` result.date
        String `software` result.software
        String `status` result.status
    Entity `skipper`
        String `last_name` skipper.left.last_name
        String `first_name` skipper.left.first_name
        String `middle_name` skipper.left.middle_name
        String `title` skipper.left.title
        Date `start` skipper.left.lifetime.start
        Date `finish` skipper.left.lifetime.finish
        Boolean `alive` skipper.left.lifetime.alive
        String `salutation` skipper.left.salutation
        Sex `sex` skipper.left.sex
        Nation `nation` skipper.nation
        Int `mna_number` skipper.mna_number
        String `name` skipper.club.name
        String `long_name` skipper.club.long_name
    Entity `skipper` unwrapped
        String `last_name` left.last_name
        String `first_name` left.first_name
        String `middle_name` left.middle_name
        String `title` left.title
        Nation `nation` nation
        Int `mna_number` mna_number
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
    ...     msg = "%%s %%s %%s" %% (at.typ, at.AQ.__class__, at.AQ.Sig_Key)
    ...     if msg not in seen :
    ...         print msg
    ...         seen.add (msg)
    AIS <Attr.Type.Querier Ckd ('EQ', 'GE', 'GT', 'IN', 'LE', 'LT', 'NE')> 0
    Account <Attr.Type.Querier Id_Entity ('EQ', 'IN', 'NE')> 2
    Address <Attr.Type.Querier Id_Entity ('EQ', 'IN', 'NE')> 2
    Angle <Attr.Type.Querier Raw ('CONTAINS', 'ENDSWITH', 'EQ', 'GE', 'GT', 'IN', 'LE', 'LT', 'NE', 'STARTSWITH')> 3
    Boat <Attr.Type.Querier Id_Entity ('EQ', 'IN', 'NE')> 2
    Boat_Class <Attr.Type.Querier Id_Entity ('EQ', 'IN', 'NE')> 2
    Boat_in_Regatta <Attr.Type.Querier Id_Entity ('EQ', 'IN', 'NE')> 2
    Boolean <Attr.Type.Querier Boolean ('EQ',)> 1
    Company <Attr.Type.Querier Id_Entity ('EQ', 'IN', 'NE')> 2
    Date <Attr.Type.Querier Date ('EQ', 'GE', 'GT', 'IN', 'LE', 'LT', 'NE')> 0
    Date-Slug <Attr.Type.Querier String ('CONTAINS', 'ENDSWITH', 'EQ', 'GE', 'GT', 'IN', 'LE', 'LT', 'NE', 'STARTSWITH')> 3
    Date-Time <Attr.Type.Querier Ckd ('EQ', 'GE', 'GT', 'IN', 'LE', 'LT', 'NE')> 0
    Date_Interval <Attr.Type.Querier Composite ()> None
    Date_List <Attr.Type.Querier Ckd ('EQ', 'GE', 'GT', 'IN', 'LE', 'LT', 'NE')> 0
    Date_Time_Interval <Attr.Type.Querier Composite ()> None
    Directory <Attr.Type.Querier String ('CONTAINS', 'ENDSWITH', 'EQ', 'GE', 'GT', 'IN', 'LE', 'LT', 'NE', 'STARTSWITH')> 3
    Email <Attr.Type.Querier Id_Entity ('EQ', 'IN', 'NE')> 2
    Email <Attr.Type.Querier String ('CONTAINS', 'ENDSWITH', 'EQ', 'GE', 'GT', 'IN', 'LE', 'LT', 'NE', 'STARTSWITH')> 3
    Entity <Attr.Type.Querier Id_Entity ('EQ', 'IN', 'NE')> 2
    Event <Attr.Type.Querier Id_Entity ('EQ', 'IN', 'NE')> 2
    Float <Attr.Type.Querier Ckd ('EQ', 'GE', 'GT', 'IN', 'LE', 'LT', 'NE')> 0
    Format <Attr.Type.Querier Ckd ('EQ', 'GE', 'GT', 'IN', 'LE', 'LT', 'NE')> 0
    Gallery <Attr.Type.Querier Id_Entity ('EQ', 'IN', 'NE')> 2
    Group <Attr.Type.Querier Id_Entity ('EQ', 'IN', 'NE')> 2
    Int <Attr.Type.Querier Ckd ('EQ', 'GE', 'GT', 'IN', 'LE', 'LT', 'NE')> 0
    Int <Attr.Type.Querier Raw ('CONTAINS', 'ENDSWITH', 'EQ', 'GE', 'GT', 'IN', 'LE', 'LT', 'NE', 'STARTSWITH')> 3
    Int_List <Attr.Type.Querier Ckd ('EQ', 'GE', 'GT', 'IN', 'LE', 'LT', 'NE')> 0
    Name <Attr.Type.Querier String ('CONTAINS', 'ENDSWITH', 'EQ', 'GE', 'GT', 'IN', 'LE', 'LT', 'NE', 'STARTSWITH')> 3
    Nation <Attr.Type.Querier Ckd ('EQ', 'GE', 'GT', 'IN', 'LE', 'LT', 'NE')> 0
    Numeric_String <Attr.Type.Querier String ('CONTAINS', 'ENDSWITH', 'EQ', 'GE', 'GT', 'IN', 'LE', 'LT', 'NE', 'STARTSWITH')> 3
    Object_PN <Attr.Type.Querier Id_Entity ('EQ', 'IN', 'NE')> 2
    Page <Attr.Type.Querier Id_Entity ('EQ', 'IN', 'NE')> 2
    Person <Attr.Type.Querier Id_Entity ('EQ', 'IN', 'NE')> 2
    Phone <Attr.Type.Querier Id_Entity ('EQ', 'IN', 'NE')> 2
    Picture <Attr.Type.Querier Composite ()> None
    Position <Attr.Type.Querier Composite ()> None
    Recurrence_Spec <Attr.Type.Querier Id_Entity ('EQ', 'IN', 'NE')> 2
    Regatta <Attr.Type.Querier Id_Entity ('EQ', 'IN', 'NE')> 2
    Regatta_C <Attr.Type.Querier Id_Entity ('EQ', 'IN', 'NE')> 2
    Regatta_Event <Attr.Type.Querier Id_Entity ('EQ', 'IN', 'NE')> 2
    Regatta_Result <Attr.Type.Querier Composite ()> None
    Sailor <Attr.Type.Querier Id_Entity ('EQ', 'IN', 'NE')> 2
    Sex <Attr.Type.Querier Ckd ('EQ', 'GE', 'GT', 'IN', 'LE', 'LT', 'NE')> 0
    String <Attr.Type.Querier String ('CONTAINS', 'ENDSWITH', 'EQ', 'GE', 'GT', 'IN', 'LE', 'LT', 'NE', 'STARTSWITH')> 3
    String <Attr.Type.Querier String_FL ('CONTAINS', 'ENDSWITH', 'EQ', 'GE', 'GT', 'IN', 'LE', 'LT', 'NE', 'STARTSWITH')> 3
    Team <Attr.Type.Querier Id_Entity ('EQ', 'IN', 'NE')> 2
    Text <Attr.Type.Querier String ('CONTAINS', 'ENDSWITH', 'EQ', 'GE', 'GT', 'IN', 'LE', 'LT', 'NE', 'STARTSWITH')> 3
    Thumbnail <Attr.Type.Querier Composite ()> None
    Time <Attr.Type.Querier Ckd ('EQ', 'GE', 'GT', 'IN', 'LE', 'LT', 'NE')> 0
    Time_Interval <Attr.Type.Querier Composite ()> None
    Unit <Attr.Type.Querier Ckd ('EQ', 'GE', 'GT', 'IN', 'LE', 'LT', 'NE')> 0
    Url <Attr.Type.Querier Id_Entity ('EQ', 'IN', 'NE')> 2
    Url <Attr.Type.Querier String ('CONTAINS', 'ENDSWITH', 'EQ', 'GE', 'GT', 'IN', 'LE', 'LT', 'NE', 'STARTSWITH')> 3
    Weekday_RR_List <Attr.Type.Querier Ckd ('EQ', 'GE', 'GT', 'IN', 'LE', 'LT', 'NE')> 0
    X <Attr.Type.Querier Ckd ('EQ', 'GE', 'GT', 'IN', 'LE', 'LT', 'NE')> 0
    Y <Attr.Type.Querier Ckd ('EQ', 'GE', 'GT', 'IN', 'LE', 'LT', 'NE')> 0

    >>> for sig, Sig_Key in sorted (at.AQ.Signatures.iteritems (), key = TFL.Getter [1]) :
    ...     print Sig_Key, sig
    0 ('EQ', 'GE', 'GT', 'IN', 'LE', 'LT', 'NE')
    1 ('EQ',)
    2 ('EQ', 'IN', 'NE')
    3 ('CONTAINS', 'ENDSWITH', 'EQ', 'GE', 'GT', 'IN', 'LE', 'LT', 'NE', 'STARTSWITH')

    >>> for k, v in sorted (at.AQ.Base_Op_Table.iteritems ()) :
    ...     print "%%-12s %%s" %% (k, v)
    CONTAINS     <Attr.Filter CONTAINS [contains]>
    ENDSWITH     <Attr.Filter ENDSWITH [ends-with]>
    EQ           <Attr.Filter EQ [==]>
    GE           <Attr.Filter GE [>=]>
    GT           <Attr.Filter GT [>]>
    IN           <Attr.Filter IN [in]>
    LE           <Attr.Filter LE [<=]>
    LT           <Attr.Filter LT [<]>
    NE           <Attr.Filter NE [!=]>
    STARTSWITH   <Attr.Filter STARTSWITH [starts-with]>

    >>> seen = set ()
    >>> for at in sorted (scope.attribute_types, key = TFL.Getter.typ) :
    ...     k = at.typ
    ...     if k not in seen and not isinstance (at, MOM.Attr._A_Entity_):
    ...         print "%%-20s %%-20s %%s" %% (at.typ, at, at.P_Type or "-"*10)
    ...         seen.add (k)
    AIS                  cert_id              <type 'int'>
    Angle                lat                  <type 'float'>
    Boolean              discarded            <type 'bool'>
    Date                 date                 <type 'datetime.date'>
    Date-Slug            perma_name           <type 'unicode'>
    Date-Time            date                 <type 'datetime.datetime'>
    Date_List            date_exceptions      <class '_MOM._Attr.Coll.List'>
    Directory            directory            <type 'str'>
    Email                address              <type 'unicode'>
    Float                beam                 <type 'float'>
    Format               format               ----------
    Int                  count                <type 'int'>
    Int_List             easter_offset        <class '_MOM._Attr.Coll.List'>
    Name                 name                 <type 'unicode'>
    Nation               nation               <type 'unicode'>
    Numeric_String       area_code            <type 'unicode'>
    Sex                  sex                  <type 'unicode'>
    String               city                 <type 'unicode'>
    Text                 abstract             <type 'unicode'>
    Time                 finish               <type 'datetime.time'>
    Unit                 unit                 <type 'int'>
    Url                  link_to              <type 'unicode'>
    Weekday_RR_List      week_day             <class '_MOM._Attr.Coll.List'>
    X                    width                <type 'int'>
    Y                    height               <type 'int'>

    >>> scope.destroy ()

"""

from _GTW.__test__.model import *

__test__ = Scaffold.create_test_dict (_test_code)

### __END__ GTW.__test__.Attr_Filter
