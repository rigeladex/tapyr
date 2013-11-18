# -*- coding: utf-8 -*-
# Copyright (C) 2010-2013 Martin Glueck All rights reserved
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
#    GTW.__test__.Boat_in_Regatta
#
# Purpose
#    Test creation and querying of Boat_in_Regatta
#
# Revision Dates
#     3-May-2010 (MG) Creation
#     3-May-2010 (CT) Creation continued
#    14-Dec-2011 (CT) Add tests for `attrs`
#    19-Jan-2012 (CT) Add tests for `object_referring_attributes`
#    19-Jan-2012 (CT) Add `_delayed` tests
#    19-Mar-2012 (CT) Adapt to `Boat_Class.name.ignore_case` now being `True`
#    19-Mar-2012 (CT) Adapt to reification of `SRM.Handicap`
#    27-Apr-2012 (CT) Add test for `skipper_not_multiplexed`
#     7-May-2012 (CT) Add test for `crew_number_valid`
#    12-Jun-2012 (CT) Add tests for `tn_pid`, `.attrs ("type_name")`
#    27-Jun-2012 (CT) Add tests for `query_changes` for `type_name`
#     1-Aug-2012 (CT) Add `_test_referential_integrity`
#     3-Aug-2012 (MG) Improve `_test_referential_integrity`
#     4-Aug-2012 (CT) Add `_test_undo`, add `raw = True` to entity creation
#    12-Oct-2012 (CT) Adapt to repr change of `An_Entity`
#    13-Nov-2012 (CT) Adapt to change of `SRM.Club.name.cooked`
#    10-Dec-2012 (CT) Add tests for `.FO` (nested attributes)
#    19-Mar-2013 (CT) Add tests for `AQ.Attrs`, `AQ.E_Type`, `AQx`
#    19-Mar-2013 (CT) Add test for `AQ.Atoms`
#    15-Apr-2013 (CT) Adapt to change of `MOM.Attr.Kind.reset`
#    26-Jul-2013 (CT) Add `_test_polymorph`
#    20-Aug-2013 (CT) Remove `show_ora`, `show_dep` from `test_code`
#                     Lazy loading of objects breaks this in SAS, SAW backends
#     9-Oct-2013 (CT) Add `_test_qr_grouped_by`
#    ««revision-date»»···
#--

from   __future__  import unicode_literals

