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

    >>> for T in scope.app_type._T_Extension :
    ...   if hasattr (T, "link_map") :
    ...     print T.type_name
    ...     print (formatted (sorted (c.type_name for c in T.link_map), level = 1))
    MOM.Id_Entity
    [ 'PAP.Entity_created_by_Person' ]
    MOM.Link
    [ 'PAP.Entity_created_by_Person' ]
    MOM.Link1
    [ 'PAP.Entity_created_by_Person' ]
    MOM._MOM_Link_n_
    [ 'PAP.Entity_created_by_Person' ]
    MOM.Link2
    [ 'PAP.Entity_created_by_Person' ]
    MOM.Link2_Ordered
    [ 'PAP.Entity_created_by_Person' ]
    MOM.Link3
    [ 'PAP.Entity_created_by_Person' ]
    MOM.Object
    [ 'PAP.Entity_created_by_Person' ]
    MOM.Named_Object
    [ 'PAP.Entity_created_by_Person' ]
    Auth.Object
    [ 'PAP.Entity_created_by_Person' ]
    Auth.Account
      [ 'Auth.Account_Activation'
      , 'Auth.Account_EMail_Verification'
      , 'Auth.Account_Password_Change_Required'
      , 'Auth.Account_Password_Reset'
      , 'Auth.Account_in_Group'
      , 'PAP.Entity_created_by_Person'
      ]
    Auth.Account_Anonymous
      [ 'Auth.Account_Activation'
      , 'Auth.Account_EMail_Verification'
      , 'Auth.Account_Password_Change_Required'
      , 'Auth.Account_Password_Reset'
      , 'Auth.Account_in_Group'
      , 'PAP.Entity_created_by_Person'
      ]
    Auth.Account_P
      [ 'Auth.Account_Activation'
      , 'Auth.Account_EMail_Verification'
      , 'Auth.Account_Password_Change_Required'
      , 'Auth.Account_Password_Reset'
      , 'Auth.Account_in_Group'
      , 'PAP.Entity_created_by_Person'
      ]
    Auth.Group
      [ 'Auth.Account_in_Group'
      , 'PAP.Entity_created_by_Person'
      ]
    Auth.Account_in_Group
    [ 'PAP.Entity_created_by_Person' ]
    Auth._Account_Action_
    [ 'PAP.Entity_created_by_Person' ]
    Auth.Account_Activation
    [ 'PAP.Entity_created_by_Person' ]
    Auth.Account_Password_Change_Required
    [ 'PAP.Entity_created_by_Person' ]
    Auth._Account_Token_Action_
    [ 'PAP.Entity_created_by_Person' ]
    Auth.Account_EMail_Verification
    [ 'PAP.Entity_created_by_Person' ]
    Auth.Account_Password_Reset
    [ 'PAP.Entity_created_by_Person' ]
    EVT.Object
    [ 'PAP.Entity_created_by_Person' ]
    EVT.Link1
    [ 'PAP.Entity_created_by_Person' ]
    EVT.Link2
    [ 'PAP.Entity_created_by_Person' ]
    EVT.Calendar
    [ 'PAP.Entity_created_by_Person' ]
    PAP.Subject
    [ 'PAP.Entity_created_by_Person' ]
    PAP.Person
      [ 'PAP.Entity_created_by_Person'
      , 'PAP.Person_has_Address'
      , 'PAP.Person_has_Email'
      , 'PAP.Person_has_Phone'
      , 'SRM.Sailor'
      ]
    SWP.Link1
    [ 'PAP.Entity_created_by_Person' ]
    SWP.Link2
    [ 'PAP.Entity_created_by_Person' ]
    SWP.Object
    [ 'PAP.Entity_created_by_Person' ]
    SWP.Object_PN
      [ 'PAP.Entity_created_by_Person'
      , 'SWP.Clip_O'
      ]
    SWP.Page
      [ 'EVT.Event'
      , 'PAP.Entity_created_by_Person'
      , 'SWP.Clip_O'
      ]
    SWP.Page_Y
      [ 'EVT.Event'
      , 'PAP.Entity_created_by_Person'
      , 'SWP.Clip_O'
      ]
    EVT.Event
      [ 'EVT.Event_occurs'
      , 'EVT.Recurrence_Spec'
      , 'PAP.Entity_created_by_Person'
      ]
    EVT.Event_occurs
    [ 'PAP.Entity_created_by_Person' ]
    EVT._Recurrence_Mixin_
    [ 'PAP.Entity_created_by_Person' ]
    EVT.Recurrence_Spec
      [ 'EVT.Recurrence_Rule'
      , 'PAP.Entity_created_by_Person'
      ]
    EVT.Recurrence_Rule
    [ 'PAP.Entity_created_by_Person' ]
    PAP.Address
      [ 'PAP.Company_has_Address'
      , 'PAP.Entity_created_by_Person'
      , 'PAP.Person_has_Address'
      ]
    PAP.Company
      [ 'PAP.Company_has_Address'
      , 'PAP.Company_has_Email'
      , 'PAP.Company_has_Phone'
      , 'PAP.Entity_created_by_Person'
      ]
    PAP.Email
      [ 'PAP.Company_has_Email'
      , 'PAP.Entity_created_by_Person'
      , 'PAP.Person_has_Email'
      ]
    PAP.Phone
      [ 'PAP.Company_has_Phone'
      , 'PAP.Entity_created_by_Person'
      , 'PAP.Person_has_Phone'
      ]
    PAP.Subject_has_Property
    [ 'PAP.Entity_created_by_Person' ]
    PAP.Subject_has_Address
    [ 'PAP.Entity_created_by_Person' ]
    PAP.Company_has_Address
    [ 'PAP.Entity_created_by_Person' ]
    PAP.Subject_has_Email
    [ 'PAP.Entity_created_by_Person' ]
    PAP.Company_has_Email
    [ 'PAP.Entity_created_by_Person' ]
    PAP.Subject_has_Phone
    [ 'PAP.Entity_created_by_Person' ]
    PAP.Company_has_Phone
    [ 'PAP.Entity_created_by_Person' ]
    PAP.Entity_created_by_Person
    [ 'PAP.Entity_created_by_Person' ]
    PAP.Person_has_Address
    [ 'PAP.Entity_created_by_Person' ]
    PAP.Person_has_Email
    [ 'PAP.Entity_created_by_Person' ]
    PAP.Person_has_Phone
    [ 'PAP.Entity_created_by_Person' ]
    SRM.Link1
    [ 'PAP.Entity_created_by_Person' ]
    SRM.Link2
    [ 'PAP.Entity_created_by_Person' ]
    SRM.Object
    [ 'PAP.Entity_created_by_Person' ]
    SRM._Boat_Class_
    [ 'PAP.Entity_created_by_Person' ]
    SRM.Boat_Class
      [ 'PAP.Entity_created_by_Person'
      , 'SRM.Boat'
      ]
    SRM.Handicap
    [ 'PAP.Entity_created_by_Person' ]
    SRM.Boat
      [ 'PAP.Entity_created_by_Person'
      , 'SRM.Boat_in_Regatta'
      ]
    SRM.Club
    [ 'PAP.Entity_created_by_Person' ]
    SRM.Regatta_Event
      [ 'PAP.Entity_created_by_Person'
      , 'SRM.Regatta_C'
      , 'SRM.Regatta_H'
      ]
    SWP.Clip_O
    [ 'PAP.Entity_created_by_Person' ]
    SWP.Clip_X
      [ 'EVT.Event'
      , 'PAP.Entity_created_by_Person'
      , 'SWP.Clip_O'
      ]
    SWP.Gallery
      [ 'PAP.Entity_created_by_Person'
      , 'SWP.Clip_O'
      , 'SWP.Picture'
      ]
    SWP.Picture
    [ 'PAP.Entity_created_by_Person' ]
    SRM.Page
      [ 'EVT.Event'
      , 'PAP.Entity_created_by_Person'
      , 'SWP.Clip_O'
      ]
    SRM.Regatta
      [ 'PAP.Entity_created_by_Person'
      , 'SRM.Boat_in_Regatta'
      ]
    SRM.Regatta_C
      [ 'PAP.Entity_created_by_Person'
      , 'SRM.Boat_in_Regatta'
      , 'SRM.Team'
      ]
    SRM.Regatta_H
      [ 'PAP.Entity_created_by_Person'
      , 'SRM.Boat_in_Regatta'
      ]
    SRM.Sailor
      [ 'PAP.Entity_created_by_Person'
      , 'SRM.Crew_Member'
      ]
    SRM.Boat_in_Regatta
      [ 'PAP.Entity_created_by_Person'
      , 'SRM.Crew_Member'
      , 'SRM.Race_Result'
      , 'SRM.Team_has_Boat_in_Regatta'
      ]
    SRM.Race_Result
    [ 'PAP.Entity_created_by_Person' ]
    SRM.Team
      [ 'PAP.Entity_created_by_Person'
      , 'SRM.Team_has_Boat_in_Regatta'
      ]
    SRM.Crew_Member
    [ 'PAP.Entity_created_by_Person' ]
    SRM.Team_has_Boat_in_Regatta
    [ 'PAP.Entity_created_by_Person' ]

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
"""

from   _GTW.__test__.model      import *

__test__ = Scaffold.create_test_dict (test_code)

### __END__ GTW.__test__.Id_Entity_Link
