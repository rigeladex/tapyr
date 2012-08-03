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
#     2-Aug-2012 (MG) New test for `auto_up_depends` attributes added
#    ««revision-date»»···
#--

from   __future__  import absolute_import, division, print_function, unicode_literals

_test_code = r"""
    >>> scope = Scaffold.scope (%(p1)s, %(n1)s) # doctest:+ELLIPSIS
    Creating new scope MOMT__...
    >>> SWP = scope.SWP

    >>> SWP.Page_U ("foo", text = "U")
    SWP.Page_U (u'foo')
    >>> SWP.Page_U.query_s (perma_name = "foo").all ()
    [SWP.Page_U (u'foo')]
    >>> SWP.Page_V.query_s (perma_name = "foo").all ()
    []
    >>> SWP.Page.query_s (perma_name = "foo").all ()
    [SWP.Page_U (u'foo')]

    >>> scope.commit ()
    >>> SWP.Page_V ("foo", text = "V")
    Traceback (most recent call last):
      ...
    Name_Clash: new definition of Page V (u'foo') clashes with existing Page U (u'foo')
    >>> SWP.Page_U.query_s (perma_name = "foo").all ()
    [SWP.Page_U (u'foo')]
    >>> SWP.Page_V.query_s (perma_name = "foo").all ()
    []
    >>> SWP.Page.query_s (perma_name = "foo").all ()
    [SWP.Page_U (u'foo')]

    >>> SWP.Page_V ("bar", text = "V")
    SWP.Page_V (u'bar')
    >>> SWP.Page_U.query_s ().all ()
    [SWP.Page_U (u'foo')]
    >>> SWP.Page_V.query_s ().all ()
    [SWP.Page_V (u'bar')]
    >>> SWP.Page.query_s ().all ()
    [SWP.Page_V (u'bar'), SWP.Page_U (u'foo')]

    >>> fmt = "%%(type_name)-45s  %%(polymorphic_epk)-5s  %%(epk_sig)s"
    >>> rets = list (et for et in scope.app_type._T_Extension if et.PNS != MOM and et.is_relevant)
    >>> rets = sorted (rets, key = TFL.Sorted_By ("epk_sig", "type_name"))
    >>> for et in rets :
    ...     print (fmt %% TFL.Caller.Object_Scope (et))
    PAP.Email                              False  ('address',)
    PAP.Phone                              False  ('country_code', 'area_code', 'number')
    PAP.Person                             False  ('last_name', 'first_name', 'middle_name', 'title')
    Auth.Account_Activation                False  ('left',)
    Auth.Account_Password_Change_Required  False  ('left',)
    EVT.Recurrence_Spec                    False  ('left',)
    SRM.Regatta                            False  ('left', 'boat_class')
    SRM.Regatta_C                          False  ('left', 'boat_class')
    SRM.Regatta_H                          False  ('left', 'boat_class')
    EVT.Event_occurs                       False  ('left', 'date', 'time')
    EVT.Event                              False  ('left', 'date', 'time', 'calendar')
    SWP.Clip_O                             False  ('left', 'date_x')
    EVT.Recurrence_Rule                    False  ('left', 'is_exception', 'desc')
    SRM.Team                               False  ('left', 'name')
    SRM.Sailor                             False  ('left', 'nation', 'mna_number', 'club')
    SRM.Boat                               False  ('left', 'nation', 'sail_number', 'sail_number_x')
    SWP.Picture                            False  ('left', 'number')
    SRM.Race_Result                        False  ('left', 'race')
    Auth.Account_in_Group                  False  ('left', 'right')
    PAP.Company_has_Address                False  ('left', 'right')
    PAP.Company_has_Email                  False  ('left', 'right')
    PAP.Company_has_Phone                  False  ('left', 'right')
    PAP.Entity_created_by_Person           False  ('left', 'right')
    PAP.Person_has_Address                 False  ('left', 'right')
    PAP.Person_has_Email                   False  ('left', 'right')
    SRM.Boat_in_Regatta                    False  ('left', 'right')
    SRM.Crew_Member                        False  ('left', 'right')
    SRM.Team_has_Boat_in_Regatta           False  ('left', 'right')
    PAP.Person_has_Phone                   False  ('left', 'right', 'extension')
    Auth.Account_EMail_Verification        False  ('left', 'token')
    Auth.Account_Password_Reset            False  ('left', 'token')
    Auth.Account                           False  ('name',)
    Auth.Account_Anonymous                 False  ('name',)
    Auth.Account_P                         False  ('name',)
    Auth.Group                             False  ('name',)
    EVT.Calendar                           False  ('name',)
    PAP.Company                            False  ('name',)
    SRM.Boat_Class                         False  ('name',)
    SRM.Club                               False  ('name',)
    SRM.Handicap                           False  ('name',)
    SRM._Boat_Class_                       False  ('name',)
    SRM.Regatta_Event                      False  ('name', 'date')
    SWP.Clip_X                             True   ('perma_name',)
    SWP.Gallery                            False  ('perma_name',)
    SWP.Page                               True   ('perma_name',)
    SWP.Page_U                             True   ('perma_name',)
    SWP.Page_V                             True   ('perma_name',)
    SRM.Page                               True   ('perma_name', 'event')
    SWP.Page_Y                             True   ('perma_name', 'year')
    PAP.Address                            False  ('street', 'zip', 'city', 'country')


    >>> fmt = "%%(type_name)-45s  %%(is_relevant)-5s  %%(polymorphic_epk)-5s  %%(polymorphic_epks)s"
    >>> for i, et in enumerate (scope.app_type._T_Extension) :
    ...   if not i :
    ...     print (fmt %% (dict (type_name = "type_name", is_relevant = "relev", polymorphic_epk = "p_epk", polymorphic_epks = "p_epks")))
    ...     print ("=" * 70)
    ...   if et.PNS != MOM :
    ...     print (fmt %% TFL.Caller.Object_Scope (et))
    type_name                                      relev  p_epk  p_epks
    ======================================================================
    Auth.Entity                                    False  False  False
    Auth.Object                                    False  False  False
    Auth.Account                                   True   False  False
    Auth.Account_Anonymous                         True   False  False
    Auth.Account_P                                 True   False  False
    Auth.Group                                     True   False  False
    Auth.Account_in_Group                          True   False  False
    Auth._Account_Action_                          False  False  False
    Auth.Account_Activation                        True   False  False
    Auth.Account_Password_Change_Required          True   False  False
    Auth._Account_Token_Action_                    False  False  False
    Auth.Account_EMail_Verification                True   False  False
    Auth.Account_Password_Reset                    True   False  False
    EVT.Entity                                     False  False  False
    EVT.Object                                     False  False  False
    EVT.Link1                                      False  False  False
    EVT.Link2                                      False  False  False
    EVT.Calendar                                   True   False  False
    PAP.Entity                                     False  False  False
    PAP.Subject                                    False  False  False
    PAP.Person                                     True   False  False
    SWP.Entity                                     False  False  False
    SWP.Link1                                      False  False  False
    SWP.Link2                                      False  False  False
    SWP.Object                                     False  False  False
    SWP.Object_PN                                  False  False  False
    SWP.Page_Mixin                                 False  False  False
    SWP.Page                                       True   True   True
    SWP.Page_Y                                     True   True   True
    EVT.Event                                      True   False  True
    EVT.Event_occurs                               True   False  True
    EVT._Recurrence_Mixin_                         False  False  False
    EVT.Recurrence_Spec                            True   False  True
    EVT.Recurrence_Rule                            True   False  True
    PAP.Address                                    True   False  False
    PAP.Company                                    True   False  False
    PAP.Email                                      True   False  False
    PAP.Phone                                      True   False  False
    PAP.Subject_has_Property                       False  False  True
    PAP.Subject_has_Address                        False  False  True
    PAP.Company_has_Address                        True   False  False
    PAP.Subject_has_Email                          False  False  True
    PAP.Company_has_Email                          True   False  False
    PAP.Subject_has_Phone                          False  False  True
    PAP.Company_has_Phone                          True   False  False
    PAP.Entity_created_by_Person                   True   False  True
    PAP.Person_has_Address                         True   False  False
    PAP.Person_has_Email                           True   False  False
    PAP.Person_has_Phone                           True   False  False
    SRM.Regatta_Result                             False  False  False
    SRM.Entity                                     False  False  False
    SRM.Link1                                      False  False  False
    SRM.Link2                                      False  False  False
    SRM.Object                                     False  False  False
    SRM._Boat_Class_                               True   False  False
    SRM.Boat_Class                                 True   False  False
    SRM.Handicap                                   True   False  False
    SRM.Boat                                       True   False  False
    SRM.Club                                       True   False  False
    SRM.Regatta_Event                              True   False  False
    SWP.Clip_O                                     True   False  True
    SWP.Clip_X                                     True   True   True
    SWP.Gallery                                    True   False  False
    SWP.Picture                                    True   False  False
    SRM.Page                                       True   True   True
    SRM.Regatta                                    True   False  False
    SRM.Regatta_C                                  True   False  False
    SRM.Regatta_H                                  True   False  False
    SRM.Sailor                                     True   False  False
    SRM.Boat_in_Regatta                            True   False  False
    SRM.Race_Result                                True   False  False
    SRM.Team                                       True   False  False
    SRM.Crew_Member                                True   False  False
    SRM.Team_has_Boat_in_Regatta                   True   False  False
    SWP.Page_U                                     True   True   True
    SWP.Page_V                                     True   True   True

    >>> fmt = "%%-45s  %%s"
    >>> for et in scope.app_type._T_Extension :
    ...     rr =  et.relevant_root.type_name if et.relevant_root else sorted (getattr (et, "relevant_roots", {}))
    ...     if rr :
    ...         print (fmt %% (et.type_name, rr))
    MOM.Id_Entity                                  ['Auth.Account', 'Auth.Account_Activation', 'Auth.Account_EMail_Verification', 'Auth.Account_Password_Change_Required', 'Auth.Account_Password_Reset', 'Auth.Account_in_Group', 'Auth.Group', 'EVT.Calendar', 'EVT.Event', 'EVT.Event_occurs', 'EVT.Recurrence_Rule', 'EVT.Recurrence_Spec', 'PAP.Address', 'PAP.Company', 'PAP.Company_has_Address', 'PAP.Company_has_Email', 'PAP.Company_has_Phone', 'PAP.Email', 'PAP.Entity_created_by_Person', 'PAP.Person', 'PAP.Person_has_Address', 'PAP.Person_has_Email', 'PAP.Person_has_Phone', 'PAP.Phone', 'SRM.Boat', 'SRM.Boat_in_Regatta', 'SRM.Club', 'SRM.Crew_Member', 'SRM.Race_Result', 'SRM.Regatta', 'SRM.Regatta_Event', 'SRM.Sailor', 'SRM.Team', 'SRM.Team_has_Boat_in_Regatta', 'SRM._Boat_Class_', 'SWP.Clip_O', 'SWP.Gallery', 'SWP.Page', 'SWP.Picture']
    MOM.Link                                       ['Auth.Account_Activation', 'Auth.Account_EMail_Verification', 'Auth.Account_Password_Change_Required', 'Auth.Account_Password_Reset', 'Auth.Account_in_Group', 'EVT.Event', 'EVT.Event_occurs', 'EVT.Recurrence_Rule', 'EVT.Recurrence_Spec', 'PAP.Company_has_Address', 'PAP.Company_has_Email', 'PAP.Company_has_Phone', 'PAP.Entity_created_by_Person', 'PAP.Person_has_Address', 'PAP.Person_has_Email', 'PAP.Person_has_Phone', 'SRM.Boat', 'SRM.Boat_in_Regatta', 'SRM.Crew_Member', 'SRM.Race_Result', 'SRM.Regatta', 'SRM.Sailor', 'SRM.Team', 'SRM.Team_has_Boat_in_Regatta', 'SWP.Clip_O', 'SWP.Picture']
    MOM.Link1                                      ['Auth.Account_Activation', 'Auth.Account_EMail_Verification', 'Auth.Account_Password_Change_Required', 'Auth.Account_Password_Reset', 'EVT.Event', 'EVT.Event_occurs', 'EVT.Recurrence_Rule', 'EVT.Recurrence_Spec', 'SRM.Boat', 'SRM.Race_Result', 'SRM.Regatta', 'SRM.Sailor', 'SRM.Team', 'SWP.Clip_O', 'SWP.Picture']
    MOM._MOM_Link_n_                               ['Auth.Account_in_Group', 'PAP.Company_has_Address', 'PAP.Company_has_Email', 'PAP.Company_has_Phone', 'PAP.Entity_created_by_Person', 'PAP.Person_has_Address', 'PAP.Person_has_Email', 'PAP.Person_has_Phone', 'SRM.Boat_in_Regatta', 'SRM.Crew_Member', 'SRM.Team_has_Boat_in_Regatta']
    MOM.Link2                                      ['Auth.Account_in_Group', 'PAP.Company_has_Address', 'PAP.Company_has_Email', 'PAP.Company_has_Phone', 'PAP.Entity_created_by_Person', 'PAP.Person_has_Address', 'PAP.Person_has_Email', 'PAP.Person_has_Phone', 'SRM.Boat_in_Regatta', 'SRM.Crew_Member', 'SRM.Team_has_Boat_in_Regatta']
    MOM.Object                                     ['Auth.Account', 'Auth.Group', 'EVT.Calendar', 'PAP.Address', 'PAP.Company', 'PAP.Email', 'PAP.Person', 'PAP.Phone', 'SRM.Club', 'SRM.Regatta_Event', 'SRM._Boat_Class_', 'SWP.Gallery', 'SWP.Page']
    MOM.Named_Object                               ['Auth.Group']
    Auth.Object                            ['Auth.Group']
    Auth.Account                           Auth.Account
    Auth.Account_Anonymous                 Auth.Account
    Auth.Account_P                         Auth.Account
    Auth.Group                             Auth.Group
    Auth.Account_in_Group                  Auth.Account_in_Group
    Auth._Account_Action_                  ['Auth.Account_Activation', 'Auth.Account_EMail_Verification', 'Auth.Account_Password_Change_Required', 'Auth.Account_Password_Reset']
    Auth.Account_Activation                Auth.Account_Activation
    Auth.Account_Password_Change_Required  Auth.Account_Password_Change_Required
    Auth._Account_Token_Action_            ['Auth.Account_EMail_Verification', 'Auth.Account_Password_Reset']
    Auth.Account_EMail_Verification        Auth.Account_EMail_Verification
    Auth.Account_Password_Reset            Auth.Account_Password_Reset
    EVT.Object                             ['EVT.Calendar']
    EVT.Link1                              ['EVT.Event', 'EVT.Event_occurs', 'EVT.Recurrence_Rule', 'EVT.Recurrence_Spec']
    EVT.Calendar                           EVT.Calendar
    PAP.Subject                            ['PAP.Company', 'PAP.Person']
    PAP.Person                             PAP.Person
    SWP.Link1                              ['SWP.Clip_O', 'SWP.Picture']
    SWP.Object                             ['SWP.Gallery', 'SWP.Page']
    SWP.Object_PN                          ['SWP.Gallery', 'SWP.Page']
    SWP.Page                               SWP.Page
    SWP.Page_Y                             SWP.Page
    EVT.Event                              EVT.Event
    EVT.Event_occurs                       EVT.Event_occurs
    EVT._Recurrence_Mixin_                 ['EVT.Recurrence_Rule', 'EVT.Recurrence_Spec']
    EVT.Recurrence_Spec                    EVT.Recurrence_Spec
    EVT.Recurrence_Rule                    EVT.Recurrence_Rule
    PAP.Address                            PAP.Address
    PAP.Company                            PAP.Company
    PAP.Email                              PAP.Email
    PAP.Phone                              PAP.Phone
    PAP.Subject_has_Property               ['PAP.Company_has_Address', 'PAP.Company_has_Email', 'PAP.Company_has_Phone', 'PAP.Person_has_Address', 'PAP.Person_has_Email', 'PAP.Person_has_Phone']
    PAP.Subject_has_Address                ['PAP.Company_has_Address', 'PAP.Person_has_Address']
    PAP.Company_has_Address                PAP.Company_has_Address
    PAP.Subject_has_Email                  ['PAP.Company_has_Email', 'PAP.Person_has_Email']
    PAP.Company_has_Email                  PAP.Company_has_Email
    PAP.Subject_has_Phone                  ['PAP.Company_has_Phone', 'PAP.Person_has_Phone']
    PAP.Company_has_Phone                  PAP.Company_has_Phone
    PAP.Entity_created_by_Person           PAP.Entity_created_by_Person
    PAP.Person_has_Address                 PAP.Person_has_Address
    PAP.Person_has_Email                   PAP.Person_has_Email
    PAP.Person_has_Phone                   PAP.Person_has_Phone
    SRM.Link1                              ['SRM.Boat', 'SRM.Race_Result', 'SRM.Regatta', 'SRM.Sailor', 'SRM.Team']
    SRM.Link2                              ['SRM.Boat_in_Regatta', 'SRM.Crew_Member', 'SRM.Team_has_Boat_in_Regatta']
    SRM.Object                             ['SRM.Club', 'SRM.Regatta_Event', 'SRM._Boat_Class_']
    SRM._Boat_Class_                       SRM._Boat_Class_
    SRM.Boat_Class                         SRM._Boat_Class_
    SRM.Handicap                           SRM._Boat_Class_
    SRM.Boat                               SRM.Boat
    SRM.Club                               SRM.Club
    SRM.Regatta_Event                      SRM.Regatta_Event
    SWP.Clip_O                             SWP.Clip_O
    SWP.Clip_X                             SWP.Page
    SWP.Gallery                            SWP.Gallery
    SWP.Picture                            SWP.Picture
    SRM.Page                               SWP.Page
    SRM.Regatta                            SRM.Regatta
    SRM.Regatta_C                          SRM.Regatta
    SRM.Regatta_H                          SRM.Regatta
    SRM.Sailor                             SRM.Sailor
    SRM.Boat_in_Regatta                    SRM.Boat_in_Regatta
    SRM.Race_Result                        SRM.Race_Result
    SRM.Team                               SRM.Team
    SRM.Crew_Member                        SRM.Crew_Member
    SRM.Team_has_Boat_in_Regatta           SRM.Team_has_Boat_in_Regatta
    SWP.Page_U                             SWP.Page
    SWP.Page_V                             SWP.Page

    >>> print (sorted (rr.type_name for rr in scope.relevant_roots))
    ['Auth.Account', 'Auth.Account_Activation', 'Auth.Account_EMail_Verification', 'Auth.Account_Password_Change_Required', 'Auth.Account_Password_Reset', 'Auth.Account_in_Group', 'Auth.Group', 'EVT.Calendar', 'EVT.Event', 'EVT.Event_occurs', 'EVT.Recurrence_Rule', 'EVT.Recurrence_Spec', 'PAP.Address', 'PAP.Company', 'PAP.Company_has_Address', 'PAP.Company_has_Email', 'PAP.Company_has_Phone', 'PAP.Email', 'PAP.Entity_created_by_Person', 'PAP.Person', 'PAP.Person_has_Address', 'PAP.Person_has_Email', 'PAP.Person_has_Phone', 'PAP.Phone', 'SRM.Boat', 'SRM.Boat_in_Regatta', 'SRM.Club', 'SRM.Crew_Member', 'SRM.Race_Result', 'SRM.Regatta', 'SRM.Regatta_Event', 'SRM.Sailor', 'SRM.Team', 'SRM.Team_has_Boat_in_Regatta', 'SRM._Boat_Class_', 'SWP.Clip_O', 'SWP.Gallery', 'SWP.Page', 'SWP.Picture']

    >>> fmt = "%%-45s  %%-20s  %%s"
    >>> for et in rets :
    ...     print (fmt %% (et.type_name, et.epk_sig_root.type_name if et.epk_sig_root is not et else "=", et.epk_sig))
    PAP.Email                              =                     ('address',)
    PAP.Phone                              =                     ('country_code', 'area_code', 'number')
    PAP.Person                             =                     ('last_name', 'first_name', 'middle_name', 'title')
    Auth.Account_Activation                =                     ('left',)
    Auth.Account_Password_Change_Required  =                     ('left',)
    EVT.Recurrence_Spec                    =                     ('left',)
    SRM.Regatta                            =                     ('left', 'boat_class')
    SRM.Regatta_C                          SRM.Regatta   ('left', 'boat_class')
    SRM.Regatta_H                          SRM.Regatta   ('left', 'boat_class')
    EVT.Event_occurs                       =                     ('left', 'date', 'time')
    EVT.Event                              =                     ('left', 'date', 'time', 'calendar')
    SWP.Clip_O                             =                     ('left', 'date_x')
    EVT.Recurrence_Rule                    =                     ('left', 'is_exception', 'desc')
    SRM.Team                               =                     ('left', 'name')
    SRM.Sailor                             =                     ('left', 'nation', 'mna_number', 'club')
    SRM.Boat                               =                     ('left', 'nation', 'sail_number', 'sail_number_x')
    SWP.Picture                            =                     ('left', 'number')
    SRM.Race_Result                        =                     ('left', 'race')
    Auth.Account_in_Group                  =                     ('left', 'right')
    PAP.Company_has_Address                =                     ('left', 'right')
    PAP.Company_has_Email                  =                     ('left', 'right')
    PAP.Company_has_Phone                  =                     ('left', 'right')
    PAP.Entity_created_by_Person           =                     ('left', 'right')
    PAP.Person_has_Address                 =                     ('left', 'right')
    PAP.Person_has_Email                   =                     ('left', 'right')
    SRM.Boat_in_Regatta                    =                     ('left', 'right')
    SRM.Crew_Member                        =                     ('left', 'right')
    SRM.Team_has_Boat_in_Regatta           =                     ('left', 'right')
    PAP.Person_has_Phone                   =                     ('left', 'right', 'extension')
    Auth.Account_EMail_Verification        =                     ('left', 'token')
    Auth.Account_Password_Reset            =                     ('left', 'token')
    Auth.Account                           =                     ('name',)
    Auth.Account_Anonymous                 Auth.Account  ('name',)
    Auth.Account_P                         Auth.Account  ('name',)
    Auth.Group                             =                     ('name',)
    EVT.Calendar                           =                     ('name',)
    PAP.Company                            =                     ('name',)
    SRM.Boat_Class                         SRM._Boat_Class_  ('name',)
    SRM.Club                               =                     ('name',)
    SRM.Handicap                           SRM._Boat_Class_  ('name',)
    SRM._Boat_Class_                       =                     ('name',)
    SRM.Regatta_Event                      =                     ('name', 'date')
    SWP.Clip_X                             SWP.Page      ('perma_name',)
    SWP.Gallery                            =                     ('perma_name',)
    SWP.Page                               =                     ('perma_name',)
    SWP.Page_U                             SWP.Page      ('perma_name',)
    SWP.Page_V                             SWP.Page      ('perma_name',)
    SRM.Page                               =                     ('perma_name', 'event')
    SWP.Page_Y                             =                     ('perma_name', 'year')
    PAP.Address                            =                     ('street', 'zip', 'city', 'country')

    >>> scope.destroy ()

"""

_auto_update = r"""
    >>> scope = Scaffold.scope (%(p1)s, %(n1)s) # doctest:+ELLIPSIS
    Creating new scope MOMT__...
    >>> SWP = scope.SWP

    >>> p = SWP.Page (perma_name = "p1", text = "First text")
    >>> p.text, p.contents
    (u'First text', u'<p>First text</p>\n')

    >>> p.set (text = "New Text")
    2
    >>> p.text, p.contents
    (u'New Text', u'<p>New Text</p>\n')

    >>> scope.commit ()

    >>> if hasattr (scope.ems.session, "expunge") : scope.ems.session.expunge ()
    >>> p = SWP.Page.query ().first ()
    >>> p.text, p.contents
    (u'New Text', u'<p>New Text</p>\n')
"""

from _GTW.__test__.model import *
from   _TFL.predicate    import any_true

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
        ( normal      = _test_code
        , auto_update = _auto_update
        )
    )

### __END__ GTW.__test__.Page_uv