_test_code = r"""
    >>> scope = Scaffold.scope (%(p1)s, %(n1)s) # doctest:+ELLIPSIS
    Creating new scope MOMT__...
    >>> PAP   = scope.PAP
    >>> SRM   = scope.SRM
    >>> BiR   = SRM.Boat_in_Regatta
    >>> today = BiR.registration_date.default
    >>> bc    = SRM.Boat_Class ("Optimist", max_crew = 1, raw = True)
    >>> ys    = SRM.Handicap ("Yardstick", raw = True)
    >>> b     = SRM.Boat.instance_or_new (u'Optimist', u"1107", u"AUT", raw = True)
    >>> p     = PAP.Person.instance_or_new (u"Tanzer", u"Christian", raw = True)
    >>> s     = SRM.Sailor.instance_or_new (p.epk_raw, nation = u"AUT", mna_number = u"29676", raw = True) ### 1
    >>> rev   = SRM.Regatta_Event (u"Himmelfahrt", (u"20080501", ), raw = True)
    >>> reg   = SRM.Regatta_C (rev.epk_raw, bc.epk_raw, raw = True)
    >>> reh   = SRM.Regatta_H (rev.epk_raw, ys,  raw = True)
    >>> list (r.name for r in sorted (rev.regattas))
    [u'Optimist', u'Yardstick']

    >>> reg.set_raw (result = dict (date = "26.5.2009 10:20", software = u"calculated with REGATTA.yellow8.com", status = "final", raw = True))
    1
    >>> unicode (reg.FO.result)
    u'2009/05/26 10:20:00, calculated with REGATTA.yellow8.com, final'
    >>> scope.commit ()

    >>> scope.MOM.Id_Entity.query ().order_by (TFL.Sorted_By ("pid")).attrs ("pid", "type_name").all ()
    [(1, 'SRM.Boat_Class'), (2, 'SRM.Handicap'), (3, 'SRM.Boat'), (4, 'PAP.Person'), (5, 'SRM.Sailor'), (6, 'SRM.Regatta_Event'), (7, 'SRM.Regatta_C'), (8, 'SRM.Regatta_H')]
    >>> scope.MOM.Id_Entity.query ().order_by (TFL.Sorted_By ("pid")).attrs ("type_name", "pid").all ()
    [('SRM.Boat_Class', 1), ('SRM.Handicap', 2), ('SRM.Boat', 3), ('PAP.Person', 4), ('SRM.Sailor', 5), ('SRM.Regatta_Event', 6), ('SRM.Regatta_C', 7), ('SRM.Regatta_H', 8)]

    >>> scope.MOM.Id_Entity.query ().order_by (TFL.Sorted_By ("type_name", "pid")).attrs ("pid", "type_name").all ()
    [(4, 'PAP.Person'), (3, 'SRM.Boat'), (1, 'SRM.Boat_Class'), (2, 'SRM.Handicap'), (7, 'SRM.Regatta_C'), (6, 'SRM.Regatta_Event'), (8, 'SRM.Regatta_H'), (5, 'SRM.Sailor')]

    >>> rev.epk_raw
    (u'Himmelfahrt', (('finish', u'2008/05/01'), ('start', u'2008/05/01')), 'SRM.Regatta_Event')
    >>> reg.epk_raw
    ((u'Himmelfahrt', (('finish', u'2008/05/01'), ('start', u'2008/05/01')), 'SRM.Regatta_Event'), (u'Optimist', 'SRM.Boat_Class'), 'SRM.Regatta_C')
    >>> SRM.Regatta_C.instance (* reg.epk)
    SRM.Regatta_C ((u'himmelfahrt', (u'2008/05/01', u'2008/05/01')), (u'optimist', ))
    >>> SRM.Regatta.instance (* reg.epk)
    SRM.Regatta_C ((u'himmelfahrt', (u'2008/05/01', u'2008/05/01')), (u'optimist', ))
    >>> SRM.Regatta_C.instance (* reg.epk_raw, raw = True)
    SRM.Regatta_C ((u'himmelfahrt', (u'2008/05/01', u'2008/05/01')), (u'optimist', ))

    >>> bir = BiR (b.epk_raw, reg.epk_raw, skipper = s.epk_raw, raw = True)
    >>> bir.registration_date == today
    True

    >>> bir.epk_raw
    (((u'Optimist', 'SRM.Boat_Class'), u'1107', u'AUT', u'', 'SRM.Boat'), ((u'Himmelfahrt', (('finish', u'2008/05/01'), ('start', u'2008/05/01')), 'SRM.Regatta_Event'), (u'Optimist', 'SRM.Boat_Class'), 'SRM.Regatta_C'), 'SRM.Boat_in_Regatta')
    >>> BiR.instance (* bir.epk_raw, raw = True)
    SRM.Boat_in_Regatta (((u'optimist', ), 1107, u'AUT', u''), ((u'himmelfahrt', (u'2008/05/01', u'2008/05/01')), (u'optimist', )))

    >>> print (bir.FO.pid)
    9
    >>> print (bir.FO.right.left.pid)
    6
    >>> print (bir.FO.left)
    Optimist, AUT 1107
    >>> print (bir.FO.left.left)
    Optimist
    >>> print (bir.FO.left.left.name)
    Optimist
    >>> print (bir.FO.right)
    Himmelfahrt 2008/05/01, Optimist
    >>> print (bir.FO.right.left)
    Himmelfahrt 2008/05/01
    >>> print (bir.FO.right.left.date)
    2008/05/01
    >>> print (bir.FO.right.left.date.start)
    2008/05/01
    >>> print (bir.FO.right.left.date.finish)
    2008/05/01

    >>> print (getattr (bir.FO, "pid"))
    9
    >>> print (getattr (bir.FO, "right.left.pid"))
    6
    >>> print (getattr (bir.FO, "left"))
    Optimist, AUT 1107
    >>> print (getattr (bir.FO, "left.left"))
    Optimist
    >>> print (getattr (bir.FO, "left.left.name"))
    Optimist
    >>> print (getattr (bir.FO, "right"))
    Himmelfahrt 2008/05/01, Optimist
    >>> print (getattr (bir.FO, "right.left"))
    Himmelfahrt 2008/05/01
    >>> print (getattr (bir.FO, "right.left.date"))
    2008/05/01
    >>> print (getattr (bir.FO, "right.left.date.finish"))
    2008/05/01

    >>> sorted (reg.boats)
    [SRM.Boat_in_Regatta (((u'optimist', ), 1107, u'AUT', u''), ((u'himmelfahrt', (u'2008/05/01', u'2008/05/01')), (u'optimist', )))]

    >>> sort_key = TFL.Sorted_By ("-regatta.event.date.start", "skipper.person.last_name", "skipper.person.first_name")

    >>> print sort_key
    <Sorted_By: Descending-Getter function for `.regatta.event.date.start`, Getter function for `.skipper.person.last_name`, Getter function for `.skipper.person.first_name`>
    >>> print BiR.E_Type.sort_key_pm (sort_key)
    <Sorted_By: Getter function for `.relevant_root.type_name`, <Sorted_By: Descending-Getter function for `.regatta.event.date.start`, Getter function for `.skipper.person.last_name`, Getter function for `.skipper.person.first_name`>>

    >>> list (BiR.query (sort_key = sort_key))
    [SRM.Boat_in_Regatta (((u'optimist', ), 1107, u'AUT', u''), ((u'himmelfahrt', (u'2008/05/01', u'2008/05/01')), (u'optimist', )))]
    >>> list (BiR.query_s (sort_key = sort_key))
    [SRM.Boat_in_Regatta (((u'optimist', ), 1107, u'AUT', u''), ((u'himmelfahrt', (u'2008/05/01', u'2008/05/01')), (u'optimist', )))]

    >>> df = SRM.Regatta.AQ.event.date.start.EQ ("2008")
    >>> df
    Q.left.date.start.between (datetime.date(2008, 1, 1), datetime.date(2008, 12, 31))

    >>> AQ  = BiR.AQ.Select (MOM.Attr.Selector.sig)
    >>> q   = SRM.Regatta.query_s ().filter (df)
    >>> fs  = tuple (x.QR for x in AQ.regatta.Unwrapped_Atoms)
    >>> fsn = tuple (x._name for x in fs)
    >>> fss = ('left.__raw_name', 'left.date')
    >>> fst = ('left', )

    >>> AQ
    <Attr.Type.Querier.E_Type for SRM.Boat_in_Regatta>
    >>> AQ._attr_selector
    <MOM.Attr.Selector.Kind sig_attr>
    >>> AQ.left._attr_selector
    <MOM.Attr.Selector.Kind sig_attr>
    >>> AQ.right.left.date._attr_selector
    <MOM.Attr.Selector.Kind sig_attr>

    >>> AQ.Attrs
    (<left.AQ [Attr.Type.Querier Id_Entity]>, <right.AQ [Attr.Type.Querier Id_Entity]>)
    >>> AQ.left.Attrs
    (<left.left.AQ [Attr.Type.Querier Id_Entity]>, <left.sail_number.AQ [Attr.Type.Querier Raw]>, <left.nation.AQ [Attr.Type.Querier Ckd]>, <left.sail_number_x.AQ [Attr.Type.Querier String]>)
    >>> AQ.right.left.date.Attrs
    (<right.left.date.start.AQ [Attr.Type.Querier Date]>, <right.left.date.finish.AQ [Attr.Type.Querier Date]>)

    >>> print AQ.E_Type.type_name
    SRM.Boat_in_Regatta
    >>> print AQ.left.E_Type.type_name
    SRM.Boat
    >>> print AQ.right.left.date.E_Type.type_name
    MOM.Date_Interval_C
    >>> print AQ.right.left.date.start.E_Type
    None

    >>> for aq in BiR.AQ.Attrs_Transitive :
    ...     print (aq, aq.E_Type.type_name if aq.E_Type else "-"*5)
    (<left.AQ [Attr.Type.Querier Id_Entity]>, 'SRM.Boat')
    (<left.left.AQ [Attr.Type.Querier Id_Entity]>, 'SRM.Boat_Class')
    (<left.left.name.AQ [Attr.Type.Querier String]>, u'-----')
    (<left.left.max_crew.AQ [Attr.Type.Querier Ckd]>, u'-----')
    (<left.left.beam.AQ [Attr.Type.Querier Ckd]>, u'-----')
    (<left.left.loa.AQ [Attr.Type.Querier Ckd]>, u'-----')
    (<left.left.sail_area.AQ [Attr.Type.Querier Ckd]>, u'-----')
    (<left.left.last_cid.AQ [Attr.Type.Querier Ckd]>, u'-----')
    (<left.left.pid.AQ [Attr.Type.Querier Ckd]>, u'-----')
    (<left.left.type_name.AQ [Attr.Type.Querier String]>, u'-----')
    (<left.sail_number.AQ [Attr.Type.Querier Raw]>, u'-----')
    (<left.nation.AQ [Attr.Type.Querier Ckd]>, u'-----')
    (<left.sail_number_x.AQ [Attr.Type.Querier String]>, u'-----')
    (<left.name.AQ [Attr.Type.Querier String]>, u'-----')
    (<left.last_cid.AQ [Attr.Type.Querier Ckd]>, u'-----')
    (<left.pid.AQ [Attr.Type.Querier Ckd]>, u'-----')
    (<left.type_name.AQ [Attr.Type.Querier String]>, u'-----')
    (<right.AQ [Attr.Type.Querier Id_Entity]>, 'SRM.Regatta')
    (<right.left.AQ [Attr.Type.Querier Id_Entity]>, 'SRM.Regatta_Event')
    (<right.left.name.AQ [Attr.Type.Querier String]>, u'-----')
    (<right.left.date.AQ [Attr.Type.Querier Composite]>, 'MOM.Date_Interval_C')
    (<right.left.date.start.AQ [Attr.Type.Querier Date]>, u'-----')
    (<right.left.date.finish.AQ [Attr.Type.Querier Date]>, u'-----')
    (<right.left.date.alive.AQ [Attr.Type.Querier Boolean]>, u'-----')
    (<right.left.club.AQ [Attr.Type.Querier Id_Entity]>, 'SRM.Club')
    (<right.left.club.name.AQ [Attr.Type.Querier String]>, u'-----')
    (<right.left.club.long_name.AQ [Attr.Type.Querier String]>, u'-----')
    (<right.left.club.last_cid.AQ [Attr.Type.Querier Ckd]>, u'-----')
    (<right.left.club.pid.AQ [Attr.Type.Querier Ckd]>, u'-----')
    (<right.left.club.type_name.AQ [Attr.Type.Querier String]>, u'-----')
    (<right.left.desc.AQ [Attr.Type.Querier String]>, u'-----')
    (<right.left.is_cancelled.AQ [Attr.Type.Querier Boolean]>, u'-----')
    (<right.left.last_cid.AQ [Attr.Type.Querier Ckd]>, u'-----')
    (<right.left.pid.AQ [Attr.Type.Querier Ckd]>, u'-----')
    (<right.left.type_name.AQ [Attr.Type.Querier String]>, u'-----')
    (<right.left.perma_name.AQ [Attr.Type.Querier String]>, u'-----')
    (<right.boat_class.AQ [Attr.Type.Querier Id_Entity]>, 'SRM._Boat_Class_')
    (<right.boat_class.name.AQ [Attr.Type.Querier String]>, u'-----')
    (<right.boat_class.last_cid.AQ [Attr.Type.Querier Ckd]>, u'-----')
    (<right.boat_class.pid.AQ [Attr.Type.Querier Ckd]>, u'-----')
    (<right.boat_class.type_name.AQ [Attr.Type.Querier String]>, u'-----')
    (<right.discards.AQ [Attr.Type.Querier Ckd]>, u'-----')
    (<right.is_cancelled.AQ [Attr.Type.Querier Boolean]>, u'-----')
    (<right.kind.AQ [Attr.Type.Querier String]>, u'-----')
    (<right.races.AQ [Attr.Type.Querier Ckd]>, u'-----')
    (<right.result.AQ [Attr.Type.Querier Composite]>, 'SRM.Regatta_Result')
    (<right.result.date.AQ [Attr.Type.Querier Ckd]>, u'-----')
    (<right.result.software.AQ [Attr.Type.Querier String]>, u'-----')
    (<right.result.status.AQ [Attr.Type.Querier String]>, u'-----')
    (<right.last_cid.AQ [Attr.Type.Querier Ckd]>, u'-----')
    (<right.pid.AQ [Attr.Type.Querier Ckd]>, u'-----')
    (<right.type_name.AQ [Attr.Type.Querier String]>, u'-----')
    (<right.perma_name.AQ [Attr.Type.Querier String]>, u'-----')
    (<skipper.AQ [Attr.Type.Querier Id_Entity]>, 'SRM.Sailor')
    (<skipper.left.AQ [Attr.Type.Querier Id_Entity]>, 'PAP.Person')
    (<skipper.left.last_name.AQ [Attr.Type.Querier String_FL]>, u'-----')
    (<skipper.left.first_name.AQ [Attr.Type.Querier String_FL]>, u'-----')
    (<skipper.left.middle_name.AQ [Attr.Type.Querier String]>, u'-----')
    (<skipper.left.title.AQ [Attr.Type.Querier String]>, u'-----')
    (<skipper.left.lifetime.AQ [Attr.Type.Querier Composite]>, 'MOM.Date_Interval')
    (<skipper.left.lifetime.start.AQ [Attr.Type.Querier Date]>, u'-----')
    (<skipper.left.lifetime.finish.AQ [Attr.Type.Querier Date]>, u'-----')
    (<skipper.left.lifetime.alive.AQ [Attr.Type.Querier Boolean]>, u'-----')
    (<skipper.left.salutation.AQ [Attr.Type.Querier String]>, u'-----')
    (<skipper.left.sex.AQ [Attr.Type.Querier Ckd]>, u'-----')
    (<skipper.left.last_cid.AQ [Attr.Type.Querier Ckd]>, u'-----')
    (<skipper.left.pid.AQ [Attr.Type.Querier Ckd]>, u'-----')
    (<skipper.left.type_name.AQ [Attr.Type.Querier String]>, u'-----')
    (<skipper.nation.AQ [Attr.Type.Querier Ckd]>, u'-----')
    (<skipper.mna_number.AQ [Attr.Type.Querier Raw]>, u'-----')
    (<skipper.club.AQ [Attr.Type.Querier Id_Entity]>, 'SRM.Club')
    (<skipper.club.name.AQ [Attr.Type.Querier String]>, u'-----')
    (<skipper.club.long_name.AQ [Attr.Type.Querier String]>, u'-----')
    (<skipper.club.last_cid.AQ [Attr.Type.Querier Ckd]>, u'-----')
    (<skipper.club.pid.AQ [Attr.Type.Querier Ckd]>, u'-----')
    (<skipper.club.type_name.AQ [Attr.Type.Querier String]>, u'-----')
    (<skipper.last_cid.AQ [Attr.Type.Querier Ckd]>, u'-----')
    (<skipper.pid.AQ [Attr.Type.Querier Ckd]>, u'-----')
    (<skipper.type_name.AQ [Attr.Type.Querier String]>, u'-----')
    (<place.AQ [Attr.Type.Querier Ckd]>, u'-----')
    (<points.AQ [Attr.Type.Querier Ckd]>, u'-----')
    (<last_cid.AQ [Attr.Type.Querier Ckd]>, u'-----')
    (<pid.AQ [Attr.Type.Querier Ckd]>, u'-----')
    (<type_name.AQ [Attr.Type.Querier String]>, u'-----')
    (<rank.AQ [Attr.Type.Querier Ckd]>, u'-----')
    (<registration_date.AQ [Attr.Type.Querier Date]>, u'-----')

    >>> BiR.AQ
    <Attr.Type.Querier.E_Type for SRM.Boat_in_Regatta>

    >>> for aq in BiR.AQ.Atoms :
    ...     print (aq._id)
    left__left__name
    left__left__max_crew
    left__left__beam
    left__left__loa
    left__left__sail_area
    left__left__last_cid
    left__left__pid
    left__left__type_name
    left__sail_number
    left__nation
    left__sail_number_x
    left__name
    left__last_cid
    left__pid
    left__type_name
    right__left__name
    right__left__date__start
    right__left__date__finish
    right__left__date__alive
    right__left__club__name
    right__left__club__long_name
    right__left__club__last_cid
    right__left__club__pid
    right__left__club__type_name
    right__left__desc
    right__left__is_cancelled
    right__left__last_cid
    right__left__pid
    right__left__type_name
    right__left__perma_name
    right__boat_class__name
    right__boat_class__last_cid
    right__boat_class__pid
    right__boat_class__type_name
    right__discards
    right__is_cancelled
    right__kind
    right__races
    right__result__date
    right__result__software
    right__result__status
    right__last_cid
    right__pid
    right__type_name
    right__perma_name
    skipper__left__last_name
    skipper__left__first_name
    skipper__left__middle_name
    skipper__left__title
    skipper__left__lifetime__start
    skipper__left__lifetime__finish
    skipper__left__lifetime__alive
    skipper__left__salutation
    skipper__left__sex
    skipper__left__last_cid
    skipper__left__pid
    skipper__left__type_name
    skipper__nation
    skipper__mna_number
    skipper__club__name
    skipper__club__long_name
    skipper__club__last_cid
    skipper__club__pid
    skipper__club__type_name
    skipper__last_cid
    skipper__pid
    skipper__type_name
    place
    points
    last_cid
    pid
    type_name
    rank
    registration_date

    >>> fs
    (Q.left.__raw_name, Q.left.date.start, Q.left.date.finish, Q.boat_class.__raw_name)

    >>> list (q)
    [SRM.Regatta_C ((u'himmelfahrt', (u'2008/05/01', u'2008/05/01')), (u'optimist', )), SRM.Regatta_H ((u'himmelfahrt', (u'2008/05/01', u'2008/05/01')), (u'yardstick', ))]

    >>> list (q.attrs (* fs))
    [(u'Himmelfahrt', datetime.date(2008, 5, 1), datetime.date(2008, 5, 1), u'Optimist'), (u'Himmelfahrt', datetime.date(2008, 5, 1), datetime.date(2008, 5, 1), u'Yardstick')]

    >>> list (q.attrs (* fsn))
    [(u'Himmelfahrt', datetime.date(2008, 5, 1), datetime.date(2008, 5, 1), u'Optimist'), (u'Himmelfahrt', datetime.date(2008, 5, 1), datetime.date(2008, 5, 1), u'Yardstick')]

    >>> list (q.attrs (* fss))
    [(u'Himmelfahrt', MOM.Date_Interval_C (u'2008/05/01', u'2008/05/01'))]

    >>> list (q.attrs (* fst))
    [(SRM.Regatta_Event (u'himmelfahrt', (u'2008/05/01', u'2008/05/01')),)]

    >>> list (q.attrs (* fst, allow_duplicates = True))
    [(SRM.Regatta_Event (u'himmelfahrt', (u'2008/05/01', u'2008/05/01')),), (SRM.Regatta_Event (u'himmelfahrt', (u'2008/05/01', u'2008/05/01')),)]

    >>> AQ  = BiR.AQ.Select (MOM.Attr.Selector.ui_attr)
    >>> AQ
    <Attr.Type.Querier.E_Type for SRM.Boat_in_Regatta>
    >>> AQ._attr_selector
    <MOM.Attr.Selector.Pred <MOM.Attr.Selector.Kind q_able> if Q.show_in_ui>
    >>> AQ.left._attr_selector
    <MOM.Attr.Selector.Pred <MOM.Attr.Selector.Kind q_able> if Q.show_in_ui>
    >>> AQ.right.left.date._attr_selector
    <MOM.Attr.Selector.Pred <MOM.Attr.Selector.Kind q_able> if Q.show_in_ui>

    >>> tuple (x.QR for x in AQ.regatta.Atoms)
    (Q.right.left.__raw_name, Q.right.left.date.start, Q.right.left.date.finish, Q.right.left.date.alive, Q.right.left.club.__raw_name, Q.right.left.club.long_name, Q.right.left.club.last_cid, Q.right.left.club.pid, Q.right.left.club.type_name, Q.right.left.desc, Q.right.left.is_cancelled, Q.right.left.last_cid, Q.right.left.pid, Q.right.left.type_name, Q.right.left.perma_name, Q.right.boat_class.__raw_name, Q.right.boat_class.last_cid, Q.right.boat_class.pid, Q.right.boat_class.type_name, Q.right.discards, Q.right.is_cancelled, Q.right.kind, Q.right.races, Q.right.result.date, Q.right.result.software, Q.right.result.status, Q.right.last_cid, Q.right.pid, Q.right.type_name, Q.right.perma_name)

    >>> scope.query_changes (type_name = "SRM.Regatta").order_by (Q.cid).first ()
    >>> scope.query_changes (type_name = "SRM.Regatta_C").order_by (Q.cid).first ()
    <Create SRM.Regatta_C ((u'Himmelfahrt', (('finish', u'2008/05/01'), ('start', u'2008/05/01')), 'SRM.Regatta_Event'), (u'Optimist', 'SRM.Boat_Class'), 'SRM.Regatta_C'), new-values = {'is_cancelled' : u'no', 'last_cid' : '7', 'perma_name' : u'optimist'}>
    >>> scope.query_changes (Q.type_name == "SRM.Regatta_H").order_by (Q.cid).first ()
    <Create SRM.Regatta_H ((u'Himmelfahrt', (('finish', u'2008/05/01'), ('start', u'2008/05/01')), 'SRM.Regatta_Event'), (u'Yardstick', 'SRM.Handicap'), 'SRM.Regatta_H'), new-values = {'is_cancelled' : u'no', 'last_cid' : '8', 'perma_name' : u'yardstick'}>

    >>> scope.query_changes ((Q.type_name == "SRM.Regatta_C") | (Q.type_name == "SRM.Regatta_H")).order_by (Q.cid).first ()
    <Create SRM.Regatta_C ((u'Himmelfahrt', (('finish', u'2008/05/01'), ('start', u'2008/05/01')), 'SRM.Regatta_Event'), (u'Optimist', 'SRM.Boat_Class'), 'SRM.Regatta_C'), new-values = {'is_cancelled' : u'no', 'last_cid' : '7', 'perma_name' : u'optimist'}>

    >>> scope.query_changes (Q.OR (Q.type_name == "SRM.Regatta_C", Q.type_name == "SRM.Regatta_H")).order_by (Q.cid).first ()
    <Create SRM.Regatta_C ((u'Himmelfahrt', (('finish', u'2008/05/01'), ('start', u'2008/05/01')), 'SRM.Regatta_Event'), (u'Optimist', 'SRM.Boat_Class'), 'SRM.Regatta_C'), new-values = {'is_cancelled' : u'no', 'last_cid' : '7', 'perma_name' : u'optimist'}>

    >>> scope.query_changes (Q.type_name.IN (('SRM.Regatta', 'SRM.Regatta_H', 'SRM.Regatta_C'))).order_by (Q.cid).first ()
    <Create SRM.Regatta_C ((u'Himmelfahrt', (('finish', u'2008/05/01'), ('start', u'2008/05/01')), 'SRM.Regatta_Event'), (u'Optimist', 'SRM.Boat_Class'), 'SRM.Regatta_C'), new-values = {'is_cancelled' : u'no', 'last_cid' : '7', 'perma_name' : u'optimist'}>

    >>> scope.commit ()

    >>> b8   = SRM.Boat.instance_or_new (u'Optimist', u"1108", u"AUT", raw = True)

    >>> b8
    SRM.Boat ((u'optimist', ), 1108, u'AUT', u'')

    >>> bir8 = BiR (b8, reg, skipper = s)
    Traceback (most recent call last):
      ...
    Invariants: A sailor can't be skipper of more than one boat in a single
    regatta event.
      The new definition of Boat_in_Regatta SRM.Boat_in_Regatta (((u'Optimist', 'SRM.Boat_Class'), u'1108', u'AUT', u'', 'SRM.Boat'), ((u'Himmelfahrt', (('finish', u'2008/05/01'), ('start', u'2008/05/01')), 'SRM.Regatta_Event'), (u'Optimist', 'SRM.Boat_Class'), 'SRM.Regatta_C')) would clash with 1 existing entities
      Already existing:
        SRM.Boat_in_Regatta (((u'Optimist', 'SRM.Boat_Class'), u'1107', u'AUT', u'', 'SRM.Boat'), ((u'Himmelfahrt', (('finish', u'2008/05/01'), ('start', u'2008/05/01')), 'SRM.Regatta_Event'), (u'Optimist', 'SRM.Boat_Class'), 'SRM.Regatta_C'))

    >>> b8
    SRM.Boat ((u'optimist', ), 1108, u'AUT', u'')

    >>> scope.commit ()

    >>> scope.rollback ()

    >>> p2  = PAP.Person.instance_or_new (u"Tanzer", u"Laurens")
    >>> s2  = SRM.Sailor.instance_or_new (p2, nation = u"AUT", raw = True)
    >>> cr = SRM.Crew_Member (bir, s2)

    >>> scope.commit ()
    Traceback (most recent call last):
      ...
    Invariants: Condition `crew_number_valid` : The number of crew members must be less than
    `boat.b_class.max_crew`. (number_of_crew < boat.b_class.max_crew)
        boat = Optimist, AUT 1107
        boat.b_class.max_crew = 1
        crew = [SRM.Sailor ((u'tanzer', u'laurens', u'', u''), u'AUT', None, u'')]
        number_of_crew = 1 << len (crew)

    >>> print bir.skipper
    ((u'tanzer', u'christian', u'', u''), u'AUT', 29676, u'')
    >>> bir.skipper is s
    True
    >>> bir.skipper.destroy ()
    >>> print bir.skipper
    Traceback (most recent call last):
      ...
    Destroyed_Entity: <Destroyed entity SRM.Boat_in_Regatta (((u'optimist', ), 1107, u'AUT', u''), ((u'himmelfahrt', (u'2008/05/01', u'2008/05/01')), (u'optimist', )))>: access to attribute 'skipper' not allowed


"""

