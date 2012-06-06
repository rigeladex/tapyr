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
#    ««revision-date»»···
#--

test_code = r"""
    >>> scope = Scaffold.scope (%(p1)s, %(n1)s) # doctest:+ELLIPSIS
    Creating new scope MOMT__...

    >>> PAP = scope.PAP
    >>> SWP = scope.SWP
    >>> per = PAP.Person           ("ln", "fn")
    >>> pa1 = SWP.Page             ("title_1", text = "text 1")
    >>> pa2 = SWP.Page             ("title_2", text = "text 2")
    >>> pa3 = SWP.Page             ("title_3", text = "text 3")
    >>> scope.commit               ()

    >>> PAP.Entity_created_by_Person (pa1, per)
    GTW.OMP.PAP.Entity_created_by_Person ((u'title_1', ), (u'ln', u'fn', u'', u''))
    >>> scope.commit ()

    >>> PAP.Entity_created_by_Person (pa3, per)
    GTW.OMP.PAP.Entity_created_by_Person ((u'title_3', ), (u'ln', u'fn', u'', u''))
    >>> scope.commit ()

    >>> PAP.Entity_created_by_Person (pa2.epk_raw, per.epk_raw, raw = True)
    GTW.OMP.PAP.Entity_created_by_Person ((u'title_2', ), (u'ln', u'fn', u'', u''))
    >>> scope.commit ()

    >>> for T in scope.app_type._T_Extension :
    ...   if hasattr (T, "link_map") :
    ...     print T.type_name
    ...     print (formatted (sorted (c.type_name for c in T.link_map), level = 1))
    MOM.Id_Entity
    [ 'GTW.OMP.PAP.Entity_created_by_Person' ]
    MOM.Link
    [ 'GTW.OMP.PAP.Entity_created_by_Person' ]
    MOM.Link1
    [ 'GTW.OMP.PAP.Entity_created_by_Person' ]
    MOM._MOM_Link_n_
    [ 'GTW.OMP.PAP.Entity_created_by_Person' ]
    MOM.Link2
    [ 'GTW.OMP.PAP.Entity_created_by_Person' ]
    MOM.Link2_Ordered
    [ 'GTW.OMP.PAP.Entity_created_by_Person' ]
    MOM.Link3
    [ 'GTW.OMP.PAP.Entity_created_by_Person' ]
    MOM.Object
    [ 'GTW.OMP.PAP.Entity_created_by_Person' ]
    MOM.Named_Object
    [ 'GTW.OMP.PAP.Entity_created_by_Person' ]
    GTW.OMP.Auth.Object
    [ 'GTW.OMP.PAP.Entity_created_by_Person' ]
    GTW.OMP.Auth.Account
      [ 'GTW.OMP.Auth.Account_Activation'
      , 'GTW.OMP.Auth.Account_EMail_Verification'
      , 'GTW.OMP.Auth.Account_Password_Change_Required'
      , 'GTW.OMP.Auth.Account_Password_Reset'
      , 'GTW.OMP.Auth.Account_in_Group'
      , 'GTW.OMP.PAP.Entity_created_by_Person'
      ]
    GTW.OMP.Auth.Account_Anonymous
      [ 'GTW.OMP.Auth.Account_Activation'
      , 'GTW.OMP.Auth.Account_EMail_Verification'
      , 'GTW.OMP.Auth.Account_Password_Change_Required'
      , 'GTW.OMP.Auth.Account_Password_Reset'
      , 'GTW.OMP.Auth.Account_in_Group'
      , 'GTW.OMP.PAP.Entity_created_by_Person'
      ]
    GTW.OMP.Auth.Account_P
      [ 'GTW.OMP.Auth.Account_Activation'
      , 'GTW.OMP.Auth.Account_EMail_Verification'
      , 'GTW.OMP.Auth.Account_Password_Change_Required'
      , 'GTW.OMP.Auth.Account_Password_Reset'
      , 'GTW.OMP.Auth.Account_in_Group'
      , 'GTW.OMP.PAP.Entity_created_by_Person'
      ]
    GTW.OMP.Auth.Group
      [ 'GTW.OMP.Auth.Account_in_Group'
      , 'GTW.OMP.PAP.Entity_created_by_Person'
      ]
    GTW.OMP.Auth.Account_in_Group
    [ 'GTW.OMP.PAP.Entity_created_by_Person' ]
    GTW.OMP.Auth._Account_Action_
    [ 'GTW.OMP.PAP.Entity_created_by_Person' ]
    GTW.OMP.Auth.Account_Activation
    [ 'GTW.OMP.PAP.Entity_created_by_Person' ]
    GTW.OMP.Auth.Account_Password_Change_Required
    [ 'GTW.OMP.PAP.Entity_created_by_Person' ]
    GTW.OMP.Auth._Account_Token_Action_
    [ 'GTW.OMP.PAP.Entity_created_by_Person' ]
    GTW.OMP.Auth.Account_EMail_Verification
    [ 'GTW.OMP.PAP.Entity_created_by_Person' ]
    GTW.OMP.Auth.Account_Password_Reset
    [ 'GTW.OMP.PAP.Entity_created_by_Person' ]
    GTW.OMP.EVT.Object
    [ 'GTW.OMP.PAP.Entity_created_by_Person' ]
    GTW.OMP.EVT.Link1
    [ 'GTW.OMP.PAP.Entity_created_by_Person' ]
    GTW.OMP.EVT.Link2
    [ 'GTW.OMP.PAP.Entity_created_by_Person' ]
    GTW.OMP.EVT.Calendar
    [ 'GTW.OMP.PAP.Entity_created_by_Person' ]
    GTW.OMP.PAP.Subject
    [ 'GTW.OMP.PAP.Entity_created_by_Person' ]
    GTW.OMP.PAP.Person
      [ 'GTW.OMP.PAP.Entity_created_by_Person'
      , 'GTW.OMP.PAP.Person_has_Address'
      , 'GTW.OMP.PAP.Person_has_Email'
      , 'GTW.OMP.PAP.Person_has_Phone'
      , 'GTW.OMP.SRM.Sailor'
      ]
    GTW.OMP.SWP.Link1
    [ 'GTW.OMP.PAP.Entity_created_by_Person' ]
    GTW.OMP.SWP.Link2
    [ 'GTW.OMP.PAP.Entity_created_by_Person' ]
    GTW.OMP.SWP.Object
    [ 'GTW.OMP.PAP.Entity_created_by_Person' ]
    GTW.OMP.SWP.Object_PN
      [ 'GTW.OMP.PAP.Entity_created_by_Person'
      , 'GTW.OMP.SWP.Clip_O'
      ]
    GTW.OMP.SWP.Page
      [ 'GTW.OMP.EVT.Event'
      , 'GTW.OMP.PAP.Entity_created_by_Person'
      , 'GTW.OMP.SWP.Clip_O'
      ]
    GTW.OMP.SWP.Page_Y
      [ 'GTW.OMP.EVT.Event'
      , 'GTW.OMP.PAP.Entity_created_by_Person'
      , 'GTW.OMP.SWP.Clip_O'
      ]
    GTW.OMP.EVT.Event
      [ 'GTW.OMP.EVT.Event_occurs'
      , 'GTW.OMP.EVT.Recurrence_Spec'
      , 'GTW.OMP.PAP.Entity_created_by_Person'
      ]
    GTW.OMP.EVT.Event_occurs
    [ 'GTW.OMP.PAP.Entity_created_by_Person' ]
    GTW.OMP.EVT._Recurrence_Mixin_
    [ 'GTW.OMP.PAP.Entity_created_by_Person' ]
    GTW.OMP.EVT.Recurrence_Spec
      [ 'GTW.OMP.EVT.Recurrence_Rule'
      , 'GTW.OMP.PAP.Entity_created_by_Person'
      ]
    GTW.OMP.EVT.Recurrence_Rule
    [ 'GTW.OMP.PAP.Entity_created_by_Person' ]
    GTW.OMP.PAP.Address
      [ 'GTW.OMP.PAP.Company_has_Address'
      , 'GTW.OMP.PAP.Entity_created_by_Person'
      , 'GTW.OMP.PAP.Person_has_Address'
      ]
    GTW.OMP.PAP.Company
      [ 'GTW.OMP.PAP.Company_has_Address'
      , 'GTW.OMP.PAP.Company_has_Email'
      , 'GTW.OMP.PAP.Company_has_Phone'
      , 'GTW.OMP.PAP.Entity_created_by_Person'
      ]
    GTW.OMP.PAP.Email
      [ 'GTW.OMP.PAP.Company_has_Email'
      , 'GTW.OMP.PAP.Entity_created_by_Person'
      , 'GTW.OMP.PAP.Person_has_Email'
      ]
    GTW.OMP.PAP.Phone
      [ 'GTW.OMP.PAP.Company_has_Phone'
      , 'GTW.OMP.PAP.Entity_created_by_Person'
      , 'GTW.OMP.PAP.Person_has_Phone'
      ]
    GTW.OMP.PAP.Subject_has_Property
    [ 'GTW.OMP.PAP.Entity_created_by_Person' ]
    GTW.OMP.PAP.Subject_has_Address
    [ 'GTW.OMP.PAP.Entity_created_by_Person' ]
    GTW.OMP.PAP.Company_has_Address
    [ 'GTW.OMP.PAP.Entity_created_by_Person' ]
    GTW.OMP.PAP.Subject_has_Email
    [ 'GTW.OMP.PAP.Entity_created_by_Person' ]
    GTW.OMP.PAP.Company_has_Email
    [ 'GTW.OMP.PAP.Entity_created_by_Person' ]
    GTW.OMP.PAP.Subject_has_Phone
    [ 'GTW.OMP.PAP.Entity_created_by_Person' ]
    GTW.OMP.PAP.Company_has_Phone
    [ 'GTW.OMP.PAP.Entity_created_by_Person' ]
    GTW.OMP.PAP.Entity_created_by_Person
    [ 'GTW.OMP.PAP.Entity_created_by_Person' ]
    GTW.OMP.PAP.Person_has_Address
    [ 'GTW.OMP.PAP.Entity_created_by_Person' ]
    GTW.OMP.PAP.Person_has_Email
    [ 'GTW.OMP.PAP.Entity_created_by_Person' ]
    GTW.OMP.PAP.Person_has_Phone
    [ 'GTW.OMP.PAP.Entity_created_by_Person' ]
    GTW.OMP.SRM.Link1
    [ 'GTW.OMP.PAP.Entity_created_by_Person' ]
    GTW.OMP.SRM.Link2
    [ 'GTW.OMP.PAP.Entity_created_by_Person' ]
    GTW.OMP.SRM.Object
    [ 'GTW.OMP.PAP.Entity_created_by_Person' ]
    GTW.OMP.SRM._Boat_Class_
    [ 'GTW.OMP.PAP.Entity_created_by_Person' ]
    GTW.OMP.SRM.Boat_Class
      [ 'GTW.OMP.PAP.Entity_created_by_Person'
      , 'GTW.OMP.SRM.Boat'
      ]
    GTW.OMP.SRM.Handicap
    [ 'GTW.OMP.PAP.Entity_created_by_Person' ]
    GTW.OMP.SRM.Boat
      [ 'GTW.OMP.PAP.Entity_created_by_Person'
      , 'GTW.OMP.SRM.Boat_in_Regatta'
      ]
    GTW.OMP.SRM.Club
    [ 'GTW.OMP.PAP.Entity_created_by_Person' ]
    GTW.OMP.SRM.Regatta_Event
      [ 'GTW.OMP.PAP.Entity_created_by_Person'
      , 'GTW.OMP.SRM.Regatta_C'
      , 'GTW.OMP.SRM.Regatta_H'
      ]
    GTW.OMP.SWP.Clip_O
    [ 'GTW.OMP.PAP.Entity_created_by_Person' ]
    GTW.OMP.SWP.Clip_X
      [ 'GTW.OMP.EVT.Event'
      , 'GTW.OMP.PAP.Entity_created_by_Person'
      , 'GTW.OMP.SWP.Clip_O'
      ]
    GTW.OMP.SWP.Gallery
      [ 'GTW.OMP.PAP.Entity_created_by_Person'
      , 'GTW.OMP.SWP.Clip_O'
      , 'GTW.OMP.SWP.Picture'
      ]
    GTW.OMP.SWP.Picture
    [ 'GTW.OMP.PAP.Entity_created_by_Person' ]
    GTW.OMP.SRM.Page
      [ 'GTW.OMP.EVT.Event'
      , 'GTW.OMP.PAP.Entity_created_by_Person'
      , 'GTW.OMP.SWP.Clip_O'
      ]
    GTW.OMP.SRM.Regatta
      [ 'GTW.OMP.PAP.Entity_created_by_Person'
      , 'GTW.OMP.SRM.Boat_in_Regatta'
      ]
    GTW.OMP.SRM.Regatta_C
      [ 'GTW.OMP.PAP.Entity_created_by_Person'
      , 'GTW.OMP.SRM.Boat_in_Regatta'
      , 'GTW.OMP.SRM.Team'
      ]
    GTW.OMP.SRM.Regatta_H
      [ 'GTW.OMP.PAP.Entity_created_by_Person'
      , 'GTW.OMP.SRM.Boat_in_Regatta'
      ]
    GTW.OMP.SRM.Sailor
      [ 'GTW.OMP.PAP.Entity_created_by_Person'
      , 'GTW.OMP.SRM.Crew_Member'
      ]
    GTW.OMP.SRM.Boat_in_Regatta
      [ 'GTW.OMP.PAP.Entity_created_by_Person'
      , 'GTW.OMP.SRM.Crew_Member'
      , 'GTW.OMP.SRM.Race_Result'
      , 'GTW.OMP.SRM.Team_has_Boat_in_Regatta'
      ]
    GTW.OMP.SRM.Race_Result
    [ 'GTW.OMP.PAP.Entity_created_by_Person' ]
    GTW.OMP.SRM.Team
      [ 'GTW.OMP.PAP.Entity_created_by_Person'
      , 'GTW.OMP.SRM.Team_has_Boat_in_Regatta'
      ]
    GTW.OMP.SRM.Crew_Member
    [ 'GTW.OMP.PAP.Entity_created_by_Person' ]
    GTW.OMP.SRM.Team_has_Boat_in_Regatta
    [ 'GTW.OMP.PAP.Entity_created_by_Person' ]

    >>> EcP = scope.PAP.Entity_created_by_Person
    >>> q  = EcP.query   ()
    >>> qs = EcP.query_s ()
    >>> q.order_by (Q.pid).all ()
    [GTW.OMP.PAP.Entity_created_by_Person ((u'title_1', ), (u'ln', u'fn', u'', u'')), GTW.OMP.PAP.Entity_created_by_Person ((u'title_3', ), (u'ln', u'fn', u'', u'')), GTW.OMP.PAP.Entity_created_by_Person ((u'title_2', ), (u'ln', u'fn', u'', u''))]
    >>> q.order_by (TFL.Sorted_By ("pid")).all ()
    [GTW.OMP.PAP.Entity_created_by_Person ((u'title_1', ), (u'ln', u'fn', u'', u'')), GTW.OMP.PAP.Entity_created_by_Person ((u'title_3', ), (u'ln', u'fn', u'', u'')), GTW.OMP.PAP.Entity_created_by_Person ((u'title_2', ), (u'ln', u'fn', u'', u''))]

    >>> q.order_by (EcP.sorted_by).all ()
    [GTW.OMP.PAP.Entity_created_by_Person ((u'title_1', ), (u'ln', u'fn', u'', u'')), GTW.OMP.PAP.Entity_created_by_Person ((u'title_2', ), (u'ln', u'fn', u'', u'')), GTW.OMP.PAP.Entity_created_by_Person ((u'title_3', ), (u'ln', u'fn', u'', u''))]
    >>> q.order_by (EcP.sort_key).all ()
    [GTW.OMP.PAP.Entity_created_by_Person ((u'title_1', ), (u'ln', u'fn', u'', u'')), GTW.OMP.PAP.Entity_created_by_Person ((u'title_2', ), (u'ln', u'fn', u'', u'')), GTW.OMP.PAP.Entity_created_by_Person ((u'title_3', ), (u'ln', u'fn', u'', u''))]

    >>> qs.all ()
    [GTW.OMP.PAP.Entity_created_by_Person ((u'title_1', ), (u'ln', u'fn', u'', u'')), GTW.OMP.PAP.Entity_created_by_Person ((u'title_2', ), (u'ln', u'fn', u'', u'')), GTW.OMP.PAP.Entity_created_by_Person ((u'title_3', ), (u'ln', u'fn', u'', u''))]

"""

from   _GTW.__test__.model      import *
from   _TFL.Formatter           import Formatter

formatted = Formatter (width = 240)

__test__ = Scaffold.create_test_dict (test_code)

### __END__ GTW.__test__.Id_Entity_Link
