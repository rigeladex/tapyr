# -*- coding: iso-8859-15 -*-
# Copyright (C) 2012 Mag. Christian Tanzer All rights reserved
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
#    GTW.__test__.Page_uv
#
# Purpose
#    Test Page subtypes.
#
# Revision Dates
#    30-Jan-2012 (CT) Creation
#    19-Mar-2012 (CT) Adapt to factoring of `PAP.Subject`
#    19-Mar-2012 (CT) Adapt to reification of `SRM.Handicap`
#    ««revision-date»»···
#--

from   __future__  import absolute_import, division, print_function, unicode_literals

_test_code = r"""
    >>> scope = Scaffold.scope (%(p1)s, %(n1)s) # doctest:+ELLIPSIS
    Creating new scope MOMT__...
    >>> SWP = scope.SWP

    >>> SWP.Page_U ("foo", text = "U")
    GTW.OMP.SWP.Page_U (u'foo')
    >>> SWP.Page_U.query_s (perma_name = "foo").all ()
    [GTW.OMP.SWP.Page_U (u'foo')]
    >>> SWP.Page_V.query_s (perma_name = "foo").all ()
    []
    >>> SWP.Page.query_s (perma_name = "foo").all ()
    [GTW.OMP.SWP.Page_U (u'foo')]

    >>> SWP.Page_V ("foo", text = "V")
    Traceback (most recent call last):
      ...
    Name_Clash: new definition of GTW.OMP.SWP.Page_V (u'foo') clashes with existing GTW.OMP.SWP.Page_U (u'foo')
    >>> SWP.Page_U.query_s (perma_name = "foo").all ()
    [GTW.OMP.SWP.Page_U (u'foo')]
    >>> SWP.Page_V.query_s (perma_name = "foo").all ()
    []
    >>> SWP.Page.query_s (perma_name = "foo").all ()
    [GTW.OMP.SWP.Page_U (u'foo')]

    >>> SWP.Page_V ("bar", text = "V")
    GTW.OMP.SWP.Page_V (u'bar')
    >>> SWP.Page_U.query_s ().all ()
    [GTW.OMP.SWP.Page_U (u'foo')]
    >>> SWP.Page_V.query_s ().all ()
    [GTW.OMP.SWP.Page_V (u'bar')]
    >>> SWP.Page.query_s ().all ()
    [GTW.OMP.SWP.Page_V (u'bar'), GTW.OMP.SWP.Page_U (u'foo')]

    >>> fmt = "%%(type_name)-45s  %%(polymorphic_epk)-5s  %%(epk_sig)s"
    >>> rets = list (et for et in scope.app_type._T_Extension if et.PNS != MOM and et.is_relevant)
    >>> rets = sorted (rets, key = TFL.Sorted_By ("epk_sig", "type_name"))
    >>> for et in rets :
    ...     print (fmt %% TFL.Caller.Object_Scope (et))
    GTW.OMP.PAP.Email                              False  ('address',)
    GTW.OMP.PAP.Phone                              False  ('country_code', 'area_code', 'number')
    GTW.OMP.PAP.Person                             False  ('last_name', 'first_name', 'middle_name', 'title')
    GTW.OMP.Auth.Account_Activation                False  ('left',)
    GTW.OMP.Auth.Account_Password_Change_Required  False  ('left',)
    GTW.OMP.EVT.Recurrence_Spec                    False  ('left',)
    GTW.OMP.SRM.Regatta                            False  ('left', 'boat_class')
    GTW.OMP.SRM.Regatta_C                          False  ('left', 'boat_class')
    GTW.OMP.SRM.Regatta_H                          False  ('left', 'boat_class')
    GTW.OMP.EVT.Event_occurs                       False  ('left', 'date', 'time')
    GTW.OMP.EVT.Event                              False  ('left', 'date', 'time', 'calendar')
    GTW.OMP.SWP.Clip_O                             False  ('left', 'date_x')
    GTW.OMP.EVT.Recurrence_Rule                    False  ('left', 'is_exception', 'desc')
    GTW.OMP.SRM.Team                               False  ('left', 'name')
    GTW.OMP.SRM.Sailor                             False  ('left', 'nation', 'mna_number', 'club')
    GTW.OMP.SRM.Boat                               False  ('left', 'nation', 'sail_number', 'sail_number_x')
    GTW.OMP.SWP.Picture                            False  ('left', 'number')
    GTW.OMP.SRM.Race_Result                        False  ('left', 'race')
    GTW.OMP.Auth.Account_in_Group                  False  ('left', 'right')
    GTW.OMP.PAP.Entity_created_by_Person           False  ('left', 'right')
    GTW.OMP.PAP.Person_has_Address                 False  ('left', 'right')
    GTW.OMP.PAP.Person_has_Email                   False  ('left', 'right')
    GTW.OMP.SRM.Boat_in_Regatta                    False  ('left', 'right')
    GTW.OMP.SRM.Crew_Member                        False  ('left', 'right')
    GTW.OMP.SRM.Team_has_Boat_in_Regatta           False  ('left', 'right')
    GTW.OMP.PAP.Person_has_Phone                   False  ('left', 'right', 'extension')
    GTW.OMP.Auth.Account_EMail_Verification        False  ('left', 'token')
    GTW.OMP.Auth.Account_Password_Reset            False  ('left', 'token')
    GTW.OMP.Auth.Account                           False  ('name',)
    GTW.OMP.Auth.Account_Anonymous                 False  ('name',)
    GTW.OMP.Auth.Account_P                         False  ('name',)
    GTW.OMP.Auth.Group                             False  ('name',)
    GTW.OMP.EVT.Calendar                           False  ('name',)
    GTW.OMP.SRM.Boat_Class                         False  ('name',)
    GTW.OMP.SRM.Club                               False  ('name',)
    GTW.OMP.SRM.Handicap                           False  ('name',)
    GTW.OMP.SRM._Boat_Class_                       False  ('name',)
    GTW.OMP.SRM.Regatta_Event                      False  ('name', 'date')
    GTW.OMP.SWP.Clip_X                             True   ('perma_name',)
    GTW.OMP.SWP.Gallery                            False  ('perma_name',)
    GTW.OMP.SWP.Page                               True   ('perma_name',)
    GTW.OMP.SWP.Page_U                             True   ('perma_name',)
    GTW.OMP.SWP.Page_V                             True   ('perma_name',)
    GTW.OMP.SRM.Page                               True   ('perma_name', 'event')
    GTW.OMP.SWP.Page_Y                             True   ('perma_name', 'year')
    GTW.OMP.PAP.Address                            False  ('street', 'zip', 'city', 'country')


    >>> fmt = "%%(type_name)-45s  %%(is_relevant)-5s  %%(polymorphic_epk)-5s  %%(polymorphic_epks)s"
    >>> for et in scope.app_type._T_Extension :
    ...   if et.PNS != MOM :
    ...     print (fmt %% TFL.Caller.Object_Scope (et))
    GTW.OMP.Auth.Entity                            False  False  False
    GTW.OMP.Auth.Object                            False  False  False
    GTW.OMP.Auth.Account                           True   False  False
    GTW.OMP.Auth.Account_Anonymous                 True   False  False
    GTW.OMP.Auth.Account_P                         True   False  False
    GTW.OMP.Auth.Group                             True   False  False
    GTW.OMP.Auth.Account_in_Group                  True   False  False
    GTW.OMP.Auth._Account_Action_                  False  False  False
    GTW.OMP.Auth.Account_Activation                True   False  False
    GTW.OMP.Auth.Account_Password_Change_Required  True   False  False
    GTW.OMP.Auth._Account_Token_Action_            False  False  False
    GTW.OMP.Auth.Account_EMail_Verification        True   False  False
    GTW.OMP.Auth.Account_Password_Reset            True   False  False
    GTW.OMP.EVT.Entity                             False  False  False
    GTW.OMP.EVT.Object                             False  False  False
    GTW.OMP.EVT.Link1                              False  False  False
    GTW.OMP.EVT.Link2                              False  False  False
    GTW.OMP.EVT.Calendar                           True   False  False
    GTW.OMP.PAP.Entity                             False  False  False
    GTW.OMP.PAP.Subject                            False  False  False
    GTW.OMP.PAP.Person                             True   False  False
    GTW.OMP.SWP.Entity                             False  False  False
    GTW.OMP.SWP.Link1                              False  False  False
    GTW.OMP.SWP.Link2                              False  False  False
    GTW.OMP.SWP.Object                             False  False  False
    GTW.OMP.SWP.Object_PN                          False  False  False
    GTW.OMP.SWP.Page_Mixin                         False  False  False
    GTW.OMP.SWP.Page                               True   True   True
    GTW.OMP.SWP.Page_Y                             True   True   True
    GTW.OMP.EVT.Event                              True   False  True
    GTW.OMP.EVT.Event_occurs                       True   False  True
    GTW.OMP.EVT._Recurrence_Mixin_                 False  False  False
    GTW.OMP.EVT.Recurrence_Spec                    True   False  True
    GTW.OMP.EVT.Recurrence_Rule                    True   False  True
    GTW.OMP.PAP.Address                            True   False  False
    GTW.OMP.PAP.Email                              True   False  False
    GTW.OMP.PAP.Phone                              True   False  False
    GTW.OMP.PAP._Person_has_Property_              False  False  False
    GTW.OMP.PAP.Person_has_Address                 True   False  False
    GTW.OMP.PAP.Entity_created_by_Person           True   False  True
    GTW.OMP.PAP.Person_has_Email                   True   False  False
    GTW.OMP.PAP.Person_has_Phone                   True   False  False
    GTW.OMP.SRM.Regatta_Result                     False  False  False
    GTW.OMP.SRM.Entity                             False  False  False
    GTW.OMP.SRM.Link1                              False  False  False
    GTW.OMP.SRM.Link2                              False  False  False
    GTW.OMP.SRM.Object                             False  False  False
    GTW.OMP.SRM._Boat_Class_                       True   False  False
    GTW.OMP.SRM.Boat_Class                         True   False  False
    GTW.OMP.SRM.Handicap                           True   False  False
    GTW.OMP.SRM.Boat                               True   False  False
    GTW.OMP.SRM.Club                               True   False  False
    GTW.OMP.SRM.Regatta_Event                      True   False  False
    GTW.OMP.SWP.Clip_O                             True   False  True
    GTW.OMP.SWP.Clip_X                             True   True   True
    GTW.OMP.SWP.Gallery                            True   False  False
    GTW.OMP.SWP.Picture                            True   False  False
    GTW.OMP.SRM.Page                               True   True   True
    GTW.OMP.SRM.Regatta                            True   False  False
    GTW.OMP.SRM.Regatta_C                          True   False  False
    GTW.OMP.SRM.Regatta_H                          True   False  False
    GTW.OMP.SRM.Sailor                             True   False  False
    GTW.OMP.SRM.Boat_in_Regatta                    True   False  False
    GTW.OMP.SRM.Race_Result                        True   False  False
    GTW.OMP.SRM.Team                               True   False  False
    GTW.OMP.SRM.Crew_Member                        True   False  False
    GTW.OMP.SRM.Team_has_Boat_in_Regatta           True   False  False
    GTW.OMP.SWP.Page_U                             True   True   True
    GTW.OMP.SWP.Page_V                             True   True   True

    >>> fmt = "%%-45s  %%s"
    >>> for et in scope.app_type._T_Extension :
    ...     rr =  et.relevant_root.type_name if et.relevant_root else sorted (getattr (et, "relevant_roots", {}))
    ...     if rr :
    ...         print (fmt %% (et.type_name, rr))
    MOM.Id_Entity                                  ['GTW.OMP.Auth.Account', 'GTW.OMP.Auth.Account_Activation', 'GTW.OMP.Auth.Account_EMail_Verification', 'GTW.OMP.Auth.Account_Password_Change_Required', 'GTW.OMP.Auth.Account_Password_Reset', 'GTW.OMP.Auth.Account_in_Group', 'GTW.OMP.Auth.Group', 'GTW.OMP.EVT.Calendar', 'GTW.OMP.EVT.Event', 'GTW.OMP.EVT.Event_occurs', 'GTW.OMP.EVT.Recurrence_Rule', 'GTW.OMP.EVT.Recurrence_Spec', 'GTW.OMP.PAP.Address', 'GTW.OMP.PAP.Email', 'GTW.OMP.PAP.Entity_created_by_Person', 'GTW.OMP.PAP.Person', 'GTW.OMP.PAP.Person_has_Address', 'GTW.OMP.PAP.Person_has_Email', 'GTW.OMP.PAP.Person_has_Phone', 'GTW.OMP.PAP.Phone', 'GTW.OMP.SRM.Boat', 'GTW.OMP.SRM.Boat_in_Regatta', 'GTW.OMP.SRM.Club', 'GTW.OMP.SRM.Crew_Member', 'GTW.OMP.SRM.Race_Result', 'GTW.OMP.SRM.Regatta', 'GTW.OMP.SRM.Regatta_Event', 'GTW.OMP.SRM.Sailor', 'GTW.OMP.SRM.Team', 'GTW.OMP.SRM.Team_has_Boat_in_Regatta', 'GTW.OMP.SRM._Boat_Class_', 'GTW.OMP.SWP.Clip_O', 'GTW.OMP.SWP.Gallery', 'GTW.OMP.SWP.Page', 'GTW.OMP.SWP.Picture']
    MOM.Link                                       ['GTW.OMP.Auth.Account_Activation', 'GTW.OMP.Auth.Account_EMail_Verification', 'GTW.OMP.Auth.Account_Password_Change_Required', 'GTW.OMP.Auth.Account_Password_Reset', 'GTW.OMP.Auth.Account_in_Group', 'GTW.OMP.EVT.Event', 'GTW.OMP.EVT.Event_occurs', 'GTW.OMP.EVT.Recurrence_Rule', 'GTW.OMP.EVT.Recurrence_Spec', 'GTW.OMP.PAP.Entity_created_by_Person', 'GTW.OMP.PAP.Person_has_Address', 'GTW.OMP.PAP.Person_has_Email', 'GTW.OMP.PAP.Person_has_Phone', 'GTW.OMP.SRM.Boat', 'GTW.OMP.SRM.Boat_in_Regatta', 'GTW.OMP.SRM.Crew_Member', 'GTW.OMP.SRM.Race_Result', 'GTW.OMP.SRM.Regatta', 'GTW.OMP.SRM.Sailor', 'GTW.OMP.SRM.Team', 'GTW.OMP.SRM.Team_has_Boat_in_Regatta', 'GTW.OMP.SWP.Clip_O', 'GTW.OMP.SWP.Picture']
    MOM.Link1                                      ['GTW.OMP.Auth.Account_Activation', 'GTW.OMP.Auth.Account_EMail_Verification', 'GTW.OMP.Auth.Account_Password_Change_Required', 'GTW.OMP.Auth.Account_Password_Reset', 'GTW.OMP.EVT.Event', 'GTW.OMP.EVT.Event_occurs', 'GTW.OMP.EVT.Recurrence_Rule', 'GTW.OMP.EVT.Recurrence_Spec', 'GTW.OMP.SRM.Boat', 'GTW.OMP.SRM.Race_Result', 'GTW.OMP.SRM.Regatta', 'GTW.OMP.SRM.Sailor', 'GTW.OMP.SRM.Team', 'GTW.OMP.SWP.Clip_O', 'GTW.OMP.SWP.Picture']
    MOM._MOM_Link_n_                               ['GTW.OMP.Auth.Account_in_Group', 'GTW.OMP.PAP.Entity_created_by_Person', 'GTW.OMP.PAP.Person_has_Address', 'GTW.OMP.PAP.Person_has_Email', 'GTW.OMP.PAP.Person_has_Phone', 'GTW.OMP.SRM.Boat_in_Regatta', 'GTW.OMP.SRM.Crew_Member', 'GTW.OMP.SRM.Team_has_Boat_in_Regatta']
    MOM.Link2                                      ['GTW.OMP.Auth.Account_in_Group', 'GTW.OMP.PAP.Entity_created_by_Person', 'GTW.OMP.PAP.Person_has_Address', 'GTW.OMP.PAP.Person_has_Email', 'GTW.OMP.PAP.Person_has_Phone', 'GTW.OMP.SRM.Boat_in_Regatta', 'GTW.OMP.SRM.Crew_Member', 'GTW.OMP.SRM.Team_has_Boat_in_Regatta']
    MOM.Object                                     ['GTW.OMP.Auth.Account', 'GTW.OMP.Auth.Group', 'GTW.OMP.EVT.Calendar', 'GTW.OMP.PAP.Address', 'GTW.OMP.PAP.Email', 'GTW.OMP.PAP.Person', 'GTW.OMP.PAP.Phone', 'GTW.OMP.SRM.Club', 'GTW.OMP.SRM.Regatta_Event', 'GTW.OMP.SRM._Boat_Class_', 'GTW.OMP.SWP.Gallery', 'GTW.OMP.SWP.Page']
    MOM.Named_Object                               ['GTW.OMP.Auth.Group']
    GTW.OMP.Auth.Object                            ['GTW.OMP.Auth.Group']
    GTW.OMP.Auth.Account                           GTW.OMP.Auth.Account
    GTW.OMP.Auth.Account_Anonymous                 GTW.OMP.Auth.Account
    GTW.OMP.Auth.Account_P                         GTW.OMP.Auth.Account
    GTW.OMP.Auth.Group                             GTW.OMP.Auth.Group
    GTW.OMP.Auth.Account_in_Group                  GTW.OMP.Auth.Account_in_Group
    GTW.OMP.Auth._Account_Action_                  ['GTW.OMP.Auth.Account_Activation', 'GTW.OMP.Auth.Account_EMail_Verification', 'GTW.OMP.Auth.Account_Password_Change_Required', 'GTW.OMP.Auth.Account_Password_Reset']
    GTW.OMP.Auth.Account_Activation                GTW.OMP.Auth.Account_Activation
    GTW.OMP.Auth.Account_Password_Change_Required  GTW.OMP.Auth.Account_Password_Change_Required
    GTW.OMP.Auth._Account_Token_Action_            ['GTW.OMP.Auth.Account_EMail_Verification', 'GTW.OMP.Auth.Account_Password_Reset']
    GTW.OMP.Auth.Account_EMail_Verification        GTW.OMP.Auth.Account_EMail_Verification
    GTW.OMP.Auth.Account_Password_Reset            GTW.OMP.Auth.Account_Password_Reset
    GTW.OMP.EVT.Object                             ['GTW.OMP.EVT.Calendar']
    GTW.OMP.EVT.Link1                              ['GTW.OMP.EVT.Event', 'GTW.OMP.EVT.Event_occurs', 'GTW.OMP.EVT.Recurrence_Rule', 'GTW.OMP.EVT.Recurrence_Spec']
    GTW.OMP.EVT.Calendar                           GTW.OMP.EVT.Calendar
    GTW.OMP.PAP.Subject                            ['GTW.OMP.PAP.Person']
    GTW.OMP.PAP.Person                             GTW.OMP.PAP.Person
    GTW.OMP.SWP.Link1                              ['GTW.OMP.SWP.Clip_O', 'GTW.OMP.SWP.Picture']
    GTW.OMP.SWP.Object                             ['GTW.OMP.SWP.Gallery', 'GTW.OMP.SWP.Page']
    GTW.OMP.SWP.Object_PN                          ['GTW.OMP.SWP.Gallery', 'GTW.OMP.SWP.Page']
    GTW.OMP.SWP.Page                               GTW.OMP.SWP.Page
    GTW.OMP.SWP.Page_Y                             GTW.OMP.SWP.Page
    GTW.OMP.EVT.Event                              GTW.OMP.EVT.Event
    GTW.OMP.EVT.Event_occurs                       GTW.OMP.EVT.Event_occurs
    GTW.OMP.EVT._Recurrence_Mixin_                 ['GTW.OMP.EVT.Recurrence_Rule', 'GTW.OMP.EVT.Recurrence_Spec']
    GTW.OMP.EVT.Recurrence_Spec                    GTW.OMP.EVT.Recurrence_Spec
    GTW.OMP.EVT.Recurrence_Rule                    GTW.OMP.EVT.Recurrence_Rule
    GTW.OMP.PAP.Address                            GTW.OMP.PAP.Address
    GTW.OMP.PAP.Email                              GTW.OMP.PAP.Email
    GTW.OMP.PAP.Phone                              GTW.OMP.PAP.Phone
    GTW.OMP.PAP._Person_has_Property_              ['GTW.OMP.PAP.Person_has_Address', 'GTW.OMP.PAP.Person_has_Email', 'GTW.OMP.PAP.Person_has_Phone']
    GTW.OMP.PAP.Person_has_Address                 GTW.OMP.PAP.Person_has_Address
    GTW.OMP.PAP.Entity_created_by_Person           GTW.OMP.PAP.Entity_created_by_Person
    GTW.OMP.PAP.Person_has_Email                   GTW.OMP.PAP.Person_has_Email
    GTW.OMP.PAP.Person_has_Phone                   GTW.OMP.PAP.Person_has_Phone
    GTW.OMP.SRM.Link1                              ['GTW.OMP.SRM.Boat', 'GTW.OMP.SRM.Race_Result', 'GTW.OMP.SRM.Regatta', 'GTW.OMP.SRM.Sailor', 'GTW.OMP.SRM.Team']
    GTW.OMP.SRM.Link2                              ['GTW.OMP.SRM.Boat_in_Regatta', 'GTW.OMP.SRM.Crew_Member', 'GTW.OMP.SRM.Team_has_Boat_in_Regatta']
    GTW.OMP.SRM.Object                             ['GTW.OMP.SRM.Club', 'GTW.OMP.SRM.Regatta_Event', 'GTW.OMP.SRM._Boat_Class_']
    GTW.OMP.SRM._Boat_Class_                       GTW.OMP.SRM._Boat_Class_
    GTW.OMP.SRM.Boat_Class                         GTW.OMP.SRM._Boat_Class_
    GTW.OMP.SRM.Handicap                           GTW.OMP.SRM._Boat_Class_
    GTW.OMP.SRM.Boat                               GTW.OMP.SRM.Boat
    GTW.OMP.SRM.Club                               GTW.OMP.SRM.Club
    GTW.OMP.SRM.Regatta_Event                      GTW.OMP.SRM.Regatta_Event
    GTW.OMP.SWP.Clip_O                             GTW.OMP.SWP.Clip_O
    GTW.OMP.SWP.Clip_X                             GTW.OMP.SWP.Page
    GTW.OMP.SWP.Gallery                            GTW.OMP.SWP.Gallery
    GTW.OMP.SWP.Picture                            GTW.OMP.SWP.Picture
    GTW.OMP.SRM.Page                               GTW.OMP.SWP.Page
    GTW.OMP.SRM.Regatta                            GTW.OMP.SRM.Regatta
    GTW.OMP.SRM.Regatta_C                          GTW.OMP.SRM.Regatta
    GTW.OMP.SRM.Regatta_H                          GTW.OMP.SRM.Regatta
    GTW.OMP.SRM.Sailor                             GTW.OMP.SRM.Sailor
    GTW.OMP.SRM.Boat_in_Regatta                    GTW.OMP.SRM.Boat_in_Regatta
    GTW.OMP.SRM.Race_Result                        GTW.OMP.SRM.Race_Result
    GTW.OMP.SRM.Team                               GTW.OMP.SRM.Team
    GTW.OMP.SRM.Crew_Member                        GTW.OMP.SRM.Crew_Member
    GTW.OMP.SRM.Team_has_Boat_in_Regatta           GTW.OMP.SRM.Team_has_Boat_in_Regatta
    GTW.OMP.SWP.Page_U                             GTW.OMP.SWP.Page
    GTW.OMP.SWP.Page_V                             GTW.OMP.SWP.Page

    >>> print (sorted (rr.type_name for rr in scope.relevant_roots))
    ['GTW.OMP.Auth.Account', 'GTW.OMP.Auth.Account_Activation', 'GTW.OMP.Auth.Account_EMail_Verification', 'GTW.OMP.Auth.Account_Password_Change_Required', 'GTW.OMP.Auth.Account_Password_Reset', 'GTW.OMP.Auth.Account_in_Group', 'GTW.OMP.Auth.Group', 'GTW.OMP.EVT.Calendar', 'GTW.OMP.EVT.Event', 'GTW.OMP.EVT.Event_occurs', 'GTW.OMP.EVT.Recurrence_Rule', 'GTW.OMP.EVT.Recurrence_Spec', 'GTW.OMP.PAP.Address', 'GTW.OMP.PAP.Email', 'GTW.OMP.PAP.Entity_created_by_Person', 'GTW.OMP.PAP.Person', 'GTW.OMP.PAP.Person_has_Address', 'GTW.OMP.PAP.Person_has_Email', 'GTW.OMP.PAP.Person_has_Phone', 'GTW.OMP.PAP.Phone', 'GTW.OMP.SRM.Boat', 'GTW.OMP.SRM.Boat_in_Regatta', 'GTW.OMP.SRM.Club', 'GTW.OMP.SRM.Crew_Member', 'GTW.OMP.SRM.Race_Result', 'GTW.OMP.SRM.Regatta', 'GTW.OMP.SRM.Regatta_Event', 'GTW.OMP.SRM.Sailor', 'GTW.OMP.SRM.Team', 'GTW.OMP.SRM.Team_has_Boat_in_Regatta', 'GTW.OMP.SRM._Boat_Class_', 'GTW.OMP.SWP.Clip_O', 'GTW.OMP.SWP.Gallery', 'GTW.OMP.SWP.Page', 'GTW.OMP.SWP.Picture']

    >>> fmt = "%%-45s  %%-20s  %%s"
    >>> for et in rets :
    ...     print (fmt %% (et.type_name, et.epk_sig_root.type_name if et.epk_sig_root is not et else "=", et.epk_sig))
    GTW.OMP.PAP.Email                              =                     ('address',)
    GTW.OMP.PAP.Phone                              =                     ('country_code', 'area_code', 'number')
    GTW.OMP.PAP.Person                             =                     ('last_name', 'first_name', 'middle_name', 'title')
    GTW.OMP.Auth.Account_Activation                =                     ('left',)
    GTW.OMP.Auth.Account_Password_Change_Required  =                     ('left',)
    GTW.OMP.EVT.Recurrence_Spec                    =                     ('left',)
    GTW.OMP.SRM.Regatta                            =                     ('left', 'boat_class')
    GTW.OMP.SRM.Regatta_C                          GTW.OMP.SRM.Regatta   ('left', 'boat_class')
    GTW.OMP.SRM.Regatta_H                          GTW.OMP.SRM.Regatta   ('left', 'boat_class')
    GTW.OMP.EVT.Event_occurs                       =                     ('left', 'date', 'time')
    GTW.OMP.EVT.Event                              =                     ('left', 'date', 'time', 'calendar')
    GTW.OMP.SWP.Clip_O                             =                     ('left', 'date_x')
    GTW.OMP.EVT.Recurrence_Rule                    =                     ('left', 'is_exception', 'desc')
    GTW.OMP.SRM.Team                               =                     ('left', 'name')
    GTW.OMP.SRM.Sailor                             =                     ('left', 'nation', 'mna_number', 'club')
    GTW.OMP.SRM.Boat                               =                     ('left', 'nation', 'sail_number', 'sail_number_x')
    GTW.OMP.SWP.Picture                            =                     ('left', 'number')
    GTW.OMP.SRM.Race_Result                        =                     ('left', 'race')
    GTW.OMP.Auth.Account_in_Group                  =                     ('left', 'right')
    GTW.OMP.PAP.Entity_created_by_Person           =                     ('left', 'right')
    GTW.OMP.PAP.Person_has_Address                 =                     ('left', 'right')
    GTW.OMP.PAP.Person_has_Email                   =                     ('left', 'right')
    GTW.OMP.SRM.Boat_in_Regatta                    =                     ('left', 'right')
    GTW.OMP.SRM.Crew_Member                        =                     ('left', 'right')
    GTW.OMP.SRM.Team_has_Boat_in_Regatta           =                     ('left', 'right')
    GTW.OMP.PAP.Person_has_Phone                   =                     ('left', 'right', 'extension')
    GTW.OMP.Auth.Account_EMail_Verification        =                     ('left', 'token')
    GTW.OMP.Auth.Account_Password_Reset            =                     ('left', 'token')
    GTW.OMP.Auth.Account                           =                     ('name',)
    GTW.OMP.Auth.Account_Anonymous                 GTW.OMP.Auth.Account  ('name',)
    GTW.OMP.Auth.Account_P                         GTW.OMP.Auth.Account  ('name',)
    GTW.OMP.Auth.Group                             =                     ('name',)
    GTW.OMP.EVT.Calendar                           =                     ('name',)
    GTW.OMP.SRM.Boat_Class                         GTW.OMP.SRM._Boat_Class_  ('name',)
    GTW.OMP.SRM.Club                               =                     ('name',)
    GTW.OMP.SRM.Handicap                           GTW.OMP.SRM._Boat_Class_  ('name',)
    GTW.OMP.SRM._Boat_Class_                       =                     ('name',)
    GTW.OMP.SRM.Regatta_Event                      =                     ('name', 'date')
    GTW.OMP.SWP.Clip_X                             GTW.OMP.SWP.Page      ('perma_name',)
    GTW.OMP.SWP.Gallery                            =                     ('perma_name',)
    GTW.OMP.SWP.Page                               =                     ('perma_name',)
    GTW.OMP.SWP.Page_U                             GTW.OMP.SWP.Page      ('perma_name',)
    GTW.OMP.SWP.Page_V                             GTW.OMP.SWP.Page      ('perma_name',)
    GTW.OMP.SRM.Page                               =                     ('perma_name', 'event')
    GTW.OMP.SWP.Page_Y                             =                     ('perma_name', 'year')
    GTW.OMP.PAP.Address                            =                     ('street', 'zip', 'city', 'country')

    >>> scope.destroy ()

"""

from _GTW.__test__.model import *
from   _TFL.predicate        import any_true

_Ancestor_Essence = GTW.OMP.SWP.Page

class Page_U (_Ancestor_Essence) :
    """Page of type U"""

    ui_name = "Page U"

# end class Page_U

class Page_V (_Ancestor_Essence) :
    """Page of type V"""

    ui_name = "Page V"

# end class Page_V

__test__ = Scaffold.create_test_dict \
    ( dict
        ( normal  = _test_code
        )
    )

### __END__ GTW.__test__.Page_uv