_test_delayed  = r"""
    >>> scope = Scaffold.scope (%(p1)s, %(n1)s) # doctest:+ELLIPSIS
    Creating new scope MOMT__...
    >>> PAP = scope.PAP
    >>> SRM = scope.SRM
    >>> BiR = SRM.Boat_in_Regatta
    >>> bc  = SRM.Boat_Class.E_Type ("Optimist", max_crew = 1, raw = True)
    >>> ys  = SRM.Handicap.E_Type ("Yardstick", raw = True)
    >>> b   = SRM.Boat.E_Type (bc, u"1107", u"AUT", raw = True)
    >>> p   = PAP.Person.E_Type (u"Tanzer", u"Christian", raw = True)
    >>> s   = SRM.Sailor.E_Type (p, nation = u"AUT", mna_number = u"29676", raw = True) ### 1
    >>> rev = SRM.Regatta_Event.E_Type (u"Himmelfahrt", (u"20080501", ), raw = True)
    >>> reg = SRM.Regatta_C.E_Type (rev, bc)
    >>> reh = SRM.Regatta_H.E_Type (rev, ys)
    >>> bir = BiR.E_Type (b, reg, skipper = s)

    >>> list (r.name for r in sorted (getattr (rev, "regattas", [])))
    []

    >>> reg.set_raw (result = dict (date = "26.5.2009 10:20", software = u"calculated with REGATTA.yellow8.com", status = "final", raw = True))
    1
    >>> unicode (reg.FO.result)
    u'2009/05/26 10:20:00, calculated with REGATTA.yellow8.com, final'

    >>> show_ora (bir)  ### before scope.add
    ---
    >>> show_dep (s)    ### before scope.add
    ---

    >>> for _ in (bc, ys, b, p, s, rev, reg, reh, bir) :
    ...     scope.add (_)

    >>> list (r.name for r in sorted (rev.regattas))
    [u'Optimist', u'Yardstick']

    >>> show_ora (bir)         ### before destroy
    ((u'tanzer', u'christian', u'', u''), u'AUT', 29676, u'') : Entity `skipper`
    >>> show_dep (bir.skipper) ### before destroy
    (((u'optimist', ), 1107, u'AUT', u''), ((u'himmelfahrt', (u'2008/05/01', u'2008/05/01')), (u'optimist', ))) : 1
    >>> print bir.skipper
    ((u'tanzer', u'christian', u'', u''), u'AUT', 29676, u'')
    >>> bir.skipper is s
    True
    >>> bir.skipper.destroy ()
    >>> show_ora (bir)  ### after destroy
    ---
    >>> show_dep (s)    ### after destroy
    ---
    >>> print bir.skipper
    Traceback (most recent call last):
      ...
    Destroyed_Entity: <Destroyed entity SRM.Boat_in_Regatta (((u'optimist', ), 1107, u'AUT', u''), ((u'himmelfahrt', (u'2008/05/01', u'2008/05/01')), (u'optimist', )))>: access to attribute 'skipper' not allowed


"""

