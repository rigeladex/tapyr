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
#    GTW.__test__.Id_Entity_Link
#
# Purpose
#    Test how generic links to object without a relevant root work,
#
# Revision Dates
#    27-Oct-2010 (MG) Creation
#    29-Mar-2012 (CT) Add test for `link_map`
#     4-Jun-2012 (MG) Test for query with order_by added
#     6-Jun-2012 (CT) Add test for `Entity_created_by_Person.sort_key`
#    12-Jun-2012 (CT) Add `date` to get deterministic output
#     3-Aug-2012 (CT) Add tests for `Ref_Req_Map` and `Ref_Opt_Map`
#     3-Aug-2012 (CT) Use `Ref_Req_Map`, not `link_map`
#    12-Sep-2012 (RS) Add `Id_Entity`
#    ««revision-date»»···
#--

test_code = r"""
    >>> scope = Scaffold.scope (%(p1)s, %(n1)s) # doctest:+ELLIPSIS
    Creating new scope MOMT__...

    >>> date = (("start", "2012/06/10"), )
    >>> PAP  = scope.PAP
    >>> SWP  = scope.SWP
    >>> per  = PAP.Person ("ln", "fn")
    >>> pa1  = SWP.Page   ("title_1", text = "text 1", date = date, raw = True)
    >>> pa2  = SWP.Page   ("title_2", text = "text 2", date = date, raw = True)
    >>> pa3  = SWP.Page   ("title_3", text = "text 3", date = date, raw = True)
    >>> scope.commit     ()

    >>> PAP.Entity_created_by_Person (pa1, per)
    PAP.Entity_created_by_Person ((u'title_1', ), (u'ln', u'fn', u'', u''))
    >>> scope.commit ()

    >>> PAP.Entity_created_by_Person (pa3, per)
    PAP.Entity_created_by_Person ((u'title_3', ), (u'ln', u'fn', u'', u''))
    >>> scope.commit ()

    >>> PAP.Entity_created_by_Person (pa2.epk_raw, per.epk_raw, raw = True)
    PAP.Entity_created_by_Person ((u'title_2', ), (u'ln', u'fn', u'', u''))
    >>> scope.commit ()

    >>> EcP = scope.PAP.Entity_created_by_Person
    >>> q  = EcP.query   ()
    >>> qs = EcP.query_s ()
    >>> q.order_by (Q.pid).all ()
    [PAP.Entity_created_by_Person ((u'title_1', ), (u'ln', u'fn', u'', u'')), PAP.Entity_created_by_Person ((u'title_3', ), (u'ln', u'fn', u'', u'')), PAP.Entity_created_by_Person ((u'title_2', ), (u'ln', u'fn', u'', u''))]
    >>> q.order_by (TFL.Sorted_By ("pid")).all ()
    [PAP.Entity_created_by_Person ((u'title_1', ), (u'ln', u'fn', u'', u'')), PAP.Entity_created_by_Person ((u'title_3', ), (u'ln', u'fn', u'', u'')), PAP.Entity_created_by_Person ((u'title_2', ), (u'ln', u'fn', u'', u''))]

    >>> q.order_by (EcP.sorted_by).all ()
    [PAP.Entity_created_by_Person ((u'title_1', ), (u'ln', u'fn', u'', u'')), PAP.Entity_created_by_Person ((u'title_2', ), (u'ln', u'fn', u'', u'')), PAP.Entity_created_by_Person ((u'title_3', ), (u'ln', u'fn', u'', u''))]

    >>> qs.all ()
    [PAP.Entity_created_by_Person ((u'title_1', ), (u'ln', u'fn', u'', u'')), PAP.Entity_created_by_Person ((u'title_2', ), (u'ln', u'fn', u'', u'')), PAP.Entity_created_by_Person ((u'title_3', ), (u'ln', u'fn', u'', u''))]

    >>> q = scope.query_changes (type_name = "SWP.Page").order_by (Q.cid)
    >>> for c in q.all () :
    ...     print c
    <Create SWP.Page (u'title_1', 'SWP.Page'), new-values = {'contents' : u'<p>text 1</p>\n', 'date' : (('start', u'2012/06/10'),), 'last_cid' : '2', 'text' : u'text 1'}>
    <Create SWP.Page (u'title_2', 'SWP.Page'), new-values = {'contents' : u'<p>text 2</p>\n', 'date' : (('start', u'2012/06/10'),), 'last_cid' : '3', 'text' : u'text 2'}>
    <Create SWP.Page (u'title_3', 'SWP.Page'), new-values = {'contents' : u'<p>text 3</p>\n', 'date' : (('start', u'2012/06/10'),), 'last_cid' : '4', 'text' : u'text 3'}>

    >>> scope.MOM.Id_Entity.query ().order_by (Q.pid).attrs ("tn_pid").all ()
    [(('PAP.Person', 1),), (('SWP.Page', 2),), (('SWP.Page', 3),), (('SWP.Page', 4),), (('PAP.Entity_created_by_Person', 5),), (('PAP.Entity_created_by_Person', 6),), (('PAP.Entity_created_by_Person', 7),)]

    >>> show_ref_maps (scope, "Ref_Req_Map")
    MOM.Id_Entity
        ('PAP.Entity_created_by_Person', ['left'])
    MOM.Link
        ('PAP.Entity_created_by_Person', ['left'])
    MOM.Link1
        ('PAP.Entity_created_by_Person', ['left'])
    MOM._MOM_Link_n_
        ('PAP.Entity_created_by_Person', ['left'])
    MOM.Link2
        ('PAP.Entity_created_by_Person', ['left'])
    MOM.Link2_Ordered
        ('PAP.Entity_created_by_Person', ['left'])
    MOM.Link3
        ('PAP.Entity_created_by_Person', ['left'])
    MOM.Object
        ('PAP.Entity_created_by_Person', ['left'])
    MOM.Named_Object
        ('PAP.Entity_created_by_Person', ['left'])
    Auth.Link1
        ('PAP.Entity_created_by_Person', ['left'])
    Auth.Link2
        ('PAP.Entity_created_by_Person', ['left'])
    Auth.Link2_Ordered
        ('PAP.Entity_created_by_Person', ['left'])
    Auth.Link3
        ('PAP.Entity_created_by_Person', ['left'])
    Auth.Object
        ('PAP.Entity_created_by_Person', ['left'])
    Auth.Id_Entity
        ('PAP.Entity_created_by_Person', ['left'])
    Auth.Named_Object
        ('PAP.Entity_created_by_Person', ['left'])
    Auth.Account
        ('Auth.Account_Activation', ['left'])
        ('Auth.Account_EMail_Verification', ['left'])
        ('Auth.Account_Password_Change_Required', ['left'])
        ('Auth.Account_Password_Reset', ['left'])
        ('Auth.Account_in_Group', ['left'])
        ('PAP.Entity_created_by_Person', ['left'])
    Auth.Account_Anonymous
        ('Auth.Account_Activation', ['left'])
        ('Auth.Account_EMail_Verification', ['left'])
        ('Auth.Account_Password_Change_Required', ['left'])
        ('Auth.Account_Password_Reset', ['left'])
    Auth.Account_P
        ('Auth.Account_Activation', ['left'])
        ('Auth.Account_EMail_Verification', ['left'])
        ('Auth.Account_Password_Change_Required', ['left'])
        ('Auth.Account_Password_Reset', ['left'])
        ('Auth.Account_in_Group', ['left'])
        ('PAP.Entity_created_by_Person', ['left'])
    Auth.Group
        ('Auth.Account_in_Group', ['right'])
        ('PAP.Entity_created_by_Person', ['left'])
    Auth.Account_in_Group
        ('PAP.Entity_created_by_Person', ['left'])
    Auth._Account_Action_
        ('PAP.Entity_created_by_Person', ['left'])
    Auth.Account_Activation
        ('PAP.Entity_created_by_Person', ['left'])
    Auth.Account_Password_Change_Required
        ('PAP.Entity_created_by_Person', ['left'])
    Auth._Account_Token_Action_
        ('PAP.Entity_created_by_Person', ['left'])
    Auth.Account_EMail_Verification
        ('PAP.Entity_created_by_Person', ['left'])
    Auth.Account_Password_Reset
        ('PAP.Entity_created_by_Person', ['left'])
    EVT.Link1
        ('PAP.Entity_created_by_Person', ['left'])
    EVT.Link2
        ('PAP.Entity_created_by_Person', ['left'])
    EVT.Link2_Ordered
        ('PAP.Entity_created_by_Person', ['left'])
    EVT.Link3
        ('PAP.Entity_created_by_Person', ['left'])
    EVT.Object
        ('PAP.Entity_created_by_Person', ['left'])
    EVT.Id_Entity
        ('PAP.Entity_created_by_Person', ['left'])
    EVT.Named_Object
        ('PAP.Entity_created_by_Person', ['left'])
    EVT.Calendar
        ('PAP.Entity_created_by_Person', ['left'])
    PAP.Link1
        ('PAP.Entity_created_by_Person', ['left'])
    PAP.Link2
        ('PAP.Entity_created_by_Person', ['left'])
    PAP.Link2_Ordered
        ('PAP.Entity_created_by_Person', ['left'])
    PAP.Link3
        ('PAP.Entity_created_by_Person', ['left'])
    PAP.Object
        ('PAP.Entity_created_by_Person', ['left'])
    PAP.Id_Entity
        ('PAP.Entity_created_by_Person', ['left'])
    PAP.Named_Object
        ('PAP.Entity_created_by_Person', ['left'])
    PAP.Subject
        ('PAP.Entity_created_by_Person', ['left'])
        ('PAP.Subject_has_Address', ['left'])
        ('PAP.Subject_has_Email', ['left'])
    PAP.Person
        ('PAP.Entity_created_by_Person', ['left', 'right'])
        ('PAP.Person_has_Address', ['left'])
        ('PAP.Person_has_Email', ['left'])
        ('PAP.Person_has_Phone', ['left'])
        ('PAP.Subject_has_Address', ['left'])
        ('PAP.Subject_has_Email', ['left'])
        ('SRM.Sailor', ['left'])
    SWP.Link1
        ('PAP.Entity_created_by_Person', ['left'])
    SWP.Link2
        ('PAP.Entity_created_by_Person', ['left'])
    SWP.Link2_Ordered
        ('PAP.Entity_created_by_Person', ['left'])
    SWP.Link3
        ('PAP.Entity_created_by_Person', ['left'])
    SWP.Object
        ('PAP.Entity_created_by_Person', ['left'])
    SWP.Id_Entity
        ('PAP.Entity_created_by_Person', ['left'])
    SWP.Named_Object
        ('PAP.Entity_created_by_Person', ['left'])
    SWP.Object_PN
        ('PAP.Entity_created_by_Person', ['left'])
        ('SWP.Clip_O', ['left'])
    SWP.Page
        ('EVT.Event', ['left'])
        ('PAP.Entity_created_by_Person', ['left'])
        ('SWP.Clip_O', ['left'])
    SWP.Page_Y
        ('EVT.Event', ['left'])
        ('PAP.Entity_created_by_Person', ['left'])
        ('SWP.Clip_O', ['left'])
    EVT.Event
        ('EVT.Event_occurs', ['left'])
        ('EVT.Recurrence_Spec', ['left'])
        ('PAP.Entity_created_by_Person', ['left'])
    EVT.Event_occurs
        ('PAP.Entity_created_by_Person', ['left'])
    EVT._Recurrence_Mixin_
        ('PAP.Entity_created_by_Person', ['left'])
    EVT.Recurrence_Spec
        ('EVT.Recurrence_Rule', ['left'])
        ('PAP.Entity_created_by_Person', ['left'])
    EVT.Recurrence_Rule
        ('PAP.Entity_created_by_Person', ['left'])
    PAP.Property
        ('PAP.Entity_created_by_Person', ['left'])
    PAP.Address
        ('PAP.Company_has_Address', ['right'])
        ('PAP.Entity_created_by_Person', ['left'])
        ('PAP.Person_has_Address', ['right'])
        ('PAP.Subject_has_Address', ['right'])
    PAP.Company
        ('PAP.Company_has_Address', ['left'])
        ('PAP.Company_has_Email', ['left'])
        ('PAP.Company_has_Phone', ['left'])
        ('PAP.Entity_created_by_Person', ['left'])
        ('PAP.Subject_has_Address', ['left'])
        ('PAP.Subject_has_Email', ['left'])
    PAP.Email
        ('PAP.Company_has_Email', ['right'])
        ('PAP.Entity_created_by_Person', ['left'])
        ('PAP.Person_has_Email', ['right'])
        ('PAP.Subject_has_Email', ['right'])
    PAP.Phone
        ('PAP.Company_has_Phone', ['right'])
        ('PAP.Entity_created_by_Person', ['left'])
        ('PAP.Person_has_Phone', ['right'])
    PAP.Subject_has_Property
        ('PAP.Entity_created_by_Person', ['left'])
    PAP.Subject_has_Phone
        ('PAP.Entity_created_by_Person', ['left'])
    PAP.Subject_has_Address
        ('PAP.Entity_created_by_Person', ['left'])
    PAP.Subject_has_Email
        ('PAP.Entity_created_by_Person', ['left'])
    SRM.Link1
        ('PAP.Entity_created_by_Person', ['left'])
    SRM.Link2
        ('PAP.Entity_created_by_Person', ['left'])
    SRM.Link2_Ordered
        ('PAP.Entity_created_by_Person', ['left'])
    SRM.Link3
        ('PAP.Entity_created_by_Person', ['left'])
    SRM.Object
        ('PAP.Entity_created_by_Person', ['left'])
    SRM.Id_Entity
        ('PAP.Entity_created_by_Person', ['left'])
    SRM.Named_Object
        ('PAP.Entity_created_by_Person', ['left'])
    SRM._Boat_Class_
        ('PAP.Entity_created_by_Person', ['left'])
    SRM.Boat_Class
        ('PAP.Entity_created_by_Person', ['left'])
        ('SRM.Boat', ['left'])
        ('SRM.Regatta_C', ['boat_class'])
    SRM.Handicap
        ('PAP.Entity_created_by_Person', ['left'])
        ('SRM.Regatta_H', ['boat_class'])
    SRM.Boat
        ('PAP.Entity_created_by_Person', ['left'])
        ('SRM.Boat_in_Regatta', ['left'])
    SRM.Club
        ('PAP.Entity_created_by_Person', ['left'])
    SRM.Regatta_Event
        ('PAP.Entity_created_by_Person', ['left'])
        ('SRM.Page', ['event'])
        ('SRM.Regatta_C', ['left'])
        ('SRM.Regatta_H', ['left'])
    SWP.Clip_O
        ('PAP.Entity_created_by_Person', ['left'])
    SWP.Clip_X
        ('EVT.Event', ['left'])
        ('PAP.Entity_created_by_Person', ['left'])
        ('SWP.Clip_O', ['left'])
    SWP.Gallery
        ('PAP.Entity_created_by_Person', ['left'])
        ('SWP.Clip_O', ['left'])
        ('SWP.Picture', ['left'])
    SWP.Picture
        ('PAP.Entity_created_by_Person', ['left'])
    SRM.Page
        ('EVT.Event', ['left'])
        ('PAP.Entity_created_by_Person', ['left'])
        ('SWP.Clip_O', ['left'])
    SRM.Regatta
        ('PAP.Entity_created_by_Person', ['left'])
        ('SRM.Boat_in_Regatta', ['right'])
    SRM.Regatta_C
        ('PAP.Entity_created_by_Person', ['left'])
        ('SRM.Boat_in_Regatta', ['right'])
        ('SRM.Team', ['left'])
    SRM.Regatta_H
        ('PAP.Entity_created_by_Person', ['left'])
        ('SRM.Boat_in_Regatta', ['right'])
    SRM.Sailor
        ('PAP.Entity_created_by_Person', ['left'])
        ('SRM.Boat_in_Regatta', ['skipper'])
        ('SRM.Crew_Member', ['right'])
    SRM.Boat_in_Regatta
        ('PAP.Entity_created_by_Person', ['left'])
        ('SRM.Crew_Member', ['left'])
        ('SRM.Race_Result', ['left'])
        ('SRM.Team_has_Boat_in_Regatta', ['right'])
    SRM.Race_Result
        ('PAP.Entity_created_by_Person', ['left'])
    SRM.Team
        ('PAP.Entity_created_by_Person', ['left'])
        ('SRM.Team_has_Boat_in_Regatta', ['left'])
    SRM.Crew_Member
        ('PAP.Entity_created_by_Person', ['left'])
    SRM.Team_has_Boat_in_Regatta
        ('PAP.Entity_created_by_Person', ['left'])
    PAP.Person_has_Email
        ('PAP.Entity_created_by_Person', ['left'])
    PAP.Company_has_Email
        ('PAP.Entity_created_by_Person', ['left'])
    PAP.Person_has_Address
        ('PAP.Entity_created_by_Person', ['left'])
    PAP.Company_has_Address
        ('PAP.Entity_created_by_Person', ['left'])
    PAP.Person_has_Phone
        ('PAP.Entity_created_by_Person', ['left'])
    PAP.Company_has_Phone
        ('PAP.Entity_created_by_Person', ['left'])

    >>> show_ref_maps (scope, "Ref_Opt_Map")
    EVT.Calendar
        ('EVT.Event', ['calendar'])
    PAP.Person
        ('SRM.Team', ['leader'])
    SRM.Club
        ('SRM.Regatta_Event', ['club'])
        ('SRM.Sailor', ['club'])
        ('SRM.Team', ['club'])

"""

from   _GTW.__test__.model      import *
from   _TFL.Formatter           import formatted_1

__test__ = Scaffold.create_test_dict (test_code)

### __END__ GTW.__test__.Id_Entity_Link