_test_polymorph = r"""
    >>> scope = Scaffold.scope (%(p1)s, %(n1)s) # doctest:+ELLIPSIS
    Creating new scope MOMT__...
    >>> PAP = scope.PAP
    >>> SRM = scope.SRM

    >>> bc    = SRM.Boat_Class ("Optimist", max_crew = 1, raw = True)
    >>> ys    = SRM.Handicap ("Yardstick", raw = True)
    >>> rev   = SRM.Regatta_Event (u"Himmelfahrt", (u"20080501", ), raw = True)
    >>> reg   = SRM.Regatta_C (rev.epk_raw, bc.epk_raw, raw = True)
    >>> reh   = SRM.Regatta_H (rev.epk_raw, ys,  raw = True)

    >>> df = SRM.Regatta.AQ.event.date.start.EQ ("2008")
    >>> df
    Q.left.date.start.between (datetime.date(2008, 1, 1), datetime.date(2008, 12, 31))
    >>> q   = SRM.Regatta.query_s ().filter (df)

    >>> list (q)
    [SRM.Regatta_C ((u'himmelfahrt', (u'2008/05/01', u'2008/05/01')), (u'optimist', )), SRM.Regatta_H ((u'himmelfahrt', (u'2008/05/01', u'2008/05/01')), (u'yardstick', ))]

    >>> sk = TFL.Sorted_By (Q.event.date, Q.event.name, Q.boat_class.name)
    >>> sk = Q.pid

    >>> SRM.Regatta.query   ().order_by (sk).all ()
    [SRM.Regatta_C ((u'himmelfahrt', (u'2008/05/01', u'2008/05/01')), (u'optimist', )), SRM.Regatta_H ((u'himmelfahrt', (u'2008/05/01', u'2008/05/01')), (u'yardstick', ))]

    >>> SRM.Regatta_C.query ().order_by (sk).all ()
    [SRM.Regatta_C ((u'himmelfahrt', (u'2008/05/01', u'2008/05/01')), (u'optimist', ))]

    >>> SRM.Regatta_H.query ().order_by (sk).all ()
    [SRM.Regatta_H ((u'himmelfahrt', (u'2008/05/01', u'2008/05/01')), (u'yardstick', ))]

"""

_test_qr_grouped_by = """
    >>> scope = Scaffold.scope (%(p1)s, %(n1)s) # doctest:+ELLIPSIS
    Creating new scope MOMT__...
    >>> PAP   = scope.PAP
    >>> SRM   = scope.SRM
    >>> BiR   = SRM.Boat_in_Regatta
    >>> today = BiR.registration_date.default
    >>> bc    = SRM.Boat_Class ("Optimist", max_crew = 1, raw = True)
    >>> ol    = SRM.Boat.instance_or_new (u'Optimist', u"1107", u"AUT", raw = True)
    >>> oc    = SRM.Boat.instance_or_new (u'Optimist', u"1134", u"AUT", raw = True)
    >>> pl    = PAP.Person.instance_or_new (u"Tanzer", u"Laurens", raw = True)
    >>> pc    = PAP.Person.instance_or_new (u"Tanzer", u"Clarissa", raw = True)
    >>> sl    = SRM.Sailor.instance_or_new (pl, nation = u"AUT", raw = True)
    >>> sc    = SRM.Sailor.instance_or_new (pc, nation = u"AUT", raw = True)
    >>> rev   = SRM.Regatta_Event (u"Himmelfahrt", (u"20080501", ), raw = True)
    >>> reg   = SRM.Regatta_C (rev.epk_raw, bc, raw = True)

    >>> birl  = BiR (ol, reg, skipper = sl)
    >>> birc  = BiR (oc, reg, skipper = sc)

    >>> _     = SRM.Race_Result (birl, 1, points = 1)
    >>> _     = SRM.Race_Result (birl, 2, points = 2)
    >>> _     = SRM.Race_Result (birl, 3, points = 3)

    >>> _     = SRM.Race_Result (birc, 1, points = 2)
    >>> _     = SRM.Race_Result (birc, 2, points = 1)
    >>> _     = SRM.Race_Result (birc, 3, points = 6)

    >>> q     = SRM.Boat_in_Regatta.query ()
    >>> qa    = q.attrs (Q.pid, Q.boat, Q.SUM (Q.race_results.points), Q.SUM (1))
    >>> qag   = qa.group_by (Q.pid, Q.boat)
    >>> for x in sorted (qag, key = TFL.Getter [2]) :
    ...     print (x [1:])
    (SRM.Boat ((u'optimist', ), 1107, u'AUT', u''), 6, 3)
    (SRM.Boat ((u'optimist', ), 1134, u'AUT', u''), 9, 3)

    >>> q = SRM.Race_Result.query ()
    >>> for x in sorted (q.attrs (Q.left, Q.SUM (Q.points)).group_by (Q.left), key = TFL.Getter [1]) :
    ...     print (x [1:])
    (6,)
    (9,)

    >>> for x in sorted (q.attrs (Q.left, Q.SUM (Q.points), Q.SUM (1)).group_by (Q.left), key = TFL.Getter [1]) :
    ...     print (x [1:])
    (6, 3)
    (9, 3)

    >>> for x in sorted (q.attrs (Q.left, Q.SUM (Q.points), Q.SUM (Q.points) / Q.SUM (1)).group_by (Q.left), key = TFL.Getter [1]) :
    ...     print (x [1:])
    (6, 2)
    (9, 3)

    >>> for x in sorted (q.attrs (Q.left, Q.MIN (Q.points), Q.MAX (Q.points), Q.AVG (Q.points), Q.COUNT (Q.points)).group_by (Q.left), key = TFL.Getter [1]) :
    ...     print (", ".join (tuple ("%%g" %% (y, ) for y in x [1:])))
    1, 3, 2, 3
    1, 6, 3, 3

"""

_test_referential_integrity = r"""
    >>> scope = Scaffold.scope (%(p1)s, %(n1)s) # doctest:+ELLIPSIS
    Creating new scope MOMT__...
    >>> PAP = scope.PAP
    >>> SRM = scope.SRM
    >>> BiR = SRM.Boat_in_Regatta
    >>> bc  = SRM.Boat_Class ("Optimist", max_crew = 1, raw = True)
    >>> cl  = SRM.Club (u"SC-AMS", raw = True)
    >>> b   = SRM.Boat (u'Optimist', u"1107", u"AUT", raw = True)
    >>> p   = PAP.Person (u"Tanzer", u"Christian", raw = True)
    >>> s   = SRM.Sailor (p, nation = u"AUT", mna_number = u"29676", club = cl, raw = True) ### 1
    >>> rev = SRM.Regatta_Event (u"Himmelfahrt", (u"20080501", ), raw = True)
    >>> reg = SRM.Regatta_C (rev.epk_raw, bc.epk_raw, raw = True)
    >>> bir = BiR (b, reg, skipper = s)

    >>> scope.commit ()

    >>> bir                                           ### before s.destroy ()
    SRM.Boat_in_Regatta (((u'optimist', ), 1107, u'AUT', u''), ((u'himmelfahrt', (u'2008/05/01', u'2008/05/01')), (u'optimist', )))
    >>> print bir.pid                                 ### before s.destroy ()
    8
    >>> print cl.pid                                  ### before s.destroy ()
    2
    >>> print s.pid                                   ### before s.destroy ()
    5
    >>> print bir.skipper                             ### before s.destroy () 1
    ((u'tanzer', u'christian', u'', u''), u'AUT', 29676, (u'scams', ))
    >>> bir.last_cid                                  ### before s.destroy ()
    8
    >>> scope.MOM.Id_Entity.query_s ().count ()       ### before s.destroy ()
    8
    >>> scope.MOM.Id_Entity.query_s ().all ()         ### before s.destroy ()
    [SRM.Regatta_Event (u'himmelfahrt', (u'2008/05/01', u'2008/05/01')), SRM.Regatta_C ((u'himmelfahrt', (u'2008/05/01', u'2008/05/01')), (u'optimist', )), SRM.Boat_Class (u'optimist'), SRM.Boat ((u'optimist', ), 1107, u'AUT', u''), SRM.Boat_in_Regatta (((u'optimist', ), 1107, u'AUT', u''), ((u'himmelfahrt', (u'2008/05/01', u'2008/05/01')), (u'optimist', ))), SRM.Club (u'scams'), PAP.Person (u'tanzer', u'christian', u'', u''), SRM.Sailor ((u'tanzer', u'christian', u'', u''), u'AUT', 29676, (u'scams', ))]

    >>> bir.skipper = None
    Traceback (most recent call last):
      ...
    Required_Empty: Condition `skipper_not_empty` : skipper is not None and skipper != ''
        skipper = None
    >>> bir.set (skipper = None)
    Traceback (most recent call last):
      ...
    Invariants: Condition `skipper_not_empty` : skipper is not None and skipper != ''
        skipper = None
    >>> print bir.skipper                             ### before s.destroy () 2
    ((u'tanzer', u'christian', u'', u''), u'AUT', 29676, (u'scams', ))

    >>> scope.max_cid                                 ### before s.destroy ()
    8

    >>> print s.club                                  ### before s.destroy ()
    (u'scams')

    >>> if hasattr (scope.ems.session, "expunge") : scope.ems.session.expunge ()
    >>> cl.destroy ()
    >>> print s.club                                  ### after cl.destroy ()
    None

    >>> scope.max_cid                                 ### after cl.destroy ()
    10
    >>> bir.last_cid                                  ### after cl.destroy ()
    8
    >>> print bir                                     ### after cl.destroy ()
    (((u'optimist', ), 1107, u'AUT', u''), ((u'himmelfahrt', (u'2008/05/01', u'2008/05/01')), (u'optimist', )))
    >>> print s.pid                                   ### after cl.destroy ()
    5
    >>> print bir.skipper                             ### after cl.destroy ()
    ((u'tanzer', u'christian', u'', u''), u'AUT', 29676, u'')

    >>> scope.pid_query (s.pid)
    SRM.Sailor ((u'tanzer', u'christian', u'', u''), u'AUT', 29676, u'')

    >>> s.destroy ()

    >>> scope.max_cid                                 ### after s.destroy ()
    12

    >>> bir.last_cid                                  ### after s.destroy ()
    8
    >>> bir.left
    Traceback (most recent call last):
      ...
    Destroyed_Entity: <Destroyed entity SRM.Boat_in_Regatta (((u'optimist', ), 1107, u'AUT', u''), ((u'himmelfahrt', (u'2008/05/01', u'2008/05/01')), (u'optimist', )))>: access to attribute 'left' not allowed
    >>> scope.MOM.Id_Entity.query_s ().count ()       ### after s.destroy ()
    5
    >>> scope.MOM.Id_Entity.query_s ().all ()         ### after s.destroy ()
    [SRM.Regatta_Event (u'himmelfahrt', (u'2008/05/01', u'2008/05/01')), SRM.Regatta_C ((u'himmelfahrt', (u'2008/05/01', u'2008/05/01')), (u'optimist', )), SRM.Boat_Class (u'optimist'), SRM.Boat ((u'optimist', ), 1107, u'AUT', u''), PAP.Person (u'tanzer', u'christian', u'', u'')]

    >>> bir                                           ### after s.destroy ()
    <Destroyed entity SRM.Boat_in_Regatta (((u'optimist', ), 1107, u'AUT', u''), ((u'himmelfahrt', (u'2008/05/01', u'2008/05/01')), (u'optimist', )))>

    >>> print bir.skipper                             ### after s.destroy ()
    Traceback (most recent call last):
      ...
    Destroyed_Entity: <Destroyed entity SRM.Boat_in_Regatta (((u'optimist', ), 1107, u'AUT', u''), ((u'himmelfahrt', (u'2008/05/01', u'2008/05/01')), (u'optimist', )))>: access to attribute 'skipper' not allowed

    >>> for c in scope.uncommitted_changes :
    ...     show_change (c)
    <Destroy SRM.Club (u'SC-AMS', 'SRM.Club'), old-values = {'last_cid' : '<n>'}>
        <Modify SRM.Sailor ((u'Tanzer', u'Christian', u'', u'', 'PAP.Person'), u'AUT', u'29676', u'', 'SRM.Sailor'), old-values = {'club' : 2, 'last_cid' : '<n>'}, new-values = {'club' : u'', 'last_cid' : '<n>'}>
    <Destroy SRM.Sailor ((u'Tanzer', u'Christian', u'', u'', 'PAP.Person'), u'AUT', u'29676', u'', 'SRM.Sailor'), old-values = {'last_cid' : '<n>'}>
        <Destroy SRM.Boat_in_Regatta (((u'Optimist', 'SRM.Boat_Class'), u'1107', u'AUT', u'', 'SRM.Boat'), ((u'Himmelfahrt', (('finish', u'2008/05/01'), ('start', u'2008/05/01')), 'SRM.Regatta_Event'), (u'Optimist', 'SRM.Boat_Class'), 'SRM.Regatta_C'), 'SRM.Boat_in_Regatta'), old-values = {'last_cid' : '<n>', 'registration_date' : u'<today>', 'skipper' : 5}>

    >>> for c in scope.uncommitted_changes :
    ...     print c.cid, c.pid, c.type_name, c.epk_pid
    ...     for cc in c.children :
    ...         print "   ", cc.cid, cc.pid, cc.type_name, cc.epk_pid
    10 2 SRM.Club (u'SC-AMS', 'SRM.Club')
        9 5 SRM.Sailor (4, u'AUT', u'29676', u'', 'SRM.Sailor')
    12 5 SRM.Sailor (4, u'AUT', u'29676', u'', 'SRM.Sailor')
        11 8 SRM.Boat_in_Regatta (3, 7, 'SRM.Boat_in_Regatta')

    >>> undo_changes (scope, list (reversed (scope.uncommitted_changes [-1:])))

    >>> for c in scope.uncommitted_changes :
    ...     show_change (c)
    <Destroy SRM.Club (u'SC-AMS', 'SRM.Club'), old-values = {'last_cid' : '<n>'}>
        <Modify SRM.Sailor ((u'Tanzer', u'Christian', u'', u'', 'PAP.Person'), u'AUT', u'29676', u'', 'SRM.Sailor'), old-values = {'club' : 2, 'last_cid' : '<n>'}, new-values = {'club' : u'', 'last_cid' : '<n>'}>
    <Destroy SRM.Sailor ((u'Tanzer', u'Christian', u'', u'', 'PAP.Person'), u'AUT', u'29676', u'', 'SRM.Sailor'), old-values = {'last_cid' : '<n>'}>
        <Destroy SRM.Boat_in_Regatta (((u'Optimist', 'SRM.Boat_Class'), u'1107', u'AUT', u'', 'SRM.Boat'), ((u'Himmelfahrt', (('finish', u'2008/05/01'), ('start', u'2008/05/01')), 'SRM.Regatta_Event'), (u'Optimist', 'SRM.Boat_Class'), 'SRM.Regatta_C'), 'SRM.Boat_in_Regatta'), old-values = {'last_cid' : '<n>', 'registration_date' : u'<today>', 'skipper' : 5}>
    <Create SRM.Sailor ((u'Tanzer', u'Christian', u'', u'', 'PAP.Person'), u'AUT', u'29676', u'', 'SRM.Sailor'), new-values = {'last_cid' : '<n>'}>
    <Create SRM.Boat_in_Regatta (((u'Optimist', 'SRM.Boat_Class'), u'1107', u'AUT', u'', 'SRM.Boat'), ((u'Himmelfahrt', (('finish', u'2008/05/01'), ('start', u'2008/05/01')), 'SRM.Regatta_Event'), (u'Optimist', 'SRM.Boat_Class'), 'SRM.Regatta_C'), 'SRM.Boat_in_Regatta'), new-values = {'last_cid' : '<n>', 'registration_date' : u'<today>', 'skipper' : 5}>

"""

_test_undo = r"""
    >>> scope = Scaffold.scope (%(p1)s, %(n1)s) # doctest:+ELLIPSIS
    Creating new scope MOMT__...
    >>> PAP = scope.PAP
    >>> SRM = scope.SRM
    >>> BiR = SRM.Boat_in_Regatta
    >>> bc  = SRM.Boat_Class ("Optimist", max_crew = 1, raw = True)
    >>> cl  = SRM.Club (u"SC-AMS", raw = True)
    >>> b   = SRM.Boat (u'Optimist', u"1107", u"AUT", raw = True)
    >>> p   = PAP.Person (u"Tanzer", u"Christian", raw = True)
    >>> s   = SRM.Sailor (p, nation = u"AUT", mna_number = u"29676", club = cl, raw = True) ### 1
    >>> rev = SRM.Regatta_Event (u"Himmelfahrt", (u"20080501", ), raw = True)
    >>> reg = SRM.Regatta_C (rev, bc)
    >>> bir = BiR (b, reg, skipper = s)

    >>> scope.commit ()

    >>> for _e in scope.MOM.Id_Entity.query_s () : ### 1
    ...    print (_e.pid, _e.as_code ())
    (6, u"SRM.Regatta_Event (u'himmelfahrt', (u'2008/05/01', u'2008/05/01'), )")
    (7, u"SRM.Regatta_C ((u'himmelfahrt', (u'2008/05/01', u'2008/05/01')), (u'optimist', ), is_cancelled = 'no')")
    (1, u"SRM.Boat_Class (u'optimist', max_crew = 1)")
    (3, u"SRM.Boat ((u'optimist', ), 1107, u'AUT', u'', )")
    (8, u'SRM.Boat_in_Regatta (((u\'optimist\', ), 1107, u\'AUT\', u\'\'), ((u\'himmelfahrt\', (u\'2008/05/01\', u\'2008/05/01\')), (u\'optimist\', )), skipper = ((u"u\'tanzer\'", u"u\'christian\'", u"u\'\'", u"u\'\'"), u"u\'AUT\'", u\'29676\', (u"u\'scams\'",)))')
    (2, u"SRM.Club (u'scams', )")
    (4, u"PAP.Person (u'tanzer', u'christian', u'', u'', )")
    (5, u"SRM.Sailor ((u'tanzer', u'christian', u'', u''), u'AUT', 29676, (u'scams', ), )")

    >>> print (sorted (scope.MOM.Id_Entity.query ().attr ("pid"))) ### 2
    [1, 2, 3, 4, 5, 6, 7, 8]

    >>> s                   ### before first destroy
    SRM.Sailor ((u'tanzer', u'christian', u'', u''), u'AUT', 29676, (u'scams', ))

    >>> cl                  ### before first destroy
    SRM.Club (u'scams')
    >>> cl.last_cid, s.last_cid, scope.max_cid
    (2, 5, 8)
    >>> cl.destroy ()

    >>> s                   ### after first destroy
    SRM.Sailor ((u'tanzer', u'christian', u'', u''), u'AUT', 29676, u'')

    >>> cl                  ### after first destroy
    <Destroyed entity SRM.Club (u'scams')>
    >>> s.last_cid, scope.max_cid
    (9, 10)
    >>> for c in scope.uncommitted_changes : ### after first destroy
    ...     show_change (c)
    <Destroy SRM.Club (u'SC-AMS', 'SRM.Club'), old-values = {'last_cid' : '<n>'}>
        <Modify SRM.Sailor ((u'Tanzer', u'Christian', u'', u'', 'PAP.Person'), u'AUT', u'29676', u'', 'SRM.Sailor'), old-values = {'club' : 2, 'last_cid' : '<n>'}, new-values = {'club' : u'', 'last_cid' : '<n>'}>

    >>> print (sorted (scope.MOM.Id_Entity.query ().attr ("pid"))) ### 3
    [1, 3, 4, 5, 6, 7, 8]

    >>> scope.rollback ()   ### first rollback
    >>> for c in scope.uncommitted_changes :
    ...     show_change (c)

    >>> print (sorted (scope.MOM.Id_Entity.query ().attr ("pid"))) ### 3.5
    [1, 2, 3, 4, 5, 6, 7, 8]

    >>> s                   ### after first rollback
    SRM.Sailor ((u'tanzer', u'christian', u'', u''), u'AUT', 29676, (u'scams', ))

    >>> cl                  ### after first rollback
    SRM.Club (u'scams')

    >>> cl_revived = SRM.Club.instance (u"SC-AMS")
    >>> cl_revived
    SRM.Club (u'scams')
    >>> cl_revived.last_cid
    2
    >>> MOM.BREAK = True*0
    >>> cl_revived.destroy ()

    >>> s                   ### after second destroy
    SRM.Sailor ((u'tanzer', u'christian', u'', u''), u'AUT', 29676, u'')

    >>> for c in scope.query_changes () : ### after second destroy of club
    ...     print (clean_change (c))
    <Create SRM.Boat_Class (u'Optimist', 'SRM.Boat_Class'), new-values = {'last_cid' : '<n>', 'max_crew' : u'1'}>
    <Create SRM.Club (u'SC-AMS', 'SRM.Club'), new-values = {'last_cid' : '<n>'}>
    <Create SRM.Boat ((u'Optimist', 'SRM.Boat_Class'), u'1107', u'AUT', u'', 'SRM.Boat'), new-values = {'last_cid' : '<n>'}>
    <Create PAP.Person (u'Tanzer', u'Christian', u'', u'', 'PAP.Person'), new-values = {'last_cid' : '<n>'}>
    <Create SRM.Sailor ((u'Tanzer', u'Christian', u'', u'', 'PAP.Person'), u'AUT', u'29676', (u'SC-AMS', 'SRM.Club'), 'SRM.Sailor'), new-values = {'last_cid' : '<n>'}>
    <Create SRM.Regatta_Event (u'Himmelfahrt', (('finish', u'2008/05/01'), ('start', u'2008/05/01')), 'SRM.Regatta_Event'), new-values = {'last_cid' : '<n>', 'perma_name' : u'himmelfahrt'}>
    <Create SRM.Regatta_C ((u'Himmelfahrt', (('finish', u'2008/05/01'), ('start', u'2008/05/01')), 'SRM.Regatta_Event'), (u'Optimist', 'SRM.Boat_Class'), 'SRM.Regatta_C'), new-values = {'is_cancelled' : u'no', 'last_cid' : '<n>', 'perma_name' : u'optimist'}>
    <Create SRM.Boat_in_Regatta (((u'Optimist', 'SRM.Boat_Class'), u'1107', u'AUT', u'', 'SRM.Boat'), ((u'Himmelfahrt', (('finish', u'2008/05/01'), ('start', u'2008/05/01')), 'SRM.Regatta_Event'), (u'Optimist', 'SRM.Boat_Class'), 'SRM.Regatta_C'), 'SRM.Boat_in_Regatta'), new-values = {'last_cid' : '<n>', 'registration_date' : u'<today>', 'skipper' : 5}>
    <Modify SRM.Sailor ((u'Tanzer', u'Christian', u'', u'', 'PAP.Person'), u'AUT', u'29676', u'', 'SRM.Sailor'), old-values = {'club' : 2, 'last_cid' : '<n>'}, new-values = {'club' : u'', 'last_cid' : '<n>'}>
    <Destroy SRM.Club (u'SC-AMS', 'SRM.Club'), old-values = {'last_cid' : '<n>'}>
        <Modify SRM.Sailor ((u'Tanzer', u'Christian', u'', u'', 'PAP.Person'), u'AUT', u'29676', u'', 'SRM.Sailor'), old-values = {'club' : 2, 'last_cid' : '<n>'}, new-values = {'club' : u'', 'last_cid' : '<n>'}>

    >>> s.destroy ()

    >>> cl_revived  ### after second destroy
    <Destroyed entity SRM.Club (u'scams')>
    >>> s  ### after second destroy
    <Destroyed entity SRM.Sailor ((u'tanzer', u'christian', u'', u''), u'AUT', 29676, u'')>

    >>> for c in scope.uncommitted_changes : ### after second destroy
    ...     show_change (c)
    <Destroy SRM.Club (u'SC-AMS', 'SRM.Club'), old-values = {'last_cid' : '<n>'}>
        <Modify SRM.Sailor ((u'Tanzer', u'Christian', u'', u'', 'PAP.Person'), u'AUT', u'29676', u'', 'SRM.Sailor'), old-values = {'club' : 2, 'last_cid' : '<n>'}, new-values = {'club' : u'', 'last_cid' : '<n>'}>
    <Destroy SRM.Sailor ((u'Tanzer', u'Christian', u'', u'', 'PAP.Person'), u'AUT', u'29676', u'', 'SRM.Sailor'), old-values = {'last_cid' : '<n>'}>
        <Destroy SRM.Boat_in_Regatta (((u'Optimist', 'SRM.Boat_Class'), u'1107', u'AUT', u'', 'SRM.Boat'), ((u'Himmelfahrt', (('finish', u'2008/05/01'), ('start', u'2008/05/01')), 'SRM.Regatta_Event'), (u'Optimist', 'SRM.Boat_Class'), 'SRM.Regatta_C'), 'SRM.Boat_in_Regatta'), old-values = {'last_cid' : '<n>', 'registration_date' : u'<today>', 'skipper' : 5}>
    >>> print (sorted (scope.MOM.Id_Entity.query ().attr ("pid"))) ### 4
    [1, 3, 4, 6, 7]

    >>> scope.rollback ()   ### second rollback

    >>> cl  ### after second rollback
    SRM.Club (u'scams')
    >>> s   ### after second rollback
    SRM.Sailor ((u'tanzer', u'christian', u'', u''), u'AUT', 29676, (u'scams', ))

    >>> for c in scope.uncommitted_changes : ### after second rollback
    ...     show_change (c)


    >>> for _e in scope.MOM.Id_Entity.query_s () : ### 5
    ...    print (_e.pid, _e.as_code ())
    (6, u"SRM.Regatta_Event (u'himmelfahrt', (u'2008/05/01', u'2008/05/01'), )")
    (7, u"SRM.Regatta_C ((u'himmelfahrt', (u'2008/05/01', u'2008/05/01')), (u'optimist', ), is_cancelled = 'no')")
    (1, u"SRM.Boat_Class (u'optimist', max_crew = 1)")
    (3, u"SRM.Boat ((u'optimist', ), 1107, u'AUT', u'', )")
    (8, u'SRM.Boat_in_Regatta (((u\'optimist\', ), 1107, u\'AUT\', u\'\'), ((u\'himmelfahrt\', (u\'2008/05/01\', u\'2008/05/01\')), (u\'optimist\', )), skipper = ((u"u\'tanzer\'", u"u\'christian\'", u"u\'\'", u"u\'\'"), u"u\'AUT\'", u\'29676\', (u"u\'scams\'",)))')
    (2, u"SRM.Club (u'scams', )")
    (4, u"PAP.Person (u'tanzer', u'christian', u'', u'', )")
    (5, u"SRM.Sailor ((u'tanzer', u'christian', u'', u''), u'AUT', 29676, (u'scams', ), )")

    >>> print (sorted (scope.MOM.Id_Entity.query ().attr ("pid"))) ### 6
    [1, 2, 3, 4, 5, 6, 7, 8]


"""

from   _GTW.__test__.model import *
from   _TFL.predicate      import first
from   _TFL.Regexp         import Multi_Re_Replacer, Re_Replacer, re
from   datetime            import datetime

_clean_change = Multi_Re_Replacer \
    ( Re_Replacer
        ( r"u'%s'" % (datetime.now ().strftime("%Y/%m/%d"), )
        , r"u'<today>'"
        )
    , Re_Replacer
        ( r"'last_cid' : '\d+'"
        , r"'last_cid' : '<n>'"
        )
    )

def clean_change (c) :
    result = str (c)
    result = _clean_change (result)
    return result
# end def clean_change

def show_change (c) :
    print clean_change (c)
# end def show_changes

def show_dep (x) :
    if x and x.dependencies :
        for k, v in sorted (x.dependencies.iteritems (), key = TFL.Getter [0].ui_display) :
            print k, ":", v
    else :
        print "---"

def show_ora (x) :
    if x and x.object_referring_attributes :
        for k, vs in sorted (x.object_referring_attributes.iteritems ()) :
            print k, ":", ", ".join (str (v) for v in vs)
    else :
        print "---"

def undo_changes (scope, changes) :
    for c in changes :
        c.undo (scope)
# end def undo_change

__test__ = Scaffold.create_test_dict \
    ( dict
        ( normal        = _test_code
        , delayed       = _test_delayed
        , polymorph     = _test_polymorph
        , qr_grouped_by = _test_qr_grouped_by
        , ref_int       = _test_referential_integrity
        , undo          = _test_undo
        )
    )

### __END__ GTW.__test__.Boat_in_Regatta
