# -*- coding: utf-8 -*-
# Copyright (C) 2013-2014 Mag. Christian Tanzer All rights reserved
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
#    GTW.__test__.SAW_ATW
#
# Purpose
#    Test App_Type_Wrapper of MOM.DBW.SAW
#
# Revision Dates
#    27-Jun-2013 (CT) Creation
#     1-Jul-2013 (CT) Add `test_ancestors`, `test_select`, `test_select_strict`
#     3-Jul-2013 (CT) Add `show_root_table`
#     3-Jul-2013 (CT) Add `test_q_able`
#     5-Jul-2013 (CT) Add test for `select.count ()`, add `test_qc_map`
#     7-Jul-2013 (CT) Add `test_q_result`; add tests to `test_parents`
#     8-Jul-2013 (CT) Add tables of `sequences` to `show_tables`
#     8-Jul-2013 (CT) Add `test_attr_wrappers`
#    10-Jul-2013 (CT) Add `show_attr_mro`
#    11-Jul-2013 (CT) Add tests to `test_q_result`
#    16-Jul-2013 (CT) Add `test_sequences`
#    16-Jul-2013 (CT) Add test for `Q_Result.E_Type_Reload` to `test_q_result`
#    19-Jul-2013 (CT) Add tests for `Q.RAW`
#     4-Aug-2013 (CT) Add `test_date_extraction` for `pg` and `sq`
#    20-Aug-2013 (CT) Exclude `test_q_result` for old sqlalchemy versions
#    25-Aug-2013 (CT) Add `test_q_result_x`
#    26-Aug-2013 (CT) Add `test_key_o_p`; call of `show_sequence`
#    29-Aug-2013 (CT) Add test case for
#                     `Q.person.lifetime == ("2013/07/15", "2013/07/21")`
#    ««revision-date»»···
#--

from   __future__ import division, print_function
from   __future__ import absolute_import, unicode_literals

from   _GTW.__test__.model               import *
from   _GTW.__test__._SAW_test_functions import *
from   _MOM.import_MOM                   import Q

_test_ancestors = """
    >>> apt, url = Scaffold.app_type_and_url (%(p1)s, %(n1)s)

    >>> show_ancestors (apt)
    MOM.Id_Entity
    MOM.MD_Change
    MOM.Link                             < MOM.Id_Entity
    MOM.Link1                            < MOM.Id_Entity
    MOM._MOM_Link_n_                     < MOM.Id_Entity
    MOM.Link2                            < MOM.Id_Entity
    MOM.Link3                            < MOM.Id_Entity
    MOM.Object                           < MOM.Id_Entity
    Auth.Id_Entity                       < MOM.Id_Entity
    Auth.Object                          < MOM.Id_Entity
    Auth._Account_                       < MOM.Id_Entity
    Auth.Account_Anonymous               < Auth._Account_   < MOM.Id_Entity
    Auth.Account                         < Auth._Account_   < MOM.Id_Entity
    MOM.Date_Time_Interval
    MOM.Date_Time_Interval_C
    MOM.Date_Time_Interval_N
    Auth.Certificate                     < MOM.Id_Entity
    Auth.Group                           < MOM.Id_Entity
    Auth.Link                            < MOM.Id_Entity
    Auth._MOM_Link_n_                    < MOM.Id_Entity
    Auth.Link2                           < MOM.Id_Entity
    Auth.Account_in_Group                < MOM.Id_Entity
    Auth.Link1                           < MOM.Id_Entity
    Auth._Account_Action_                < MOM.Id_Entity
    Auth.Account_Activation              < MOM.Id_Entity
    Auth.Account_Password_Change_Required < MOM.Id_Entity
    Auth._Account_Token_Action_          < MOM.Id_Entity
    Auth.Account_EMail_Verification      < MOM.Id_Entity
    Auth.Account_Password_Reset          < MOM.Id_Entity
    EVT.Id_Entity                        < MOM.Id_Entity
    EVT.Object                           < MOM.Id_Entity
    EVT.Calendar                         < MOM.Id_Entity
    MOM.Date_Interval
    MOM.Date_Interval_C
    MOM.Date_Interval_N
    MOM.Time_Interval
    EVT.Link                             < MOM.Id_Entity
    EVT.Link1                            < MOM.Id_Entity
    SWP.Id_Entity                        < MOM.Id_Entity
    SWP.Object                           < MOM.Id_Entity
    SWP.Object_PN                        < MOM.Id_Entity
    SWP.Page_Mixin
    SWP.Page                             < MOM.Id_Entity
    SWP.Page_Y                           < SWP.Page         < MOM.Id_Entity
    EVT.Event                            < MOM.Id_Entity
    EVT.Event_occurs                     < MOM.Id_Entity
    EVT._Recurrence_Mixin_               < MOM.Id_Entity
    EVT.Recurrence_Spec                  < MOM.Id_Entity
    EVT.Recurrence_Rule                  < MOM.Id_Entity
    MOM.Position
    PAP.Id_Entity                        < MOM.Id_Entity
    PAP.Object                           < MOM.Id_Entity
    PAP.Property                         < MOM.Id_Entity
    PAP.Address                          < MOM.Id_Entity
    PAP.Subject                          < MOM.Id_Entity
    PAP.Legal_Entity                     < MOM.Id_Entity
    PAP.Company                          < MOM.Id_Entity
    PAP.Email                            < MOM.Id_Entity
    PAP.Phone                            < MOM.Id_Entity
    PAP.Person                           < MOM.Id_Entity
    PAP.Url                              < MOM.Id_Entity
    PAP.Link                             < MOM.Id_Entity
    PAP.Link1                            < MOM.Id_Entity
    PAP.Address_Position                 < MOM.Id_Entity
    PAP._MOM_Link_n_                     < MOM.Id_Entity
    PAP.Link2                            < MOM.Id_Entity
    PAP.Subject_has_Property             < MOM.Id_Entity
    PAP.Person_has_Account               < MOM.Id_Entity
    SRM.Regatta_Result
    SRM.Id_Entity                        < MOM.Id_Entity
    SRM.Object                           < MOM.Id_Entity
    SRM._Boat_Class_                     < MOM.Id_Entity
    SRM.Boat_Class                       < SRM._Boat_Class_ < MOM.Id_Entity
    SRM.Handicap                         < SRM._Boat_Class_ < MOM.Id_Entity
    SRM.Link                             < MOM.Id_Entity
    SRM.Link1                            < MOM.Id_Entity
    SRM.Boat                             < MOM.Id_Entity
    SRM.Club                             < MOM.Id_Entity
    SRM.Regatta_Event                    < MOM.Id_Entity
    SWP.Link                             < MOM.Id_Entity
    SWP.Link1                            < MOM.Id_Entity
    SWP.Clip_O                           < MOM.Id_Entity
    SWP.Clip_X                           < SWP.Page         < MOM.Id_Entity
    SWP.Gallery                          < MOM.Id_Entity
    MOM.D2_Value_Int
    MOM.D2_Value_Float
    MOM._Pic_
    MOM._Thumb_
    SWP.Picture                          < MOM.Id_Entity
    SRM.Page                             < SWP.Page         < MOM.Id_Entity
    SRM.Regatta                          < MOM.Id_Entity
    SRM.Regatta_C                        < SRM.Regatta      < MOM.Id_Entity
    SRM.Regatta_H                        < SRM.Regatta      < MOM.Id_Entity
    SRM.Sailor                           < MOM.Id_Entity
    SRM._MOM_Link_n_                     < MOM.Id_Entity
    SRM.Link2                            < MOM.Id_Entity
    SRM.Boat_in_Regatta                  < MOM.Id_Entity
    SRM.Race_Result                      < MOM.Id_Entity
    SRM.Team                             < MOM.Id_Entity
    SRM.Crew_Member                      < MOM.Id_Entity
    SRM.Team_has_Boat_in_Regatta         < MOM.Id_Entity
    PAP.Subject_has_Address              < PAP.Subject_has_Property < MOM.Id_Entity
    PAP.Subject_has_Email                < PAP.Subject_has_Property < MOM.Id_Entity
    PAP.Subject_has_Phone                < PAP.Subject_has_Property < MOM.Id_Entity
    PAP.Subject_has_Url                  < PAP.Subject_has_Property < MOM.Id_Entity
    PAP.Company_has_Url                  < PAP.Subject_has_Property < MOM.Id_Entity
    PAP.Person_has_Url                   < PAP.Subject_has_Property < MOM.Id_Entity
    PAP.Company_has_Phone                < PAP.Subject_has_Phone < PAP.Subject_has_Property < MOM.Id_Entity
    PAP.Person_has_Phone                 < PAP.Subject_has_Phone < PAP.Subject_has_Property < MOM.Id_Entity
    PAP.Company_has_Email                < PAP.Subject_has_Property < MOM.Id_Entity
    PAP.Person_has_Email                 < PAP.Subject_has_Property < MOM.Id_Entity
    PAP.Company_has_Address              < PAP.Subject_has_Property < MOM.Id_Entity
    PAP.Person_has_Address               < PAP.Subject_has_Property < MOM.Id_Entity

    >>> show_root_table (apt)
    MOM.Id_Entity                        mom_id_entity
    MOM.MD_Change                        mom_md_change
    MOM.Link                             mom_id_entity
    MOM.Link1                            mom_id_entity
    MOM._MOM_Link_n_                     mom_id_entity
    MOM.Link2                            mom_id_entity
    MOM.Link3                            mom_id_entity
    MOM.Object                           mom_id_entity
    Auth.Id_Entity                       mom_id_entity
    Auth.Object                          mom_id_entity
    Auth._Account_                       mom_id_entity
    Auth.Account_Anonymous               mom_id_entity
    Auth.Account                         mom_id_entity
    MOM.Date_Time_Interval               None
    MOM.Date_Time_Interval_C             None
    MOM.Date_Time_Interval_N             None
    Auth.Certificate                     mom_id_entity
    Auth.Group                           mom_id_entity
    Auth.Link                            mom_id_entity
    Auth._MOM_Link_n_                    mom_id_entity
    Auth.Link2                           mom_id_entity
    Auth.Account_in_Group                mom_id_entity
    Auth.Link1                           mom_id_entity
    Auth._Account_Action_                mom_id_entity
    Auth.Account_Activation              mom_id_entity
    Auth.Account_Password_Change_Required mom_id_entity
    Auth._Account_Token_Action_          mom_id_entity
    Auth.Account_EMail_Verification      mom_id_entity
    Auth.Account_Password_Reset          mom_id_entity
    EVT.Id_Entity                        mom_id_entity
    EVT.Object                           mom_id_entity
    EVT.Calendar                         mom_id_entity
    MOM.Date_Interval                    None
    MOM.Date_Interval_C                  None
    MOM.Date_Interval_N                  None
    MOM.Time_Interval                    None
    EVT.Link                             mom_id_entity
    EVT.Link1                            mom_id_entity
    SWP.Id_Entity                        mom_id_entity
    SWP.Object                           mom_id_entity
    SWP.Object_PN                        mom_id_entity
    SWP.Page_Mixin                       None
    SWP.Page                             mom_id_entity
    SWP.Page_Y                           mom_id_entity
    EVT.Event                            mom_id_entity
    EVT.Event_occurs                     mom_id_entity
    EVT._Recurrence_Mixin_               mom_id_entity
    EVT.Recurrence_Spec                  mom_id_entity
    EVT.Recurrence_Rule                  mom_id_entity
    MOM.Position                         None
    PAP.Id_Entity                        mom_id_entity
    PAP.Object                           mom_id_entity
    PAP.Property                         mom_id_entity
    PAP.Address                          mom_id_entity
    PAP.Subject                          mom_id_entity
    PAP.Legal_Entity                     mom_id_entity
    PAP.Company                          mom_id_entity
    PAP.Email                            mom_id_entity
    PAP.Phone                            mom_id_entity
    PAP.Person                           mom_id_entity
    PAP.Url                              mom_id_entity
    PAP.Link                             mom_id_entity
    PAP.Link1                            mom_id_entity
    PAP.Address_Position                 mom_id_entity
    PAP._MOM_Link_n_                     mom_id_entity
    PAP.Link2                            mom_id_entity
    PAP.Subject_has_Property             mom_id_entity
    PAP.Person_has_Account               mom_id_entity
    SRM.Regatta_Result                   None
    SRM.Id_Entity                        mom_id_entity
    SRM.Object                           mom_id_entity
    SRM._Boat_Class_                     mom_id_entity
    SRM.Boat_Class                       mom_id_entity
    SRM.Handicap                         mom_id_entity
    SRM.Link                             mom_id_entity
    SRM.Link1                            mom_id_entity
    SRM.Boat                             mom_id_entity
    SRM.Club                             mom_id_entity
    SRM.Regatta_Event                    mom_id_entity
    SWP.Link                             mom_id_entity
    SWP.Link1                            mom_id_entity
    SWP.Clip_O                           mom_id_entity
    SWP.Clip_X                           mom_id_entity
    SWP.Gallery                          mom_id_entity
    MOM.D2_Value_Int                     None
    MOM.D2_Value_Float                   None
    MOM._Pic_                            None
    MOM._Thumb_                          None
    SWP.Picture                          mom_id_entity
    SRM.Page                             mom_id_entity
    SRM.Regatta                          mom_id_entity
    SRM.Regatta_C                        mom_id_entity
    SRM.Regatta_H                        mom_id_entity
    SRM.Sailor                           mom_id_entity
    SRM._MOM_Link_n_                     mom_id_entity
    SRM.Link2                            mom_id_entity
    SRM.Boat_in_Regatta                  mom_id_entity
    SRM.Race_Result                      mom_id_entity
    SRM.Team                             mom_id_entity
    SRM.Crew_Member                      mom_id_entity
    SRM.Team_has_Boat_in_Regatta         mom_id_entity
    PAP.Subject_has_Address              mom_id_entity
    PAP.Subject_has_Email                mom_id_entity
    PAP.Subject_has_Phone                mom_id_entity
    PAP.Subject_has_Url                  mom_id_entity
    PAP.Company_has_Url                  mom_id_entity
    PAP.Person_has_Url                   mom_id_entity
    PAP.Company_has_Phone                mom_id_entity
    PAP.Person_has_Phone                 mom_id_entity
    PAP.Company_has_Email                mom_id_entity
    PAP.Person_has_Email                 mom_id_entity
    PAP.Company_has_Address              mom_id_entity
    PAP.Person_has_Address               mom_id_entity


"""

_test_attr_wrappers = """
    >>> apt, url = Scaffold.app_type_and_url (%(p1)s, %(n1)s)

    >>> show_attr_wrappers (apt)
    MOM.Id_Entity
      Kind_Wrapper_R : Rev_Ref `creation`
          Computed, _Rev_Query_, _Cached_, _Volatile_, _System_
      Kind_Wrapper : Boolean `electric`
          Internal, _DB_System_, _DB_Attr_, _System_
      Kind_Wrapper_R : Rev_Ref `last_change`
          Computed, _Rev_Query_, _Cached_, _Volatile_, _System_
      Kind_Wrapper : Int `last_cid`
          Internal, _DB_System_, _DB_Attr_, _System_
      Kind_Wrapper : Surrogate `pid`
          Just_Once_Mixin, Internal, _DB_System_, _DB_Attr_, _System_
      Kind_Wrapper : String `type_name`
          _Type_Name_Mixin_, Internal, _DB_System_, _DB_Attr_, _System_
      Kind_Wrapper : Boolean `x_locked`
          Internal, _DB_System_, _DB_Attr_, _System_
    MOM.MD_Change
      Kind_Date_Time_Wrapper : Date-Time `c_time`
          _Sync_Change_, Internal, _DB_System_, _DB_Attr_, _System_
      Kind_Wrapper_S : Entity `c_user`
          _Id_Entity_Reference_Mixin_, _EPK_Mixin_, _SPK_Mixin_, _Sync_Change_, Internal, _DB_System_, _DB_Attr_, _System_
      Kind_Wrapper : Surrogate `cid`
          Just_Once_Mixin, _Sync_Change_, Internal, _DB_System_, _DB_Attr_, _System_
      Kind_Wrapper : String `kind`
          _Sync_Change_, Internal, _DB_System_, _DB_Attr_, _System_
      Kind_Wrapper_Q : Int `parent`
          Query, _Cached_, _Volatile_, _System_
      Kind_Wrapper : Int `parent_cid`
          _Sync_Change_, Internal, _DB_System_, _DB_Attr_, _System_
      Kind_Wrapper : Int `pid`
          _Sync_Change_, Internal, _DB_System_, _DB_Attr_, _System_
      Kind_Wrapper : Blob `scm_change`
          Internal, _DB_System_, _DB_Attr_, _System_
      Kind_Date_Time_Wrapper : Date-Time `time`
          _Sync_Change_, Internal, _DB_System_, _DB_Attr_, _System_
      Kind_Wrapper : String `type_name`
          _Sync_Change_, Internal, _DB_System_, _DB_Attr_, _System_
      Kind_Wrapper_S : Entity `user`
          _Id_Entity_Reference_Mixin_, _EPK_Mixin_, _SPK_Mixin_, _Sync_Change_, Internal, _DB_System_, _DB_Attr_, _System_
    MOM.Link
      Kind_Wrapper_P : Left `left`
          Link_Role, _EPK_Mixin_, _SPK_Mixin_, Primary, _Required_Mixin_, _Primary_, _User_, _DB_Attr_
    MOM.Link1
      Kind_Wrapper_P : Left `left`
          Init_Only_Mixin, Just_Once_Mixin, Link_Role, _EPK_Mixin_, _SPK_Mixin_, Primary, _Required_Mixin_, _Primary_, _User_, _DB_Attr_
    MOM._MOM_Link_n_
      Kind_Wrapper_P : Left `left`
          Link_Role, _EPK_Mixin_, _SPK_Mixin_, Primary, _Required_Mixin_, _Primary_, _User_, _DB_Attr_
      Kind_Wrapper_P : Right `right`
          Link_Role, _EPK_Mixin_, _SPK_Mixin_, Primary, _Required_Mixin_, _Primary_, _User_, _DB_Attr_
    MOM.Link2
      Kind_Wrapper_P : Left `left`
          Link_Role, _EPK_Mixin_, _SPK_Mixin_, Primary, _Required_Mixin_, _Primary_, _User_, _DB_Attr_
      Kind_Wrapper_P : Right `right`
          Link_Role, _EPK_Mixin_, _SPK_Mixin_, Primary, _Required_Mixin_, _Primary_, _User_, _DB_Attr_
    MOM.Link3
      Kind_Wrapper_P : Left `left`
          Link_Role, _EPK_Mixin_, _SPK_Mixin_, Primary, _Required_Mixin_, _Primary_, _User_, _DB_Attr_
      Kind_Wrapper_P : Middle `middle`
          Link_Role, _EPK_Mixin_, _SPK_Mixin_, Primary, _Required_Mixin_, _Primary_, _User_, _DB_Attr_
      Kind_Wrapper_P : Right `right`
          Link_Role, _EPK_Mixin_, _SPK_Mixin_, Primary, _Required_Mixin_, _Primary_, _User_, _DB_Attr_
    Auth._Account_
      Kind_Wrapper_Q : Boolean `active`
          _Auto_Update_Mixin_, Query, _Cached_, _Volatile_, _System_
      Kind_Wrapper : Boolean `enabled`
          Optional, _User_, _DB_Attr_
      Kind_Wrapper : Email `name`
          Primary, _Required_Mixin_, _Primary_, _User_, _DB_Attr_
      Kind_Wrapper : Boolean `superuser`
          Optional, _User_, _DB_Attr_
      Kind_Wrapper : Boolean `suspended`
          Internal, _DB_System_, _DB_Attr_, _System_
    Auth.Account_Anonymous <-- Auth._Account_
    Auth.Account
      Kind_Wrapper_R : Link_Ref_List `_account_action_s`
          Computed, _Rev_Query_, _Cached_, _Volatile_, _System_
      Kind_Wrapper_R : Link_Ref_List `_account_token_action_s`
          Computed, _Rev_Query_, _Cached_, _Volatile_, _System_
      Kind_Wrapper_R : Link_Ref_List `account_email_verifications`
          Computed, _Rev_Query_, _Cached_, _Volatile_, _System_
      Kind_Wrapper_R : Link_Ref_List `account_password_resets`
          Computed, _Rev_Query_, _Cached_, _Volatile_, _System_
      Kind_Wrapper_R : Link_Ref `activation`
          Computed, _Rev_Query_, _Cached_, _Volatile_, _System_
      Kind_Wrapper_R : Link_Ref_List `activations`
          Computed, _Rev_Query_, _Cached_, _Volatile_, _System_
      Kind_Wrapper_R : Link_Ref_List `group_links`
          Computed, _Rev_Query_, _Cached_, _Volatile_, _System_
      Kind_Wrapper_R : Role_Ref_Set `groups`
          Computed, _Rev_Query_, _Cached_, _Volatile_, _System_
      Kind_Wrapper : String `password`
          Internal, _DB_System_, _DB_Attr_, _System_
      Kind_Wrapper_R : Link_Ref `password_change_required`
          Computed, _Rev_Query_, _Cached_, _Volatile_, _System_
      Kind_Wrapper_R : Link_Ref_List `password_change_requireds`
          Computed, _Rev_Query_, _Cached_, _Volatile_, _System_
      Kind_Wrapper_R : Role_Ref `person`
          Computed, _Rev_Query_, _Cached_, _Volatile_, _System_
      Kind_Wrapper_R : Link_Ref `person_link`
          Computed, _Rev_Query_, _Cached_, _Volatile_, _System_
      Kind_Wrapper_R : Link_Ref_List `person_links`
          Computed, _Rev_Query_, _Cached_, _Volatile_, _System_
      Kind_Wrapper : String `ph_name`
          Sticky_Mixin, _Sticky_Mixin_, Internal, _DB_System_, _DB_Attr_, _System_
    MOM.Date_Time_Interval
      Kind_Wrapper_Q : Boolean `alive`
          _Nested_Mixin_, Computed, Query, _Cached_, _Volatile_, _System_
      Kind_Date_Time_Wrapper : Date-Time `finish`
          _Nested_Mixin_, Optional, _User_, _DB_Attr_
      Kind_Date_Time_Wrapper : Date-Time `start`
          _Nested_Mixin_, Necessary, _User_, _DB_Attr_
    MOM.Date_Time_Interval_C
      Kind_Wrapper_Q : Boolean `alive`
          _Nested_Mixin_, Computed, Query, _Cached_, _Volatile_, _System_
      Kind_Date_Time_Wrapper : Date-Time `finish`
          _Nested_Mixin_, Computed_Set_Mixin, Computed_Mixin, Optional, _User_, _DB_Attr_
      Kind_Date_Time_Wrapper : Date-Time `start`
          _Nested_Mixin_, Necessary, _User_, _DB_Attr_
    MOM.Date_Time_Interval_N
      Kind_Wrapper_Q : Boolean `alive`
          _Nested_Mixin_, Computed, Query, _Cached_, _Volatile_, _System_
      Kind_Date_Time_Wrapper : Date-Time `finish`
          _Nested_Mixin_, Optional, _User_, _DB_Attr_
      Kind_Date_Time_Wrapper : Date-Time `start`
          _Nested_Mixin_, Sticky_Mixin, _Sticky_Mixin_, Necessary, _User_, _DB_Attr_
    Auth.Certificate
      Kind_Wrapper_Q : Boolean `alive`
          Computed, Query, _Cached_, _Volatile_, _System_
      Kind_Wrapper : Surrogate `cert_id`
          Just_Once_Mixin, Internal, _DB_System_, _DB_Attr_, _System_
      Kind_Wrapper : String `desc`
          Primary_Optional, _Sticky_Mixin_, _Primary_D_, _Primary_, _User_, _DB_Attr_
      Kind_Wrapper : Email `email`
          Primary, _Required_Mixin_, _Primary_, _User_, _DB_Attr_
      Kind_Wrapper : None `pem`
          Internal, _DB_System_, _DB_Attr_, _System_
      Kind_Date_Time_Wrapper : Date-Time `revocation_date`
          Optional, _User_, _DB_Attr_
      Kind_Wrapper_C : Date_Time_Interval `validity`
          _Composite_Mixin_, Primary, _Required_Mixin_, _Primary_, _User_, _DB_Attr_
        MOM.Date_Time_Interval
          Kind_Wrapper_Q : Boolean `alive`
              _Nested_Mixin_, Computed, Query, _Cached_, _Volatile_, _System_
          Kind_Date_Time_Wrapper : Date-Time `finish`
              _Nested_Mixin_, Optional, _User_, _DB_Attr_
          Kind_Date_Time_Wrapper : Date-Time `start`
              _Nested_Mixin_, Necessary, _User_, _DB_Attr_
    Auth.Group
      Kind_Wrapper_R : Link_Ref_List `account_links`
          Computed, _Rev_Query_, _Cached_, _Volatile_, _System_
      Kind_Wrapper_R : Role_Ref_Set `accounts`
          Computed, _Rev_Query_, _Cached_, _Volatile_, _System_
      Kind_Wrapper : String `desc`
          Optional, _User_, _DB_Attr_
      Kind_Wrapper : String `name`
          Primary, _Required_Mixin_, _Primary_, _User_, _DB_Attr_
    Auth.Link
      Kind_Wrapper_P : Left `left`
          Link_Role, _EPK_Mixin_, _SPK_Mixin_, Primary, _Required_Mixin_, _Primary_, _User_, _DB_Attr_
    Auth._MOM_Link_n_
      Kind_Wrapper_P : Left `left`
          Link_Role, _EPK_Mixin_, _SPK_Mixin_, Primary, _Required_Mixin_, _Primary_, _User_, _DB_Attr_
      Kind_Wrapper_P : Right `right`
          Link_Role, _EPK_Mixin_, _SPK_Mixin_, Primary, _Required_Mixin_, _Primary_, _User_, _DB_Attr_
    Auth.Link2
      Kind_Wrapper_P : Left `left`
          Link_Role, _EPK_Mixin_, _SPK_Mixin_, Primary, _Required_Mixin_, _Primary_, _User_, _DB_Attr_
      Kind_Wrapper_P : Right `right`
          Link_Role, _EPK_Mixin_, _SPK_Mixin_, Primary, _Required_Mixin_, _Primary_, _User_, _DB_Attr_
    Auth.Account_in_Group
      Kind_Wrapper_S : Account `left`
          Link_Role, _EPK_Mixin_, _SPK_Mixin_, Primary, _Required_Mixin_, _Primary_, _User_, _DB_Attr_
      Kind_Wrapper_S : Group `right`
          Link_Role, _EPK_Mixin_, _SPK_Mixin_, Primary, _Required_Mixin_, _Primary_, _User_, _DB_Attr_
    Auth.Link1
      Kind_Wrapper_P : Left `left`
          Link_Role, _EPK_Mixin_, _SPK_Mixin_, Primary, _Required_Mixin_, _Primary_, _User_, _DB_Attr_
    Auth._Account_Action_
      Kind_Wrapper_P : Account `left`
          Init_Only_Mixin, Just_Once_Mixin, Link_Role, _EPK_Mixin_, _SPK_Mixin_, Primary, _Required_Mixin_, _Primary_, _User_, _DB_Attr_
    Auth.Account_Activation
      Kind_Wrapper_S : Account `left`
          Init_Only_Mixin, Just_Once_Mixin, Link_Role, _EPK_Mixin_, _SPK_Mixin_, Primary, _Required_Mixin_, _Primary_, _User_, _DB_Attr_
    Auth.Account_Password_Change_Required
      Kind_Wrapper_S : Account `left`
          Init_Only_Mixin, Just_Once_Mixin, Link_Role, _EPK_Mixin_, _SPK_Mixin_, Primary, _Required_Mixin_, _Primary_, _User_, _DB_Attr_
    Auth._Account_Token_Action_
      Kind_Wrapper_P : Date-Time `expires`
          Necessary, _User_, _DB_Attr_
      Kind_Wrapper_P : Account `left`
          Init_Only_Mixin, Just_Once_Mixin, Link_Role, _EPK_Mixin_, _SPK_Mixin_, Primary, _Required_Mixin_, _Primary_, _User_, _DB_Attr_
      Kind_Wrapper_P : String `token`
          Init_Only_Mixin, Just_Once_Mixin, Primary, _Required_Mixin_, _Primary_, _User_, _DB_Attr_
    Auth.Account_EMail_Verification
      Kind_Date_Time_Wrapper : Date-Time `expires`
          Necessary, _User_, _DB_Attr_
      Kind_Wrapper_S : Account `left`
          Init_Only_Mixin, Just_Once_Mixin, Link_Role, _EPK_Mixin_, _SPK_Mixin_, Primary, _Required_Mixin_, _Primary_, _User_, _DB_Attr_
      Kind_Wrapper : Email `new_email`
          Optional, _User_, _DB_Attr_
      Kind_Wrapper : String `token`
          Init_Only_Mixin, Just_Once_Mixin, Primary, _Required_Mixin_, _Primary_, _User_, _DB_Attr_
    Auth.Account_Password_Reset
      Kind_Date_Time_Wrapper : Date-Time `expires`
          Necessary, _User_, _DB_Attr_
      Kind_Wrapper_S : Account `left`
          Init_Only_Mixin, Just_Once_Mixin, Link_Role, _EPK_Mixin_, _SPK_Mixin_, Primary, _Required_Mixin_, _Primary_, _User_, _DB_Attr_
      Kind_Wrapper : String `password`
          Necessary, _User_, _DB_Attr_
      Kind_Wrapper : String `token`
          Init_Only_Mixin, Just_Once_Mixin, Primary, _Required_Mixin_, _Primary_, _User_, _DB_Attr_
    EVT.Calendar
      Kind_Wrapper : String `desc`
          Optional, _User_, _DB_Attr_
      Kind_Wrapper : Name `name`
          Primary, _Required_Mixin_, _Primary_, _User_, _DB_Attr_
    MOM.Date_Interval
      Kind_Wrapper_Q : Boolean `alive`
          _Nested_Mixin_, Computed, Query, _Cached_, _Volatile_, _System_
      Kind_Wrapper_Date : Date `finish`
          _Nested_Mixin_, Optional, _User_, _DB_Attr_
      Kind_Wrapper_Date : Date `start`
          _Nested_Mixin_, Necessary, _User_, _DB_Attr_
    MOM.Date_Interval_C
      Kind_Wrapper_Q : Boolean `alive`
          _Nested_Mixin_, Computed, Query, _Cached_, _Volatile_, _System_
      Kind_Wrapper_Date : Date `finish`
          _Nested_Mixin_, Computed_Set_Mixin, Computed_Mixin, Optional, _User_, _DB_Attr_
      Kind_Wrapper_Date : Date `start`
          _Nested_Mixin_, Necessary, _User_, _DB_Attr_
    MOM.Date_Interval_N
      Kind_Wrapper_Q : Boolean `alive`
          _Nested_Mixin_, Computed, Query, _Cached_, _Volatile_, _System_
      Kind_Wrapper_Date : Date `finish`
          _Nested_Mixin_, Optional, _User_, _DB_Attr_
      Kind_Wrapper_Date : Date `start`
          _Nested_Mixin_, Sticky_Mixin, _Sticky_Mixin_, Necessary, _User_, _DB_Attr_
    MOM.Time_Interval
      Kind_Wrapper_Time : Time `finish`
          _Nested_Mixin_, Optional, _User_, _DB_Attr_
      Kind_Wrapper_Time : Time `start`
          _Nested_Mixin_, Necessary, _User_, _DB_Attr_
    EVT.Link
      Kind_Wrapper_P : Left `left`
          Link_Role, _EPK_Mixin_, _SPK_Mixin_, Primary, _Required_Mixin_, _Primary_, _User_, _DB_Attr_
    EVT.Link1
      Kind_Wrapper_P : Left `left`
          Link_Role, _EPK_Mixin_, _SPK_Mixin_, Primary, _Required_Mixin_, _Primary_, _User_, _DB_Attr_
    SWP.Object_PN
      Kind_Wrapper_R : Link_Ref_List `clips`
          Computed, _Rev_Query_, _Cached_, _Volatile_, _System_
      Kind_Wrapper_P : Date_Interval `date`
          _Composite_Mixin_, Optional, _User_, _DB_Attr_
      Kind_Wrapper_P : Date-Slug `perma_name`
          Primary, _Required_Mixin_, _Primary_, _User_, _DB_Attr_
      Kind_Wrapper_P : String `short_title`
          Necessary, _User_, _DB_Attr_
      Kind_Wrapper_P : String `title`
          Necessary, _User_, _DB_Attr_
    SWP.Page_Mixin
      Kind_Wrapper : Text `contents`
          _Auto_Update_Mixin_, Internal, _DB_System_, _DB_Attr_, _System_
      Kind_Wrapper : Format `format`
          Sticky_Mixin, _Sticky_Mixin_, Optional, _User_, _DB_Attr_
      Kind_Wrapper : String `head_line`
          Optional, _User_, _DB_Attr_
      Kind_Wrapper : Boolean `hidden`
          Optional, _User_, _DB_Attr_
      Kind_Wrapper : Int `prio`
          Sticky_Mixin, _Sticky_Mixin_, Optional, _User_, _DB_Attr_
      Kind_Wrapper : Text `text`
          Required, _Required_Mixin_, _User_, _DB_Attr_
    SWP.Page
      Kind_Wrapper_R : Link_Ref_List `clips`
          Computed, _Rev_Query_, _Cached_, _Volatile_, _System_
      Kind_Wrapper : Text `contents`
          _Auto_Update_Mixin_, Internal, _DB_System_, _DB_Attr_, _System_
      Kind_Wrapper_C : Date_Interval `date`
          _Composite_Mixin_, Optional, _User_, _DB_Attr_
        MOM.Date_Interval_N
          Kind_Wrapper_Q : Boolean `alive`
              _Nested_Mixin_, Computed, Query, _Cached_, _Volatile_, _System_
          Kind_Wrapper_Date : Date `finish`
              _Nested_Mixin_, Optional, _User_, _DB_Attr_
          Kind_Wrapper_Date : Date `start`
              _Nested_Mixin_, Sticky_Mixin, _Sticky_Mixin_, Necessary, _User_, _DB_Attr_
      Kind_Wrapper_R : Link_Ref_List `events`
          Computed, _Rev_Query_, _Cached_, _Volatile_, _System_
      Kind_Wrapper : Format `format`
          Sticky_Mixin, _Sticky_Mixin_, Optional, _User_, _DB_Attr_
      Kind_Wrapper : String `head_line`
          Optional, _User_, _DB_Attr_
      Kind_Wrapper : Boolean `hidden`
          Optional, _User_, _DB_Attr_
      Kind_Wrapper : Date-Slug `perma_name`
          Primary, _Required_Mixin_, _Primary_, _User_, _DB_Attr_
      Kind_Wrapper : Int `prio`
          Sticky_Mixin, _Sticky_Mixin_, Optional, _User_, _DB_Attr_
      Kind_Wrapper : String `short_title`
          Necessary, _User_, _DB_Attr_
      Kind_Wrapper : Text `text`
          Required, _Required_Mixin_, _User_, _DB_Attr_
      Kind_Wrapper : String `title`
          Necessary, _User_, _DB_Attr_
    SWP.Page_Y
      Kind_Wrapper : Int `year`
          Primary_Optional, _Sticky_Mixin_, _Primary_D_, _Primary_, _User_, _DB_Attr_
    EVT.Event
      Kind_Wrapper_S : Entity `calendar`
          _Id_Entity_Reference_Mixin_, _EPK_Mixin_, _SPK_Mixin_, Primary_Optional, _Sticky_Mixin_, _Primary_D_, _Primary_, _User_, _DB_Attr_
      Kind_Wrapper_C : Date_Interval `date`
          _Composite_Mixin_, Primary_Optional, _Sticky_Mixin_, _Primary_D_, _Primary_, _User_, _DB_Attr_
        MOM.Date_Interval
          Kind_Wrapper_Q : Boolean `alive`
              _Nested_Mixin_, Computed, Query, _Cached_, _Volatile_, _System_
          Kind_Wrapper_Date : Date `finish`
              _Nested_Mixin_, Optional, _User_, _DB_Attr_
          Kind_Wrapper_Date : Date `start`
              _Nested_Mixin_, Necessary, _User_, _DB_Attr_
      Kind_Wrapper : String `detail`
          Optional, _User_, _DB_Attr_
      Kind_Wrapper_S : Page `left`
          Init_Only_Mixin, Just_Once_Mixin, Link_Role, _EPK_Mixin_, _SPK_Mixin_, Primary, _Required_Mixin_, _Primary_, _User_, _DB_Attr_
      Kind_Wrapper_R : Link_Ref_List `occurs`
          Computed, _Rev_Query_, _Cached_, _Volatile_, _System_
      Kind_Wrapper_R : Link_Ref `recurrence`
          Computed, _Rev_Query_, _Cached_, _Volatile_, _System_
      Kind_Wrapper : String `short_title`
          Computed_Set_Mixin, Computed_Mixin, Optional, _User_, _DB_Attr_
      Kind_Wrapper_C : Time_Interval `time`
          _Composite_Mixin_, Primary_Optional, _Sticky_Mixin_, _Primary_D_, _Primary_, _User_, _DB_Attr_
        MOM.Time_Interval
          Kind_Wrapper_Time : Time `finish`
              _Nested_Mixin_, Optional, _User_, _DB_Attr_
          Kind_Wrapper_Time : Time `start`
              _Nested_Mixin_, Necessary, _User_, _DB_Attr_
    EVT.Event_occurs
      Kind_Wrapper_Date : Date `date`
          Primary, _Required_Mixin_, _Primary_, _User_, _DB_Attr_
      Kind_Wrapper_S : Event `left`
          Init_Only_Mixin, Just_Once_Mixin, Link_Role, _EPK_Mixin_, _SPK_Mixin_, Primary, _Required_Mixin_, _Primary_, _User_, _DB_Attr_
      Kind_Wrapper_C : Time_Interval `time`
          _Composite_Mixin_, Primary_Optional, _Sticky_Mixin_, _Primary_D_, _Primary_, _User_, _DB_Attr_
        MOM.Time_Interval
          Kind_Wrapper_Time : Time `finish`
              _Nested_Mixin_, Optional, _User_, _DB_Attr_
          Kind_Wrapper_Time : Time `start`
              _Nested_Mixin_, Necessary, _User_, _DB_Attr_
    EVT._Recurrence_Mixin_
      Kind_Wrapper_P : Left `left`
          Link_Role, _EPK_Mixin_, _SPK_Mixin_, Primary, _Required_Mixin_, _Primary_, _User_, _DB_Attr_
    EVT.Recurrence_Spec
      Kind_Wrapper : Date_List `date_exceptions`
          Optional, _User_, _DB_Attr_
      Kind_Wrapper : Date_List `dates`
          Optional, _User_, _DB_Attr_
      Kind_Wrapper_S : Event `left`
          Init_Only_Mixin, Just_Once_Mixin, Link_Role, _EPK_Mixin_, _SPK_Mixin_, Primary, _Required_Mixin_, _Primary_, _User_, _DB_Attr_
      Kind_Wrapper_R : Link_Ref_List `rules`
          Computed, _Rev_Query_, _Cached_, _Volatile_, _System_
    EVT.Recurrence_Rule
      Kind_Wrapper : Int `count`
          Optional, _User_, _DB_Attr_
      Kind_Wrapper : String `desc`
          Primary_Optional, _Sticky_Mixin_, _Primary_D_, _Primary_, _User_, _DB_Attr_
      Kind_Wrapper : Int_List `easter_offset`
          Optional, _User_, _DB_Attr_
      Kind_Wrapper_Date : Date `finish`
          Computed_Set_Mixin, Computed_Mixin, Optional, _User_, _DB_Attr_
      Kind_Wrapper : Boolean `is_exception`
          Primary_Optional, _Sticky_Mixin_, _Primary_D_, _Primary_, _User_, _DB_Attr_
      Kind_Wrapper_S : Recurrence_Spec `left`
          Init_Only_Mixin, Just_Once_Mixin, Link_Role, _EPK_Mixin_, _SPK_Mixin_, Primary, _Required_Mixin_, _Primary_, _User_, _DB_Attr_
      Kind_Wrapper : Int_List `month`
          Optional, _User_, _DB_Attr_
      Kind_Wrapper : Int_List `month_day`
          Optional, _User_, _DB_Attr_
      Kind_Wrapper : Int `period`
          Optional, _User_, _DB_Attr_
      Kind_Wrapper : Int_List `restrict_pos`
          Optional, _User_, _DB_Attr_
      Kind_Wrapper_Date : Date `start`
          Computed_Set_Mixin, Computed_Mixin, Optional, _User_, _DB_Attr_
      Kind_Wrapper : Unit `unit`
          Sticky_Mixin, _Sticky_Mixin_, Optional, _User_, _DB_Attr_
      Kind_Wrapper : Int_List `week`
          Optional, _User_, _DB_Attr_
      Kind_Wrapper : Weekday_RR_List `week_day`
          Optional, _User_, _DB_Attr_
      Kind_Wrapper : Int_List `year_day`
          Optional, _User_, _DB_Attr_
    MOM.Position
      Kind_Wrapper : Float `height`
          _Nested_Mixin_, Optional, _User_, _DB_Attr_
      Kind_Wrapper : Angle `lat`
          _Nested_Mixin_, _Raw_Value_Mixin_, Necessary, _User_, _DB_Attr_
      Kind_Wrapper : Angle `lon`
          _Nested_Mixin_, _Raw_Value_Mixin_, Necessary, _User_, _DB_Attr_
    PAP.Property
      Kind_Wrapper_P : String `desc`
          Optional, _User_, _DB_Attr_
      Kind_Wrapper_R : Link_Ref_List `subject_links`
          Computed, _Rev_Query_, _Cached_, _Volatile_, _System_
    PAP.Address
      Kind_Wrapper : String `city`
          _Raw_Value_Mixin_, Primary, _Required_Mixin_, _Primary_, _User_, _DB_Attr_
      Kind_Wrapper_R : Role_Ref_Set `companies`
          Computed, _Rev_Query_, _Cached_, _Volatile_, _System_
      Kind_Wrapper_R : Link_Ref_List `company_links`
          Computed, _Rev_Query_, _Cached_, _Volatile_, _System_
      Kind_Wrapper : String `country`
          _Raw_Value_Mixin_, Primary, _Required_Mixin_, _Primary_, _User_, _DB_Attr_
      Kind_Wrapper : String `desc`
          Optional, _User_, _DB_Attr_
      Kind_Wrapper_R : Link_Ref `gps`
          Computed, _Rev_Query_, _Cached_, _Volatile_, _System_
      Kind_Wrapper_R : Link_Ref_List `person_links`
          Computed, _Rev_Query_, _Cached_, _Volatile_, _System_
      Kind_Wrapper_R : Role_Ref_Set `persons`
          Computed, _Rev_Query_, _Cached_, _Volatile_, _System_
      Kind_Wrapper : String `region`
          _Raw_Value_Mixin_, Optional, _User_, _DB_Attr_
      Kind_Wrapper : String `street`
          _Raw_Value_Mixin_, Primary, _Required_Mixin_, _Primary_, _User_, _DB_Attr_
      Kind_Wrapper_R : Link_Ref_List `subject_links`
          Computed, _Rev_Query_, _Cached_, _Volatile_, _System_
      Kind_Wrapper : String `zip`
          _Raw_Value_Mixin_, Primary, _Required_Mixin_, _Primary_, _User_, _DB_Attr_
    PAP.Subject
      Kind_Wrapper_R : Link_Ref_List `address_links`
          Computed, _Rev_Query_, _Cached_, _Volatile_, _System_
      Kind_Wrapper_R : Role_Ref_Set `addresses`
          Computed, _Rev_Query_, _Cached_, _Volatile_, _System_
      Kind_Wrapper_R : Link_Ref_List `email_links`
          Computed, _Rev_Query_, _Cached_, _Volatile_, _System_
      Kind_Wrapper_R : Role_Ref_Set `emails`
          Computed, _Rev_Query_, _Cached_, _Volatile_, _System_
      Kind_Wrapper_P : Date_Interval `lifetime`
          _Composite_Mixin_, Optional, _User_, _DB_Attr_
      Kind_Wrapper_R : Link_Ref_List `phone_links`
          Computed, _Rev_Query_, _Cached_, _Volatile_, _System_
      Kind_Wrapper_R : Role_Ref_Set `phones`
          Computed, _Rev_Query_, _Cached_, _Volatile_, _System_
      Kind_Wrapper_R : Link_Ref_List `property_links`
          Computed, _Rev_Query_, _Cached_, _Volatile_, _System_
      Kind_Wrapper_R : Link_Ref_List `url_links`
          Computed, _Rev_Query_, _Cached_, _Volatile_, _System_
      Kind_Wrapper_R : Role_Ref_Set `urls`
          Computed, _Rev_Query_, _Cached_, _Volatile_, _System_
    PAP.Legal_Entity
      Kind_Wrapper_R : Link_Ref_List `address_links`
          Computed, _Rev_Query_, _Cached_, _Volatile_, _System_
      Kind_Wrapper_R : Role_Ref_Set `addresses`
          Computed, _Rev_Query_, _Cached_, _Volatile_, _System_
      Kind_Wrapper_R : Link_Ref_List `email_links`
          Computed, _Rev_Query_, _Cached_, _Volatile_, _System_
      Kind_Wrapper_R : Role_Ref_Set `emails`
          Computed, _Rev_Query_, _Cached_, _Volatile_, _System_
      Kind_Wrapper_P : Date_Interval `lifetime`
          _Composite_Mixin_, Optional, _User_, _DB_Attr_
      Kind_Wrapper_P : String `name`
          _Raw_Value_Mixin_, Primary, _Required_Mixin_, _Primary_, _User_, _DB_Attr_
      Kind_Wrapper_R : Link_Ref_List `phone_links`
          Computed, _Rev_Query_, _Cached_, _Volatile_, _System_
      Kind_Wrapper_R : Role_Ref_Set `phones`
          Computed, _Rev_Query_, _Cached_, _Volatile_, _System_
      Kind_Wrapper_R : Link_Ref_List `property_links`
          Computed, _Rev_Query_, _Cached_, _Volatile_, _System_
      Kind_Wrapper_P : String `short_name`
          _Raw_Value_Mixin_, Optional, _User_, _DB_Attr_
      Kind_Wrapper_R : Link_Ref_List `url_links`
          Computed, _Rev_Query_, _Cached_, _Volatile_, _System_
      Kind_Wrapper_R : Role_Ref_Set `urls`
          Computed, _Rev_Query_, _Cached_, _Volatile_, _System_
    PAP.Company
      Kind_Wrapper_R : Link_Ref_List `address_links`
          Computed, _Rev_Query_, _Cached_, _Volatile_, _System_
      Kind_Wrapper_R : Role_Ref_Set `addresses`
          Computed, _Rev_Query_, _Cached_, _Volatile_, _System_
      Kind_Wrapper_R : Link_Ref_List `email_links`
          Computed, _Rev_Query_, _Cached_, _Volatile_, _System_
      Kind_Wrapper_R : Role_Ref_Set `emails`
          Computed, _Rev_Query_, _Cached_, _Volatile_, _System_
      Kind_Wrapper_C : Date_Interval `lifetime`
          _Composite_Mixin_, Optional, _User_, _DB_Attr_
        MOM.Date_Interval
          Kind_Wrapper_Q : Boolean `alive`
              _Nested_Mixin_, Computed, Query, _Cached_, _Volatile_, _System_
          Kind_Wrapper_Date : Date `finish`
              _Nested_Mixin_, Optional, _User_, _DB_Attr_
          Kind_Wrapper_Date : Date `start`
              _Nested_Mixin_, Necessary, _User_, _DB_Attr_
      Kind_Wrapper : String `name`
          _Raw_Value_Mixin_, Primary, _Required_Mixin_, _Primary_, _User_, _DB_Attr_
      Kind_Wrapper_R : Link_Ref_List `phone_links`
          Computed, _Rev_Query_, _Cached_, _Volatile_, _System_
      Kind_Wrapper_R : Role_Ref_Set `phones`
          Computed, _Rev_Query_, _Cached_, _Volatile_, _System_
      Kind_Wrapper_R : Link_Ref_List `property_links`
          Computed, _Rev_Query_, _Cached_, _Volatile_, _System_
      Kind_Wrapper : String `registered_in`
          _Raw_Value_Mixin_, Primary_Optional, _Sticky_Mixin_, _Primary_D_, _Primary_, _User_, _DB_Attr_
      Kind_Wrapper : String `short_name`
          _Raw_Value_Mixin_, Optional, _User_, _DB_Attr_
      Kind_Wrapper_R : Link_Ref_List `url_links`
          Computed, _Rev_Query_, _Cached_, _Volatile_, _System_
      Kind_Wrapper_R : Role_Ref_Set `urls`
          Computed, _Rev_Query_, _Cached_, _Volatile_, _System_
    PAP.Email
      Kind_Wrapper : Email `address`
          _Raw_Value_Mixin_, Primary, _Required_Mixin_, _Primary_, _User_, _DB_Attr_
      Kind_Wrapper_R : Role_Ref_Set `companies`
          Computed, _Rev_Query_, _Cached_, _Volatile_, _System_
      Kind_Wrapper_R : Link_Ref_List `company_links`
          Computed, _Rev_Query_, _Cached_, _Volatile_, _System_
      Kind_Wrapper : String `desc`
          Optional, _User_, _DB_Attr_
      Kind_Wrapper_R : Link_Ref_List `person_links`
          Computed, _Rev_Query_, _Cached_, _Volatile_, _System_
      Kind_Wrapper_R : Role_Ref_Set `persons`
          Computed, _Rev_Query_, _Cached_, _Volatile_, _System_
      Kind_Wrapper_R : Link_Ref_List `subject_links`
          Computed, _Rev_Query_, _Cached_, _Volatile_, _System_
    PAP.Phone
      Kind_Wrapper : Numeric_String `area_code`
          Primary, _Required_Mixin_, _Primary_, _User_, _DB_Attr_
      Kind_Wrapper_R : Role_Ref_Set `companies`
          Computed, _Rev_Query_, _Cached_, _Volatile_, _System_
      Kind_Wrapper_R : Link_Ref_List `company_links`
          Computed, _Rev_Query_, _Cached_, _Volatile_, _System_
      Kind_Wrapper : Numeric_String `country_code`
          Primary, _Required_Mixin_, _Primary_, _User_, _DB_Attr_
      Kind_Wrapper : String `desc`
          Optional, _User_, _DB_Attr_
      Kind_Wrapper : Numeric_String `number`
          Primary, _Required_Mixin_, _Primary_, _User_, _DB_Attr_
      Kind_Wrapper_R : Link_Ref_List `person_links`
          Computed, _Rev_Query_, _Cached_, _Volatile_, _System_
      Kind_Wrapper_R : Role_Ref_Set `persons`
          Computed, _Rev_Query_, _Cached_, _Volatile_, _System_
      Kind_Wrapper_R : Link_Ref_List `subject_links`
          Computed, _Rev_Query_, _Cached_, _Volatile_, _System_
    PAP.Person
      Kind_Wrapper_R : Link_Ref_List `account_links`
          Computed, _Rev_Query_, _Cached_, _Volatile_, _System_
      Kind_Wrapper_R : Role_Ref_Set `accounts`
          Computed, _Rev_Query_, _Cached_, _Volatile_, _System_
      Kind_Wrapper_R : Link_Ref_List `address_links`
          Computed, _Rev_Query_, _Cached_, _Volatile_, _System_
      Kind_Wrapper_R : Role_Ref_Set `addresses`
          Computed, _Rev_Query_, _Cached_, _Volatile_, _System_
      Kind_Wrapper_R : Link_Ref_List `email_links`
          Computed, _Rev_Query_, _Cached_, _Volatile_, _System_
      Kind_Wrapper_R : Role_Ref_Set `emails`
          Computed, _Rev_Query_, _Cached_, _Volatile_, _System_
      Kind_Wrapper : String `first_name`
          _Raw_Value_Mixin_, Primary, _Required_Mixin_, _Primary_, _User_, _DB_Attr_
      Kind_Wrapper : String `last_name`
          _Raw_Value_Mixin_, Primary, _Required_Mixin_, _Primary_, _User_, _DB_Attr_
      Kind_Wrapper_C : Date_Interval `lifetime`
          _Composite_Mixin_, Optional, _User_, _DB_Attr_
        MOM.Date_Interval
          Kind_Wrapper_Q : Boolean `alive`
              _Nested_Mixin_, Computed, Query, _Cached_, _Volatile_, _System_
          Kind_Wrapper_Date : Date `finish`
              _Nested_Mixin_, Optional, _User_, _DB_Attr_
          Kind_Wrapper_Date : Date `start`
              _Nested_Mixin_, Necessary, _User_, _DB_Attr_
      Kind_Wrapper : String `middle_name`
          _Raw_Value_Mixin_, Primary_Optional, _Sticky_Mixin_, _Primary_D_, _Primary_, _User_, _DB_Attr_
      Kind_Wrapper_R : Link_Ref_List `phone_links`
          Computed, _Rev_Query_, _Cached_, _Volatile_, _System_
      Kind_Wrapper_R : Role_Ref_Set `phones`
          Computed, _Rev_Query_, _Cached_, _Volatile_, _System_
      Kind_Wrapper_R : Link_Ref_List `property_links`
          Computed, _Rev_Query_, _Cached_, _Volatile_, _System_
      Kind_Wrapper_R : Link_Ref_List `sailors`
          Computed, _Rev_Query_, _Cached_, _Volatile_, _System_
      Kind_Wrapper : Sex `sex`
          Necessary, _User_, _DB_Attr_
      Kind_Wrapper : String `title`
          _Raw_Value_Mixin_, Primary_Optional, _Sticky_Mixin_, _Primary_D_, _Primary_, _User_, _DB_Attr_
      Kind_Wrapper_R : Link_Ref_List `url_links`
          Computed, _Rev_Query_, _Cached_, _Volatile_, _System_
      Kind_Wrapper_R : Role_Ref_Set `urls`
          Computed, _Rev_Query_, _Cached_, _Volatile_, _System_
    PAP.Url
      Kind_Wrapper_R : Role_Ref_Set `companies`
          Computed, _Rev_Query_, _Cached_, _Volatile_, _System_
      Kind_Wrapper_R : Link_Ref_List `company_links`
          Computed, _Rev_Query_, _Cached_, _Volatile_, _System_
      Kind_Wrapper : String `desc`
          Optional, _User_, _DB_Attr_
      Kind_Wrapper_R : Link_Ref_List `person_links`
          Computed, _Rev_Query_, _Cached_, _Volatile_, _System_
      Kind_Wrapper_R : Role_Ref_Set `persons`
          Computed, _Rev_Query_, _Cached_, _Volatile_, _System_
      Kind_Wrapper_R : Link_Ref_List `subject_links`
          Computed, _Rev_Query_, _Cached_, _Volatile_, _System_
      Kind_Wrapper : Url `value`
          Primary, _Required_Mixin_, _Primary_, _User_, _DB_Attr_
    PAP.Link
      Kind_Wrapper_P : Left `left`
          Link_Role, _EPK_Mixin_, _SPK_Mixin_, Primary, _Required_Mixin_, _Primary_, _User_, _DB_Attr_
    PAP.Link1
      Kind_Wrapper_P : Left `left`
          Link_Role, _EPK_Mixin_, _SPK_Mixin_, Primary, _Required_Mixin_, _Primary_, _User_, _DB_Attr_
    PAP.Address_Position
      Kind_Wrapper_S : Address `left`
          Init_Only_Mixin, Just_Once_Mixin, Link_Role, _EPK_Mixin_, _SPK_Mixin_, Primary, _Required_Mixin_, _Primary_, _User_, _DB_Attr_
      Kind_Wrapper_C : Position `position`
          _Composite_Mixin_, Primary, _Required_Mixin_, _Primary_, _User_, _DB_Attr_
        MOM.Position
          Kind_Wrapper : Float `height`
              _Nested_Mixin_, Optional, _User_, _DB_Attr_
          Kind_Wrapper : Angle `lat`
              _Nested_Mixin_, _Raw_Value_Mixin_, Necessary, _User_, _DB_Attr_
          Kind_Wrapper : Angle `lon`
              _Nested_Mixin_, _Raw_Value_Mixin_, Necessary, _User_, _DB_Attr_
    PAP._MOM_Link_n_
      Kind_Wrapper_P : Left `left`
          Link_Role, _EPK_Mixin_, _SPK_Mixin_, Primary, _Required_Mixin_, _Primary_, _User_, _DB_Attr_
      Kind_Wrapper_P : Right `right`
          Link_Role, _EPK_Mixin_, _SPK_Mixin_, Primary, _Required_Mixin_, _Primary_, _User_, _DB_Attr_
    PAP.Link2
      Kind_Wrapper_P : Left `left`
          Link_Role, _EPK_Mixin_, _SPK_Mixin_, Primary, _Required_Mixin_, _Primary_, _User_, _DB_Attr_
      Kind_Wrapper_P : Right `right`
          Link_Role, _EPK_Mixin_, _SPK_Mixin_, Primary, _Required_Mixin_, _Primary_, _User_, _DB_Attr_
    PAP.Subject_has_Property
      Kind_Wrapper : String `desc`
          Computed_Set_Mixin, Computed_Mixin, Optional, _User_, _DB_Attr_
      Kind_Wrapper_S : Subject `left`
          Link_Role, _EPK_Mixin_, _SPK_Mixin_, Primary, _Required_Mixin_, _Primary_, _User_, _DB_Attr_
      Kind_Wrapper_S : Property `right`
          Link_Role, _EPK_Mixin_, _SPK_Mixin_, Primary, _Required_Mixin_, _Primary_, _User_, _DB_Attr_
    PAP.Person_has_Account
      Kind_Wrapper_S : Person `left`
          Link_Role, _EPK_Mixin_, _SPK_Mixin_, Primary, _Required_Mixin_, _Primary_, _User_, _DB_Attr_
      Kind_Wrapper_S : Account `right`
          Link_Role, _EPK_Mixin_, _SPK_Mixin_, Primary, _Required_Mixin_, _Primary_, _User_, _DB_Attr_
    SRM.Regatta_Result
      Kind_Date_Time_Wrapper : Date-Time `date`
          _Nested_Mixin_, Necessary, _User_, _DB_Attr_
      Kind_Wrapper : String `software`
          _Nested_Mixin_, Optional, _User_, _DB_Attr_
      Kind_Wrapper : String `status`
          _Nested_Mixin_, Optional, _User_, _DB_Attr_
    SRM._Boat_Class_
      Kind_Wrapper : String `name`
          _Raw_Value_Mixin_, Primary, _Required_Mixin_, _Primary_, _User_, _DB_Attr_
    SRM.Boat_Class
      Kind_Wrapper : Float `beam`
          Optional, _User_, _DB_Attr_
      Kind_Wrapper_R : Link_Ref_List `boats`
          Computed, _Rev_Query_, _Cached_, _Volatile_, _System_
      Kind_Wrapper : Float `loa`
          Optional, _User_, _DB_Attr_
      Kind_Wrapper : Int `max_crew`
          Required, _Required_Mixin_, _User_, _DB_Attr_
      Kind_Wrapper : Float `sail_area`
          Optional, _User_, _DB_Attr_
    SRM.Handicap <-- SRM._Boat_Class_
    SRM.Link
      Kind_Wrapper_P : Left `left`
          Link_Role, _EPK_Mixin_, _SPK_Mixin_, Primary, _Required_Mixin_, _Primary_, _User_, _DB_Attr_
    SRM.Link1
      Kind_Wrapper_P : Left `left`
          Link_Role, _EPK_Mixin_, _SPK_Mixin_, Primary, _Required_Mixin_, _Primary_, _User_, _DB_Attr_
    SRM.Boat
      Kind_Wrapper_S : Boat_Class `left`
          Init_Only_Mixin, Just_Once_Mixin, Link_Role, _EPK_Mixin_, _SPK_Mixin_, Primary, _Required_Mixin_, _Primary_, _User_, _DB_Attr_
      Kind_Wrapper : String `name`
          Optional, _User_, _DB_Attr_
      Kind_Wrapper : Nation `nation`
          Primary_Optional, _Sticky_Mixin_, _Primary_D_, _Primary_, _User_, _DB_Attr_
      Kind_Wrapper_R : Link_Ref_List `regatta_links`
          Computed, _Rev_Query_, _Cached_, _Volatile_, _System_
      Kind_Wrapper : Int `sail_number`
          _Raw_Value_Mixin_, Primary, _Required_Mixin_, _Primary_, _User_, _DB_Attr_
      Kind_Wrapper : String `sail_number_x`
          _Raw_Value_Mixin_, Primary_Optional, _Sticky_Mixin_, _Primary_D_, _Primary_, _User_, _DB_Attr_
    SRM.Club
      Kind_Wrapper : String `long_name`
          Optional, _User_, _DB_Attr_
      Kind_Wrapper : String `name`
          _Raw_Value_Mixin_, Primary, _Required_Mixin_, _Primary_, _User_, _DB_Attr_
    SRM.Regatta_Event
      Kind_Wrapper_S : Entity `club`
          _Id_Entity_Reference_Mixin_, _EPK_Mixin_, _SPK_Mixin_, Optional, _User_, _DB_Attr_
      Kind_Wrapper_C : Date_Interval `date`
          _Composite_Mixin_, Primary, _Required_Mixin_, _Primary_, _User_, _DB_Attr_
        MOM.Date_Interval_C
          Kind_Wrapper_Q : Boolean `alive`
              _Nested_Mixin_, Computed, Query, _Cached_, _Volatile_, _System_
          Kind_Wrapper_Date : Date `finish`
              _Nested_Mixin_, Computed_Set_Mixin, Computed_Mixin, Optional, _User_, _DB_Attr_
          Kind_Wrapper_Date : Date `start`
              _Nested_Mixin_, Necessary, _User_, _DB_Attr_
      Kind_Wrapper : String `desc`
          Optional, _User_, _DB_Attr_
      Kind_Wrapper : Boolean `is_cancelled`
          Optional, _User_, _DB_Attr_
      Kind_Wrapper : String `name`
          _Raw_Value_Mixin_, Primary, _Required_Mixin_, _Primary_, _User_, _DB_Attr_
      Kind_Wrapper : String `perma_name`
          Computed_Set_Mixin, Computed_Mixin, _Auto_Update_Lazy_Mixin_, _Auto_Update_Mixin_, Internal, _DB_System_, _DB_Attr_, _System_
      Kind_Wrapper_R : Link_Ref_List `regattas`
          Computed, _Rev_Query_, _Cached_, _Volatile_, _System_
      Kind_Wrapper_Q : Int `year`
          Query, _Cached_, _Volatile_, _System_
    SWP.Link
      Kind_Wrapper_P : Left `left`
          Link_Role, _EPK_Mixin_, _SPK_Mixin_, Primary, _Required_Mixin_, _Primary_, _User_, _DB_Attr_
    SWP.Link1
      Kind_Wrapper_P : Left `left`
          Link_Role, _EPK_Mixin_, _SPK_Mixin_, Primary, _Required_Mixin_, _Primary_, _User_, _DB_Attr_
    SWP.Clip_O
      Kind_Wrapper : Text `abstract`
          Required, _Required_Mixin_, _User_, _DB_Attr_
      Kind_Wrapper : Text `contents`
          _Auto_Update_Mixin_, Internal, _DB_System_, _DB_Attr_, _System_
      Kind_Wrapper_C : Date_Interval `date`
          _Composite_Mixin_, _Auto_Update_Mixin_, Internal, _DB_System_, _DB_Attr_, _System_
        MOM.Date_Interval
          Kind_Wrapper_Q : Boolean `alive`
              _Nested_Mixin_, Computed, Query, _Cached_, _Volatile_, _System_
          Kind_Wrapper_Date : Date `finish`
              _Nested_Mixin_, Optional, _User_, _DB_Attr_
          Kind_Wrapper_Date : Date `start`
              _Nested_Mixin_, Necessary, _User_, _DB_Attr_
      Kind_Wrapper_C : Date_Interval `date_x`
          _Composite_Mixin_, Primary_Optional, _Sticky_Mixin_, _Primary_D_, _Primary_, _User_, _DB_Attr_
        MOM.Date_Interval
          Kind_Wrapper_Q : Boolean `alive`
              _Nested_Mixin_, Computed, Query, _Cached_, _Volatile_, _System_
          Kind_Wrapper_Date : Date `finish`
              _Nested_Mixin_, Optional, _User_, _DB_Attr_
          Kind_Wrapper_Date : Date `start`
              _Nested_Mixin_, Necessary, _User_, _DB_Attr_
      Kind_Wrapper_S : Object_PN `left`
          Init_Only_Mixin, Just_Once_Mixin, Link_Role, _EPK_Mixin_, _SPK_Mixin_, Primary, _Required_Mixin_, _Primary_, _User_, _DB_Attr_
      Kind_Wrapper : Int `prio`
          Sticky_Mixin, _Sticky_Mixin_, Optional, _User_, _DB_Attr_
    SWP.Clip_X
      Kind_Wrapper : Url `link_to`
          Optional, _User_, _DB_Attr_
    SWP.Gallery
      Kind_Wrapper_R : Link_Ref_List `clips`
          Computed, _Rev_Query_, _Cached_, _Volatile_, _System_
      Kind_Wrapper_C : Date_Interval `date`
          _Composite_Mixin_, Optional, _User_, _DB_Attr_
        MOM.Date_Interval_N
          Kind_Wrapper_Q : Boolean `alive`
              _Nested_Mixin_, Computed, Query, _Cached_, _Volatile_, _System_
          Kind_Wrapper_Date : Date `finish`
              _Nested_Mixin_, Optional, _User_, _DB_Attr_
          Kind_Wrapper_Date : Date `start`
              _Nested_Mixin_, Sticky_Mixin, _Sticky_Mixin_, Necessary, _User_, _DB_Attr_
      Kind_Wrapper : Directory `directory`
          Necessary, _User_, _DB_Attr_
      Kind_Wrapper : Date-Slug `perma_name`
          Primary, _Required_Mixin_, _Primary_, _User_, _DB_Attr_
      Kind_Wrapper_R : Link_Ref_List `pictures`
          Computed, _Rev_Query_, _Cached_, _Volatile_, _System_
      Kind_Wrapper : String `short_title`
          Necessary, _User_, _DB_Attr_
      Kind_Wrapper : String `title`
          Necessary, _User_, _DB_Attr_
    MOM.D2_Value_Int
      Kind_Wrapper : X `x`
          _Nested_Mixin_, Necessary, _User_, _DB_Attr_
      Kind_Wrapper : Y `y`
          _Nested_Mixin_, Necessary, _User_, _DB_Attr_
    MOM.D2_Value_Float
      Kind_Wrapper : X `x`
          _Nested_Mixin_, Necessary, _User_, _DB_Attr_
      Kind_Wrapper : Y `y`
          _Nested_Mixin_, Necessary, _User_, _DB_Attr_
    MOM._Pic_
      Kind_Wrapper : String `extension`
          _Nested_Mixin_, Init_Only_Mixin, Just_Once_Mixin, Optional, _User_, _DB_Attr_
      Kind_Wrapper : Y `height`
          _Nested_Mixin_, Necessary, _User_, _DB_Attr_
      Kind_Wrapper : X `width`
          _Nested_Mixin_, Necessary, _User_, _DB_Attr_
    MOM._Thumb_
      Kind_Wrapper : String `extension`
          _Nested_Mixin_, Init_Only_Mixin, Just_Once_Mixin, Optional, _User_, _DB_Attr_
      Kind_Wrapper : Y `height`
          _Nested_Mixin_, Necessary, _User_, _DB_Attr_
      Kind_Wrapper : X `width`
          _Nested_Mixin_, Necessary, _User_, _DB_Attr_
    SWP.Picture
      Kind_Wrapper_S : Gallery `left`
          Init_Only_Mixin, Just_Once_Mixin, Link_Role, _EPK_Mixin_, _SPK_Mixin_, Primary, _Required_Mixin_, _Primary_, _User_, _DB_Attr_
      Kind_Wrapper : String `name`
          Computed_Set_Mixin, Computed_Mixin, Optional, _User_, _DB_Attr_
      Kind_Wrapper : Int `number`
          Primary, _Required_Mixin_, _Primary_, _User_, _DB_Attr_
      Kind_Wrapper_C : Picture `photo`
          _Composite_Mixin_, Necessary, _User_, _DB_Attr_
        MOM._Pic_
          Kind_Wrapper : String `extension`
              _Nested_Mixin_, Init_Only_Mixin, Just_Once_Mixin, Optional, _User_, _DB_Attr_
          Kind_Wrapper : Y `height`
              _Nested_Mixin_, Necessary, _User_, _DB_Attr_
          Kind_Wrapper : X `width`
              _Nested_Mixin_, Necessary, _User_, _DB_Attr_
      Kind_Wrapper_C : Thumbnail `thumb`
          _Composite_Mixin_, Necessary, _User_, _DB_Attr_
        MOM._Thumb_
          Kind_Wrapper : String `extension`
              _Nested_Mixin_, Init_Only_Mixin, Just_Once_Mixin, Optional, _User_, _DB_Attr_
          Kind_Wrapper : Y `height`
              _Nested_Mixin_, Necessary, _User_, _DB_Attr_
          Kind_Wrapper : X `width`
              _Nested_Mixin_, Necessary, _User_, _DB_Attr_
    SRM.Page
      Kind_Wrapper : String `desc`
          Computed_Set_Mixin, Computed_Mixin, Optional, _User_, _DB_Attr_
      Kind_Wrapper_S : Entity `event`
          _Id_Entity_Reference_Mixin_, _EPK_Mixin_, _SPK_Mixin_, Primary, _Required_Mixin_, _Primary_, _User_, _DB_Attr_
    SRM.Regatta
      Kind_Wrapper_S : Entity `boat_class`
          _Id_Entity_Reference_Mixin_, _EPK_Mixin_, _SPK_Mixin_, Primary, _Required_Mixin_, _Primary_, _User_, _DB_Attr_
      Kind_Wrapper_R : Link_Ref_List `boats`
          Computed, _Rev_Query_, _Cached_, _Volatile_, _System_
      Kind_Wrapper : Int `discards`
          Optional, _User_, _DB_Attr_
      Kind_Wrapper : Boolean `is_cancelled`
          Computed_Set_Mixin, Computed_Mixin, Optional, _User_, _DB_Attr_
      Kind_Wrapper : String `kind`
          Optional, _User_, _DB_Attr_
      Kind_Wrapper_S : Regatta_Event `left`
          Init_Only_Mixin, Just_Once_Mixin, Link_Role, _EPK_Mixin_, _SPK_Mixin_, Primary, _Required_Mixin_, _Primary_, _User_, _DB_Attr_
      Kind_Wrapper : String `perma_name`
          Computed_Set_Mixin, Computed_Mixin, _Auto_Update_Lazy_Mixin_, _Auto_Update_Mixin_, Internal, _DB_System_, _DB_Attr_, _System_
      Kind_Wrapper : Int `races`
          Optional, _User_, _DB_Attr_
      Kind_Wrapper_Q : Int `races_counted`
          Query, _Cached_, _Volatile_, _System_
      Kind_Wrapper_C : Regatta_Result `result`
          _Composite_Mixin_, Optional, _User_, _DB_Attr_
        SRM.Regatta_Result
          Kind_Date_Time_Wrapper : Date-Time `date`
              _Nested_Mixin_, Necessary, _User_, _DB_Attr_
          Kind_Wrapper : String `software`
              _Nested_Mixin_, Optional, _User_, _DB_Attr_
          Kind_Wrapper : String `status`
              _Nested_Mixin_, Optional, _User_, _DB_Attr_
      Kind_Wrapper_Q : Int `year`
          Query, _Cached_, _Volatile_, _System_
    SRM.Regatta_C
      Kind_Wrapper : Boolean `is_team_race`
          Optional, _User_, _DB_Attr_
      Kind_Wrapper_R : Link_Ref_List `teams`
          Computed, _Rev_Query_, _Cached_, _Volatile_, _System_
    SRM.Regatta_H
      Kind_Wrapper_Q : Blob `handicap`
          Query, _Cached_, _Volatile_, _System_
    SRM.Sailor
      Kind_Wrapper_R : Link_Ref_List `boat_in_regatta_links`
          Computed, _Rev_Query_, _Cached_, _Volatile_, _System_
      Kind_Wrapper_S : Entity `club`
          _Id_Entity_Reference_Mixin_, _EPK_Mixin_, _SPK_Mixin_, Primary_Optional, _Sticky_Mixin_, _Primary_D_, _Primary_, _User_, _DB_Attr_
      Kind_Wrapper_S : Person `left`
          Init_Only_Mixin, Just_Once_Mixin, Link_Role, _EPK_Mixin_, _SPK_Mixin_, Primary, _Required_Mixin_, _Primary_, _User_, _DB_Attr_
      Kind_Wrapper : Int `mna_number`
          _Raw_Value_Mixin_, Primary_Optional, _Sticky_Mixin_, _Primary_D_, _Primary_, _User_, _DB_Attr_
      Kind_Wrapper : Nation `nation`
          Primary_Optional, _Sticky_Mixin_, _Primary_D_, _Primary_, _User_, _DB_Attr_
    SRM._MOM_Link_n_
      Kind_Wrapper_P : Left `left`
          Link_Role, _EPK_Mixin_, _SPK_Mixin_, Primary, _Required_Mixin_, _Primary_, _User_, _DB_Attr_
      Kind_Wrapper_P : Right `right`
          Link_Role, _EPK_Mixin_, _SPK_Mixin_, Primary, _Required_Mixin_, _Primary_, _User_, _DB_Attr_
    SRM.Link2
      Kind_Wrapper_P : Left `left`
          Link_Role, _EPK_Mixin_, _SPK_Mixin_, Primary, _Required_Mixin_, _Primary_, _User_, _DB_Attr_
      Kind_Wrapper_P : Right `right`
          Link_Role, _EPK_Mixin_, _SPK_Mixin_, Primary, _Required_Mixin_, _Primary_, _User_, _DB_Attr_
    SRM.Boat_in_Regatta
      Kind_Wrapper_R : Role_Ref_Set `_crew`
          Computed, _Rev_Query_, _Cached_, _Volatile_, _System_
      Kind_Wrapper_S : Boat `left`
          Link_Role, _EPK_Mixin_, _SPK_Mixin_, Primary, _Required_Mixin_, _Primary_, _User_, _DB_Attr_
      Kind_Wrapper : Int `place`
          Optional, _User_, _DB_Attr_
      Kind_Wrapper : Int `points`
          Optional, _User_, _DB_Attr_
      Kind_Wrapper_R : Link_Ref_List `race_results`
          Computed, _Rev_Query_, _Cached_, _Volatile_, _System_
      Kind_Wrapper : Int `rank`
          Internal, _DB_System_, _DB_Attr_, _System_
      Kind_Wrapper_Date : Date `registration_date`
          Init_Only_Mixin, Just_Once_Mixin, Internal, _DB_System_, _DB_Attr_, _System_
      Kind_Wrapper_S : Regatta `right`
          Link_Role, _EPK_Mixin_, _SPK_Mixin_, Primary, _Required_Mixin_, _Primary_, _User_, _DB_Attr_
      Kind_Wrapper_R : Link_Ref_List `sailor_links`
          Computed, _Rev_Query_, _Cached_, _Volatile_, _System_
      Kind_Wrapper_S : Entity `skipper`
          _Id_Entity_Reference_Mixin_, _EPK_Mixin_, _SPK_Mixin_, Required, _Required_Mixin_, _User_, _DB_Attr_
      Kind_Wrapper_R : Link_Ref_List `team_links`
          Computed, _Rev_Query_, _Cached_, _Volatile_, _System_
      Kind_Wrapper_R : Role_Ref_Set `teams`
          Computed, _Rev_Query_, _Cached_, _Volatile_, _System_
    SRM.Race_Result
      Kind_Wrapper : Boolean `discarded`
          Sticky_Mixin, _Sticky_Mixin_, Optional, _User_, _DB_Attr_
      Kind_Wrapper_S : Boat_in_Regatta `left`
          Init_Only_Mixin, Just_Once_Mixin, Link_Role, _EPK_Mixin_, _SPK_Mixin_, Primary, _Required_Mixin_, _Primary_, _User_, _DB_Attr_
      Kind_Wrapper : Int `points`
          Necessary, _User_, _DB_Attr_
      Kind_Wrapper : Int `race`
          Primary, _Required_Mixin_, _Primary_, _User_, _DB_Attr_
      Kind_Wrapper : String `status`
          Optional, _User_, _DB_Attr_
    SRM.Team
      Kind_Wrapper_R : Link_Ref_List `boat_links`
          Computed, _Rev_Query_, _Cached_, _Volatile_, _System_
      Kind_Wrapper_R : Role_Ref_Set `boats`
          Computed, _Rev_Query_, _Cached_, _Volatile_, _System_
      Kind_Wrapper_S : Entity `club`
          _Id_Entity_Reference_Mixin_, _EPK_Mixin_, _SPK_Mixin_, Optional, _User_, _DB_Attr_
      Kind_Wrapper : String `desc`
          Optional, _User_, _DB_Attr_
      Kind_Wrapper_S : Entity `leader`
          _Id_Entity_Reference_Mixin_, _EPK_Mixin_, _SPK_Mixin_, Optional, _User_, _DB_Attr_
      Kind_Wrapper_S : Regatta_C `left`
          Init_Only_Mixin, Just_Once_Mixin, Link_Role, _EPK_Mixin_, _SPK_Mixin_, Primary, _Required_Mixin_, _Primary_, _User_, _DB_Attr_
      Kind_Wrapper : String `name`
          _Raw_Value_Mixin_, Primary, _Required_Mixin_, _Primary_, _User_, _DB_Attr_
      Kind_Wrapper : Int `place`
          Optional, _User_, _DB_Attr_
      Kind_Wrapper_Date : Date `registration_date`
          Internal, _DB_System_, _DB_Attr_, _System_
    SRM.Crew_Member
      Kind_Wrapper : Int `key`
          Sticky_Mixin, _Sticky_Mixin_, Optional, _User_, _DB_Attr_
      Kind_Wrapper_S : Boat_in_Regatta `left`
          Link_Role, _EPK_Mixin_, _SPK_Mixin_, Primary, _Required_Mixin_, _Primary_, _User_, _DB_Attr_
      Kind_Wrapper_S : Sailor `right`
          Link_Role, _EPK_Mixin_, _SPK_Mixin_, Primary, _Required_Mixin_, _Primary_, _User_, _DB_Attr_
      Kind_Wrapper : String `role`
          Optional, _User_, _DB_Attr_
    SRM.Team_has_Boat_in_Regatta
      Kind_Wrapper_S : Team `left`
          Link_Role, _EPK_Mixin_, _SPK_Mixin_, Primary, _Required_Mixin_, _Primary_, _User_, _DB_Attr_
      Kind_Wrapper_S : Boat_in_Regatta `right`
          Link_Role, _EPK_Mixin_, _SPK_Mixin_, Primary, _Required_Mixin_, _Primary_, _User_, _DB_Attr_
    PAP.Subject_has_Address <-- PAP.Subject_has_Property
    PAP.Subject_has_Email <-- PAP.Subject_has_Property
    PAP.Subject_has_Phone
      Kind_Wrapper : Numeric_String `extension`
          Primary_Optional, _Sticky_Mixin_, _Primary_D_, _Primary_, _User_, _DB_Attr_
    PAP.Subject_has_Url <-- PAP.Subject_has_Property
    PAP.Company_has_Url <-- PAP.Subject_has_Property
    PAP.Person_has_Url <-- PAP.Subject_has_Property
    PAP.Company_has_Phone <-- PAP.Subject_has_Phone
    PAP.Person_has_Phone <-- PAP.Subject_has_Phone
    PAP.Company_has_Email <-- PAP.Subject_has_Property
    PAP.Person_has_Email <-- PAP.Subject_has_Property
    PAP.Company_has_Address <-- PAP.Subject_has_Property
    PAP.Person_has_Address <-- PAP.Subject_has_Property

    >>> show_attr_mro (apt ["Auth.Account"])
    Auth.Account
      _account_action_s    -> Auth._Account_Action_
        Computed, _Rev_Query_, _Cached_, _Volatile_, _System_
      _account_token_action_s -> Auth._Account_Token_Action_
        Computed, _Rev_Query_, _Cached_, _Volatile_, _System_
      account_email_verifications -> Auth.Account_EMail_Verification
        Computed, _Rev_Query_, _Cached_, _Volatile_, _System_
      account_password_resets -> Auth.Account_Password_Reset
        Computed, _Rev_Query_, _Cached_, _Volatile_, _System_
      activation           -> Auth.Account_Activation
        Computed, _Rev_Query_, _Cached_, _Volatile_, _System_
      activations          -> Auth.Account_Activation
        Computed, _Rev_Query_, _Cached_, _Volatile_, _System_
      active
        _Auto_Update_Mixin_, Query, _Cached_, _Volatile_, _System_
      created_by           -> MOM.Id_Entity
        _Id_Entity_Reference_Mixin_, _EPK_Mixin_, _SPK_Mixin_, Computed, _Cached_, _Volatile_, _System_
      creation             -> MOM.MD_Change
        Computed, _Rev_Query_, _Cached_, _Volatile_, _System_
      creation_date
        Computed, _Cached_, _Volatile_, _System_
      electric
        Internal, _DB_System_, _DB_Attr_, _System_
      enabled
        Optional, _User_, _DB_Attr_
      group_links          -> Auth.Account_in_Group
        Computed, _Rev_Query_, _Cached_, _Volatile_, _System_
      groups               -> Auth.Group
        Computed, _Rev_Query_, _Cached_, _Volatile_, _System_
      is_used
        Cached, _Cached_, _Volatile_, _System_
      last_change          -> MOM.MD_Change
        Computed, _Rev_Query_, _Cached_, _Volatile_, _System_
      last_changed
        Computed, _Cached_, _Volatile_, _System_
      last_changed_by      -> MOM.Id_Entity
        _Id_Entity_Reference_Mixin_, _EPK_Mixin_, _SPK_Mixin_, Computed, _Cached_, _Volatile_, _System_
      last_cid
        Internal, _DB_System_, _DB_Attr_, _System_
      name
        Primary, _Required_Mixin_, _Primary_, _User_, _DB_Attr_
      password
        Internal, _DB_System_, _DB_Attr_, _System_
      password_change_required -> Auth.Account_Password_Change_Required
        Computed, _Rev_Query_, _Cached_, _Volatile_, _System_
      password_change_requireds -> Auth.Account_Password_Change_Required
        Computed, _Rev_Query_, _Cached_, _Volatile_, _System_
      person               -> PAP.Person
        Computed, _Rev_Query_, _Cached_, _Volatile_, _System_
      person_link          -> PAP.Person_has_Account
        Computed, _Rev_Query_, _Cached_, _Volatile_, _System_
      person_links         -> PAP.Person_has_Account
        Computed, _Rev_Query_, _Cached_, _Volatile_, _System_
      ph_name
        Sticky_Mixin, _Sticky_Mixin_, Internal, _DB_System_, _DB_Attr_, _System_
      pid
        Just_Once_Mixin, Internal, _DB_System_, _DB_Attr_, _System_
      superuser
        Optional, _User_, _DB_Attr_
      suspended
        Internal, _DB_System_, _DB_Attr_, _System_
      type_name
        _Type_Name_Mixin_, Internal, _DB_System_, _DB_Attr_, _System_
      ui_display
        Computed, _Cached_, _Volatile_, _System_
      ui_repr
        Computed, _Cached_, _Volatile_, _System_
      x_locked
        Internal, _DB_System_, _DB_Attr_, _System_

    >>> show_attr_mro (apt ["PAP.Person"])
    PAP.Person
      account_links        -> PAP.Person_has_Account
        Computed, _Rev_Query_, _Cached_, _Volatile_, _System_
      accounts             -> Auth.Account
        Computed, _Rev_Query_, _Cached_, _Volatile_, _System_
      address_links        -> PAP.Person_has_Address
        Computed, _Rev_Query_, _Cached_, _Volatile_, _System_
      addresses            -> PAP.Address
        Computed, _Rev_Query_, _Cached_, _Volatile_, _System_
      created_by           -> MOM.Id_Entity
        _Id_Entity_Reference_Mixin_, _EPK_Mixin_, _SPK_Mixin_, Computed, _Cached_, _Volatile_, _System_
      creation             -> MOM.MD_Change
        Computed, _Rev_Query_, _Cached_, _Volatile_, _System_
      creation_date
        Computed, _Cached_, _Volatile_, _System_
      electric
        Internal, _DB_System_, _DB_Attr_, _System_
      email_links          -> PAP.Person_has_Email
        Computed, _Rev_Query_, _Cached_, _Volatile_, _System_
      emails               -> PAP.Email
        Computed, _Rev_Query_, _Cached_, _Volatile_, _System_
      first_name
        _Raw_Value_Mixin_, Primary, _Required_Mixin_, _Primary_, _User_, _DB_Attr_
      is_used
        Cached, _Cached_, _Volatile_, _System_
      last_change          -> MOM.MD_Change
        Computed, _Rev_Query_, _Cached_, _Volatile_, _System_
      last_changed
        Computed, _Cached_, _Volatile_, _System_
      last_changed_by      -> MOM.Id_Entity
        _Id_Entity_Reference_Mixin_, _EPK_Mixin_, _SPK_Mixin_, Computed, _Cached_, _Volatile_, _System_
      last_cid
        Internal, _DB_System_, _DB_Attr_, _System_
      last_name
        _Raw_Value_Mixin_, Primary, _Required_Mixin_, _Primary_, _User_, _DB_Attr_
      lifetime             -> MOM.Date_Interval
        _Composite_Mixin_, Optional, _User_, _DB_Attr_
        alive
          _Nested_Mixin_, Computed, Query, _Cached_, _Volatile_, _System_
        days
          _Nested_Mixin_, Computed_Set_Mixin, Computed_Mixin, _Auto_Update_Lazy_Mixin_, _Auto_Update_Mixin_, Cached, _Cached_, _Volatile_, _System_
        finish
          _Nested_Mixin_, Optional, _User_, _DB_Attr_
        start
          _Nested_Mixin_, Necessary, _User_, _DB_Attr_
        ui_display
          _Nested_Mixin_, Computed, _Cached_, _Volatile_, _System_
        ui_repr
          Computed, _Cached_, _Volatile_, _System_
      middle_name
        _Raw_Value_Mixin_, Primary_Optional, _Sticky_Mixin_, _Primary_D_, _Primary_, _User_, _DB_Attr_
      phone_links          -> PAP.Person_has_Phone
        Computed, _Rev_Query_, _Cached_, _Volatile_, _System_
      phones               -> PAP.Phone
        Computed, _Rev_Query_, _Cached_, _Volatile_, _System_
      pid
        Just_Once_Mixin, Internal, _DB_System_, _DB_Attr_, _System_
      property_links       -> PAP.Subject_has_Property
        Computed, _Rev_Query_, _Cached_, _Volatile_, _System_
      sailors              -> SRM.Sailor
        Computed, _Rev_Query_, _Cached_, _Volatile_, _System_
      sex
        Necessary, _User_, _DB_Attr_
      title
        _Raw_Value_Mixin_, Primary_Optional, _Sticky_Mixin_, _Primary_D_, _Primary_, _User_, _DB_Attr_
      type_name
        _Type_Name_Mixin_, Internal, _DB_System_, _DB_Attr_, _System_
      ui_display
        Computed, _Cached_, _Volatile_, _System_
      ui_repr
        Computed, _Cached_, _Volatile_, _System_
      url_links            -> PAP.Person_has_Url
        Computed, _Rev_Query_, _Cached_, _Volatile_, _System_
      urls                 -> PAP.Url
        Computed, _Rev_Query_, _Cached_, _Volatile_, _System_
      x_locked
        Internal, _DB_System_, _DB_Attr_, _System_

    >>> show_attr_mro (apt ["PAP.Person_has_Phone"])
    PAP.Person_has_Phone
      created_by           -> MOM.Id_Entity
        _Id_Entity_Reference_Mixin_, _EPK_Mixin_, _SPK_Mixin_, Computed, _Cached_, _Volatile_, _System_
      creation      -> MOM.MD_Change
        Computed, _Rev_Query_, _Cached_, _Volatile_, _System_
      creation_date
        Computed, _Cached_, _Volatile_, _System_
      desc
        Computed_Set_Mixin, Computed_Mixin, Optional, _User_, _DB_Attr_
      electric
        Internal, _DB_System_, _DB_Attr_, _System_
      extension
        Primary_Optional, _Sticky_Mixin_, _Primary_D_, _Primary_, _User_, _DB_Attr_
      is_used
        Cached, _Cached_, _Volatile_, _System_
      last_change          -> MOM.MD_Change
        Computed, _Rev_Query_, _Cached_, _Volatile_, _System_
      last_changed
        Computed, _Cached_, _Volatile_, _System_
      last_changed_by      -> MOM.Id_Entity
        _Id_Entity_Reference_Mixin_, _EPK_Mixin_, _SPK_Mixin_, Computed, _Cached_, _Volatile_, _System_
      last_cid
        Internal, _DB_System_, _DB_Attr_, _System_
      left                 -> PAP.Person
        Link_Role, _EPK_Mixin_, _SPK_Mixin_, Primary, _Required_Mixin_, _Primary_, _User_, _DB_Attr_
      pid
        Just_Once_Mixin, Internal, _DB_System_, _DB_Attr_, _System_
      right                -> PAP.Phone
        Link_Role, _EPK_Mixin_, _SPK_Mixin_, Primary, _Required_Mixin_, _Primary_, _User_, _DB_Attr_
      type_name
        _Type_Name_Mixin_, Internal, _DB_System_, _DB_Attr_, _System_
      ui_display
        Computed, _Cached_, _Volatile_, _System_
      ui_repr
        Computed, _Cached_, _Volatile_, _System_
      x_locked
        Internal, _DB_System_, _DB_Attr_, _System_

"""

_test_fk_cols = """
    >>> apt, url = Scaffold.app_type_and_url (%(p1)s, %(n1)s)

    >>> for ETW in apt._SAW.e_types_t :
    ...     if ETW.fk_cols :
    ...         print (ETW.type_name)
    ...         for fkc in sorted (ETW.fk_cols, key = lambda x: x.name) :
    ...             print ("   ", formatted_column (fkc))
    MOM.MD_Change
        Column c_user                    : Integer              Internal__Computed__Sync_Change__Id_Entity_Reference Entity c_user Id_Entity()
        Column user                      : Integer              Internal__Computed__Sync_Change__Id_Entity_Reference Entity user Id_Entity()
    Auth.Account_in_Group
        Column left                      : Integer              Link_Role Account left Id_Entity()
        Column right                     : Integer              Link_Role Group right Id_Entity()
    Auth.Account_Activation
        Column left                      : Integer              Link_Role__Init_Only Account left Id_Entity()
    Auth.Account_Password_Change_Required
        Column left                      : Integer              Link_Role__Init_Only Account left Id_Entity()
    Auth.Account_EMail_Verification
        Column left                      : Integer              Link_Role__Init_Only Account left Id_Entity()
    Auth.Account_Password_Reset
        Column left                      : Integer              Link_Role__Init_Only Account left Id_Entity()
    EVT.Event
        Column calendar                  : Integer              Primary_Optional__Id_Entity_Reference Entity calendar Id_Entity()
        Column left                      : Integer              Link_Role__Init_Only Page left Id_Entity()
    EVT.Event_occurs
        Column left                      : Integer              Link_Role__Init_Only Event left Id_Entity()
    EVT.Recurrence_Spec
        Column left                      : Integer              Link_Role__Init_Only Event left Id_Entity()
    EVT.Recurrence_Rule
        Column left                      : Integer              Link_Role__Init_Only Recurrence_Spec left Id_Entity()
    PAP.Address_Position
        Column left                      : Integer              Link_Role__Init_Only Address left Id_Entity()
    PAP.Subject_has_Property
        Column left                      : Integer              Link_Role Subject left Id_Entity()
        Column right                     : Integer              Link_Role Property right Id_Entity()
    PAP.Person_has_Account
        Column left                      : Integer              Link_Role Person left Id_Entity()
        Column right                     : Integer              Link_Role Account right Id_Entity()
    SRM.Boat
        Column left                      : Integer              Link_Role__Init_Only Boat_Class left Id_Entity()
    SRM.Regatta_Event
        Column club                      : Integer              Optional__Id_Entity_Reference Entity club Id_Entity()
    SWP.Clip_O
        Column left                      : Integer              Link_Role__Init_Only Object_PN left Id_Entity()
    SWP.Picture
        Column left                      : Integer              Link_Role__Init_Only Gallery left Id_Entity()
    SRM.Page
        Column event                     : Integer              Primary__Id_Entity_Reference Entity event Id_Entity()
    SRM.Regatta
        Column boat_class                : Integer              Primary__Id_Entity_Reference Entity boat_class Id_Entity()
        Column left                      : Integer              Link_Role__Init_Only Regatta_Event left Id_Entity()
    SRM.Sailor
        Column club                      : Integer              Primary_Optional__Id_Entity_Reference Entity club Id_Entity()
        Column left                      : Integer              Link_Role__Init_Only Person left Id_Entity()
    SRM.Boat_in_Regatta
        Column left                      : Integer              Link_Role Boat left Id_Entity()
        Column right                     : Integer              Link_Role Regatta right Id_Entity()
        Column skipper                   : Integer              Required__Id_Entity_Reference Entity skipper Id_Entity()
    SRM.Race_Result
        Column left                      : Integer              Link_Role__Init_Only Boat_in_Regatta left Id_Entity()
    SRM.Team
        Column club                      : Integer              Optional__Id_Entity_Reference Entity club Id_Entity()
        Column leader                    : Integer              Optional__Id_Entity_Reference Entity leader Id_Entity()
        Column left                      : Integer              Link_Role__Init_Only Regatta_C left Id_Entity()
    SRM.Crew_Member
        Column left                      : Integer              Link_Role Boat_in_Regatta left Id_Entity()
        Column right                     : Integer              Link_Role Sailor right Id_Entity()
    SRM.Team_has_Boat_in_Regatta
        Column left                      : Integer              Link_Role Team left Id_Entity()
        Column right                     : Integer              Link_Role Boat_in_Regatta right Id_Entity()

"""

_test_key_o_p = """
    >>> apt, url = Scaffold.app_type_and_url (%(p1)s, %(n1)s)

    >>> show_key_o_p (apt)
    MOM.Id_Entity                            : pid             None
    MOM.MD_Change                            : cid             None
    Auth._Account_                           : None            pid
    Auth.Account_Anonymous                   : None            pid
    Auth.Account                             : None            pid
    Auth.Certificate                         : cert_id         pid
    Auth.Group                               : None            pid
    Auth.Account_in_Group                    : None            pid
    Auth.Account_Activation                  : None            pid
    Auth.Account_Password_Change_Required    : None            pid
    Auth.Account_EMail_Verification          : None            pid
    Auth.Account_Password_Reset              : None            pid
    EVT.Calendar                             : None            pid
    SWP.Page                                 : None            pid
    SWP.Page_Y                               : None            pid
    EVT.Event                                : None            pid
    EVT.Event_occurs                         : None            pid
    EVT.Recurrence_Spec                      : None            pid
    EVT.Recurrence_Rule                      : None            pid
    PAP.Address                              : None            pid
    PAP.Company                              : None            pid
    PAP.Email                                : None            pid
    PAP.Phone                                : None            pid
    PAP.Person                               : None            pid
    PAP.Url                                  : None            pid
    PAP.Address_Position                     : None            pid
    PAP.Subject_has_Property                 : None            pid
    PAP.Person_has_Account                   : None            pid
    SRM._Boat_Class_                         : None            pid
    SRM.Boat_Class                           : None            pid
    SRM.Handicap                             : None            pid
    SRM.Boat                                 : None            pid
    SRM.Club                                 : None            pid
    SRM.Regatta_Event                        : None            pid
    SWP.Clip_O                               : None            pid
    SWP.Clip_X                               : None            pid
    SWP.Gallery                              : None            pid
    SWP.Picture                              : None            pid
    SRM.Page                                 : None            pid
    SRM.Regatta                              : None            pid
    SRM.Regatta_C                            : None            pid
    SRM.Regatta_H                            : None            pid
    SRM.Sailor                               : None            pid
    SRM.Boat_in_Regatta                      : None            pid
    SRM.Race_Result                          : None            pid
    SRM.Team                                 : None            pid
    SRM.Crew_Member                          : None            pid
    SRM.Team_has_Boat_in_Regatta             : None            pid
    PAP.Subject_has_Phone                    : None            pid
    PAP.Company_has_Url                      : None            pid
    PAP.Person_has_Url                       : None            pid
    PAP.Company_has_Phone                    : None            pid
    PAP.Person_has_Phone                     : None            pid
    PAP.Company_has_Email                    : None            pid
    PAP.Person_has_Email                     : None            pid
    PAP.Company_has_Address                  : None            pid
    PAP.Person_has_Address                   : None            pid


"""

_test_parents = """
    >>> apt, url = Scaffold.app_type_and_url (%(p1)s, %(n1)s)

    >>> ETW = apt ["SRM.Page"]._SAW

    >>> print (ETW)
    <SAW : SRM.Page [srm_page : swp_page : mom_id_entity]>

    >>> print (nl.join (str (a) for a in ETW.ancestors)) ### SRM.Page
    <SAW : SWP.Page [swp_page : mom_id_entity]>
    <SAW : MOM.Id_Entity [mom_id_entity]>

    >>> print (nl.join (str (t) for t in ETW.sa_tables)) ### SRM.Page
    mom_id_entity
    swp_page
    srm_page

    >>> ETW = apt ["PAP.Subject"]._SAW
    >>> print (nl.join (str (a) for a in ETW.ancestors)) ### PAP.Subject
    <SAW : MOM.Id_Entity [mom_id_entity]>

    >>> print (nl.join (str (a) for a in ETW.children)) ### PAP.Subject
    <SAW : PAP.Company [pap_company : mom_id_entity]>
    <SAW : PAP.Person [pap_person : mom_id_entity]>

    >>> print (nl.join (str (t) for t in ETW.sa_tables)) ### PAP.Subject
    mom_id_entity
    pap_company
    pap_person

    >>> ETW = apt ["PAP.Person"]._SAW
    >>> print (nl.join (str (a) for a in ETW.ancestors)) ### PAP.Person
    <SAW : MOM.Id_Entity [mom_id_entity]>

    >>> print (nl.join (str (a) for a in ETW.children)) ### PAP.Person

    >>> print (nl.join (str (t) for t in ETW.sa_tables)) ### PAP.Person
    mom_id_entity
    pap_person

    >>> ETW = apt ["SRM.Regatta"]._SAW
    >>> print (nl.join (str (a) for a in ETW.ancestors)) ### SRM.Regatta
    <SAW : MOM.Id_Entity [mom_id_entity]>

    >>> print (nl.join (str (a) for a in ETW.children)) ### SRM.Regatta
    <SAW : SRM.Regatta_C [srm_regatta_c : srm_regatta : mom_id_entity]>
    <SAW : SRM.Regatta_H [srm_regatta_h : srm_regatta : mom_id_entity]>

    >>> print (nl.join (str (t) for t in ETW.sa_tables)) ### SRM.Regatta
    mom_id_entity
    srm_regatta
    srm_regatta_c

    >>> ETW = apt ["PAP.Subject_has_Property"]._SAW
    >>> print (nl.join (str (a) for a in ETW.ancestors)) ### PAP.Subject_has_Property
    <SAW : MOM.Id_Entity [mom_id_entity]>

    >>> print (nl.join (str (a) for a in ETW.children)) ### PAP.Subject_has_Property
    <SAW : PAP.Subject_has_Phone [pap_subject_has_phone : pap_subject_has_property : mom_id_entity]>
    <SAW : PAP.Company_has_Url [pap_company_has_url : pap_subject_has_property : mom_id_entity]>
    <SAW : PAP.Person_has_Url [pap_person_has_url : pap_subject_has_property : mom_id_entity]>
    <SAW : PAP.Company_has_Email [pap_company_has_email : pap_subject_has_property : mom_id_entity]>
    <SAW : PAP.Person_has_Email [pap_person_has_email : pap_subject_has_property : mom_id_entity]>
    <SAW : PAP.Company_has_Address [pap_company_has_address : pap_subject_has_property : mom_id_entity]>
    <SAW : PAP.Person_has_Address [pap_person_has_address : pap_subject_has_property : mom_id_entity]>

    >>> print (nl.join (str (t) for t in ETW.sa_tables)) ### PAP.Subject_has_Property
    mom_id_entity
    pap_subject_has_property
    pap_subject_has_phone

    >>> ETW = apt ["PAP.Subject_has_Phone"]._SAW
    >>> print (nl.join (str (a) for a in ETW.ancestors)) ### PAP.Subject_has_Phone
    <SAW : PAP.Subject_has_Property [pap_subject_has_property : mom_id_entity]>
    <SAW : MOM.Id_Entity [mom_id_entity]>

    >>> print (nl.join (str (a) for a in ETW.children)) ### PAP.Subject_has_Phone
    <SAW : PAP.Company_has_Phone [pap_company_has_phone : pap_subject_has_phone : pap_subject_has_property : mom_id_entity]>
    <SAW : PAP.Person_has_Phone [pap_person_has_phone : pap_subject_has_phone : pap_subject_has_property : mom_id_entity]>

    >>> print (nl.join (str (t) for t in ETW.sa_tables)) ### PAP.Subject_has_Phone
    mom_id_entity
    pap_subject_has_property
    pap_subject_has_phone

    >>> ETW = apt ["PAP.Person_has_Phone"]._SAW
    >>> print (nl.join (str (a) for a in ETW.ancestors)) ### PAP.Person_has_Phone
    <SAW : PAP.Subject_has_Phone [pap_subject_has_phone : pap_subject_has_property : mom_id_entity]>
    <SAW : PAP.Subject_has_Property [pap_subject_has_property : mom_id_entity]>
    <SAW : MOM.Id_Entity [mom_id_entity]>

    >>> print (nl.join (str (a) for a in ETW.children)) ### PAP.Person_has_Phone

    >>> print (nl.join (str (t) for t in ETW.sa_tables)) ### PAP.Person_has_Phone
    mom_id_entity
    pap_subject_has_property
    pap_subject_has_phone
    pap_person_has_phone

    >>> ETW = apt ["PAP.Person_has_Url"]._SAW
    >>> print (nl.join (str (a) for a in ETW.ancestors)) ### PAP.Person_has_Url
    <SAW : PAP.Subject_has_Property [pap_subject_has_property : mom_id_entity]>
    <SAW : MOM.Id_Entity [mom_id_entity]>

    >>> print (nl.join (str (a) for a in ETW.children)) ### PAP.Person_has_Url

    >>> print (nl.join (str (t) for t in ETW.sa_tables)) ### PAP.Person_has_Url
    mom_id_entity
    pap_subject_has_property
    pap_person_has_url

    >>> ETW = apt ["SRM.Regatta_C"]._SAW
    >>> print (nl.join (str (a) for a in ETW.ancestors)) ### SRM.Regatta_C
    <SAW : SRM.Regatta [srm_regatta : mom_id_entity]>
    <SAW : MOM.Id_Entity [mom_id_entity]>

    >>> print (nl.join (str (a) for a in ETW.children)) ### SRM.Regatta_C

    >>> print (nl.join (str (t) for t in ETW.sa_tables)) ### SRM.Regatta_C
    mom_id_entity
    srm_regatta
    srm_regatta_c

    >>> ETW = apt ["SRM.Regatta_H"]._SAW
    >>> print (ETW)
    <SAW : SRM.Regatta_H [srm_regatta_h : srm_regatta : mom_id_entity]>

    >>> print (nl.join (str (a) for a in ETW.ancestors)) ### SRM.Regatta_H
    <SAW : SRM.Regatta [srm_regatta : mom_id_entity]>
    <SAW : MOM.Id_Entity [mom_id_entity]>

    >>> print (nl.join (str (a) for a in ETW.children)) ### SRM.Regatta_H

    >>> print (nl.join (str (t) for t in ETW.sa_tables)) ### SRM.Regatta_H
    mom_id_entity
    srm_regatta
    srm_regatta_h


"""

_test_q_able = """
    >>> apt, url = Scaffold.app_type_and_url (%(p1)s, %(n1)s)

    >>> show_q_able (apt)
    <SAW : MOM.Id_Entity [mom_id_entity]>
      <SAW : Rev_Ref `creation`>
      <SAW : Boolean `electric` [mom_id_entity.electric]>
      <SAW : Rev_Ref `last_change`>
      <SAW : Int `last_cid` [mom_id_entity.last_cid]>
      <SAW : Surrogate `pid` [mom_id_entity.pid]>
      <SAW : String `type_name` [mom_id_entity.type_name]>
      <SAW : Boolean `x_locked` [mom_id_entity.x_locked]>
    <SAW : MOM.MD_Change [mom_md_change]>
      <SAW : Date-Time `c_time` [mom_md_change.c_time]>
      <SAW : Entity `c_user` [mom_md_change.c_user]>
      <SAW : Surrogate `cid` [mom_md_change.cid]>
      <SAW : String `kind` [mom_md_change.kind]>
      <SAW : Int `parent`>
      <SAW : Int `parent_cid` [mom_md_change.parent_cid]>
      <SAW : Int `pid` [mom_md_change.pid]>
      <SAW : Blob `scm_change` [mom_md_change.scm_change]>
      <SAW : Date-Time `time` [mom_md_change.time]>
      <SAW : String `type_name` [mom_md_change.type_name]>
      <SAW : Entity `user` [mom_md_change.user]>
    <SAW : MOM.Link [mom_id_entity]>
      <SAW : Rev_Ref `creation`>
      <SAW : Boolean `electric` [mom_id_entity.electric]>
      <SAW : Rev_Ref `last_change`>
      <SAW : Int `last_cid` [mom_id_entity.last_cid]>
      <SAW : Left `left` (Auth.Account_Activation | Auth.Account_EMail_Verification | Auth.Account_Password_Change_Required | Auth.Account_Password_Reset | Auth.Account_in_Group | EVT.Event | EVT.Event_occurs | EVT.Recurrence_Rule | EVT.Recurrence_Spec | PAP.Address_Position | PAP.Person_has_Account | PAP.Subject_has_Property | SRM.Boat | SRM.Boat_in_Regatta | SRM.Crew_Member | SRM.Race_Result | SRM.Regatta | SRM.Sailor | SRM.Team | SRM.Team_has_Boat_in_Regatta | SWP.Clip_O | SWP.Picture)>
      <SAW : Surrogate `pid` [mom_id_entity.pid]>
      <SAW : String `type_name` [mom_id_entity.type_name]>
      <SAW : Boolean `x_locked` [mom_id_entity.x_locked]>
    <SAW : MOM.Link1 [mom_id_entity]>
      <SAW : Rev_Ref `creation`>
      <SAW : Boolean `electric` [mom_id_entity.electric]>
      <SAW : Rev_Ref `last_change`>
      <SAW : Int `last_cid` [mom_id_entity.last_cid]>
      <SAW : Left `left` (Auth.Account_Activation | Auth.Account_EMail_Verification | Auth.Account_Password_Change_Required | Auth.Account_Password_Reset | EVT.Event | EVT.Event_occurs | EVT.Recurrence_Rule | EVT.Recurrence_Spec | PAP.Address_Position | SRM.Boat | SRM.Race_Result | SRM.Regatta | SRM.Sailor | SRM.Team | SWP.Clip_O | SWP.Picture)>
      <SAW : Surrogate `pid` [mom_id_entity.pid]>
      <SAW : String `type_name` [mom_id_entity.type_name]>
      <SAW : Boolean `x_locked` [mom_id_entity.x_locked]>
    <SAW : MOM._MOM_Link_n_ [mom_id_entity]>
      <SAW : Rev_Ref `creation`>
      <SAW : Boolean `electric` [mom_id_entity.electric]>
      <SAW : Rev_Ref `last_change`>
      <SAW : Int `last_cid` [mom_id_entity.last_cid]>
      <SAW : Left `left` (Auth.Account_in_Group | PAP.Person_has_Account | PAP.Subject_has_Property | SRM.Boat_in_Regatta | SRM.Crew_Member | SRM.Team_has_Boat_in_Regatta)>
      <SAW : Surrogate `pid` [mom_id_entity.pid]>
      <SAW : Right `right` (Auth.Account_in_Group | PAP.Person_has_Account | PAP.Subject_has_Property | SRM.Boat_in_Regatta | SRM.Crew_Member | SRM.Team_has_Boat_in_Regatta)>
      <SAW : String `type_name` [mom_id_entity.type_name]>
      <SAW : Boolean `x_locked` [mom_id_entity.x_locked]>
    <SAW : MOM.Link2 [mom_id_entity]>
      <SAW : Rev_Ref `creation`>
      <SAW : Boolean `electric` [mom_id_entity.electric]>
      <SAW : Rev_Ref `last_change`>
      <SAW : Int `last_cid` [mom_id_entity.last_cid]>
      <SAW : Left `left` (Auth.Account_in_Group | PAP.Person_has_Account | PAP.Subject_has_Property | SRM.Boat_in_Regatta | SRM.Crew_Member | SRM.Team_has_Boat_in_Regatta)>
      <SAW : Surrogate `pid` [mom_id_entity.pid]>
      <SAW : Right `right` (Auth.Account_in_Group | PAP.Person_has_Account | PAP.Subject_has_Property | SRM.Boat_in_Regatta | SRM.Crew_Member | SRM.Team_has_Boat_in_Regatta)>
      <SAW : String `type_name` [mom_id_entity.type_name]>
      <SAW : Boolean `x_locked` [mom_id_entity.x_locked]>
    <SAW : MOM.Link3 [mom_id_entity]>
      <SAW : Rev_Ref `creation`>
      <SAW : Boolean `electric` [mom_id_entity.electric]>
      <SAW : Rev_Ref `last_change`>
      <SAW : Int `last_cid` [mom_id_entity.last_cid]>
      <SAW : Left `left` ()>
      <SAW : Middle `middle` ()>
      <SAW : Surrogate `pid` [mom_id_entity.pid]>
      <SAW : Right `right` ()>
      <SAW : String `type_name` [mom_id_entity.type_name]>
      <SAW : Boolean `x_locked` [mom_id_entity.x_locked]>
    <SAW : MOM.Object [mom_id_entity]>
      <SAW : Rev_Ref `creation`>
      <SAW : Boolean `electric` [mom_id_entity.electric]>
      <SAW : Rev_Ref `last_change`>
      <SAW : Int `last_cid` [mom_id_entity.last_cid]>
      <SAW : Surrogate `pid` [mom_id_entity.pid]>
      <SAW : String `type_name` [mom_id_entity.type_name]>
      <SAW : Boolean `x_locked` [mom_id_entity.x_locked]>
    <SAW : Auth.Id_Entity [mom_id_entity]>
      <SAW : Rev_Ref `creation`>
      <SAW : Boolean `electric` [mom_id_entity.electric]>
      <SAW : Rev_Ref `last_change`>
      <SAW : Int `last_cid` [mom_id_entity.last_cid]>
      <SAW : Surrogate `pid` [mom_id_entity.pid]>
      <SAW : String `type_name` [mom_id_entity.type_name]>
      <SAW : Boolean `x_locked` [mom_id_entity.x_locked]>
    <SAW : Auth.Object [mom_id_entity]>
      <SAW : Rev_Ref `creation`>
      <SAW : Boolean `electric` [mom_id_entity.electric]>
      <SAW : Rev_Ref `last_change`>
      <SAW : Int `last_cid` [mom_id_entity.last_cid]>
      <SAW : Surrogate `pid` [mom_id_entity.pid]>
      <SAW : String `type_name` [mom_id_entity.type_name]>
      <SAW : Boolean `x_locked` [mom_id_entity.x_locked]>
    <SAW : Auth._Account_ [auth__account_ : mom_id_entity]>
      <SAW : Boolean `active`>
      <SAW : Rev_Ref `creation`>
      <SAW : Boolean `electric` [mom_id_entity.electric]>
      <SAW : Boolean `enabled` [auth__account_.enabled]>
      <SAW : Rev_Ref `last_change`>
      <SAW : Int `last_cid` [mom_id_entity.last_cid]>
      <SAW : Email `name` [auth__account_.name]>
      <SAW : Surrogate `pid` [mom_id_entity.pid]>
      <SAW : Boolean `superuser` [auth__account_.superuser]>
      <SAW : Boolean `suspended` [auth__account_.suspended]>
      <SAW : String `type_name` [mom_id_entity.type_name]>
      <SAW : Boolean `x_locked` [mom_id_entity.x_locked]>
    <SAW : Auth.Account_Anonymous [auth_account_anonymous : auth__account_ : mom_id_entity]>
      <SAW : Boolean `active`>
      <SAW : Rev_Ref `creation`>
      <SAW : Boolean `electric` [mom_id_entity.electric]>
      <SAW : Boolean `enabled` [auth__account_.enabled]>
      <SAW : Rev_Ref `last_change`>
      <SAW : Int `last_cid` [mom_id_entity.last_cid]>
      <SAW : Email `name` [auth__account_.name]>
      <SAW : Surrogate `pid` [mom_id_entity.pid]>
      <SAW : Boolean `superuser` [auth__account_.superuser]>
      <SAW : Boolean `suspended` [auth__account_.suspended]>
      <SAW : String `type_name` [mom_id_entity.type_name]>
      <SAW : Boolean `x_locked` [mom_id_entity.x_locked]>
    <SAW : Auth.Account [auth_account : auth__account_ : mom_id_entity]>
      <SAW : Link_Ref_List `_account_action_s`>
      <SAW : Link_Ref_List `_account_token_action_s`>
      <SAW : Link_Ref_List `account_email_verifications`>
      <SAW : Link_Ref_List `account_password_resets`>
      <SAW : Link_Ref `activation`>
      <SAW : Link_Ref_List `activations`>
      <SAW : Boolean `active`>
      <SAW : Rev_Ref `creation`>
      <SAW : Boolean `electric` [mom_id_entity.electric]>
      <SAW : Boolean `enabled` [auth__account_.enabled]>
      <SAW : Link_Ref_List `group_links`>
      <SAW : Role_Ref_Set `groups`>
      <SAW : Rev_Ref `last_change`>
      <SAW : Int `last_cid` [mom_id_entity.last_cid]>
      <SAW : Email `name` [auth__account_.name]>
      <SAW : String `password` [auth_account.password]>
      <SAW : Link_Ref `password_change_required`>
      <SAW : Link_Ref_List `password_change_requireds`>
      <SAW : Role_Ref `person`>
      <SAW : Link_Ref `person_link`>
      <SAW : Link_Ref_List `person_links`>
      <SAW : String `ph_name` [auth_account.ph_name]>
      <SAW : Surrogate `pid` [mom_id_entity.pid]>
      <SAW : Boolean `superuser` [auth__account_.superuser]>
      <SAW : Boolean `suspended` [auth__account_.suspended]>
      <SAW : String `type_name` [mom_id_entity.type_name]>
      <SAW : Boolean `x_locked` [mom_id_entity.x_locked]>
    <SAW : MOM.Date_Time_Interval []>
      <SAW : Boolean `alive`>
      <SAW : Date-Time `finish` [finish]>
      <SAW : Date-Time `start` [start]>
    <SAW : MOM.Date_Time_Interval_C []>
      <SAW : Boolean `alive`>
      <SAW : Date-Time `finish` [finish]>
      <SAW : Date-Time `start` [start]>
    <SAW : MOM.Date_Time_Interval_N []>
      <SAW : Boolean `alive`>
      <SAW : Date-Time `finish` [finish]>
      <SAW : Date-Time `start` [start]>
    <SAW : Auth.Certificate [auth_certificate : mom_id_entity]>
      <SAW : Boolean `alive`>
      <SAW : Surrogate `cert_id` [auth_certificate.cert_id]>
      <SAW : Rev_Ref `creation`>
      <SAW : String `desc` [auth_certificate.desc]>
      <SAW : Boolean `electric` [mom_id_entity.electric]>
      <SAW : Email `email` [auth_certificate.email]>
      <SAW : Rev_Ref `last_change`>
      <SAW : Int `last_cid` [mom_id_entity.last_cid]>
      <SAW : None `pem` [auth_certificate.pem]>
      <SAW : Surrogate `pid` [mom_id_entity.pid]>
      <SAW : Date-Time `revocation_date` [auth_certificate.revocation_date]>
      <SAW : String `type_name` [mom_id_entity.type_name]>
      <SAW : Date_Time_Interval `validity` [auth_certificate.validity__finish, auth_certificate.validity__start]>
      <SAW : Boolean `validity.alive`>
      <SAW : Boolean `x_locked` [mom_id_entity.x_locked]>
    <SAW : Auth.Group [auth_group : mom_id_entity]>
      <SAW : Link_Ref_List `account_links`>
      <SAW : Role_Ref_Set `accounts`>
      <SAW : Rev_Ref `creation`>
      <SAW : String `desc` [auth_group.desc]>
      <SAW : Boolean `electric` [mom_id_entity.electric]>
      <SAW : Rev_Ref `last_change`>
      <SAW : Int `last_cid` [mom_id_entity.last_cid]>
      <SAW : String `name` [auth_group.name]>
      <SAW : Surrogate `pid` [mom_id_entity.pid]>
      <SAW : String `type_name` [mom_id_entity.type_name]>
      <SAW : Boolean `x_locked` [mom_id_entity.x_locked]>
    <SAW : Auth.Link [mom_id_entity]>
      <SAW : Rev_Ref `creation`>
      <SAW : Boolean `electric` [mom_id_entity.electric]>
      <SAW : Rev_Ref `last_change`>
      <SAW : Int `last_cid` [mom_id_entity.last_cid]>
      <SAW : Left `left` (Auth.Account_Activation | Auth.Account_EMail_Verification | Auth.Account_Password_Change_Required | Auth.Account_Password_Reset | Auth.Account_in_Group)>
      <SAW : Surrogate `pid` [mom_id_entity.pid]>
      <SAW : String `type_name` [mom_id_entity.type_name]>
      <SAW : Boolean `x_locked` [mom_id_entity.x_locked]>
    <SAW : Auth._MOM_Link_n_ [mom_id_entity]>
      <SAW : Rev_Ref `creation`>
      <SAW : Boolean `electric` [mom_id_entity.electric]>
      <SAW : Rev_Ref `last_change`>
      <SAW : Int `last_cid` [mom_id_entity.last_cid]>
      <SAW : Left `left` (Auth.Account_in_Group)>
      <SAW : Surrogate `pid` [mom_id_entity.pid]>
      <SAW : Right `right` (Auth.Account_in_Group)>
      <SAW : String `type_name` [mom_id_entity.type_name]>
      <SAW : Boolean `x_locked` [mom_id_entity.x_locked]>
    <SAW : Auth.Link2 [mom_id_entity]>
      <SAW : Rev_Ref `creation`>
      <SAW : Boolean `electric` [mom_id_entity.electric]>
      <SAW : Rev_Ref `last_change`>
      <SAW : Int `last_cid` [mom_id_entity.last_cid]>
      <SAW : Left `left` (Auth.Account_in_Group)>
      <SAW : Surrogate `pid` [mom_id_entity.pid]>
      <SAW : Right `right` (Auth.Account_in_Group)>
      <SAW : String `type_name` [mom_id_entity.type_name]>
      <SAW : Boolean `x_locked` [mom_id_entity.x_locked]>
    <SAW : Auth.Account_in_Group [auth_account_in_group : mom_id_entity]>
      <SAW : Rev_Ref `creation`>
      <SAW : Boolean `electric` [mom_id_entity.electric]>
      <SAW : Rev_Ref `last_change`>
      <SAW : Int `last_cid` [mom_id_entity.last_cid]>
      <SAW : Account `left` [auth_account_in_group.left]>
      <SAW : Surrogate `pid` [mom_id_entity.pid]>
      <SAW : Group `right` [auth_account_in_group.right]>
      <SAW : String `type_name` [mom_id_entity.type_name]>
      <SAW : Boolean `x_locked` [mom_id_entity.x_locked]>
    <SAW : Auth.Link1 [mom_id_entity]>
      <SAW : Rev_Ref `creation`>
      <SAW : Boolean `electric` [mom_id_entity.electric]>
      <SAW : Rev_Ref `last_change`>
      <SAW : Int `last_cid` [mom_id_entity.last_cid]>
      <SAW : Left `left` (Auth.Account_Activation | Auth.Account_EMail_Verification | Auth.Account_Password_Change_Required | Auth.Account_Password_Reset)>
      <SAW : Surrogate `pid` [mom_id_entity.pid]>
      <SAW : String `type_name` [mom_id_entity.type_name]>
      <SAW : Boolean `x_locked` [mom_id_entity.x_locked]>
    <SAW : Auth._Account_Action_ [mom_id_entity]>
      <SAW : Rev_Ref `creation`>
      <SAW : Boolean `electric` [mom_id_entity.electric]>
      <SAW : Rev_Ref `last_change`>
      <SAW : Int `last_cid` [mom_id_entity.last_cid]>
      <SAW : Account `left` (Auth.Account_Activation | Auth.Account_EMail_Verification | Auth.Account_Password_Change_Required | Auth.Account_Password_Reset)>
      <SAW : Surrogate `pid` [mom_id_entity.pid]>
      <SAW : String `type_name` [mom_id_entity.type_name]>
      <SAW : Boolean `x_locked` [mom_id_entity.x_locked]>
    <SAW : Auth.Account_Activation [auth_account_activation : mom_id_entity]>
      <SAW : Rev_Ref `creation`>
      <SAW : Boolean `electric` [mom_id_entity.electric]>
      <SAW : Rev_Ref `last_change`>
      <SAW : Int `last_cid` [mom_id_entity.last_cid]>
      <SAW : Account `left` [auth_account_activation.left]>
      <SAW : Surrogate `pid` [mom_id_entity.pid]>
      <SAW : String `type_name` [mom_id_entity.type_name]>
      <SAW : Boolean `x_locked` [mom_id_entity.x_locked]>
    <SAW : Auth.Account_Password_Change_Required [auth_account_password_change_required : mom_id_entity]>
      <SAW : Rev_Ref `creation`>
      <SAW : Boolean `electric` [mom_id_entity.electric]>
      <SAW : Rev_Ref `last_change`>
      <SAW : Int `last_cid` [mom_id_entity.last_cid]>
      <SAW : Account `left` [auth_account_password_change_required.left]>
      <SAW : Surrogate `pid` [mom_id_entity.pid]>
      <SAW : String `type_name` [mom_id_entity.type_name]>
      <SAW : Boolean `x_locked` [mom_id_entity.x_locked]>
    <SAW : Auth._Account_Token_Action_ [mom_id_entity]>
      <SAW : Rev_Ref `creation`>
      <SAW : Boolean `electric` [mom_id_entity.electric]>
      <SAW : Date-Time `expires` (Auth.Account_EMail_Verification | Auth.Account_Password_Reset)>
      <SAW : Rev_Ref `last_change`>
      <SAW : Int `last_cid` [mom_id_entity.last_cid]>
      <SAW : Account `left` (Auth.Account_EMail_Verification | Auth.Account_Password_Reset)>
      <SAW : Surrogate `pid` [mom_id_entity.pid]>
      <SAW : String `token` (Auth.Account_EMail_Verification | Auth.Account_Password_Reset)>
      <SAW : String `type_name` [mom_id_entity.type_name]>
      <SAW : Boolean `x_locked` [mom_id_entity.x_locked]>
    <SAW : Auth.Account_EMail_Verification [auth_account_email_verification : mom_id_entity]>
      <SAW : Rev_Ref `creation`>
      <SAW : Boolean `electric` [mom_id_entity.electric]>
      <SAW : Date-Time `expires` [auth_account_email_verification.expires]>
      <SAW : Rev_Ref `last_change`>
      <SAW : Int `last_cid` [mom_id_entity.last_cid]>
      <SAW : Account `left` [auth_account_email_verification.left]>
      <SAW : Email `new_email` [auth_account_email_verification.new_email]>
      <SAW : Surrogate `pid` [mom_id_entity.pid]>
      <SAW : String `token` [auth_account_email_verification.token]>
      <SAW : String `type_name` [mom_id_entity.type_name]>
      <SAW : Boolean `x_locked` [mom_id_entity.x_locked]>
    <SAW : Auth.Account_Password_Reset [auth_account_password_reset : mom_id_entity]>
      <SAW : Rev_Ref `creation`>
      <SAW : Boolean `electric` [mom_id_entity.electric]>
      <SAW : Date-Time `expires` [auth_account_password_reset.expires]>
      <SAW : Rev_Ref `last_change`>
      <SAW : Int `last_cid` [mom_id_entity.last_cid]>
      <SAW : Account `left` [auth_account_password_reset.left]>
      <SAW : String `password` [auth_account_password_reset.password]>
      <SAW : Surrogate `pid` [mom_id_entity.pid]>
      <SAW : String `token` [auth_account_password_reset.token]>
      <SAW : String `type_name` [mom_id_entity.type_name]>
      <SAW : Boolean `x_locked` [mom_id_entity.x_locked]>
    <SAW : EVT.Id_Entity [mom_id_entity]>
      <SAW : Rev_Ref `creation`>
      <SAW : Boolean `electric` [mom_id_entity.electric]>
      <SAW : Rev_Ref `last_change`>
      <SAW : Int `last_cid` [mom_id_entity.last_cid]>
      <SAW : Surrogate `pid` [mom_id_entity.pid]>
      <SAW : String `type_name` [mom_id_entity.type_name]>
      <SAW : Boolean `x_locked` [mom_id_entity.x_locked]>
    <SAW : EVT.Object [mom_id_entity]>
      <SAW : Rev_Ref `creation`>
      <SAW : Boolean `electric` [mom_id_entity.electric]>
      <SAW : Rev_Ref `last_change`>
      <SAW : Int `last_cid` [mom_id_entity.last_cid]>
      <SAW : Surrogate `pid` [mom_id_entity.pid]>
      <SAW : String `type_name` [mom_id_entity.type_name]>
      <SAW : Boolean `x_locked` [mom_id_entity.x_locked]>
    <SAW : EVT.Calendar [evt_calendar : mom_id_entity]>
      <SAW : Rev_Ref `creation`>
      <SAW : String `desc` [evt_calendar.desc]>
      <SAW : Boolean `electric` [mom_id_entity.electric]>
      <SAW : Rev_Ref `last_change`>
      <SAW : Int `last_cid` [mom_id_entity.last_cid]>
      <SAW : Name `name` [evt_calendar.name]>
      <SAW : Surrogate `pid` [mom_id_entity.pid]>
      <SAW : String `type_name` [mom_id_entity.type_name]>
      <SAW : Boolean `x_locked` [mom_id_entity.x_locked]>
    <SAW : MOM.Date_Interval []>
      <SAW : Boolean `alive`>
      <SAW : Date `finish` [finish]>
      <SAW : Date `start` [start]>
    <SAW : MOM.Date_Interval_C []>
      <SAW : Boolean `alive`>
      <SAW : Date `finish` [finish]>
      <SAW : Date `start` [start]>
    <SAW : MOM.Date_Interval_N []>
      <SAW : Boolean `alive`>
      <SAW : Date `finish` [finish]>
      <SAW : Date `start` [start]>
    <SAW : MOM.Time_Interval []>
      <SAW : Time `finish` [finish]>
      <SAW : Time `start` [start]>
    <SAW : EVT.Link [mom_id_entity]>
      <SAW : Rev_Ref `creation`>
      <SAW : Boolean `electric` [mom_id_entity.electric]>
      <SAW : Rev_Ref `last_change`>
      <SAW : Int `last_cid` [mom_id_entity.last_cid]>
      <SAW : Left `left` (EVT.Event | EVT.Event_occurs | EVT.Recurrence_Rule | EVT.Recurrence_Spec)>
      <SAW : Surrogate `pid` [mom_id_entity.pid]>
      <SAW : String `type_name` [mom_id_entity.type_name]>
      <SAW : Boolean `x_locked` [mom_id_entity.x_locked]>
    <SAW : EVT.Link1 [mom_id_entity]>
      <SAW : Rev_Ref `creation`>
      <SAW : Boolean `electric` [mom_id_entity.electric]>
      <SAW : Rev_Ref `last_change`>
      <SAW : Int `last_cid` [mom_id_entity.last_cid]>
      <SAW : Left `left` (EVT.Event | EVT.Event_occurs | EVT.Recurrence_Rule | EVT.Recurrence_Spec)>
      <SAW : Surrogate `pid` [mom_id_entity.pid]>
      <SAW : String `type_name` [mom_id_entity.type_name]>
      <SAW : Boolean `x_locked` [mom_id_entity.x_locked]>
    <SAW : SWP.Id_Entity [mom_id_entity]>
      <SAW : Rev_Ref `creation`>
      <SAW : Boolean `electric` [mom_id_entity.electric]>
      <SAW : Rev_Ref `last_change`>
      <SAW : Int `last_cid` [mom_id_entity.last_cid]>
      <SAW : Surrogate `pid` [mom_id_entity.pid]>
      <SAW : String `type_name` [mom_id_entity.type_name]>
      <SAW : Boolean `x_locked` [mom_id_entity.x_locked]>
    <SAW : SWP.Object [mom_id_entity]>
      <SAW : Rev_Ref `creation`>
      <SAW : Boolean `electric` [mom_id_entity.electric]>
      <SAW : Rev_Ref `last_change`>
      <SAW : Int `last_cid` [mom_id_entity.last_cid]>
      <SAW : Surrogate `pid` [mom_id_entity.pid]>
      <SAW : String `type_name` [mom_id_entity.type_name]>
      <SAW : Boolean `x_locked` [mom_id_entity.x_locked]>
    <SAW : SWP.Object_PN [mom_id_entity]>
      <SAW : Link_Ref_List `clips`>
      <SAW : Rev_Ref `creation`>
      <SAW : Date_Interval `date` (SWP.Gallery | SWP.Page)>
      <SAW : Boolean `electric` [mom_id_entity.electric]>
      <SAW : Rev_Ref `last_change`>
      <SAW : Int `last_cid` [mom_id_entity.last_cid]>
      <SAW : Date-Slug `perma_name` (SWP.Gallery | SWP.Page)>
      <SAW : Surrogate `pid` [mom_id_entity.pid]>
      <SAW : String `short_title` (SWP.Gallery | SWP.Page)>
      <SAW : String `title` (SWP.Gallery | SWP.Page)>
      <SAW : String `type_name` [mom_id_entity.type_name]>
      <SAW : Boolean `x_locked` [mom_id_entity.x_locked]>
    <SAW : SWP.Page_Mixin []>
      <SAW : Text `contents` [contents]>
      <SAW : Format `format` [format]>
      <SAW : String `head_line` [head_line]>
      <SAW : Boolean `hidden` [hidden]>
      <SAW : Int `prio` [prio]>
      <SAW : Text `text` [text]>
    <SAW : SWP.Page [swp_page : mom_id_entity]>
      <SAW : Link_Ref_List `clips`>
      <SAW : Text `contents` [swp_page.contents]>
      <SAW : Rev_Ref `creation`>
      <SAW : Date_Interval `date` [swp_page.date__finish, swp_page.date__start]>
      <SAW : Boolean `date.alive`>
      <SAW : Boolean `electric` [mom_id_entity.electric]>
      <SAW : Link_Ref_List `events`>
      <SAW : Format `format` [swp_page.format]>
      <SAW : String `head_line` [swp_page.head_line]>
      <SAW : Boolean `hidden` [swp_page.hidden]>
      <SAW : Rev_Ref `last_change`>
      <SAW : Int `last_cid` [mom_id_entity.last_cid]>
      <SAW : Date-Slug `perma_name` [swp_page.perma_name]>
      <SAW : Surrogate `pid` [mom_id_entity.pid]>
      <SAW : Int `prio` [swp_page.prio]>
      <SAW : String `short_title` [swp_page.short_title]>
      <SAW : Text `text` [swp_page.text]>
      <SAW : String `title` [swp_page.title]>
      <SAW : String `type_name` [mom_id_entity.type_name]>
      <SAW : Boolean `x_locked` [mom_id_entity.x_locked]>
    <SAW : SWP.Page_Y [swp_page_y : swp_page : mom_id_entity]>
      <SAW : Link_Ref_List `clips`>
      <SAW : Text `contents` [swp_page.contents]>
      <SAW : Rev_Ref `creation`>
      <SAW : Date_Interval `date` [swp_page.date__finish, swp_page.date__start]>
      <SAW : Boolean `date.alive`>
      <SAW : Boolean `electric` [mom_id_entity.electric]>
      <SAW : Link_Ref_List `events`>
      <SAW : Format `format` [swp_page.format]>
      <SAW : String `head_line` [swp_page.head_line]>
      <SAW : Boolean `hidden` [swp_page.hidden]>
      <SAW : Rev_Ref `last_change`>
      <SAW : Int `last_cid` [mom_id_entity.last_cid]>
      <SAW : Date-Slug `perma_name` [swp_page.perma_name]>
      <SAW : Surrogate `pid` [mom_id_entity.pid]>
      <SAW : Int `prio` [swp_page.prio]>
      <SAW : String `short_title` [swp_page.short_title]>
      <SAW : Text `text` [swp_page.text]>
      <SAW : String `title` [swp_page.title]>
      <SAW : String `type_name` [mom_id_entity.type_name]>
      <SAW : Boolean `x_locked` [mom_id_entity.x_locked]>
      <SAW : Int `year` [swp_page_y.year]>
    <SAW : EVT.Event [evt_event : mom_id_entity]>
      <SAW : Entity `calendar` [evt_event.calendar]>
      <SAW : Rev_Ref `creation`>
      <SAW : Date_Interval `date` [evt_event.date__finish, evt_event.date__start]>
      <SAW : Boolean `date.alive`>
      <SAW : String `detail` [evt_event.detail]>
      <SAW : Boolean `electric` [mom_id_entity.electric]>
      <SAW : Rev_Ref `last_change`>
      <SAW : Int `last_cid` [mom_id_entity.last_cid]>
      <SAW : Page `left` [evt_event.left]>
      <SAW : Link_Ref_List `occurs`>
      <SAW : Surrogate `pid` [mom_id_entity.pid]>
      <SAW : Link_Ref `recurrence`>
      <SAW : String `short_title` [evt_event.short_title]>
      <SAW : Time_Interval `time` [evt_event.time__finish, evt_event.time__start]>
      <SAW : String `type_name` [mom_id_entity.type_name]>
      <SAW : Boolean `x_locked` [mom_id_entity.x_locked]>
    <SAW : EVT.Event_occurs [evt_event_occurs : mom_id_entity]>
      <SAW : Rev_Ref `creation`>
      <SAW : Date `date` [evt_event_occurs.date]>
      <SAW : Boolean `electric` [mom_id_entity.electric]>
      <SAW : Rev_Ref `last_change`>
      <SAW : Int `last_cid` [mom_id_entity.last_cid]>
      <SAW : Event `left` [evt_event_occurs.left]>
      <SAW : Surrogate `pid` [mom_id_entity.pid]>
      <SAW : Time_Interval `time` [evt_event_occurs.time__finish, evt_event_occurs.time__start]>
      <SAW : String `type_name` [mom_id_entity.type_name]>
      <SAW : Boolean `x_locked` [mom_id_entity.x_locked]>
    <SAW : EVT._Recurrence_Mixin_ [mom_id_entity]>
      <SAW : Rev_Ref `creation`>
      <SAW : Boolean `electric` [mom_id_entity.electric]>
      <SAW : Rev_Ref `last_change`>
      <SAW : Int `last_cid` [mom_id_entity.last_cid]>
      <SAW : Left `left` (EVT.Recurrence_Rule | EVT.Recurrence_Spec)>
      <SAW : Surrogate `pid` [mom_id_entity.pid]>
      <SAW : String `type_name` [mom_id_entity.type_name]>
      <SAW : Boolean `x_locked` [mom_id_entity.x_locked]>
    <SAW : EVT.Recurrence_Spec [evt_recurrence_spec : mom_id_entity]>
      <SAW : Rev_Ref `creation`>
      <SAW : Date_List `date_exceptions` [evt_recurrence_spec.date_exceptions]>
      <SAW : Date_List `dates` [evt_recurrence_spec.dates]>
      <SAW : Boolean `electric` [mom_id_entity.electric]>
      <SAW : Rev_Ref `last_change`>
      <SAW : Int `last_cid` [mom_id_entity.last_cid]>
      <SAW : Event `left` [evt_recurrence_spec.left]>
      <SAW : Surrogate `pid` [mom_id_entity.pid]>
      <SAW : Link_Ref_List `rules`>
      <SAW : String `type_name` [mom_id_entity.type_name]>
      <SAW : Boolean `x_locked` [mom_id_entity.x_locked]>
    <SAW : EVT.Recurrence_Rule [evt_recurrence_rule : mom_id_entity]>
      <SAW : Int `count` [evt_recurrence_rule.count]>
      <SAW : Rev_Ref `creation`>
      <SAW : String `desc` [evt_recurrence_rule.desc]>
      <SAW : Int_List `easter_offset` [evt_recurrence_rule.easter_offset]>
      <SAW : Boolean `electric` [mom_id_entity.electric]>
      <SAW : Date `finish` [evt_recurrence_rule.finish]>
      <SAW : Boolean `is_exception` [evt_recurrence_rule.is_exception]>
      <SAW : Rev_Ref `last_change`>
      <SAW : Int `last_cid` [mom_id_entity.last_cid]>
      <SAW : Recurrence_Spec `left` [evt_recurrence_rule.left]>
      <SAW : Int_List `month` [evt_recurrence_rule.month]>
      <SAW : Int_List `month_day` [evt_recurrence_rule.month_day]>
      <SAW : Int `period` [evt_recurrence_rule.period]>
      <SAW : Surrogate `pid` [mom_id_entity.pid]>
      <SAW : Int_List `restrict_pos` [evt_recurrence_rule.restrict_pos]>
      <SAW : Date `start` [evt_recurrence_rule.start]>
      <SAW : String `type_name` [mom_id_entity.type_name]>
      <SAW : Unit `unit` [evt_recurrence_rule.unit]>
      <SAW : Int_List `week` [evt_recurrence_rule.week]>
      <SAW : Weekday_RR_List `week_day` [evt_recurrence_rule.week_day]>
      <SAW : Boolean `x_locked` [mom_id_entity.x_locked]>
      <SAW : Int_List `year_day` [evt_recurrence_rule.year_day]>
    <SAW : MOM.Position []>
      <SAW : Float `height` [height]>
      <SAW : Angle `lat` [lat, __raw_lat]>
      <SAW : Angle `lon` [lon, __raw_lon]>
    <SAW : PAP.Id_Entity [mom_id_entity]>
      <SAW : Rev_Ref `creation`>
      <SAW : Boolean `electric` [mom_id_entity.electric]>
      <SAW : Rev_Ref `last_change`>
      <SAW : Int `last_cid` [mom_id_entity.last_cid]>
      <SAW : Surrogate `pid` [mom_id_entity.pid]>
      <SAW : String `type_name` [mom_id_entity.type_name]>
      <SAW : Boolean `x_locked` [mom_id_entity.x_locked]>
    <SAW : PAP.Object [mom_id_entity]>
      <SAW : Rev_Ref `creation`>
      <SAW : Boolean `electric` [mom_id_entity.electric]>
      <SAW : Rev_Ref `last_change`>
      <SAW : Int `last_cid` [mom_id_entity.last_cid]>
      <SAW : Surrogate `pid` [mom_id_entity.pid]>
      <SAW : String `type_name` [mom_id_entity.type_name]>
      <SAW : Boolean `x_locked` [mom_id_entity.x_locked]>
    <SAW : PAP.Property [mom_id_entity]>
      <SAW : Rev_Ref `creation`>
      <SAW : String `desc` (PAP.Address | PAP.Email | PAP.Phone | PAP.Url)>
      <SAW : Boolean `electric` [mom_id_entity.electric]>
      <SAW : Rev_Ref `last_change`>
      <SAW : Int `last_cid` [mom_id_entity.last_cid]>
      <SAW : Surrogate `pid` [mom_id_entity.pid]>
      <SAW : Link_Ref_List `subject_links`>
      <SAW : String `type_name` [mom_id_entity.type_name]>
      <SAW : Boolean `x_locked` [mom_id_entity.x_locked]>
    <SAW : PAP.Address [pap_address : mom_id_entity]>
      <SAW : String `city` [pap_address.city, pap_address.__raw_city]>
      <SAW : Role_Ref_Set `companies`>
      <SAW : Link_Ref_List `company_links`>
      <SAW : String `country` [pap_address.country, pap_address.__raw_country]>
      <SAW : Rev_Ref `creation`>
      <SAW : String `desc` [pap_address.desc]>
      <SAW : Boolean `electric` [mom_id_entity.electric]>
      <SAW : Link_Ref `gps`>
      <SAW : Rev_Ref `last_change`>
      <SAW : Int `last_cid` [mom_id_entity.last_cid]>
      <SAW : Link_Ref_List `person_links`>
      <SAW : Role_Ref_Set `persons`>
      <SAW : Surrogate `pid` [mom_id_entity.pid]>
      <SAW : String `region` [pap_address.region, pap_address.__raw_region]>
      <SAW : String `street` [pap_address.street, pap_address.__raw_street]>
      <SAW : Link_Ref_List `subject_links`>
      <SAW : String `type_name` [mom_id_entity.type_name]>
      <SAW : Boolean `x_locked` [mom_id_entity.x_locked]>
      <SAW : String `zip` [pap_address.zip, pap_address.__raw_zip]>
    <SAW : PAP.Subject [mom_id_entity]>
      <SAW : Link_Ref_List `address_links`>
      <SAW : Role_Ref_Set `addresses`>
      <SAW : Rev_Ref `creation`>
      <SAW : Boolean `electric` [mom_id_entity.electric]>
      <SAW : Link_Ref_List `email_links`>
      <SAW : Role_Ref_Set `emails`>
      <SAW : Rev_Ref `last_change`>
      <SAW : Int `last_cid` [mom_id_entity.last_cid]>
      <SAW : Date_Interval `lifetime` (PAP.Company | PAP.Person)>
      <SAW : Link_Ref_List `phone_links`>
      <SAW : Role_Ref_Set `phones`>
      <SAW : Surrogate `pid` [mom_id_entity.pid]>
      <SAW : Link_Ref_List `property_links`>
      <SAW : String `type_name` [mom_id_entity.type_name]>
      <SAW : Link_Ref_List `url_links`>
      <SAW : Role_Ref_Set `urls`>
      <SAW : Boolean `x_locked` [mom_id_entity.x_locked]>
    <SAW : PAP.Legal_Entity [mom_id_entity]>
      <SAW : Link_Ref_List `address_links`>
      <SAW : Role_Ref_Set `addresses`>
      <SAW : Rev_Ref `creation`>
      <SAW : Boolean `electric` [mom_id_entity.electric]>
      <SAW : Link_Ref_List `email_links`>
      <SAW : Role_Ref_Set `emails`>
      <SAW : Rev_Ref `last_change`>
      <SAW : Int `last_cid` [mom_id_entity.last_cid]>
      <SAW : Date_Interval `lifetime` (PAP.Company)>
      <SAW : String `name` (PAP.Company)>
      <SAW : Link_Ref_List `phone_links`>
      <SAW : Role_Ref_Set `phones`>
      <SAW : Surrogate `pid` [mom_id_entity.pid]>
      <SAW : Link_Ref_List `property_links`>
      <SAW : String `short_name` (PAP.Company)>
      <SAW : String `type_name` [mom_id_entity.type_name]>
      <SAW : Link_Ref_List `url_links`>
      <SAW : Role_Ref_Set `urls`>
      <SAW : Boolean `x_locked` [mom_id_entity.x_locked]>
    <SAW : PAP.Company [pap_company : mom_id_entity]>
      <SAW : Link_Ref_List `address_links`>
      <SAW : Role_Ref_Set `addresses`>
      <SAW : Rev_Ref `creation`>
      <SAW : Boolean `electric` [mom_id_entity.electric]>
      <SAW : Link_Ref_List `email_links`>
      <SAW : Role_Ref_Set `emails`>
      <SAW : Rev_Ref `last_change`>
      <SAW : Int `last_cid` [mom_id_entity.last_cid]>
      <SAW : Date_Interval `lifetime` [pap_company.lifetime__finish, pap_company.lifetime__start]>
      <SAW : Boolean `lifetime.alive`>
      <SAW : String `name` [pap_company.name, pap_company.__raw_name]>
      <SAW : Link_Ref_List `phone_links`>
      <SAW : Role_Ref_Set `phones`>
      <SAW : Surrogate `pid` [mom_id_entity.pid]>
      <SAW : Link_Ref_List `property_links`>
      <SAW : String `registered_in` [pap_company.registered_in, pap_company.__raw_registered_in]>
      <SAW : String `short_name` [pap_company.short_name, pap_company.__raw_short_name]>
      <SAW : String `type_name` [mom_id_entity.type_name]>
      <SAW : Link_Ref_List `url_links`>
      <SAW : Role_Ref_Set `urls`>
      <SAW : Boolean `x_locked` [mom_id_entity.x_locked]>
    <SAW : PAP.Email [pap_email : mom_id_entity]>
      <SAW : Email `address` [pap_email.address, pap_email.__raw_address]>
      <SAW : Role_Ref_Set `companies`>
      <SAW : Link_Ref_List `company_links`>
      <SAW : Rev_Ref `creation`>
      <SAW : String `desc` [pap_email.desc]>
      <SAW : Boolean `electric` [mom_id_entity.electric]>
      <SAW : Rev_Ref `last_change`>
      <SAW : Int `last_cid` [mom_id_entity.last_cid]>
      <SAW : Link_Ref_List `person_links`>
      <SAW : Role_Ref_Set `persons`>
      <SAW : Surrogate `pid` [mom_id_entity.pid]>
      <SAW : Link_Ref_List `subject_links`>
      <SAW : String `type_name` [mom_id_entity.type_name]>
      <SAW : Boolean `x_locked` [mom_id_entity.x_locked]>
    <SAW : PAP.Phone [pap_phone : mom_id_entity]>
      <SAW : Numeric_String `area_code` [pap_phone.area_code]>
      <SAW : Role_Ref_Set `companies`>
      <SAW : Link_Ref_List `company_links`>
      <SAW : Numeric_String `country_code` [pap_phone.country_code]>
      <SAW : Rev_Ref `creation`>
      <SAW : String `desc` [pap_phone.desc]>
      <SAW : Boolean `electric` [mom_id_entity.electric]>
      <SAW : Rev_Ref `last_change`>
      <SAW : Int `last_cid` [mom_id_entity.last_cid]>
      <SAW : Numeric_String `number` [pap_phone.number]>
      <SAW : Link_Ref_List `person_links`>
      <SAW : Role_Ref_Set `persons`>
      <SAW : Surrogate `pid` [mom_id_entity.pid]>
      <SAW : Link_Ref_List `subject_links`>
      <SAW : String `type_name` [mom_id_entity.type_name]>
      <SAW : Boolean `x_locked` [mom_id_entity.x_locked]>
    <SAW : PAP.Person [pap_person : mom_id_entity]>
      <SAW : Link_Ref_List `account_links`>
      <SAW : Role_Ref_Set `accounts`>
      <SAW : Link_Ref_List `address_links`>
      <SAW : Role_Ref_Set `addresses`>
      <SAW : Rev_Ref `creation`>
      <SAW : Boolean `electric` [mom_id_entity.electric]>
      <SAW : Link_Ref_List `email_links`>
      <SAW : Role_Ref_Set `emails`>
      <SAW : String `first_name` [pap_person.first_name, pap_person.__raw_first_name]>
      <SAW : Rev_Ref `last_change`>
      <SAW : Int `last_cid` [mom_id_entity.last_cid]>
      <SAW : String `last_name` [pap_person.last_name, pap_person.__raw_last_name]>
      <SAW : Date_Interval `lifetime` [pap_person.lifetime__finish, pap_person.lifetime__start]>
      <SAW : Boolean `lifetime.alive`>
      <SAW : String `middle_name` [pap_person.middle_name, pap_person.__raw_middle_name]>
      <SAW : Link_Ref_List `phone_links`>
      <SAW : Role_Ref_Set `phones`>
      <SAW : Surrogate `pid` [mom_id_entity.pid]>
      <SAW : Link_Ref_List `property_links`>
      <SAW : Link_Ref_List `sailors`>
      <SAW : Sex `sex` [pap_person.sex]>
      <SAW : String `title` [pap_person.title, pap_person.__raw_title]>
      <SAW : String `type_name` [mom_id_entity.type_name]>
      <SAW : Link_Ref_List `url_links`>
      <SAW : Role_Ref_Set `urls`>
      <SAW : Boolean `x_locked` [mom_id_entity.x_locked]>
    <SAW : PAP.Url [pap_url : mom_id_entity]>
      <SAW : Role_Ref_Set `companies`>
      <SAW : Link_Ref_List `company_links`>
      <SAW : Rev_Ref `creation`>
      <SAW : String `desc` [pap_url.desc]>
      <SAW : Boolean `electric` [mom_id_entity.electric]>
      <SAW : Rev_Ref `last_change`>
      <SAW : Int `last_cid` [mom_id_entity.last_cid]>
      <SAW : Link_Ref_List `person_links`>
      <SAW : Role_Ref_Set `persons`>
      <SAW : Surrogate `pid` [mom_id_entity.pid]>
      <SAW : Link_Ref_List `subject_links`>
      <SAW : String `type_name` [mom_id_entity.type_name]>
      <SAW : Url `value` [pap_url.value]>
      <SAW : Boolean `x_locked` [mom_id_entity.x_locked]>
    <SAW : PAP.Link [mom_id_entity]>
      <SAW : Rev_Ref `creation`>
      <SAW : Boolean `electric` [mom_id_entity.electric]>
      <SAW : Rev_Ref `last_change`>
      <SAW : Int `last_cid` [mom_id_entity.last_cid]>
      <SAW : Left `left` (PAP.Address_Position | PAP.Person_has_Account | PAP.Subject_has_Property)>
      <SAW : Surrogate `pid` [mom_id_entity.pid]>
      <SAW : String `type_name` [mom_id_entity.type_name]>
      <SAW : Boolean `x_locked` [mom_id_entity.x_locked]>
    <SAW : PAP.Link1 [mom_id_entity]>
      <SAW : Rev_Ref `creation`>
      <SAW : Boolean `electric` [mom_id_entity.electric]>
      <SAW : Rev_Ref `last_change`>
      <SAW : Int `last_cid` [mom_id_entity.last_cid]>
      <SAW : Left `left` (PAP.Address_Position)>
      <SAW : Surrogate `pid` [mom_id_entity.pid]>
      <SAW : String `type_name` [mom_id_entity.type_name]>
      <SAW : Boolean `x_locked` [mom_id_entity.x_locked]>
    <SAW : PAP.Address_Position [pap_address_position : mom_id_entity]>
      <SAW : Rev_Ref `creation`>
      <SAW : Boolean `electric` [mom_id_entity.electric]>
      <SAW : Rev_Ref `last_change`>
      <SAW : Int `last_cid` [mom_id_entity.last_cid]>
      <SAW : Address `left` [pap_address_position.left]>
      <SAW : Surrogate `pid` [mom_id_entity.pid]>
      <SAW : Position `position` [pap_address_position.position__height, pap_address_position.position__lat, pap_address_position.position____raw_lat, pap_address_position.position__lon, pap_address_position.position____raw_lon]>
      <SAW : String `type_name` [mom_id_entity.type_name]>
      <SAW : Boolean `x_locked` [mom_id_entity.x_locked]>
    <SAW : PAP._MOM_Link_n_ [mom_id_entity]>
      <SAW : Rev_Ref `creation`>
      <SAW : Boolean `electric` [mom_id_entity.electric]>
      <SAW : Rev_Ref `last_change`>
      <SAW : Int `last_cid` [mom_id_entity.last_cid]>
      <SAW : Left `left` (PAP.Person_has_Account | PAP.Subject_has_Property)>
      <SAW : Surrogate `pid` [mom_id_entity.pid]>
      <SAW : Right `right` (PAP.Person_has_Account | PAP.Subject_has_Property)>
      <SAW : String `type_name` [mom_id_entity.type_name]>
      <SAW : Boolean `x_locked` [mom_id_entity.x_locked]>
    <SAW : PAP.Link2 [mom_id_entity]>
      <SAW : Rev_Ref `creation`>
      <SAW : Boolean `electric` [mom_id_entity.electric]>
      <SAW : Rev_Ref `last_change`>
      <SAW : Int `last_cid` [mom_id_entity.last_cid]>
      <SAW : Left `left` (PAP.Person_has_Account | PAP.Subject_has_Property)>
      <SAW : Surrogate `pid` [mom_id_entity.pid]>
      <SAW : Right `right` (PAP.Person_has_Account | PAP.Subject_has_Property)>
      <SAW : String `type_name` [mom_id_entity.type_name]>
      <SAW : Boolean `x_locked` [mom_id_entity.x_locked]>
    <SAW : PAP.Subject_has_Property [pap_subject_has_property : mom_id_entity]>
      <SAW : Rev_Ref `creation`>
      <SAW : String `desc` [pap_subject_has_property.desc]>
      <SAW : Boolean `electric` [mom_id_entity.electric]>
      <SAW : Rev_Ref `last_change`>
      <SAW : Int `last_cid` [mom_id_entity.last_cid]>
      <SAW : Subject `left` [pap_subject_has_property.left]>
      <SAW : Surrogate `pid` [mom_id_entity.pid]>
      <SAW : Property `right` [pap_subject_has_property.right]>
      <SAW : String `type_name` [mom_id_entity.type_name]>
      <SAW : Boolean `x_locked` [mom_id_entity.x_locked]>
    <SAW : PAP.Person_has_Account [pap_person_has_account : mom_id_entity]>
      <SAW : Rev_Ref `creation`>
      <SAW : Boolean `electric` [mom_id_entity.electric]>
      <SAW : Rev_Ref `last_change`>
      <SAW : Int `last_cid` [mom_id_entity.last_cid]>
      <SAW : Person `left` [pap_person_has_account.left]>
      <SAW : Surrogate `pid` [mom_id_entity.pid]>
      <SAW : Account `right` [pap_person_has_account.right]>
      <SAW : String `type_name` [mom_id_entity.type_name]>
      <SAW : Boolean `x_locked` [mom_id_entity.x_locked]>
    <SAW : SRM.Regatta_Result []>
      <SAW : Date-Time `date` [date]>
      <SAW : String `software` [software]>
      <SAW : String `status` [status]>
    <SAW : SRM.Id_Entity [mom_id_entity]>
      <SAW : Rev_Ref `creation`>
      <SAW : Boolean `electric` [mom_id_entity.electric]>
      <SAW : Rev_Ref `last_change`>
      <SAW : Int `last_cid` [mom_id_entity.last_cid]>
      <SAW : Surrogate `pid` [mom_id_entity.pid]>
      <SAW : String `type_name` [mom_id_entity.type_name]>
      <SAW : Boolean `x_locked` [mom_id_entity.x_locked]>
    <SAW : SRM.Object [mom_id_entity]>
      <SAW : Rev_Ref `creation`>
      <SAW : Boolean `electric` [mom_id_entity.electric]>
      <SAW : Rev_Ref `last_change`>
      <SAW : Int `last_cid` [mom_id_entity.last_cid]>
      <SAW : Surrogate `pid` [mom_id_entity.pid]>
      <SAW : String `type_name` [mom_id_entity.type_name]>
      <SAW : Boolean `x_locked` [mom_id_entity.x_locked]>
    <SAW : SRM._Boat_Class_ [srm__boat_class_ : mom_id_entity]>
      <SAW : Rev_Ref `creation`>
      <SAW : Boolean `electric` [mom_id_entity.electric]>
      <SAW : Rev_Ref `last_change`>
      <SAW : Int `last_cid` [mom_id_entity.last_cid]>
      <SAW : String `name` [srm__boat_class_.name, srm__boat_class_.__raw_name]>
      <SAW : Surrogate `pid` [mom_id_entity.pid]>
      <SAW : String `type_name` [mom_id_entity.type_name]>
      <SAW : Boolean `x_locked` [mom_id_entity.x_locked]>
    <SAW : SRM.Boat_Class [srm_boat_class : srm__boat_class_ : mom_id_entity]>
      <SAW : Float `beam` [srm_boat_class.beam]>
      <SAW : Link_Ref_List `boats`>
      <SAW : Rev_Ref `creation`>
      <SAW : Boolean `electric` [mom_id_entity.electric]>
      <SAW : Rev_Ref `last_change`>
      <SAW : Int `last_cid` [mom_id_entity.last_cid]>
      <SAW : Float `loa` [srm_boat_class.loa]>
      <SAW : Int `max_crew` [srm_boat_class.max_crew]>
      <SAW : String `name` [srm__boat_class_.name, srm__boat_class_.__raw_name]>
      <SAW : Surrogate `pid` [mom_id_entity.pid]>
      <SAW : Float `sail_area` [srm_boat_class.sail_area]>
      <SAW : String `type_name` [mom_id_entity.type_name]>
      <SAW : Boolean `x_locked` [mom_id_entity.x_locked]>
    <SAW : SRM.Handicap [srm_handicap : srm__boat_class_ : mom_id_entity]>
      <SAW : Rev_Ref `creation`>
      <SAW : Boolean `electric` [mom_id_entity.electric]>
      <SAW : Rev_Ref `last_change`>
      <SAW : Int `last_cid` [mom_id_entity.last_cid]>
      <SAW : String `name` [srm__boat_class_.name, srm__boat_class_.__raw_name]>
      <SAW : Surrogate `pid` [mom_id_entity.pid]>
      <SAW : String `type_name` [mom_id_entity.type_name]>
      <SAW : Boolean `x_locked` [mom_id_entity.x_locked]>
    <SAW : SRM.Link [mom_id_entity]>
      <SAW : Rev_Ref `creation`>
      <SAW : Boolean `electric` [mom_id_entity.electric]>
      <SAW : Rev_Ref `last_change`>
      <SAW : Int `last_cid` [mom_id_entity.last_cid]>
      <SAW : Left `left` (SRM.Boat | SRM.Boat_in_Regatta | SRM.Crew_Member | SRM.Race_Result | SRM.Regatta | SRM.Sailor | SRM.Team | SRM.Team_has_Boat_in_Regatta)>
      <SAW : Surrogate `pid` [mom_id_entity.pid]>
      <SAW : String `type_name` [mom_id_entity.type_name]>
      <SAW : Boolean `x_locked` [mom_id_entity.x_locked]>
    <SAW : SRM.Link1 [mom_id_entity]>
      <SAW : Rev_Ref `creation`>
      <SAW : Boolean `electric` [mom_id_entity.electric]>
      <SAW : Rev_Ref `last_change`>
      <SAW : Int `last_cid` [mom_id_entity.last_cid]>
      <SAW : Left `left` (SRM.Boat | SRM.Race_Result | SRM.Regatta | SRM.Sailor | SRM.Team)>
      <SAW : Surrogate `pid` [mom_id_entity.pid]>
      <SAW : String `type_name` [mom_id_entity.type_name]>
      <SAW : Boolean `x_locked` [mom_id_entity.x_locked]>
    <SAW : SRM.Boat [srm_boat : mom_id_entity]>
      <SAW : Rev_Ref `creation`>
      <SAW : Boolean `electric` [mom_id_entity.electric]>
      <SAW : Rev_Ref `last_change`>
      <SAW : Int `last_cid` [mom_id_entity.last_cid]>
      <SAW : Boat_Class `left` [srm_boat.left]>
      <SAW : String `name` [srm_boat.name]>
      <SAW : Nation `nation` [srm_boat.nation]>
      <SAW : Surrogate `pid` [mom_id_entity.pid]>
      <SAW : Link_Ref_List `regatta_links`>
      <SAW : Int `sail_number` [srm_boat.sail_number, srm_boat.__raw_sail_number]>
      <SAW : String `sail_number_x` [srm_boat.sail_number_x, srm_boat.__raw_sail_number_x]>
      <SAW : String `type_name` [mom_id_entity.type_name]>
      <SAW : Boolean `x_locked` [mom_id_entity.x_locked]>
    <SAW : SRM.Club [srm_club : mom_id_entity]>
      <SAW : Rev_Ref `creation`>
      <SAW : Boolean `electric` [mom_id_entity.electric]>
      <SAW : Rev_Ref `last_change`>
      <SAW : Int `last_cid` [mom_id_entity.last_cid]>
      <SAW : String `long_name` [srm_club.long_name]>
      <SAW : String `name` [srm_club.name, srm_club.__raw_name]>
      <SAW : Surrogate `pid` [mom_id_entity.pid]>
      <SAW : String `type_name` [mom_id_entity.type_name]>
      <SAW : Boolean `x_locked` [mom_id_entity.x_locked]>
    <SAW : SRM.Regatta_Event [srm_regatta_event : mom_id_entity]>
      <SAW : Entity `club` [srm_regatta_event.club]>
      <SAW : Rev_Ref `creation`>
      <SAW : Date_Interval `date` [srm_regatta_event.date__finish, srm_regatta_event.date__start]>
      <SAW : Boolean `date.alive`>
      <SAW : String `desc` [srm_regatta_event.desc]>
      <SAW : Boolean `electric` [mom_id_entity.electric]>
      <SAW : Boolean `is_cancelled` [srm_regatta_event.is_cancelled]>
      <SAW : Rev_Ref `last_change`>
      <SAW : Int `last_cid` [mom_id_entity.last_cid]>
      <SAW : String `name` [srm_regatta_event.name, srm_regatta_event.__raw_name]>
      <SAW : String `perma_name` [srm_regatta_event.perma_name]>
      <SAW : Surrogate `pid` [mom_id_entity.pid]>
      <SAW : Link_Ref_List `regattas`>
      <SAW : String `type_name` [mom_id_entity.type_name]>
      <SAW : Boolean `x_locked` [mom_id_entity.x_locked]>
      <SAW : Int `year`>
    <SAW : SWP.Link [mom_id_entity]>
      <SAW : Rev_Ref `creation`>
      <SAW : Boolean `electric` [mom_id_entity.electric]>
      <SAW : Rev_Ref `last_change`>
      <SAW : Int `last_cid` [mom_id_entity.last_cid]>
      <SAW : Left `left` (SWP.Clip_O | SWP.Picture)>
      <SAW : Surrogate `pid` [mom_id_entity.pid]>
      <SAW : String `type_name` [mom_id_entity.type_name]>
      <SAW : Boolean `x_locked` [mom_id_entity.x_locked]>
    <SAW : SWP.Link1 [mom_id_entity]>
      <SAW : Rev_Ref `creation`>
      <SAW : Boolean `electric` [mom_id_entity.electric]>
      <SAW : Rev_Ref `last_change`>
      <SAW : Int `last_cid` [mom_id_entity.last_cid]>
      <SAW : Left `left` (SWP.Clip_O | SWP.Picture)>
      <SAW : Surrogate `pid` [mom_id_entity.pid]>
      <SAW : String `type_name` [mom_id_entity.type_name]>
      <SAW : Boolean `x_locked` [mom_id_entity.x_locked]>
    <SAW : SWP.Clip_O [swp_clip_o : mom_id_entity]>
      <SAW : Text `abstract` [swp_clip_o.abstract]>
      <SAW : Text `contents` [swp_clip_o.contents]>
      <SAW : Rev_Ref `creation`>
      <SAW : Date_Interval `date` [swp_clip_o.date__finish, swp_clip_o.date__start]>
      <SAW : Boolean `date.alive`>
      <SAW : Date_Interval `date_x` [swp_clip_o.date_x__finish, swp_clip_o.date_x__start]>
      <SAW : Boolean `date_x.alive`>
      <SAW : Boolean `electric` [mom_id_entity.electric]>
      <SAW : Rev_Ref `last_change`>
      <SAW : Int `last_cid` [mom_id_entity.last_cid]>
      <SAW : Object_PN `left` [swp_clip_o.left]>
      <SAW : Surrogate `pid` [mom_id_entity.pid]>
      <SAW : Int `prio` [swp_clip_o.prio]>
      <SAW : String `type_name` [mom_id_entity.type_name]>
      <SAW : Boolean `x_locked` [mom_id_entity.x_locked]>
    <SAW : SWP.Clip_X [swp_clip_x : swp_page : mom_id_entity]>
      <SAW : Link_Ref_List `clips`>
      <SAW : Text `contents` [swp_page.contents]>
      <SAW : Rev_Ref `creation`>
      <SAW : Date_Interval `date` [swp_page.date__finish, swp_page.date__start]>
      <SAW : Boolean `date.alive`>
      <SAW : Boolean `electric` [mom_id_entity.electric]>
      <SAW : Link_Ref_List `events`>
      <SAW : Format `format` [swp_page.format]>
      <SAW : String `head_line` [swp_page.head_line]>
      <SAW : Boolean `hidden` [swp_page.hidden]>
      <SAW : Rev_Ref `last_change`>
      <SAW : Int `last_cid` [mom_id_entity.last_cid]>
      <SAW : Url `link_to` [swp_clip_x.link_to]>
      <SAW : Date-Slug `perma_name` [swp_page.perma_name]>
      <SAW : Surrogate `pid` [mom_id_entity.pid]>
      <SAW : Int `prio` [swp_page.prio]>
      <SAW : String `short_title` [swp_page.short_title]>
      <SAW : Text `text` [swp_page.text]>
      <SAW : String `title` [swp_page.title]>
      <SAW : String `type_name` [mom_id_entity.type_name]>
      <SAW : Boolean `x_locked` [mom_id_entity.x_locked]>
    <SAW : SWP.Gallery [swp_gallery : mom_id_entity]>
      <SAW : Link_Ref_List `clips`>
      <SAW : Rev_Ref `creation`>
      <SAW : Date_Interval `date` [swp_gallery.date__finish, swp_gallery.date__start]>
      <SAW : Boolean `date.alive`>
      <SAW : Directory `directory` [swp_gallery.directory]>
      <SAW : Boolean `electric` [mom_id_entity.electric]>
      <SAW : Rev_Ref `last_change`>
      <SAW : Int `last_cid` [mom_id_entity.last_cid]>
      <SAW : Date-Slug `perma_name` [swp_gallery.perma_name]>
      <SAW : Link_Ref_List `pictures`>
      <SAW : Surrogate `pid` [mom_id_entity.pid]>
      <SAW : String `short_title` [swp_gallery.short_title]>
      <SAW : String `title` [swp_gallery.title]>
      <SAW : String `type_name` [mom_id_entity.type_name]>
      <SAW : Boolean `x_locked` [mom_id_entity.x_locked]>
    <SAW : MOM.D2_Value_Int []>
      <SAW : X `x` [x]>
      <SAW : Y `y` [y]>
    <SAW : MOM.D2_Value_Float []>
      <SAW : X `x` [x]>
      <SAW : Y `y` [y]>
    <SAW : MOM._Pic_ []>
      <SAW : String `extension` [extension]>
      <SAW : Y `height` [height]>
      <SAW : X `width` [width]>
    <SAW : MOM._Thumb_ []>
      <SAW : String `extension` [extension]>
      <SAW : Y `height` [height]>
      <SAW : X `width` [width]>
    <SAW : SWP.Picture [swp_picture : mom_id_entity]>
      <SAW : Rev_Ref `creation`>
      <SAW : Boolean `electric` [mom_id_entity.electric]>
      <SAW : Rev_Ref `last_change`>
      <SAW : Int `last_cid` [mom_id_entity.last_cid]>
      <SAW : Gallery `left` [swp_picture.left]>
      <SAW : String `name` [swp_picture.name]>
      <SAW : Int `number` [swp_picture.number]>
      <SAW : Picture `photo` [swp_picture.photo__extension, swp_picture.photo__height, swp_picture.photo__width]>
      <SAW : Surrogate `pid` [mom_id_entity.pid]>
      <SAW : Thumbnail `thumb` [swp_picture.thumb__extension, swp_picture.thumb__height, swp_picture.thumb__width]>
      <SAW : String `type_name` [mom_id_entity.type_name]>
      <SAW : Boolean `x_locked` [mom_id_entity.x_locked]>
    <SAW : SRM.Page [srm_page : swp_page : mom_id_entity]>
      <SAW : Link_Ref_List `clips`>
      <SAW : Text `contents` [swp_page.contents]>
      <SAW : Rev_Ref `creation`>
      <SAW : Date_Interval `date` [swp_page.date__finish, swp_page.date__start]>
      <SAW : Boolean `date.alive`>
      <SAW : String `desc` [srm_page.desc]>
      <SAW : Boolean `electric` [mom_id_entity.electric]>
      <SAW : Entity `event` [srm_page.event]>
      <SAW : Link_Ref_List `events`>
      <SAW : Format `format` [swp_page.format]>
      <SAW : String `head_line` [swp_page.head_line]>
      <SAW : Boolean `hidden` [swp_page.hidden]>
      <SAW : Rev_Ref `last_change`>
      <SAW : Int `last_cid` [mom_id_entity.last_cid]>
      <SAW : Date-Slug `perma_name` [swp_page.perma_name]>
      <SAW : Surrogate `pid` [mom_id_entity.pid]>
      <SAW : Int `prio` [swp_page.prio]>
      <SAW : String `short_title` [swp_page.short_title]>
      <SAW : Text `text` [swp_page.text]>
      <SAW : String `title` [swp_page.title]>
      <SAW : String `type_name` [mom_id_entity.type_name]>
      <SAW : Boolean `x_locked` [mom_id_entity.x_locked]>
    <SAW : SRM.Regatta [srm_regatta : mom_id_entity]>
      <SAW : Entity `boat_class` [srm_regatta.boat_class]>
      <SAW : Link_Ref_List `boats`>
      <SAW : Rev_Ref `creation`>
      <SAW : Int `discards` [srm_regatta.discards]>
      <SAW : Boolean `electric` [mom_id_entity.electric]>
      <SAW : Boolean `is_cancelled` [srm_regatta.is_cancelled]>
      <SAW : String `kind` [srm_regatta.kind]>
      <SAW : Rev_Ref `last_change`>
      <SAW : Int `last_cid` [mom_id_entity.last_cid]>
      <SAW : Regatta_Event `left` [srm_regatta.left]>
      <SAW : String `perma_name` [srm_regatta.perma_name]>
      <SAW : Surrogate `pid` [mom_id_entity.pid]>
      <SAW : Int `races` [srm_regatta.races]>
      <SAW : Int `races_counted`>
      <SAW : Regatta_Result `result` [srm_regatta.result__date, srm_regatta.result__software, srm_regatta.result__status]>
      <SAW : String `type_name` [mom_id_entity.type_name]>
      <SAW : Boolean `x_locked` [mom_id_entity.x_locked]>
      <SAW : Int `year`>
    <SAW : SRM.Regatta_C [srm_regatta_c : srm_regatta : mom_id_entity]>
      <SAW : Entity `boat_class` [srm_regatta.boat_class]>
      <SAW : Link_Ref_List `boats`>
      <SAW : Rev_Ref `creation`>
      <SAW : Int `discards` [srm_regatta.discards]>
      <SAW : Boolean `electric` [mom_id_entity.electric]>
      <SAW : Boolean `is_cancelled` [srm_regatta.is_cancelled]>
      <SAW : Boolean `is_team_race` [srm_regatta_c.is_team_race]>
      <SAW : String `kind` [srm_regatta.kind]>
      <SAW : Rev_Ref `last_change`>
      <SAW : Int `last_cid` [mom_id_entity.last_cid]>
      <SAW : Regatta_Event `left` [srm_regatta.left]>
      <SAW : String `perma_name` [srm_regatta.perma_name]>
      <SAW : Surrogate `pid` [mom_id_entity.pid]>
      <SAW : Int `races` [srm_regatta.races]>
      <SAW : Int `races_counted`>
      <SAW : Regatta_Result `result` [srm_regatta.result__date, srm_regatta.result__software, srm_regatta.result__status]>
      <SAW : Link_Ref_List `teams`>
      <SAW : String `type_name` [mom_id_entity.type_name]>
      <SAW : Boolean `x_locked` [mom_id_entity.x_locked]>
      <SAW : Int `year`>
    <SAW : SRM.Regatta_H [srm_regatta_h : srm_regatta : mom_id_entity]>
      <SAW : Entity `boat_class` [srm_regatta.boat_class]>
      <SAW : Link_Ref_List `boats`>
      <SAW : Rev_Ref `creation`>
      <SAW : Int `discards` [srm_regatta.discards]>
      <SAW : Boolean `electric` [mom_id_entity.electric]>
      <SAW : Blob `handicap`>
      <SAW : Boolean `is_cancelled` [srm_regatta.is_cancelled]>
      <SAW : String `kind` [srm_regatta.kind]>
      <SAW : Rev_Ref `last_change`>
      <SAW : Int `last_cid` [mom_id_entity.last_cid]>
      <SAW : Regatta_Event `left` [srm_regatta.left]>
      <SAW : String `perma_name` [srm_regatta.perma_name]>
      <SAW : Surrogate `pid` [mom_id_entity.pid]>
      <SAW : Int `races` [srm_regatta.races]>
      <SAW : Int `races_counted`>
      <SAW : Regatta_Result `result` [srm_regatta.result__date, srm_regatta.result__software, srm_regatta.result__status]>
      <SAW : String `type_name` [mom_id_entity.type_name]>
      <SAW : Boolean `x_locked` [mom_id_entity.x_locked]>
      <SAW : Int `year`>
    <SAW : SRM.Sailor [srm_sailor : mom_id_entity]>
      <SAW : Link_Ref_List `boat_in_regatta_links`>
      <SAW : Entity `club` [srm_sailor.club]>
      <SAW : Rev_Ref `creation`>
      <SAW : Boolean `electric` [mom_id_entity.electric]>
      <SAW : Rev_Ref `last_change`>
      <SAW : Int `last_cid` [mom_id_entity.last_cid]>
      <SAW : Person `left` [srm_sailor.left]>
      <SAW : Int `mna_number` [srm_sailor.mna_number, srm_sailor.__raw_mna_number]>
      <SAW : Nation `nation` [srm_sailor.nation]>
      <SAW : Surrogate `pid` [mom_id_entity.pid]>
      <SAW : String `type_name` [mom_id_entity.type_name]>
      <SAW : Boolean `x_locked` [mom_id_entity.x_locked]>
    <SAW : SRM._MOM_Link_n_ [mom_id_entity]>
      <SAW : Rev_Ref `creation`>
      <SAW : Boolean `electric` [mom_id_entity.electric]>
      <SAW : Rev_Ref `last_change`>
      <SAW : Int `last_cid` [mom_id_entity.last_cid]>
      <SAW : Left `left` (SRM.Boat_in_Regatta | SRM.Crew_Member | SRM.Team_has_Boat_in_Regatta)>
      <SAW : Surrogate `pid` [mom_id_entity.pid]>
      <SAW : Right `right` (SRM.Boat_in_Regatta | SRM.Crew_Member | SRM.Team_has_Boat_in_Regatta)>
      <SAW : String `type_name` [mom_id_entity.type_name]>
      <SAW : Boolean `x_locked` [mom_id_entity.x_locked]>
    <SAW : SRM.Link2 [mom_id_entity]>
      <SAW : Rev_Ref `creation`>
      <SAW : Boolean `electric` [mom_id_entity.electric]>
      <SAW : Rev_Ref `last_change`>
      <SAW : Int `last_cid` [mom_id_entity.last_cid]>
      <SAW : Left `left` (SRM.Boat_in_Regatta | SRM.Crew_Member | SRM.Team_has_Boat_in_Regatta)>
      <SAW : Surrogate `pid` [mom_id_entity.pid]>
      <SAW : Right `right` (SRM.Boat_in_Regatta | SRM.Crew_Member | SRM.Team_has_Boat_in_Regatta)>
      <SAW : String `type_name` [mom_id_entity.type_name]>
      <SAW : Boolean `x_locked` [mom_id_entity.x_locked]>
    <SAW : SRM.Boat_in_Regatta [srm_boat_in_regatta : mom_id_entity]>
      <SAW : Role_Ref_Set `_crew`>
      <SAW : Rev_Ref `creation`>
      <SAW : Boolean `electric` [mom_id_entity.electric]>
      <SAW : Rev_Ref `last_change`>
      <SAW : Int `last_cid` [mom_id_entity.last_cid]>
      <SAW : Boat `left` [srm_boat_in_regatta.left]>
      <SAW : Surrogate `pid` [mom_id_entity.pid]>
      <SAW : Int `place` [srm_boat_in_regatta.place]>
      <SAW : Int `points` [srm_boat_in_regatta.points]>
      <SAW : Link_Ref_List `race_results`>
      <SAW : Int `rank` [srm_boat_in_regatta.rank]>
      <SAW : Date `registration_date` [srm_boat_in_regatta.registration_date]>
      <SAW : Regatta `right` [srm_boat_in_regatta.right]>
      <SAW : Link_Ref_List `sailor_links`>
      <SAW : Entity `skipper` [srm_boat_in_regatta.skipper]>
      <SAW : Link_Ref_List `team_links`>
      <SAW : Role_Ref_Set `teams`>
      <SAW : String `type_name` [mom_id_entity.type_name]>
      <SAW : Boolean `x_locked` [mom_id_entity.x_locked]>
    <SAW : SRM.Race_Result [srm_race_result : mom_id_entity]>
      <SAW : Rev_Ref `creation`>
      <SAW : Boolean `discarded` [srm_race_result.discarded]>
      <SAW : Boolean `electric` [mom_id_entity.electric]>
      <SAW : Rev_Ref `last_change`>
      <SAW : Int `last_cid` [mom_id_entity.last_cid]>
      <SAW : Boat_in_Regatta `left` [srm_race_result.left]>
      <SAW : Surrogate `pid` [mom_id_entity.pid]>
      <SAW : Int `points` [srm_race_result.points]>
      <SAW : Int `race` [srm_race_result.race]>
      <SAW : String `status` [srm_race_result.status]>
      <SAW : String `type_name` [mom_id_entity.type_name]>
      <SAW : Boolean `x_locked` [mom_id_entity.x_locked]>
    <SAW : SRM.Team [srm_team : mom_id_entity]>
      <SAW : Link_Ref_List `boat_links`>
      <SAW : Role_Ref_Set `boats`>
      <SAW : Entity `club` [srm_team.club]>
      <SAW : Rev_Ref `creation`>
      <SAW : String `desc` [srm_team.desc]>
      <SAW : Boolean `electric` [mom_id_entity.electric]>
      <SAW : Rev_Ref `last_change`>
      <SAW : Int `last_cid` [mom_id_entity.last_cid]>
      <SAW : Entity `leader` [srm_team.leader]>
      <SAW : Regatta_C `left` [srm_team.left]>
      <SAW : String `name` [srm_team.name, srm_team.__raw_name]>
      <SAW : Surrogate `pid` [mom_id_entity.pid]>
      <SAW : Int `place` [srm_team.place]>
      <SAW : Date `registration_date` [srm_team.registration_date]>
      <SAW : String `type_name` [mom_id_entity.type_name]>
      <SAW : Boolean `x_locked` [mom_id_entity.x_locked]>
    <SAW : SRM.Crew_Member [srm_crew_member : mom_id_entity]>
      <SAW : Rev_Ref `creation`>
      <SAW : Boolean `electric` [mom_id_entity.electric]>
      <SAW : Int `key` [srm_crew_member.key]>
      <SAW : Rev_Ref `last_change`>
      <SAW : Int `last_cid` [mom_id_entity.last_cid]>
      <SAW : Boat_in_Regatta `left` [srm_crew_member.left]>
      <SAW : Surrogate `pid` [mom_id_entity.pid]>
      <SAW : Sailor `right` [srm_crew_member.right]>
      <SAW : String `role` [srm_crew_member.role]>
      <SAW : String `type_name` [mom_id_entity.type_name]>
      <SAW : Boolean `x_locked` [mom_id_entity.x_locked]>
    <SAW : SRM.Team_has_Boat_in_Regatta [srm_team_has_boat_in_regatta : mom_id_entity]>
      <SAW : Rev_Ref `creation`>
      <SAW : Boolean `electric` [mom_id_entity.electric]>
      <SAW : Rev_Ref `last_change`>
      <SAW : Int `last_cid` [mom_id_entity.last_cid]>
      <SAW : Team `left` [srm_team_has_boat_in_regatta.left]>
      <SAW : Surrogate `pid` [mom_id_entity.pid]>
      <SAW : Boat_in_Regatta `right` [srm_team_has_boat_in_regatta.right]>
      <SAW : String `type_name` [mom_id_entity.type_name]>
      <SAW : Boolean `x_locked` [mom_id_entity.x_locked]>
    <SAW : PAP.Subject_has_Address [pap_subject_has_property : mom_id_entity]>
      <SAW : Rev_Ref `creation`>
      <SAW : String `desc` [pap_subject_has_property.desc]>
      <SAW : Boolean `electric` [mom_id_entity.electric]>
      <SAW : Rev_Ref `last_change`>
      <SAW : Int `last_cid` [mom_id_entity.last_cid]>
      <SAW : Subject `left` [pap_subject_has_property.left]>
      <SAW : Surrogate `pid` [mom_id_entity.pid]>
      <SAW : Address `right` [pap_subject_has_property.right]>
      <SAW : String `type_name` [mom_id_entity.type_name]>
      <SAW : Boolean `x_locked` [mom_id_entity.x_locked]>
    <SAW : PAP.Subject_has_Email [pap_subject_has_property : mom_id_entity]>
      <SAW : Rev_Ref `creation`>
      <SAW : String `desc` [pap_subject_has_property.desc]>
      <SAW : Boolean `electric` [mom_id_entity.electric]>
      <SAW : Rev_Ref `last_change`>
      <SAW : Int `last_cid` [mom_id_entity.last_cid]>
      <SAW : Subject `left` [pap_subject_has_property.left]>
      <SAW : Surrogate `pid` [mom_id_entity.pid]>
      <SAW : Email `right` [pap_subject_has_property.right]>
      <SAW : String `type_name` [mom_id_entity.type_name]>
      <SAW : Boolean `x_locked` [mom_id_entity.x_locked]>
    <SAW : PAP.Subject_has_Phone [pap_subject_has_phone : pap_subject_has_property : mom_id_entity]>
      <SAW : Rev_Ref `creation`>
      <SAW : String `desc` [pap_subject_has_property.desc]>
      <SAW : Boolean `electric` [mom_id_entity.electric]>
      <SAW : Numeric_String `extension` [pap_subject_has_phone.extension]>
      <SAW : Rev_Ref `last_change`>
      <SAW : Int `last_cid` [mom_id_entity.last_cid]>
      <SAW : Subject `left` [pap_subject_has_property.left]>
      <SAW : Surrogate `pid` [mom_id_entity.pid]>
      <SAW : Phone `right` [pap_subject_has_property.right]>
      <SAW : String `type_name` [mom_id_entity.type_name]>
      <SAW : Boolean `x_locked` [mom_id_entity.x_locked]>
    <SAW : PAP.Subject_has_Url [pap_subject_has_property : mom_id_entity]>
      <SAW : Rev_Ref `creation`>
      <SAW : String `desc` [pap_subject_has_property.desc]>
      <SAW : Boolean `electric` [mom_id_entity.electric]>
      <SAW : Rev_Ref `last_change`>
      <SAW : Int `last_cid` [mom_id_entity.last_cid]>
      <SAW : Subject `left` [pap_subject_has_property.left]>
      <SAW : Surrogate `pid` [mom_id_entity.pid]>
      <SAW : Url `right` [pap_subject_has_property.right]>
      <SAW : String `type_name` [mom_id_entity.type_name]>
      <SAW : Boolean `x_locked` [mom_id_entity.x_locked]>
    <SAW : PAP.Company_has_Url [pap_company_has_url : pap_subject_has_property : mom_id_entity]>
      <SAW : Rev_Ref `creation`>
      <SAW : String `desc` [pap_subject_has_property.desc]>
      <SAW : Boolean `electric` [mom_id_entity.electric]>
      <SAW : Rev_Ref `last_change`>
      <SAW : Int `last_cid` [mom_id_entity.last_cid]>
      <SAW : Company `left` [pap_subject_has_property.left]>
      <SAW : Surrogate `pid` [mom_id_entity.pid]>
      <SAW : Url `right` [pap_subject_has_property.right]>
      <SAW : String `type_name` [mom_id_entity.type_name]>
      <SAW : Boolean `x_locked` [mom_id_entity.x_locked]>
    <SAW : PAP.Person_has_Url [pap_person_has_url : pap_subject_has_property : mom_id_entity]>
      <SAW : Rev_Ref `creation`>
      <SAW : String `desc` [pap_subject_has_property.desc]>
      <SAW : Boolean `electric` [mom_id_entity.electric]>
      <SAW : Rev_Ref `last_change`>
      <SAW : Int `last_cid` [mom_id_entity.last_cid]>
      <SAW : Person `left` [pap_subject_has_property.left]>
      <SAW : Surrogate `pid` [mom_id_entity.pid]>
      <SAW : Url `right` [pap_subject_has_property.right]>
      <SAW : String `type_name` [mom_id_entity.type_name]>
      <SAW : Boolean `x_locked` [mom_id_entity.x_locked]>
    <SAW : PAP.Company_has_Phone [pap_company_has_phone : pap_subject_has_phone : pap_subject_has_property : mom_id_entity]>
      <SAW : Rev_Ref `creation`>
      <SAW : String `desc` [pap_subject_has_property.desc]>
      <SAW : Boolean `electric` [mom_id_entity.electric]>
      <SAW : Numeric_String `extension` [pap_subject_has_phone.extension]>
      <SAW : Rev_Ref `last_change`>
      <SAW : Int `last_cid` [mom_id_entity.last_cid]>
      <SAW : Company `left` [pap_subject_has_property.left]>
      <SAW : Surrogate `pid` [mom_id_entity.pid]>
      <SAW : Phone `right` [pap_subject_has_property.right]>
      <SAW : String `type_name` [mom_id_entity.type_name]>
      <SAW : Boolean `x_locked` [mom_id_entity.x_locked]>
    <SAW : PAP.Person_has_Phone [pap_person_has_phone : pap_subject_has_phone : pap_subject_has_property : mom_id_entity]>
      <SAW : Rev_Ref `creation`>
      <SAW : String `desc` [pap_subject_has_property.desc]>
      <SAW : Boolean `electric` [mom_id_entity.electric]>
      <SAW : Numeric_String `extension` [pap_subject_has_phone.extension]>
      <SAW : Rev_Ref `last_change`>
      <SAW : Int `last_cid` [mom_id_entity.last_cid]>
      <SAW : Person `left` [pap_subject_has_property.left]>
      <SAW : Surrogate `pid` [mom_id_entity.pid]>
      <SAW : Phone `right` [pap_subject_has_property.right]>
      <SAW : String `type_name` [mom_id_entity.type_name]>
      <SAW : Boolean `x_locked` [mom_id_entity.x_locked]>
    <SAW : PAP.Company_has_Email [pap_company_has_email : pap_subject_has_property : mom_id_entity]>
      <SAW : Rev_Ref `creation`>
      <SAW : String `desc` [pap_subject_has_property.desc]>
      <SAW : Boolean `electric` [mom_id_entity.electric]>
      <SAW : Rev_Ref `last_change`>
      <SAW : Int `last_cid` [mom_id_entity.last_cid]>
      <SAW : Company `left` [pap_subject_has_property.left]>
      <SAW : Surrogate `pid` [mom_id_entity.pid]>
      <SAW : Email `right` [pap_subject_has_property.right]>
      <SAW : String `type_name` [mom_id_entity.type_name]>
      <SAW : Boolean `x_locked` [mom_id_entity.x_locked]>
    <SAW : PAP.Person_has_Email [pap_person_has_email : pap_subject_has_property : mom_id_entity]>
      <SAW : Rev_Ref `creation`>
      <SAW : String `desc` [pap_subject_has_property.desc]>
      <SAW : Boolean `electric` [mom_id_entity.electric]>
      <SAW : Rev_Ref `last_change`>
      <SAW : Int `last_cid` [mom_id_entity.last_cid]>
      <SAW : Person `left` [pap_subject_has_property.left]>
      <SAW : Surrogate `pid` [mom_id_entity.pid]>
      <SAW : Email `right` [pap_subject_has_property.right]>
      <SAW : String `type_name` [mom_id_entity.type_name]>
      <SAW : Boolean `x_locked` [mom_id_entity.x_locked]>
    <SAW : PAP.Company_has_Address [pap_company_has_address : pap_subject_has_property : mom_id_entity]>
      <SAW : Rev_Ref `creation`>
      <SAW : String `desc` [pap_subject_has_property.desc]>
      <SAW : Boolean `electric` [mom_id_entity.electric]>
      <SAW : Rev_Ref `last_change`>
      <SAW : Int `last_cid` [mom_id_entity.last_cid]>
      <SAW : Company `left` [pap_subject_has_property.left]>
      <SAW : Surrogate `pid` [mom_id_entity.pid]>
      <SAW : Address `right` [pap_subject_has_property.right]>
      <SAW : String `type_name` [mom_id_entity.type_name]>
      <SAW : Boolean `x_locked` [mom_id_entity.x_locked]>
    <SAW : PAP.Person_has_Address [pap_person_has_address : pap_subject_has_property : mom_id_entity]>
      <SAW : Rev_Ref `creation`>
      <SAW : String `desc` [pap_subject_has_property.desc]>
      <SAW : Boolean `electric` [mom_id_entity.electric]>
      <SAW : Rev_Ref `last_change`>
      <SAW : Int `last_cid` [mom_id_entity.last_cid]>
      <SAW : Person `left` [pap_subject_has_property.left]>
      <SAW : Surrogate `pid` [mom_id_entity.pid]>
      <SAW : Address `right` [pap_subject_has_property.right]>
      <SAW : String `type_name` [mom_id_entity.type_name]>
      <SAW : Boolean `x_locked` [mom_id_entity.x_locked]>

    >>> show_q_able_names (apt)
    <SAW : MOM.Id_Entity [mom_id_entity]>
      creation                      : creation
      electric                      : electric
      last_change                   : last_change
      last_cid                      : last_cid
      pid                           : pid
      type_name                     : type_name
      x_locked                      : x_locked
    <SAW : MOM.MD_Change [mom_md_change]>
      c_time                        : c_time
      c_user                        : c_user
      cid                           : cid
      kind                          : kind
      parent                        : parent
      parent_cid                    : parent_cid
      pid                           : pid
      scm_change                    : scm_change
      time                          : time
      type_name                     : type_name
      user                          : user
    <SAW : MOM.Link [mom_id_entity]>
      creation                      : creation
      electric                      : electric
      last_change                   : last_change
      last_cid                      : last_cid
      left                          : left
      pid                           : pid
      type_name                     : type_name
      x_locked                      : x_locked
    <SAW : MOM.Link1 [mom_id_entity]>
      creation                      : creation
      electric                      : electric
      last_change                   : last_change
      last_cid                      : last_cid
      left                          : left
      pid                           : pid
      type_name                     : type_name
      x_locked                      : x_locked
    <SAW : MOM._MOM_Link_n_ [mom_id_entity]>
      creation                      : creation
      electric                      : electric
      last_change                   : last_change
      last_cid                      : last_cid
      left                          : left
      pid                           : pid
      right                         : right
      type_name                     : type_name
      x_locked                      : x_locked
    <SAW : MOM.Link2 [mom_id_entity]>
      creation                      : creation
      electric                      : electric
      last_change                   : last_change
      last_cid                      : last_cid
      left                          : left
      pid                           : pid
      right                         : right
      type_name                     : type_name
      x_locked                      : x_locked
    <SAW : MOM.Link3 [mom_id_entity]>
      creation                      : creation
      electric                      : electric
      last_change                   : last_change
      last_cid                      : last_cid
      left                          : left
      middle                        : middle
      pid                           : pid
      right                         : right
      type_name                     : type_name
      x_locked                      : x_locked
    <SAW : MOM.Object [mom_id_entity]>
      creation                      : creation
      electric                      : electric
      last_change                   : last_change
      last_cid                      : last_cid
      pid                           : pid
      type_name                     : type_name
      x_locked                      : x_locked
    <SAW : Auth.Id_Entity [mom_id_entity]>
      creation                      : creation
      electric                      : electric
      last_change                   : last_change
      last_cid                      : last_cid
      pid                           : pid
      type_name                     : type_name
      x_locked                      : x_locked
    <SAW : Auth.Object [mom_id_entity]>
      creation                      : creation
      electric                      : electric
      last_change                   : last_change
      last_cid                      : last_cid
      pid                           : pid
      type_name                     : type_name
      x_locked                      : x_locked
    <SAW : Auth._Account_ [auth__account_ : mom_id_entity]>
      active                        : active
      creation                      : creation
      electric                      : electric
      enabled                       : enabled
      last_change                   : last_change
      last_cid                      : last_cid
      name                          : name
      pid                           : pid
      superuser                     : superuser
      suspended                     : suspended
      type_name                     : type_name
      x_locked                      : x_locked
    <SAW : Auth.Account_Anonymous [auth_account_anonymous : auth__account_ : mom_id_entity]>
      active                        : active
      creation                      : creation
      electric                      : electric
      enabled                       : enabled
      last_change                   : last_change
      last_cid                      : last_cid
      name                          : name
      pid                           : pid
      superuser                     : superuser
      suspended                     : suspended
      type_name                     : type_name
      x_locked                      : x_locked
    <SAW : Auth.Account [auth_account : auth__account_ : mom_id_entity]>
      _account_action_s             : _account_action_s
      _account_token_action_s       : _account_token_action_s
      account_email_verifications   : account_email_verifications
      account_password_resets       : account_password_resets
      activation                    : activation
      activations                   : activations
      active                        : active
      creation                      : creation
      electric                      : electric
      enabled                       : enabled
      group_links                   : group_links
      groups                        : groups
      last_change                   : last_change
      last_cid                      : last_cid
      name                          : name
      password                      : password
      password_change_required      : password_change_required
      password_change_requireds     : password_change_requireds
      person                        : person
      person_link                   : person_link
      person_links                  : person_links
      ph_name                       : ph_name
      pid                           : pid
      superuser                     : superuser
      suspended                     : suspended
      type_name                     : type_name
      x_locked                      : x_locked
    <SAW : MOM.Date_Time_Interval []>
      alive                         : alive
      finish                        : finish
      start                         : start
    <SAW : MOM.Date_Time_Interval_C []>
      alive                         : alive
      finish                        : finish
      start                         : start
    <SAW : MOM.Date_Time_Interval_N []>
      alive                         : alive
      finish                        : finish
      start                         : start
    <SAW : Auth.Certificate [auth_certificate : mom_id_entity]>
      alive                         : alive
      cert_id                       : cert_id
      creation                      : creation
      desc                          : desc
      electric                      : electric
      email                         : email
      last_change                   : last_change
      last_cid                      : last_cid
      pem                           : pem
      pid                           : pid
      revocation_date               : revocation_date
      type_name                     : type_name
      validity                      : validity
          alive                         : validity.alive
          finish                        : validity.finish
          start                         : validity.start
      x_locked                      : x_locked
    <SAW : Auth.Group [auth_group : mom_id_entity]>
      account_links                 : account_links
      accounts                      : accounts
      creation                      : creation
      desc                          : desc
      electric                      : electric
      last_change                   : last_change
      last_cid                      : last_cid
      name                          : name
      pid                           : pid
      type_name                     : type_name
      x_locked                      : x_locked
    <SAW : Auth.Link [mom_id_entity]>
      creation                      : creation
      electric                      : electric
      last_change                   : last_change
      last_cid                      : last_cid
      left                          : left
      pid                           : pid
      type_name                     : type_name
      x_locked                      : x_locked
    <SAW : Auth._MOM_Link_n_ [mom_id_entity]>
      creation                      : creation
      electric                      : electric
      last_change                   : last_change
      last_cid                      : last_cid
      left                          : left
      pid                           : pid
      right                         : right
      type_name                     : type_name
      x_locked                      : x_locked
    <SAW : Auth.Link2 [mom_id_entity]>
      creation                      : creation
      electric                      : electric
      last_change                   : last_change
      last_cid                      : last_cid
      left                          : left
      pid                           : pid
      right                         : right
      type_name                     : type_name
      x_locked                      : x_locked
    <SAW : Auth.Account_in_Group [auth_account_in_group : mom_id_entity]>
      creation                      : creation
      electric                      : electric
      last_change                   : last_change
      last_cid                      : last_cid
      left                          : account, left
      pid                           : pid
      right                         : group, right
      type_name                     : type_name
      x_locked                      : x_locked
    <SAW : Auth.Link1 [mom_id_entity]>
      creation                      : creation
      electric                      : electric
      last_change                   : last_change
      last_cid                      : last_cid
      left                          : left
      pid                           : pid
      type_name                     : type_name
      x_locked                      : x_locked
    <SAW : Auth._Account_Action_ [mom_id_entity]>
      creation                      : creation
      electric                      : electric
      last_change                   : last_change
      last_cid                      : last_cid
      left                          : account, left
      pid                           : pid
      type_name                     : type_name
      x_locked                      : x_locked
    <SAW : Auth.Account_Activation [auth_account_activation : mom_id_entity]>
      creation                      : creation
      electric                      : electric
      last_change                   : last_change
      last_cid                      : last_cid
      left                          : account, left
      pid                           : pid
      type_name                     : type_name
      x_locked                      : x_locked
    <SAW : Auth.Account_Password_Change_Required [auth_account_password_change_required : mom_id_entity]>
      creation                      : creation
      electric                      : electric
      last_change                   : last_change
      last_cid                      : last_cid
      left                          : account, left
      pid                           : pid
      type_name                     : type_name
      x_locked                      : x_locked
    <SAW : Auth._Account_Token_Action_ [mom_id_entity]>
      creation                      : creation
      electric                      : electric
      expires                       : expires
      last_change                   : last_change
      last_cid                      : last_cid
      left                          : account, left
      pid                           : pid
      token                         : token
      type_name                     : type_name
      x_locked                      : x_locked
    <SAW : Auth.Account_EMail_Verification [auth_account_email_verification : mom_id_entity]>
      creation                      : creation
      electric                      : electric
      expires                       : expires
      last_change                   : last_change
      last_cid                      : last_cid
      left                          : account, left
      new_email                     : new_email
      pid                           : pid
      token                         : token
      type_name                     : type_name
      x_locked                      : x_locked
    <SAW : Auth.Account_Password_Reset [auth_account_password_reset : mom_id_entity]>
      creation                      : creation
      electric                      : electric
      expires                       : expires
      last_change                   : last_change
      last_cid                      : last_cid
      left                          : account, left
      password                      : password
      pid                           : pid
      token                         : token
      type_name                     : type_name
      x_locked                      : x_locked
    <SAW : EVT.Id_Entity [mom_id_entity]>
      creation                      : creation
      electric                      : electric
      last_change                   : last_change
      last_cid                      : last_cid
      pid                           : pid
      type_name                     : type_name
      x_locked                      : x_locked
    <SAW : EVT.Object [mom_id_entity]>
      creation                      : creation
      electric                      : electric
      last_change                   : last_change
      last_cid                      : last_cid
      pid                           : pid
      type_name                     : type_name
      x_locked                      : x_locked
    <SAW : EVT.Calendar [evt_calendar : mom_id_entity]>
      creation                      : creation
      desc                          : desc
      electric                      : electric
      last_change                   : last_change
      last_cid                      : last_cid
      name                          : name
      pid                           : pid
      type_name                     : type_name
      x_locked                      : x_locked
    <SAW : MOM.Date_Interval []>
      alive                         : alive
      finish                        : finish
      start                         : start
    <SAW : MOM.Date_Interval_C []>
      alive                         : alive
      finish                        : finish
      start                         : start
    <SAW : MOM.Date_Interval_N []>
      alive                         : alive
      finish                        : finish
      start                         : start
    <SAW : MOM.Time_Interval []>
      finish                        : finish
      start                         : start
    <SAW : EVT.Link [mom_id_entity]>
      creation                      : creation
      electric                      : electric
      last_change                   : last_change
      last_cid                      : last_cid
      left                          : left
      pid                           : pid
      type_name                     : type_name
      x_locked                      : x_locked
    <SAW : EVT.Link1 [mom_id_entity]>
      creation                      : creation
      electric                      : electric
      last_change                   : last_change
      last_cid                      : last_cid
      left                          : left
      pid                           : pid
      type_name                     : type_name
      x_locked                      : x_locked
    <SAW : SWP.Id_Entity [mom_id_entity]>
      creation                      : creation
      electric                      : electric
      last_change                   : last_change
      last_cid                      : last_cid
      pid                           : pid
      type_name                     : type_name
      x_locked                      : x_locked
    <SAW : SWP.Object [mom_id_entity]>
      creation                      : creation
      electric                      : electric
      last_change                   : last_change
      last_cid                      : last_cid
      pid                           : pid
      type_name                     : type_name
      x_locked                      : x_locked
    <SAW : SWP.Object_PN [mom_id_entity]>
      clips                         : clips
      creation                      : creation
      date                          : date
      electric                      : electric
      last_change                   : last_change
      last_cid                      : last_cid
      perma_name                    : perma_name
      pid                           : pid
      short_title                   : short_title
      title                         : title
      type_name                     : type_name
      x_locked                      : x_locked
    <SAW : SWP.Page_Mixin []>
      contents                      : contents
      format                        : format
      head_line                     : head_line
      hidden                        : hidden
      prio                          : prio
      text                          : text
    <SAW : SWP.Page [swp_page : mom_id_entity]>
      clips                         : clips
      contents                      : contents
      creation                      : creation
      date                          : date
          alive                         : date.alive
          finish                        : date.finish
          start                         : date.start
      electric                      : electric
      events                        : events
      format                        : format
      head_line                     : head_line
      hidden                        : hidden
      last_change                   : last_change
      last_cid                      : last_cid
      perma_name                    : perma_name
      pid                           : pid
      prio                          : prio
      short_title                   : short_title
      text                          : text
      title                         : title
      type_name                     : type_name
      x_locked                      : x_locked
    <SAW : SWP.Page_Y [swp_page_y : swp_page : mom_id_entity]>
      clips                         : clips
      contents                      : contents
      creation                      : creation
      date                          : date
          alive                         : date.alive
          finish                        : date.finish
          start                         : date.start
      electric                      : electric
      events                        : events
      format                        : format
      head_line                     : head_line
      hidden                        : hidden
      last_change                   : last_change
      last_cid                      : last_cid
      perma_name                    : perma_name
      pid                           : pid
      prio                          : prio
      short_title                   : short_title
      text                          : text
      title                         : title
      type_name                     : type_name
      x_locked                      : x_locked
      year                          : year
    <SAW : EVT.Event [evt_event : mom_id_entity]>
      calendar                      : calendar
      creation                      : creation
      date                          : date
          alive                         : date.alive
          finish                        : date.finish
          start                         : date.start
      detail                        : detail
      electric                      : electric
      last_change                   : last_change
      last_cid                      : last_cid
      left                          : left, object
      occurs                        : occurs
      pid                           : pid
      recurrence                    : recurrence
      short_title                   : short_title
      time                          : time
          finish                        : time.finish
          start                         : time.start
      type_name                     : type_name
      x_locked                      : x_locked
    <SAW : EVT.Event_occurs [evt_event_occurs : mom_id_entity]>
      creation                      : creation
      date                          : date
      electric                      : electric
      last_change                   : last_change
      last_cid                      : last_cid
      left                          : event, left
      pid                           : pid
      time                          : time
          finish                        : time.finish
          start                         : time.start
      type_name                     : type_name
      x_locked                      : x_locked
    <SAW : EVT._Recurrence_Mixin_ [mom_id_entity]>
      creation                      : creation
      electric                      : electric
      last_change                   : last_change
      last_cid                      : last_cid
      left                          : left
      pid                           : pid
      type_name                     : type_name
      x_locked                      : x_locked
    <SAW : EVT.Recurrence_Spec [evt_recurrence_spec : mom_id_entity]>
      creation                      : creation
      date_exceptions               : date_exceptions
      dates                         : dates
      electric                      : electric
      last_change                   : last_change
      last_cid                      : last_cid
      left                          : event, left
      pid                           : pid
      rules                         : rules
      type_name                     : type_name
      x_locked                      : x_locked
    <SAW : EVT.Recurrence_Rule [evt_recurrence_rule : mom_id_entity]>
      count                         : count
      creation                      : creation
      desc                          : desc
      easter_offset                 : easter_offset
      electric                      : electric
      finish                        : finish
      is_exception                  : is_exception
      last_change                   : last_change
      last_cid                      : last_cid
      left                          : left, recurrence_spec
      month                         : month
      month_day                     : month_day
      period                        : period
      pid                           : pid
      restrict_pos                  : restrict_pos
      start                         : start
      type_name                     : type_name
      unit                          : unit
      week                          : week
      week_day                      : week_day
      x_locked                      : x_locked
      year_day                      : year_day
    <SAW : MOM.Position []>
      height                        : height
      lat                           : lat
      lon                           : lon
    <SAW : PAP.Id_Entity [mom_id_entity]>
      creation                      : creation
      electric                      : electric
      last_change                   : last_change
      last_cid                      : last_cid
      pid                           : pid
      type_name                     : type_name
      x_locked                      : x_locked
    <SAW : PAP.Object [mom_id_entity]>
      creation                      : creation
      electric                      : electric
      last_change                   : last_change
      last_cid                      : last_cid
      pid                           : pid
      type_name                     : type_name
      x_locked                      : x_locked
    <SAW : PAP.Property [mom_id_entity]>
      creation                      : creation
      desc                          : desc
      electric                      : electric
      last_change                   : last_change
      last_cid                      : last_cid
      pid                           : pid
      subject_links                 : subject_links
      type_name                     : type_name
      x_locked                      : x_locked
    <SAW : PAP.Address [pap_address : mom_id_entity]>
      city                          : city
      companies                     : companies
      company_links                 : company_links
      country                       : country
      creation                      : creation
      desc                          : desc
      electric                      : electric
      gps                           : gps
      last_change                   : last_change
      last_cid                      : last_cid
      person_links                  : person_links
      persons                       : persons
      pid                           : pid
      region                        : region
      street                        : street
      subject_links                 : subject_links
      type_name                     : type_name
      x_locked                      : x_locked
      zip                           : zip
    <SAW : PAP.Subject [mom_id_entity]>
      address_links                 : address_links
      addresses                     : addresses
      creation                      : creation
      electric                      : electric
      email_links                   : email_links
      emails                        : emails
      last_change                   : last_change
      last_cid                      : last_cid
      lifetime                      : lifetime
      phone_links                   : phone_links
      phones                        : phones
      pid                           : pid
      property_links                : property_links
      type_name                     : type_name
      url_links                     : url_links
      urls                          : urls
      x_locked                      : x_locked
    <SAW : PAP.Legal_Entity [mom_id_entity]>
      address_links                 : address_links
      addresses                     : addresses
      creation                      : creation
      electric                      : electric
      email_links                   : email_links
      emails                        : emails
      last_change                   : last_change
      last_cid                      : last_cid
      lifetime                      : lifetime
      name                          : name
      phone_links                   : phone_links
      phones                        : phones
      pid                           : pid
      property_links                : property_links
      short_name                    : short_name
      type_name                     : type_name
      url_links                     : url_links
      urls                          : urls
      x_locked                      : x_locked
    <SAW : PAP.Company [pap_company : mom_id_entity]>
      address_links                 : address_links
      addresses                     : addresses
      creation                      : creation
      electric                      : electric
      email_links                   : email_links
      emails                        : emails
      last_change                   : last_change
      last_cid                      : last_cid
      lifetime                      : lifetime
          alive                         : lifetime.alive
          finish                        : lifetime.finish
          start                         : lifetime.start
      name                          : name
      phone_links                   : phone_links
      phones                        : phones
      pid                           : pid
      property_links                : property_links
      registered_in                 : registered_in
      short_name                    : short_name
      type_name                     : type_name
      url_links                     : url_links
      urls                          : urls
      x_locked                      : x_locked
    <SAW : PAP.Email [pap_email : mom_id_entity]>
      address                       : address
      companies                     : companies
      company_links                 : company_links
      creation                      : creation
      desc                          : desc
      electric                      : electric
      last_change                   : last_change
      last_cid                      : last_cid
      person_links                  : person_links
      persons                       : persons
      pid                           : pid
      subject_links                 : subject_links
      type_name                     : type_name
      x_locked                      : x_locked
    <SAW : PAP.Phone [pap_phone : mom_id_entity]>
      area_code                     : area_code
      companies                     : companies
      company_links                 : company_links
      country_code                  : country_code
      creation                      : creation
      desc                          : desc
      electric                      : electric
      last_change                   : last_change
      last_cid                      : last_cid
      number                        : number
      person_links                  : person_links
      persons                       : persons
      pid                           : pid
      subject_links                 : subject_links
      type_name                     : type_name
      x_locked                      : x_locked
    <SAW : PAP.Person [pap_person : mom_id_entity]>
      account_links                 : account_links
      accounts                      : accounts
      address_links                 : address_links
      addresses                     : addresses
      creation                      : creation
      electric                      : electric
      email_links                   : email_links
      emails                        : emails
      first_name                    : first_name
      last_change                   : last_change
      last_cid                      : last_cid
      last_name                     : last_name
      lifetime                      : lifetime
          alive                         : lifetime.alive
          finish                        : lifetime.finish
          start                         : lifetime.start
      middle_name                   : middle_name
      phone_links                   : phone_links
      phones                        : phones
      pid                           : pid
      property_links                : property_links
      sailors                       : sailors
      sex                           : sex
      title                         : title
      type_name                     : type_name
      url_links                     : url_links
      urls                          : urls
      x_locked                      : x_locked
    <SAW : PAP.Url [pap_url : mom_id_entity]>
      companies                     : companies
      company_links                 : company_links
      creation                      : creation
      desc                          : desc
      electric                      : electric
      last_change                   : last_change
      last_cid                      : last_cid
      person_links                  : person_links
      persons                       : persons
      pid                           : pid
      subject_links                 : subject_links
      type_name                     : type_name
      value                         : value
      x_locked                      : x_locked
    <SAW : PAP.Link [mom_id_entity]>
      creation                      : creation
      electric                      : electric
      last_change                   : last_change
      last_cid                      : last_cid
      left                          : left
      pid                           : pid
      type_name                     : type_name
      x_locked                      : x_locked
    <SAW : PAP.Link1 [mom_id_entity]>
      creation                      : creation
      electric                      : electric
      last_change                   : last_change
      last_cid                      : last_cid
      left                          : left
      pid                           : pid
      type_name                     : type_name
      x_locked                      : x_locked
    <SAW : PAP.Address_Position [pap_address_position : mom_id_entity]>
      creation                      : creation
      electric                      : electric
      last_change                   : last_change
      last_cid                      : last_cid
      left                          : address, left
      pid                           : pid
      position                      : position
          height                        : position.height
          lat                           : position.lat
          lon                           : position.lon
      type_name                     : type_name
      x_locked                      : x_locked
    <SAW : PAP._MOM_Link_n_ [mom_id_entity]>
      creation                      : creation
      electric                      : electric
      last_change                   : last_change
      last_cid                      : last_cid
      left                          : left
      pid                           : pid
      right                         : right
      type_name                     : type_name
      x_locked                      : x_locked
    <SAW : PAP.Link2 [mom_id_entity]>
      creation                      : creation
      electric                      : electric
      last_change                   : last_change
      last_cid                      : last_cid
      left                          : left
      pid                           : pid
      right                         : right
      type_name                     : type_name
      x_locked                      : x_locked
    <SAW : PAP.Subject_has_Property [pap_subject_has_property : mom_id_entity]>
      creation                      : creation
      desc                          : desc
      electric                      : electric
      last_change                   : last_change
      last_cid                      : last_cid
      left                          : left, subject
      pid                           : pid
      right                         : property, right
      type_name                     : type_name
      x_locked                      : x_locked
    <SAW : PAP.Person_has_Account [pap_person_has_account : mom_id_entity]>
      creation                      : creation
      electric                      : electric
      last_change                   : last_change
      last_cid                      : last_cid
      left                          : left, person
      pid                           : pid
      right                         : account, right
      type_name                     : type_name
      x_locked                      : x_locked
    <SAW : SRM.Regatta_Result []>
      date                          : date
      software                      : software
      status                        : status
    <SAW : SRM.Id_Entity [mom_id_entity]>
      creation                      : creation
      electric                      : electric
      last_change                   : last_change
      last_cid                      : last_cid
      pid                           : pid
      type_name                     : type_name
      x_locked                      : x_locked
    <SAW : SRM.Object [mom_id_entity]>
      creation                      : creation
      electric                      : electric
      last_change                   : last_change
      last_cid                      : last_cid
      pid                           : pid
      type_name                     : type_name
      x_locked                      : x_locked
    <SAW : SRM._Boat_Class_ [srm__boat_class_ : mom_id_entity]>
      creation                      : creation
      electric                      : electric
      last_change                   : last_change
      last_cid                      : last_cid
      name                          : name
      pid                           : pid
      type_name                     : type_name
      x_locked                      : x_locked
    <SAW : SRM.Boat_Class [srm_boat_class : srm__boat_class_ : mom_id_entity]>
      beam                          : beam
      boats                         : boats
      creation                      : creation
      electric                      : electric
      last_change                   : last_change
      last_cid                      : last_cid
      loa                           : loa
      max_crew                      : max_crew
      name                          : name
      pid                           : pid
      sail_area                     : sail_area
      type_name                     : type_name
      x_locked                      : x_locked
    <SAW : SRM.Handicap [srm_handicap : srm__boat_class_ : mom_id_entity]>
      creation                      : creation
      electric                      : electric
      last_change                   : last_change
      last_cid                      : last_cid
      name                          : name
      pid                           : pid
      type_name                     : type_name
      x_locked                      : x_locked
    <SAW : SRM.Link [mom_id_entity]>
      creation                      : creation
      electric                      : electric
      last_change                   : last_change
      last_cid                      : last_cid
      left                          : left
      pid                           : pid
      type_name                     : type_name
      x_locked                      : x_locked
    <SAW : SRM.Link1 [mom_id_entity]>
      creation                      : creation
      electric                      : electric
      last_change                   : last_change
      last_cid                      : last_cid
      left                          : left
      pid                           : pid
      type_name                     : type_name
      x_locked                      : x_locked
    <SAW : SRM.Boat [srm_boat : mom_id_entity]>
      creation                      : creation
      electric                      : electric
      last_change                   : last_change
      last_cid                      : last_cid
      left                          : b_class, left
      name                          : name
      nation                        : nation
      pid                           : pid
      regatta_links                 : regatta_links
      sail_number                   : sail_number
      sail_number_x                 : sail_number_x
      type_name                     : type_name
      x_locked                      : x_locked
    <SAW : SRM.Club [srm_club : mom_id_entity]>
      creation                      : creation
      electric                      : electric
      last_change                   : last_change
      last_cid                      : last_cid
      long_name                     : long_name
      name                          : name
      pid                           : pid
      type_name                     : type_name
      x_locked                      : x_locked
    <SAW : SRM.Regatta_Event [srm_regatta_event : mom_id_entity]>
      club                          : club
      creation                      : creation
      date                          : date
          alive                         : date.alive
          finish                        : date.finish
          start                         : date.start
      desc                          : desc
      electric                      : electric
      is_cancelled                  : is_cancelled
      last_change                   : last_change
      last_cid                      : last_cid
      name                          : name
      perma_name                    : perma_name
      pid                           : pid
      regattas                      : regattas
      type_name                     : type_name
      x_locked                      : x_locked
      year                          : year
    <SAW : SWP.Link [mom_id_entity]>
      creation                      : creation
      electric                      : electric
      last_change                   : last_change
      last_cid                      : last_cid
      left                          : left
      pid                           : pid
      type_name                     : type_name
      x_locked                      : x_locked
    <SAW : SWP.Link1 [mom_id_entity]>
      creation                      : creation
      electric                      : electric
      last_change                   : last_change
      last_cid                      : last_cid
      left                          : left
      pid                           : pid
      type_name                     : type_name
      x_locked                      : x_locked
    <SAW : SWP.Clip_O [swp_clip_o : mom_id_entity]>
      abstract                      : abstract
      contents                      : contents
      creation                      : creation
      date                          : date
          alive                         : date.alive
          finish                        : date.finish
          start                         : date.start
      date_x                        : date_x
          alive                         : date_x.alive
          finish                        : date_x.finish
          start                         : date_x.start
      electric                      : electric
      last_change                   : last_change
      last_cid                      : last_cid
      left                          : left, object
      pid                           : pid
      prio                          : prio
      type_name                     : type_name
      x_locked                      : x_locked
    <SAW : SWP.Clip_X [swp_clip_x : swp_page : mom_id_entity]>
      clips                         : clips
      contents                      : contents
      creation                      : creation
      date                          : date
          alive                         : date.alive
          finish                        : date.finish
          start                         : date.start
      electric                      : electric
      events                        : events
      format                        : format
      head_line                     : head_line
      hidden                        : hidden
      last_change                   : last_change
      last_cid                      : last_cid
      link_to                       : link_to
      perma_name                    : perma_name
      pid                           : pid
      prio                          : prio
      short_title                   : short_title
      text                          : text
      title                         : title
      type_name                     : type_name
      x_locked                      : x_locked
    <SAW : SWP.Gallery [swp_gallery : mom_id_entity]>
      clips                         : clips
      creation                      : creation
      date                          : date
          alive                         : date.alive
          finish                        : date.finish
          start                         : date.start
      directory                     : directory
      electric                      : electric
      last_change                   : last_change
      last_cid                      : last_cid
      perma_name                    : perma_name
      pictures                      : pictures
      pid                           : pid
      short_title                   : short_title
      title                         : title
      type_name                     : type_name
      x_locked                      : x_locked
    <SAW : MOM.D2_Value_Int []>
      x                             : x
      y                             : y
    <SAW : MOM.D2_Value_Float []>
      x                             : x
      y                             : y
    <SAW : MOM._Pic_ []>
      extension                     : extension
      height                        : height, y
      width                         : width, x
    <SAW : MOM._Thumb_ []>
      extension                     : extension
      height                        : height
      width                         : width
    <SAW : SWP.Picture [swp_picture : mom_id_entity]>
      creation                      : creation
      electric                      : electric
      last_change                   : last_change
      last_cid                      : last_cid
      left                          : gallery, left
      name                          : name
      number                        : number
      photo                         : photo
          extension                     : photo.extension
          height                        : photo.height, photo.y
          width                         : photo.width, photo.x
      pid                           : pid
      thumb                         : thumb
          extension                     : thumb.extension
          height                        : thumb.height
          width                         : thumb.width
      type_name                     : type_name
      x_locked                      : x_locked
    <SAW : SRM.Page [srm_page : swp_page : mom_id_entity]>
      clips                         : clips
      contents                      : contents
      creation                      : creation
      date                          : date
          alive                         : date.alive
          finish                        : date.finish
          start                         : date.start
      desc                          : desc
      electric                      : electric
      event                         : event
      events                        : events
      format                        : format
      head_line                     : head_line
      hidden                        : hidden
      last_change                   : last_change
      last_cid                      : last_cid
      perma_name                    : perma_name
      pid                           : pid
      prio                          : prio
      short_title                   : short_title
      text                          : text
      title                         : title
      type_name                     : type_name
      x_locked                      : x_locked
    <SAW : SRM.Regatta [srm_regatta : mom_id_entity]>
      boat_class                    : boat_class
      boats                         : boats
      creation                      : creation
      discards                      : discards
      electric                      : electric
      is_cancelled                  : is_cancelled
      kind                          : kind
      last_change                   : last_change
      last_cid                      : last_cid
      left                          : event, left
      perma_name                    : perma_name
      pid                           : pid
      races                         : races
      races_counted                 : races_counted
      result                        : result
          date                          : result.date
          software                      : result.software
          status                        : result.status
      type_name                     : type_name
      x_locked                      : x_locked
      year                          : year
    <SAW : SRM.Regatta_C [srm_regatta_c : srm_regatta : mom_id_entity]>
      boat_class                    : boat_class
      boats                         : boats
      creation                      : creation
      discards                      : discards
      electric                      : electric
      is_cancelled                  : is_cancelled
      is_team_race                  : is_team_race
      kind                          : kind
      last_change                   : last_change
      last_cid                      : last_cid
      left                          : event, left
      perma_name                    : perma_name
      pid                           : pid
      races                         : races
      races_counted                 : races_counted
      result                        : result
          date                          : result.date
          software                      : result.software
          status                        : result.status
      teams                         : teams
      type_name                     : type_name
      x_locked                      : x_locked
      year                          : year
    <SAW : SRM.Regatta_H [srm_regatta_h : srm_regatta : mom_id_entity]>
      boat_class                    : boat_class
      boats                         : boats
      creation                      : creation
      discards                      : discards
      electric                      : electric
      handicap                      : handicap
      is_cancelled                  : is_cancelled
      kind                          : kind
      last_change                   : last_change
      last_cid                      : last_cid
      left                          : event, left
      perma_name                    : perma_name
      pid                           : pid
      races                         : races
      races_counted                 : races_counted
      result                        : result
          date                          : result.date
          software                      : result.software
          status                        : result.status
      type_name                     : type_name
      x_locked                      : x_locked
      year                          : year
    <SAW : SRM.Sailor [srm_sailor : mom_id_entity]>
      boat_in_regatta_links         : boat_in_regatta_links
      club                          : club
      creation                      : creation
      electric                      : electric
      last_change                   : last_change
      last_cid                      : last_cid
      left                          : left, person
      mna_number                    : mna_number
      nation                        : nation
      pid                           : pid
      type_name                     : type_name
      x_locked                      : x_locked
    <SAW : SRM._MOM_Link_n_ [mom_id_entity]>
      creation                      : creation
      electric                      : electric
      last_change                   : last_change
      last_cid                      : last_cid
      left                          : left
      pid                           : pid
      right                         : right
      type_name                     : type_name
      x_locked                      : x_locked
    <SAW : SRM.Link2 [mom_id_entity]>
      creation                      : creation
      electric                      : electric
      last_change                   : last_change
      last_cid                      : last_cid
      left                          : left
      pid                           : pid
      right                         : right
      type_name                     : type_name
      x_locked                      : x_locked
    <SAW : SRM.Boat_in_Regatta [srm_boat_in_regatta : mom_id_entity]>
      _crew                         : _crew
      creation                      : creation
      electric                      : electric
      last_change                   : last_change
      last_cid                      : last_cid
      left                          : boat, left
      pid                           : pid
      place                         : place
      points                        : points
      race_results                  : race_results
      rank                          : rank
      registration_date             : registration_date
      right                         : regatta, right
      sailor_links                  : sailor_links
      skipper                       : skipper
      team_links                    : team_links
      teams                         : teams
      type_name                     : type_name
      x_locked                      : x_locked
    <SAW : SRM.Race_Result [srm_race_result : mom_id_entity]>
      creation                      : creation
      discarded                     : discarded
      electric                      : electric
      last_change                   : last_change
      last_cid                      : last_cid
      left                          : boat_in_regatta, left
      pid                           : pid
      points                        : points
      race                          : race
      status                        : status
      type_name                     : type_name
      x_locked                      : x_locked
    <SAW : SRM.Team [srm_team : mom_id_entity]>
      boat_links                    : boat_links
      boats                         : boats
      club                          : club
      creation                      : creation
      desc                          : desc
      electric                      : electric
      last_change                   : last_change
      last_cid                      : last_cid
      leader                        : leader
      left                          : left, regatta
      name                          : name
      pid                           : pid
      place                         : place
      registration_date             : registration_date
      type_name                     : type_name
      x_locked                      : x_locked
    <SAW : SRM.Crew_Member [srm_crew_member : mom_id_entity]>
      creation                      : creation
      electric                      : electric
      key                           : key
      last_change                   : last_change
      last_cid                      : last_cid
      left                          : boat_in_regatta, left
      pid                           : pid
      right                         : right, sailor
      role                          : role
      type_name                     : type_name
      x_locked                      : x_locked
    <SAW : SRM.Team_has_Boat_in_Regatta [srm_team_has_boat_in_regatta : mom_id_entity]>
      creation                      : creation
      electric                      : electric
      last_change                   : last_change
      last_cid                      : last_cid
      left                          : left, team
      pid                           : pid
      right                         : boat, right
      type_name                     : type_name
      x_locked                      : x_locked
    <SAW : PAP.Subject_has_Address [pap_subject_has_property : mom_id_entity]>
      creation                      : creation
      desc                          : desc
      electric                      : electric
      last_change                   : last_change
      last_cid                      : last_cid
      left                          : left, subject
      pid                           : pid
      right                         : address, property, right
      type_name                     : type_name
      x_locked                      : x_locked
    <SAW : PAP.Subject_has_Email [pap_subject_has_property : mom_id_entity]>
      creation                      : creation
      desc                          : desc
      electric                      : electric
      last_change                   : last_change
      last_cid                      : last_cid
      left                          : left, subject
      pid                           : pid
      right                         : email, property, right
      type_name                     : type_name
      x_locked                      : x_locked
    <SAW : PAP.Subject_has_Phone [pap_subject_has_phone : pap_subject_has_property : mom_id_entity]>
      creation                      : creation
      desc                          : desc
      electric                      : electric
      extension                     : extension
      last_change                   : last_change
      last_cid                      : last_cid
      left                          : left, subject
      pid                           : pid
      right                         : phone, property, right
      type_name                     : type_name
      x_locked                      : x_locked
    <SAW : PAP.Subject_has_Url [pap_subject_has_property : mom_id_entity]>
      creation                      : creation
      desc                          : desc
      electric                      : electric
      last_change                   : last_change
      last_cid                      : last_cid
      left                          : left, subject
      pid                           : pid
      right                         : property, right, url
      type_name                     : type_name
      x_locked                      : x_locked
    <SAW : PAP.Company_has_Url [pap_company_has_url : pap_subject_has_property : mom_id_entity]>
      creation                      : creation
      desc                          : desc
      electric                      : electric
      last_change                   : last_change
      last_cid                      : last_cid
      left                          : company, left, subject
      pid                           : pid
      right                         : property, right, url
      type_name                     : type_name
      x_locked                      : x_locked
    <SAW : PAP.Person_has_Url [pap_person_has_url : pap_subject_has_property : mom_id_entity]>
      creation                      : creation
      desc                          : desc
      electric                      : electric
      last_change                   : last_change
      last_cid                      : last_cid
      left                          : left, person, subject
      pid                           : pid
      right                         : property, right, url
      type_name                     : type_name
      x_locked                      : x_locked
    <SAW : PAP.Company_has_Phone [pap_company_has_phone : pap_subject_has_phone : pap_subject_has_property : mom_id_entity]>
      creation                      : creation
      desc                          : desc
      electric                      : electric
      extension                     : extension
      last_change                   : last_change
      last_cid                      : last_cid
      left                          : company, left, subject
      pid                           : pid
      right                         : phone, property, right
      type_name                     : type_name
      x_locked                      : x_locked
    <SAW : PAP.Person_has_Phone [pap_person_has_phone : pap_subject_has_phone : pap_subject_has_property : mom_id_entity]>
      creation                      : creation
      desc                          : desc
      electric                      : electric
      extension                     : extension
      last_change                   : last_change
      last_cid                      : last_cid
      left                          : left, person, subject
      pid                           : pid
      right                         : phone, property, right
      type_name                     : type_name
      x_locked                      : x_locked
    <SAW : PAP.Company_has_Email [pap_company_has_email : pap_subject_has_property : mom_id_entity]>
      creation                      : creation
      desc                          : desc
      electric                      : electric
      last_change                   : last_change
      last_cid                      : last_cid
      left                          : company, left, subject
      pid                           : pid
      right                         : email, property, right
      type_name                     : type_name
      x_locked                      : x_locked
    <SAW : PAP.Person_has_Email [pap_person_has_email : pap_subject_has_property : mom_id_entity]>
      creation                      : creation
      desc                          : desc
      electric                      : electric
      last_change                   : last_change
      last_cid                      : last_cid
      left                          : left, person, subject
      pid                           : pid
      right                         : email, property, right
      type_name                     : type_name
      x_locked                      : x_locked
    <SAW : PAP.Company_has_Address [pap_company_has_address : pap_subject_has_property : mom_id_entity]>
      creation                      : creation
      desc                          : desc
      electric                      : electric
      last_change                   : last_change
      last_cid                      : last_cid
      left                          : company, left, subject
      pid                           : pid
      right                         : address, property, right
      type_name                     : type_name
      x_locked                      : x_locked
    <SAW : PAP.Person_has_Address [pap_person_has_address : pap_subject_has_property : mom_id_entity]>
      creation                      : creation
      desc                          : desc
      electric                      : electric
      last_change                   : last_change
      last_cid                      : last_cid
      left                          : left, person, subject
      pid                           : pid
      right                         : address, property, right
      type_name                     : type_name
      x_locked                      : x_locked

"""

_test_q_result = """
    >>> apt, url = Scaffold.app_type_and_url (%(p1)s, %(n1)s)

    >>> ET = apt ["PAP.Person"]
    >>> qrt = apt.DBW.PNS.Q_Result.E_Type (ET, _strict = False)

    >>> print (qrt.filter (pid = 1).attr (Q.lifetime)) ### PAP.Person
    SQL: SELECT DISTINCT
           pap_person.lifetime__finish AS pap_person_lifetime__finish,
           pap_person.lifetime__start AS pap_person_lifetime__start
         FROM mom_id_entity
           JOIN pap_person ON mom_id_entity.pid = pap_person.pid
         WHERE mom_id_entity.pid = :pid_1

    >>> print (qrt.attrs (Q.last_name, Q.lifetime)) ### PAP.Person
    SQL: SELECT DISTINCT
           pap_person.last_name AS pap_person_last_name,
           pap_person.lifetime__finish AS pap_person_lifetime__finish,
           pap_person.lifetime__start AS pap_person_lifetime__start
         FROM mom_id_entity
           JOIN pap_person ON mom_id_entity.pid = pap_person.pid

    >>> show_query (qrt.filter (Q.pid.IN ([1, 2]))) ### PAP.Person
    SQL: SELECT
           mom_id_entity.electric AS mom_id_entity_electric,
           mom_id_entity.last_cid AS mom_id_entity_last_cid,
           mom_id_entity.pid AS mom_id_entity_pid,
           mom_id_entity.type_name AS mom_id_entity_type_name,
           mom_id_entity.x_locked AS mom_id_entity_x_locked,
           pap_person.__raw_first_name AS pap_person___raw_first_name,
           pap_person.__raw_last_name AS pap_person___raw_last_name,
           pap_person.__raw_middle_name AS pap_person___raw_middle_name,
           pap_person.__raw_title AS pap_person___raw_title,
           pap_person.first_name AS pap_person_first_name,
           pap_person.last_name AS pap_person_last_name,
           pap_person.lifetime__finish AS pap_person_lifetime__finish,
           pap_person.lifetime__start AS pap_person_lifetime__start,
           pap_person.middle_name AS pap_person_middle_name,
           pap_person.pid AS pap_person_pid,
           pap_person.sex AS pap_person_sex,
           pap_person.title AS pap_person_title
         FROM mom_id_entity
           JOIN pap_person ON mom_id_entity.pid = pap_person.pid
         WHERE mom_id_entity.pid IN (:pid_1, :pid_2)
    Parameters:
         pid_1                : 1
         pid_2                : 2

    >>> print (qrt.order_by (ET.sorted_by_epk)) ### PAP.Person
    SQL: SELECT
           mom_id_entity.electric AS mom_id_entity_electric,
           mom_id_entity.last_cid AS mom_id_entity_last_cid,
           mom_id_entity.pid AS mom_id_entity_pid,
           mom_id_entity.type_name AS mom_id_entity_type_name,
           mom_id_entity.x_locked AS mom_id_entity_x_locked,
           pap_person.__raw_first_name AS pap_person___raw_first_name,
           pap_person.__raw_last_name AS pap_person___raw_last_name,
           pap_person.__raw_middle_name AS pap_person___raw_middle_name,
           pap_person.__raw_title AS pap_person___raw_title,
           pap_person.first_name AS pap_person_first_name,
           pap_person.last_name AS pap_person_last_name,
           pap_person.lifetime__finish AS pap_person_lifetime__finish,
           pap_person.lifetime__start AS pap_person_lifetime__start,
           pap_person.middle_name AS pap_person_middle_name,
           pap_person.pid AS pap_person_pid,
           pap_person.sex AS pap_person_sex,
           pap_person.title AS pap_person_title
         FROM mom_id_entity
           JOIN pap_person ON mom_id_entity.pid = pap_person.pid
         ORDER BY pap_person.last_name, pap_person.first_name, pap_person.middle_name, pap_person.title

    >>> print (qrt.filter (Q.RAW.last_name == "Tanzer")) ### PAP.Person
    SQL: SELECT
           mom_id_entity.electric AS mom_id_entity_electric,
           mom_id_entity.last_cid AS mom_id_entity_last_cid,
           mom_id_entity.pid AS mom_id_entity_pid,
           mom_id_entity.type_name AS mom_id_entity_type_name,
           mom_id_entity.x_locked AS mom_id_entity_x_locked,
           pap_person.__raw_first_name AS pap_person___raw_first_name,
           pap_person.__raw_last_name AS pap_person___raw_last_name,
           pap_person.__raw_middle_name AS pap_person___raw_middle_name,
           pap_person.__raw_title AS pap_person___raw_title,
           pap_person.first_name AS pap_person_first_name,
           pap_person.last_name AS pap_person_last_name,
           pap_person.lifetime__finish AS pap_person_lifetime__finish,
           pap_person.lifetime__start AS pap_person_lifetime__start,
           pap_person.middle_name AS pap_person_middle_name,
           pap_person.pid AS pap_person_pid,
           pap_person.sex AS pap_person_sex,
           pap_person.title AS pap_person_title
         FROM mom_id_entity
           JOIN pap_person ON mom_id_entity.pid = pap_person.pid
          WHERE pap_person.__raw_last_name = :__raw_last_name_1

    >>> show_query (qrt.filter ((Q.RAW.title.STARTSWITH ("D")))) ### PAP.Person
    SQL: SELECT
           mom_id_entity.electric AS mom_id_entity_electric,
           mom_id_entity.last_cid AS mom_id_entity_last_cid,
           mom_id_entity.pid AS mom_id_entity_pid,
           mom_id_entity.type_name AS mom_id_entity_type_name,
           mom_id_entity.x_locked AS mom_id_entity_x_locked,
           pap_person.__raw_first_name AS pap_person___raw_first_name,
           pap_person.__raw_last_name AS pap_person___raw_last_name,
           pap_person.__raw_middle_name AS pap_person___raw_middle_name,
           pap_person.__raw_title AS pap_person___raw_title,
           pap_person.first_name AS pap_person_first_name,
           pap_person.last_name AS pap_person_last_name,
           pap_person.lifetime__finish AS pap_person_lifetime__finish,
           pap_person.lifetime__start AS pap_person_lifetime__start,
           pap_person.middle_name AS pap_person_middle_name,
           pap_person.pid AS pap_person_pid,
           pap_person.sex AS pap_person_sex,
           pap_person.title AS pap_person_title
         FROM mom_id_entity
           JOIN pap_person ON mom_id_entity.pid = pap_person.pid
         WHERE pap_person.__raw_title LIKE :__raw_title_1 || '%%%%'
    Parameters:
         __raw_title_1        : u'D'

    >>> show_query (qrt.filter (Q.RAW.title.STARTSWITH ("D")).attrs (Q.title, Q.SUM (1))) ### PAP.Person
    SQL: SELECT DISTINCT
           pap_person.title AS pap_person_title,
           sum(:param_1) AS sum_1
         FROM mom_id_entity
           JOIN pap_person ON mom_id_entity.pid = pap_person.pid
         WHERE pap_person.__raw_title LIKE :__raw_title_1 || '%%%%'
    Parameters:
         __raw_title_1        : u'D'
         param_1              : 1

    >>> ET = apt ["PAP.Subject"]
    >>> qrs = apt.DBW.PNS.Q_Result.E_Type (ET, _strict = True)
    >>> qrt = apt.DBW.PNS.Q_Result.E_Type (ET, _strict = False)

    >>> print (ET._SAW) ### PAP.Subject
    <SAW : PAP.Subject [mom_id_entity]>

    >>> print (qrs) ### PAP.Subject
    SQL: SELECT mom_id_entity.pid
         FROM mom_id_entity
         WHERE false

    >>> print (qrt) ### PAP.Subject
    SQL: SELECT
           mom_id_entity.electric AS mom_id_entity_electric,
           mom_id_entity.last_cid AS mom_id_entity_last_cid,
           mom_id_entity.pid AS mom_id_entity_pid,
           mom_id_entity.type_name AS mom_id_entity_type_name,
           mom_id_entity.x_locked AS mom_id_entity_x_locked,
           pap_company.__raw_name AS pap_company___raw_name,
           pap_company.__raw_registered_in AS pap_company___raw_registered_in,
           pap_company.__raw_short_name AS pap_company___raw_short_name,
           pap_company.lifetime__finish AS pap_company_lifetime__finish,
           pap_company.lifetime__start AS pap_company_lifetime__start,
           pap_company.name AS pap_company_name,
           pap_company.pid AS pap_company_pid,
           pap_company.registered_in AS pap_company_registered_in,
           pap_company.short_name AS pap_company_short_name,
           pap_person.__raw_first_name AS pap_person___raw_first_name,
           pap_person.__raw_last_name AS pap_person___raw_last_name,
           pap_person.__raw_middle_name AS pap_person___raw_middle_name,
           pap_person.__raw_title AS pap_person___raw_title,
           pap_person.first_name AS pap_person_first_name,
           pap_person.last_name AS pap_person_last_name,
           pap_person.lifetime__finish AS pap_person_lifetime__finish,
           pap_person.lifetime__start AS pap_person_lifetime__start,
           pap_person.middle_name AS pap_person_middle_name,
           pap_person.pid AS pap_person_pid,
           pap_person.sex AS pap_person_sex,
           pap_person.title AS pap_person_title
         FROM mom_id_entity
           LEFT OUTER JOIN pap_company ON mom_id_entity.pid = pap_company.pid
           LEFT OUTER JOIN pap_person ON mom_id_entity.pid = pap_person.pid
         WHERE mom_id_entity.pid = pap_company.pid
            OR mom_id_entity.pid = pap_person.pid

    >>> print (qrt.filter (Q.creation.user == 42)) ### PAP.Subject
    SQL: SELECT
           mom_id_entity.electric AS mom_id_entity_electric,
           mom_id_entity.last_cid AS mom_id_entity_last_cid,
           mom_id_entity.pid AS mom_id_entity_pid,
           mom_id_entity.type_name AS mom_id_entity_type_name,
           mom_id_entity.x_locked AS mom_id_entity_x_locked,
           pap_company.__raw_name AS pap_company___raw_name,
           pap_company.__raw_registered_in AS pap_company___raw_registered_in,
           pap_company.__raw_short_name AS pap_company___raw_short_name,
           pap_company.lifetime__finish AS pap_company_lifetime__finish,
           pap_company.lifetime__start AS pap_company_lifetime__start,
           pap_company.name AS pap_company_name,
           pap_company.pid AS pap_company_pid,
           pap_company.registered_in AS pap_company_registered_in,
           pap_company.short_name AS pap_company_short_name,
           pap_person.__raw_first_name AS pap_person___raw_first_name,
           pap_person.__raw_last_name AS pap_person___raw_last_name,
           pap_person.__raw_middle_name AS pap_person___raw_middle_name,
           pap_person.__raw_title AS pap_person___raw_title,
           pap_person.first_name AS pap_person_first_name,
           pap_person.last_name AS pap_person_last_name,
           pap_person.lifetime__finish AS pap_person_lifetime__finish,
           pap_person.lifetime__start AS pap_person_lifetime__start,
           pap_person.middle_name AS pap_person_middle_name,
           pap_person.pid AS pap_person_pid,
           pap_person.sex AS pap_person_sex,
           pap_person.title AS pap_person_title
         FROM mom_id_entity
           LEFT OUTER JOIN pap_company ON mom_id_entity.pid = pap_company.pid
           LEFT OUTER JOIN pap_person ON mom_id_entity.pid = pap_person.pid
           LEFT OUTER JOIN mom_md_change AS mom_md_change__1 ON mom_md_change__1.pid = mom_id_entity.pid
         WHERE (mom_id_entity.pid = pap_company.pid
            OR mom_id_entity.pid = pap_person.pid)
            AND mom_md_change__1.kind = :kind_1
            AND mom_md_change__1."user" = :user_1

    >>> ET = apt ["MOM.MD_Change"]
    >>> qrt = apt.DBW.PNS.Q_Result.E_Type (ET, _strict = False)
    >>> print (qrt.filter (Q.parent_cid == 23)) ### MOM.MD_Change
    SQL: SELECT
           mom_md_change."user" AS mom_md_change_user,
           mom_md_change.c_time AS mom_md_change_c_time,
           mom_md_change.c_user AS mom_md_change_c_user,
           mom_md_change.cid AS mom_md_change_cid,
           mom_md_change.kind AS mom_md_change_kind,
           mom_md_change.parent_cid AS mom_md_change_parent_cid,
           mom_md_change.pid AS mom_md_change_pid,
           mom_md_change.scm_change AS mom_md_change_scm_change,
           mom_md_change.time AS mom_md_change_time,
           mom_md_change.type_name AS mom_md_change_type_name
         FROM mom_md_change
         WHERE mom_md_change.parent_cid = :parent_cid_1

    >>> print (qrt.filter (Q.user.creation.user == Q.user, Q.parent_cid == 23)) ### MOM.MD_Change
    SQL: SELECT
           mom_md_change."user" AS mom_md_change_user,
           mom_md_change.c_time AS mom_md_change_c_time,
           mom_md_change.c_user AS mom_md_change_c_user,
           mom_md_change.cid AS mom_md_change_cid,
           mom_md_change.kind AS mom_md_change_kind,
           mom_md_change.parent_cid AS mom_md_change_parent_cid,
           mom_md_change.pid AS mom_md_change_pid,
           mom_md_change.scm_change AS mom_md_change_scm_change,
           mom_md_change.time AS mom_md_change_time,
           mom_md_change.type_name AS mom_md_change_type_name
         FROM mom_md_change
           JOIN mom_id_entity AS mom_id_entity__1 ON mom_id_entity__1.pid = mom_md_change."user"
           JOIN mom_md_change AS mom_md_change__2 ON mom_md_change__2.pid = mom_id_entity__1.pid
         WHERE mom_md_change__2.kind = :kind_1
            AND mom_md_change__2."user" = mom_md_change."user"
            AND mom_md_change.parent_cid = :parent_cid_1

    >>> ET = apt ["SRM.Regatta_H"]
    >>> qrs = apt.DBW.PNS.Q_Result.E_Type (ET, _strict = True)
    >>> qrt = apt.DBW.PNS.Q_Result.E_Type (ET, _strict = False)

    >>> print (qrt) ### SRM.Regatta_H
    SQL: SELECT
           mom_id_entity.electric AS mom_id_entity_electric,
           mom_id_entity.last_cid AS mom_id_entity_last_cid,
           mom_id_entity.pid AS mom_id_entity_pid,
           mom_id_entity.type_name AS mom_id_entity_type_name,
           mom_id_entity.x_locked AS mom_id_entity_x_locked,
           srm_regatta."left" AS srm_regatta_left,
           srm_regatta.boat_class AS srm_regatta_boat_class,
           srm_regatta.discards AS srm_regatta_discards,
           srm_regatta.is_cancelled AS srm_regatta_is_cancelled,
           srm_regatta.kind AS srm_regatta_kind,
           srm_regatta.perma_name AS srm_regatta_perma_name,
           srm_regatta.pid AS srm_regatta_pid,
           srm_regatta.races AS srm_regatta_races,
           srm_regatta.result__date AS srm_regatta_result__date,
           srm_regatta.result__software AS srm_regatta_result__software,
           srm_regatta.result__status AS srm_regatta_result__status,
           srm_regatta_h.pid AS srm_regatta_h_pid
         FROM mom_id_entity
           JOIN srm_regatta ON mom_id_entity.pid = srm_regatta.pid
           JOIN srm_regatta_h ON srm_regatta.pid = srm_regatta_h.pid

    >>> ET = apt ["SRM.Regatta"]
    >>> qrs = apt.DBW.PNS.Q_Result.E_Type (ET, _strict = True)
    >>> qrt = apt.DBW.PNS.Q_Result.E_Type (ET, _strict = False)

    >>> print (ET._SAW) ### SRM.Regatta
    <SAW : SRM.Regatta [srm_regatta : mom_id_entity]>

    >>> print (qrs) ### SRM.Regatta
    SQL: SELECT srm_regatta.pid
         FROM srm_regatta
         WHERE false

    >>> print (qrt) ### SRM.Regatta
    SQL: SELECT
           mom_id_entity.electric AS mom_id_entity_electric,
           mom_id_entity.last_cid AS mom_id_entity_last_cid,
           mom_id_entity.pid AS mom_id_entity_pid,
           mom_id_entity.type_name AS mom_id_entity_type_name,
           mom_id_entity.x_locked AS mom_id_entity_x_locked,
           srm_regatta."left" AS srm_regatta_left,
           srm_regatta.boat_class AS srm_regatta_boat_class,
           srm_regatta.discards AS srm_regatta_discards,
           srm_regatta.is_cancelled AS srm_regatta_is_cancelled,
           srm_regatta.kind AS srm_regatta_kind,
           srm_regatta.perma_name AS srm_regatta_perma_name,
           srm_regatta.pid AS srm_regatta_pid,
           srm_regatta.races AS srm_regatta_races,
           srm_regatta.result__date AS srm_regatta_result__date,
           srm_regatta.result__software AS srm_regatta_result__software,
           srm_regatta.result__status AS srm_regatta_result__status,
           srm_regatta_c.is_team_race AS srm_regatta_c_is_team_race,
           srm_regatta_c.pid AS srm_regatta_c_pid
         FROM mom_id_entity
           JOIN srm_regatta ON mom_id_entity.pid = srm_regatta.pid
           LEFT OUTER JOIN srm_regatta_c ON srm_regatta.pid = srm_regatta_c.pid

    >>> print (qrt.filter (Q.RAW.left.date.start == "2008/05/01")) ### SRM.Regatta
    SQL: SELECT
           mom_id_entity.electric AS mom_id_entity_electric,
           mom_id_entity.last_cid AS mom_id_entity_last_cid,
           mom_id_entity.pid AS mom_id_entity_pid,
           mom_id_entity.type_name AS mom_id_entity_type_name,
           mom_id_entity.x_locked AS mom_id_entity_x_locked,
           srm_regatta."left" AS srm_regatta_left,
           srm_regatta.boat_class AS srm_regatta_boat_class,
           srm_regatta.discards AS srm_regatta_discards,
           srm_regatta.is_cancelled AS srm_regatta_is_cancelled,
           srm_regatta.kind AS srm_regatta_kind,
           srm_regatta.perma_name AS srm_regatta_perma_name,
           srm_regatta.pid AS srm_regatta_pid,
           srm_regatta.races AS srm_regatta_races,
           srm_regatta.result__date AS srm_regatta_result__date,
           srm_regatta.result__software AS srm_regatta_result__software,
           srm_regatta.result__status AS srm_regatta_result__status,
           srm_regatta_c.is_team_race AS srm_regatta_c_is_team_race,
           srm_regatta_c.pid AS srm_regatta_c_pid
         FROM mom_id_entity
           JOIN srm_regatta ON mom_id_entity.pid = srm_regatta.pid
           LEFT OUTER JOIN srm_regatta_c ON srm_regatta.pid = srm_regatta_c.pid
           JOIN srm_regatta_event AS srm_regatta_event__1 ON srm_regatta_event__1.pid = srm_regatta."left"
         WHERE srm_regatta_event__1.date__start = :date__start_1

    >>> ET = apt ["SRM.Regatta_C"]
    >>> qrs = apt.DBW.PNS.Q_Result.E_Type (ET, _strict = True)
    >>> qrt = apt.DBW.PNS.Q_Result.E_Type (ET, _strict = False)

    >>> print (ET._SAW) ### SRM.Regatta_C
    <SAW : SRM.Regatta_C [srm_regatta_c : srm_regatta : mom_id_entity]>

    >>> print (qrs) ### SRM.Regatta_C
    SQL: SELECT
           mom_id_entity.electric AS mom_id_entity_electric,
           mom_id_entity.last_cid AS mom_id_entity_last_cid,
           mom_id_entity.pid AS mom_id_entity_pid,
           mom_id_entity.type_name AS mom_id_entity_type_name,
           mom_id_entity.x_locked AS mom_id_entity_x_locked,
           srm_regatta."left" AS srm_regatta_left,
           srm_regatta.boat_class AS srm_regatta_boat_class,
           srm_regatta.discards AS srm_regatta_discards,
           srm_regatta.is_cancelled AS srm_regatta_is_cancelled,
           srm_regatta.kind AS srm_regatta_kind,
           srm_regatta.perma_name AS srm_regatta_perma_name,
           srm_regatta.pid AS srm_regatta_pid,
           srm_regatta.races AS srm_regatta_races,
           srm_regatta.result__date AS srm_regatta_result__date,
           srm_regatta.result__software AS srm_regatta_result__software,
           srm_regatta.result__status AS srm_regatta_result__status,
           srm_regatta_c.is_team_race AS srm_regatta_c_is_team_race,
           srm_regatta_c.pid AS srm_regatta_c_pid
         FROM mom_id_entity
           JOIN srm_regatta ON mom_id_entity.pid = srm_regatta.pid
           JOIN srm_regatta_c ON srm_regatta.pid = srm_regatta_c.pid
         WHERE mom_id_entity.type_name = :type_name_1

    >>> print (qrt) ### SRM.Regatta_C
    SQL: SELECT
           mom_id_entity.electric AS mom_id_entity_electric,
           mom_id_entity.last_cid AS mom_id_entity_last_cid,
           mom_id_entity.pid AS mom_id_entity_pid,
           mom_id_entity.type_name AS mom_id_entity_type_name,
           mom_id_entity.x_locked AS mom_id_entity_x_locked,
           srm_regatta."left" AS srm_regatta_left,
           srm_regatta.boat_class AS srm_regatta_boat_class,
           srm_regatta.discards AS srm_regatta_discards,
           srm_regatta.is_cancelled AS srm_regatta_is_cancelled,
           srm_regatta.kind AS srm_regatta_kind,
           srm_regatta.perma_name AS srm_regatta_perma_name,
           srm_regatta.pid AS srm_regatta_pid,
           srm_regatta.races AS srm_regatta_races,
           srm_regatta.result__date AS srm_regatta_result__date,
           srm_regatta.result__software AS srm_regatta_result__software,
           srm_regatta.result__status AS srm_regatta_result__status,
           srm_regatta_c.is_team_race AS srm_regatta_c_is_team_race,
           srm_regatta_c.pid AS srm_regatta_c_pid
         FROM mom_id_entity
           JOIN srm_regatta ON mom_id_entity.pid = srm_regatta.pid
           JOIN srm_regatta_c ON srm_regatta.pid = srm_regatta_c.pid

    >>> print (qrt.limit (5).offset (10)) ### SRM.Regatta_C
    SQL: SELECT
           mom_id_entity.electric AS mom_id_entity_electric,
           mom_id_entity.last_cid AS mom_id_entity_last_cid,
           mom_id_entity.pid AS mom_id_entity_pid,
           mom_id_entity.type_name AS mom_id_entity_type_name,
           mom_id_entity.x_locked AS mom_id_entity_x_locked,
           srm_regatta."left" AS srm_regatta_left,
           srm_regatta.boat_class AS srm_regatta_boat_class,
           srm_regatta.discards AS srm_regatta_discards,
           srm_regatta.is_cancelled AS srm_regatta_is_cancelled,
           srm_regatta.kind AS srm_regatta_kind,
           srm_regatta.perma_name AS srm_regatta_perma_name,
           srm_regatta.pid AS srm_regatta_pid,
           srm_regatta.races AS srm_regatta_races,
           srm_regatta.result__date AS srm_regatta_result__date,
           srm_regatta.result__software AS srm_regatta_result__software,
           srm_regatta.result__status AS srm_regatta_result__status,
           srm_regatta_c.is_team_race AS srm_regatta_c_is_team_race,
           srm_regatta_c.pid AS srm_regatta_c_pid
         FROM mom_id_entity
           JOIN srm_regatta ON mom_id_entity.pid = srm_regatta.pid
           JOIN srm_regatta_c ON srm_regatta.pid = srm_regatta_c.pid
         LIMIT :param_1 OFFSET :param_2

    >>> show_query (qrt.filter (Q.event.date.start >= "2010/01/01", Q.event.date.start <= "2010/12/31")) ### SRM.Regatta_C
    SQL: SELECT
           mom_id_entity.electric AS mom_id_entity_electric,
           mom_id_entity.last_cid AS mom_id_entity_last_cid,
           mom_id_entity.pid AS mom_id_entity_pid,
           mom_id_entity.type_name AS mom_id_entity_type_name,
           mom_id_entity.x_locked AS mom_id_entity_x_locked,
           srm_regatta."left" AS srm_regatta_left,
           srm_regatta.boat_class AS srm_regatta_boat_class,
           srm_regatta.discards AS srm_regatta_discards,
           srm_regatta.is_cancelled AS srm_regatta_is_cancelled,
           srm_regatta.kind AS srm_regatta_kind,
           srm_regatta.perma_name AS srm_regatta_perma_name,
           srm_regatta.pid AS srm_regatta_pid,
           srm_regatta.races AS srm_regatta_races,
           srm_regatta.result__date AS srm_regatta_result__date,
           srm_regatta.result__software AS srm_regatta_result__software,
           srm_regatta.result__status AS srm_regatta_result__status,
           srm_regatta_c.is_team_race AS srm_regatta_c_is_team_race,
           srm_regatta_c.pid AS srm_regatta_c_pid
         FROM mom_id_entity
           JOIN srm_regatta ON mom_id_entity.pid = srm_regatta.pid
           JOIN srm_regatta_c ON srm_regatta.pid = srm_regatta_c.pid
           JOIN srm_regatta_event AS srm_regatta_event__1 ON srm_regatta_event__1.pid = srm_regatta."left"
         WHERE srm_regatta_event__1.date__start >= :date__start_1
            AND srm_regatta_event__1.date__start <= :date__start_2
    Parameters:
         date__start_1        : datetime.date(2010, 1, 1)
         date__start_2        : datetime.date(2010, 12, 31)

    >>> show_query (qrt.filter (Q.event.date.start.D.YEAR (2010))) ### SRM.Regatta_C
    SQL: SELECT
           mom_id_entity.electric AS mom_id_entity_electric,
           mom_id_entity.last_cid AS mom_id_entity_last_cid,
           mom_id_entity.pid AS mom_id_entity_pid,
           mom_id_entity.type_name AS mom_id_entity_type_name,
           mom_id_entity.x_locked AS mom_id_entity_x_locked,
           srm_regatta."left" AS srm_regatta_left,
           srm_regatta.boat_class AS srm_regatta_boat_class,
           srm_regatta.discards AS srm_regatta_discards,
           srm_regatta.is_cancelled AS srm_regatta_is_cancelled,
           srm_regatta.kind AS srm_regatta_kind,
           srm_regatta.perma_name AS srm_regatta_perma_name,
           srm_regatta.pid AS srm_regatta_pid,
           srm_regatta.races AS srm_regatta_races,
           srm_regatta.result__date AS srm_regatta_result__date,
           srm_regatta.result__software AS srm_regatta_result__software,
           srm_regatta.result__status AS srm_regatta_result__status,
           srm_regatta_c.is_team_race AS srm_regatta_c_is_team_race,
           srm_regatta_c.pid AS srm_regatta_c_pid
         FROM mom_id_entity
           JOIN srm_regatta ON mom_id_entity.pid = srm_regatta.pid
           JOIN srm_regatta_c ON srm_regatta.pid = srm_regatta_c.pid
           JOIN srm_regatta_event AS srm_regatta_event__1 ON srm_regatta_event__1.pid = srm_regatta."left"
         WHERE srm_regatta_event__1.date__start IS NOT NULL
            AND srm_regatta_event__1.date__start >= :date__start_1
            AND srm_regatta_event__1.date__start <= :date__start_2
    Parameters:
         date__start_1        : datetime.date(2010, 1, 1)
         date__start_2        : datetime.date(2010, 12, 31)

    >>> print (qrt.group_by (Q.is_team_race)) ### SRM.Regatta_C
    SQL: SELECT
           mom_id_entity.electric AS mom_id_entity_electric,
           mom_id_entity.last_cid AS mom_id_entity_last_cid,
           mom_id_entity.pid AS mom_id_entity_pid,
           mom_id_entity.type_name AS mom_id_entity_type_name,
           mom_id_entity.x_locked AS mom_id_entity_x_locked,
           srm_regatta."left" AS srm_regatta_left,
           srm_regatta.boat_class AS srm_regatta_boat_class,
           srm_regatta.discards AS srm_regatta_discards,
           srm_regatta.is_cancelled AS srm_regatta_is_cancelled,
           srm_regatta.kind AS srm_regatta_kind,
           srm_regatta.perma_name AS srm_regatta_perma_name,
           srm_regatta.pid AS srm_regatta_pid,
           srm_regatta.races AS srm_regatta_races,
           srm_regatta.result__date AS srm_regatta_result__date,
           srm_regatta.result__software AS srm_regatta_result__software,
           srm_regatta.result__status AS srm_regatta_result__status,
           srm_regatta_c.is_team_race AS srm_regatta_c_is_team_race,
           srm_regatta_c.pid AS srm_regatta_c_pid
         FROM mom_id_entity
           JOIN srm_regatta ON mom_id_entity.pid = srm_regatta.pid
           JOIN srm_regatta_c ON srm_regatta.pid = srm_regatta_c.pid GROUP BY srm_regatta_c.is_team_race

    >>> print (qrt.group_by ("boat_class")) ### SRM.Regatta_C
    SQL: SELECT
           mom_id_entity.electric AS mom_id_entity_electric,
           mom_id_entity.last_cid AS mom_id_entity_last_cid,
           mom_id_entity.pid AS mom_id_entity_pid,
           mom_id_entity.type_name AS mom_id_entity_type_name,
           mom_id_entity.x_locked AS mom_id_entity_x_locked,
           srm_regatta."left" AS srm_regatta_left,
           srm_regatta.boat_class AS srm_regatta_boat_class,
           srm_regatta.discards AS srm_regatta_discards,
           srm_regatta.is_cancelled AS srm_regatta_is_cancelled,
           srm_regatta.kind AS srm_regatta_kind,
           srm_regatta.perma_name AS srm_regatta_perma_name,
           srm_regatta.pid AS srm_regatta_pid,
           srm_regatta.races AS srm_regatta_races,
           srm_regatta.result__date AS srm_regatta_result__date,
           srm_regatta.result__software AS srm_regatta_result__software,
           srm_regatta.result__status AS srm_regatta_result__status,
           srm_regatta_c.is_team_race AS srm_regatta_c_is_team_race,
           srm_regatta_c.pid AS srm_regatta_c_pid
         FROM mom_id_entity
           JOIN srm_regatta ON mom_id_entity.pid = srm_regatta.pid
           JOIN srm_regatta_c ON srm_regatta.pid = srm_regatta_c.pid GROUP BY srm_regatta.boat_class

    >>> print (qrt.filter (Q.boat_class)) ### SRM.Regatta_C
    SQL: SELECT
           mom_id_entity.electric AS mom_id_entity_electric,
           mom_id_entity.last_cid AS mom_id_entity_last_cid,
           mom_id_entity.pid AS mom_id_entity_pid,
           mom_id_entity.type_name AS mom_id_entity_type_name,
           mom_id_entity.x_locked AS mom_id_entity_x_locked,
           srm_regatta."left" AS srm_regatta_left,
           srm_regatta.boat_class AS srm_regatta_boat_class,
           srm_regatta.discards AS srm_regatta_discards,
           srm_regatta.is_cancelled AS srm_regatta_is_cancelled,
           srm_regatta.kind AS srm_regatta_kind,
           srm_regatta.perma_name AS srm_regatta_perma_name,
           srm_regatta.pid AS srm_regatta_pid,
           srm_regatta.races AS srm_regatta_races,
           srm_regatta.result__date AS srm_regatta_result__date,
           srm_regatta.result__software AS srm_regatta_result__software,
           srm_regatta.result__status AS srm_regatta_result__status,
           srm_regatta_c.is_team_race AS srm_regatta_c_is_team_race,
           srm_regatta_c.pid AS srm_regatta_c_pid
         FROM mom_id_entity
           JOIN srm_regatta ON mom_id_entity.pid = srm_regatta.pid
           JOIN srm_regatta_c ON srm_regatta.pid = srm_regatta_c.pid
         WHERE srm_regatta.boat_class IS NOT NULL

    >>> print (qrt.filter (Q.RAW.boat_class.max_crew <= "2")) ### SRM.Regatta_C
    SQL: SELECT
           mom_id_entity.electric AS mom_id_entity_electric,
           mom_id_entity.last_cid AS mom_id_entity_last_cid,
           mom_id_entity.pid AS mom_id_entity_pid,
           mom_id_entity.type_name AS mom_id_entity_type_name,
           mom_id_entity.x_locked AS mom_id_entity_x_locked,
           srm_regatta."left" AS srm_regatta_left,
           srm_regatta.boat_class AS srm_regatta_boat_class,
           srm_regatta.discards AS srm_regatta_discards,
           srm_regatta.is_cancelled AS srm_regatta_is_cancelled,
           srm_regatta.kind AS srm_regatta_kind,
           srm_regatta.perma_name AS srm_regatta_perma_name,
           srm_regatta.pid AS srm_regatta_pid,
           srm_regatta.races AS srm_regatta_races,
           srm_regatta.result__date AS srm_regatta_result__date,
           srm_regatta.result__software AS srm_regatta_result__software,
           srm_regatta.result__status AS srm_regatta_result__status,
           srm_regatta_c.is_team_race AS srm_regatta_c_is_team_race,
           srm_regatta_c.pid AS srm_regatta_c_pid
         FROM mom_id_entity
           JOIN srm_regatta ON mom_id_entity.pid = srm_regatta.pid
           JOIN srm_regatta_c ON srm_regatta.pid = srm_regatta_c.pid
           JOIN srm_boat_class AS srm_boat_class__1 ON srm_boat_class__1.pid = srm_regatta.boat_class
         WHERE srm_boat_class__1.max_crew <= :max_crew_1

    >>> print (qrt.filter (Q.RAW.races == "3")) ### SRM.Regatta_C
    SQL: SELECT
           mom_id_entity.electric AS mom_id_entity_electric,
           mom_id_entity.last_cid AS mom_id_entity_last_cid,
           mom_id_entity.pid AS mom_id_entity_pid,
           mom_id_entity.type_name AS mom_id_entity_type_name,
           mom_id_entity.x_locked AS mom_id_entity_x_locked,
           srm_regatta."left" AS srm_regatta_left,
           srm_regatta.boat_class AS srm_regatta_boat_class,
           srm_regatta.discards AS srm_regatta_discards,
           srm_regatta.is_cancelled AS srm_regatta_is_cancelled,
           srm_regatta.kind AS srm_regatta_kind,
           srm_regatta.perma_name AS srm_regatta_perma_name,
           srm_regatta.pid AS srm_regatta_pid,
           srm_regatta.races AS srm_regatta_races,
           srm_regatta.result__date AS srm_regatta_result__date,
           srm_regatta.result__software AS srm_regatta_result__software,
           srm_regatta.result__status AS srm_regatta_result__status,
           srm_regatta_c.is_team_race AS srm_regatta_c_is_team_race,
           srm_regatta_c.pid AS srm_regatta_c_pid
         FROM mom_id_entity
           JOIN srm_regatta ON mom_id_entity.pid = srm_regatta.pid
           JOIN srm_regatta_c ON srm_regatta.pid = srm_regatta_c.pid
         WHERE srm_regatta.races = :races_1

    >>> print (qrt.filter (- Q.races)) ### SRM.Regatta_C
    SQL: SELECT
           mom_id_entity.electric AS mom_id_entity_electric,
           mom_id_entity.last_cid AS mom_id_entity_last_cid,
           mom_id_entity.pid AS mom_id_entity_pid,
           mom_id_entity.type_name AS mom_id_entity_type_name,
           mom_id_entity.x_locked AS mom_id_entity_x_locked,
           srm_regatta."left" AS srm_regatta_left,
           srm_regatta.boat_class AS srm_regatta_boat_class,
           srm_regatta.discards AS srm_regatta_discards,
           srm_regatta.is_cancelled AS srm_regatta_is_cancelled,
           srm_regatta.kind AS srm_regatta_kind,
           srm_regatta.perma_name AS srm_regatta_perma_name,
           srm_regatta.pid AS srm_regatta_pid,
           srm_regatta.races AS srm_regatta_races,
           srm_regatta.result__date AS srm_regatta_result__date,
           srm_regatta.result__software AS srm_regatta_result__software,
           srm_regatta.result__status AS srm_regatta_result__status,
           srm_regatta_c.is_team_race AS srm_regatta_c_is_team_race,
           srm_regatta_c.pid AS srm_regatta_c_pid
         FROM mom_id_entity
           JOIN srm_regatta ON mom_id_entity.pid = srm_regatta.pid
           JOIN srm_regatta_c ON srm_regatta.pid = srm_regatta_c.pid
         WHERE -srm_regatta.races

    >>> print (qrt.filter (Q.boat_class == 42)) ### SRM.Regatta_C
    SQL: SELECT
           mom_id_entity.electric AS mom_id_entity_electric,
           mom_id_entity.last_cid AS mom_id_entity_last_cid,
           mom_id_entity.pid AS mom_id_entity_pid,
           mom_id_entity.type_name AS mom_id_entity_type_name,
           mom_id_entity.x_locked AS mom_id_entity_x_locked,
           srm_regatta."left" AS srm_regatta_left,
           srm_regatta.boat_class AS srm_regatta_boat_class,
           srm_regatta.discards AS srm_regatta_discards,
           srm_regatta.is_cancelled AS srm_regatta_is_cancelled,
           srm_regatta.kind AS srm_regatta_kind,
           srm_regatta.perma_name AS srm_regatta_perma_name,
           srm_regatta.pid AS srm_regatta_pid,
           srm_regatta.races AS srm_regatta_races,
           srm_regatta.result__date AS srm_regatta_result__date,
           srm_regatta.result__software AS srm_regatta_result__software,
           srm_regatta.result__status AS srm_regatta_result__status,
           srm_regatta_c.is_team_race AS srm_regatta_c_is_team_race,
           srm_regatta_c.pid AS srm_regatta_c_pid
         FROM mom_id_entity
           JOIN srm_regatta ON mom_id_entity.pid = srm_regatta.pid
           JOIN srm_regatta_c ON srm_regatta.pid = srm_regatta_c.pid
         WHERE srm_regatta.boat_class = :boat_class_1

    >>> print (qrt.filter (Q.boat_class.name)) ### SRM.Regatta_C
    SQL: SELECT
           mom_id_entity.electric AS mom_id_entity_electric,
           mom_id_entity.last_cid AS mom_id_entity_last_cid,
           mom_id_entity.pid AS mom_id_entity_pid,
           mom_id_entity.type_name AS mom_id_entity_type_name,
           mom_id_entity.x_locked AS mom_id_entity_x_locked,
           srm_regatta."left" AS srm_regatta_left,
           srm_regatta.boat_class AS srm_regatta_boat_class,
           srm_regatta.discards AS srm_regatta_discards,
           srm_regatta.is_cancelled AS srm_regatta_is_cancelled,
           srm_regatta.kind AS srm_regatta_kind,
           srm_regatta.perma_name AS srm_regatta_perma_name,
           srm_regatta.pid AS srm_regatta_pid,
           srm_regatta.races AS srm_regatta_races,
           srm_regatta.result__date AS srm_regatta_result__date,
           srm_regatta.result__software AS srm_regatta_result__software,
           srm_regatta.result__status AS srm_regatta_result__status,
           srm_regatta_c.is_team_race AS srm_regatta_c_is_team_race,
           srm_regatta_c.pid AS srm_regatta_c_pid
         FROM mom_id_entity
           JOIN srm_regatta ON mom_id_entity.pid = srm_regatta.pid
           JOIN srm_regatta_c ON srm_regatta.pid = srm_regatta_c.pid
           JOIN srm_boat_class AS srm_boat_class__1 ON srm_boat_class__1.pid = srm_regatta.boat_class
           JOIN srm__boat_class_ AS srm__boat_class___1 ON srm__boat_class___1.pid = srm_regatta.boat_class
         WHERE srm__boat_class___1.name != :name_1

    >>> print (qrt.filter (Q.boat_class.name == "Seascape 18")) ### SRM.Regatta_C
    SQL: SELECT
           mom_id_entity.electric AS mom_id_entity_electric,
           mom_id_entity.last_cid AS mom_id_entity_last_cid,
           mom_id_entity.pid AS mom_id_entity_pid,
           mom_id_entity.type_name AS mom_id_entity_type_name,
           mom_id_entity.x_locked AS mom_id_entity_x_locked,
           srm_regatta."left" AS srm_regatta_left,
           srm_regatta.boat_class AS srm_regatta_boat_class,
           srm_regatta.discards AS srm_regatta_discards,
           srm_regatta.is_cancelled AS srm_regatta_is_cancelled,
           srm_regatta.kind AS srm_regatta_kind,
           srm_regatta.perma_name AS srm_regatta_perma_name,
           srm_regatta.pid AS srm_regatta_pid,
           srm_regatta.races AS srm_regatta_races,
           srm_regatta.result__date AS srm_regatta_result__date,
           srm_regatta.result__software AS srm_regatta_result__software,
           srm_regatta.result__status AS srm_regatta_result__status,
           srm_regatta_c.is_team_race AS srm_regatta_c_is_team_race,
           srm_regatta_c.pid AS srm_regatta_c_pid
         FROM mom_id_entity
           JOIN srm_regatta ON mom_id_entity.pid = srm_regatta.pid
           JOIN srm_regatta_c ON srm_regatta.pid = srm_regatta_c.pid
           JOIN srm_boat_class AS srm_boat_class__1 ON srm_boat_class__1.pid = srm_regatta.boat_class
           JOIN srm__boat_class_ AS srm__boat_class___1 ON srm__boat_class___1.pid = srm_regatta.boat_class
         WHERE srm__boat_class___1.name = :name_1

    >>> print (qrt.filter (Q.boat_class.name == Q.perma_name)) ### SRM.Regatta_C
    SQL: SELECT
           mom_id_entity.electric AS mom_id_entity_electric,
           mom_id_entity.last_cid AS mom_id_entity_last_cid,
           mom_id_entity.pid AS mom_id_entity_pid,
           mom_id_entity.type_name AS mom_id_entity_type_name,
           mom_id_entity.x_locked AS mom_id_entity_x_locked,
           srm_regatta."left" AS srm_regatta_left,
           srm_regatta.boat_class AS srm_regatta_boat_class,
           srm_regatta.discards AS srm_regatta_discards,
           srm_regatta.is_cancelled AS srm_regatta_is_cancelled,
           srm_regatta.kind AS srm_regatta_kind,
           srm_regatta.perma_name AS srm_regatta_perma_name,
           srm_regatta.pid AS srm_regatta_pid,
           srm_regatta.races AS srm_regatta_races,
           srm_regatta.result__date AS srm_regatta_result__date,
           srm_regatta.result__software AS srm_regatta_result__software,
           srm_regatta.result__status AS srm_regatta_result__status,
           srm_regatta_c.is_team_race AS srm_regatta_c_is_team_race,
           srm_regatta_c.pid AS srm_regatta_c_pid
         FROM mom_id_entity
           JOIN srm_regatta ON mom_id_entity.pid = srm_regatta.pid
           JOIN srm_regatta_c ON srm_regatta.pid = srm_regatta_c.pid
           JOIN srm_boat_class AS srm_boat_class__1 ON srm_boat_class__1.pid = srm_regatta.boat_class
           JOIN srm__boat_class_ AS srm__boat_class___1 ON srm__boat_class___1.pid = srm_regatta.boat_class
         WHERE srm__boat_class___1.name = srm_regatta.perma_name

    >>> print (qrt.filter (Q.boat_class.max_crew)) ### SRM.Regatta_C
    SQL: SELECT
           mom_id_entity.electric AS mom_id_entity_electric,
           mom_id_entity.last_cid AS mom_id_entity_last_cid,
           mom_id_entity.pid AS mom_id_entity_pid,
           mom_id_entity.type_name AS mom_id_entity_type_name,
           mom_id_entity.x_locked AS mom_id_entity_x_locked,
           srm_regatta."left" AS srm_regatta_left,
           srm_regatta.boat_class AS srm_regatta_boat_class,
           srm_regatta.discards AS srm_regatta_discards,
           srm_regatta.is_cancelled AS srm_regatta_is_cancelled,
           srm_regatta.kind AS srm_regatta_kind,
           srm_regatta.perma_name AS srm_regatta_perma_name,
           srm_regatta.pid AS srm_regatta_pid,
           srm_regatta.races AS srm_regatta_races,
           srm_regatta.result__date AS srm_regatta_result__date,
           srm_regatta.result__software AS srm_regatta_result__software,
           srm_regatta.result__status AS srm_regatta_result__status,
           srm_regatta_c.is_team_race AS srm_regatta_c_is_team_race,
           srm_regatta_c.pid AS srm_regatta_c_pid
         FROM mom_id_entity
           JOIN srm_regatta ON mom_id_entity.pid = srm_regatta.pid
           JOIN srm_regatta_c ON srm_regatta.pid = srm_regatta_c.pid
           JOIN srm_boat_class AS srm_boat_class__1 ON srm_boat_class__1.pid = srm_regatta.boat_class
         WHERE srm_boat_class__1.max_crew IS NOT NULL
            AND srm_boat_class__1.max_crew != :max_crew_1

    >>> print (qrt.filter (Q.result)) ### SRM.Regatta_C
    Traceback (most recent call last):
      ...
    TypeError: Cannot filter by composite attribute SRM.Regatta_Result.result

    >>> print (qrt.filter (Q.result == ("2013-05-26", ))) ### SRM.Regatta_C
    SQL: SELECT
           mom_id_entity.electric AS mom_id_entity_electric,
           mom_id_entity.last_cid AS mom_id_entity_last_cid,
           mom_id_entity.pid AS mom_id_entity_pid,
           mom_id_entity.type_name AS mom_id_entity_type_name,
           mom_id_entity.x_locked AS mom_id_entity_x_locked,
           srm_regatta."left" AS srm_regatta_left,
           srm_regatta.boat_class AS srm_regatta_boat_class,
           srm_regatta.discards AS srm_regatta_discards,
           srm_regatta.is_cancelled AS srm_regatta_is_cancelled,
           srm_regatta.kind AS srm_regatta_kind,
           srm_regatta.perma_name AS srm_regatta_perma_name,
           srm_regatta.pid AS srm_regatta_pid,
           srm_regatta.races AS srm_regatta_races,
           srm_regatta.result__date AS srm_regatta_result__date,
           srm_regatta.result__software AS srm_regatta_result__software,
           srm_regatta.result__status AS srm_regatta_result__status,
           srm_regatta_c.is_team_race AS srm_regatta_c_is_team_race,
           srm_regatta_c.pid AS srm_regatta_c_pid
         FROM mom_id_entity
           JOIN srm_regatta ON mom_id_entity.pid = srm_regatta.pid
           JOIN srm_regatta_c ON srm_regatta.pid = srm_regatta_c.pid
         WHERE srm_regatta.result__date = :result__date_1

    >>> print (qrt.filter (Q.result.date)) ### SRM.Regatta_C
    SQL: SELECT
           mom_id_entity.electric AS mom_id_entity_electric,
           mom_id_entity.last_cid AS mom_id_entity_last_cid,
           mom_id_entity.pid AS mom_id_entity_pid,
           mom_id_entity.type_name AS mom_id_entity_type_name,
           mom_id_entity.x_locked AS mom_id_entity_x_locked,
           srm_regatta."left" AS srm_regatta_left,
           srm_regatta.boat_class AS srm_regatta_boat_class,
           srm_regatta.discards AS srm_regatta_discards,
           srm_regatta.is_cancelled AS srm_regatta_is_cancelled,
           srm_regatta.kind AS srm_regatta_kind,
           srm_regatta.perma_name AS srm_regatta_perma_name,
           srm_regatta.pid AS srm_regatta_pid,
           srm_regatta.races AS srm_regatta_races,
           srm_regatta.result__date AS srm_regatta_result__date,
           srm_regatta.result__software AS srm_regatta_result__software,
           srm_regatta.result__status AS srm_regatta_result__status,
           srm_regatta_c.is_team_race AS srm_regatta_c_is_team_race,
           srm_regatta_c.pid AS srm_regatta_c_pid
         FROM mom_id_entity
           JOIN srm_regatta ON mom_id_entity.pid = srm_regatta.pid
           JOIN srm_regatta_c ON srm_regatta.pid = srm_regatta_c.pid
         WHERE srm_regatta.result__date IS NOT NULL

    >>> print (qrt.filter (Q.left)) ### SRM.Regatta_C
    SQL: SELECT
           mom_id_entity.electric AS mom_id_entity_electric,
           mom_id_entity.last_cid AS mom_id_entity_last_cid,
           mom_id_entity.pid AS mom_id_entity_pid,
           mom_id_entity.type_name AS mom_id_entity_type_name,
           mom_id_entity.x_locked AS mom_id_entity_x_locked,
           srm_regatta."left" AS srm_regatta_left,
           srm_regatta.boat_class AS srm_regatta_boat_class,
           srm_regatta.discards AS srm_regatta_discards,
           srm_regatta.is_cancelled AS srm_regatta_is_cancelled,
           srm_regatta.kind AS srm_regatta_kind,
           srm_regatta.perma_name AS srm_regatta_perma_name,
           srm_regatta.pid AS srm_regatta_pid,
           srm_regatta.races AS srm_regatta_races,
           srm_regatta.result__date AS srm_regatta_result__date,
           srm_regatta.result__software AS srm_regatta_result__software,
           srm_regatta.result__status AS srm_regatta_result__status,
           srm_regatta_c.is_team_race AS srm_regatta_c_is_team_race,
           srm_regatta_c.pid AS srm_regatta_c_pid
         FROM mom_id_entity
           JOIN srm_regatta ON mom_id_entity.pid = srm_regatta.pid
           JOIN srm_regatta_c ON srm_regatta.pid = srm_regatta_c.pid
         WHERE srm_regatta."left" IS NOT NULL

    >>> print (qrt.filter (Q.left.date.start)) ### SRM.Regatta_C
    SQL: SELECT
           mom_id_entity.electric AS mom_id_entity_electric,
           mom_id_entity.last_cid AS mom_id_entity_last_cid,
           mom_id_entity.pid AS mom_id_entity_pid,
           mom_id_entity.type_name AS mom_id_entity_type_name,
           mom_id_entity.x_locked AS mom_id_entity_x_locked,
           srm_regatta."left" AS srm_regatta_left,
           srm_regatta.boat_class AS srm_regatta_boat_class,
           srm_regatta.discards AS srm_regatta_discards,
           srm_regatta.is_cancelled AS srm_regatta_is_cancelled,
           srm_regatta.kind AS srm_regatta_kind,
           srm_regatta.perma_name AS srm_regatta_perma_name,
           srm_regatta.pid AS srm_regatta_pid,
           srm_regatta.races AS srm_regatta_races,
           srm_regatta.result__date AS srm_regatta_result__date,
           srm_regatta.result__software AS srm_regatta_result__software,
           srm_regatta.result__status AS srm_regatta_result__status,
           srm_regatta_c.is_team_race AS srm_regatta_c_is_team_race,
           srm_regatta_c.pid AS srm_regatta_c_pid
         FROM mom_id_entity
           JOIN srm_regatta ON mom_id_entity.pid = srm_regatta.pid
           JOIN srm_regatta_c ON srm_regatta.pid = srm_regatta_c.pid
           JOIN srm_regatta_event AS srm_regatta_event__1 ON srm_regatta_event__1.pid = srm_regatta."left"
         WHERE srm_regatta_event__1.date__start IS NOT NULL

    >>> print (qrt.filter (Q.left.date.start == "2013-07-21")) ### SRM.Regatta_C
    SQL: SELECT
           mom_id_entity.electric AS mom_id_entity_electric,
           mom_id_entity.last_cid AS mom_id_entity_last_cid,
           mom_id_entity.pid AS mom_id_entity_pid,
           mom_id_entity.type_name AS mom_id_entity_type_name,
           mom_id_entity.x_locked AS mom_id_entity_x_locked,
           srm_regatta."left" AS srm_regatta_left,
           srm_regatta.boat_class AS srm_regatta_boat_class,
           srm_regatta.discards AS srm_regatta_discards,
           srm_regatta.is_cancelled AS srm_regatta_is_cancelled,
           srm_regatta.kind AS srm_regatta_kind,
           srm_regatta.perma_name AS srm_regatta_perma_name,
           srm_regatta.pid AS srm_regatta_pid,
           srm_regatta.races AS srm_regatta_races,
           srm_regatta.result__date AS srm_regatta_result__date,
           srm_regatta.result__software AS srm_regatta_result__software,
           srm_regatta.result__status AS srm_regatta_result__status,
           srm_regatta_c.is_team_race AS srm_regatta_c_is_team_race,
           srm_regatta_c.pid AS srm_regatta_c_pid
         FROM mom_id_entity
           JOIN srm_regatta ON mom_id_entity.pid = srm_regatta.pid
           JOIN srm_regatta_c ON srm_regatta.pid = srm_regatta_c.pid
           JOIN srm_regatta_event AS srm_regatta_event__1 ON srm_regatta_event__1.pid = srm_regatta."left"
         WHERE srm_regatta_event__1.date__start = :date__start_1

    >>> print (qrt.filter (Q.left.date.alive)) ### SRM.Regatta_C
    SQL: SELECT
           mom_id_entity.electric AS mom_id_entity_electric,
           mom_id_entity.last_cid AS mom_id_entity_last_cid,
           mom_id_entity.pid AS mom_id_entity_pid,
           mom_id_entity.type_name AS mom_id_entity_type_name,
           mom_id_entity.x_locked AS mom_id_entity_x_locked,
           srm_regatta."left" AS srm_regatta_left,
           srm_regatta.boat_class AS srm_regatta_boat_class,
           srm_regatta.discards AS srm_regatta_discards,
           srm_regatta.is_cancelled AS srm_regatta_is_cancelled,
           srm_regatta.kind AS srm_regatta_kind,
           srm_regatta.perma_name AS srm_regatta_perma_name,
           srm_regatta.pid AS srm_regatta_pid,
           srm_regatta.races AS srm_regatta_races,
           srm_regatta.result__date AS srm_regatta_result__date,
           srm_regatta.result__software AS srm_regatta_result__software,
           srm_regatta.result__status AS srm_regatta_result__status,
           srm_regatta_c.is_team_race AS srm_regatta_c_is_team_race,
           srm_regatta_c.pid AS srm_regatta_c_pid
         FROM mom_id_entity
           JOIN srm_regatta ON mom_id_entity.pid = srm_regatta.pid
           JOIN srm_regatta_c ON srm_regatta.pid = srm_regatta_c.pid
           JOIN srm_regatta_event AS srm_regatta_event__1 ON srm_regatta_event__1.pid = srm_regatta."left"
         WHERE (srm_regatta_event__1.date__start IS NULL
            OR srm_regatta_event__1.date__start <= :date__start_1)
            AND (srm_regatta_event__1.date__finish IS NULL
            OR srm_regatta_event__1.date__finish >= :date__finish_1)

    >>> ET = apt ["SRM.Boat_in_Regatta"]
    >>> qrt = apt.DBW.PNS.Q_Result.E_Type (ET, _strict = False)

    >>> print (qrt.filter (Q.regatta.event.date.start > "2009/05/21")) ### SRM.Boat_in_Regatta
    SQL: SELECT
           mom_id_entity.electric AS mom_id_entity_electric,
           mom_id_entity.last_cid AS mom_id_entity_last_cid,
           mom_id_entity.pid AS mom_id_entity_pid,
           mom_id_entity.type_name AS mom_id_entity_type_name,
           mom_id_entity.x_locked AS mom_id_entity_x_locked,
           srm_boat_in_regatta."left" AS srm_boat_in_regatta_left,
           srm_boat_in_regatta."right" AS srm_boat_in_regatta_right,
           srm_boat_in_regatta.pid AS srm_boat_in_regatta_pid,
           srm_boat_in_regatta.place AS srm_boat_in_regatta_place,
           srm_boat_in_regatta.points AS srm_boat_in_regatta_points,
           srm_boat_in_regatta.rank AS srm_boat_in_regatta_rank,
           srm_boat_in_regatta.registration_date AS srm_boat_in_regatta_registration_date,
           srm_boat_in_regatta.skipper AS srm_boat_in_regatta_skipper
         FROM mom_id_entity
           JOIN srm_boat_in_regatta ON mom_id_entity.pid = srm_boat_in_regatta.pid
           JOIN srm_regatta AS srm_regatta__1 ON srm_regatta__1.pid = srm_boat_in_regatta."right"
           JOIN srm_regatta_event AS srm_regatta_event__2 ON srm_regatta_event__2.pid = srm_regatta__1."left"
         WHERE srm_regatta_event__2.date__start > :date__start_1

    >>> print (qrt.filter (Q.right.left.date.start > "2009/05/21")) ### SRM.Boat_in_Regatta
    SQL: SELECT
           mom_id_entity.electric AS mom_id_entity_electric,
           mom_id_entity.last_cid AS mom_id_entity_last_cid,
           mom_id_entity.pid AS mom_id_entity_pid,
           mom_id_entity.type_name AS mom_id_entity_type_name,
           mom_id_entity.x_locked AS mom_id_entity_x_locked,
           srm_boat_in_regatta."left" AS srm_boat_in_regatta_left,
           srm_boat_in_regatta."right" AS srm_boat_in_regatta_right,
           srm_boat_in_regatta.pid AS srm_boat_in_regatta_pid,
           srm_boat_in_regatta.place AS srm_boat_in_regatta_place,
           srm_boat_in_regatta.points AS srm_boat_in_regatta_points,
           srm_boat_in_regatta.rank AS srm_boat_in_regatta_rank,
           srm_boat_in_regatta.registration_date AS srm_boat_in_regatta_registration_date,
           srm_boat_in_regatta.skipper AS srm_boat_in_regatta_skipper
         FROM mom_id_entity
           JOIN srm_boat_in_regatta ON mom_id_entity.pid = srm_boat_in_regatta.pid
           JOIN srm_regatta AS srm_regatta__1 ON srm_regatta__1.pid = srm_boat_in_regatta."right"
           JOIN srm_regatta_event AS srm_regatta_event__2 ON srm_regatta_event__2.pid = srm_regatta__1."left"
         WHERE srm_regatta_event__2.date__start > :date__start_1

    >>> ET  = apt ["PAP.Person_has_Phone"]
    >>> qrt = apt.DBW.PNS.Q_Result.E_Type (ET, _strict = False)

    >>> print (apt.DBW.PNS.Q_Result.E_Type_Reload (ET)) ### PAP.Person_has_Phone
    SQL: SELECT
           mom_id_entity.electric AS mom_id_entity_electric,
           mom_id_entity.last_cid AS mom_id_entity_last_cid,
           mom_id_entity.pid AS mom_id_entity_pid,
           mom_id_entity.type_name AS mom_id_entity_type_name,
           mom_id_entity.x_locked AS mom_id_entity_x_locked,
           pap_person_has_phone.pid AS pap_person_has_phone_pid,
           pap_subject_has_phone.extension AS pap_subject_has_phone_extension,
           pap_subject_has_phone.pid AS pap_subject_has_phone_pid,
           pap_subject_has_property."desc" AS pap_subject_has_property_desc,
           pap_subject_has_property."left" AS pap_subject_has_property_left,
           pap_subject_has_property."right" AS pap_subject_has_property_right,
           pap_subject_has_property.pid AS pap_subject_has_property_pid
         FROM mom_id_entity
           JOIN pap_subject_has_property ON mom_id_entity.pid = pap_subject_has_property.pid
           JOIN pap_subject_has_phone ON pap_subject_has_property.pid = pap_subject_has_phone.pid
           JOIN pap_person_has_phone ON pap_subject_has_phone.pid = pap_person_has_phone.pid
         WHERE mom_id_entity.pid = :spk
         LIMIT :param_1

    >>> print (qrt.attr (Q.desc, allow_duplicates = True)) ### PAP.Person_has_Phone
    SQL: SELECT pap_subject_has_property."desc" AS pap_subject_has_property_desc
         FROM mom_id_entity
           JOIN pap_subject_has_property ON mom_id_entity.pid = pap_subject_has_property.pid
           JOIN pap_subject_has_phone ON pap_subject_has_property.pid = pap_subject_has_phone.pid
           JOIN pap_person_has_phone ON pap_subject_has_phone.pid = pap_person_has_phone.pid

    >>> print (qrt.attr (Q.person.lifetime.start)) ### PAP.Person_has_Phone
    SQL: SELECT DISTINCT pap_person__1.lifetime__start AS pap_person__1_lifetime__start
         FROM mom_id_entity
           JOIN pap_subject_has_property ON mom_id_entity.pid = pap_subject_has_property.pid
           JOIN pap_subject_has_phone ON pap_subject_has_property.pid = pap_subject_has_phone.pid
           JOIN pap_person_has_phone ON pap_subject_has_phone.pid = pap_person_has_phone.pid
           JOIN pap_person AS pap_person__1 ON pap_person__1.pid = pap_subject_has_property."left"

    >>> print (qrt.attrs (Q.phone.number, Q.desc, Q.person.lifetime.start)) ### PAP.Person_has_Phone
    SQL: SELECT DISTINCT
           pap_person__1.lifetime__start AS pap_person__1_lifetime__start,
           pap_phone__1.number AS pap_phone__1_number,
           pap_subject_has_property."desc" AS pap_subject_has_property_desc
         FROM mom_id_entity
           JOIN pap_subject_has_property ON mom_id_entity.pid = pap_subject_has_property.pid
           JOIN pap_subject_has_phone ON pap_subject_has_property.pid = pap_subject_has_phone.pid
           JOIN pap_person_has_phone ON pap_subject_has_phone.pid = pap_person_has_phone.pid
           JOIN pap_phone AS pap_phone__1 ON pap_phone__1.pid = pap_subject_has_property."right"
           JOIN pap_person AS pap_person__1 ON pap_person__1.pid = pap_subject_has_property."left"

    >>> print (qrt.filter (Q.person.lifetime == ("2013/07/15", ))) ### PAP.Person_has_Phone
    SQL: SELECT
           mom_id_entity.electric AS mom_id_entity_electric,
           mom_id_entity.last_cid AS mom_id_entity_last_cid,
           mom_id_entity.pid AS mom_id_entity_pid,
           mom_id_entity.type_name AS mom_id_entity_type_name,
           mom_id_entity.x_locked AS mom_id_entity_x_locked,
           pap_person_has_phone.pid AS pap_person_has_phone_pid,
           pap_subject_has_phone.extension AS pap_subject_has_phone_extension,
           pap_subject_has_phone.pid AS pap_subject_has_phone_pid,
           pap_subject_has_property."desc" AS pap_subject_has_property_desc,
           pap_subject_has_property."left" AS pap_subject_has_property_left,
           pap_subject_has_property."right" AS pap_subject_has_property_right,
           pap_subject_has_property.pid AS pap_subject_has_property_pid
         FROM mom_id_entity
           JOIN pap_subject_has_property ON mom_id_entity.pid = pap_subject_has_property.pid
           JOIN pap_subject_has_phone ON pap_subject_has_property.pid = pap_subject_has_phone.pid
           JOIN pap_person_has_phone ON pap_subject_has_phone.pid = pap_person_has_phone.pid
           JOIN pap_person AS pap_person__1 ON pap_person__1.pid = pap_subject_has_property."left"
         WHERE pap_person__1.lifetime__start = :lifetime__start_1

    >>> print (qrt.order_by (Q.person.lifetime)) ### PAP.Person_has_Phone
    SQL: SELECT
           mom_id_entity.electric AS mom_id_entity_electric,
           mom_id_entity.last_cid AS mom_id_entity_last_cid,
           mom_id_entity.pid AS mom_id_entity_pid,
           mom_id_entity.type_name AS mom_id_entity_type_name,
           mom_id_entity.x_locked AS mom_id_entity_x_locked,
           pap_person_has_phone.pid AS pap_person_has_phone_pid,
           pap_subject_has_phone.extension AS pap_subject_has_phone_extension,
           pap_subject_has_phone.pid AS pap_subject_has_phone_pid,
           pap_subject_has_property."desc" AS pap_subject_has_property_desc,
           pap_subject_has_property."left" AS pap_subject_has_property_left,
           pap_subject_has_property."right" AS pap_subject_has_property_right,
           pap_subject_has_property.pid AS pap_subject_has_property_pid
         FROM mom_id_entity
           JOIN pap_subject_has_property ON mom_id_entity.pid = pap_subject_has_property.pid
           JOIN pap_subject_has_phone ON pap_subject_has_property.pid = pap_subject_has_phone.pid
           JOIN pap_person_has_phone ON pap_subject_has_phone.pid = pap_person_has_phone.pid
           JOIN pap_person AS pap_person__1 ON pap_person__1.pid = pap_subject_has_property."left"
         ORDER BY pap_person__1.lifetime__start, pap_person__1.lifetime__finish

    >>> ET = apt ["PAP.Subject_has_Email"]
    >>> qrt = apt.DBW.PNS.Q_Result.E_Type (ET, _strict = False)

    >>> print (qrt) ### PAP.Subject_has_Email
    SQL: SELECT
           mom_id_entity.electric AS mom_id_entity_electric,
           mom_id_entity.last_cid AS mom_id_entity_last_cid,
           mom_id_entity.pid AS mom_id_entity_pid,
           mom_id_entity.type_name AS mom_id_entity_type_name,
           mom_id_entity.x_locked AS mom_id_entity_x_locked,
           pap_company_has_email.pid AS pap_company_has_email_pid,
           pap_person_has_email.pid AS pap_person_has_email_pid,
           pap_subject_has_property."desc" AS pap_subject_has_property_desc,
           pap_subject_has_property."left" AS pap_subject_has_property_left,
           pap_subject_has_property."right" AS pap_subject_has_property_right,
           pap_subject_has_property.pid AS pap_subject_has_property_pid
         FROM mom_id_entity
           JOIN pap_subject_has_property ON mom_id_entity.pid = pap_subject_has_property.pid
           LEFT OUTER JOIN pap_company_has_email ON pap_subject_has_property.pid = pap_company_has_email.pid
           LEFT OUTER JOIN pap_person_has_email ON pap_subject_has_property.pid = pap_person_has_email.pid
         WHERE mom_id_entity.pid = pap_company_has_email.pid
            OR mom_id_entity.pid = pap_person_has_email.pid

    >>> print (qrt.filter (Q.left.lifetime.start > "2000/01/01")) ### PAP.Subject_has_Email
    SQL: SELECT
           mom_id_entity.electric AS mom_id_entity_electric,
           mom_id_entity.last_cid AS mom_id_entity_last_cid,
           mom_id_entity.pid AS mom_id_entity_pid,
           mom_id_entity.type_name AS mom_id_entity_type_name,
           mom_id_entity.x_locked AS mom_id_entity_x_locked,
           pap_company_has_email.pid AS pap_company_has_email_pid,
           pap_person_has_email.pid AS pap_person_has_email_pid,
           pap_subject_has_property."desc" AS pap_subject_has_property_desc,
           pap_subject_has_property."left" AS pap_subject_has_property_left,
           pap_subject_has_property."right" AS pap_subject_has_property_right,
           pap_subject_has_property.pid AS pap_subject_has_property_pid
         FROM mom_id_entity
           JOIN pap_subject_has_property ON mom_id_entity.pid = pap_subject_has_property.pid
           LEFT OUTER JOIN pap_company_has_email ON pap_subject_has_property.pid = pap_company_has_email.pid
           LEFT OUTER JOIN pap_person_has_email ON pap_subject_has_property.pid = pap_person_has_email.pid
           LEFT OUTER JOIN mom_id_entity AS mom_id_entity__8 ON mom_id_entity__8.pid = pap_subject_has_property."left"
           LEFT OUTER JOIN pap_company AS pap_company__1 ON pap_company__1.pid = pap_subject_has_property."left"
           LEFT OUTER JOIN pap_person AS pap_person__2 ON pap_person__2.pid = pap_subject_has_property."left"
         WHERE (mom_id_entity.pid = pap_company_has_email.pid
            OR mom_id_entity.pid = pap_person_has_email.pid)
            AND (pap_company__1.lifetime__start > :lifetime__start_1
            OR pap_person__2.lifetime__start > :lifetime__start_2)

    >>> print (qrt.filter (Q.right.address == "lucky@mangari.org")) ### PAP.Subject_has_Email
    SQL: SELECT
           mom_id_entity.electric AS mom_id_entity_electric,
           mom_id_entity.last_cid AS mom_id_entity_last_cid,
           mom_id_entity.pid AS mom_id_entity_pid,
           mom_id_entity.type_name AS mom_id_entity_type_name,
           mom_id_entity.x_locked AS mom_id_entity_x_locked,
           pap_company_has_email.pid AS pap_company_has_email_pid,
           pap_person_has_email.pid AS pap_person_has_email_pid,
           pap_subject_has_property."desc" AS pap_subject_has_property_desc,
           pap_subject_has_property."left" AS pap_subject_has_property_left,
           pap_subject_has_property."right" AS pap_subject_has_property_right,
           pap_subject_has_property.pid AS pap_subject_has_property_pid
         FROM mom_id_entity
           JOIN pap_subject_has_property ON mom_id_entity.pid = pap_subject_has_property.pid
           LEFT OUTER JOIN pap_company_has_email ON pap_subject_has_property.pid = pap_company_has_email.pid
           LEFT OUTER JOIN pap_person_has_email ON pap_subject_has_property.pid = pap_person_has_email.pid
           LEFT OUTER JOIN pap_email AS pap_email__1 ON pap_email__1.pid = pap_subject_has_property."right"
         WHERE (mom_id_entity.pid = pap_company_has_email.pid
            OR mom_id_entity.pid = pap_person_has_email.pid)
            AND pap_email__1.address = :address_1

    >>> print (qrt.filter (Q.right.address.ENDSWITH ("@mangari.org"))) ### PAP.Subject_has_Email
    SQL: SELECT
           mom_id_entity.electric AS mom_id_entity_electric,
           mom_id_entity.last_cid AS mom_id_entity_last_cid,
           mom_id_entity.pid AS mom_id_entity_pid,
           mom_id_entity.type_name AS mom_id_entity_type_name,
           mom_id_entity.x_locked AS mom_id_entity_x_locked,
           pap_company_has_email.pid AS pap_company_has_email_pid,
           pap_person_has_email.pid AS pap_person_has_email_pid,
           pap_subject_has_property."desc" AS pap_subject_has_property_desc,
           pap_subject_has_property."left" AS pap_subject_has_property_left,
           pap_subject_has_property."right" AS pap_subject_has_property_right,
           pap_subject_has_property.pid AS pap_subject_has_property_pid
         FROM mom_id_entity
           JOIN pap_subject_has_property ON mom_id_entity.pid = pap_subject_has_property.pid
           LEFT OUTER JOIN pap_company_has_email ON pap_subject_has_property.pid = pap_company_has_email.pid
           LEFT OUTER JOIN pap_person_has_email ON pap_subject_has_property.pid = pap_person_has_email.pid
           LEFT OUTER JOIN pap_email AS pap_email__1 ON pap_email__1.pid = pap_subject_has_property."right"
         WHERE (mom_id_entity.pid = pap_company_has_email.pid
            OR mom_id_entity.pid = pap_person_has_email.pid)
            AND (pap_email__1.address LIKE '%%%%' || :address_1)

    >>> ET = apt ["PAP.Person_has_Email"]
    >>> qrt = apt.DBW.PNS.Q_Result.E_Type (ET, _strict = False)

    >>> print (qrt.filter (Q.right.address.ENDSWITH ("@mangari.org"))) ### PAP.Person_has_Email
    SQL: SELECT
           mom_id_entity.electric AS mom_id_entity_electric,
           mom_id_entity.last_cid AS mom_id_entity_last_cid,
           mom_id_entity.pid AS mom_id_entity_pid,
           mom_id_entity.type_name AS mom_id_entity_type_name,
           mom_id_entity.x_locked AS mom_id_entity_x_locked,
           pap_person_has_email.pid AS pap_person_has_email_pid,
           pap_subject_has_property."desc" AS pap_subject_has_property_desc,
           pap_subject_has_property."left" AS pap_subject_has_property_left,
           pap_subject_has_property."right" AS pap_subject_has_property_right,
           pap_subject_has_property.pid AS pap_subject_has_property_pid
         FROM mom_id_entity
           JOIN pap_subject_has_property ON mom_id_entity.pid = pap_subject_has_property.pid
           JOIN pap_person_has_email ON pap_subject_has_property.pid = pap_person_has_email.pid
           JOIN pap_email AS pap_email__2 ON pap_email__2.pid = pap_subject_has_property."right"
         WHERE pap_email__2.address LIKE '%%%%' || :address_1

    >>> ET = apt ["PAP.Subject_has_Phone"]
    >>> qrt = apt.DBW.PNS.Q_Result.E_Type (ET, _strict = False)

    >>> print (qrt.filter (Q.subject.electric)) ### PAP.Subject_has_Phone
    SQL: SELECT
           mom_id_entity.electric AS mom_id_entity_electric,
           mom_id_entity.last_cid AS mom_id_entity_last_cid,
           mom_id_entity.pid AS mom_id_entity_pid,
           mom_id_entity.type_name AS mom_id_entity_type_name,
           mom_id_entity.x_locked AS mom_id_entity_x_locked,
           pap_subject_has_phone.extension AS pap_subject_has_phone_extension,
           pap_subject_has_phone.pid AS pap_subject_has_phone_pid,
           pap_subject_has_property."desc" AS pap_subject_has_property_desc,
           pap_subject_has_property."left" AS pap_subject_has_property_left,
           pap_subject_has_property."right" AS pap_subject_has_property_right,
           pap_subject_has_property.pid AS pap_subject_has_property_pid
         FROM mom_id_entity
           JOIN pap_subject_has_property ON mom_id_entity.pid = pap_subject_has_property.pid
           JOIN pap_subject_has_phone ON pap_subject_has_property.pid = pap_subject_has_phone.pid
           LEFT OUTER JOIN mom_id_entity AS mom_id_entity__13 ON mom_id_entity__13.pid = pap_subject_has_property."left"
         WHERE mom_id_entity__13.electric = true

    >>> print (qrt.filter (Q.phone.electric != Q.subject.electric)) ### PAP.Subject_has_Phone
    SQL: SELECT
           mom_id_entity.electric AS mom_id_entity_electric,
           mom_id_entity.last_cid AS mom_id_entity_last_cid,
           mom_id_entity.pid AS mom_id_entity_pid,
           mom_id_entity.type_name AS mom_id_entity_type_name,
           mom_id_entity.x_locked AS mom_id_entity_x_locked,
           pap_subject_has_phone.extension AS pap_subject_has_phone_extension,
           pap_subject_has_phone.pid AS pap_subject_has_phone_pid,
           pap_subject_has_property."desc" AS pap_subject_has_property_desc,
           pap_subject_has_property."left" AS pap_subject_has_property_left,
           pap_subject_has_property."right" AS pap_subject_has_property_right,
           pap_subject_has_property.pid AS pap_subject_has_property_pid
         FROM mom_id_entity
           JOIN pap_subject_has_property ON mom_id_entity.pid = pap_subject_has_property.pid
           JOIN pap_subject_has_phone ON pap_subject_has_property.pid = pap_subject_has_phone.pid
           LEFT OUTER JOIN pap_phone AS pap_phone__2 ON pap_phone__2.pid = pap_subject_has_property."right"
           LEFT OUTER JOIN mom_id_entity AS mom_id_entity__14 ON mom_id_entity__14.pid = pap_subject_has_property."right"
           LEFT OUTER JOIN mom_id_entity AS mom_id_entity__13 ON mom_id_entity__13.pid = pap_subject_has_property."left"
         WHERE mom_id_entity__14.electric != mom_id_entity__13.electric

    >>> print (qrt.filter (~ Q.electric)) ### PAP.Subject_has_Phone
    SQL: SELECT
           mom_id_entity.electric AS mom_id_entity_electric,
           mom_id_entity.last_cid AS mom_id_entity_last_cid,
           mom_id_entity.pid AS mom_id_entity_pid,
           mom_id_entity.type_name AS mom_id_entity_type_name,
           mom_id_entity.x_locked AS mom_id_entity_x_locked,
           pap_subject_has_phone.extension AS pap_subject_has_phone_extension,
           pap_subject_has_phone.pid AS pap_subject_has_phone_pid,
           pap_subject_has_property."desc" AS pap_subject_has_property_desc,
           pap_subject_has_property."left" AS pap_subject_has_property_left,
           pap_subject_has_property."right" AS pap_subject_has_property_right,
           pap_subject_has_property.pid AS pap_subject_has_property_pid
         FROM mom_id_entity
           JOIN pap_subject_has_property ON mom_id_entity.pid = pap_subject_has_property.pid
           JOIN pap_subject_has_phone ON pap_subject_has_property.pid = pap_subject_has_phone.pid
         WHERE NOT mom_id_entity.electric

    >>> print (qrt.filter (Q.x_locked)) ### PAP.Subject_has_Phone
    SQL: SELECT
           mom_id_entity.electric AS mom_id_entity_electric,
           mom_id_entity.last_cid AS mom_id_entity_last_cid,
           mom_id_entity.pid AS mom_id_entity_pid,
           mom_id_entity.type_name AS mom_id_entity_type_name,
           mom_id_entity.x_locked AS mom_id_entity_x_locked,
           pap_subject_has_phone.extension AS pap_subject_has_phone_extension,
           pap_subject_has_phone.pid AS pap_subject_has_phone_pid,
           pap_subject_has_property."desc" AS pap_subject_has_property_desc,
           pap_subject_has_property."left" AS pap_subject_has_property_left,
           pap_subject_has_property."right" AS pap_subject_has_property_right,
           pap_subject_has_property.pid AS pap_subject_has_property_pid
         FROM mom_id_entity
           JOIN pap_subject_has_property ON mom_id_entity.pid = pap_subject_has_property.pid
           JOIN pap_subject_has_phone ON pap_subject_has_property.pid = pap_subject_has_phone.pid
         WHERE mom_id_entity.x_locked = true

    >>> print (qrt.filter (Q.left)) ### PAP.Subject_has_Phone
    SQL: SELECT
           mom_id_entity.electric AS mom_id_entity_electric,
           mom_id_entity.last_cid AS mom_id_entity_last_cid,
           mom_id_entity.pid AS mom_id_entity_pid,
           mom_id_entity.type_name AS mom_id_entity_type_name,
           mom_id_entity.x_locked AS mom_id_entity_x_locked,
           pap_subject_has_phone.extension AS pap_subject_has_phone_extension,
           pap_subject_has_phone.pid AS pap_subject_has_phone_pid,
           pap_subject_has_property."desc" AS pap_subject_has_property_desc,
           pap_subject_has_property."left" AS pap_subject_has_property_left,
           pap_subject_has_property."right" AS pap_subject_has_property_right,
           pap_subject_has_property.pid AS pap_subject_has_property_pid
         FROM mom_id_entity
           JOIN pap_subject_has_property ON mom_id_entity.pid = pap_subject_has_property.pid
           JOIN pap_subject_has_phone ON pap_subject_has_property.pid = pap_subject_has_phone.pid
         WHERE pap_subject_has_property."left" IS NOT NULL

    >>> ET = apt ["Auth.Account"]
    >>> qrt = apt.DBW.PNS.Q_Result.E_Type (ET, _strict = False)

    >>> print (qrt.attrs (Q.enabled, Q.person, Q.person.lifetime)) ### Auth.Account
    SQL: SELECT DISTINCT
           auth__account_.enabled AS auth__account__enabled,
           pap_person__3.lifetime__finish AS pap_person__3_lifetime__finish,
           pap_person__3.lifetime__start AS pap_person__3_lifetime__start,
           pap_person_has_account__1."left" AS pap_person_has_account__1_left
         FROM mom_id_entity
           JOIN auth__account_ ON mom_id_entity.pid = auth__account_.pid
           JOIN auth_account ON auth__account_.pid = auth_account.pid
           JOIN pap_person_has_account AS pap_person_has_account__1 ON pap_person_has_account__1."right" = auth_account.pid
           JOIN pap_person AS pap_person__3 ON pap_person__3.pid = pap_person_has_account__1."left"

    >>> print (apt.DBW.PNS.Q_Result.E_Type_Reload (ET)) ### Auth.Account
    SQL: SELECT
           auth__account_.enabled AS auth__account__enabled,
           auth__account_.name AS auth__account__name,
           auth__account_.pid AS auth__account__pid,
           auth__account_.superuser AS auth__account__superuser,
           auth__account_.suspended AS auth__account__suspended,
           auth_account.password AS auth_account_password,
           auth_account.ph_name AS auth_account_ph_name,
           auth_account.pid AS auth_account_pid,
           mom_id_entity.electric AS mom_id_entity_electric,
           mom_id_entity.last_cid AS mom_id_entity_last_cid,
           mom_id_entity.pid AS mom_id_entity_pid,
           mom_id_entity.type_name AS mom_id_entity_type_name,
           mom_id_entity.x_locked AS mom_id_entity_x_locked
         FROM mom_id_entity
           JOIN auth__account_ ON mom_id_entity.pid = auth__account_.pid
           JOIN auth_account ON auth__account_.pid = auth_account.pid
         WHERE mom_id_entity.pid = :spk
         LIMIT :param_1

    >>> print (qrt.filter (Q.person)) ### Auth.Account # doctest:+ELLIPSIS
    SQL: SELECT
           auth__account_.enabled AS auth__account__enabled,
           auth__account_.name AS auth__account__name,
           auth__account_.pid AS auth__account__pid,
           auth__account_.superuser AS auth__account__superuser,
           auth__account_.suspended AS auth__account__suspended,
           auth_account.password AS auth_account_password,
           auth_account.ph_name AS auth_account_ph_name,
           auth_account.pid AS auth_account_pid,
           mom_id_entity.electric AS mom_id_entity_electric,
           mom_id_entity.last_cid AS mom_id_entity_last_cid,
           mom_id_entity.pid AS mom_id_entity_pid,
           mom_id_entity.type_name AS mom_id_entity_type_name,
           mom_id_entity.x_locked AS mom_id_entity_x_locked
         FROM mom_id_entity
           JOIN auth__account_ ON mom_id_entity.pid = auth__account_.pid
           JOIN auth_account ON auth__account_.pid = auth_account.pid
           JOIN pap_person_has_account AS pap_person_has_account__1 ON pap_person_has_account__1."right" = auth_account.pid
           JOIN pap_person AS pap_person__3 ON pap_person__3.pid = pap_person_has_account__1."left"
         WHERE pap_person_has_account__1."left" IS NOT NULL

    >>> print (qrt.filter (Q.person.lifetime == ("2013/07/15", ))) ### Auth.Account
    SQL: SELECT
           auth__account_.enabled AS auth__account__enabled,
           auth__account_.name AS auth__account__name,
           auth__account_.pid AS auth__account__pid,
           auth__account_.superuser AS auth__account__superuser,
           auth__account_.suspended AS auth__account__suspended,
           auth_account.password AS auth_account_password,
           auth_account.ph_name AS auth_account_ph_name,
           auth_account.pid AS auth_account_pid,
           mom_id_entity.electric AS mom_id_entity_electric,
           mom_id_entity.last_cid AS mom_id_entity_last_cid,
           mom_id_entity.pid AS mom_id_entity_pid,
           mom_id_entity.type_name AS mom_id_entity_type_name,
           mom_id_entity.x_locked AS mom_id_entity_x_locked
         FROM mom_id_entity
           JOIN auth__account_ ON mom_id_entity.pid = auth__account_.pid
           JOIN auth_account ON auth__account_.pid = auth_account.pid
           JOIN pap_person_has_account AS pap_person_has_account__1 ON pap_person_has_account__1."right" = auth_account.pid
           JOIN pap_person AS pap_person__3 ON pap_person__3.pid = pap_person_has_account__1."left"
         WHERE pap_person__3.lifetime__start = :lifetime__start_1

    >>> print (qrt.filter (Q.person.lifetime == ("2013/07/15", "2013/07/21"))) ### Auth.Account
    SQL: SELECT
           auth__account_.enabled AS auth__account__enabled,
           auth__account_.name AS auth__account__name,
           auth__account_.pid AS auth__account__pid,
           auth__account_.superuser AS auth__account__superuser,
           auth__account_.suspended AS auth__account__suspended,
           auth_account.password AS auth_account_password,
           auth_account.ph_name AS auth_account_ph_name,
           auth_account.pid AS auth_account_pid,
           mom_id_entity.electric AS mom_id_entity_electric,
           mom_id_entity.last_cid AS mom_id_entity_last_cid,
           mom_id_entity.pid AS mom_id_entity_pid,
           mom_id_entity.type_name AS mom_id_entity_type_name,
           mom_id_entity.x_locked AS mom_id_entity_x_locked
         FROM mom_id_entity
           JOIN auth__account_ ON mom_id_entity.pid = auth__account_.pid
           JOIN auth_account ON auth__account_.pid = auth_account.pid
           JOIN pap_person_has_account AS pap_person_has_account__1 ON pap_person_has_account__1."right" = auth_account.pid
           JOIN pap_person AS pap_person__3 ON pap_person__3.pid = pap_person_has_account__1."left"
         WHERE pap_person__3.lifetime__start = :lifetime__start_1
            AND pap_person__3.lifetime__finish = :lifetime__finish_1

    >>> str (qrt.filter (Q.RAW.person.lifetime == ("2013/07/15", ))) == str (qrt.filter (Q.person.lifetime == ("2013/07/15", ))) ### Auth.Account
    True

    >>> print (qrt.filter (Q.RAW.person.last_name == "Tanzer")) ### Auth.Account # doctest:+ELLIPSIS
    SQL: SELECT
           auth__account_.enabled AS auth__account__enabled,
           auth__account_.name AS auth__account__name,
           auth__account_.pid AS auth__account__pid,
           auth__account_.superuser AS auth__account__superuser,
           auth__account_.suspended AS auth__account__suspended,
           auth_account.password AS auth_account_password,
           auth_account.ph_name AS auth_account_ph_name,
           auth_account.pid AS auth_account_pid,
           mom_id_entity.electric AS mom_id_entity_electric,
           mom_id_entity.last_cid AS mom_id_entity_last_cid,
           mom_id_entity.pid AS mom_id_entity_pid,
           mom_id_entity.type_name AS mom_id_entity_type_name,
           mom_id_entity.x_locked AS mom_id_entity_x_locked
         FROM mom_id_entity
           JOIN auth__account_ ON mom_id_entity.pid = auth__account_.pid
           JOIN auth_account ON auth__account_.pid = auth_account.pid
           JOIN pap_person_has_account AS pap_person_has_account__1 ON pap_person_has_account__1."right" = auth_account.pid
           JOIN pap_person AS pap_person__3 ON pap_person__3.pid = pap_person_has_account__1."left"
         WHERE pap_person__3.__raw_last_name = :__raw_last_name_1

    >>> print (qrt.filter (Q.person.last_name == "tanzer")) ### Auth.Account # doctest:+ELLIPSIS
    SQL: SELECT
           auth__account_.enabled AS auth__account__enabled,
           auth__account_.name AS auth__account__name,
           auth__account_.pid AS auth__account__pid,
           auth__account_.superuser AS auth__account__superuser,
           auth__account_.suspended AS auth__account__suspended,
           auth_account.password AS auth_account_password,
           auth_account.ph_name AS auth_account_ph_name,
           auth_account.pid AS auth_account_pid,
           mom_id_entity.electric AS mom_id_entity_electric,
           mom_id_entity.last_cid AS mom_id_entity_last_cid,
           mom_id_entity.pid AS mom_id_entity_pid,
           mom_id_entity.type_name AS mom_id_entity_type_name,
           mom_id_entity.x_locked AS mom_id_entity_x_locked
         FROM mom_id_entity
           JOIN auth__account_ ON mom_id_entity.pid = auth__account_.pid
           JOIN auth_account ON auth__account_.pid = auth_account.pid
           JOIN pap_person_has_account AS pap_person_has_account__1 ON pap_person_has_account__1."right" = auth_account.pid
           JOIN pap_person AS pap_person__3 ON pap_person__3.pid = pap_person_has_account__1."left"
         WHERE pap_person__3.last_name = :last_name_1

    >>> print (qrt.filter (Q.person.last_name.STARTSWITH ("tan"))) ### Auth.Account # doctest:+ELLIPSIS
    SQL: SELECT
           auth__account_.enabled AS auth__account__enabled,
           auth__account_.name AS auth__account__name,
           auth__account_.pid AS auth__account__pid,
           auth__account_.superuser AS auth__account__superuser,
           auth__account_.suspended AS auth__account__suspended,
           auth_account.password AS auth_account_password,
           auth_account.ph_name AS auth_account_ph_name,
           auth_account.pid AS auth_account_pid,
           mom_id_entity.electric AS mom_id_entity_electric,
           mom_id_entity.last_cid AS mom_id_entity_last_cid,
           mom_id_entity.pid AS mom_id_entity_pid,
           mom_id_entity.type_name AS mom_id_entity_type_name,
           mom_id_entity.x_locked AS mom_id_entity_x_locked
         FROM mom_id_entity
           JOIN auth__account_ ON mom_id_entity.pid = auth__account_.pid
           JOIN auth_account ON auth__account_.pid = auth_account.pid
           JOIN pap_person_has_account AS pap_person_has_account__1 ON pap_person_has_account__1."right" = auth_account.pid
           JOIN pap_person AS pap_person__3 ON pap_person__3.pid = pap_person_has_account__1."left"
         WHERE pap_person__3.last_name LIKE :last_name_1 || '%%%%'

    >>> print (qrt.order_by (- Q.superuser).order_by (Q.name)) ### Auth.Account
    SQL: SELECT
           auth__account_.enabled AS auth__account__enabled,
           auth__account_.name AS auth__account__name,
           auth__account_.pid AS auth__account__pid,
           auth__account_.superuser AS auth__account__superuser,
           auth__account_.suspended AS auth__account__suspended,
           auth_account.password AS auth_account_password,
           auth_account.ph_name AS auth_account_ph_name,
           auth_account.pid AS auth_account_pid,
           mom_id_entity.electric AS mom_id_entity_electric,
           mom_id_entity.last_cid AS mom_id_entity_last_cid,
           mom_id_entity.pid AS mom_id_entity_pid,
           mom_id_entity.type_name AS mom_id_entity_type_name,
           mom_id_entity.x_locked AS mom_id_entity_x_locked
         FROM mom_id_entity
           JOIN auth__account_ ON mom_id_entity.pid = auth__account_.pid
           JOIN auth_account ON auth__account_.pid = auth_account.pid
         ORDER BY auth__account_.name, auth__account_.superuser DESC

    >>> print (qrt.order_by (Q.name, - Q.superuser)) ### Auth.Account
    SQL: SELECT
           auth__account_.enabled AS auth__account__enabled,
           auth__account_.name AS auth__account__name,
           auth__account_.pid AS auth__account__pid,
           auth__account_.superuser AS auth__account__superuser,
           auth__account_.suspended AS auth__account__suspended,
           auth_account.password AS auth_account_password,
           auth_account.ph_name AS auth_account_ph_name,
           auth_account.pid AS auth_account_pid,
           mom_id_entity.electric AS mom_id_entity_electric,
           mom_id_entity.last_cid AS mom_id_entity_last_cid,
           mom_id_entity.pid AS mom_id_entity_pid,
           mom_id_entity.type_name AS mom_id_entity_type_name,
           mom_id_entity.x_locked AS mom_id_entity_x_locked
         FROM mom_id_entity
           JOIN auth__account_ ON mom_id_entity.pid = auth__account_.pid
           JOIN auth_account ON auth__account_.pid = auth_account.pid
         ORDER BY auth__account_.name, auth__account_.superuser DESC

    >>> print (qrt.order_by (Q.person)) ### Auth.Account
    SQL: SELECT
           auth__account_.enabled AS auth__account__enabled,
           auth__account_.name AS auth__account__name,
           auth__account_.pid AS auth__account__pid,
           auth__account_.superuser AS auth__account__superuser,
           auth__account_.suspended AS auth__account__suspended,
           auth_account.password AS auth_account_password,
           auth_account.ph_name AS auth_account_ph_name,
           auth_account.pid AS auth_account_pid,
           mom_id_entity.electric AS mom_id_entity_electric,
           mom_id_entity.last_cid AS mom_id_entity_last_cid,
           mom_id_entity.pid AS mom_id_entity_pid,
           mom_id_entity.type_name AS mom_id_entity_type_name,
           mom_id_entity.x_locked AS mom_id_entity_x_locked
         FROM mom_id_entity
           JOIN auth__account_ ON mom_id_entity.pid = auth__account_.pid
           JOIN auth_account ON auth__account_.pid = auth_account.pid
           JOIN pap_person_has_account AS pap_person_has_account__1 ON pap_person_has_account__1."right" = auth_account.pid
           JOIN pap_person AS pap_person__3 ON pap_person__3.pid = pap_person_has_account__1."left"
         ORDER BY pap_person__3.last_name, pap_person__3.first_name, pap_person__3.middle_name, pap_person__3.title

    >>> print (qrt.order_by (- Q.person)) ### Auth.Account
    SQL: SELECT
           auth__account_.enabled AS auth__account__enabled,
           auth__account_.name AS auth__account__name,
           auth__account_.pid AS auth__account__pid,
           auth__account_.superuser AS auth__account__superuser,
           auth__account_.suspended AS auth__account__suspended,
           auth_account.password AS auth_account_password,
           auth_account.ph_name AS auth_account_ph_name,
           auth_account.pid AS auth_account_pid,
           mom_id_entity.electric AS mom_id_entity_electric,
           mom_id_entity.last_cid AS mom_id_entity_last_cid,
           mom_id_entity.pid AS mom_id_entity_pid,
           mom_id_entity.type_name AS mom_id_entity_type_name,
           mom_id_entity.x_locked AS mom_id_entity_x_locked
         FROM mom_id_entity
           JOIN auth__account_ ON mom_id_entity.pid = auth__account_.pid
           JOIN auth_account ON auth__account_.pid = auth_account.pid
           JOIN pap_person_has_account AS pap_person_has_account__1 ON pap_person_has_account__1."right" = auth_account.pid
           JOIN pap_person AS pap_person__3 ON pap_person__3.pid = pap_person_has_account__1."left"
         ORDER BY pap_person__3.last_name DESC, pap_person__3.first_name DESC, pap_person__3.middle_name DESC, pap_person__3.title DESC

    >>> print (qrt.order_by (Q.person.lifetime)) ### Auth.Account
    SQL: SELECT
           auth__account_.enabled AS auth__account__enabled,
           auth__account_.name AS auth__account__name,
           auth__account_.pid AS auth__account__pid,
           auth__account_.superuser AS auth__account__superuser,
           auth__account_.suspended AS auth__account__suspended,
           auth_account.password AS auth_account_password,
           auth_account.ph_name AS auth_account_ph_name,
           auth_account.pid AS auth_account_pid,
           mom_id_entity.electric AS mom_id_entity_electric,
           mom_id_entity.last_cid AS mom_id_entity_last_cid,
           mom_id_entity.pid AS mom_id_entity_pid,
           mom_id_entity.type_name AS mom_id_entity_type_name,
           mom_id_entity.x_locked AS mom_id_entity_x_locked
         FROM mom_id_entity
           JOIN auth__account_ ON mom_id_entity.pid = auth__account_.pid
           JOIN auth_account ON auth__account_.pid = auth_account.pid
           JOIN pap_person_has_account AS pap_person_has_account__1 ON pap_person_has_account__1."right" = auth_account.pid
           JOIN pap_person AS pap_person__3 ON pap_person__3.pid = pap_person_has_account__1."left"
         ORDER BY pap_person__3.lifetime__start, pap_person__3.lifetime__finish

    >>> print (qrt.order_by (- Q.person.lifetime)) ### Auth.Account
    SQL: SELECT
           auth__account_.enabled AS auth__account__enabled,
           auth__account_.name AS auth__account__name,
           auth__account_.pid AS auth__account__pid,
           auth__account_.superuser AS auth__account__superuser,
           auth__account_.suspended AS auth__account__suspended,
           auth_account.password AS auth_account_password,
           auth_account.ph_name AS auth_account_ph_name,
           auth_account.pid AS auth_account_pid,
           mom_id_entity.electric AS mom_id_entity_electric,
           mom_id_entity.last_cid AS mom_id_entity_last_cid,
           mom_id_entity.pid AS mom_id_entity_pid,
           mom_id_entity.type_name AS mom_id_entity_type_name,
           mom_id_entity.x_locked AS mom_id_entity_x_locked
         FROM mom_id_entity
           JOIN auth__account_ ON mom_id_entity.pid = auth__account_.pid
           JOIN auth_account ON auth__account_.pid = auth_account.pid
           JOIN pap_person_has_account AS pap_person_has_account__1 ON pap_person_has_account__1."right" = auth_account.pid
           JOIN pap_person AS pap_person__3 ON pap_person__3.pid = pap_person_has_account__1."left"
         ORDER BY pap_person__3.lifetime__start DESC, pap_person__3.lifetime__finish DESC

    >>> print (qrt.order_by ("person.last_name", "-name")) ### Auth.Account
    SQL: SELECT
           auth__account_.enabled AS auth__account__enabled,
           auth__account_.name AS auth__account__name,
           auth__account_.pid AS auth__account__pid,
           auth__account_.superuser AS auth__account__superuser,
           auth__account_.suspended AS auth__account__suspended,
           auth_account.password AS auth_account_password,
           auth_account.ph_name AS auth_account_ph_name,
           auth_account.pid AS auth_account_pid,
           mom_id_entity.electric AS mom_id_entity_electric,
           mom_id_entity.last_cid AS mom_id_entity_last_cid,
           mom_id_entity.pid AS mom_id_entity_pid,
           mom_id_entity.type_name AS mom_id_entity_type_name,
           mom_id_entity.x_locked AS mom_id_entity_x_locked
         FROM mom_id_entity
           JOIN auth__account_ ON mom_id_entity.pid = auth__account_.pid
           JOIN auth_account ON auth__account_.pid = auth_account.pid
           JOIN pap_person_has_account AS pap_person_has_account__1 ON pap_person_has_account__1."right" = auth_account.pid
           JOIN pap_person AS pap_person__3 ON pap_person__3.pid = pap_person_has_account__1."left"
         ORDER BY pap_person__3.last_name, auth__account_.name DESC

    >>> print (qrt.order_by ("person.last_name")) ### Auth.Account
    SQL: SELECT
           auth__account_.enabled AS auth__account__enabled,
           auth__account_.name AS auth__account__name,
           auth__account_.pid AS auth__account__pid,
           auth__account_.superuser AS auth__account__superuser,
           auth__account_.suspended AS auth__account__suspended,
           auth_account.password AS auth_account_password,
           auth_account.ph_name AS auth_account_ph_name,
           auth_account.pid AS auth_account_pid,
           mom_id_entity.electric AS mom_id_entity_electric,
           mom_id_entity.last_cid AS mom_id_entity_last_cid,
           mom_id_entity.pid AS mom_id_entity_pid,
           mom_id_entity.type_name AS mom_id_entity_type_name,
           mom_id_entity.x_locked AS mom_id_entity_x_locked
         FROM mom_id_entity
           JOIN auth__account_ ON mom_id_entity.pid = auth__account_.pid
           JOIN auth_account ON auth__account_.pid = auth_account.pid
           JOIN pap_person_has_account AS pap_person_has_account__1 ON pap_person_has_account__1."right" = auth_account.pid
           JOIN pap_person AS pap_person__3 ON pap_person__3.pid = pap_person_has_account__1."left"
         ORDER BY pap_person__3.last_name

    >>> print (qrt.order_by (Q.person.last_name)) ### Auth.Account
    SQL: SELECT
           auth__account_.enabled AS auth__account__enabled,
           auth__account_.name AS auth__account__name,
           auth__account_.pid AS auth__account__pid,
           auth__account_.superuser AS auth__account__superuser,
           auth__account_.suspended AS auth__account__suspended,
           auth_account.password AS auth_account_password,
           auth_account.ph_name AS auth_account_ph_name,
           auth_account.pid AS auth_account_pid,
           mom_id_entity.electric AS mom_id_entity_electric,
           mom_id_entity.last_cid AS mom_id_entity_last_cid,
           mom_id_entity.pid AS mom_id_entity_pid,
           mom_id_entity.type_name AS mom_id_entity_type_name,
           mom_id_entity.x_locked AS mom_id_entity_x_locked
         FROM mom_id_entity
           JOIN auth__account_ ON mom_id_entity.pid = auth__account_.pid
           JOIN auth_account ON auth__account_.pid = auth_account.pid
           JOIN pap_person_has_account AS pap_person_has_account__1 ON pap_person_has_account__1."right" = auth_account.pid
           JOIN pap_person AS pap_person__3 ON pap_person__3.pid = pap_person_has_account__1."left"
         ORDER BY pap_person__3.last_name

    >>> print (qrt.order_by (- Q.person.last_name)) ### Auth.Account
    SQL: SELECT
           auth__account_.enabled AS auth__account__enabled,
           auth__account_.name AS auth__account__name,
           auth__account_.pid AS auth__account__pid,
           auth__account_.superuser AS auth__account__superuser,
           auth__account_.suspended AS auth__account__suspended,
           auth_account.password AS auth_account_password,
           auth_account.ph_name AS auth_account_ph_name,
           auth_account.pid AS auth_account_pid,
           mom_id_entity.electric AS mom_id_entity_electric,
           mom_id_entity.last_cid AS mom_id_entity_last_cid,
           mom_id_entity.pid AS mom_id_entity_pid,
           mom_id_entity.type_name AS mom_id_entity_type_name,
           mom_id_entity.x_locked AS mom_id_entity_x_locked
         FROM mom_id_entity
           JOIN auth__account_ ON mom_id_entity.pid = auth__account_.pid
           JOIN auth_account ON auth__account_.pid = auth_account.pid
           JOIN pap_person_has_account AS pap_person_has_account__1 ON pap_person_has_account__1."right" = auth_account.pid
           JOIN pap_person AS pap_person__3 ON pap_person__3.pid = pap_person_has_account__1."left"
         ORDER BY pap_person__3.last_name DESC

    >>> print (qrt.filter (Q.person.last_name.STARTSWITH ("tan") | Q.person.last_name.ENDSWITH ("beck"))) ### Auth.Account # doctest:+ELLIPSIS
    SQL: SELECT
           auth__account_.enabled AS auth__account__enabled,
           auth__account_.name AS auth__account__name,
           auth__account_.pid AS auth__account__pid,
           auth__account_.superuser AS auth__account__superuser,
           auth__account_.suspended AS auth__account__suspended,
           auth_account.password AS auth_account_password,
           auth_account.ph_name AS auth_account_ph_name,
           auth_account.pid AS auth_account_pid,
           mom_id_entity.electric AS mom_id_entity_electric,
           mom_id_entity.last_cid AS mom_id_entity_last_cid,
           mom_id_entity.pid AS mom_id_entity_pid,
           mom_id_entity.type_name AS mom_id_entity_type_name,
           mom_id_entity.x_locked AS mom_id_entity_x_locked
         FROM mom_id_entity
           JOIN auth__account_ ON mom_id_entity.pid = auth__account_.pid
           JOIN auth_account ON auth__account_.pid = auth_account.pid
           JOIN pap_person_has_account AS pap_person_has_account__1 ON pap_person_has_account__1."right" = auth_account.pid
           JOIN pap_person AS pap_person__3 ON pap_person__3.pid = pap_person_has_account__1."left"
         WHERE (pap_person__3.last_name LIKE :last_name_1 || '%%%%')
            OR (pap_person__3.last_name LIKE '%%%%' || :last_name_2)

    >>> print (qrt.filter (Q.person_links)) ### Auth.Account # doctest:+ELLIPSIS
    SQL: SELECT
           auth__account_.enabled AS auth__account__enabled,
           auth__account_.name AS auth__account__name,
           auth__account_.pid AS auth__account__pid,
           auth__account_.superuser AS auth__account__superuser,
           auth__account_.suspended AS auth__account__suspended,
           auth_account.password AS auth_account_password,
           auth_account.ph_name AS auth_account_ph_name,
           auth_account.pid AS auth_account_pid,
           mom_id_entity.electric AS mom_id_entity_electric,
           mom_id_entity.last_cid AS mom_id_entity_last_cid,
           mom_id_entity.pid AS mom_id_entity_pid,
           mom_id_entity.type_name AS mom_id_entity_type_name,
           mom_id_entity.x_locked AS mom_id_entity_x_locked
         FROM mom_id_entity
           JOIN auth__account_ ON mom_id_entity.pid = auth__account_.pid
           JOIN auth_account ON auth__account_.pid = auth_account.pid
           JOIN pap_person_has_account AS pap_person_has_account__2 ON pap_person_has_account__2."right" = auth_account.pid
         WHERE pap_person_has_account__2."right" IS NOT NULL

    >>> print (qrt.filter (Q.person_links.person)) ### Auth.Account # doctest:+ELLIPSIS
    SQL: SELECT
           auth__account_.enabled AS auth__account__enabled,
           auth__account_.name AS auth__account__name,
           auth__account_.pid AS auth__account__pid,
           auth__account_.superuser AS auth__account__superuser,
           auth__account_.suspended AS auth__account__suspended,
           auth_account.password AS auth_account_password,
           auth_account.ph_name AS auth_account_ph_name,
           auth_account.pid AS auth_account_pid,
           mom_id_entity.electric AS mom_id_entity_electric,
           mom_id_entity.last_cid AS mom_id_entity_last_cid,
           mom_id_entity.pid AS mom_id_entity_pid,
           mom_id_entity.type_name AS mom_id_entity_type_name,
           mom_id_entity.x_locked AS mom_id_entity_x_locked
         FROM mom_id_entity
           JOIN auth__account_ ON mom_id_entity.pid = auth__account_.pid
           JOIN auth_account ON auth__account_.pid = auth_account.pid
           JOIN pap_person_has_account AS pap_person_has_account__2 ON pap_person_has_account__2."right" = auth_account.pid
         WHERE pap_person_has_account__2."left" IS NOT NULL

    >>> print (qrt.filter (Q.person_links.person == 42)) ### Auth.Account # doctest:+ELLIPSIS
    SQL: SELECT
           auth__account_.enabled AS auth__account__enabled,
           auth__account_.name AS auth__account__name,
           auth__account_.pid AS auth__account__pid,
           auth__account_.superuser AS auth__account__superuser,
           auth__account_.suspended AS auth__account__suspended,
           auth_account.password AS auth_account_password,
           auth_account.ph_name AS auth_account_ph_name,
           auth_account.pid AS auth_account_pid,
           mom_id_entity.electric AS mom_id_entity_electric,
           mom_id_entity.last_cid AS mom_id_entity_last_cid,
           mom_id_entity.pid AS mom_id_entity_pid,
           mom_id_entity.type_name AS mom_id_entity_type_name,
           mom_id_entity.x_locked AS mom_id_entity_x_locked
         FROM mom_id_entity
           JOIN auth__account_ ON mom_id_entity.pid = auth__account_.pid
           JOIN auth_account ON auth__account_.pid = auth_account.pid
           JOIN pap_person_has_account AS pap_person_has_account__2 ON pap_person_has_account__2."right" = auth_account.pid
         WHERE pap_person_has_account__2."left" = :left_1

    >>> print (qrt.filter (Q.person_links.person.last_name == "tanzer")) ### Auth.Account # doctest:+ELLIPSIS
    SQL: SELECT
           auth__account_.enabled AS auth__account__enabled,
           auth__account_.name AS auth__account__name,
           auth__account_.pid AS auth__account__pid,
           auth__account_.superuser AS auth__account__superuser,
           auth__account_.suspended AS auth__account__suspended,
           auth_account.password AS auth_account_password,
           auth_account.ph_name AS auth_account_ph_name,
           auth_account.pid AS auth_account_pid,
           mom_id_entity.electric AS mom_id_entity_electric,
           mom_id_entity.last_cid AS mom_id_entity_last_cid,
           mom_id_entity.pid AS mom_id_entity_pid,
           mom_id_entity.type_name AS mom_id_entity_type_name,
           mom_id_entity.x_locked AS mom_id_entity_x_locked
         FROM mom_id_entity
           JOIN auth__account_ ON mom_id_entity.pid = auth__account_.pid
           JOIN auth_account ON auth__account_.pid = auth_account.pid
           JOIN pap_person_has_account AS pap_person_has_account__2 ON pap_person_has_account__2."right" = auth_account.pid
           JOIN pap_person AS pap_person__4 ON pap_person__4.pid = pap_person_has_account__2."left"
         WHERE pap_person__4.last_name = :last_name_1

    >>> print (qrt.filter (Q.person_links.person.account_links.account.name == "foo@bar.baz")) ### Auth.Account # doctest:+ELLIPSIS
    SQL: SELECT
           auth__account_.enabled AS auth__account__enabled,
           auth__account_.name AS auth__account__name,
           auth__account_.pid AS auth__account__pid,
           auth__account_.superuser AS auth__account__superuser,
           auth__account_.suspended AS auth__account__suspended,
           auth_account.password AS auth_account_password,
           auth_account.ph_name AS auth_account_ph_name,
           auth_account.pid AS auth_account_pid,
           mom_id_entity.electric AS mom_id_entity_electric,
           mom_id_entity.last_cid AS mom_id_entity_last_cid,
           mom_id_entity.pid AS mom_id_entity_pid,
           mom_id_entity.type_name AS mom_id_entity_type_name,
           mom_id_entity.x_locked AS mom_id_entity_x_locked
         FROM mom_id_entity
           JOIN auth__account_ ON mom_id_entity.pid = auth__account_.pid
           JOIN auth_account ON auth__account_.pid = auth_account.pid
           JOIN pap_person_has_account AS pap_person_has_account__2 ON pap_person_has_account__2."right" = auth_account.pid
           JOIN pap_person AS pap_person__4 ON pap_person__4.pid = pap_person_has_account__2."left"
           JOIN pap_person_has_account AS pap_person_has_account__3 ON pap_person_has_account__3."left" = pap_person__4.pid
           JOIN auth_account AS auth_account__1 ON auth_account__1.pid = pap_person_has_account__3."right"
           JOIN auth__account_ AS auth__account___1 ON auth__account___1.pid = pap_person_has_account__3."right"
         WHERE auth__account___1.name = :name_1

    >>> ET = apt ["PAP.Person_has_Account"]
    >>> qrt = apt.DBW.PNS.Q_Result.E_Type (ET, _strict = False)

    >>> print (qrt.filter (Q.person.last_name == "nl")) ### PAP.Person_has_Account
    SQL: SELECT
           mom_id_entity.electric AS mom_id_entity_electric,
           mom_id_entity.last_cid AS mom_id_entity_last_cid,
           mom_id_entity.pid AS mom_id_entity_pid,
           mom_id_entity.type_name AS mom_id_entity_type_name,
           mom_id_entity.x_locked AS mom_id_entity_x_locked,
           pap_person_has_account."left" AS pap_person_has_account_left,
           pap_person_has_account."right" AS pap_person_has_account_right,
           pap_person_has_account.pid AS pap_person_has_account_pid
         FROM mom_id_entity
           JOIN pap_person_has_account ON mom_id_entity.pid = pap_person_has_account.pid
           JOIN pap_person AS pap_person__5 ON pap_person__5.pid = pap_person_has_account."left"
         WHERE pap_person__5.last_name = :last_name_1

    >>> ET = apt ["PAP.Subject"]
    >>> qrt = apt.DBW.PNS.Q_Result.E_Type (ET, _strict = False)

    >>> print (qrt.filter (Q.phone_links.phone.number == 42)) ### PAP.Subject
    SQL: SELECT
           mom_id_entity.electric AS mom_id_entity_electric,
           mom_id_entity.last_cid AS mom_id_entity_last_cid,
           mom_id_entity.pid AS mom_id_entity_pid,
           mom_id_entity.type_name AS mom_id_entity_type_name,
           mom_id_entity.x_locked AS mom_id_entity_x_locked,
           pap_company.__raw_name AS pap_company___raw_name,
           pap_company.__raw_registered_in AS pap_company___raw_registered_in,
           pap_company.__raw_short_name AS pap_company___raw_short_name,
           pap_company.lifetime__finish AS pap_company_lifetime__finish,
           pap_company.lifetime__start AS pap_company_lifetime__start,
           pap_company.name AS pap_company_name,
           pap_company.pid AS pap_company_pid,
           pap_company.registered_in AS pap_company_registered_in,
           pap_company.short_name AS pap_company_short_name,
           pap_person.__raw_first_name AS pap_person___raw_first_name,
           pap_person.__raw_last_name AS pap_person___raw_last_name,
           pap_person.__raw_middle_name AS pap_person___raw_middle_name,
           pap_person.__raw_title AS pap_person___raw_title,
           pap_person.first_name AS pap_person_first_name,
           pap_person.last_name AS pap_person_last_name,
           pap_person.lifetime__finish AS pap_person_lifetime__finish,
           pap_person.lifetime__start AS pap_person_lifetime__start,
           pap_person.middle_name AS pap_person_middle_name,
           pap_person.pid AS pap_person_pid,
           pap_person.sex AS pap_person_sex,
           pap_person.title AS pap_person_title
         FROM mom_id_entity
           LEFT OUTER JOIN pap_company ON mom_id_entity.pid = pap_company.pid
           LEFT OUTER JOIN pap_person ON mom_id_entity.pid = pap_person.pid
           LEFT OUTER JOIN pap_subject_has_property AS pap_subject_has_property__1 ON pap_subject_has_property__1."left" = mom_id_entity.pid
           LEFT OUTER JOIN pap_phone AS pap_phone__3 ON pap_phone__3.pid = pap_subject_has_property__1."right"
         WHERE (mom_id_entity.pid = pap_company.pid
            OR mom_id_entity.pid = pap_person.pid)
            AND pap_phone__3.number = :number_1

    >>> ET = apt ["SRM.Sailor"]
    >>> qrt = apt.DBW.PNS.Q_Result.E_Type (ET, _strict = False)

    >>> print (qrt.filter (Q.left == Q.BVAR.this)) ### SRM.Sailor
    SQL: SELECT
           mom_id_entity.electric AS mom_id_entity_electric,
           mom_id_entity.last_cid AS mom_id_entity_last_cid,
           mom_id_entity.pid AS mom_id_entity_pid,
           mom_id_entity.type_name AS mom_id_entity_type_name,
           mom_id_entity.x_locked AS mom_id_entity_x_locked,
           srm_sailor."left" AS srm_sailor_left,
           srm_sailor.__raw_mna_number AS srm_sailor___raw_mna_number,
           srm_sailor.club AS srm_sailor_club,
           srm_sailor.mna_number AS srm_sailor_mna_number,
           srm_sailor.nation AS srm_sailor_nation,
           srm_sailor.pid AS srm_sailor_pid
         FROM mom_id_entity
           JOIN srm_sailor ON mom_id_entity.pid = srm_sailor.pid
         WHERE srm_sailor."left" = :this

    >>> print (qrt.filter (Q.left == 23)) ### SRM.Sailor
    SQL: SELECT
           mom_id_entity.electric AS mom_id_entity_electric,
           mom_id_entity.last_cid AS mom_id_entity_last_cid,
           mom_id_entity.pid AS mom_id_entity_pid,
           mom_id_entity.type_name AS mom_id_entity_type_name,
           mom_id_entity.x_locked AS mom_id_entity_x_locked,
           srm_sailor."left" AS srm_sailor_left,
           srm_sailor.__raw_mna_number AS srm_sailor___raw_mna_number,
           srm_sailor.club AS srm_sailor_club,
           srm_sailor.mna_number AS srm_sailor_mna_number,
           srm_sailor.nation AS srm_sailor_nation,
           srm_sailor.pid AS srm_sailor_pid
         FROM mom_id_entity
           JOIN srm_sailor ON mom_id_entity.pid = srm_sailor.pid
         WHERE srm_sailor."left" = :left_1

    >>> print (qrt.filter (Q.left.pid == 23)) ### SRM.Sailor
    SQL: SELECT
           mom_id_entity.electric AS mom_id_entity_electric,
           mom_id_entity.last_cid AS mom_id_entity_last_cid,
           mom_id_entity.pid AS mom_id_entity_pid,
           mom_id_entity.type_name AS mom_id_entity_type_name,
           mom_id_entity.x_locked AS mom_id_entity_x_locked,
           srm_sailor."left" AS srm_sailor_left,
           srm_sailor.__raw_mna_number AS srm_sailor___raw_mna_number,
           srm_sailor.club AS srm_sailor_club,
           srm_sailor.mna_number AS srm_sailor_mna_number,
           srm_sailor.nation AS srm_sailor_nation,
           srm_sailor.pid AS srm_sailor_pid
         FROM mom_id_entity
           JOIN srm_sailor ON mom_id_entity.pid = srm_sailor.pid
         WHERE srm_sailor."left" = :left_1

    >>> print (formatted_select (None, select = qrt.filter (Q.left.pid == 23).sa_query_count)) ### SRM.Sailor
    SELECT count(:param_1) AS count
        FROM (SELECT mom_id_entity.electric AS mom_id_entity_electric,
                     mom_id_entity.last_cid AS mom_id_entity_last_cid,
                     mom_id_entity.pid AS mom_id_entity_pid,
                     mom_id_entity.type_name AS mom_id_entity_type_name,
                     mom_id_entity.x_locked AS mom_id_entity_x_locked,
                     srm_sailor."left" AS srm_sailor_left,
                     srm_sailor.__raw_mna_number AS srm_sailor___raw_mna_number,
                     srm_sailor.club AS srm_sailor_club,
                     srm_sailor.mna_number AS srm_sailor_mna_number,
                     srm_sailor.nation AS srm_sailor_nation,
                     srm_sailor.pid AS srm_sailor_pid
              FROM mom_id_entity
                 JOIN srm_sailor ON mom_id_entity.pid = srm_sailor.pid
        WHERE srm_sailor."left" = :left_1
             ) AS __count__

    >>> ET = apt ["SRM.Team"]
    >>> qrt = apt.DBW.PNS.Q_Result.E_Type (ET, _strict = False)

    >>> print (qrt.filter (Q.regatta.event.date.start == "2010-09-18")) ### SRM.Team
    SQL: SELECT
           mom_id_entity.electric AS mom_id_entity_electric,
           mom_id_entity.last_cid AS mom_id_entity_last_cid,
           mom_id_entity.pid AS mom_id_entity_pid,
           mom_id_entity.type_name AS mom_id_entity_type_name,
           mom_id_entity.x_locked AS mom_id_entity_x_locked,
           srm_team."desc" AS srm_team_desc,
           srm_team."left" AS srm_team_left,
           srm_team.__raw_name AS srm_team___raw_name,
           srm_team.club AS srm_team_club,
           srm_team.leader AS srm_team_leader,
           srm_team.name AS srm_team_name,
           srm_team.pid AS srm_team_pid,
           srm_team.place AS srm_team_place,
           srm_team.registration_date AS srm_team_registration_date
         FROM mom_id_entity
           JOIN srm_team ON mom_id_entity.pid = srm_team.pid
           JOIN srm_regatta_c AS srm_regatta_c__1 ON srm_regatta_c__1.pid = srm_team."left"
           JOIN srm_regatta AS srm_regatta__2 ON srm_regatta__2.pid = srm_team."left"
           JOIN srm_regatta_event AS srm_regatta_event__3 ON srm_regatta_event__3.pid = srm_regatta__2."left"
         WHERE srm_regatta_event__3.date__start = :date__start_1

    >>> print (qrt.order_by (TFL.Sorted_By ("-regatta.event.date.start", "name"))) ### SRM.Team
    SQL: SELECT
           mom_id_entity.electric AS mom_id_entity_electric,
           mom_id_entity.last_cid AS mom_id_entity_last_cid,
           mom_id_entity.pid AS mom_id_entity_pid,
           mom_id_entity.type_name AS mom_id_entity_type_name,
           mom_id_entity.x_locked AS mom_id_entity_x_locked,
           srm_team."desc" AS srm_team_desc,
           srm_team."left" AS srm_team_left,
           srm_team.__raw_name AS srm_team___raw_name,
           srm_team.club AS srm_team_club,
           srm_team.leader AS srm_team_leader,
           srm_team.name AS srm_team_name,
           srm_team.pid AS srm_team_pid,
           srm_team.place AS srm_team_place,
           srm_team.registration_date AS srm_team_registration_date
         FROM mom_id_entity
           JOIN srm_team ON mom_id_entity.pid = srm_team.pid
           JOIN srm_regatta_c AS srm_regatta_c__1 ON srm_regatta_c__1.pid = srm_team."left"
           JOIN srm_regatta AS srm_regatta__2 ON srm_regatta__2.pid = srm_team."left"
           JOIN srm_regatta_event AS srm_regatta_event__3 ON srm_regatta_event__3.pid = srm_regatta__2."left"
         ORDER BY srm_regatta_event__3.date__start DESC, srm_team.name

    >>> ET  = apt ["MOM.MD_Change"]
    >>> qrt = apt.DBW.PNS.Q_Result.E_Type (ET, _strict = False)

    >>> print (apt.DBW.PNS.Q_Result.E_Type_Reload (ET)) ### MOM.MD_Change
    SQL: SELECT
           mom_md_change."user" AS mom_md_change_user,
           mom_md_change.c_time AS mom_md_change_c_time,
           mom_md_change.c_user AS mom_md_change_c_user,
           mom_md_change.cid AS mom_md_change_cid,
           mom_md_change.kind AS mom_md_change_kind,
           mom_md_change.parent_cid AS mom_md_change_parent_cid,
           mom_md_change.pid AS mom_md_change_pid,
           mom_md_change.scm_change AS mom_md_change_scm_change,
           mom_md_change.time AS mom_md_change_time,
           mom_md_change.type_name AS mom_md_change_type_name
         FROM mom_md_change
         WHERE mom_md_change.cid = :spk
         LIMIT :param_1

    >>> ET  = apt ["SWP.Clip_O"]
    >>> qrc = apt.DBW.PNS.Q_Result.E_Type (ET, _strict = False)

    >>> show_query (qrc.filter (Q.left.type_name == "SWP.Page")) ### SWP.Clip_O
    SQL: SELECT
           mom_id_entity.electric AS mom_id_entity_electric,
           mom_id_entity.last_cid AS mom_id_entity_last_cid,
           mom_id_entity.pid AS mom_id_entity_pid,
           mom_id_entity.type_name AS mom_id_entity_type_name,
           mom_id_entity.x_locked AS mom_id_entity_x_locked,
           swp_clip_o."left" AS swp_clip_o_left,
           swp_clip_o.abstract AS swp_clip_o_abstract,
           swp_clip_o.contents AS swp_clip_o_contents,
           swp_clip_o.date__finish AS swp_clip_o_date__finish,
           swp_clip_o.date__start AS swp_clip_o_date__start,
           swp_clip_o.date_x__finish AS swp_clip_o_date_x__finish,
           swp_clip_o.date_x__start AS swp_clip_o_date_x__start,
           swp_clip_o.pid AS swp_clip_o_pid,
           swp_clip_o.prio AS swp_clip_o_prio
         FROM mom_id_entity
           JOIN swp_clip_o ON mom_id_entity.pid = swp_clip_o.pid
           LEFT OUTER JOIN mom_id_entity AS mom_id_entity__26 ON mom_id_entity__26.pid = swp_clip_o."left"
         WHERE mom_id_entity__26.type_name = :type_name_1
    Parameters:
         type_name_1          : u'SWP.Page'

    >>> show_query (qrc.filter (Q.left.type_name == "SWP.Page_Y")) ### SWP.Clip_O
    SQL: SELECT
           mom_id_entity.electric AS mom_id_entity_electric,
           mom_id_entity.last_cid AS mom_id_entity_last_cid,
           mom_id_entity.pid AS mom_id_entity_pid,
           mom_id_entity.type_name AS mom_id_entity_type_name,
           mom_id_entity.x_locked AS mom_id_entity_x_locked,
           swp_clip_o."left" AS swp_clip_o_left,
           swp_clip_o.abstract AS swp_clip_o_abstract,
           swp_clip_o.contents AS swp_clip_o_contents,
           swp_clip_o.date__finish AS swp_clip_o_date__finish,
           swp_clip_o.date__start AS swp_clip_o_date__start,
           swp_clip_o.date_x__finish AS swp_clip_o_date_x__finish,
           swp_clip_o.date_x__start AS swp_clip_o_date_x__start,
           swp_clip_o.pid AS swp_clip_o_pid,
           swp_clip_o.prio AS swp_clip_o_prio
         FROM mom_id_entity
           JOIN swp_clip_o ON mom_id_entity.pid = swp_clip_o.pid
           LEFT OUTER JOIN mom_id_entity AS mom_id_entity__26 ON mom_id_entity__26.pid = swp_clip_o."left"
         WHERE mom_id_entity__26.type_name = :type_name_1
    Parameters:
         type_name_1          : u'SWP.Page_Y'

    >>> ET = apt ["SRM.Race_Result"]
    >>> qrt = apt.DBW.PNS.Q_Result.E_Type (ET, _strict = False)

    >>> show_query (qrt.attrs (Q.left, Q.SUM (Q.points), Q.left.points).group_by (Q.left)) ### SRM.Race_Result
    SQL: SELECT DISTINCT
           coalesce(sum(srm_race_result.points), :param_1) AS points_sum,
           srm_boat_in_regatta__1.points AS srm_boat_in_regatta__1_points,
           srm_race_result."left" AS srm_race_result_left
         FROM mom_id_entity
           JOIN srm_race_result ON mom_id_entity.pid = srm_race_result.pid
           JOIN srm_boat_in_regatta AS srm_boat_in_regatta__1 ON srm_boat_in_regatta__1.pid = srm_race_result."left"
         GROUP BY srm_race_result."left"
    Parameters:
         param_1              : 0

    >>> ET = apt ["SRM.Boat_in_Regatta"]
    >>> qrt = apt.DBW.PNS.Q_Result.E_Type (ET, _strict = False)

    >>> show_query (qrt.attrs (Q.boat, Q.SUM (Q.race_results.points), Q.points).group_by (Q.boat)) ### SRM.Boat_in_Regatta
    SQL: SELECT DISTINCT
           coalesce(sum(srm_race_result__1.points), :param_1) AS points_sum,
           srm_boat_in_regatta."left" AS srm_boat_in_regatta_left,
           srm_boat_in_regatta.points AS srm_boat_in_regatta_points
         FROM mom_id_entity
           JOIN srm_boat_in_regatta ON mom_id_entity.pid = srm_boat_in_regatta.pid
           JOIN srm_race_result AS srm_race_result__1 ON srm_race_result__1."left" = srm_boat_in_regatta.pid
         GROUP BY srm_boat_in_regatta."left"
    Parameters:
         param_1              : 0

"""

_test_q_result_x = """
    >>> apt, url = Scaffold.app_type_and_url (%(p1)s, %(n1)s)

    >>> ET = apt ["SRM.Regatta_C"]
    >>> qrs = apt.DBW.PNS.Q_Result.E_Type (ET, _strict = True)
    >>> qrt = apt.DBW.PNS.Q_Result.E_Type (ET, _strict = False)

    ### XXX fix this: nested Q-expressions should work

    >>> print (qrt.filter (Q.races %% 2 == 1)) ### SRM.Regatta_C
    SQL: SELECT
           mom_id_entity.electric AS mom_id_entity_electric,
           mom_id_entity.last_cid AS mom_id_entity_last_cid,
           mom_id_entity.pid AS mom_id_entity_pid,
           mom_id_entity.type_name AS mom_id_entity_type_name,
           mom_id_entity.x_locked AS mom_id_entity_x_locked,
           srm_regatta."left" AS srm_regatta_left,
           srm_regatta.boat_class AS srm_regatta_boat_class,
           srm_regatta.discards AS srm_regatta_discards,
           srm_regatta.is_cancelled AS srm_regatta_is_cancelled,
           srm_regatta.kind AS srm_regatta_kind,
           srm_regatta.perma_name AS srm_regatta_perma_name,
           srm_regatta.pid AS srm_regatta_pid,
           srm_regatta.races AS srm_regatta_races,
           srm_regatta.result__date AS srm_regatta_result__date,
           srm_regatta.result__software AS srm_regatta_result__software,
           srm_regatta.result__status AS srm_regatta_result__status,
           srm_regatta_c.is_team_race AS srm_regatta_c_is_team_race,
           srm_regatta_c.pid AS srm_regatta_c_pid
         FROM mom_id_entity
           JOIN srm_regatta ON mom_id_entity.pid = srm_regatta.pid
           JOIN srm_regatta_c ON srm_regatta.pid = srm_regatta_c.pid
         WHERE srm_regatta.races %% :races_1 = :param_1

    >>> print (qrt.filter (1 == (Q.races %% 2))) ### SRM.Regatta_C
    SQL: SELECT
           mom_id_entity.electric AS mom_id_entity_electric,
           mom_id_entity.last_cid AS mom_id_entity_last_cid,
           mom_id_entity.pid AS mom_id_entity_pid,
           mom_id_entity.type_name AS mom_id_entity_type_name,
           mom_id_entity.x_locked AS mom_id_entity_x_locked,
           srm_regatta."left" AS srm_regatta_left,
           srm_regatta.boat_class AS srm_regatta_boat_class,
           srm_regatta.discards AS srm_regatta_discards,
           srm_regatta.is_cancelled AS srm_regatta_is_cancelled,
           srm_regatta.kind AS srm_regatta_kind,
           srm_regatta.perma_name AS srm_regatta_perma_name,
           srm_regatta.pid AS srm_regatta_pid,
           srm_regatta.races AS srm_regatta_races,
           srm_regatta.result__date AS srm_regatta_result__date,
           srm_regatta.result__software AS srm_regatta_result__software,
           srm_regatta.result__status AS srm_regatta_result__status,
           srm_regatta_c.is_team_race AS srm_regatta_c_is_team_race,
           srm_regatta_c.pid AS srm_regatta_c_pid
         FROM mom_id_entity
           JOIN srm_regatta ON mom_id_entity.pid = srm_regatta.pid
           JOIN srm_regatta_c ON srm_regatta.pid = srm_regatta_c.pid
         WHERE srm_regatta.races %% :races_1 = :param_1

    >>> print (qrt.filter (Q.races - 3 == Q.discards)) ### SRM.Regatta_C
    SQL: SELECT
           mom_id_entity.electric AS mom_id_entity_electric,
           mom_id_entity.last_cid AS mom_id_entity_last_cid,
           mom_id_entity.pid AS mom_id_entity_pid,
           mom_id_entity.type_name AS mom_id_entity_type_name,
           mom_id_entity.x_locked AS mom_id_entity_x_locked,
           srm_regatta."left" AS srm_regatta_left,
           srm_regatta.boat_class AS srm_regatta_boat_class,
           srm_regatta.discards AS srm_regatta_discards,
           srm_regatta.is_cancelled AS srm_regatta_is_cancelled,
           srm_regatta.kind AS srm_regatta_kind,
           srm_regatta.perma_name AS srm_regatta_perma_name,
           srm_regatta.pid AS srm_regatta_pid,
           srm_regatta.races AS srm_regatta_races,
           srm_regatta.result__date AS srm_regatta_result__date,
           srm_regatta.result__software AS srm_regatta_result__software,
           srm_regatta.result__status AS srm_regatta_result__status,
           srm_regatta_c.is_team_race AS srm_regatta_c_is_team_race,
           srm_regatta_c.pid AS srm_regatta_c_pid
         FROM mom_id_entity
           JOIN srm_regatta ON mom_id_entity.pid = srm_regatta.pid
           JOIN srm_regatta_c ON srm_regatta.pid = srm_regatta_c.pid
         WHERE srm_regatta.races - :races_1 = srm_regatta.discards

    >>> print (qrt.filter (Q.races == Q.discards + 3)) ### SRM.Regatta_C
    SQL: SELECT
           mom_id_entity.electric AS mom_id_entity_electric,
           mom_id_entity.last_cid AS mom_id_entity_last_cid,
           mom_id_entity.pid AS mom_id_entity_pid,
           mom_id_entity.type_name AS mom_id_entity_type_name,
           mom_id_entity.x_locked AS mom_id_entity_x_locked,
           srm_regatta."left" AS srm_regatta_left,
           srm_regatta.boat_class AS srm_regatta_boat_class,
           srm_regatta.discards AS srm_regatta_discards,
           srm_regatta.is_cancelled AS srm_regatta_is_cancelled,
           srm_regatta.kind AS srm_regatta_kind,
           srm_regatta.perma_name AS srm_regatta_perma_name,
           srm_regatta.pid AS srm_regatta_pid,
           srm_regatta.races AS srm_regatta_races,
           srm_regatta.result__date AS srm_regatta_result__date,
           srm_regatta.result__software AS srm_regatta_result__software,
           srm_regatta.result__status AS srm_regatta_result__status,
           srm_regatta_c.is_team_race AS srm_regatta_c_is_team_race,
           srm_regatta_c.pid AS srm_regatta_c_pid
         FROM mom_id_entity
           JOIN srm_regatta ON mom_id_entity.pid = srm_regatta.pid
           JOIN srm_regatta_c ON srm_regatta.pid = srm_regatta_c.pid
         WHERE srm_regatta.races = srm_regatta.discards + :discards_1

"""

_test_qc_map = """
    >>> apt, url = Scaffold.app_type_and_url (%(p1)s, %(n1)s)

    >>> show_qc_map (apt)
    <SAW : MOM.Id_Entity [mom_id_entity]>
        creation                  : <SAW : Rev_Ref `creation`>
        electric                  : mom_id_entity.electric
        last_change               : <SAW : Rev_Ref `last_change`>
        last_cid                  : mom_id_entity.last_cid
        pid                       : mom_id_entity.pid
        type_name                 : mom_id_entity.type_name
        x_locked                  : mom_id_entity.x_locked
    <SAW : MOM.MD_Change [mom_md_change]>
        c_time                    : mom_md_change.c_time
        c_user                    : mom_md_change.c_user
        cid                       : mom_md_change.cid
        kind                      : mom_md_change.kind
        parent                    : <SAW : Int `parent`>
        parent_cid                : mom_md_change.parent_cid
        pid                       : mom_md_change.pid
        scm_change                : mom_md_change.scm_change
        time                      : mom_md_change.time
        type_name                 : mom_md_change.type_name
        user                      : mom_md_change.user
    <SAW : MOM.Link [mom_id_entity]>
        creation                  : <SAW : Rev_Ref `creation`>
        electric                  : mom_id_entity.electric
        last_change               : <SAW : Rev_Ref `last_change`>
        last_cid                  : mom_id_entity.last_cid
        left                      : <SAW : Left `left` (Auth.Account_Activation | Auth.Account_EMail_Verification |
        pid                       : mom_id_entity.pid
        type_name                 : mom_id_entity.type_name
        x_locked                  : mom_id_entity.x_locked
    <SAW : MOM.Link1 [mom_id_entity]>
        creation                  : <SAW : Rev_Ref `creation`>
        electric                  : mom_id_entity.electric
        last_change               : <SAW : Rev_Ref `last_change`>
        last_cid                  : mom_id_entity.last_cid
        left                      : <SAW : Left `left` (Auth.Account_Activation | Auth.Account_EMail_Verification |
        pid                       : mom_id_entity.pid
        type_name                 : mom_id_entity.type_name
        x_locked                  : mom_id_entity.x_locked
    <SAW : MOM._MOM_Link_n_ [mom_id_entity]>
        creation                  : <SAW : Rev_Ref `creation`>
        electric                  : mom_id_entity.electric
        last_change               : <SAW : Rev_Ref `last_change`>
        last_cid                  : mom_id_entity.last_cid
        left                      : <SAW : Left `left` (Auth.Account_in_Group | PAP.Person_has_Account | PAP.Subject
        pid                       : mom_id_entity.pid
        right                     : <SAW : Right `right` (Auth.Account_in_Group | PAP.Person_has_Account | PAP.Subje
        type_name                 : mom_id_entity.type_name
        x_locked                  : mom_id_entity.x_locked
    <SAW : MOM.Link2 [mom_id_entity]>
        creation                  : <SAW : Rev_Ref `creation`>
        electric                  : mom_id_entity.electric
        last_change               : <SAW : Rev_Ref `last_change`>
        last_cid                  : mom_id_entity.last_cid
        left                      : <SAW : Left `left` (Auth.Account_in_Group | PAP.Person_has_Account | PAP.Subject
        pid                       : mom_id_entity.pid
        right                     : <SAW : Right `right` (Auth.Account_in_Group | PAP.Person_has_Account | PAP.Subje
        type_name                 : mom_id_entity.type_name
        x_locked                  : mom_id_entity.x_locked
    <SAW : MOM.Link3 [mom_id_entity]>
        creation                  : <SAW : Rev_Ref `creation`>
        electric                  : mom_id_entity.electric
        last_change               : <SAW : Rev_Ref `last_change`>
        last_cid                  : mom_id_entity.last_cid
        left                      : <SAW : Left `left` ()>
        middle                    : <SAW : Middle `middle` ()>
        pid                       : mom_id_entity.pid
        right                     : <SAW : Right `right` ()>
        type_name                 : mom_id_entity.type_name
        x_locked                  : mom_id_entity.x_locked
    <SAW : MOM.Object [mom_id_entity]>
        creation                  : <SAW : Rev_Ref `creation`>
        electric                  : mom_id_entity.electric
        last_change               : <SAW : Rev_Ref `last_change`>
        last_cid                  : mom_id_entity.last_cid
        pid                       : mom_id_entity.pid
        type_name                 : mom_id_entity.type_name
        x_locked                  : mom_id_entity.x_locked
    <SAW : Auth.Id_Entity [mom_id_entity]>
        creation                  : <SAW : Rev_Ref `creation`>
        electric                  : mom_id_entity.electric
        last_change               : <SAW : Rev_Ref `last_change`>
        last_cid                  : mom_id_entity.last_cid
        pid                       : mom_id_entity.pid
        type_name                 : mom_id_entity.type_name
        x_locked                  : mom_id_entity.x_locked
    <SAW : Auth.Object [mom_id_entity]>
        creation                  : <SAW : Rev_Ref `creation`>
        electric                  : mom_id_entity.electric
        last_change               : <SAW : Rev_Ref `last_change`>
        last_cid                  : mom_id_entity.last_cid
        pid                       : mom_id_entity.pid
        type_name                 : mom_id_entity.type_name
        x_locked                  : mom_id_entity.x_locked
    <SAW : Auth._Account_ [auth__account_ : mom_id_entity]>
        active                    : <SAW : Boolean `active`>
        creation                  : <SAW : Rev_Ref `creation`>
        electric                  : mom_id_entity.electric
        enabled                   : auth__account_.enabled
        last_change               : <SAW : Rev_Ref `last_change`>
        last_cid                  : mom_id_entity.last_cid
        name                      : auth__account_.name
        pid                       : mom_id_entity.pid
        superuser                 : auth__account_.superuser
        suspended                 : auth__account_.suspended
        type_name                 : mom_id_entity.type_name
        x_locked                  : mom_id_entity.x_locked
    <SAW : Auth.Account_Anonymous [auth_account_anonymous : auth__account_ : mom_id_entity]>
        active                    : <SAW : Boolean `active`>
        creation                  : <SAW : Rev_Ref `creation`>
        electric                  : mom_id_entity.electric
        enabled                   : auth__account_.enabled
        last_change               : <SAW : Rev_Ref `last_change`>
        last_cid                  : mom_id_entity.last_cid
        name                      : auth__account_.name
        pid                       : mom_id_entity.pid
        superuser                 : auth__account_.superuser
        suspended                 : auth__account_.suspended
        type_name                 : mom_id_entity.type_name
        x_locked                  : mom_id_entity.x_locked
    <SAW : Auth.Account [auth_account : auth__account_ : mom_id_entity]>
        _account_action_s         : <SAW : Link_Ref_List `_account_action_s`>
        _account_token_action_s   : <SAW : Link_Ref_List `_account_token_action_s`>
        account_email_verifications: <SAW : Link_Ref_List `account_email_verifications`>
        account_password_resets   : <SAW : Link_Ref_List `account_password_resets`>
        activation                : <SAW : Link_Ref `activation`>
        activations               : <SAW : Link_Ref_List `activations`>
        active                    : <SAW : Boolean `active`>
        creation                  : <SAW : Rev_Ref `creation`>
        electric                  : mom_id_entity.electric
        enabled                   : auth__account_.enabled
        group_links               : <SAW : Link_Ref_List `group_links`>
        groups                    : <SAW : Role_Ref_Set `groups`>
        last_change               : <SAW : Rev_Ref `last_change`>
        last_cid                  : mom_id_entity.last_cid
        name                      : auth__account_.name
        password                  : auth_account.password
        password_change_required  : <SAW : Link_Ref `password_change_required`>
        password_change_requireds : <SAW : Link_Ref_List `password_change_requireds`>
        person                    : <SAW : Role_Ref `person`>
        person_link               : <SAW : Link_Ref `person_link`>
        person_links              : <SAW : Link_Ref_List `person_links`>
        ph_name                   : auth_account.ph_name
        pid                       : mom_id_entity.pid
        superuser                 : auth__account_.superuser
        suspended                 : auth__account_.suspended
        type_name                 : mom_id_entity.type_name
        x_locked                  : mom_id_entity.x_locked
    <SAW : Auth.Certificate [auth_certificate : mom_id_entity]>
        alive                     : <SAW : Boolean `alive`>
        cert_id                   : auth_certificate.cert_id
        creation                  : <SAW : Rev_Ref `creation`>
        desc                      : auth_certificate.desc
        electric                  : mom_id_entity.electric
        email                     : auth_certificate.email
        last_change               : <SAW : Rev_Ref `last_change`>
        last_cid                  : mom_id_entity.last_cid
        pem                       : auth_certificate.pem
        pid                       : mom_id_entity.pid
        revocation_date           : auth_certificate.revocation_date
        type_name                 : mom_id_entity.type_name
        validity                  : <Col-Mapper for MOM.Date_Time_Interval>
            alive                 : <SAW : Boolean `validity.alive`>
            finish                : auth_certificate.validity__finish
            start                 : auth_certificate.validity__start
        validity.alive            : <SAW : Boolean `validity.alive`>
        validity.finish           : auth_certificate.validity__finish
        validity.start            : auth_certificate.validity__start
        x_locked                  : mom_id_entity.x_locked
    <SAW : Auth.Group [auth_group : mom_id_entity]>
        account_links             : <SAW : Link_Ref_List `account_links`>
        accounts                  : <SAW : Role_Ref_Set `accounts`>
        creation                  : <SAW : Rev_Ref `creation`>
        desc                      : auth_group.desc
        electric                  : mom_id_entity.electric
        last_change               : <SAW : Rev_Ref `last_change`>
        last_cid                  : mom_id_entity.last_cid
        name                      : auth_group.name
        pid                       : mom_id_entity.pid
        type_name                 : mom_id_entity.type_name
        x_locked                  : mom_id_entity.x_locked
    <SAW : Auth.Link [mom_id_entity]>
        creation                  : <SAW : Rev_Ref `creation`>
        electric                  : mom_id_entity.electric
        last_change               : <SAW : Rev_Ref `last_change`>
        last_cid                  : mom_id_entity.last_cid
        left                      : <SAW : Left `left` (Auth.Account_Activation | Auth.Account_EMail_Verification |
        pid                       : mom_id_entity.pid
        type_name                 : mom_id_entity.type_name
        x_locked                  : mom_id_entity.x_locked
    <SAW : Auth._MOM_Link_n_ [mom_id_entity]>
        creation                  : <SAW : Rev_Ref `creation`>
        electric                  : mom_id_entity.electric
        last_change               : <SAW : Rev_Ref `last_change`>
        last_cid                  : mom_id_entity.last_cid
        left                      : <SAW : Left `left` (Auth.Account_in_Group)>
        pid                       : mom_id_entity.pid
        right                     : <SAW : Right `right` (Auth.Account_in_Group)>
        type_name                 : mom_id_entity.type_name
        x_locked                  : mom_id_entity.x_locked
    <SAW : Auth.Link2 [mom_id_entity]>
        creation                  : <SAW : Rev_Ref `creation`>
        electric                  : mom_id_entity.electric
        last_change               : <SAW : Rev_Ref `last_change`>
        last_cid                  : mom_id_entity.last_cid
        left                      : <SAW : Left `left` (Auth.Account_in_Group)>
        pid                       : mom_id_entity.pid
        right                     : <SAW : Right `right` (Auth.Account_in_Group)>
        type_name                 : mom_id_entity.type_name
        x_locked                  : mom_id_entity.x_locked
    <SAW : Auth.Account_in_Group [auth_account_in_group : mom_id_entity]>
        account                   : auth_account_in_group.left
        creation                  : <SAW : Rev_Ref `creation`>
        electric                  : mom_id_entity.electric
        group                     : auth_account_in_group.right
        last_change               : <SAW : Rev_Ref `last_change`>
        last_cid                  : mom_id_entity.last_cid
        left                      : auth_account_in_group.left
        pid                       : mom_id_entity.pid
        right                     : auth_account_in_group.right
        type_name                 : mom_id_entity.type_name
        x_locked                  : mom_id_entity.x_locked
    <SAW : Auth.Link1 [mom_id_entity]>
        creation                  : <SAW : Rev_Ref `creation`>
        electric                  : mom_id_entity.electric
        last_change               : <SAW : Rev_Ref `last_change`>
        last_cid                  : mom_id_entity.last_cid
        left                      : <SAW : Left `left` (Auth.Account_Activation | Auth.Account_EMail_Verification |
        pid                       : mom_id_entity.pid
        type_name                 : mom_id_entity.type_name
        x_locked                  : mom_id_entity.x_locked
    <SAW : Auth._Account_Action_ [mom_id_entity]>
        account                   : <SAW : Account `left` (Auth.Account_Activation | Auth.Account_EMail_Verification
        creation                  : <SAW : Rev_Ref `creation`>
        electric                  : mom_id_entity.electric
        last_change               : <SAW : Rev_Ref `last_change`>
        last_cid                  : mom_id_entity.last_cid
        left                      : <SAW : Account `left` (Auth.Account_Activation | Auth.Account_EMail_Verification
        pid                       : mom_id_entity.pid
        type_name                 : mom_id_entity.type_name
        x_locked                  : mom_id_entity.x_locked
    <SAW : Auth.Account_Activation [auth_account_activation : mom_id_entity]>
        account                   : auth_account_activation.left
        creation                  : <SAW : Rev_Ref `creation`>
        electric                  : mom_id_entity.electric
        last_change               : <SAW : Rev_Ref `last_change`>
        last_cid                  : mom_id_entity.last_cid
        left                      : auth_account_activation.left
        pid                       : mom_id_entity.pid
        type_name                 : mom_id_entity.type_name
        x_locked                  : mom_id_entity.x_locked
    <SAW : Auth.Account_Password_Change_Required [auth_account_password_change_required : mom_id_entity]>
        account                   : auth_account_password_change_required.left
        creation                  : <SAW : Rev_Ref `creation`>
        electric                  : mom_id_entity.electric
        last_change               : <SAW : Rev_Ref `last_change`>
        last_cid                  : mom_id_entity.last_cid
        left                      : auth_account_password_change_required.left
        pid                       : mom_id_entity.pid
        type_name                 : mom_id_entity.type_name
        x_locked                  : mom_id_entity.x_locked
    <SAW : Auth._Account_Token_Action_ [mom_id_entity]>
        account                   : <SAW : Account `left` (Auth.Account_EMail_Verification | Auth.Account_Password_R
        creation                  : <SAW : Rev_Ref `creation`>
        electric                  : mom_id_entity.electric
        expires                   : <SAW : Date-Time `expires` (Auth.Account_EMail_Verification | Auth.Account_Passw
        last_change               : <SAW : Rev_Ref `last_change`>
        last_cid                  : mom_id_entity.last_cid
        left                      : <SAW : Account `left` (Auth.Account_EMail_Verification | Auth.Account_Password_R
        pid                       : mom_id_entity.pid
        token                     : <SAW : String `token` (Auth.Account_EMail_Verification | Auth.Account_Password_R
        type_name                 : mom_id_entity.type_name
        x_locked                  : mom_id_entity.x_locked
    <SAW : Auth.Account_EMail_Verification [auth_account_email_verification : mom_id_entity]>
        account                   : auth_account_email_verification.left
        creation                  : <SAW : Rev_Ref `creation`>
        electric                  : mom_id_entity.electric
        expires                   : auth_account_email_verification.expires
        last_change               : <SAW : Rev_Ref `last_change`>
        last_cid                  : mom_id_entity.last_cid
        left                      : auth_account_email_verification.left
        new_email                 : auth_account_email_verification.new_email
        pid                       : mom_id_entity.pid
        token                     : auth_account_email_verification.token
        type_name                 : mom_id_entity.type_name
        x_locked                  : mom_id_entity.x_locked
    <SAW : Auth.Account_Password_Reset [auth_account_password_reset : mom_id_entity]>
        account                   : auth_account_password_reset.left
        creation                  : <SAW : Rev_Ref `creation`>
        electric                  : mom_id_entity.electric
        expires                   : auth_account_password_reset.expires
        last_change               : <SAW : Rev_Ref `last_change`>
        last_cid                  : mom_id_entity.last_cid
        left                      : auth_account_password_reset.left
        password                  : auth_account_password_reset.password
        pid                       : mom_id_entity.pid
        token                     : auth_account_password_reset.token
        type_name                 : mom_id_entity.type_name
        x_locked                  : mom_id_entity.x_locked
    <SAW : EVT.Id_Entity [mom_id_entity]>
        creation                  : <SAW : Rev_Ref `creation`>
        electric                  : mom_id_entity.electric
        last_change               : <SAW : Rev_Ref `last_change`>
        last_cid                  : mom_id_entity.last_cid
        pid                       : mom_id_entity.pid
        type_name                 : mom_id_entity.type_name
        x_locked                  : mom_id_entity.x_locked
    <SAW : EVT.Object [mom_id_entity]>
        creation                  : <SAW : Rev_Ref `creation`>
        electric                  : mom_id_entity.electric
        last_change               : <SAW : Rev_Ref `last_change`>
        last_cid                  : mom_id_entity.last_cid
        pid                       : mom_id_entity.pid
        type_name                 : mom_id_entity.type_name
        x_locked                  : mom_id_entity.x_locked
    <SAW : EVT.Calendar [evt_calendar : mom_id_entity]>
        creation                  : <SAW : Rev_Ref `creation`>
        desc                      : evt_calendar.desc
        electric                  : mom_id_entity.electric
        last_change               : <SAW : Rev_Ref `last_change`>
        last_cid                  : mom_id_entity.last_cid
        name                      : evt_calendar.name
        pid                       : mom_id_entity.pid
        type_name                 : mom_id_entity.type_name
        x_locked                  : mom_id_entity.x_locked
    <SAW : EVT.Link [mom_id_entity]>
        creation                  : <SAW : Rev_Ref `creation`>
        electric                  : mom_id_entity.electric
        last_change               : <SAW : Rev_Ref `last_change`>
        last_cid                  : mom_id_entity.last_cid
        left                      : <SAW : Left `left` (EVT.Event | EVT.Event_occurs | EVT.Recurrence_Rule | EVT.Rec
        pid                       : mom_id_entity.pid
        type_name                 : mom_id_entity.type_name
        x_locked                  : mom_id_entity.x_locked
    <SAW : EVT.Link1 [mom_id_entity]>
        creation                  : <SAW : Rev_Ref `creation`>
        electric                  : mom_id_entity.electric
        last_change               : <SAW : Rev_Ref `last_change`>
        last_cid                  : mom_id_entity.last_cid
        left                      : <SAW : Left `left` (EVT.Event | EVT.Event_occurs | EVT.Recurrence_Rule | EVT.Rec
        pid                       : mom_id_entity.pid
        type_name                 : mom_id_entity.type_name
        x_locked                  : mom_id_entity.x_locked
    <SAW : SWP.Id_Entity [mom_id_entity]>
        creation                  : <SAW : Rev_Ref `creation`>
        electric                  : mom_id_entity.electric
        last_change               : <SAW : Rev_Ref `last_change`>
        last_cid                  : mom_id_entity.last_cid
        pid                       : mom_id_entity.pid
        type_name                 : mom_id_entity.type_name
        x_locked                  : mom_id_entity.x_locked
    <SAW : SWP.Object [mom_id_entity]>
        creation                  : <SAW : Rev_Ref `creation`>
        electric                  : mom_id_entity.electric
        last_change               : <SAW : Rev_Ref `last_change`>
        last_cid                  : mom_id_entity.last_cid
        pid                       : mom_id_entity.pid
        type_name                 : mom_id_entity.type_name
        x_locked                  : mom_id_entity.x_locked
    <SAW : SWP.Object_PN [mom_id_entity]>
        clips                     : <SAW : Link_Ref_List `clips`>
        creation                  : <SAW : Rev_Ref `creation`>
        date                      : <SAW : Date_Interval `date` (SWP.Gallery | SWP.Page)>
        electric                  : mom_id_entity.electric
        last_change               : <SAW : Rev_Ref `last_change`>
        last_cid                  : mom_id_entity.last_cid
        perma_name                : <SAW : Date-Slug `perma_name` (SWP.Gallery | SWP.Page)>
        pid                       : mom_id_entity.pid
        short_title               : <SAW : String `short_title` (SWP.Gallery | SWP.Page)>
        title                     : <SAW : String `title` (SWP.Gallery | SWP.Page)>
        type_name                 : mom_id_entity.type_name
        x_locked                  : mom_id_entity.x_locked
    <SAW : SWP.Page [swp_page : mom_id_entity]>
        clips                     : <SAW : Link_Ref_List `clips`>
        contents                  : swp_page.contents
        creation                  : <SAW : Rev_Ref `creation`>
        date                      : <Col-Mapper for MOM.Date_Interval_N>
            alive                 : <SAW : Boolean `date.alive`>
            finish                : swp_page.date__finish
            start                 : swp_page.date__start
        date.alive                : <SAW : Boolean `date.alive`>
        date.finish               : swp_page.date__finish
        date.start                : swp_page.date__start
        electric                  : mom_id_entity.electric
        events                    : <SAW : Link_Ref_List `events`>
        format                    : swp_page.format
        head_line                 : swp_page.head_line
        hidden                    : swp_page.hidden
        last_change               : <SAW : Rev_Ref `last_change`>
        last_cid                  : mom_id_entity.last_cid
        perma_name                : swp_page.perma_name
        pid                       : mom_id_entity.pid
        prio                      : swp_page.prio
        short_title               : swp_page.short_title
        text                      : swp_page.text
        title                     : swp_page.title
        type_name                 : mom_id_entity.type_name
        x_locked                  : mom_id_entity.x_locked
    <SAW : SWP.Page_Y [swp_page_y : swp_page : mom_id_entity]>
        clips                     : <SAW : Link_Ref_List `clips`>
        contents                  : swp_page.contents
        creation                  : <SAW : Rev_Ref `creation`>
        date                      : <Col-Mapper for MOM.Date_Interval_N>
            alive                 : <SAW : Boolean `date.alive`>
            finish                : swp_page.date__finish
            start                 : swp_page.date__start
        date.alive                : <SAW : Boolean `date.alive`>
        date.finish               : swp_page.date__finish
        date.start                : swp_page.date__start
        electric                  : mom_id_entity.electric
        events                    : <SAW : Link_Ref_List `events`>
        format                    : swp_page.format
        head_line                 : swp_page.head_line
        hidden                    : swp_page.hidden
        last_change               : <SAW : Rev_Ref `last_change`>
        last_cid                  : mom_id_entity.last_cid
        perma_name                : swp_page.perma_name
        pid                       : mom_id_entity.pid
        prio                      : swp_page.prio
        short_title               : swp_page.short_title
        text                      : swp_page.text
        title                     : swp_page.title
        type_name                 : mom_id_entity.type_name
        x_locked                  : mom_id_entity.x_locked
        year                      : swp_page_y.year
    <SAW : EVT.Event [evt_event : mom_id_entity]>
        calendar                  : evt_event.calendar
        creation                  : <SAW : Rev_Ref `creation`>
        date                      : <Col-Mapper for MOM.Date_Interval>
            alive                 : <SAW : Boolean `date.alive`>
            finish                : evt_event.date__finish
            start                 : evt_event.date__start
        date.alive                : <SAW : Boolean `date.alive`>
        date.finish               : evt_event.date__finish
        date.start                : evt_event.date__start
        detail                    : evt_event.detail
        electric                  : mom_id_entity.electric
        last_change               : <SAW : Rev_Ref `last_change`>
        last_cid                  : mom_id_entity.last_cid
        left                      : evt_event.left
        object                    : evt_event.left
        occurs                    : <SAW : Link_Ref_List `occurs`>
        pid                       : mom_id_entity.pid
        recurrence                : <SAW : Link_Ref `recurrence`>
        short_title               : evt_event.short_title
        time                      : <Col-Mapper for MOM.Time_Interval>
            finish                : evt_event.time__finish
            start                 : evt_event.time__start
        time.finish               : evt_event.time__finish
        time.start                : evt_event.time__start
        type_name                 : mom_id_entity.type_name
        x_locked                  : mom_id_entity.x_locked
    <SAW : EVT.Event_occurs [evt_event_occurs : mom_id_entity]>
        creation                  : <SAW : Rev_Ref `creation`>
        date                      : evt_event_occurs.date
        electric                  : mom_id_entity.electric
        event                     : evt_event_occurs.left
        last_change               : <SAW : Rev_Ref `last_change`>
        last_cid                  : mom_id_entity.last_cid
        left                      : evt_event_occurs.left
        pid                       : mom_id_entity.pid
        time                      : <Col-Mapper for MOM.Time_Interval>
            finish                : evt_event_occurs.time__finish
            start                 : evt_event_occurs.time__start
        time.finish               : evt_event_occurs.time__finish
        time.start                : evt_event_occurs.time__start
        type_name                 : mom_id_entity.type_name
        x_locked                  : mom_id_entity.x_locked
    <SAW : EVT._Recurrence_Mixin_ [mom_id_entity]>
        creation                  : <SAW : Rev_Ref `creation`>
        electric                  : mom_id_entity.electric
        last_change               : <SAW : Rev_Ref `last_change`>
        last_cid                  : mom_id_entity.last_cid
        left                      : <SAW : Left `left` (EVT.Recurrence_Rule | EVT.Recurrence_Spec)>
        pid                       : mom_id_entity.pid
        type_name                 : mom_id_entity.type_name
        x_locked                  : mom_id_entity.x_locked
    <SAW : EVT.Recurrence_Spec [evt_recurrence_spec : mom_id_entity]>
        creation                  : <SAW : Rev_Ref `creation`>
        date_exceptions           : evt_recurrence_spec.date_exceptions
        dates                     : evt_recurrence_spec.dates
        electric                  : mom_id_entity.electric
        event                     : evt_recurrence_spec.left
        last_change               : <SAW : Rev_Ref `last_change`>
        last_cid                  : mom_id_entity.last_cid
        left                      : evt_recurrence_spec.left
        pid                       : mom_id_entity.pid
        rules                     : <SAW : Link_Ref_List `rules`>
        type_name                 : mom_id_entity.type_name
        x_locked                  : mom_id_entity.x_locked
    <SAW : EVT.Recurrence_Rule [evt_recurrence_rule : mom_id_entity]>
        count                     : evt_recurrence_rule.count
        creation                  : <SAW : Rev_Ref `creation`>
        desc                      : evt_recurrence_rule.desc
        easter_offset             : evt_recurrence_rule.easter_offset
        electric                  : mom_id_entity.electric
        finish                    : evt_recurrence_rule.finish
        is_exception              : evt_recurrence_rule.is_exception
        last_change               : <SAW : Rev_Ref `last_change`>
        last_cid                  : mom_id_entity.last_cid
        left                      : evt_recurrence_rule.left
        month                     : evt_recurrence_rule.month
        month_day                 : evt_recurrence_rule.month_day
        period                    : evt_recurrence_rule.period
        pid                       : mom_id_entity.pid
        recurrence_spec           : evt_recurrence_rule.left
        restrict_pos              : evt_recurrence_rule.restrict_pos
        start                     : evt_recurrence_rule.start
        type_name                 : mom_id_entity.type_name
        unit                      : evt_recurrence_rule.unit
        week                      : evt_recurrence_rule.week
        week_day                  : evt_recurrence_rule.week_day
        x_locked                  : mom_id_entity.x_locked
        year_day                  : evt_recurrence_rule.year_day
    <SAW : PAP.Id_Entity [mom_id_entity]>
        creation                  : <SAW : Rev_Ref `creation`>
        electric                  : mom_id_entity.electric
        last_change               : <SAW : Rev_Ref `last_change`>
        last_cid                  : mom_id_entity.last_cid
        pid                       : mom_id_entity.pid
        type_name                 : mom_id_entity.type_name
        x_locked                  : mom_id_entity.x_locked
    <SAW : PAP.Object [mom_id_entity]>
        creation                  : <SAW : Rev_Ref `creation`>
        electric                  : mom_id_entity.electric
        last_change               : <SAW : Rev_Ref `last_change`>
        last_cid                  : mom_id_entity.last_cid
        pid                       : mom_id_entity.pid
        type_name                 : mom_id_entity.type_name
        x_locked                  : mom_id_entity.x_locked
    <SAW : PAP.Property [mom_id_entity]>
        creation                  : <SAW : Rev_Ref `creation`>
        desc                      : <SAW : String `desc` (PAP.Address | PAP.Email | PAP.Phone | PAP.Url)>
        electric                  : mom_id_entity.electric
        last_change               : <SAW : Rev_Ref `last_change`>
        last_cid                  : mom_id_entity.last_cid
        pid                       : mom_id_entity.pid
        subject_links             : <SAW : Link_Ref_List `subject_links`>
        type_name                 : mom_id_entity.type_name
        x_locked                  : mom_id_entity.x_locked
    <SAW : PAP.Address [pap_address : mom_id_entity]>
        __raw_city                : pap_address.__raw_city
        __raw_country             : pap_address.__raw_country
        __raw_region              : pap_address.__raw_region
        __raw_street              : pap_address.__raw_street
        __raw_zip                 : pap_address.__raw_zip
        city                      : pap_address.city
        companies                 : <SAW : Role_Ref_Set `companies`>
        company_links             : <SAW : Link_Ref_List `company_links`>
        country                   : pap_address.country
        creation                  : <SAW : Rev_Ref `creation`>
        desc                      : pap_address.desc
        electric                  : mom_id_entity.electric
        gps                       : <SAW : Link_Ref `gps`>
        last_change               : <SAW : Rev_Ref `last_change`>
        last_cid                  : mom_id_entity.last_cid
        person_links              : <SAW : Link_Ref_List `person_links`>
        persons                   : <SAW : Role_Ref_Set `persons`>
        pid                       : mom_id_entity.pid
        region                    : pap_address.region
        street                    : pap_address.street
        subject_links             : <SAW : Link_Ref_List `subject_links`>
        type_name                 : mom_id_entity.type_name
        x_locked                  : mom_id_entity.x_locked
        zip                       : pap_address.zip
    <SAW : PAP.Subject [mom_id_entity]>
        address_links             : <SAW : Link_Ref_List `address_links`>
        addresses                 : <SAW : Role_Ref_Set `addresses`>
        creation                  : <SAW : Rev_Ref `creation`>
        electric                  : mom_id_entity.electric
        email_links               : <SAW : Link_Ref_List `email_links`>
        emails                    : <SAW : Role_Ref_Set `emails`>
        last_change               : <SAW : Rev_Ref `last_change`>
        last_cid                  : mom_id_entity.last_cid
        lifetime                  : <SAW : Date_Interval `lifetime` (PAP.Company | PAP.Person)>
        phone_links               : <SAW : Link_Ref_List `phone_links`>
        phones                    : <SAW : Role_Ref_Set `phones`>
        pid                       : mom_id_entity.pid
        property_links            : <SAW : Link_Ref_List `property_links`>
        type_name                 : mom_id_entity.type_name
        url_links                 : <SAW : Link_Ref_List `url_links`>
        urls                      : <SAW : Role_Ref_Set `urls`>
        x_locked                  : mom_id_entity.x_locked
    <SAW : PAP.Legal_Entity [mom_id_entity]>
        address_links             : <SAW : Link_Ref_List `address_links`>
        addresses                 : <SAW : Role_Ref_Set `addresses`>
        creation                  : <SAW : Rev_Ref `creation`>
        electric                  : mom_id_entity.electric
        email_links               : <SAW : Link_Ref_List `email_links`>
        emails                    : <SAW : Role_Ref_Set `emails`>
        last_change               : <SAW : Rev_Ref `last_change`>
        last_cid                  : mom_id_entity.last_cid
        lifetime                  : <SAW : Date_Interval `lifetime` (PAP.Company)>
        name                      : <SAW : String `name` (PAP.Company)>
        phone_links               : <SAW : Link_Ref_List `phone_links`>
        phones                    : <SAW : Role_Ref_Set `phones`>
        pid                       : mom_id_entity.pid
        property_links            : <SAW : Link_Ref_List `property_links`>
        short_name                : <SAW : String `short_name` (PAP.Company)>
        type_name                 : mom_id_entity.type_name
        url_links                 : <SAW : Link_Ref_List `url_links`>
        urls                      : <SAW : Role_Ref_Set `urls`>
        x_locked                  : mom_id_entity.x_locked
    <SAW : PAP.Company [pap_company : mom_id_entity]>
        __raw_name                : pap_company.__raw_name
        __raw_registered_in       : pap_company.__raw_registered_in
        __raw_short_name          : pap_company.__raw_short_name
        address_links             : <SAW : Link_Ref_List `address_links`>
        addresses                 : <SAW : Role_Ref_Set `addresses`>
        creation                  : <SAW : Rev_Ref `creation`>
        electric                  : mom_id_entity.electric
        email_links               : <SAW : Link_Ref_List `email_links`>
        emails                    : <SAW : Role_Ref_Set `emails`>
        last_change               : <SAW : Rev_Ref `last_change`>
        last_cid                  : mom_id_entity.last_cid
        lifetime                  : <Col-Mapper for MOM.Date_Interval>
            alive                 : <SAW : Boolean `lifetime.alive`>
            finish                : pap_company.lifetime__finish
            start                 : pap_company.lifetime__start
        lifetime.alive            : <SAW : Boolean `lifetime.alive`>
        lifetime.finish           : pap_company.lifetime__finish
        lifetime.start            : pap_company.lifetime__start
        name                      : pap_company.name
        phone_links               : <SAW : Link_Ref_List `phone_links`>
        phones                    : <SAW : Role_Ref_Set `phones`>
        pid                       : mom_id_entity.pid
        property_links            : <SAW : Link_Ref_List `property_links`>
        registered_in             : pap_company.registered_in
        short_name                : pap_company.short_name
        type_name                 : mom_id_entity.type_name
        url_links                 : <SAW : Link_Ref_List `url_links`>
        urls                      : <SAW : Role_Ref_Set `urls`>
        x_locked                  : mom_id_entity.x_locked
    <SAW : PAP.Email [pap_email : mom_id_entity]>
        __raw_address             : pap_email.__raw_address
        address                   : pap_email.address
        companies                 : <SAW : Role_Ref_Set `companies`>
        company_links             : <SAW : Link_Ref_List `company_links`>
        creation                  : <SAW : Rev_Ref `creation`>
        desc                      : pap_email.desc
        electric                  : mom_id_entity.electric
        last_change               : <SAW : Rev_Ref `last_change`>
        last_cid                  : mom_id_entity.last_cid
        person_links              : <SAW : Link_Ref_List `person_links`>
        persons                   : <SAW : Role_Ref_Set `persons`>
        pid                       : mom_id_entity.pid
        subject_links             : <SAW : Link_Ref_List `subject_links`>
        type_name                 : mom_id_entity.type_name
        x_locked                  : mom_id_entity.x_locked
    <SAW : PAP.Phone [pap_phone : mom_id_entity]>
        area_code                 : pap_phone.area_code
        companies                 : <SAW : Role_Ref_Set `companies`>
        company_links             : <SAW : Link_Ref_List `company_links`>
        country_code              : pap_phone.country_code
        creation                  : <SAW : Rev_Ref `creation`>
        desc                      : pap_phone.desc
        electric                  : mom_id_entity.electric
        last_change               : <SAW : Rev_Ref `last_change`>
        last_cid                  : mom_id_entity.last_cid
        number                    : pap_phone.number
        person_links              : <SAW : Link_Ref_List `person_links`>
        persons                   : <SAW : Role_Ref_Set `persons`>
        pid                       : mom_id_entity.pid
        subject_links             : <SAW : Link_Ref_List `subject_links`>
        type_name                 : mom_id_entity.type_name
        x_locked                  : mom_id_entity.x_locked
    <SAW : PAP.Person [pap_person : mom_id_entity]>
        __raw_first_name          : pap_person.__raw_first_name
        __raw_last_name           : pap_person.__raw_last_name
        __raw_middle_name         : pap_person.__raw_middle_name
        __raw_title               : pap_person.__raw_title
        account_links             : <SAW : Link_Ref_List `account_links`>
        accounts                  : <SAW : Role_Ref_Set `accounts`>
        address_links             : <SAW : Link_Ref_List `address_links`>
        addresses                 : <SAW : Role_Ref_Set `addresses`>
        creation                  : <SAW : Rev_Ref `creation`>
        electric                  : mom_id_entity.electric
        email_links               : <SAW : Link_Ref_List `email_links`>
        emails                    : <SAW : Role_Ref_Set `emails`>
        first_name                : pap_person.first_name
        last_change               : <SAW : Rev_Ref `last_change`>
        last_cid                  : mom_id_entity.last_cid
        last_name                 : pap_person.last_name
        lifetime                  : <Col-Mapper for MOM.Date_Interval>
            alive                 : <SAW : Boolean `lifetime.alive`>
            finish                : pap_person.lifetime__finish
            start                 : pap_person.lifetime__start
        lifetime.alive            : <SAW : Boolean `lifetime.alive`>
        lifetime.finish           : pap_person.lifetime__finish
        lifetime.start            : pap_person.lifetime__start
        middle_name               : pap_person.middle_name
        phone_links               : <SAW : Link_Ref_List `phone_links`>
        phones                    : <SAW : Role_Ref_Set `phones`>
        pid                       : mom_id_entity.pid
        property_links            : <SAW : Link_Ref_List `property_links`>
        sailors                   : <SAW : Link_Ref_List `sailors`>
        sex                       : pap_person.sex
        title                     : pap_person.title
        type_name                 : mom_id_entity.type_name
        url_links                 : <SAW : Link_Ref_List `url_links`>
        urls                      : <SAW : Role_Ref_Set `urls`>
        x_locked                  : mom_id_entity.x_locked
    <SAW : PAP.Url [pap_url : mom_id_entity]>
        companies                 : <SAW : Role_Ref_Set `companies`>
        company_links             : <SAW : Link_Ref_List `company_links`>
        creation                  : <SAW : Rev_Ref `creation`>
        desc                      : pap_url.desc
        electric                  : mom_id_entity.electric
        last_change               : <SAW : Rev_Ref `last_change`>
        last_cid                  : mom_id_entity.last_cid
        person_links              : <SAW : Link_Ref_List `person_links`>
        persons                   : <SAW : Role_Ref_Set `persons`>
        pid                       : mom_id_entity.pid
        subject_links             : <SAW : Link_Ref_List `subject_links`>
        type_name                 : mom_id_entity.type_name
        value                     : pap_url.value
        x_locked                  : mom_id_entity.x_locked
    <SAW : PAP.Link [mom_id_entity]>
        creation                  : <SAW : Rev_Ref `creation`>
        electric                  : mom_id_entity.electric
        last_change               : <SAW : Rev_Ref `last_change`>
        last_cid                  : mom_id_entity.last_cid
        left                      : <SAW : Left `left` (PAP.Address_Position | PAP.Person_has_Account | PAP.Subject_
        pid                       : mom_id_entity.pid
        type_name                 : mom_id_entity.type_name
        x_locked                  : mom_id_entity.x_locked
    <SAW : PAP.Link1 [mom_id_entity]>
        creation                  : <SAW : Rev_Ref `creation`>
        electric                  : mom_id_entity.electric
        last_change               : <SAW : Rev_Ref `last_change`>
        last_cid                  : mom_id_entity.last_cid
        left                      : <SAW : Left `left` (PAP.Address_Position)>
        pid                       : mom_id_entity.pid
        type_name                 : mom_id_entity.type_name
        x_locked                  : mom_id_entity.x_locked
    <SAW : PAP.Address_Position [pap_address_position : mom_id_entity]>
        address                   : pap_address_position.left
        creation                  : <SAW : Rev_Ref `creation`>
        electric                  : mom_id_entity.electric
        last_change               : <SAW : Rev_Ref `last_change`>
        last_cid                  : mom_id_entity.last_cid
        left                      : pap_address_position.left
        pid                       : mom_id_entity.pid
        position                  : <Col-Mapper for MOM.Position>
            ___raw_lat            : pap_address_position.position____raw_lat
            ___raw_lon            : pap_address_position.position____raw_lon
            height                : pap_address_position.position__height
            lat                   : pap_address_position.position__lat
            lon                   : pap_address_position.position__lon
        position.height           : pap_address_position.position__height
        position.lat              : pap_address_position.position__lat
        position.lon              : pap_address_position.position__lon
        position____raw_lat       : pap_address_position.position____raw_lat
        position____raw_lon       : pap_address_position.position____raw_lon
        type_name                 : mom_id_entity.type_name
        x_locked                  : mom_id_entity.x_locked
    <SAW : PAP._MOM_Link_n_ [mom_id_entity]>
        creation                  : <SAW : Rev_Ref `creation`>
        electric                  : mom_id_entity.electric
        last_change               : <SAW : Rev_Ref `last_change`>
        last_cid                  : mom_id_entity.last_cid
        left                      : <SAW : Left `left` (PAP.Person_has_Account | PAP.Subject_has_Property)>
        pid                       : mom_id_entity.pid
        right                     : <SAW : Right `right` (PAP.Person_has_Account | PAP.Subject_has_Property)>
        type_name                 : mom_id_entity.type_name
        x_locked                  : mom_id_entity.x_locked
    <SAW : PAP.Link2 [mom_id_entity]>
        creation                  : <SAW : Rev_Ref `creation`>
        electric                  : mom_id_entity.electric
        last_change               : <SAW : Rev_Ref `last_change`>
        last_cid                  : mom_id_entity.last_cid
        left                      : <SAW : Left `left` (PAP.Person_has_Account | PAP.Subject_has_Property)>
        pid                       : mom_id_entity.pid
        right                     : <SAW : Right `right` (PAP.Person_has_Account | PAP.Subject_has_Property)>
        type_name                 : mom_id_entity.type_name
        x_locked                  : mom_id_entity.x_locked
    <SAW : PAP.Subject_has_Property [pap_subject_has_property : mom_id_entity]>
        creation                  : <SAW : Rev_Ref `creation`>
        desc                      : pap_subject_has_property.desc
        electric                  : mom_id_entity.electric
        last_change               : <SAW : Rev_Ref `last_change`>
        last_cid                  : mom_id_entity.last_cid
        left                      : pap_subject_has_property.left
        pid                       : mom_id_entity.pid
        property                  : pap_subject_has_property.right
        right                     : pap_subject_has_property.right
        subject                   : pap_subject_has_property.left
        type_name                 : mom_id_entity.type_name
        x_locked                  : mom_id_entity.x_locked
    <SAW : PAP.Person_has_Account [pap_person_has_account : mom_id_entity]>
        account                   : pap_person_has_account.right
        creation                  : <SAW : Rev_Ref `creation`>
        electric                  : mom_id_entity.electric
        last_change               : <SAW : Rev_Ref `last_change`>
        last_cid                  : mom_id_entity.last_cid
        left                      : pap_person_has_account.left
        person                    : pap_person_has_account.left
        pid                       : mom_id_entity.pid
        right                     : pap_person_has_account.right
        type_name                 : mom_id_entity.type_name
        x_locked                  : mom_id_entity.x_locked
    <SAW : SRM.Id_Entity [mom_id_entity]>
        creation                  : <SAW : Rev_Ref `creation`>
        electric                  : mom_id_entity.electric
        last_change               : <SAW : Rev_Ref `last_change`>
        last_cid                  : mom_id_entity.last_cid
        pid                       : mom_id_entity.pid
        type_name                 : mom_id_entity.type_name
        x_locked                  : mom_id_entity.x_locked
    <SAW : SRM.Object [mom_id_entity]>
        creation                  : <SAW : Rev_Ref `creation`>
        electric                  : mom_id_entity.electric
        last_change               : <SAW : Rev_Ref `last_change`>
        last_cid                  : mom_id_entity.last_cid
        pid                       : mom_id_entity.pid
        type_name                 : mom_id_entity.type_name
        x_locked                  : mom_id_entity.x_locked
    <SAW : SRM._Boat_Class_ [srm__boat_class_ : mom_id_entity]>
        __raw_name                : srm__boat_class_.__raw_name
        creation                  : <SAW : Rev_Ref `creation`>
        electric                  : mom_id_entity.electric
        last_change               : <SAW : Rev_Ref `last_change`>
        last_cid                  : mom_id_entity.last_cid
        name                      : srm__boat_class_.name
        pid                       : mom_id_entity.pid
        type_name                 : mom_id_entity.type_name
        x_locked                  : mom_id_entity.x_locked
    <SAW : SRM.Boat_Class [srm_boat_class : srm__boat_class_ : mom_id_entity]>
        __raw_name                : srm__boat_class_.__raw_name
        beam                      : srm_boat_class.beam
        boats                     : <SAW : Link_Ref_List `boats`>
        creation                  : <SAW : Rev_Ref `creation`>
        electric                  : mom_id_entity.electric
        last_change               : <SAW : Rev_Ref `last_change`>
        last_cid                  : mom_id_entity.last_cid
        loa                       : srm_boat_class.loa
        max_crew                  : srm_boat_class.max_crew
        name                      : srm__boat_class_.name
        pid                       : mom_id_entity.pid
        sail_area                 : srm_boat_class.sail_area
        type_name                 : mom_id_entity.type_name
        x_locked                  : mom_id_entity.x_locked
    <SAW : SRM.Handicap [srm_handicap : srm__boat_class_ : mom_id_entity]>
        __raw_name                : srm__boat_class_.__raw_name
        creation                  : <SAW : Rev_Ref `creation`>
        electric                  : mom_id_entity.electric
        last_change               : <SAW : Rev_Ref `last_change`>
        last_cid                  : mom_id_entity.last_cid
        name                      : srm__boat_class_.name
        pid                       : mom_id_entity.pid
        type_name                 : mom_id_entity.type_name
        x_locked                  : mom_id_entity.x_locked
    <SAW : SRM.Link [mom_id_entity]>
        creation                  : <SAW : Rev_Ref `creation`>
        electric                  : mom_id_entity.electric
        last_change               : <SAW : Rev_Ref `last_change`>
        last_cid                  : mom_id_entity.last_cid
        left                      : <SAW : Left `left` (SRM.Boat | SRM.Boat_in_Regatta | SRM.Crew_Member | SRM.Race_
        pid                       : mom_id_entity.pid
        type_name                 : mom_id_entity.type_name
        x_locked                  : mom_id_entity.x_locked
    <SAW : SRM.Link1 [mom_id_entity]>
        creation                  : <SAW : Rev_Ref `creation`>
        electric                  : mom_id_entity.electric
        last_change               : <SAW : Rev_Ref `last_change`>
        last_cid                  : mom_id_entity.last_cid
        left                      : <SAW : Left `left` (SRM.Boat | SRM.Race_Result | SRM.Regatta | SRM.Sailor | SRM.
        pid                       : mom_id_entity.pid
        type_name                 : mom_id_entity.type_name
        x_locked                  : mom_id_entity.x_locked
    <SAW : SRM.Boat [srm_boat : mom_id_entity]>
        __raw_sail_number         : srm_boat.__raw_sail_number
        __raw_sail_number_x       : srm_boat.__raw_sail_number_x
        b_class                   : srm_boat.left
        creation                  : <SAW : Rev_Ref `creation`>
        electric                  : mom_id_entity.electric
        last_change               : <SAW : Rev_Ref `last_change`>
        last_cid                  : mom_id_entity.last_cid
        left                      : srm_boat.left
        name                      : srm_boat.name
        nation                    : srm_boat.nation
        pid                       : mom_id_entity.pid
        regatta_links             : <SAW : Link_Ref_List `regatta_links`>
        sail_number               : srm_boat.sail_number
        sail_number_x             : srm_boat.sail_number_x
        type_name                 : mom_id_entity.type_name
        x_locked                  : mom_id_entity.x_locked
    <SAW : SRM.Club [srm_club : mom_id_entity]>
        __raw_name                : srm_club.__raw_name
        creation                  : <SAW : Rev_Ref `creation`>
        electric                  : mom_id_entity.electric
        last_change               : <SAW : Rev_Ref `last_change`>
        last_cid                  : mom_id_entity.last_cid
        long_name                 : srm_club.long_name
        name                      : srm_club.name
        pid                       : mom_id_entity.pid
        type_name                 : mom_id_entity.type_name
        x_locked                  : mom_id_entity.x_locked
    <SAW : SRM.Regatta_Event [srm_regatta_event : mom_id_entity]>
        __raw_name                : srm_regatta_event.__raw_name
        club                      : srm_regatta_event.club
        creation                  : <SAW : Rev_Ref `creation`>
        date                      : <Col-Mapper for MOM.Date_Interval_C>
            alive                 : <SAW : Boolean `date.alive`>
            finish                : srm_regatta_event.date__finish
            start                 : srm_regatta_event.date__start
        date.alive                : <SAW : Boolean `date.alive`>
        date.finish               : srm_regatta_event.date__finish
        date.start                : srm_regatta_event.date__start
        desc                      : srm_regatta_event.desc
        electric                  : mom_id_entity.electric
        is_cancelled              : srm_regatta_event.is_cancelled
        last_change               : <SAW : Rev_Ref `last_change`>
        last_cid                  : mom_id_entity.last_cid
        name                      : srm_regatta_event.name
        perma_name                : srm_regatta_event.perma_name
        pid                       : mom_id_entity.pid
        regattas                  : <SAW : Link_Ref_List `regattas`>
        type_name                 : mom_id_entity.type_name
        x_locked                  : mom_id_entity.x_locked
        year                      : <SAW : Int `year`>
    <SAW : SWP.Link [mom_id_entity]>
        creation                  : <SAW : Rev_Ref `creation`>
        electric                  : mom_id_entity.electric
        last_change               : <SAW : Rev_Ref `last_change`>
        last_cid                  : mom_id_entity.last_cid
        left                      : <SAW : Left `left` (SWP.Clip_O | SWP.Picture)>
        pid                       : mom_id_entity.pid
        type_name                 : mom_id_entity.type_name
        x_locked                  : mom_id_entity.x_locked
    <SAW : SWP.Link1 [mom_id_entity]>
        creation                  : <SAW : Rev_Ref `creation`>
        electric                  : mom_id_entity.electric
        last_change               : <SAW : Rev_Ref `last_change`>
        last_cid                  : mom_id_entity.last_cid
        left                      : <SAW : Left `left` (SWP.Clip_O | SWP.Picture)>
        pid                       : mom_id_entity.pid
        type_name                 : mom_id_entity.type_name
        x_locked                  : mom_id_entity.x_locked
    <SAW : SWP.Clip_O [swp_clip_o : mom_id_entity]>
        abstract                  : swp_clip_o.abstract
        contents                  : swp_clip_o.contents
        creation                  : <SAW : Rev_Ref `creation`>
        date                      : <Col-Mapper for MOM.Date_Interval>
            alive                 : <SAW : Boolean `date.alive`>
            finish                : swp_clip_o.date__finish
            start                 : swp_clip_o.date__start
        date.alive                : <SAW : Boolean `date.alive`>
        date.finish               : swp_clip_o.date__finish
        date.start                : swp_clip_o.date__start
        date_x                    : <Col-Mapper for MOM.Date_Interval>
            alive                 : <SAW : Boolean `date_x.alive`>
            finish                : swp_clip_o.date_x__finish
            start                 : swp_clip_o.date_x__start
        date_x.alive              : <SAW : Boolean `date_x.alive`>
        date_x.finish             : swp_clip_o.date_x__finish
        date_x.start              : swp_clip_o.date_x__start
        electric                  : mom_id_entity.electric
        last_change               : <SAW : Rev_Ref `last_change`>
        last_cid                  : mom_id_entity.last_cid
        left                      : swp_clip_o.left
        object                    : swp_clip_o.left
        pid                       : mom_id_entity.pid
        prio                      : swp_clip_o.prio
        type_name                 : mom_id_entity.type_name
        x_locked                  : mom_id_entity.x_locked
    <SAW : SWP.Clip_X [swp_clip_x : swp_page : mom_id_entity]>
        clips                     : <SAW : Link_Ref_List `clips`>
        contents                  : swp_page.contents
        creation                  : <SAW : Rev_Ref `creation`>
        date                      : <Col-Mapper for MOM.Date_Interval_N>
            alive                 : <SAW : Boolean `date.alive`>
            finish                : swp_page.date__finish
            start                 : swp_page.date__start
        date.alive                : <SAW : Boolean `date.alive`>
        date.finish               : swp_page.date__finish
        date.start                : swp_page.date__start
        electric                  : mom_id_entity.electric
        events                    : <SAW : Link_Ref_List `events`>
        format                    : swp_page.format
        head_line                 : swp_page.head_line
        hidden                    : swp_page.hidden
        last_change               : <SAW : Rev_Ref `last_change`>
        last_cid                  : mom_id_entity.last_cid
        link_to                   : swp_clip_x.link_to
        perma_name                : swp_page.perma_name
        pid                       : mom_id_entity.pid
        prio                      : swp_page.prio
        short_title               : swp_page.short_title
        text                      : swp_page.text
        title                     : swp_page.title
        type_name                 : mom_id_entity.type_name
        x_locked                  : mom_id_entity.x_locked
    <SAW : SWP.Gallery [swp_gallery : mom_id_entity]>
        clips                     : <SAW : Link_Ref_List `clips`>
        creation                  : <SAW : Rev_Ref `creation`>
        date                      : <Col-Mapper for MOM.Date_Interval_N>
            alive                 : <SAW : Boolean `date.alive`>
            finish                : swp_gallery.date__finish
            start                 : swp_gallery.date__start
        date.alive                : <SAW : Boolean `date.alive`>
        date.finish               : swp_gallery.date__finish
        date.start                : swp_gallery.date__start
        directory                 : swp_gallery.directory
        electric                  : mom_id_entity.electric
        last_change               : <SAW : Rev_Ref `last_change`>
        last_cid                  : mom_id_entity.last_cid
        perma_name                : swp_gallery.perma_name
        pictures                  : <SAW : Link_Ref_List `pictures`>
        pid                       : mom_id_entity.pid
        short_title               : swp_gallery.short_title
        title                     : swp_gallery.title
        type_name                 : mom_id_entity.type_name
        x_locked                  : mom_id_entity.x_locked
    <SAW : SWP.Picture [swp_picture : mom_id_entity]>
        creation                  : <SAW : Rev_Ref `creation`>
        electric                  : mom_id_entity.electric
        gallery                   : swp_picture.left
        last_change               : <SAW : Rev_Ref `last_change`>
        last_cid                  : mom_id_entity.last_cid
        left                      : swp_picture.left
        name                      : swp_picture.name
        number                    : swp_picture.number
        photo                     : <Col-Mapper for MOM._Pic_>
            extension             : swp_picture.photo__extension
            height                : swp_picture.photo__height
            width                 : swp_picture.photo__width
            x                     : swp_picture.photo__width
            y                     : swp_picture.photo__height
        photo.extension           : swp_picture.photo__extension
        photo.height              : swp_picture.photo__height
        photo.width               : swp_picture.photo__width
        photo.x                   : swp_picture.photo__width
        photo.y                   : swp_picture.photo__height
        pid                       : mom_id_entity.pid
        thumb                     : <Col-Mapper for MOM._Thumb_>
            extension             : swp_picture.thumb__extension
            height                : swp_picture.thumb__height
            width                 : swp_picture.thumb__width
        thumb.extension           : swp_picture.thumb__extension
        thumb.height              : swp_picture.thumb__height
        thumb.width               : swp_picture.thumb__width
        type_name                 : mom_id_entity.type_name
        x_locked                  : mom_id_entity.x_locked
    <SAW : SRM.Page [srm_page : swp_page : mom_id_entity]>
        clips                     : <SAW : Link_Ref_List `clips`>
        contents                  : swp_page.contents
        creation                  : <SAW : Rev_Ref `creation`>
        date                      : <Col-Mapper for MOM.Date_Interval_N>
            alive                 : <SAW : Boolean `date.alive`>
            finish                : swp_page.date__finish
            start                 : swp_page.date__start
        date.alive                : <SAW : Boolean `date.alive`>
        date.finish               : swp_page.date__finish
        date.start                : swp_page.date__start
        desc                      : srm_page.desc
        electric                  : mom_id_entity.electric
        event                     : srm_page.event
        events                    : <SAW : Link_Ref_List `events`>
        format                    : swp_page.format
        head_line                 : swp_page.head_line
        hidden                    : swp_page.hidden
        last_change               : <SAW : Rev_Ref `last_change`>
        last_cid                  : mom_id_entity.last_cid
        perma_name                : swp_page.perma_name
        pid                       : mom_id_entity.pid
        prio                      : swp_page.prio
        short_title               : swp_page.short_title
        text                      : swp_page.text
        title                     : swp_page.title
        type_name                 : mom_id_entity.type_name
        x_locked                  : mom_id_entity.x_locked
    <SAW : SRM.Regatta [srm_regatta : mom_id_entity]>
        boat_class                : srm_regatta.boat_class
        boats                     : <SAW : Link_Ref_List `boats`>
        creation                  : <SAW : Rev_Ref `creation`>
        discards                  : srm_regatta.discards
        electric                  : mom_id_entity.electric
        event                     : srm_regatta.left
        is_cancelled              : srm_regatta.is_cancelled
        kind                      : srm_regatta.kind
        last_change               : <SAW : Rev_Ref `last_change`>
        last_cid                  : mom_id_entity.last_cid
        left                      : srm_regatta.left
        perma_name                : srm_regatta.perma_name
        pid                       : mom_id_entity.pid
        races                     : srm_regatta.races
        races_counted             : <SAW : Int `races_counted`>
        result                    : <Col-Mapper for SRM.Regatta_Result>
            date                  : srm_regatta.result__date
            software              : srm_regatta.result__software
            status                : srm_regatta.result__status
        result.date               : srm_regatta.result__date
        result.software           : srm_regatta.result__software
        result.status             : srm_regatta.result__status
        type_name                 : mom_id_entity.type_name
        x_locked                  : mom_id_entity.x_locked
        year                      : <SAW : Int `year`>
    <SAW : SRM.Regatta_C [srm_regatta_c : srm_regatta : mom_id_entity]>
        boat_class                : srm_regatta.boat_class
        boats                     : <SAW : Link_Ref_List `boats`>
        creation                  : <SAW : Rev_Ref `creation`>
        discards                  : srm_regatta.discards
        electric                  : mom_id_entity.electric
        event                     : srm_regatta.left
        is_cancelled              : srm_regatta.is_cancelled
        is_team_race              : srm_regatta_c.is_team_race
        kind                      : srm_regatta.kind
        last_change               : <SAW : Rev_Ref `last_change`>
        last_cid                  : mom_id_entity.last_cid
        left                      : srm_regatta.left
        perma_name                : srm_regatta.perma_name
        pid                       : mom_id_entity.pid
        races                     : srm_regatta.races
        races_counted             : <SAW : Int `races_counted`>
        result                    : <Col-Mapper for SRM.Regatta_Result>
            date                  : srm_regatta.result__date
            software              : srm_regatta.result__software
            status                : srm_regatta.result__status
        result.date               : srm_regatta.result__date
        result.software           : srm_regatta.result__software
        result.status             : srm_regatta.result__status
        teams                     : <SAW : Link_Ref_List `teams`>
        type_name                 : mom_id_entity.type_name
        x_locked                  : mom_id_entity.x_locked
        year                      : <SAW : Int `year`>
    <SAW : SRM.Regatta_H [srm_regatta_h : srm_regatta : mom_id_entity]>
        boat_class                : srm_regatta.boat_class
        boats                     : <SAW : Link_Ref_List `boats`>
        creation                  : <SAW : Rev_Ref `creation`>
        discards                  : srm_regatta.discards
        electric                  : mom_id_entity.electric
        event                     : srm_regatta.left
        handicap                  : <SAW : Blob `handicap`>
        is_cancelled              : srm_regatta.is_cancelled
        kind                      : srm_regatta.kind
        last_change               : <SAW : Rev_Ref `last_change`>
        last_cid                  : mom_id_entity.last_cid
        left                      : srm_regatta.left
        perma_name                : srm_regatta.perma_name
        pid                       : mom_id_entity.pid
        races                     : srm_regatta.races
        races_counted             : <SAW : Int `races_counted`>
        result                    : <Col-Mapper for SRM.Regatta_Result>
            date                  : srm_regatta.result__date
            software              : srm_regatta.result__software
            status                : srm_regatta.result__status
        result.date               : srm_regatta.result__date
        result.software           : srm_regatta.result__software
        result.status             : srm_regatta.result__status
        type_name                 : mom_id_entity.type_name
        x_locked                  : mom_id_entity.x_locked
        year                      : <SAW : Int `year`>
    <SAW : SRM.Sailor [srm_sailor : mom_id_entity]>
        __raw_mna_number          : srm_sailor.__raw_mna_number
        boat_in_regatta_links     : <SAW : Link_Ref_List `boat_in_regatta_links`>
        club                      : srm_sailor.club
        creation                  : <SAW : Rev_Ref `creation`>
        electric                  : mom_id_entity.electric
        last_change               : <SAW : Rev_Ref `last_change`>
        last_cid                  : mom_id_entity.last_cid
        left                      : srm_sailor.left
        mna_number                : srm_sailor.mna_number
        nation                    : srm_sailor.nation
        person                    : srm_sailor.left
        pid                       : mom_id_entity.pid
        type_name                 : mom_id_entity.type_name
        x_locked                  : mom_id_entity.x_locked
    <SAW : SRM._MOM_Link_n_ [mom_id_entity]>
        creation                  : <SAW : Rev_Ref `creation`>
        electric                  : mom_id_entity.electric
        last_change               : <SAW : Rev_Ref `last_change`>
        last_cid                  : mom_id_entity.last_cid
        left                      : <SAW : Left `left` (SRM.Boat_in_Regatta | SRM.Crew_Member | SRM.Team_has_Boat_in
        pid                       : mom_id_entity.pid
        right                     : <SAW : Right `right` (SRM.Boat_in_Regatta | SRM.Crew_Member | SRM.Team_has_Boat_
        type_name                 : mom_id_entity.type_name
        x_locked                  : mom_id_entity.x_locked
    <SAW : SRM.Link2 [mom_id_entity]>
        creation                  : <SAW : Rev_Ref `creation`>
        electric                  : mom_id_entity.electric
        last_change               : <SAW : Rev_Ref `last_change`>
        last_cid                  : mom_id_entity.last_cid
        left                      : <SAW : Left `left` (SRM.Boat_in_Regatta | SRM.Crew_Member | SRM.Team_has_Boat_in
        pid                       : mom_id_entity.pid
        right                     : <SAW : Right `right` (SRM.Boat_in_Regatta | SRM.Crew_Member | SRM.Team_has_Boat_
        type_name                 : mom_id_entity.type_name
        x_locked                  : mom_id_entity.x_locked
    <SAW : SRM.Boat_in_Regatta [srm_boat_in_regatta : mom_id_entity]>
        _crew                     : <SAW : Role_Ref_Set `_crew`>
        boat                      : srm_boat_in_regatta.left
        creation                  : <SAW : Rev_Ref `creation`>
        electric                  : mom_id_entity.electric
        last_change               : <SAW : Rev_Ref `last_change`>
        last_cid                  : mom_id_entity.last_cid
        left                      : srm_boat_in_regatta.left
        pid                       : mom_id_entity.pid
        place                     : srm_boat_in_regatta.place
        points                    : srm_boat_in_regatta.points
        race_results              : <SAW : Link_Ref_List `race_results`>
        rank                      : srm_boat_in_regatta.rank
        regatta                   : srm_boat_in_regatta.right
        registration_date         : srm_boat_in_regatta.registration_date
        right                     : srm_boat_in_regatta.right
        sailor_links              : <SAW : Link_Ref_List `sailor_links`>
        skipper                   : srm_boat_in_regatta.skipper
        team_links                : <SAW : Link_Ref_List `team_links`>
        teams                     : <SAW : Role_Ref_Set `teams`>
        type_name                 : mom_id_entity.type_name
        x_locked                  : mom_id_entity.x_locked
    <SAW : SRM.Race_Result [srm_race_result : mom_id_entity]>
        boat_in_regatta           : srm_race_result.left
        creation                  : <SAW : Rev_Ref `creation`>
        discarded                 : srm_race_result.discarded
        electric                  : mom_id_entity.electric
        last_change               : <SAW : Rev_Ref `last_change`>
        last_cid                  : mom_id_entity.last_cid
        left                      : srm_race_result.left
        pid                       : mom_id_entity.pid
        points                    : srm_race_result.points
        race                      : srm_race_result.race
        status                    : srm_race_result.status
        type_name                 : mom_id_entity.type_name
        x_locked                  : mom_id_entity.x_locked
    <SAW : SRM.Team [srm_team : mom_id_entity]>
        __raw_name                : srm_team.__raw_name
        boat_links                : <SAW : Link_Ref_List `boat_links`>
        boats                     : <SAW : Role_Ref_Set `boats`>
        club                      : srm_team.club
        creation                  : <SAW : Rev_Ref `creation`>
        desc                      : srm_team.desc
        electric                  : mom_id_entity.electric
        last_change               : <SAW : Rev_Ref `last_change`>
        last_cid                  : mom_id_entity.last_cid
        leader                    : srm_team.leader
        left                      : srm_team.left
        name                      : srm_team.name
        pid                       : mom_id_entity.pid
        place                     : srm_team.place
        regatta                   : srm_team.left
        registration_date         : srm_team.registration_date
        type_name                 : mom_id_entity.type_name
        x_locked                  : mom_id_entity.x_locked
    <SAW : SRM.Crew_Member [srm_crew_member : mom_id_entity]>
        boat_in_regatta           : srm_crew_member.left
        creation                  : <SAW : Rev_Ref `creation`>
        electric                  : mom_id_entity.electric
        key                       : srm_crew_member.key
        last_change               : <SAW : Rev_Ref `last_change`>
        last_cid                  : mom_id_entity.last_cid
        left                      : srm_crew_member.left
        pid                       : mom_id_entity.pid
        right                     : srm_crew_member.right
        role                      : srm_crew_member.role
        sailor                    : srm_crew_member.right
        type_name                 : mom_id_entity.type_name
        x_locked                  : mom_id_entity.x_locked
    <SAW : SRM.Team_has_Boat_in_Regatta [srm_team_has_boat_in_regatta : mom_id_entity]>
        boat                      : srm_team_has_boat_in_regatta.right
        creation                  : <SAW : Rev_Ref `creation`>
        electric                  : mom_id_entity.electric
        last_change               : <SAW : Rev_Ref `last_change`>
        last_cid                  : mom_id_entity.last_cid
        left                      : srm_team_has_boat_in_regatta.left
        pid                       : mom_id_entity.pid
        right                     : srm_team_has_boat_in_regatta.right
        team                      : srm_team_has_boat_in_regatta.left
        type_name                 : mom_id_entity.type_name
        x_locked                  : mom_id_entity.x_locked
    <SAW : PAP.Subject_has_Address [pap_subject_has_property : mom_id_entity]>
        address                   : pap_subject_has_property.right
        creation                  : <SAW : Rev_Ref `creation`>
        desc                      : pap_subject_has_property.desc
        electric                  : mom_id_entity.electric
        last_change               : <SAW : Rev_Ref `last_change`>
        last_cid                  : mom_id_entity.last_cid
        left                      : pap_subject_has_property.left
        pid                       : mom_id_entity.pid
        property                  : pap_subject_has_property.right
        right                     : pap_subject_has_property.right
        subject                   : pap_subject_has_property.left
        type_name                 : mom_id_entity.type_name
        x_locked                  : mom_id_entity.x_locked
    <SAW : PAP.Subject_has_Email [pap_subject_has_property : mom_id_entity]>
        creation                  : <SAW : Rev_Ref `creation`>
        desc                      : pap_subject_has_property.desc
        electric                  : mom_id_entity.electric
        email                     : pap_subject_has_property.right
        last_change               : <SAW : Rev_Ref `last_change`>
        last_cid                  : mom_id_entity.last_cid
        left                      : pap_subject_has_property.left
        pid                       : mom_id_entity.pid
        property                  : pap_subject_has_property.right
        right                     : pap_subject_has_property.right
        subject                   : pap_subject_has_property.left
        type_name                 : mom_id_entity.type_name
        x_locked                  : mom_id_entity.x_locked
    <SAW : PAP.Subject_has_Phone [pap_subject_has_phone : pap_subject_has_property : mom_id_entity]>
        creation                  : <SAW : Rev_Ref `creation`>
        desc                      : pap_subject_has_property.desc
        electric                  : mom_id_entity.electric
        extension                 : pap_subject_has_phone.extension
        last_change               : <SAW : Rev_Ref `last_change`>
        last_cid                  : mom_id_entity.last_cid
        left                      : pap_subject_has_property.left
        phone                     : pap_subject_has_property.right
        pid                       : mom_id_entity.pid
        property                  : pap_subject_has_property.right
        right                     : pap_subject_has_property.right
        subject                   : pap_subject_has_property.left
        type_name                 : mom_id_entity.type_name
        x_locked                  : mom_id_entity.x_locked
    <SAW : PAP.Subject_has_Url [pap_subject_has_property : mom_id_entity]>
        creation                  : <SAW : Rev_Ref `creation`>
        desc                      : pap_subject_has_property.desc
        electric                  : mom_id_entity.electric
        last_change               : <SAW : Rev_Ref `last_change`>
        last_cid                  : mom_id_entity.last_cid
        left                      : pap_subject_has_property.left
        pid                       : mom_id_entity.pid
        property                  : pap_subject_has_property.right
        right                     : pap_subject_has_property.right
        subject                   : pap_subject_has_property.left
        type_name                 : mom_id_entity.type_name
        url                       : pap_subject_has_property.right
        x_locked                  : mom_id_entity.x_locked
    <SAW : PAP.Company_has_Url [pap_company_has_url : pap_subject_has_property : mom_id_entity]>
        company                   : pap_subject_has_property.left
        creation                  : <SAW : Rev_Ref `creation`>
        desc                      : pap_subject_has_property.desc
        electric                  : mom_id_entity.electric
        last_change               : <SAW : Rev_Ref `last_change`>
        last_cid                  : mom_id_entity.last_cid
        left                      : pap_subject_has_property.left
        pid                       : mom_id_entity.pid
        property                  : pap_subject_has_property.right
        right                     : pap_subject_has_property.right
        subject                   : pap_subject_has_property.left
        type_name                 : mom_id_entity.type_name
        url                       : pap_subject_has_property.right
        x_locked                  : mom_id_entity.x_locked
    <SAW : PAP.Person_has_Url [pap_person_has_url : pap_subject_has_property : mom_id_entity]>
        creation                  : <SAW : Rev_Ref `creation`>
        desc                      : pap_subject_has_property.desc
        electric                  : mom_id_entity.electric
        last_change               : <SAW : Rev_Ref `last_change`>
        last_cid                  : mom_id_entity.last_cid
        left                      : pap_subject_has_property.left
        person                    : pap_subject_has_property.left
        pid                       : mom_id_entity.pid
        property                  : pap_subject_has_property.right
        right                     : pap_subject_has_property.right
        subject                   : pap_subject_has_property.left
        type_name                 : mom_id_entity.type_name
        url                       : pap_subject_has_property.right
        x_locked                  : mom_id_entity.x_locked
    <SAW : PAP.Company_has_Phone [pap_company_has_phone : pap_subject_has_phone : pap_subject_has_property : mom_id_entity]>
        company                   : pap_subject_has_property.left
        creation                  : <SAW : Rev_Ref `creation`>
        desc                      : pap_subject_has_property.desc
        electric                  : mom_id_entity.electric
        extension                 : pap_subject_has_phone.extension
        last_change               : <SAW : Rev_Ref `last_change`>
        last_cid                  : mom_id_entity.last_cid
        left                      : pap_subject_has_property.left
        phone                     : pap_subject_has_property.right
        pid                       : mom_id_entity.pid
        property                  : pap_subject_has_property.right
        right                     : pap_subject_has_property.right
        subject                   : pap_subject_has_property.left
        type_name                 : mom_id_entity.type_name
        x_locked                  : mom_id_entity.x_locked
    <SAW : PAP.Person_has_Phone [pap_person_has_phone : pap_subject_has_phone : pap_subject_has_property : mom_id_entity]>
        creation                  : <SAW : Rev_Ref `creation`>
        desc                      : pap_subject_has_property.desc
        electric                  : mom_id_entity.electric
        extension                 : pap_subject_has_phone.extension
        last_change               : <SAW : Rev_Ref `last_change`>
        last_cid                  : mom_id_entity.last_cid
        left                      : pap_subject_has_property.left
        person                    : pap_subject_has_property.left
        phone                     : pap_subject_has_property.right
        pid                       : mom_id_entity.pid
        property                  : pap_subject_has_property.right
        right                     : pap_subject_has_property.right
        subject                   : pap_subject_has_property.left
        type_name                 : mom_id_entity.type_name
        x_locked                  : mom_id_entity.x_locked
    <SAW : PAP.Company_has_Email [pap_company_has_email : pap_subject_has_property : mom_id_entity]>
        company                   : pap_subject_has_property.left
        creation                  : <SAW : Rev_Ref `creation`>
        desc                      : pap_subject_has_property.desc
        electric                  : mom_id_entity.electric
        email                     : pap_subject_has_property.right
        last_change               : <SAW : Rev_Ref `last_change`>
        last_cid                  : mom_id_entity.last_cid
        left                      : pap_subject_has_property.left
        pid                       : mom_id_entity.pid
        property                  : pap_subject_has_property.right
        right                     : pap_subject_has_property.right
        subject                   : pap_subject_has_property.left
        type_name                 : mom_id_entity.type_name
        x_locked                  : mom_id_entity.x_locked
    <SAW : PAP.Person_has_Email [pap_person_has_email : pap_subject_has_property : mom_id_entity]>
        creation                  : <SAW : Rev_Ref `creation`>
        desc                      : pap_subject_has_property.desc
        electric                  : mom_id_entity.electric
        email                     : pap_subject_has_property.right
        last_change               : <SAW : Rev_Ref `last_change`>
        last_cid                  : mom_id_entity.last_cid
        left                      : pap_subject_has_property.left
        person                    : pap_subject_has_property.left
        pid                       : mom_id_entity.pid
        property                  : pap_subject_has_property.right
        right                     : pap_subject_has_property.right
        subject                   : pap_subject_has_property.left
        type_name                 : mom_id_entity.type_name
        x_locked                  : mom_id_entity.x_locked
    <SAW : PAP.Company_has_Address [pap_company_has_address : pap_subject_has_property : mom_id_entity]>
        address                   : pap_subject_has_property.right
        company                   : pap_subject_has_property.left
        creation                  : <SAW : Rev_Ref `creation`>
        desc                      : pap_subject_has_property.desc
        electric                  : mom_id_entity.electric
        last_change               : <SAW : Rev_Ref `last_change`>
        last_cid                  : mom_id_entity.last_cid
        left                      : pap_subject_has_property.left
        pid                       : mom_id_entity.pid
        property                  : pap_subject_has_property.right
        right                     : pap_subject_has_property.right
        subject                   : pap_subject_has_property.left
        type_name                 : mom_id_entity.type_name
        x_locked                  : mom_id_entity.x_locked
    <SAW : PAP.Person_has_Address [pap_person_has_address : pap_subject_has_property : mom_id_entity]>
        address                   : pap_subject_has_property.right
        creation                  : <SAW : Rev_Ref `creation`>
        desc                      : pap_subject_has_property.desc
        electric                  : mom_id_entity.electric
        last_change               : <SAW : Rev_Ref `last_change`>
        last_cid                  : mom_id_entity.last_cid
        left                      : pap_subject_has_property.left
        person                    : pap_subject_has_property.left
        pid                       : mom_id_entity.pid
        property                  : pap_subject_has_property.right
        right                     : pap_subject_has_property.right
        subject                   : pap_subject_has_property.left
        type_name                 : mom_id_entity.type_name
        x_locked                  : mom_id_entity.x_locked


"""

_test_select = """
    >>> apt, url = Scaffold.app_type_and_url (%(p1)s, %(n1)s)

    >>> show_selects (apt)
    MOM.Id_Entity
        SELECT auth__account_.enabled AS auth__account__enabled,
               auth__account_.name AS auth__account__name,
               auth__account_.pid AS auth__account__pid,
               auth__account_.superuser AS auth__account__superuser,
               auth__account_.suspended AS auth__account__suspended,
               auth_account.password AS auth_account_password,
               auth_account.ph_name AS auth_account_ph_name,
               auth_account.pid AS auth_account_pid,
               auth_account_activation."left" AS auth_account_activation_left,
               auth_account_activation.pid AS auth_account_activation_pid,
               auth_account_email_verification."left" AS auth_account_email_verification_left,
               auth_account_email_verification.expires AS auth_account_email_verification_expires,
               auth_account_email_verification.new_email AS auth_account_email_verification_new_email,
               auth_account_email_verification.pid AS auth_account_email_verification_pid,
               auth_account_email_verification.token AS auth_account_email_verification_token,
               auth_account_in_group."left" AS auth_account_in_group_left,
               auth_account_in_group."right" AS auth_account_in_group_right,
               auth_account_in_group.pid AS auth_account_in_group_pid,
               auth_account_password_change_required."left" AS auth_account_password_change_required_left,
               auth_account_password_change_required.pid AS auth_account_password_change_required_pid,
               auth_account_password_reset."left" AS auth_account_password_reset_left,
               auth_account_password_reset.expires AS auth_account_password_reset_expires,
               auth_account_password_reset.password AS auth_account_password_reset_password,
               auth_account_password_reset.pid AS auth_account_password_reset_pid,
               auth_account_password_reset.token AS auth_account_password_reset_token,
               auth_certificate."desc" AS auth_certificate_desc,
               auth_certificate.cert_id AS auth_certificate_cert_id,
               auth_certificate.email AS auth_certificate_email,
               auth_certificate.pem AS auth_certificate_pem,
               auth_certificate.pid AS auth_certificate_pid,
               auth_certificate.revocation_date AS auth_certificate_revocation_date,
               auth_certificate.validity__finish AS auth_certificate_validity__finish,
               auth_certificate.validity__start AS auth_certificate_validity__start,
               auth_group."desc" AS auth_group_desc,
               auth_group.name AS auth_group_name,
               auth_group.pid AS auth_group_pid,
               evt_calendar."desc" AS evt_calendar_desc,
               evt_calendar.name AS evt_calendar_name,
               evt_calendar.pid AS evt_calendar_pid,
               evt_event."left" AS evt_event_left,
               evt_event.calendar AS evt_event_calendar,
               evt_event.date__finish AS evt_event_date__finish,
               evt_event.date__start AS evt_event_date__start,
               evt_event.detail AS evt_event_detail,
               evt_event.pid AS evt_event_pid,
               evt_event.short_title AS evt_event_short_title,
               evt_event.time__finish AS evt_event_time__finish,
               evt_event.time__start AS evt_event_time__start,
               evt_event_occurs."left" AS evt_event_occurs_left,
               evt_event_occurs.date AS evt_event_occurs_date,
               evt_event_occurs.pid AS evt_event_occurs_pid,
               evt_event_occurs.time__finish AS evt_event_occurs_time__finish,
               evt_event_occurs.time__start AS evt_event_occurs_time__start,
               evt_recurrence_rule."desc" AS evt_recurrence_rule_desc,
               evt_recurrence_rule."left" AS evt_recurrence_rule_left,
               evt_recurrence_rule.count AS evt_recurrence_rule_count,
               evt_recurrence_rule.easter_offset AS evt_recurrence_rule_easter_offset,
               evt_recurrence_rule.finish AS evt_recurrence_rule_finish,
               evt_recurrence_rule.is_exception AS evt_recurrence_rule_is_exception,
               evt_recurrence_rule.month AS evt_recurrence_rule_month,
               evt_recurrence_rule.month_day AS evt_recurrence_rule_month_day,
               evt_recurrence_rule.period AS evt_recurrence_rule_period,
               evt_recurrence_rule.pid AS evt_recurrence_rule_pid,
               evt_recurrence_rule.restrict_pos AS evt_recurrence_rule_restrict_pos,
               evt_recurrence_rule.start AS evt_recurrence_rule_start,
               evt_recurrence_rule.unit AS evt_recurrence_rule_unit,
               evt_recurrence_rule.week AS evt_recurrence_rule_week,
               evt_recurrence_rule.week_day AS evt_recurrence_rule_week_day,
               evt_recurrence_rule.year_day AS evt_recurrence_rule_year_day,
               evt_recurrence_spec."left" AS evt_recurrence_spec_left,
               evt_recurrence_spec.date_exceptions AS evt_recurrence_spec_date_exceptions,
               evt_recurrence_spec.dates AS evt_recurrence_spec_dates,
               evt_recurrence_spec.pid AS evt_recurrence_spec_pid,
               mom_id_entity.electric AS mom_id_entity_electric,
               mom_id_entity.last_cid AS mom_id_entity_last_cid,
               mom_id_entity.pid AS mom_id_entity_pid,
               mom_id_entity.type_name AS mom_id_entity_type_name,
               mom_id_entity.x_locked AS mom_id_entity_x_locked,
               pap_address."desc" AS pap_address_desc,
               pap_address.__raw_city AS pap_address___raw_city,
               pap_address.__raw_country AS pap_address___raw_country,
               pap_address.__raw_region AS pap_address___raw_region,
               pap_address.__raw_street AS pap_address___raw_street,
               pap_address.__raw_zip AS pap_address___raw_zip,
               pap_address.city AS pap_address_city,
               pap_address.country AS pap_address_country,
               pap_address.pid AS pap_address_pid,
               pap_address.region AS pap_address_region,
               pap_address.street AS pap_address_street,
               pap_address.zip AS pap_address_zip,
               pap_address_position."left" AS pap_address_position_left,
               pap_address_position.pid AS pap_address_position_pid,
               pap_address_position.position____raw_lat AS pap_address_position_position____raw_lat,
               pap_address_position.position____raw_lon AS pap_address_position_position____raw_lon,
               pap_address_position.position__height AS pap_address_position_position__height,
               pap_address_position.position__lat AS pap_address_position_position__lat,
               pap_address_position.position__lon AS pap_address_position_position__lon,
               pap_company.__raw_name AS pap_company___raw_name,
               pap_company.__raw_registered_in AS pap_company___raw_registered_in,
               pap_company.__raw_short_name AS pap_company___raw_short_name,
               pap_company.lifetime__finish AS pap_company_lifetime__finish,
               pap_company.lifetime__start AS pap_company_lifetime__start,
               pap_company.name AS pap_company_name,
               pap_company.pid AS pap_company_pid,
               pap_company.registered_in AS pap_company_registered_in,
               pap_company.short_name AS pap_company_short_name,
               pap_email."desc" AS pap_email_desc,
               pap_email.__raw_address AS pap_email___raw_address,
               pap_email.address AS pap_email_address,
               pap_email.pid AS pap_email_pid,
               pap_person.__raw_first_name AS pap_person___raw_first_name,
               pap_person.__raw_last_name AS pap_person___raw_last_name,
               pap_person.__raw_middle_name AS pap_person___raw_middle_name,
               pap_person.__raw_title AS pap_person___raw_title,
               pap_person.first_name AS pap_person_first_name,
               pap_person.last_name AS pap_person_last_name,
               pap_person.lifetime__finish AS pap_person_lifetime__finish,
               pap_person.lifetime__start AS pap_person_lifetime__start,
               pap_person.middle_name AS pap_person_middle_name,
               pap_person.pid AS pap_person_pid,
               pap_person.sex AS pap_person_sex,
               pap_person.title AS pap_person_title,
               pap_person_has_account."left" AS pap_person_has_account_left,
               pap_person_has_account."right" AS pap_person_has_account_right,
               pap_person_has_account.pid AS pap_person_has_account_pid,
               pap_phone."desc" AS pap_phone_desc,
               pap_phone.area_code AS pap_phone_area_code,
               pap_phone.country_code AS pap_phone_country_code,
               pap_phone.number AS pap_phone_number,
               pap_phone.pid AS pap_phone_pid,
               pap_subject_has_phone.extension AS pap_subject_has_phone_extension,
               pap_subject_has_phone.pid AS pap_subject_has_phone_pid,
               pap_subject_has_property."desc" AS pap_subject_has_property_desc,
               pap_subject_has_property."left" AS pap_subject_has_property_left,
               pap_subject_has_property."right" AS pap_subject_has_property_right,
               pap_subject_has_property.pid AS pap_subject_has_property_pid,
               pap_url."desc" AS pap_url_desc,
               pap_url.pid AS pap_url_pid,
               pap_url.value AS pap_url_value,
               srm__boat_class_.__raw_name AS srm__boat_class____raw_name,
               srm__boat_class_.name AS srm__boat_class__name,
               srm__boat_class_.pid AS srm__boat_class__pid,
               srm_boat."left" AS srm_boat_left,
               srm_boat.__raw_sail_number AS srm_boat___raw_sail_number,
               srm_boat.__raw_sail_number_x AS srm_boat___raw_sail_number_x,
               srm_boat.name AS srm_boat_name,
               srm_boat.nation AS srm_boat_nation,
               srm_boat.pid AS srm_boat_pid,
               srm_boat.sail_number AS srm_boat_sail_number,
               srm_boat.sail_number_x AS srm_boat_sail_number_x,
               srm_boat_class.beam AS srm_boat_class_beam,
               srm_boat_class.loa AS srm_boat_class_loa,
               srm_boat_class.max_crew AS srm_boat_class_max_crew,
               srm_boat_class.pid AS srm_boat_class_pid,
               srm_boat_class.sail_area AS srm_boat_class_sail_area,
               srm_boat_in_regatta."left" AS srm_boat_in_regatta_left,
               srm_boat_in_regatta."right" AS srm_boat_in_regatta_right,
               srm_boat_in_regatta.pid AS srm_boat_in_regatta_pid,
               srm_boat_in_regatta.place AS srm_boat_in_regatta_place,
               srm_boat_in_regatta.points AS srm_boat_in_regatta_points,
               srm_boat_in_regatta.rank AS srm_boat_in_regatta_rank,
               srm_boat_in_regatta.registration_date AS srm_boat_in_regatta_registration_date,
               srm_boat_in_regatta.skipper AS srm_boat_in_regatta_skipper,
               srm_club.__raw_name AS srm_club___raw_name,
               srm_club.long_name AS srm_club_long_name,
               srm_club.name AS srm_club_name,
               srm_club.pid AS srm_club_pid,
               srm_crew_member."left" AS srm_crew_member_left,
               srm_crew_member."right" AS srm_crew_member_right,
               srm_crew_member.key AS srm_crew_member_key,
               srm_crew_member.pid AS srm_crew_member_pid,
               srm_crew_member.role AS srm_crew_member_role,
               srm_page."desc" AS srm_page_desc,
               srm_page.event AS srm_page_event,
               srm_page.pid AS srm_page_pid,
               srm_race_result."left" AS srm_race_result_left,
               srm_race_result.discarded AS srm_race_result_discarded,
               srm_race_result.pid AS srm_race_result_pid,
               srm_race_result.points AS srm_race_result_points,
               srm_race_result.race AS srm_race_result_race,
               srm_race_result.status AS srm_race_result_status,
               srm_regatta."left" AS srm_regatta_left,
               srm_regatta.boat_class AS srm_regatta_boat_class,
               srm_regatta.discards AS srm_regatta_discards,
               srm_regatta.is_cancelled AS srm_regatta_is_cancelled,
               srm_regatta.kind AS srm_regatta_kind,
               srm_regatta.perma_name AS srm_regatta_perma_name,
               srm_regatta.pid AS srm_regatta_pid,
               srm_regatta.races AS srm_regatta_races,
               srm_regatta.result__date AS srm_regatta_result__date,
               srm_regatta.result__software AS srm_regatta_result__software,
               srm_regatta.result__status AS srm_regatta_result__status,
               srm_regatta_c.is_team_race AS srm_regatta_c_is_team_race,
               srm_regatta_c.pid AS srm_regatta_c_pid,
               srm_regatta_event."desc" AS srm_regatta_event_desc,
               srm_regatta_event.__raw_name AS srm_regatta_event___raw_name,
               srm_regatta_event.club AS srm_regatta_event_club,
               srm_regatta_event.date__finish AS srm_regatta_event_date__finish,
               srm_regatta_event.date__start AS srm_regatta_event_date__start,
               srm_regatta_event.is_cancelled AS srm_regatta_event_is_cancelled,
               srm_regatta_event.name AS srm_regatta_event_name,
               srm_regatta_event.perma_name AS srm_regatta_event_perma_name,
               srm_regatta_event.pid AS srm_regatta_event_pid,
               srm_sailor."left" AS srm_sailor_left,
               srm_sailor.__raw_mna_number AS srm_sailor___raw_mna_number,
               srm_sailor.club AS srm_sailor_club,
               srm_sailor.mna_number AS srm_sailor_mna_number,
               srm_sailor.nation AS srm_sailor_nation,
               srm_sailor.pid AS srm_sailor_pid,
               srm_team."desc" AS srm_team_desc,
               srm_team."left" AS srm_team_left,
               srm_team.__raw_name AS srm_team___raw_name,
               srm_team.club AS srm_team_club,
               srm_team.leader AS srm_team_leader,
               srm_team.name AS srm_team_name,
               srm_team.pid AS srm_team_pid,
               srm_team.place AS srm_team_place,
               srm_team.registration_date AS srm_team_registration_date,
               srm_team_has_boat_in_regatta."left" AS srm_team_has_boat_in_regatta_left,
               srm_team_has_boat_in_regatta."right" AS srm_team_has_boat_in_regatta_right,
               srm_team_has_boat_in_regatta.pid AS srm_team_has_boat_in_regatta_pid,
               swp_clip_o."left" AS swp_clip_o_left,
               swp_clip_o.abstract AS swp_clip_o_abstract,
               swp_clip_o.contents AS swp_clip_o_contents,
               swp_clip_o.date__finish AS swp_clip_o_date__finish,
               swp_clip_o.date__start AS swp_clip_o_date__start,
               swp_clip_o.date_x__finish AS swp_clip_o_date_x__finish,
               swp_clip_o.date_x__start AS swp_clip_o_date_x__start,
               swp_clip_o.pid AS swp_clip_o_pid,
               swp_clip_o.prio AS swp_clip_o_prio,
               swp_clip_x.link_to AS swp_clip_x_link_to,
               swp_clip_x.pid AS swp_clip_x_pid,
               swp_gallery.date__finish AS swp_gallery_date__finish,
               swp_gallery.date__start AS swp_gallery_date__start,
               swp_gallery.directory AS swp_gallery_directory,
               swp_gallery.perma_name AS swp_gallery_perma_name,
               swp_gallery.pid AS swp_gallery_pid,
               swp_gallery.short_title AS swp_gallery_short_title,
               swp_gallery.title AS swp_gallery_title,
               swp_page.contents AS swp_page_contents,
               swp_page.date__finish AS swp_page_date__finish,
               swp_page.date__start AS swp_page_date__start,
               swp_page.format AS swp_page_format,
               swp_page.head_line AS swp_page_head_line,
               swp_page.hidden AS swp_page_hidden,
               swp_page.perma_name AS swp_page_perma_name,
               swp_page.pid AS swp_page_pid,
               swp_page.prio AS swp_page_prio,
               swp_page.short_title AS swp_page_short_title,
               swp_page.text AS swp_page_text,
               swp_page.title AS swp_page_title,
               swp_page_y.pid AS swp_page_y_pid,
               swp_page_y.year AS swp_page_y_year,
               swp_picture."left" AS swp_picture_left,
               swp_picture.name AS swp_picture_name,
               swp_picture.number AS swp_picture_number,
               swp_picture.photo__extension AS swp_picture_photo__extension,
               swp_picture.photo__height AS swp_picture_photo__height,
               swp_picture.photo__width AS swp_picture_photo__width,
               swp_picture.pid AS swp_picture_pid,
               swp_picture.thumb__extension AS swp_picture_thumb__extension,
               swp_picture.thumb__height AS swp_picture_thumb__height,
               swp_picture.thumb__width AS swp_picture_thumb__width
        FROM mom_id_entity
           LEFT OUTER JOIN auth__account_ ON mom_id_entity.pid = auth__account_.pid
           LEFT OUTER JOIN auth_account ON auth__account_.pid = auth_account.pid
           LEFT OUTER JOIN auth_certificate ON mom_id_entity.pid = auth_certificate.pid
           LEFT OUTER JOIN auth_group ON mom_id_entity.pid = auth_group.pid
           LEFT OUTER JOIN auth_account_in_group ON mom_id_entity.pid = auth_account_in_group.pid
           LEFT OUTER JOIN auth_account_activation ON mom_id_entity.pid = auth_account_activation.pid
           LEFT OUTER JOIN auth_account_password_change_required ON mom_id_entity.pid = auth_account_password_change_required.pid
           LEFT OUTER JOIN auth_account_email_verification ON mom_id_entity.pid = auth_account_email_verification.pid
           LEFT OUTER JOIN auth_account_password_reset ON mom_id_entity.pid = auth_account_password_reset.pid
           LEFT OUTER JOIN evt_calendar ON mom_id_entity.pid = evt_calendar.pid
           LEFT OUTER JOIN swp_page ON mom_id_entity.pid = swp_page.pid
           LEFT OUTER JOIN swp_page_y ON swp_page.pid = swp_page_y.pid
           LEFT OUTER JOIN swp_clip_x ON swp_page.pid = swp_clip_x.pid
           LEFT OUTER JOIN srm_page ON swp_page.pid = srm_page.pid
           LEFT OUTER JOIN evt_event ON mom_id_entity.pid = evt_event.pid
           LEFT OUTER JOIN evt_event_occurs ON mom_id_entity.pid = evt_event_occurs.pid
           LEFT OUTER JOIN evt_recurrence_spec ON mom_id_entity.pid = evt_recurrence_spec.pid
           LEFT OUTER JOIN evt_recurrence_rule ON mom_id_entity.pid = evt_recurrence_rule.pid
           LEFT OUTER JOIN pap_address ON mom_id_entity.pid = pap_address.pid
           LEFT OUTER JOIN pap_company ON mom_id_entity.pid = pap_company.pid
           LEFT OUTER JOIN pap_email ON mom_id_entity.pid = pap_email.pid
           LEFT OUTER JOIN pap_phone ON mom_id_entity.pid = pap_phone.pid
           LEFT OUTER JOIN pap_person ON mom_id_entity.pid = pap_person.pid
           LEFT OUTER JOIN pap_url ON mom_id_entity.pid = pap_url.pid
           LEFT OUTER JOIN pap_address_position ON mom_id_entity.pid = pap_address_position.pid
           LEFT OUTER JOIN pap_subject_has_property ON mom_id_entity.pid = pap_subject_has_property.pid
           LEFT OUTER JOIN pap_subject_has_phone ON pap_subject_has_property.pid = pap_subject_has_phone.pid
           LEFT OUTER JOIN pap_person_has_account ON mom_id_entity.pid = pap_person_has_account.pid
           LEFT OUTER JOIN srm__boat_class_ ON mom_id_entity.pid = srm__boat_class_.pid
           LEFT OUTER JOIN srm_boat_class ON srm__boat_class_.pid = srm_boat_class.pid
           LEFT OUTER JOIN srm_boat ON mom_id_entity.pid = srm_boat.pid
           LEFT OUTER JOIN srm_club ON mom_id_entity.pid = srm_club.pid
           LEFT OUTER JOIN srm_regatta_event ON mom_id_entity.pid = srm_regatta_event.pid
           LEFT OUTER JOIN swp_clip_o ON mom_id_entity.pid = swp_clip_o.pid
           LEFT OUTER JOIN swp_gallery ON mom_id_entity.pid = swp_gallery.pid
           LEFT OUTER JOIN swp_picture ON mom_id_entity.pid = swp_picture.pid
           LEFT OUTER JOIN srm_regatta ON mom_id_entity.pid = srm_regatta.pid
           LEFT OUTER JOIN srm_regatta_c ON srm_regatta.pid = srm_regatta_c.pid
           LEFT OUTER JOIN srm_sailor ON mom_id_entity.pid = srm_sailor.pid
           LEFT OUTER JOIN srm_boat_in_regatta ON mom_id_entity.pid = srm_boat_in_regatta.pid
           LEFT OUTER JOIN srm_race_result ON mom_id_entity.pid = srm_race_result.pid
           LEFT OUTER JOIN srm_team ON mom_id_entity.pid = srm_team.pid
           LEFT OUTER JOIN srm_crew_member ON mom_id_entity.pid = srm_crew_member.pid
           LEFT OUTER JOIN srm_team_has_boat_in_regatta ON mom_id_entity.pid = srm_team_has_boat_in_regatta.pid
    MOM.MD_Change
        SELECT mom_md_change."user" AS mom_md_change_user,
               mom_md_change.c_time AS mom_md_change_c_time,
               mom_md_change.c_user AS mom_md_change_c_user,
               mom_md_change.cid AS mom_md_change_cid,
               mom_md_change.kind AS mom_md_change_kind,
               mom_md_change.parent_cid AS mom_md_change_parent_cid,
               mom_md_change.pid AS mom_md_change_pid,
               mom_md_change.scm_change AS mom_md_change_scm_change,
               mom_md_change.time AS mom_md_change_time,
               mom_md_change.type_name AS mom_md_change_type_name
        FROM mom_md_change
    MOM.Link
        SELECT auth_account_activation."left" AS auth_account_activation_left,
               auth_account_activation.pid AS auth_account_activation_pid,
               auth_account_email_verification."left" AS auth_account_email_verification_left,
               auth_account_email_verification.expires AS auth_account_email_verification_expires,
               auth_account_email_verification.new_email AS auth_account_email_verification_new_email,
               auth_account_email_verification.pid AS auth_account_email_verification_pid,
               auth_account_email_verification.token AS auth_account_email_verification_token,
               auth_account_in_group."left" AS auth_account_in_group_left,
               auth_account_in_group."right" AS auth_account_in_group_right,
               auth_account_in_group.pid AS auth_account_in_group_pid,
               auth_account_password_change_required."left" AS auth_account_password_change_required_left,
               auth_account_password_change_required.pid AS auth_account_password_change_required_pid,
               auth_account_password_reset."left" AS auth_account_password_reset_left,
               auth_account_password_reset.expires AS auth_account_password_reset_expires,
               auth_account_password_reset.password AS auth_account_password_reset_password,
               auth_account_password_reset.pid AS auth_account_password_reset_pid,
               auth_account_password_reset.token AS auth_account_password_reset_token,
               evt_event."left" AS evt_event_left,
               evt_event.calendar AS evt_event_calendar,
               evt_event.date__finish AS evt_event_date__finish,
               evt_event.date__start AS evt_event_date__start,
               evt_event.detail AS evt_event_detail,
               evt_event.pid AS evt_event_pid,
               evt_event.short_title AS evt_event_short_title,
               evt_event.time__finish AS evt_event_time__finish,
               evt_event.time__start AS evt_event_time__start,
               evt_event_occurs."left" AS evt_event_occurs_left,
               evt_event_occurs.date AS evt_event_occurs_date,
               evt_event_occurs.pid AS evt_event_occurs_pid,
               evt_event_occurs.time__finish AS evt_event_occurs_time__finish,
               evt_event_occurs.time__start AS evt_event_occurs_time__start,
               evt_recurrence_rule."desc" AS evt_recurrence_rule_desc,
               evt_recurrence_rule."left" AS evt_recurrence_rule_left,
               evt_recurrence_rule.count AS evt_recurrence_rule_count,
               evt_recurrence_rule.easter_offset AS evt_recurrence_rule_easter_offset,
               evt_recurrence_rule.finish AS evt_recurrence_rule_finish,
               evt_recurrence_rule.is_exception AS evt_recurrence_rule_is_exception,
               evt_recurrence_rule.month AS evt_recurrence_rule_month,
               evt_recurrence_rule.month_day AS evt_recurrence_rule_month_day,
               evt_recurrence_rule.period AS evt_recurrence_rule_period,
               evt_recurrence_rule.pid AS evt_recurrence_rule_pid,
               evt_recurrence_rule.restrict_pos AS evt_recurrence_rule_restrict_pos,
               evt_recurrence_rule.start AS evt_recurrence_rule_start,
               evt_recurrence_rule.unit AS evt_recurrence_rule_unit,
               evt_recurrence_rule.week AS evt_recurrence_rule_week,
               evt_recurrence_rule.week_day AS evt_recurrence_rule_week_day,
               evt_recurrence_rule.year_day AS evt_recurrence_rule_year_day,
               evt_recurrence_spec."left" AS evt_recurrence_spec_left,
               evt_recurrence_spec.date_exceptions AS evt_recurrence_spec_date_exceptions,
               evt_recurrence_spec.dates AS evt_recurrence_spec_dates,
               evt_recurrence_spec.pid AS evt_recurrence_spec_pid,
               mom_id_entity.electric AS mom_id_entity_electric,
               mom_id_entity.last_cid AS mom_id_entity_last_cid,
               mom_id_entity.pid AS mom_id_entity_pid,
               mom_id_entity.type_name AS mom_id_entity_type_name,
               mom_id_entity.x_locked AS mom_id_entity_x_locked,
               pap_address_position."left" AS pap_address_position_left,
               pap_address_position.pid AS pap_address_position_pid,
               pap_address_position.position____raw_lat AS pap_address_position_position____raw_lat,
               pap_address_position.position____raw_lon AS pap_address_position_position____raw_lon,
               pap_address_position.position__height AS pap_address_position_position__height,
               pap_address_position.position__lat AS pap_address_position_position__lat,
               pap_address_position.position__lon AS pap_address_position_position__lon,
               pap_person_has_account."left" AS pap_person_has_account_left,
               pap_person_has_account."right" AS pap_person_has_account_right,
               pap_person_has_account.pid AS pap_person_has_account_pid,
               pap_subject_has_phone.extension AS pap_subject_has_phone_extension,
               pap_subject_has_phone.pid AS pap_subject_has_phone_pid,
               pap_subject_has_property."desc" AS pap_subject_has_property_desc,
               pap_subject_has_property."left" AS pap_subject_has_property_left,
               pap_subject_has_property."right" AS pap_subject_has_property_right,
               pap_subject_has_property.pid AS pap_subject_has_property_pid,
               srm_boat."left" AS srm_boat_left,
               srm_boat.__raw_sail_number AS srm_boat___raw_sail_number,
               srm_boat.__raw_sail_number_x AS srm_boat___raw_sail_number_x,
               srm_boat.name AS srm_boat_name,
               srm_boat.nation AS srm_boat_nation,
               srm_boat.pid AS srm_boat_pid,
               srm_boat.sail_number AS srm_boat_sail_number,
               srm_boat.sail_number_x AS srm_boat_sail_number_x,
               srm_boat_in_regatta."left" AS srm_boat_in_regatta_left,
               srm_boat_in_regatta."right" AS srm_boat_in_regatta_right,
               srm_boat_in_regatta.pid AS srm_boat_in_regatta_pid,
               srm_boat_in_regatta.place AS srm_boat_in_regatta_place,
               srm_boat_in_regatta.points AS srm_boat_in_regatta_points,
               srm_boat_in_regatta.rank AS srm_boat_in_regatta_rank,
               srm_boat_in_regatta.registration_date AS srm_boat_in_regatta_registration_date,
               srm_boat_in_regatta.skipper AS srm_boat_in_regatta_skipper,
               srm_crew_member."left" AS srm_crew_member_left,
               srm_crew_member."right" AS srm_crew_member_right,
               srm_crew_member.key AS srm_crew_member_key,
               srm_crew_member.pid AS srm_crew_member_pid,
               srm_crew_member.role AS srm_crew_member_role,
               srm_race_result."left" AS srm_race_result_left,
               srm_race_result.discarded AS srm_race_result_discarded,
               srm_race_result.pid AS srm_race_result_pid,
               srm_race_result.points AS srm_race_result_points,
               srm_race_result.race AS srm_race_result_race,
               srm_race_result.status AS srm_race_result_status,
               srm_regatta."left" AS srm_regatta_left,
               srm_regatta.boat_class AS srm_regatta_boat_class,
               srm_regatta.discards AS srm_regatta_discards,
               srm_regatta.is_cancelled AS srm_regatta_is_cancelled,
               srm_regatta.kind AS srm_regatta_kind,
               srm_regatta.perma_name AS srm_regatta_perma_name,
               srm_regatta.pid AS srm_regatta_pid,
               srm_regatta.races AS srm_regatta_races,
               srm_regatta.result__date AS srm_regatta_result__date,
               srm_regatta.result__software AS srm_regatta_result__software,
               srm_regatta.result__status AS srm_regatta_result__status,
               srm_regatta_c.is_team_race AS srm_regatta_c_is_team_race,
               srm_regatta_c.pid AS srm_regatta_c_pid,
               srm_sailor."left" AS srm_sailor_left,
               srm_sailor.__raw_mna_number AS srm_sailor___raw_mna_number,
               srm_sailor.club AS srm_sailor_club,
               srm_sailor.mna_number AS srm_sailor_mna_number,
               srm_sailor.nation AS srm_sailor_nation,
               srm_sailor.pid AS srm_sailor_pid,
               srm_team."desc" AS srm_team_desc,
               srm_team."left" AS srm_team_left,
               srm_team.__raw_name AS srm_team___raw_name,
               srm_team.club AS srm_team_club,
               srm_team.leader AS srm_team_leader,
               srm_team.name AS srm_team_name,
               srm_team.pid AS srm_team_pid,
               srm_team.place AS srm_team_place,
               srm_team.registration_date AS srm_team_registration_date,
               srm_team_has_boat_in_regatta."left" AS srm_team_has_boat_in_regatta_left,
               srm_team_has_boat_in_regatta."right" AS srm_team_has_boat_in_regatta_right,
               srm_team_has_boat_in_regatta.pid AS srm_team_has_boat_in_regatta_pid,
               swp_clip_o."left" AS swp_clip_o_left,
               swp_clip_o.abstract AS swp_clip_o_abstract,
               swp_clip_o.contents AS swp_clip_o_contents,
               swp_clip_o.date__finish AS swp_clip_o_date__finish,
               swp_clip_o.date__start AS swp_clip_o_date__start,
               swp_clip_o.date_x__finish AS swp_clip_o_date_x__finish,
               swp_clip_o.date_x__start AS swp_clip_o_date_x__start,
               swp_clip_o.pid AS swp_clip_o_pid,
               swp_clip_o.prio AS swp_clip_o_prio,
               swp_picture."left" AS swp_picture_left,
               swp_picture.name AS swp_picture_name,
               swp_picture.number AS swp_picture_number,
               swp_picture.photo__extension AS swp_picture_photo__extension,
               swp_picture.photo__height AS swp_picture_photo__height,
               swp_picture.photo__width AS swp_picture_photo__width,
               swp_picture.pid AS swp_picture_pid,
               swp_picture.thumb__extension AS swp_picture_thumb__extension,
               swp_picture.thumb__height AS swp_picture_thumb__height,
               swp_picture.thumb__width AS swp_picture_thumb__width
        FROM mom_id_entity
           LEFT OUTER JOIN auth_account_in_group ON mom_id_entity.pid = auth_account_in_group.pid
           LEFT OUTER JOIN auth_account_activation ON mom_id_entity.pid = auth_account_activation.pid
           LEFT OUTER JOIN auth_account_password_change_required ON mom_id_entity.pid = auth_account_password_change_required.pid
           LEFT OUTER JOIN auth_account_email_verification ON mom_id_entity.pid = auth_account_email_verification.pid
           LEFT OUTER JOIN auth_account_password_reset ON mom_id_entity.pid = auth_account_password_reset.pid
           LEFT OUTER JOIN evt_event ON mom_id_entity.pid = evt_event.pid
           LEFT OUTER JOIN evt_event_occurs ON mom_id_entity.pid = evt_event_occurs.pid
           LEFT OUTER JOIN evt_recurrence_spec ON mom_id_entity.pid = evt_recurrence_spec.pid
           LEFT OUTER JOIN evt_recurrence_rule ON mom_id_entity.pid = evt_recurrence_rule.pid
           LEFT OUTER JOIN pap_address_position ON mom_id_entity.pid = pap_address_position.pid
           LEFT OUTER JOIN pap_subject_has_property ON mom_id_entity.pid = pap_subject_has_property.pid
           LEFT OUTER JOIN pap_subject_has_phone ON pap_subject_has_property.pid = pap_subject_has_phone.pid
           LEFT OUTER JOIN pap_person_has_account ON mom_id_entity.pid = pap_person_has_account.pid
           LEFT OUTER JOIN srm_boat ON mom_id_entity.pid = srm_boat.pid
           LEFT OUTER JOIN swp_clip_o ON mom_id_entity.pid = swp_clip_o.pid
           LEFT OUTER JOIN swp_picture ON mom_id_entity.pid = swp_picture.pid
           LEFT OUTER JOIN srm_regatta ON mom_id_entity.pid = srm_regatta.pid
           LEFT OUTER JOIN srm_regatta_c ON srm_regatta.pid = srm_regatta_c.pid
           LEFT OUTER JOIN srm_sailor ON mom_id_entity.pid = srm_sailor.pid
           LEFT OUTER JOIN srm_boat_in_regatta ON mom_id_entity.pid = srm_boat_in_regatta.pid
           LEFT OUTER JOIN srm_race_result ON mom_id_entity.pid = srm_race_result.pid
           LEFT OUTER JOIN srm_team ON mom_id_entity.pid = srm_team.pid
           LEFT OUTER JOIN srm_crew_member ON mom_id_entity.pid = srm_crew_member.pid
           LEFT OUTER JOIN srm_team_has_boat_in_regatta ON mom_id_entity.pid = srm_team_has_boat_in_regatta.pid
        WHERE mom_id_entity.pid = auth_account_in_group.pid
            OR mom_id_entity.pid = auth_account_activation.pid
            OR mom_id_entity.pid = auth_account_password_change_required.pid
            OR mom_id_entity.pid = auth_account_email_verification.pid
            OR mom_id_entity.pid = auth_account_password_reset.pid
            OR mom_id_entity.pid = evt_event.pid
            OR mom_id_entity.pid = evt_event_occurs.pid
            OR mom_id_entity.pid = evt_recurrence_spec.pid
            OR mom_id_entity.pid = evt_recurrence_rule.pid
            OR mom_id_entity.pid = pap_address_position.pid
            OR mom_id_entity.pid = pap_subject_has_property.pid
            OR mom_id_entity.pid = pap_subject_has_phone.pid
            OR mom_id_entity.pid = pap_person_has_account.pid
            OR mom_id_entity.pid = srm_boat.pid
            OR mom_id_entity.pid = swp_clip_o.pid
            OR mom_id_entity.pid = swp_picture.pid
            OR mom_id_entity.pid = srm_regatta.pid
            OR mom_id_entity.pid = srm_regatta_c.pid
            OR mom_id_entity.pid = srm_sailor.pid
            OR mom_id_entity.pid = srm_boat_in_regatta.pid
            OR mom_id_entity.pid = srm_race_result.pid
            OR mom_id_entity.pid = srm_team.pid
            OR mom_id_entity.pid = srm_crew_member.pid
            OR mom_id_entity.pid = srm_team_has_boat_in_regatta.pid
    MOM.Link1
        SELECT auth_account_activation."left" AS auth_account_activation_left,
               auth_account_activation.pid AS auth_account_activation_pid,
               auth_account_email_verification."left" AS auth_account_email_verification_left,
               auth_account_email_verification.expires AS auth_account_email_verification_expires,
               auth_account_email_verification.new_email AS auth_account_email_verification_new_email,
               auth_account_email_verification.pid AS auth_account_email_verification_pid,
               auth_account_email_verification.token AS auth_account_email_verification_token,
               auth_account_password_change_required."left" AS auth_account_password_change_required_left,
               auth_account_password_change_required.pid AS auth_account_password_change_required_pid,
               auth_account_password_reset."left" AS auth_account_password_reset_left,
               auth_account_password_reset.expires AS auth_account_password_reset_expires,
               auth_account_password_reset.password AS auth_account_password_reset_password,
               auth_account_password_reset.pid AS auth_account_password_reset_pid,
               auth_account_password_reset.token AS auth_account_password_reset_token,
               evt_event."left" AS evt_event_left,
               evt_event.calendar AS evt_event_calendar,
               evt_event.date__finish AS evt_event_date__finish,
               evt_event.date__start AS evt_event_date__start,
               evt_event.detail AS evt_event_detail,
               evt_event.pid AS evt_event_pid,
               evt_event.short_title AS evt_event_short_title,
               evt_event.time__finish AS evt_event_time__finish,
               evt_event.time__start AS evt_event_time__start,
               evt_event_occurs."left" AS evt_event_occurs_left,
               evt_event_occurs.date AS evt_event_occurs_date,
               evt_event_occurs.pid AS evt_event_occurs_pid,
               evt_event_occurs.time__finish AS evt_event_occurs_time__finish,
               evt_event_occurs.time__start AS evt_event_occurs_time__start,
               evt_recurrence_rule."desc" AS evt_recurrence_rule_desc,
               evt_recurrence_rule."left" AS evt_recurrence_rule_left,
               evt_recurrence_rule.count AS evt_recurrence_rule_count,
               evt_recurrence_rule.easter_offset AS evt_recurrence_rule_easter_offset,
               evt_recurrence_rule.finish AS evt_recurrence_rule_finish,
               evt_recurrence_rule.is_exception AS evt_recurrence_rule_is_exception,
               evt_recurrence_rule.month AS evt_recurrence_rule_month,
               evt_recurrence_rule.month_day AS evt_recurrence_rule_month_day,
               evt_recurrence_rule.period AS evt_recurrence_rule_period,
               evt_recurrence_rule.pid AS evt_recurrence_rule_pid,
               evt_recurrence_rule.restrict_pos AS evt_recurrence_rule_restrict_pos,
               evt_recurrence_rule.start AS evt_recurrence_rule_start,
               evt_recurrence_rule.unit AS evt_recurrence_rule_unit,
               evt_recurrence_rule.week AS evt_recurrence_rule_week,
               evt_recurrence_rule.week_day AS evt_recurrence_rule_week_day,
               evt_recurrence_rule.year_day AS evt_recurrence_rule_year_day,
               evt_recurrence_spec."left" AS evt_recurrence_spec_left,
               evt_recurrence_spec.date_exceptions AS evt_recurrence_spec_date_exceptions,
               evt_recurrence_spec.dates AS evt_recurrence_spec_dates,
               evt_recurrence_spec.pid AS evt_recurrence_spec_pid,
               mom_id_entity.electric AS mom_id_entity_electric,
               mom_id_entity.last_cid AS mom_id_entity_last_cid,
               mom_id_entity.pid AS mom_id_entity_pid,
               mom_id_entity.type_name AS mom_id_entity_type_name,
               mom_id_entity.x_locked AS mom_id_entity_x_locked,
               pap_address_position."left" AS pap_address_position_left,
               pap_address_position.pid AS pap_address_position_pid,
               pap_address_position.position____raw_lat AS pap_address_position_position____raw_lat,
               pap_address_position.position____raw_lon AS pap_address_position_position____raw_lon,
               pap_address_position.position__height AS pap_address_position_position__height,
               pap_address_position.position__lat AS pap_address_position_position__lat,
               pap_address_position.position__lon AS pap_address_position_position__lon,
               srm_boat."left" AS srm_boat_left,
               srm_boat.__raw_sail_number AS srm_boat___raw_sail_number,
               srm_boat.__raw_sail_number_x AS srm_boat___raw_sail_number_x,
               srm_boat.name AS srm_boat_name,
               srm_boat.nation AS srm_boat_nation,
               srm_boat.pid AS srm_boat_pid,
               srm_boat.sail_number AS srm_boat_sail_number,
               srm_boat.sail_number_x AS srm_boat_sail_number_x,
               srm_race_result."left" AS srm_race_result_left,
               srm_race_result.discarded AS srm_race_result_discarded,
               srm_race_result.pid AS srm_race_result_pid,
               srm_race_result.points AS srm_race_result_points,
               srm_race_result.race AS srm_race_result_race,
               srm_race_result.status AS srm_race_result_status,
               srm_regatta."left" AS srm_regatta_left,
               srm_regatta.boat_class AS srm_regatta_boat_class,
               srm_regatta.discards AS srm_regatta_discards,
               srm_regatta.is_cancelled AS srm_regatta_is_cancelled,
               srm_regatta.kind AS srm_regatta_kind,
               srm_regatta.perma_name AS srm_regatta_perma_name,
               srm_regatta.pid AS srm_regatta_pid,
               srm_regatta.races AS srm_regatta_races,
               srm_regatta.result__date AS srm_regatta_result__date,
               srm_regatta.result__software AS srm_regatta_result__software,
               srm_regatta.result__status AS srm_regatta_result__status,
               srm_regatta_c.is_team_race AS srm_regatta_c_is_team_race,
               srm_regatta_c.pid AS srm_regatta_c_pid,
               srm_sailor."left" AS srm_sailor_left,
               srm_sailor.__raw_mna_number AS srm_sailor___raw_mna_number,
               srm_sailor.club AS srm_sailor_club,
               srm_sailor.mna_number AS srm_sailor_mna_number,
               srm_sailor.nation AS srm_sailor_nation,
               srm_sailor.pid AS srm_sailor_pid,
               srm_team."desc" AS srm_team_desc,
               srm_team."left" AS srm_team_left,
               srm_team.__raw_name AS srm_team___raw_name,
               srm_team.club AS srm_team_club,
               srm_team.leader AS srm_team_leader,
               srm_team.name AS srm_team_name,
               srm_team.pid AS srm_team_pid,
               srm_team.place AS srm_team_place,
               srm_team.registration_date AS srm_team_registration_date,
               swp_clip_o."left" AS swp_clip_o_left,
               swp_clip_o.abstract AS swp_clip_o_abstract,
               swp_clip_o.contents AS swp_clip_o_contents,
               swp_clip_o.date__finish AS swp_clip_o_date__finish,
               swp_clip_o.date__start AS swp_clip_o_date__start,
               swp_clip_o.date_x__finish AS swp_clip_o_date_x__finish,
               swp_clip_o.date_x__start AS swp_clip_o_date_x__start,
               swp_clip_o.pid AS swp_clip_o_pid,
               swp_clip_o.prio AS swp_clip_o_prio,
               swp_picture."left" AS swp_picture_left,
               swp_picture.name AS swp_picture_name,
               swp_picture.number AS swp_picture_number,
               swp_picture.photo__extension AS swp_picture_photo__extension,
               swp_picture.photo__height AS swp_picture_photo__height,
               swp_picture.photo__width AS swp_picture_photo__width,
               swp_picture.pid AS swp_picture_pid,
               swp_picture.thumb__extension AS swp_picture_thumb__extension,
               swp_picture.thumb__height AS swp_picture_thumb__height,
               swp_picture.thumb__width AS swp_picture_thumb__width
        FROM mom_id_entity
           LEFT OUTER JOIN auth_account_activation ON mom_id_entity.pid = auth_account_activation.pid
           LEFT OUTER JOIN auth_account_password_change_required ON mom_id_entity.pid = auth_account_password_change_required.pid
           LEFT OUTER JOIN auth_account_email_verification ON mom_id_entity.pid = auth_account_email_verification.pid
           LEFT OUTER JOIN auth_account_password_reset ON mom_id_entity.pid = auth_account_password_reset.pid
           LEFT OUTER JOIN evt_event ON mom_id_entity.pid = evt_event.pid
           LEFT OUTER JOIN evt_event_occurs ON mom_id_entity.pid = evt_event_occurs.pid
           LEFT OUTER JOIN evt_recurrence_spec ON mom_id_entity.pid = evt_recurrence_spec.pid
           LEFT OUTER JOIN evt_recurrence_rule ON mom_id_entity.pid = evt_recurrence_rule.pid
           LEFT OUTER JOIN pap_address_position ON mom_id_entity.pid = pap_address_position.pid
           LEFT OUTER JOIN srm_boat ON mom_id_entity.pid = srm_boat.pid
           LEFT OUTER JOIN swp_clip_o ON mom_id_entity.pid = swp_clip_o.pid
           LEFT OUTER JOIN swp_picture ON mom_id_entity.pid = swp_picture.pid
           LEFT OUTER JOIN srm_regatta ON mom_id_entity.pid = srm_regatta.pid
           LEFT OUTER JOIN srm_regatta_c ON srm_regatta.pid = srm_regatta_c.pid
           LEFT OUTER JOIN srm_sailor ON mom_id_entity.pid = srm_sailor.pid
           LEFT OUTER JOIN srm_race_result ON mom_id_entity.pid = srm_race_result.pid
           LEFT OUTER JOIN srm_team ON mom_id_entity.pid = srm_team.pid
        WHERE mom_id_entity.pid = auth_account_activation.pid
            OR mom_id_entity.pid = auth_account_password_change_required.pid
            OR mom_id_entity.pid = auth_account_email_verification.pid
            OR mom_id_entity.pid = auth_account_password_reset.pid
            OR mom_id_entity.pid = evt_event.pid
            OR mom_id_entity.pid = evt_event_occurs.pid
            OR mom_id_entity.pid = evt_recurrence_spec.pid
            OR mom_id_entity.pid = evt_recurrence_rule.pid
            OR mom_id_entity.pid = pap_address_position.pid
            OR mom_id_entity.pid = srm_boat.pid
            OR mom_id_entity.pid = swp_clip_o.pid
            OR mom_id_entity.pid = swp_picture.pid
            OR mom_id_entity.pid = srm_regatta.pid
            OR mom_id_entity.pid = srm_regatta_c.pid
            OR mom_id_entity.pid = srm_sailor.pid
            OR mom_id_entity.pid = srm_race_result.pid
            OR mom_id_entity.pid = srm_team.pid
    MOM._MOM_Link_n_
        SELECT auth_account_in_group."left" AS auth_account_in_group_left,
               auth_account_in_group."right" AS auth_account_in_group_right,
               auth_account_in_group.pid AS auth_account_in_group_pid,
               mom_id_entity.electric AS mom_id_entity_electric,
               mom_id_entity.last_cid AS mom_id_entity_last_cid,
               mom_id_entity.pid AS mom_id_entity_pid,
               mom_id_entity.type_name AS mom_id_entity_type_name,
               mom_id_entity.x_locked AS mom_id_entity_x_locked,
               pap_person_has_account."left" AS pap_person_has_account_left,
               pap_person_has_account."right" AS pap_person_has_account_right,
               pap_person_has_account.pid AS pap_person_has_account_pid,
               pap_subject_has_phone.extension AS pap_subject_has_phone_extension,
               pap_subject_has_phone.pid AS pap_subject_has_phone_pid,
               pap_subject_has_property."desc" AS pap_subject_has_property_desc,
               pap_subject_has_property."left" AS pap_subject_has_property_left,
               pap_subject_has_property."right" AS pap_subject_has_property_right,
               pap_subject_has_property.pid AS pap_subject_has_property_pid,
               srm_boat_in_regatta."left" AS srm_boat_in_regatta_left,
               srm_boat_in_regatta."right" AS srm_boat_in_regatta_right,
               srm_boat_in_regatta.pid AS srm_boat_in_regatta_pid,
               srm_boat_in_regatta.place AS srm_boat_in_regatta_place,
               srm_boat_in_regatta.points AS srm_boat_in_regatta_points,
               srm_boat_in_regatta.rank AS srm_boat_in_regatta_rank,
               srm_boat_in_regatta.registration_date AS srm_boat_in_regatta_registration_date,
               srm_boat_in_regatta.skipper AS srm_boat_in_regatta_skipper,
               srm_crew_member."left" AS srm_crew_member_left,
               srm_crew_member."right" AS srm_crew_member_right,
               srm_crew_member.key AS srm_crew_member_key,
               srm_crew_member.pid AS srm_crew_member_pid,
               srm_crew_member.role AS srm_crew_member_role,
               srm_team_has_boat_in_regatta."left" AS srm_team_has_boat_in_regatta_left,
               srm_team_has_boat_in_regatta."right" AS srm_team_has_boat_in_regatta_right,
               srm_team_has_boat_in_regatta.pid AS srm_team_has_boat_in_regatta_pid
        FROM mom_id_entity
           LEFT OUTER JOIN auth_account_in_group ON mom_id_entity.pid = auth_account_in_group.pid
           LEFT OUTER JOIN pap_subject_has_property ON mom_id_entity.pid = pap_subject_has_property.pid
           LEFT OUTER JOIN pap_subject_has_phone ON pap_subject_has_property.pid = pap_subject_has_phone.pid
           LEFT OUTER JOIN pap_person_has_account ON mom_id_entity.pid = pap_person_has_account.pid
           LEFT OUTER JOIN srm_boat_in_regatta ON mom_id_entity.pid = srm_boat_in_regatta.pid
           LEFT OUTER JOIN srm_crew_member ON mom_id_entity.pid = srm_crew_member.pid
           LEFT OUTER JOIN srm_team_has_boat_in_regatta ON mom_id_entity.pid = srm_team_has_boat_in_regatta.pid
        WHERE mom_id_entity.pid = auth_account_in_group.pid
            OR mom_id_entity.pid = pap_subject_has_property.pid
            OR mom_id_entity.pid = pap_subject_has_phone.pid
            OR mom_id_entity.pid = pap_person_has_account.pid
            OR mom_id_entity.pid = srm_boat_in_regatta.pid
            OR mom_id_entity.pid = srm_crew_member.pid
            OR mom_id_entity.pid = srm_team_has_boat_in_regatta.pid
    MOM.Link2
        SELECT auth_account_in_group."left" AS auth_account_in_group_left,
               auth_account_in_group."right" AS auth_account_in_group_right,
               auth_account_in_group.pid AS auth_account_in_group_pid,
               mom_id_entity.electric AS mom_id_entity_electric,
               mom_id_entity.last_cid AS mom_id_entity_last_cid,
               mom_id_entity.pid AS mom_id_entity_pid,
               mom_id_entity.type_name AS mom_id_entity_type_name,
               mom_id_entity.x_locked AS mom_id_entity_x_locked,
               pap_person_has_account."left" AS pap_person_has_account_left,
               pap_person_has_account."right" AS pap_person_has_account_right,
               pap_person_has_account.pid AS pap_person_has_account_pid,
               pap_subject_has_phone.extension AS pap_subject_has_phone_extension,
               pap_subject_has_phone.pid AS pap_subject_has_phone_pid,
               pap_subject_has_property."desc" AS pap_subject_has_property_desc,
               pap_subject_has_property."left" AS pap_subject_has_property_left,
               pap_subject_has_property."right" AS pap_subject_has_property_right,
               pap_subject_has_property.pid AS pap_subject_has_property_pid,
               srm_boat_in_regatta."left" AS srm_boat_in_regatta_left,
               srm_boat_in_regatta."right" AS srm_boat_in_regatta_right,
               srm_boat_in_regatta.pid AS srm_boat_in_regatta_pid,
               srm_boat_in_regatta.place AS srm_boat_in_regatta_place,
               srm_boat_in_regatta.points AS srm_boat_in_regatta_points,
               srm_boat_in_regatta.rank AS srm_boat_in_regatta_rank,
               srm_boat_in_regatta.registration_date AS srm_boat_in_regatta_registration_date,
               srm_boat_in_regatta.skipper AS srm_boat_in_regatta_skipper,
               srm_crew_member."left" AS srm_crew_member_left,
               srm_crew_member."right" AS srm_crew_member_right,
               srm_crew_member.key AS srm_crew_member_key,
               srm_crew_member.pid AS srm_crew_member_pid,
               srm_crew_member.role AS srm_crew_member_role,
               srm_team_has_boat_in_regatta."left" AS srm_team_has_boat_in_regatta_left,
               srm_team_has_boat_in_regatta."right" AS srm_team_has_boat_in_regatta_right,
               srm_team_has_boat_in_regatta.pid AS srm_team_has_boat_in_regatta_pid
        FROM mom_id_entity
           LEFT OUTER JOIN auth_account_in_group ON mom_id_entity.pid = auth_account_in_group.pid
           LEFT OUTER JOIN pap_subject_has_property ON mom_id_entity.pid = pap_subject_has_property.pid
           LEFT OUTER JOIN pap_subject_has_phone ON pap_subject_has_property.pid = pap_subject_has_phone.pid
           LEFT OUTER JOIN pap_person_has_account ON mom_id_entity.pid = pap_person_has_account.pid
           LEFT OUTER JOIN srm_boat_in_regatta ON mom_id_entity.pid = srm_boat_in_regatta.pid
           LEFT OUTER JOIN srm_crew_member ON mom_id_entity.pid = srm_crew_member.pid
           LEFT OUTER JOIN srm_team_has_boat_in_regatta ON mom_id_entity.pid = srm_team_has_boat_in_regatta.pid
        WHERE mom_id_entity.pid = auth_account_in_group.pid
            OR mom_id_entity.pid = pap_subject_has_property.pid
            OR mom_id_entity.pid = pap_subject_has_phone.pid
            OR mom_id_entity.pid = pap_person_has_account.pid
            OR mom_id_entity.pid = srm_boat_in_regatta.pid
            OR mom_id_entity.pid = srm_crew_member.pid
            OR mom_id_entity.pid = srm_team_has_boat_in_regatta.pid
    MOM.Object
        SELECT auth__account_.enabled AS auth__account__enabled,
               auth__account_.name AS auth__account__name,
               auth__account_.pid AS auth__account__pid,
               auth__account_.superuser AS auth__account__superuser,
               auth__account_.suspended AS auth__account__suspended,
               auth_account.password AS auth_account_password,
               auth_account.ph_name AS auth_account_ph_name,
               auth_account.pid AS auth_account_pid,
               auth_certificate."desc" AS auth_certificate_desc,
               auth_certificate.cert_id AS auth_certificate_cert_id,
               auth_certificate.email AS auth_certificate_email,
               auth_certificate.pem AS auth_certificate_pem,
               auth_certificate.pid AS auth_certificate_pid,
               auth_certificate.revocation_date AS auth_certificate_revocation_date,
               auth_certificate.validity__finish AS auth_certificate_validity__finish,
               auth_certificate.validity__start AS auth_certificate_validity__start,
               auth_group."desc" AS auth_group_desc,
               auth_group.name AS auth_group_name,
               auth_group.pid AS auth_group_pid,
               evt_calendar."desc" AS evt_calendar_desc,
               evt_calendar.name AS evt_calendar_name,
               evt_calendar.pid AS evt_calendar_pid,
               mom_id_entity.electric AS mom_id_entity_electric,
               mom_id_entity.last_cid AS mom_id_entity_last_cid,
               mom_id_entity.pid AS mom_id_entity_pid,
               mom_id_entity.type_name AS mom_id_entity_type_name,
               mom_id_entity.x_locked AS mom_id_entity_x_locked,
               pap_address."desc" AS pap_address_desc,
               pap_address.__raw_city AS pap_address___raw_city,
               pap_address.__raw_country AS pap_address___raw_country,
               pap_address.__raw_region AS pap_address___raw_region,
               pap_address.__raw_street AS pap_address___raw_street,
               pap_address.__raw_zip AS pap_address___raw_zip,
               pap_address.city AS pap_address_city,
               pap_address.country AS pap_address_country,
               pap_address.pid AS pap_address_pid,
               pap_address.region AS pap_address_region,
               pap_address.street AS pap_address_street,
               pap_address.zip AS pap_address_zip,
               pap_company.__raw_name AS pap_company___raw_name,
               pap_company.__raw_registered_in AS pap_company___raw_registered_in,
               pap_company.__raw_short_name AS pap_company___raw_short_name,
               pap_company.lifetime__finish AS pap_company_lifetime__finish,
               pap_company.lifetime__start AS pap_company_lifetime__start,
               pap_company.name AS pap_company_name,
               pap_company.pid AS pap_company_pid,
               pap_company.registered_in AS pap_company_registered_in,
               pap_company.short_name AS pap_company_short_name,
               pap_email."desc" AS pap_email_desc,
               pap_email.__raw_address AS pap_email___raw_address,
               pap_email.address AS pap_email_address,
               pap_email.pid AS pap_email_pid,
               pap_person.__raw_first_name AS pap_person___raw_first_name,
               pap_person.__raw_last_name AS pap_person___raw_last_name,
               pap_person.__raw_middle_name AS pap_person___raw_middle_name,
               pap_person.__raw_title AS pap_person___raw_title,
               pap_person.first_name AS pap_person_first_name,
               pap_person.last_name AS pap_person_last_name,
               pap_person.lifetime__finish AS pap_person_lifetime__finish,
               pap_person.lifetime__start AS pap_person_lifetime__start,
               pap_person.middle_name AS pap_person_middle_name,
               pap_person.pid AS pap_person_pid,
               pap_person.sex AS pap_person_sex,
               pap_person.title AS pap_person_title,
               pap_phone."desc" AS pap_phone_desc,
               pap_phone.area_code AS pap_phone_area_code,
               pap_phone.country_code AS pap_phone_country_code,
               pap_phone.number AS pap_phone_number,
               pap_phone.pid AS pap_phone_pid,
               pap_url."desc" AS pap_url_desc,
               pap_url.pid AS pap_url_pid,
               pap_url.value AS pap_url_value,
               srm__boat_class_.__raw_name AS srm__boat_class____raw_name,
               srm__boat_class_.name AS srm__boat_class__name,
               srm__boat_class_.pid AS srm__boat_class__pid,
               srm_boat_class.beam AS srm_boat_class_beam,
               srm_boat_class.loa AS srm_boat_class_loa,
               srm_boat_class.max_crew AS srm_boat_class_max_crew,
               srm_boat_class.pid AS srm_boat_class_pid,
               srm_boat_class.sail_area AS srm_boat_class_sail_area,
               srm_club.__raw_name AS srm_club___raw_name,
               srm_club.long_name AS srm_club_long_name,
               srm_club.name AS srm_club_name,
               srm_club.pid AS srm_club_pid,
               srm_page."desc" AS srm_page_desc,
               srm_page.event AS srm_page_event,
               srm_page.pid AS srm_page_pid,
               srm_regatta_event."desc" AS srm_regatta_event_desc,
               srm_regatta_event.__raw_name AS srm_regatta_event___raw_name,
               srm_regatta_event.club AS srm_regatta_event_club,
               srm_regatta_event.date__finish AS srm_regatta_event_date__finish,
               srm_regatta_event.date__start AS srm_regatta_event_date__start,
               srm_regatta_event.is_cancelled AS srm_regatta_event_is_cancelled,
               srm_regatta_event.name AS srm_regatta_event_name,
               srm_regatta_event.perma_name AS srm_regatta_event_perma_name,
               srm_regatta_event.pid AS srm_regatta_event_pid,
               swp_clip_x.link_to AS swp_clip_x_link_to,
               swp_clip_x.pid AS swp_clip_x_pid,
               swp_gallery.date__finish AS swp_gallery_date__finish,
               swp_gallery.date__start AS swp_gallery_date__start,
               swp_gallery.directory AS swp_gallery_directory,
               swp_gallery.perma_name AS swp_gallery_perma_name,
               swp_gallery.pid AS swp_gallery_pid,
               swp_gallery.short_title AS swp_gallery_short_title,
               swp_gallery.title AS swp_gallery_title,
               swp_page.contents AS swp_page_contents,
               swp_page.date__finish AS swp_page_date__finish,
               swp_page.date__start AS swp_page_date__start,
               swp_page.format AS swp_page_format,
               swp_page.head_line AS swp_page_head_line,
               swp_page.hidden AS swp_page_hidden,
               swp_page.perma_name AS swp_page_perma_name,
               swp_page.pid AS swp_page_pid,
               swp_page.prio AS swp_page_prio,
               swp_page.short_title AS swp_page_short_title,
               swp_page.text AS swp_page_text,
               swp_page.title AS swp_page_title,
               swp_page_y.pid AS swp_page_y_pid,
               swp_page_y.year AS swp_page_y_year
        FROM mom_id_entity
           LEFT OUTER JOIN auth__account_ ON mom_id_entity.pid = auth__account_.pid
           LEFT OUTER JOIN auth_account ON auth__account_.pid = auth_account.pid
           LEFT OUTER JOIN auth_certificate ON mom_id_entity.pid = auth_certificate.pid
           LEFT OUTER JOIN auth_group ON mom_id_entity.pid = auth_group.pid
           LEFT OUTER JOIN evt_calendar ON mom_id_entity.pid = evt_calendar.pid
           LEFT OUTER JOIN swp_page ON mom_id_entity.pid = swp_page.pid
           LEFT OUTER JOIN swp_page_y ON swp_page.pid = swp_page_y.pid
           LEFT OUTER JOIN swp_clip_x ON swp_page.pid = swp_clip_x.pid
           LEFT OUTER JOIN srm_page ON swp_page.pid = srm_page.pid
           LEFT OUTER JOIN pap_address ON mom_id_entity.pid = pap_address.pid
           LEFT OUTER JOIN pap_company ON mom_id_entity.pid = pap_company.pid
           LEFT OUTER JOIN pap_email ON mom_id_entity.pid = pap_email.pid
           LEFT OUTER JOIN pap_phone ON mom_id_entity.pid = pap_phone.pid
           LEFT OUTER JOIN pap_person ON mom_id_entity.pid = pap_person.pid
           LEFT OUTER JOIN pap_url ON mom_id_entity.pid = pap_url.pid
           LEFT OUTER JOIN srm__boat_class_ ON mom_id_entity.pid = srm__boat_class_.pid
           LEFT OUTER JOIN srm_boat_class ON srm__boat_class_.pid = srm_boat_class.pid
           LEFT OUTER JOIN srm_club ON mom_id_entity.pid = srm_club.pid
           LEFT OUTER JOIN srm_regatta_event ON mom_id_entity.pid = srm_regatta_event.pid
           LEFT OUTER JOIN swp_gallery ON mom_id_entity.pid = swp_gallery.pid
        WHERE mom_id_entity.pid = auth__account_.pid
            OR mom_id_entity.pid = auth_account.pid
            OR mom_id_entity.pid = auth_certificate.pid
            OR mom_id_entity.pid = auth_group.pid
            OR mom_id_entity.pid = evt_calendar.pid
            OR mom_id_entity.pid = swp_page.pid
            OR mom_id_entity.pid = swp_page_y.pid
            OR mom_id_entity.pid = swp_clip_x.pid
            OR mom_id_entity.pid = srm_page.pid
            OR mom_id_entity.pid = pap_address.pid
            OR mom_id_entity.pid = pap_company.pid
            OR mom_id_entity.pid = pap_email.pid
            OR mom_id_entity.pid = pap_phone.pid
            OR mom_id_entity.pid = pap_person.pid
            OR mom_id_entity.pid = pap_url.pid
            OR mom_id_entity.pid = srm__boat_class_.pid
            OR mom_id_entity.pid = srm_boat_class.pid
            OR mom_id_entity.pid = srm_club.pid
            OR mom_id_entity.pid = srm_regatta_event.pid
            OR mom_id_entity.pid = swp_gallery.pid
    Auth.Id_Entity
        SELECT auth__account_.enabled AS auth__account__enabled,
               auth__account_.name AS auth__account__name,
               auth__account_.pid AS auth__account__pid,
               auth__account_.superuser AS auth__account__superuser,
               auth__account_.suspended AS auth__account__suspended,
               auth_account.password AS auth_account_password,
               auth_account.ph_name AS auth_account_ph_name,
               auth_account.pid AS auth_account_pid,
               auth_account_activation."left" AS auth_account_activation_left,
               auth_account_activation.pid AS auth_account_activation_pid,
               auth_account_email_verification."left" AS auth_account_email_verification_left,
               auth_account_email_verification.expires AS auth_account_email_verification_expires,
               auth_account_email_verification.new_email AS auth_account_email_verification_new_email,
               auth_account_email_verification.pid AS auth_account_email_verification_pid,
               auth_account_email_verification.token AS auth_account_email_verification_token,
               auth_account_in_group."left" AS auth_account_in_group_left,
               auth_account_in_group."right" AS auth_account_in_group_right,
               auth_account_in_group.pid AS auth_account_in_group_pid,
               auth_account_password_change_required."left" AS auth_account_password_change_required_left,
               auth_account_password_change_required.pid AS auth_account_password_change_required_pid,
               auth_account_password_reset."left" AS auth_account_password_reset_left,
               auth_account_password_reset.expires AS auth_account_password_reset_expires,
               auth_account_password_reset.password AS auth_account_password_reset_password,
               auth_account_password_reset.pid AS auth_account_password_reset_pid,
               auth_account_password_reset.token AS auth_account_password_reset_token,
               auth_certificate."desc" AS auth_certificate_desc,
               auth_certificate.cert_id AS auth_certificate_cert_id,
               auth_certificate.email AS auth_certificate_email,
               auth_certificate.pem AS auth_certificate_pem,
               auth_certificate.pid AS auth_certificate_pid,
               auth_certificate.revocation_date AS auth_certificate_revocation_date,
               auth_certificate.validity__finish AS auth_certificate_validity__finish,
               auth_certificate.validity__start AS auth_certificate_validity__start,
               auth_group."desc" AS auth_group_desc,
               auth_group.name AS auth_group_name,
               auth_group.pid AS auth_group_pid,
               mom_id_entity.electric AS mom_id_entity_electric,
               mom_id_entity.last_cid AS mom_id_entity_last_cid,
               mom_id_entity.pid AS mom_id_entity_pid,
               mom_id_entity.type_name AS mom_id_entity_type_name,
               mom_id_entity.x_locked AS mom_id_entity_x_locked
        FROM mom_id_entity
           LEFT OUTER JOIN auth__account_ ON mom_id_entity.pid = auth__account_.pid
           LEFT OUTER JOIN auth_account ON auth__account_.pid = auth_account.pid
           LEFT OUTER JOIN auth_certificate ON mom_id_entity.pid = auth_certificate.pid
           LEFT OUTER JOIN auth_group ON mom_id_entity.pid = auth_group.pid
           LEFT OUTER JOIN auth_account_in_group ON mom_id_entity.pid = auth_account_in_group.pid
           LEFT OUTER JOIN auth_account_activation ON mom_id_entity.pid = auth_account_activation.pid
           LEFT OUTER JOIN auth_account_password_change_required ON mom_id_entity.pid = auth_account_password_change_required.pid
           LEFT OUTER JOIN auth_account_email_verification ON mom_id_entity.pid = auth_account_email_verification.pid
           LEFT OUTER JOIN auth_account_password_reset ON mom_id_entity.pid = auth_account_password_reset.pid
        WHERE mom_id_entity.pid = auth__account_.pid
            OR mom_id_entity.pid = auth_account.pid
            OR mom_id_entity.pid = auth_certificate.pid
            OR mom_id_entity.pid = auth_group.pid
            OR mom_id_entity.pid = auth_account_in_group.pid
            OR mom_id_entity.pid = auth_account_activation.pid
            OR mom_id_entity.pid = auth_account_password_change_required.pid
            OR mom_id_entity.pid = auth_account_email_verification.pid
            OR mom_id_entity.pid = auth_account_password_reset.pid
    Auth.Object
        SELECT auth__account_.enabled AS auth__account__enabled,
               auth__account_.name AS auth__account__name,
               auth__account_.pid AS auth__account__pid,
               auth__account_.superuser AS auth__account__superuser,
               auth__account_.suspended AS auth__account__suspended,
               auth_account.password AS auth_account_password,
               auth_account.ph_name AS auth_account_ph_name,
               auth_account.pid AS auth_account_pid,
               auth_certificate."desc" AS auth_certificate_desc,
               auth_certificate.cert_id AS auth_certificate_cert_id,
               auth_certificate.email AS auth_certificate_email,
               auth_certificate.pem AS auth_certificate_pem,
               auth_certificate.pid AS auth_certificate_pid,
               auth_certificate.revocation_date AS auth_certificate_revocation_date,
               auth_certificate.validity__finish AS auth_certificate_validity__finish,
               auth_certificate.validity__start AS auth_certificate_validity__start,
               auth_group."desc" AS auth_group_desc,
               auth_group.name AS auth_group_name,
               auth_group.pid AS auth_group_pid,
               mom_id_entity.electric AS mom_id_entity_electric,
               mom_id_entity.last_cid AS mom_id_entity_last_cid,
               mom_id_entity.pid AS mom_id_entity_pid,
               mom_id_entity.type_name AS mom_id_entity_type_name,
               mom_id_entity.x_locked AS mom_id_entity_x_locked
        FROM mom_id_entity
           LEFT OUTER JOIN auth__account_ ON mom_id_entity.pid = auth__account_.pid
           LEFT OUTER JOIN auth_account ON auth__account_.pid = auth_account.pid
           LEFT OUTER JOIN auth_certificate ON mom_id_entity.pid = auth_certificate.pid
           LEFT OUTER JOIN auth_group ON mom_id_entity.pid = auth_group.pid
        WHERE mom_id_entity.pid = auth__account_.pid
            OR mom_id_entity.pid = auth_account.pid
            OR mom_id_entity.pid = auth_certificate.pid
            OR mom_id_entity.pid = auth_group.pid
    Auth._Account_
        SELECT auth__account_.enabled AS auth__account__enabled,
               auth__account_.name AS auth__account__name,
               auth__account_.pid AS auth__account__pid,
               auth__account_.superuser AS auth__account__superuser,
               auth__account_.suspended AS auth__account__suspended,
               auth_account.password AS auth_account_password,
               auth_account.ph_name AS auth_account_ph_name,
               auth_account.pid AS auth_account_pid,
               mom_id_entity.electric AS mom_id_entity_electric,
               mom_id_entity.last_cid AS mom_id_entity_last_cid,
               mom_id_entity.pid AS mom_id_entity_pid,
               mom_id_entity.type_name AS mom_id_entity_type_name,
               mom_id_entity.x_locked AS mom_id_entity_x_locked
        FROM mom_id_entity
           JOIN auth__account_ ON mom_id_entity.pid = auth__account_.pid
           LEFT OUTER JOIN auth_account ON auth__account_.pid = auth_account.pid
    Auth.Account_Anonymous Auth._Account_
        SELECT auth__account_.enabled AS auth__account__enabled,
               auth__account_.name AS auth__account__name,
               auth__account_.pid AS auth__account__pid,
               auth__account_.superuser AS auth__account__superuser,
               auth__account_.suspended AS auth__account__suspended,
               auth_account_anonymous.pid AS auth_account_anonymous_pid,
               mom_id_entity.electric AS mom_id_entity_electric,
               mom_id_entity.last_cid AS mom_id_entity_last_cid,
               mom_id_entity.pid AS mom_id_entity_pid,
               mom_id_entity.type_name AS mom_id_entity_type_name,
               mom_id_entity.x_locked AS mom_id_entity_x_locked
        FROM mom_id_entity
           JOIN auth__account_ ON mom_id_entity.pid = auth__account_.pid
           JOIN auth_account_anonymous ON auth__account_.pid = auth_account_anonymous.pid
    Auth.Account Auth._Account_
        SELECT auth__account_.enabled AS auth__account__enabled,
               auth__account_.name AS auth__account__name,
               auth__account_.pid AS auth__account__pid,
               auth__account_.superuser AS auth__account__superuser,
               auth__account_.suspended AS auth__account__suspended,
               auth_account.password AS auth_account_password,
               auth_account.ph_name AS auth_account_ph_name,
               auth_account.pid AS auth_account_pid,
               mom_id_entity.electric AS mom_id_entity_electric,
               mom_id_entity.last_cid AS mom_id_entity_last_cid,
               mom_id_entity.pid AS mom_id_entity_pid,
               mom_id_entity.type_name AS mom_id_entity_type_name,
               mom_id_entity.x_locked AS mom_id_entity_x_locked
        FROM mom_id_entity
           JOIN auth__account_ ON mom_id_entity.pid = auth__account_.pid
           JOIN auth_account ON auth__account_.pid = auth_account.pid
    Auth.Certificate
        SELECT auth_certificate."desc" AS auth_certificate_desc,
               auth_certificate.cert_id AS auth_certificate_cert_id,
               auth_certificate.email AS auth_certificate_email,
               auth_certificate.pem AS auth_certificate_pem,
               auth_certificate.pid AS auth_certificate_pid,
               auth_certificate.revocation_date AS auth_certificate_revocation_date,
               auth_certificate.validity__finish AS auth_certificate_validity__finish,
               auth_certificate.validity__start AS auth_certificate_validity__start,
               mom_id_entity.electric AS mom_id_entity_electric,
               mom_id_entity.last_cid AS mom_id_entity_last_cid,
               mom_id_entity.pid AS mom_id_entity_pid,
               mom_id_entity.type_name AS mom_id_entity_type_name,
               mom_id_entity.x_locked AS mom_id_entity_x_locked
        FROM mom_id_entity
           JOIN auth_certificate ON mom_id_entity.pid = auth_certificate.pid
    Auth.Group
        SELECT auth_group."desc" AS auth_group_desc,
               auth_group.name AS auth_group_name,
               auth_group.pid AS auth_group_pid,
               mom_id_entity.electric AS mom_id_entity_electric,
               mom_id_entity.last_cid AS mom_id_entity_last_cid,
               mom_id_entity.pid AS mom_id_entity_pid,
               mom_id_entity.type_name AS mom_id_entity_type_name,
               mom_id_entity.x_locked AS mom_id_entity_x_locked
        FROM mom_id_entity
           JOIN auth_group ON mom_id_entity.pid = auth_group.pid
    Auth.Link
        SELECT auth_account_activation."left" AS auth_account_activation_left,
               auth_account_activation.pid AS auth_account_activation_pid,
               auth_account_email_verification."left" AS auth_account_email_verification_left,
               auth_account_email_verification.expires AS auth_account_email_verification_expires,
               auth_account_email_verification.new_email AS auth_account_email_verification_new_email,
               auth_account_email_verification.pid AS auth_account_email_verification_pid,
               auth_account_email_verification.token AS auth_account_email_verification_token,
               auth_account_in_group."left" AS auth_account_in_group_left,
               auth_account_in_group."right" AS auth_account_in_group_right,
               auth_account_in_group.pid AS auth_account_in_group_pid,
               auth_account_password_change_required."left" AS auth_account_password_change_required_left,
               auth_account_password_change_required.pid AS auth_account_password_change_required_pid,
               auth_account_password_reset."left" AS auth_account_password_reset_left,
               auth_account_password_reset.expires AS auth_account_password_reset_expires,
               auth_account_password_reset.password AS auth_account_password_reset_password,
               auth_account_password_reset.pid AS auth_account_password_reset_pid,
               auth_account_password_reset.token AS auth_account_password_reset_token,
               mom_id_entity.electric AS mom_id_entity_electric,
               mom_id_entity.last_cid AS mom_id_entity_last_cid,
               mom_id_entity.pid AS mom_id_entity_pid,
               mom_id_entity.type_name AS mom_id_entity_type_name,
               mom_id_entity.x_locked AS mom_id_entity_x_locked
        FROM mom_id_entity
           LEFT OUTER JOIN auth_account_in_group ON mom_id_entity.pid = auth_account_in_group.pid
           LEFT OUTER JOIN auth_account_activation ON mom_id_entity.pid = auth_account_activation.pid
           LEFT OUTER JOIN auth_account_password_change_required ON mom_id_entity.pid = auth_account_password_change_required.pid
           LEFT OUTER JOIN auth_account_email_verification ON mom_id_entity.pid = auth_account_email_verification.pid
           LEFT OUTER JOIN auth_account_password_reset ON mom_id_entity.pid = auth_account_password_reset.pid
        WHERE mom_id_entity.pid = auth_account_in_group.pid
            OR mom_id_entity.pid = auth_account_activation.pid
            OR mom_id_entity.pid = auth_account_password_change_required.pid
            OR mom_id_entity.pid = auth_account_email_verification.pid
            OR mom_id_entity.pid = auth_account_password_reset.pid
    Auth._MOM_Link_n_
        SELECT auth_account_in_group."left" AS auth_account_in_group_left,
               auth_account_in_group."right" AS auth_account_in_group_right,
               auth_account_in_group.pid AS auth_account_in_group_pid,
               mom_id_entity.electric AS mom_id_entity_electric,
               mom_id_entity.last_cid AS mom_id_entity_last_cid,
               mom_id_entity.pid AS mom_id_entity_pid,
               mom_id_entity.type_name AS mom_id_entity_type_name,
               mom_id_entity.x_locked AS mom_id_entity_x_locked
        FROM mom_id_entity
           LEFT OUTER JOIN auth_account_in_group ON mom_id_entity.pid = auth_account_in_group.pid
        WHERE mom_id_entity.pid = auth_account_in_group.pid
    Auth.Link2
        SELECT auth_account_in_group."left" AS auth_account_in_group_left,
               auth_account_in_group."right" AS auth_account_in_group_right,
               auth_account_in_group.pid AS auth_account_in_group_pid,
               mom_id_entity.electric AS mom_id_entity_electric,
               mom_id_entity.last_cid AS mom_id_entity_last_cid,
               mom_id_entity.pid AS mom_id_entity_pid,
               mom_id_entity.type_name AS mom_id_entity_type_name,
               mom_id_entity.x_locked AS mom_id_entity_x_locked
        FROM mom_id_entity
           LEFT OUTER JOIN auth_account_in_group ON mom_id_entity.pid = auth_account_in_group.pid
        WHERE mom_id_entity.pid = auth_account_in_group.pid
    Auth.Account_in_Group
        SELECT auth_account_in_group."left" AS auth_account_in_group_left,
               auth_account_in_group."right" AS auth_account_in_group_right,
               auth_account_in_group.pid AS auth_account_in_group_pid,
               mom_id_entity.electric AS mom_id_entity_electric,
               mom_id_entity.last_cid AS mom_id_entity_last_cid,
               mom_id_entity.pid AS mom_id_entity_pid,
               mom_id_entity.type_name AS mom_id_entity_type_name,
               mom_id_entity.x_locked AS mom_id_entity_x_locked
        FROM mom_id_entity
           JOIN auth_account_in_group ON mom_id_entity.pid = auth_account_in_group.pid
    Auth.Link1
        SELECT auth_account_activation."left" AS auth_account_activation_left,
               auth_account_activation.pid AS auth_account_activation_pid,
               auth_account_email_verification."left" AS auth_account_email_verification_left,
               auth_account_email_verification.expires AS auth_account_email_verification_expires,
               auth_account_email_verification.new_email AS auth_account_email_verification_new_email,
               auth_account_email_verification.pid AS auth_account_email_verification_pid,
               auth_account_email_verification.token AS auth_account_email_verification_token,
               auth_account_password_change_required."left" AS auth_account_password_change_required_left,
               auth_account_password_change_required.pid AS auth_account_password_change_required_pid,
               auth_account_password_reset."left" AS auth_account_password_reset_left,
               auth_account_password_reset.expires AS auth_account_password_reset_expires,
               auth_account_password_reset.password AS auth_account_password_reset_password,
               auth_account_password_reset.pid AS auth_account_password_reset_pid,
               auth_account_password_reset.token AS auth_account_password_reset_token,
               mom_id_entity.electric AS mom_id_entity_electric,
               mom_id_entity.last_cid AS mom_id_entity_last_cid,
               mom_id_entity.pid AS mom_id_entity_pid,
               mom_id_entity.type_name AS mom_id_entity_type_name,
               mom_id_entity.x_locked AS mom_id_entity_x_locked
        FROM mom_id_entity
           LEFT OUTER JOIN auth_account_activation ON mom_id_entity.pid = auth_account_activation.pid
           LEFT OUTER JOIN auth_account_password_change_required ON mom_id_entity.pid = auth_account_password_change_required.pid
           LEFT OUTER JOIN auth_account_email_verification ON mom_id_entity.pid = auth_account_email_verification.pid
           LEFT OUTER JOIN auth_account_password_reset ON mom_id_entity.pid = auth_account_password_reset.pid
        WHERE mom_id_entity.pid = auth_account_activation.pid
            OR mom_id_entity.pid = auth_account_password_change_required.pid
            OR mom_id_entity.pid = auth_account_email_verification.pid
            OR mom_id_entity.pid = auth_account_password_reset.pid
    Auth._Account_Action_
        SELECT auth_account_activation."left" AS auth_account_activation_left,
               auth_account_activation.pid AS auth_account_activation_pid,
               auth_account_email_verification."left" AS auth_account_email_verification_left,
               auth_account_email_verification.expires AS auth_account_email_verification_expires,
               auth_account_email_verification.new_email AS auth_account_email_verification_new_email,
               auth_account_email_verification.pid AS auth_account_email_verification_pid,
               auth_account_email_verification.token AS auth_account_email_verification_token,
               auth_account_password_change_required."left" AS auth_account_password_change_required_left,
               auth_account_password_change_required.pid AS auth_account_password_change_required_pid,
               auth_account_password_reset."left" AS auth_account_password_reset_left,
               auth_account_password_reset.expires AS auth_account_password_reset_expires,
               auth_account_password_reset.password AS auth_account_password_reset_password,
               auth_account_password_reset.pid AS auth_account_password_reset_pid,
               auth_account_password_reset.token AS auth_account_password_reset_token,
               mom_id_entity.electric AS mom_id_entity_electric,
               mom_id_entity.last_cid AS mom_id_entity_last_cid,
               mom_id_entity.pid AS mom_id_entity_pid,
               mom_id_entity.type_name AS mom_id_entity_type_name,
               mom_id_entity.x_locked AS mom_id_entity_x_locked
        FROM mom_id_entity
           LEFT OUTER JOIN auth_account_activation ON mom_id_entity.pid = auth_account_activation.pid
           LEFT OUTER JOIN auth_account_password_change_required ON mom_id_entity.pid = auth_account_password_change_required.pid
           LEFT OUTER JOIN auth_account_email_verification ON mom_id_entity.pid = auth_account_email_verification.pid
           LEFT OUTER JOIN auth_account_password_reset ON mom_id_entity.pid = auth_account_password_reset.pid
        WHERE mom_id_entity.pid = auth_account_activation.pid
            OR mom_id_entity.pid = auth_account_password_change_required.pid
            OR mom_id_entity.pid = auth_account_email_verification.pid
            OR mom_id_entity.pid = auth_account_password_reset.pid
    Auth.Account_Activation
        SELECT auth_account_activation."left" AS auth_account_activation_left,
               auth_account_activation.pid AS auth_account_activation_pid,
               mom_id_entity.electric AS mom_id_entity_electric,
               mom_id_entity.last_cid AS mom_id_entity_last_cid,
               mom_id_entity.pid AS mom_id_entity_pid,
               mom_id_entity.type_name AS mom_id_entity_type_name,
               mom_id_entity.x_locked AS mom_id_entity_x_locked
        FROM mom_id_entity
           JOIN auth_account_activation ON mom_id_entity.pid = auth_account_activation.pid
    Auth.Account_Password_Change_Required
        SELECT auth_account_password_change_required."left" AS auth_account_password_change_required_left,
               auth_account_password_change_required.pid AS auth_account_password_change_required_pid,
               mom_id_entity.electric AS mom_id_entity_electric,
               mom_id_entity.last_cid AS mom_id_entity_last_cid,
               mom_id_entity.pid AS mom_id_entity_pid,
               mom_id_entity.type_name AS mom_id_entity_type_name,
               mom_id_entity.x_locked AS mom_id_entity_x_locked
        FROM mom_id_entity
           JOIN auth_account_password_change_required ON mom_id_entity.pid = auth_account_password_change_required.pid
    Auth._Account_Token_Action_
        SELECT auth_account_email_verification."left" AS auth_account_email_verification_left,
               auth_account_email_verification.expires AS auth_account_email_verification_expires,
               auth_account_email_verification.new_email AS auth_account_email_verification_new_email,
               auth_account_email_verification.pid AS auth_account_email_verification_pid,
               auth_account_email_verification.token AS auth_account_email_verification_token,
               auth_account_password_reset."left" AS auth_account_password_reset_left,
               auth_account_password_reset.expires AS auth_account_password_reset_expires,
               auth_account_password_reset.password AS auth_account_password_reset_password,
               auth_account_password_reset.pid AS auth_account_password_reset_pid,
               auth_account_password_reset.token AS auth_account_password_reset_token,
               mom_id_entity.electric AS mom_id_entity_electric,
               mom_id_entity.last_cid AS mom_id_entity_last_cid,
               mom_id_entity.pid AS mom_id_entity_pid,
               mom_id_entity.type_name AS mom_id_entity_type_name,
               mom_id_entity.x_locked AS mom_id_entity_x_locked
        FROM mom_id_entity
           LEFT OUTER JOIN auth_account_email_verification ON mom_id_entity.pid = auth_account_email_verification.pid
           LEFT OUTER JOIN auth_account_password_reset ON mom_id_entity.pid = auth_account_password_reset.pid
        WHERE mom_id_entity.pid = auth_account_email_verification.pid
            OR mom_id_entity.pid = auth_account_password_reset.pid
    Auth.Account_EMail_Verification
        SELECT auth_account_email_verification."left" AS auth_account_email_verification_left,
               auth_account_email_verification.expires AS auth_account_email_verification_expires,
               auth_account_email_verification.new_email AS auth_account_email_verification_new_email,
               auth_account_email_verification.pid AS auth_account_email_verification_pid,
               auth_account_email_verification.token AS auth_account_email_verification_token,
               mom_id_entity.electric AS mom_id_entity_electric,
               mom_id_entity.last_cid AS mom_id_entity_last_cid,
               mom_id_entity.pid AS mom_id_entity_pid,
               mom_id_entity.type_name AS mom_id_entity_type_name,
               mom_id_entity.x_locked AS mom_id_entity_x_locked
        FROM mom_id_entity
           JOIN auth_account_email_verification ON mom_id_entity.pid = auth_account_email_verification.pid
    Auth.Account_Password_Reset
        SELECT auth_account_password_reset."left" AS auth_account_password_reset_left,
               auth_account_password_reset.expires AS auth_account_password_reset_expires,
               auth_account_password_reset.password AS auth_account_password_reset_password,
               auth_account_password_reset.pid AS auth_account_password_reset_pid,
               auth_account_password_reset.token AS auth_account_password_reset_token,
               mom_id_entity.electric AS mom_id_entity_electric,
               mom_id_entity.last_cid AS mom_id_entity_last_cid,
               mom_id_entity.pid AS mom_id_entity_pid,
               mom_id_entity.type_name AS mom_id_entity_type_name,
               mom_id_entity.x_locked AS mom_id_entity_x_locked
        FROM mom_id_entity
           JOIN auth_account_password_reset ON mom_id_entity.pid = auth_account_password_reset.pid
    EVT.Id_Entity
        SELECT evt_calendar."desc" AS evt_calendar_desc,
               evt_calendar.name AS evt_calendar_name,
               evt_calendar.pid AS evt_calendar_pid,
               evt_event."left" AS evt_event_left,
               evt_event.calendar AS evt_event_calendar,
               evt_event.date__finish AS evt_event_date__finish,
               evt_event.date__start AS evt_event_date__start,
               evt_event.detail AS evt_event_detail,
               evt_event.pid AS evt_event_pid,
               evt_event.short_title AS evt_event_short_title,
               evt_event.time__finish AS evt_event_time__finish,
               evt_event.time__start AS evt_event_time__start,
               evt_event_occurs."left" AS evt_event_occurs_left,
               evt_event_occurs.date AS evt_event_occurs_date,
               evt_event_occurs.pid AS evt_event_occurs_pid,
               evt_event_occurs.time__finish AS evt_event_occurs_time__finish,
               evt_event_occurs.time__start AS evt_event_occurs_time__start,
               evt_recurrence_rule."desc" AS evt_recurrence_rule_desc,
               evt_recurrence_rule."left" AS evt_recurrence_rule_left,
               evt_recurrence_rule.count AS evt_recurrence_rule_count,
               evt_recurrence_rule.easter_offset AS evt_recurrence_rule_easter_offset,
               evt_recurrence_rule.finish AS evt_recurrence_rule_finish,
               evt_recurrence_rule.is_exception AS evt_recurrence_rule_is_exception,
               evt_recurrence_rule.month AS evt_recurrence_rule_month,
               evt_recurrence_rule.month_day AS evt_recurrence_rule_month_day,
               evt_recurrence_rule.period AS evt_recurrence_rule_period,
               evt_recurrence_rule.pid AS evt_recurrence_rule_pid,
               evt_recurrence_rule.restrict_pos AS evt_recurrence_rule_restrict_pos,
               evt_recurrence_rule.start AS evt_recurrence_rule_start,
               evt_recurrence_rule.unit AS evt_recurrence_rule_unit,
               evt_recurrence_rule.week AS evt_recurrence_rule_week,
               evt_recurrence_rule.week_day AS evt_recurrence_rule_week_day,
               evt_recurrence_rule.year_day AS evt_recurrence_rule_year_day,
               evt_recurrence_spec."left" AS evt_recurrence_spec_left,
               evt_recurrence_spec.date_exceptions AS evt_recurrence_spec_date_exceptions,
               evt_recurrence_spec.dates AS evt_recurrence_spec_dates,
               evt_recurrence_spec.pid AS evt_recurrence_spec_pid,
               mom_id_entity.electric AS mom_id_entity_electric,
               mom_id_entity.last_cid AS mom_id_entity_last_cid,
               mom_id_entity.pid AS mom_id_entity_pid,
               mom_id_entity.type_name AS mom_id_entity_type_name,
               mom_id_entity.x_locked AS mom_id_entity_x_locked
        FROM mom_id_entity
           LEFT OUTER JOIN evt_calendar ON mom_id_entity.pid = evt_calendar.pid
           LEFT OUTER JOIN evt_event ON mom_id_entity.pid = evt_event.pid
           LEFT OUTER JOIN evt_event_occurs ON mom_id_entity.pid = evt_event_occurs.pid
           LEFT OUTER JOIN evt_recurrence_spec ON mom_id_entity.pid = evt_recurrence_spec.pid
           LEFT OUTER JOIN evt_recurrence_rule ON mom_id_entity.pid = evt_recurrence_rule.pid
        WHERE mom_id_entity.pid = evt_calendar.pid
            OR mom_id_entity.pid = evt_event.pid
            OR mom_id_entity.pid = evt_event_occurs.pid
            OR mom_id_entity.pid = evt_recurrence_spec.pid
            OR mom_id_entity.pid = evt_recurrence_rule.pid
    EVT.Object
        SELECT evt_calendar."desc" AS evt_calendar_desc,
               evt_calendar.name AS evt_calendar_name,
               evt_calendar.pid AS evt_calendar_pid,
               mom_id_entity.electric AS mom_id_entity_electric,
               mom_id_entity.last_cid AS mom_id_entity_last_cid,
               mom_id_entity.pid AS mom_id_entity_pid,
               mom_id_entity.type_name AS mom_id_entity_type_name,
               mom_id_entity.x_locked AS mom_id_entity_x_locked
        FROM mom_id_entity
           LEFT OUTER JOIN evt_calendar ON mom_id_entity.pid = evt_calendar.pid
        WHERE mom_id_entity.pid = evt_calendar.pid
    EVT.Calendar
        SELECT evt_calendar."desc" AS evt_calendar_desc,
               evt_calendar.name AS evt_calendar_name,
               evt_calendar.pid AS evt_calendar_pid,
               mom_id_entity.electric AS mom_id_entity_electric,
               mom_id_entity.last_cid AS mom_id_entity_last_cid,
               mom_id_entity.pid AS mom_id_entity_pid,
               mom_id_entity.type_name AS mom_id_entity_type_name,
               mom_id_entity.x_locked AS mom_id_entity_x_locked
        FROM mom_id_entity
           JOIN evt_calendar ON mom_id_entity.pid = evt_calendar.pid
    EVT.Link
        SELECT evt_event."left" AS evt_event_left,
               evt_event.calendar AS evt_event_calendar,
               evt_event.date__finish AS evt_event_date__finish,
               evt_event.date__start AS evt_event_date__start,
               evt_event.detail AS evt_event_detail,
               evt_event.pid AS evt_event_pid,
               evt_event.short_title AS evt_event_short_title,
               evt_event.time__finish AS evt_event_time__finish,
               evt_event.time__start AS evt_event_time__start,
               evt_event_occurs."left" AS evt_event_occurs_left,
               evt_event_occurs.date AS evt_event_occurs_date,
               evt_event_occurs.pid AS evt_event_occurs_pid,
               evt_event_occurs.time__finish AS evt_event_occurs_time__finish,
               evt_event_occurs.time__start AS evt_event_occurs_time__start,
               evt_recurrence_rule."desc" AS evt_recurrence_rule_desc,
               evt_recurrence_rule."left" AS evt_recurrence_rule_left,
               evt_recurrence_rule.count AS evt_recurrence_rule_count,
               evt_recurrence_rule.easter_offset AS evt_recurrence_rule_easter_offset,
               evt_recurrence_rule.finish AS evt_recurrence_rule_finish,
               evt_recurrence_rule.is_exception AS evt_recurrence_rule_is_exception,
               evt_recurrence_rule.month AS evt_recurrence_rule_month,
               evt_recurrence_rule.month_day AS evt_recurrence_rule_month_day,
               evt_recurrence_rule.period AS evt_recurrence_rule_period,
               evt_recurrence_rule.pid AS evt_recurrence_rule_pid,
               evt_recurrence_rule.restrict_pos AS evt_recurrence_rule_restrict_pos,
               evt_recurrence_rule.start AS evt_recurrence_rule_start,
               evt_recurrence_rule.unit AS evt_recurrence_rule_unit,
               evt_recurrence_rule.week AS evt_recurrence_rule_week,
               evt_recurrence_rule.week_day AS evt_recurrence_rule_week_day,
               evt_recurrence_rule.year_day AS evt_recurrence_rule_year_day,
               evt_recurrence_spec."left" AS evt_recurrence_spec_left,
               evt_recurrence_spec.date_exceptions AS evt_recurrence_spec_date_exceptions,
               evt_recurrence_spec.dates AS evt_recurrence_spec_dates,
               evt_recurrence_spec.pid AS evt_recurrence_spec_pid,
               mom_id_entity.electric AS mom_id_entity_electric,
               mom_id_entity.last_cid AS mom_id_entity_last_cid,
               mom_id_entity.pid AS mom_id_entity_pid,
               mom_id_entity.type_name AS mom_id_entity_type_name,
               mom_id_entity.x_locked AS mom_id_entity_x_locked
        FROM mom_id_entity
           LEFT OUTER JOIN evt_event ON mom_id_entity.pid = evt_event.pid
           LEFT OUTER JOIN evt_event_occurs ON mom_id_entity.pid = evt_event_occurs.pid
           LEFT OUTER JOIN evt_recurrence_spec ON mom_id_entity.pid = evt_recurrence_spec.pid
           LEFT OUTER JOIN evt_recurrence_rule ON mom_id_entity.pid = evt_recurrence_rule.pid
        WHERE mom_id_entity.pid = evt_event.pid
            OR mom_id_entity.pid = evt_event_occurs.pid
            OR mom_id_entity.pid = evt_recurrence_spec.pid
            OR mom_id_entity.pid = evt_recurrence_rule.pid
    EVT.Link1
        SELECT evt_event."left" AS evt_event_left,
               evt_event.calendar AS evt_event_calendar,
               evt_event.date__finish AS evt_event_date__finish,
               evt_event.date__start AS evt_event_date__start,
               evt_event.detail AS evt_event_detail,
               evt_event.pid AS evt_event_pid,
               evt_event.short_title AS evt_event_short_title,
               evt_event.time__finish AS evt_event_time__finish,
               evt_event.time__start AS evt_event_time__start,
               evt_event_occurs."left" AS evt_event_occurs_left,
               evt_event_occurs.date AS evt_event_occurs_date,
               evt_event_occurs.pid AS evt_event_occurs_pid,
               evt_event_occurs.time__finish AS evt_event_occurs_time__finish,
               evt_event_occurs.time__start AS evt_event_occurs_time__start,
               evt_recurrence_rule."desc" AS evt_recurrence_rule_desc,
               evt_recurrence_rule."left" AS evt_recurrence_rule_left,
               evt_recurrence_rule.count AS evt_recurrence_rule_count,
               evt_recurrence_rule.easter_offset AS evt_recurrence_rule_easter_offset,
               evt_recurrence_rule.finish AS evt_recurrence_rule_finish,
               evt_recurrence_rule.is_exception AS evt_recurrence_rule_is_exception,
               evt_recurrence_rule.month AS evt_recurrence_rule_month,
               evt_recurrence_rule.month_day AS evt_recurrence_rule_month_day,
               evt_recurrence_rule.period AS evt_recurrence_rule_period,
               evt_recurrence_rule.pid AS evt_recurrence_rule_pid,
               evt_recurrence_rule.restrict_pos AS evt_recurrence_rule_restrict_pos,
               evt_recurrence_rule.start AS evt_recurrence_rule_start,
               evt_recurrence_rule.unit AS evt_recurrence_rule_unit,
               evt_recurrence_rule.week AS evt_recurrence_rule_week,
               evt_recurrence_rule.week_day AS evt_recurrence_rule_week_day,
               evt_recurrence_rule.year_day AS evt_recurrence_rule_year_day,
               evt_recurrence_spec."left" AS evt_recurrence_spec_left,
               evt_recurrence_spec.date_exceptions AS evt_recurrence_spec_date_exceptions,
               evt_recurrence_spec.dates AS evt_recurrence_spec_dates,
               evt_recurrence_spec.pid AS evt_recurrence_spec_pid,
               mom_id_entity.electric AS mom_id_entity_electric,
               mom_id_entity.last_cid AS mom_id_entity_last_cid,
               mom_id_entity.pid AS mom_id_entity_pid,
               mom_id_entity.type_name AS mom_id_entity_type_name,
               mom_id_entity.x_locked AS mom_id_entity_x_locked
        FROM mom_id_entity
           LEFT OUTER JOIN evt_event ON mom_id_entity.pid = evt_event.pid
           LEFT OUTER JOIN evt_event_occurs ON mom_id_entity.pid = evt_event_occurs.pid
           LEFT OUTER JOIN evt_recurrence_spec ON mom_id_entity.pid = evt_recurrence_spec.pid
           LEFT OUTER JOIN evt_recurrence_rule ON mom_id_entity.pid = evt_recurrence_rule.pid
        WHERE mom_id_entity.pid = evt_event.pid
            OR mom_id_entity.pid = evt_event_occurs.pid
            OR mom_id_entity.pid = evt_recurrence_spec.pid
            OR mom_id_entity.pid = evt_recurrence_rule.pid
    SWP.Id_Entity
        SELECT mom_id_entity.electric AS mom_id_entity_electric,
               mom_id_entity.last_cid AS mom_id_entity_last_cid,
               mom_id_entity.pid AS mom_id_entity_pid,
               mom_id_entity.type_name AS mom_id_entity_type_name,
               mom_id_entity.x_locked AS mom_id_entity_x_locked,
               srm_page."desc" AS srm_page_desc,
               srm_page.event AS srm_page_event,
               srm_page.pid AS srm_page_pid,
               swp_clip_o."left" AS swp_clip_o_left,
               swp_clip_o.abstract AS swp_clip_o_abstract,
               swp_clip_o.contents AS swp_clip_o_contents,
               swp_clip_o.date__finish AS swp_clip_o_date__finish,
               swp_clip_o.date__start AS swp_clip_o_date__start,
               swp_clip_o.date_x__finish AS swp_clip_o_date_x__finish,
               swp_clip_o.date_x__start AS swp_clip_o_date_x__start,
               swp_clip_o.pid AS swp_clip_o_pid,
               swp_clip_o.prio AS swp_clip_o_prio,
               swp_clip_x.link_to AS swp_clip_x_link_to,
               swp_clip_x.pid AS swp_clip_x_pid,
               swp_gallery.date__finish AS swp_gallery_date__finish,
               swp_gallery.date__start AS swp_gallery_date__start,
               swp_gallery.directory AS swp_gallery_directory,
               swp_gallery.perma_name AS swp_gallery_perma_name,
               swp_gallery.pid AS swp_gallery_pid,
               swp_gallery.short_title AS swp_gallery_short_title,
               swp_gallery.title AS swp_gallery_title,
               swp_page.contents AS swp_page_contents,
               swp_page.date__finish AS swp_page_date__finish,
               swp_page.date__start AS swp_page_date__start,
               swp_page.format AS swp_page_format,
               swp_page.head_line AS swp_page_head_line,
               swp_page.hidden AS swp_page_hidden,
               swp_page.perma_name AS swp_page_perma_name,
               swp_page.pid AS swp_page_pid,
               swp_page.prio AS swp_page_prio,
               swp_page.short_title AS swp_page_short_title,
               swp_page.text AS swp_page_text,
               swp_page.title AS swp_page_title,
               swp_page_y.pid AS swp_page_y_pid,
               swp_page_y.year AS swp_page_y_year,
               swp_picture."left" AS swp_picture_left,
               swp_picture.name AS swp_picture_name,
               swp_picture.number AS swp_picture_number,
               swp_picture.photo__extension AS swp_picture_photo__extension,
               swp_picture.photo__height AS swp_picture_photo__height,
               swp_picture.photo__width AS swp_picture_photo__width,
               swp_picture.pid AS swp_picture_pid,
               swp_picture.thumb__extension AS swp_picture_thumb__extension,
               swp_picture.thumb__height AS swp_picture_thumb__height,
               swp_picture.thumb__width AS swp_picture_thumb__width
        FROM mom_id_entity
           LEFT OUTER JOIN swp_page ON mom_id_entity.pid = swp_page.pid
           LEFT OUTER JOIN swp_page_y ON swp_page.pid = swp_page_y.pid
           LEFT OUTER JOIN swp_clip_x ON swp_page.pid = swp_clip_x.pid
           LEFT OUTER JOIN srm_page ON swp_page.pid = srm_page.pid
           LEFT OUTER JOIN swp_clip_o ON mom_id_entity.pid = swp_clip_o.pid
           LEFT OUTER JOIN swp_gallery ON mom_id_entity.pid = swp_gallery.pid
           LEFT OUTER JOIN swp_picture ON mom_id_entity.pid = swp_picture.pid
        WHERE mom_id_entity.pid = swp_page.pid
            OR mom_id_entity.pid = swp_page_y.pid
            OR mom_id_entity.pid = swp_clip_x.pid
            OR mom_id_entity.pid = srm_page.pid
            OR mom_id_entity.pid = swp_clip_o.pid
            OR mom_id_entity.pid = swp_gallery.pid
            OR mom_id_entity.pid = swp_picture.pid
    SWP.Object
        SELECT mom_id_entity.electric AS mom_id_entity_electric,
               mom_id_entity.last_cid AS mom_id_entity_last_cid,
               mom_id_entity.pid AS mom_id_entity_pid,
               mom_id_entity.type_name AS mom_id_entity_type_name,
               mom_id_entity.x_locked AS mom_id_entity_x_locked,
               srm_page."desc" AS srm_page_desc,
               srm_page.event AS srm_page_event,
               srm_page.pid AS srm_page_pid,
               swp_clip_x.link_to AS swp_clip_x_link_to,
               swp_clip_x.pid AS swp_clip_x_pid,
               swp_gallery.date__finish AS swp_gallery_date__finish,
               swp_gallery.date__start AS swp_gallery_date__start,
               swp_gallery.directory AS swp_gallery_directory,
               swp_gallery.perma_name AS swp_gallery_perma_name,
               swp_gallery.pid AS swp_gallery_pid,
               swp_gallery.short_title AS swp_gallery_short_title,
               swp_gallery.title AS swp_gallery_title,
               swp_page.contents AS swp_page_contents,
               swp_page.date__finish AS swp_page_date__finish,
               swp_page.date__start AS swp_page_date__start,
               swp_page.format AS swp_page_format,
               swp_page.head_line AS swp_page_head_line,
               swp_page.hidden AS swp_page_hidden,
               swp_page.perma_name AS swp_page_perma_name,
               swp_page.pid AS swp_page_pid,
               swp_page.prio AS swp_page_prio,
               swp_page.short_title AS swp_page_short_title,
               swp_page.text AS swp_page_text,
               swp_page.title AS swp_page_title,
               swp_page_y.pid AS swp_page_y_pid,
               swp_page_y.year AS swp_page_y_year
        FROM mom_id_entity
           LEFT OUTER JOIN swp_page ON mom_id_entity.pid = swp_page.pid
           LEFT OUTER JOIN swp_page_y ON swp_page.pid = swp_page_y.pid
           LEFT OUTER JOIN swp_clip_x ON swp_page.pid = swp_clip_x.pid
           LEFT OUTER JOIN srm_page ON swp_page.pid = srm_page.pid
           LEFT OUTER JOIN swp_gallery ON mom_id_entity.pid = swp_gallery.pid
        WHERE mom_id_entity.pid = swp_page.pid
            OR mom_id_entity.pid = swp_page_y.pid
            OR mom_id_entity.pid = swp_clip_x.pid
            OR mom_id_entity.pid = srm_page.pid
            OR mom_id_entity.pid = swp_gallery.pid
    SWP.Object_PN
        SELECT mom_id_entity.electric AS mom_id_entity_electric,
               mom_id_entity.last_cid AS mom_id_entity_last_cid,
               mom_id_entity.pid AS mom_id_entity_pid,
               mom_id_entity.type_name AS mom_id_entity_type_name,
               mom_id_entity.x_locked AS mom_id_entity_x_locked,
               srm_page."desc" AS srm_page_desc,
               srm_page.event AS srm_page_event,
               srm_page.pid AS srm_page_pid,
               swp_clip_x.link_to AS swp_clip_x_link_to,
               swp_clip_x.pid AS swp_clip_x_pid,
               swp_gallery.date__finish AS swp_gallery_date__finish,
               swp_gallery.date__start AS swp_gallery_date__start,
               swp_gallery.directory AS swp_gallery_directory,
               swp_gallery.perma_name AS swp_gallery_perma_name,
               swp_gallery.pid AS swp_gallery_pid,
               swp_gallery.short_title AS swp_gallery_short_title,
               swp_gallery.title AS swp_gallery_title,
               swp_page.contents AS swp_page_contents,
               swp_page.date__finish AS swp_page_date__finish,
               swp_page.date__start AS swp_page_date__start,
               swp_page.format AS swp_page_format,
               swp_page.head_line AS swp_page_head_line,
               swp_page.hidden AS swp_page_hidden,
               swp_page.perma_name AS swp_page_perma_name,
               swp_page.pid AS swp_page_pid,
               swp_page.prio AS swp_page_prio,
               swp_page.short_title AS swp_page_short_title,
               swp_page.text AS swp_page_text,
               swp_page.title AS swp_page_title,
               swp_page_y.pid AS swp_page_y_pid,
               swp_page_y.year AS swp_page_y_year
        FROM mom_id_entity
           LEFT OUTER JOIN swp_page ON mom_id_entity.pid = swp_page.pid
           LEFT OUTER JOIN swp_page_y ON swp_page.pid = swp_page_y.pid
           LEFT OUTER JOIN swp_clip_x ON swp_page.pid = swp_clip_x.pid
           LEFT OUTER JOIN srm_page ON swp_page.pid = srm_page.pid
           LEFT OUTER JOIN swp_gallery ON mom_id_entity.pid = swp_gallery.pid
        WHERE mom_id_entity.pid = swp_page.pid
            OR mom_id_entity.pid = swp_page_y.pid
            OR mom_id_entity.pid = swp_clip_x.pid
            OR mom_id_entity.pid = srm_page.pid
            OR mom_id_entity.pid = swp_gallery.pid
    SWP.Page
        SELECT mom_id_entity.electric AS mom_id_entity_electric,
               mom_id_entity.last_cid AS mom_id_entity_last_cid,
               mom_id_entity.pid AS mom_id_entity_pid,
               mom_id_entity.type_name AS mom_id_entity_type_name,
               mom_id_entity.x_locked AS mom_id_entity_x_locked,
               srm_page."desc" AS srm_page_desc,
               srm_page.event AS srm_page_event,
               srm_page.pid AS srm_page_pid,
               swp_clip_x.link_to AS swp_clip_x_link_to,
               swp_clip_x.pid AS swp_clip_x_pid,
               swp_page.contents AS swp_page_contents,
               swp_page.date__finish AS swp_page_date__finish,
               swp_page.date__start AS swp_page_date__start,
               swp_page.format AS swp_page_format,
               swp_page.head_line AS swp_page_head_line,
               swp_page.hidden AS swp_page_hidden,
               swp_page.perma_name AS swp_page_perma_name,
               swp_page.pid AS swp_page_pid,
               swp_page.prio AS swp_page_prio,
               swp_page.short_title AS swp_page_short_title,
               swp_page.text AS swp_page_text,
               swp_page.title AS swp_page_title,
               swp_page_y.pid AS swp_page_y_pid,
               swp_page_y.year AS swp_page_y_year
        FROM mom_id_entity
           JOIN swp_page ON mom_id_entity.pid = swp_page.pid
           LEFT OUTER JOIN swp_page_y ON swp_page.pid = swp_page_y.pid
           LEFT OUTER JOIN swp_clip_x ON swp_page.pid = swp_clip_x.pid
           LEFT OUTER JOIN srm_page ON swp_page.pid = srm_page.pid
    SWP.Page_Y SWP.Page
        SELECT mom_id_entity.electric AS mom_id_entity_electric,
               mom_id_entity.last_cid AS mom_id_entity_last_cid,
               mom_id_entity.pid AS mom_id_entity_pid,
               mom_id_entity.type_name AS mom_id_entity_type_name,
               mom_id_entity.x_locked AS mom_id_entity_x_locked,
               swp_page.contents AS swp_page_contents,
               swp_page.date__finish AS swp_page_date__finish,
               swp_page.date__start AS swp_page_date__start,
               swp_page.format AS swp_page_format,
               swp_page.head_line AS swp_page_head_line,
               swp_page.hidden AS swp_page_hidden,
               swp_page.perma_name AS swp_page_perma_name,
               swp_page.pid AS swp_page_pid,
               swp_page.prio AS swp_page_prio,
               swp_page.short_title AS swp_page_short_title,
               swp_page.text AS swp_page_text,
               swp_page.title AS swp_page_title,
               swp_page_y.pid AS swp_page_y_pid,
               swp_page_y.year AS swp_page_y_year
        FROM mom_id_entity
           JOIN swp_page ON mom_id_entity.pid = swp_page.pid
           JOIN swp_page_y ON swp_page.pid = swp_page_y.pid
    EVT.Event
        SELECT evt_event."left" AS evt_event_left,
               evt_event.calendar AS evt_event_calendar,
               evt_event.date__finish AS evt_event_date__finish,
               evt_event.date__start AS evt_event_date__start,
               evt_event.detail AS evt_event_detail,
               evt_event.pid AS evt_event_pid,
               evt_event.short_title AS evt_event_short_title,
               evt_event.time__finish AS evt_event_time__finish,
               evt_event.time__start AS evt_event_time__start,
               mom_id_entity.electric AS mom_id_entity_electric,
               mom_id_entity.last_cid AS mom_id_entity_last_cid,
               mom_id_entity.pid AS mom_id_entity_pid,
               mom_id_entity.type_name AS mom_id_entity_type_name,
               mom_id_entity.x_locked AS mom_id_entity_x_locked
        FROM mom_id_entity
           JOIN evt_event ON mom_id_entity.pid = evt_event.pid
    EVT.Event_occurs
        SELECT evt_event_occurs."left" AS evt_event_occurs_left,
               evt_event_occurs.date AS evt_event_occurs_date,
               evt_event_occurs.pid AS evt_event_occurs_pid,
               evt_event_occurs.time__finish AS evt_event_occurs_time__finish,
               evt_event_occurs.time__start AS evt_event_occurs_time__start,
               mom_id_entity.electric AS mom_id_entity_electric,
               mom_id_entity.last_cid AS mom_id_entity_last_cid,
               mom_id_entity.pid AS mom_id_entity_pid,
               mom_id_entity.type_name AS mom_id_entity_type_name,
               mom_id_entity.x_locked AS mom_id_entity_x_locked
        FROM mom_id_entity
           JOIN evt_event_occurs ON mom_id_entity.pid = evt_event_occurs.pid
    EVT._Recurrence_Mixin_
        SELECT evt_recurrence_rule."desc" AS evt_recurrence_rule_desc,
               evt_recurrence_rule."left" AS evt_recurrence_rule_left,
               evt_recurrence_rule.count AS evt_recurrence_rule_count,
               evt_recurrence_rule.easter_offset AS evt_recurrence_rule_easter_offset,
               evt_recurrence_rule.finish AS evt_recurrence_rule_finish,
               evt_recurrence_rule.is_exception AS evt_recurrence_rule_is_exception,
               evt_recurrence_rule.month AS evt_recurrence_rule_month,
               evt_recurrence_rule.month_day AS evt_recurrence_rule_month_day,
               evt_recurrence_rule.period AS evt_recurrence_rule_period,
               evt_recurrence_rule.pid AS evt_recurrence_rule_pid,
               evt_recurrence_rule.restrict_pos AS evt_recurrence_rule_restrict_pos,
               evt_recurrence_rule.start AS evt_recurrence_rule_start,
               evt_recurrence_rule.unit AS evt_recurrence_rule_unit,
               evt_recurrence_rule.week AS evt_recurrence_rule_week,
               evt_recurrence_rule.week_day AS evt_recurrence_rule_week_day,
               evt_recurrence_rule.year_day AS evt_recurrence_rule_year_day,
               evt_recurrence_spec."left" AS evt_recurrence_spec_left,
               evt_recurrence_spec.date_exceptions AS evt_recurrence_spec_date_exceptions,
               evt_recurrence_spec.dates AS evt_recurrence_spec_dates,
               evt_recurrence_spec.pid AS evt_recurrence_spec_pid,
               mom_id_entity.electric AS mom_id_entity_electric,
               mom_id_entity.last_cid AS mom_id_entity_last_cid,
               mom_id_entity.pid AS mom_id_entity_pid,
               mom_id_entity.type_name AS mom_id_entity_type_name,
               mom_id_entity.x_locked AS mom_id_entity_x_locked
        FROM mom_id_entity
           LEFT OUTER JOIN evt_recurrence_spec ON mom_id_entity.pid = evt_recurrence_spec.pid
           LEFT OUTER JOIN evt_recurrence_rule ON mom_id_entity.pid = evt_recurrence_rule.pid
        WHERE mom_id_entity.pid = evt_recurrence_spec.pid
            OR mom_id_entity.pid = evt_recurrence_rule.pid
    EVT.Recurrence_Spec
        SELECT evt_recurrence_spec."left" AS evt_recurrence_spec_left,
               evt_recurrence_spec.date_exceptions AS evt_recurrence_spec_date_exceptions,
               evt_recurrence_spec.dates AS evt_recurrence_spec_dates,
               evt_recurrence_spec.pid AS evt_recurrence_spec_pid,
               mom_id_entity.electric AS mom_id_entity_electric,
               mom_id_entity.last_cid AS mom_id_entity_last_cid,
               mom_id_entity.pid AS mom_id_entity_pid,
               mom_id_entity.type_name AS mom_id_entity_type_name,
               mom_id_entity.x_locked AS mom_id_entity_x_locked
        FROM mom_id_entity
           JOIN evt_recurrence_spec ON mom_id_entity.pid = evt_recurrence_spec.pid
    EVT.Recurrence_Rule
        SELECT evt_recurrence_rule."desc" AS evt_recurrence_rule_desc,
               evt_recurrence_rule."left" AS evt_recurrence_rule_left,
               evt_recurrence_rule.count AS evt_recurrence_rule_count,
               evt_recurrence_rule.easter_offset AS evt_recurrence_rule_easter_offset,
               evt_recurrence_rule.finish AS evt_recurrence_rule_finish,
               evt_recurrence_rule.is_exception AS evt_recurrence_rule_is_exception,
               evt_recurrence_rule.month AS evt_recurrence_rule_month,
               evt_recurrence_rule.month_day AS evt_recurrence_rule_month_day,
               evt_recurrence_rule.period AS evt_recurrence_rule_period,
               evt_recurrence_rule.pid AS evt_recurrence_rule_pid,
               evt_recurrence_rule.restrict_pos AS evt_recurrence_rule_restrict_pos,
               evt_recurrence_rule.start AS evt_recurrence_rule_start,
               evt_recurrence_rule.unit AS evt_recurrence_rule_unit,
               evt_recurrence_rule.week AS evt_recurrence_rule_week,
               evt_recurrence_rule.week_day AS evt_recurrence_rule_week_day,
               evt_recurrence_rule.year_day AS evt_recurrence_rule_year_day,
               mom_id_entity.electric AS mom_id_entity_electric,
               mom_id_entity.last_cid AS mom_id_entity_last_cid,
               mom_id_entity.pid AS mom_id_entity_pid,
               mom_id_entity.type_name AS mom_id_entity_type_name,
               mom_id_entity.x_locked AS mom_id_entity_x_locked
        FROM mom_id_entity
           JOIN evt_recurrence_rule ON mom_id_entity.pid = evt_recurrence_rule.pid
    PAP.Id_Entity
        SELECT mom_id_entity.electric AS mom_id_entity_electric,
               mom_id_entity.last_cid AS mom_id_entity_last_cid,
               mom_id_entity.pid AS mom_id_entity_pid,
               mom_id_entity.type_name AS mom_id_entity_type_name,
               mom_id_entity.x_locked AS mom_id_entity_x_locked,
               pap_address."desc" AS pap_address_desc,
               pap_address.__raw_city AS pap_address___raw_city,
               pap_address.__raw_country AS pap_address___raw_country,
               pap_address.__raw_region AS pap_address___raw_region,
               pap_address.__raw_street AS pap_address___raw_street,
               pap_address.__raw_zip AS pap_address___raw_zip,
               pap_address.city AS pap_address_city,
               pap_address.country AS pap_address_country,
               pap_address.pid AS pap_address_pid,
               pap_address.region AS pap_address_region,
               pap_address.street AS pap_address_street,
               pap_address.zip AS pap_address_zip,
               pap_address_position."left" AS pap_address_position_left,
               pap_address_position.pid AS pap_address_position_pid,
               pap_address_position.position____raw_lat AS pap_address_position_position____raw_lat,
               pap_address_position.position____raw_lon AS pap_address_position_position____raw_lon,
               pap_address_position.position__height AS pap_address_position_position__height,
               pap_address_position.position__lat AS pap_address_position_position__lat,
               pap_address_position.position__lon AS pap_address_position_position__lon,
               pap_company.__raw_name AS pap_company___raw_name,
               pap_company.__raw_registered_in AS pap_company___raw_registered_in,
               pap_company.__raw_short_name AS pap_company___raw_short_name,
               pap_company.lifetime__finish AS pap_company_lifetime__finish,
               pap_company.lifetime__start AS pap_company_lifetime__start,
               pap_company.name AS pap_company_name,
               pap_company.pid AS pap_company_pid,
               pap_company.registered_in AS pap_company_registered_in,
               pap_company.short_name AS pap_company_short_name,
               pap_email."desc" AS pap_email_desc,
               pap_email.__raw_address AS pap_email___raw_address,
               pap_email.address AS pap_email_address,
               pap_email.pid AS pap_email_pid,
               pap_person.__raw_first_name AS pap_person___raw_first_name,
               pap_person.__raw_last_name AS pap_person___raw_last_name,
               pap_person.__raw_middle_name AS pap_person___raw_middle_name,
               pap_person.__raw_title AS pap_person___raw_title,
               pap_person.first_name AS pap_person_first_name,
               pap_person.last_name AS pap_person_last_name,
               pap_person.lifetime__finish AS pap_person_lifetime__finish,
               pap_person.lifetime__start AS pap_person_lifetime__start,
               pap_person.middle_name AS pap_person_middle_name,
               pap_person.pid AS pap_person_pid,
               pap_person.sex AS pap_person_sex,
               pap_person.title AS pap_person_title,
               pap_person_has_account."left" AS pap_person_has_account_left,
               pap_person_has_account."right" AS pap_person_has_account_right,
               pap_person_has_account.pid AS pap_person_has_account_pid,
               pap_phone."desc" AS pap_phone_desc,
               pap_phone.area_code AS pap_phone_area_code,
               pap_phone.country_code AS pap_phone_country_code,
               pap_phone.number AS pap_phone_number,
               pap_phone.pid AS pap_phone_pid,
               pap_subject_has_phone.extension AS pap_subject_has_phone_extension,
               pap_subject_has_phone.pid AS pap_subject_has_phone_pid,
               pap_subject_has_property."desc" AS pap_subject_has_property_desc,
               pap_subject_has_property."left" AS pap_subject_has_property_left,
               pap_subject_has_property."right" AS pap_subject_has_property_right,
               pap_subject_has_property.pid AS pap_subject_has_property_pid,
               pap_url."desc" AS pap_url_desc,
               pap_url.pid AS pap_url_pid,
               pap_url.value AS pap_url_value
        FROM mom_id_entity
           LEFT OUTER JOIN pap_address ON mom_id_entity.pid = pap_address.pid
           LEFT OUTER JOIN pap_company ON mom_id_entity.pid = pap_company.pid
           LEFT OUTER JOIN pap_email ON mom_id_entity.pid = pap_email.pid
           LEFT OUTER JOIN pap_phone ON mom_id_entity.pid = pap_phone.pid
           LEFT OUTER JOIN pap_person ON mom_id_entity.pid = pap_person.pid
           LEFT OUTER JOIN pap_url ON mom_id_entity.pid = pap_url.pid
           LEFT OUTER JOIN pap_address_position ON mom_id_entity.pid = pap_address_position.pid
           LEFT OUTER JOIN pap_subject_has_property ON mom_id_entity.pid = pap_subject_has_property.pid
           LEFT OUTER JOIN pap_subject_has_phone ON pap_subject_has_property.pid = pap_subject_has_phone.pid
           LEFT OUTER JOIN pap_person_has_account ON mom_id_entity.pid = pap_person_has_account.pid
        WHERE mom_id_entity.pid = pap_address.pid
            OR mom_id_entity.pid = pap_company.pid
            OR mom_id_entity.pid = pap_email.pid
            OR mom_id_entity.pid = pap_phone.pid
            OR mom_id_entity.pid = pap_person.pid
            OR mom_id_entity.pid = pap_url.pid
            OR mom_id_entity.pid = pap_address_position.pid
            OR mom_id_entity.pid = pap_subject_has_property.pid
            OR mom_id_entity.pid = pap_subject_has_phone.pid
            OR mom_id_entity.pid = pap_person_has_account.pid
    PAP.Object
        SELECT mom_id_entity.electric AS mom_id_entity_electric,
               mom_id_entity.last_cid AS mom_id_entity_last_cid,
               mom_id_entity.pid AS mom_id_entity_pid,
               mom_id_entity.type_name AS mom_id_entity_type_name,
               mom_id_entity.x_locked AS mom_id_entity_x_locked,
               pap_address."desc" AS pap_address_desc,
               pap_address.__raw_city AS pap_address___raw_city,
               pap_address.__raw_country AS pap_address___raw_country,
               pap_address.__raw_region AS pap_address___raw_region,
               pap_address.__raw_street AS pap_address___raw_street,
               pap_address.__raw_zip AS pap_address___raw_zip,
               pap_address.city AS pap_address_city,
               pap_address.country AS pap_address_country,
               pap_address.pid AS pap_address_pid,
               pap_address.region AS pap_address_region,
               pap_address.street AS pap_address_street,
               pap_address.zip AS pap_address_zip,
               pap_company.__raw_name AS pap_company___raw_name,
               pap_company.__raw_registered_in AS pap_company___raw_registered_in,
               pap_company.__raw_short_name AS pap_company___raw_short_name,
               pap_company.lifetime__finish AS pap_company_lifetime__finish,
               pap_company.lifetime__start AS pap_company_lifetime__start,
               pap_company.name AS pap_company_name,
               pap_company.pid AS pap_company_pid,
               pap_company.registered_in AS pap_company_registered_in,
               pap_company.short_name AS pap_company_short_name,
               pap_email."desc" AS pap_email_desc,
               pap_email.__raw_address AS pap_email___raw_address,
               pap_email.address AS pap_email_address,
               pap_email.pid AS pap_email_pid,
               pap_person.__raw_first_name AS pap_person___raw_first_name,
               pap_person.__raw_last_name AS pap_person___raw_last_name,
               pap_person.__raw_middle_name AS pap_person___raw_middle_name,
               pap_person.__raw_title AS pap_person___raw_title,
               pap_person.first_name AS pap_person_first_name,
               pap_person.last_name AS pap_person_last_name,
               pap_person.lifetime__finish AS pap_person_lifetime__finish,
               pap_person.lifetime__start AS pap_person_lifetime__start,
               pap_person.middle_name AS pap_person_middle_name,
               pap_person.pid AS pap_person_pid,
               pap_person.sex AS pap_person_sex,
               pap_person.title AS pap_person_title,
               pap_phone."desc" AS pap_phone_desc,
               pap_phone.area_code AS pap_phone_area_code,
               pap_phone.country_code AS pap_phone_country_code,
               pap_phone.number AS pap_phone_number,
               pap_phone.pid AS pap_phone_pid,
               pap_url."desc" AS pap_url_desc,
               pap_url.pid AS pap_url_pid,
               pap_url.value AS pap_url_value
        FROM mom_id_entity
           LEFT OUTER JOIN pap_address ON mom_id_entity.pid = pap_address.pid
           LEFT OUTER JOIN pap_company ON mom_id_entity.pid = pap_company.pid
           LEFT OUTER JOIN pap_email ON mom_id_entity.pid = pap_email.pid
           LEFT OUTER JOIN pap_phone ON mom_id_entity.pid = pap_phone.pid
           LEFT OUTER JOIN pap_person ON mom_id_entity.pid = pap_person.pid
           LEFT OUTER JOIN pap_url ON mom_id_entity.pid = pap_url.pid
        WHERE mom_id_entity.pid = pap_address.pid
            OR mom_id_entity.pid = pap_company.pid
            OR mom_id_entity.pid = pap_email.pid
            OR mom_id_entity.pid = pap_phone.pid
            OR mom_id_entity.pid = pap_person.pid
            OR mom_id_entity.pid = pap_url.pid
    PAP.Property
        SELECT mom_id_entity.electric AS mom_id_entity_electric,
               mom_id_entity.last_cid AS mom_id_entity_last_cid,
               mom_id_entity.pid AS mom_id_entity_pid,
               mom_id_entity.type_name AS mom_id_entity_type_name,
               mom_id_entity.x_locked AS mom_id_entity_x_locked,
               pap_address."desc" AS pap_address_desc,
               pap_address.__raw_city AS pap_address___raw_city,
               pap_address.__raw_country AS pap_address___raw_country,
               pap_address.__raw_region AS pap_address___raw_region,
               pap_address.__raw_street AS pap_address___raw_street,
               pap_address.__raw_zip AS pap_address___raw_zip,
               pap_address.city AS pap_address_city,
               pap_address.country AS pap_address_country,
               pap_address.pid AS pap_address_pid,
               pap_address.region AS pap_address_region,
               pap_address.street AS pap_address_street,
               pap_address.zip AS pap_address_zip,
               pap_email."desc" AS pap_email_desc,
               pap_email.__raw_address AS pap_email___raw_address,
               pap_email.address AS pap_email_address,
               pap_email.pid AS pap_email_pid,
               pap_phone."desc" AS pap_phone_desc,
               pap_phone.area_code AS pap_phone_area_code,
               pap_phone.country_code AS pap_phone_country_code,
               pap_phone.number AS pap_phone_number,
               pap_phone.pid AS pap_phone_pid,
               pap_url."desc" AS pap_url_desc,
               pap_url.pid AS pap_url_pid,
               pap_url.value AS pap_url_value
        FROM mom_id_entity
           LEFT OUTER JOIN pap_address ON mom_id_entity.pid = pap_address.pid
           LEFT OUTER JOIN pap_email ON mom_id_entity.pid = pap_email.pid
           LEFT OUTER JOIN pap_phone ON mom_id_entity.pid = pap_phone.pid
           LEFT OUTER JOIN pap_url ON mom_id_entity.pid = pap_url.pid
        WHERE mom_id_entity.pid = pap_address.pid
            OR mom_id_entity.pid = pap_email.pid
            OR mom_id_entity.pid = pap_phone.pid
            OR mom_id_entity.pid = pap_url.pid
    PAP.Address
        SELECT mom_id_entity.electric AS mom_id_entity_electric,
               mom_id_entity.last_cid AS mom_id_entity_last_cid,
               mom_id_entity.pid AS mom_id_entity_pid,
               mom_id_entity.type_name AS mom_id_entity_type_name,
               mom_id_entity.x_locked AS mom_id_entity_x_locked,
               pap_address."desc" AS pap_address_desc,
               pap_address.__raw_city AS pap_address___raw_city,
               pap_address.__raw_country AS pap_address___raw_country,
               pap_address.__raw_region AS pap_address___raw_region,
               pap_address.__raw_street AS pap_address___raw_street,
               pap_address.__raw_zip AS pap_address___raw_zip,
               pap_address.city AS pap_address_city,
               pap_address.country AS pap_address_country,
               pap_address.pid AS pap_address_pid,
               pap_address.region AS pap_address_region,
               pap_address.street AS pap_address_street,
               pap_address.zip AS pap_address_zip
        FROM mom_id_entity
           JOIN pap_address ON mom_id_entity.pid = pap_address.pid
    PAP.Subject
        SELECT mom_id_entity.electric AS mom_id_entity_electric,
               mom_id_entity.last_cid AS mom_id_entity_last_cid,
               mom_id_entity.pid AS mom_id_entity_pid,
               mom_id_entity.type_name AS mom_id_entity_type_name,
               mom_id_entity.x_locked AS mom_id_entity_x_locked,
               pap_company.__raw_name AS pap_company___raw_name,
               pap_company.__raw_registered_in AS pap_company___raw_registered_in,
               pap_company.__raw_short_name AS pap_company___raw_short_name,
               pap_company.lifetime__finish AS pap_company_lifetime__finish,
               pap_company.lifetime__start AS pap_company_lifetime__start,
               pap_company.name AS pap_company_name,
               pap_company.pid AS pap_company_pid,
               pap_company.registered_in AS pap_company_registered_in,
               pap_company.short_name AS pap_company_short_name,
               pap_person.__raw_first_name AS pap_person___raw_first_name,
               pap_person.__raw_last_name AS pap_person___raw_last_name,
               pap_person.__raw_middle_name AS pap_person___raw_middle_name,
               pap_person.__raw_title AS pap_person___raw_title,
               pap_person.first_name AS pap_person_first_name,
               pap_person.last_name AS pap_person_last_name,
               pap_person.lifetime__finish AS pap_person_lifetime__finish,
               pap_person.lifetime__start AS pap_person_lifetime__start,
               pap_person.middle_name AS pap_person_middle_name,
               pap_person.pid AS pap_person_pid,
               pap_person.sex AS pap_person_sex,
               pap_person.title AS pap_person_title
        FROM mom_id_entity
           LEFT OUTER JOIN pap_company ON mom_id_entity.pid = pap_company.pid
           LEFT OUTER JOIN pap_person ON mom_id_entity.pid = pap_person.pid
        WHERE mom_id_entity.pid = pap_company.pid
            OR mom_id_entity.pid = pap_person.pid
    PAP.Legal_Entity
        SELECT mom_id_entity.electric AS mom_id_entity_electric,
               mom_id_entity.last_cid AS mom_id_entity_last_cid,
               mom_id_entity.pid AS mom_id_entity_pid,
               mom_id_entity.type_name AS mom_id_entity_type_name,
               mom_id_entity.x_locked AS mom_id_entity_x_locked,
               pap_company.__raw_name AS pap_company___raw_name,
               pap_company.__raw_registered_in AS pap_company___raw_registered_in,
               pap_company.__raw_short_name AS pap_company___raw_short_name,
               pap_company.lifetime__finish AS pap_company_lifetime__finish,
               pap_company.lifetime__start AS pap_company_lifetime__start,
               pap_company.name AS pap_company_name,
               pap_company.pid AS pap_company_pid,
               pap_company.registered_in AS pap_company_registered_in,
               pap_company.short_name AS pap_company_short_name
        FROM mom_id_entity
           LEFT OUTER JOIN pap_company ON mom_id_entity.pid = pap_company.pid
        WHERE mom_id_entity.pid = pap_company.pid
    PAP.Company
        SELECT mom_id_entity.electric AS mom_id_entity_electric,
               mom_id_entity.last_cid AS mom_id_entity_last_cid,
               mom_id_entity.pid AS mom_id_entity_pid,
               mom_id_entity.type_name AS mom_id_entity_type_name,
               mom_id_entity.x_locked AS mom_id_entity_x_locked,
               pap_company.__raw_name AS pap_company___raw_name,
               pap_company.__raw_registered_in AS pap_company___raw_registered_in,
               pap_company.__raw_short_name AS pap_company___raw_short_name,
               pap_company.lifetime__finish AS pap_company_lifetime__finish,
               pap_company.lifetime__start AS pap_company_lifetime__start,
               pap_company.name AS pap_company_name,
               pap_company.pid AS pap_company_pid,
               pap_company.registered_in AS pap_company_registered_in,
               pap_company.short_name AS pap_company_short_name
        FROM mom_id_entity
           JOIN pap_company ON mom_id_entity.pid = pap_company.pid
    PAP.Email
        SELECT mom_id_entity.electric AS mom_id_entity_electric,
               mom_id_entity.last_cid AS mom_id_entity_last_cid,
               mom_id_entity.pid AS mom_id_entity_pid,
               mom_id_entity.type_name AS mom_id_entity_type_name,
               mom_id_entity.x_locked AS mom_id_entity_x_locked,
               pap_email."desc" AS pap_email_desc,
               pap_email.__raw_address AS pap_email___raw_address,
               pap_email.address AS pap_email_address,
               pap_email.pid AS pap_email_pid
        FROM mom_id_entity
           JOIN pap_email ON mom_id_entity.pid = pap_email.pid
    PAP.Phone
        SELECT mom_id_entity.electric AS mom_id_entity_electric,
               mom_id_entity.last_cid AS mom_id_entity_last_cid,
               mom_id_entity.pid AS mom_id_entity_pid,
               mom_id_entity.type_name AS mom_id_entity_type_name,
               mom_id_entity.x_locked AS mom_id_entity_x_locked,
               pap_phone."desc" AS pap_phone_desc,
               pap_phone.area_code AS pap_phone_area_code,
               pap_phone.country_code AS pap_phone_country_code,
               pap_phone.number AS pap_phone_number,
               pap_phone.pid AS pap_phone_pid
        FROM mom_id_entity
           JOIN pap_phone ON mom_id_entity.pid = pap_phone.pid
    PAP.Person
        SELECT mom_id_entity.electric AS mom_id_entity_electric,
               mom_id_entity.last_cid AS mom_id_entity_last_cid,
               mom_id_entity.pid AS mom_id_entity_pid,
               mom_id_entity.type_name AS mom_id_entity_type_name,
               mom_id_entity.x_locked AS mom_id_entity_x_locked,
               pap_person.__raw_first_name AS pap_person___raw_first_name,
               pap_person.__raw_last_name AS pap_person___raw_last_name,
               pap_person.__raw_middle_name AS pap_person___raw_middle_name,
               pap_person.__raw_title AS pap_person___raw_title,
               pap_person.first_name AS pap_person_first_name,
               pap_person.last_name AS pap_person_last_name,
               pap_person.lifetime__finish AS pap_person_lifetime__finish,
               pap_person.lifetime__start AS pap_person_lifetime__start,
               pap_person.middle_name AS pap_person_middle_name,
               pap_person.pid AS pap_person_pid,
               pap_person.sex AS pap_person_sex,
               pap_person.title AS pap_person_title
        FROM mom_id_entity
           JOIN pap_person ON mom_id_entity.pid = pap_person.pid
    PAP.Url
        SELECT mom_id_entity.electric AS mom_id_entity_electric,
               mom_id_entity.last_cid AS mom_id_entity_last_cid,
               mom_id_entity.pid AS mom_id_entity_pid,
               mom_id_entity.type_name AS mom_id_entity_type_name,
               mom_id_entity.x_locked AS mom_id_entity_x_locked,
               pap_url."desc" AS pap_url_desc,
               pap_url.pid AS pap_url_pid,
               pap_url.value AS pap_url_value
        FROM mom_id_entity
           JOIN pap_url ON mom_id_entity.pid = pap_url.pid
    PAP.Link
        SELECT mom_id_entity.electric AS mom_id_entity_electric,
               mom_id_entity.last_cid AS mom_id_entity_last_cid,
               mom_id_entity.pid AS mom_id_entity_pid,
               mom_id_entity.type_name AS mom_id_entity_type_name,
               mom_id_entity.x_locked AS mom_id_entity_x_locked,
               pap_address_position."left" AS pap_address_position_left,
               pap_address_position.pid AS pap_address_position_pid,
               pap_address_position.position____raw_lat AS pap_address_position_position____raw_lat,
               pap_address_position.position____raw_lon AS pap_address_position_position____raw_lon,
               pap_address_position.position__height AS pap_address_position_position__height,
               pap_address_position.position__lat AS pap_address_position_position__lat,
               pap_address_position.position__lon AS pap_address_position_position__lon,
               pap_person_has_account."left" AS pap_person_has_account_left,
               pap_person_has_account."right" AS pap_person_has_account_right,
               pap_person_has_account.pid AS pap_person_has_account_pid,
               pap_subject_has_phone.extension AS pap_subject_has_phone_extension,
               pap_subject_has_phone.pid AS pap_subject_has_phone_pid,
               pap_subject_has_property."desc" AS pap_subject_has_property_desc,
               pap_subject_has_property."left" AS pap_subject_has_property_left,
               pap_subject_has_property."right" AS pap_subject_has_property_right,
               pap_subject_has_property.pid AS pap_subject_has_property_pid
        FROM mom_id_entity
           LEFT OUTER JOIN pap_address_position ON mom_id_entity.pid = pap_address_position.pid
           LEFT OUTER JOIN pap_subject_has_property ON mom_id_entity.pid = pap_subject_has_property.pid
           LEFT OUTER JOIN pap_subject_has_phone ON pap_subject_has_property.pid = pap_subject_has_phone.pid
           LEFT OUTER JOIN pap_person_has_account ON mom_id_entity.pid = pap_person_has_account.pid
        WHERE mom_id_entity.pid = pap_address_position.pid
            OR mom_id_entity.pid = pap_subject_has_property.pid
            OR mom_id_entity.pid = pap_subject_has_phone.pid
            OR mom_id_entity.pid = pap_person_has_account.pid
    PAP.Link1
        SELECT mom_id_entity.electric AS mom_id_entity_electric,
               mom_id_entity.last_cid AS mom_id_entity_last_cid,
               mom_id_entity.pid AS mom_id_entity_pid,
               mom_id_entity.type_name AS mom_id_entity_type_name,
               mom_id_entity.x_locked AS mom_id_entity_x_locked,
               pap_address_position."left" AS pap_address_position_left,
               pap_address_position.pid AS pap_address_position_pid,
               pap_address_position.position____raw_lat AS pap_address_position_position____raw_lat,
               pap_address_position.position____raw_lon AS pap_address_position_position____raw_lon,
               pap_address_position.position__height AS pap_address_position_position__height,
               pap_address_position.position__lat AS pap_address_position_position__lat,
               pap_address_position.position__lon AS pap_address_position_position__lon
        FROM mom_id_entity
           LEFT OUTER JOIN pap_address_position ON mom_id_entity.pid = pap_address_position.pid
        WHERE mom_id_entity.pid = pap_address_position.pid
    PAP.Address_Position
        SELECT mom_id_entity.electric AS mom_id_entity_electric,
               mom_id_entity.last_cid AS mom_id_entity_last_cid,
               mom_id_entity.pid AS mom_id_entity_pid,
               mom_id_entity.type_name AS mom_id_entity_type_name,
               mom_id_entity.x_locked AS mom_id_entity_x_locked,
               pap_address_position."left" AS pap_address_position_left,
               pap_address_position.pid AS pap_address_position_pid,
               pap_address_position.position____raw_lat AS pap_address_position_position____raw_lat,
               pap_address_position.position____raw_lon AS pap_address_position_position____raw_lon,
               pap_address_position.position__height AS pap_address_position_position__height,
               pap_address_position.position__lat AS pap_address_position_position__lat,
               pap_address_position.position__lon AS pap_address_position_position__lon
        FROM mom_id_entity
           JOIN pap_address_position ON mom_id_entity.pid = pap_address_position.pid
    PAP._MOM_Link_n_
        SELECT mom_id_entity.electric AS mom_id_entity_electric,
               mom_id_entity.last_cid AS mom_id_entity_last_cid,
               mom_id_entity.pid AS mom_id_entity_pid,
               mom_id_entity.type_name AS mom_id_entity_type_name,
               mom_id_entity.x_locked AS mom_id_entity_x_locked,
               pap_person_has_account."left" AS pap_person_has_account_left,
               pap_person_has_account."right" AS pap_person_has_account_right,
               pap_person_has_account.pid AS pap_person_has_account_pid,
               pap_subject_has_phone.extension AS pap_subject_has_phone_extension,
               pap_subject_has_phone.pid AS pap_subject_has_phone_pid,
               pap_subject_has_property."desc" AS pap_subject_has_property_desc,
               pap_subject_has_property."left" AS pap_subject_has_property_left,
               pap_subject_has_property."right" AS pap_subject_has_property_right,
               pap_subject_has_property.pid AS pap_subject_has_property_pid
        FROM mom_id_entity
           LEFT OUTER JOIN pap_subject_has_property ON mom_id_entity.pid = pap_subject_has_property.pid
           LEFT OUTER JOIN pap_subject_has_phone ON pap_subject_has_property.pid = pap_subject_has_phone.pid
           LEFT OUTER JOIN pap_person_has_account ON mom_id_entity.pid = pap_person_has_account.pid
        WHERE mom_id_entity.pid = pap_subject_has_property.pid
            OR mom_id_entity.pid = pap_subject_has_phone.pid
            OR mom_id_entity.pid = pap_person_has_account.pid
    PAP.Link2
        SELECT mom_id_entity.electric AS mom_id_entity_electric,
               mom_id_entity.last_cid AS mom_id_entity_last_cid,
               mom_id_entity.pid AS mom_id_entity_pid,
               mom_id_entity.type_name AS mom_id_entity_type_name,
               mom_id_entity.x_locked AS mom_id_entity_x_locked,
               pap_person_has_account."left" AS pap_person_has_account_left,
               pap_person_has_account."right" AS pap_person_has_account_right,
               pap_person_has_account.pid AS pap_person_has_account_pid,
               pap_subject_has_phone.extension AS pap_subject_has_phone_extension,
               pap_subject_has_phone.pid AS pap_subject_has_phone_pid,
               pap_subject_has_property."desc" AS pap_subject_has_property_desc,
               pap_subject_has_property."left" AS pap_subject_has_property_left,
               pap_subject_has_property."right" AS pap_subject_has_property_right,
               pap_subject_has_property.pid AS pap_subject_has_property_pid
        FROM mom_id_entity
           LEFT OUTER JOIN pap_subject_has_property ON mom_id_entity.pid = pap_subject_has_property.pid
           LEFT OUTER JOIN pap_subject_has_phone ON pap_subject_has_property.pid = pap_subject_has_phone.pid
           LEFT OUTER JOIN pap_person_has_account ON mom_id_entity.pid = pap_person_has_account.pid
        WHERE mom_id_entity.pid = pap_subject_has_property.pid
            OR mom_id_entity.pid = pap_subject_has_phone.pid
            OR mom_id_entity.pid = pap_person_has_account.pid
    PAP.Subject_has_Property
        SELECT mom_id_entity.electric AS mom_id_entity_electric,
               mom_id_entity.last_cid AS mom_id_entity_last_cid,
               mom_id_entity.pid AS mom_id_entity_pid,
               mom_id_entity.type_name AS mom_id_entity_type_name,
               mom_id_entity.x_locked AS mom_id_entity_x_locked,
               pap_subject_has_phone.extension AS pap_subject_has_phone_extension,
               pap_subject_has_phone.pid AS pap_subject_has_phone_pid,
               pap_subject_has_property."desc" AS pap_subject_has_property_desc,
               pap_subject_has_property."left" AS pap_subject_has_property_left,
               pap_subject_has_property."right" AS pap_subject_has_property_right,
               pap_subject_has_property.pid AS pap_subject_has_property_pid
        FROM mom_id_entity
           JOIN pap_subject_has_property ON mom_id_entity.pid = pap_subject_has_property.pid
           LEFT OUTER JOIN pap_subject_has_phone ON pap_subject_has_property.pid = pap_subject_has_phone.pid
    PAP.Person_has_Account
        SELECT mom_id_entity.electric AS mom_id_entity_electric,
               mom_id_entity.last_cid AS mom_id_entity_last_cid,
               mom_id_entity.pid AS mom_id_entity_pid,
               mom_id_entity.type_name AS mom_id_entity_type_name,
               mom_id_entity.x_locked AS mom_id_entity_x_locked,
               pap_person_has_account."left" AS pap_person_has_account_left,
               pap_person_has_account."right" AS pap_person_has_account_right,
               pap_person_has_account.pid AS pap_person_has_account_pid
        FROM mom_id_entity
           JOIN pap_person_has_account ON mom_id_entity.pid = pap_person_has_account.pid
    SRM.Id_Entity
        SELECT mom_id_entity.electric AS mom_id_entity_electric,
               mom_id_entity.last_cid AS mom_id_entity_last_cid,
               mom_id_entity.pid AS mom_id_entity_pid,
               mom_id_entity.type_name AS mom_id_entity_type_name,
               mom_id_entity.x_locked AS mom_id_entity_x_locked,
               srm__boat_class_.__raw_name AS srm__boat_class____raw_name,
               srm__boat_class_.name AS srm__boat_class__name,
               srm__boat_class_.pid AS srm__boat_class__pid,
               srm_boat."left" AS srm_boat_left,
               srm_boat.__raw_sail_number AS srm_boat___raw_sail_number,
               srm_boat.__raw_sail_number_x AS srm_boat___raw_sail_number_x,
               srm_boat.name AS srm_boat_name,
               srm_boat.nation AS srm_boat_nation,
               srm_boat.pid AS srm_boat_pid,
               srm_boat.sail_number AS srm_boat_sail_number,
               srm_boat.sail_number_x AS srm_boat_sail_number_x,
               srm_boat_class.beam AS srm_boat_class_beam,
               srm_boat_class.loa AS srm_boat_class_loa,
               srm_boat_class.max_crew AS srm_boat_class_max_crew,
               srm_boat_class.pid AS srm_boat_class_pid,
               srm_boat_class.sail_area AS srm_boat_class_sail_area,
               srm_boat_in_regatta."left" AS srm_boat_in_regatta_left,
               srm_boat_in_regatta."right" AS srm_boat_in_regatta_right,
               srm_boat_in_regatta.pid AS srm_boat_in_regatta_pid,
               srm_boat_in_regatta.place AS srm_boat_in_regatta_place,
               srm_boat_in_regatta.points AS srm_boat_in_regatta_points,
               srm_boat_in_regatta.rank AS srm_boat_in_regatta_rank,
               srm_boat_in_regatta.registration_date AS srm_boat_in_regatta_registration_date,
               srm_boat_in_regatta.skipper AS srm_boat_in_regatta_skipper,
               srm_club.__raw_name AS srm_club___raw_name,
               srm_club.long_name AS srm_club_long_name,
               srm_club.name AS srm_club_name,
               srm_club.pid AS srm_club_pid,
               srm_crew_member."left" AS srm_crew_member_left,
               srm_crew_member."right" AS srm_crew_member_right,
               srm_crew_member.key AS srm_crew_member_key,
               srm_crew_member.pid AS srm_crew_member_pid,
               srm_crew_member.role AS srm_crew_member_role,
               srm_race_result."left" AS srm_race_result_left,
               srm_race_result.discarded AS srm_race_result_discarded,
               srm_race_result.pid AS srm_race_result_pid,
               srm_race_result.points AS srm_race_result_points,
               srm_race_result.race AS srm_race_result_race,
               srm_race_result.status AS srm_race_result_status,
               srm_regatta."left" AS srm_regatta_left,
               srm_regatta.boat_class AS srm_regatta_boat_class,
               srm_regatta.discards AS srm_regatta_discards,
               srm_regatta.is_cancelled AS srm_regatta_is_cancelled,
               srm_regatta.kind AS srm_regatta_kind,
               srm_regatta.perma_name AS srm_regatta_perma_name,
               srm_regatta.pid AS srm_regatta_pid,
               srm_regatta.races AS srm_regatta_races,
               srm_regatta.result__date AS srm_regatta_result__date,
               srm_regatta.result__software AS srm_regatta_result__software,
               srm_regatta.result__status AS srm_regatta_result__status,
               srm_regatta_c.is_team_race AS srm_regatta_c_is_team_race,
               srm_regatta_c.pid AS srm_regatta_c_pid,
               srm_regatta_event."desc" AS srm_regatta_event_desc,
               srm_regatta_event.__raw_name AS srm_regatta_event___raw_name,
               srm_regatta_event.club AS srm_regatta_event_club,
               srm_regatta_event.date__finish AS srm_regatta_event_date__finish,
               srm_regatta_event.date__start AS srm_regatta_event_date__start,
               srm_regatta_event.is_cancelled AS srm_regatta_event_is_cancelled,
               srm_regatta_event.name AS srm_regatta_event_name,
               srm_regatta_event.perma_name AS srm_regatta_event_perma_name,
               srm_regatta_event.pid AS srm_regatta_event_pid,
               srm_sailor."left" AS srm_sailor_left,
               srm_sailor.__raw_mna_number AS srm_sailor___raw_mna_number,
               srm_sailor.club AS srm_sailor_club,
               srm_sailor.mna_number AS srm_sailor_mna_number,
               srm_sailor.nation AS srm_sailor_nation,
               srm_sailor.pid AS srm_sailor_pid,
               srm_team."desc" AS srm_team_desc,
               srm_team."left" AS srm_team_left,
               srm_team.__raw_name AS srm_team___raw_name,
               srm_team.club AS srm_team_club,
               srm_team.leader AS srm_team_leader,
               srm_team.name AS srm_team_name,
               srm_team.pid AS srm_team_pid,
               srm_team.place AS srm_team_place,
               srm_team.registration_date AS srm_team_registration_date,
               srm_team_has_boat_in_regatta."left" AS srm_team_has_boat_in_regatta_left,
               srm_team_has_boat_in_regatta."right" AS srm_team_has_boat_in_regatta_right,
               srm_team_has_boat_in_regatta.pid AS srm_team_has_boat_in_regatta_pid
        FROM mom_id_entity
           LEFT OUTER JOIN srm__boat_class_ ON mom_id_entity.pid = srm__boat_class_.pid
           LEFT OUTER JOIN srm_boat_class ON srm__boat_class_.pid = srm_boat_class.pid
           LEFT OUTER JOIN srm_boat ON mom_id_entity.pid = srm_boat.pid
           LEFT OUTER JOIN srm_club ON mom_id_entity.pid = srm_club.pid
           LEFT OUTER JOIN srm_regatta_event ON mom_id_entity.pid = srm_regatta_event.pid
           LEFT OUTER JOIN srm_regatta ON mom_id_entity.pid = srm_regatta.pid
           LEFT OUTER JOIN srm_regatta_c ON srm_regatta.pid = srm_regatta_c.pid
           LEFT OUTER JOIN srm_sailor ON mom_id_entity.pid = srm_sailor.pid
           LEFT OUTER JOIN srm_boat_in_regatta ON mom_id_entity.pid = srm_boat_in_regatta.pid
           LEFT OUTER JOIN srm_race_result ON mom_id_entity.pid = srm_race_result.pid
           LEFT OUTER JOIN srm_team ON mom_id_entity.pid = srm_team.pid
           LEFT OUTER JOIN srm_crew_member ON mom_id_entity.pid = srm_crew_member.pid
           LEFT OUTER JOIN srm_team_has_boat_in_regatta ON mom_id_entity.pid = srm_team_has_boat_in_regatta.pid
        WHERE mom_id_entity.pid = srm__boat_class_.pid
            OR mom_id_entity.pid = srm_boat_class.pid
            OR mom_id_entity.pid = srm_boat.pid
            OR mom_id_entity.pid = srm_club.pid
            OR mom_id_entity.pid = srm_regatta_event.pid
            OR mom_id_entity.pid = srm_regatta.pid
            OR mom_id_entity.pid = srm_regatta_c.pid
            OR mom_id_entity.pid = srm_sailor.pid
            OR mom_id_entity.pid = srm_boat_in_regatta.pid
            OR mom_id_entity.pid = srm_race_result.pid
            OR mom_id_entity.pid = srm_team.pid
            OR mom_id_entity.pid = srm_crew_member.pid
            OR mom_id_entity.pid = srm_team_has_boat_in_regatta.pid
    SRM.Object
        SELECT mom_id_entity.electric AS mom_id_entity_electric,
               mom_id_entity.last_cid AS mom_id_entity_last_cid,
               mom_id_entity.pid AS mom_id_entity_pid,
               mom_id_entity.type_name AS mom_id_entity_type_name,
               mom_id_entity.x_locked AS mom_id_entity_x_locked,
               srm__boat_class_.__raw_name AS srm__boat_class____raw_name,
               srm__boat_class_.name AS srm__boat_class__name,
               srm__boat_class_.pid AS srm__boat_class__pid,
               srm_boat_class.beam AS srm_boat_class_beam,
               srm_boat_class.loa AS srm_boat_class_loa,
               srm_boat_class.max_crew AS srm_boat_class_max_crew,
               srm_boat_class.pid AS srm_boat_class_pid,
               srm_boat_class.sail_area AS srm_boat_class_sail_area,
               srm_club.__raw_name AS srm_club___raw_name,
               srm_club.long_name AS srm_club_long_name,
               srm_club.name AS srm_club_name,
               srm_club.pid AS srm_club_pid,
               srm_regatta_event."desc" AS srm_regatta_event_desc,
               srm_regatta_event.__raw_name AS srm_regatta_event___raw_name,
               srm_regatta_event.club AS srm_regatta_event_club,
               srm_regatta_event.date__finish AS srm_regatta_event_date__finish,
               srm_regatta_event.date__start AS srm_regatta_event_date__start,
               srm_regatta_event.is_cancelled AS srm_regatta_event_is_cancelled,
               srm_regatta_event.name AS srm_regatta_event_name,
               srm_regatta_event.perma_name AS srm_regatta_event_perma_name,
               srm_regatta_event.pid AS srm_regatta_event_pid
        FROM mom_id_entity
           LEFT OUTER JOIN srm__boat_class_ ON mom_id_entity.pid = srm__boat_class_.pid
           LEFT OUTER JOIN srm_boat_class ON srm__boat_class_.pid = srm_boat_class.pid
           LEFT OUTER JOIN srm_club ON mom_id_entity.pid = srm_club.pid
           LEFT OUTER JOIN srm_regatta_event ON mom_id_entity.pid = srm_regatta_event.pid
        WHERE mom_id_entity.pid = srm__boat_class_.pid
            OR mom_id_entity.pid = srm_boat_class.pid
            OR mom_id_entity.pid = srm_club.pid
            OR mom_id_entity.pid = srm_regatta_event.pid
    SRM._Boat_Class_
        SELECT mom_id_entity.electric AS mom_id_entity_electric,
               mom_id_entity.last_cid AS mom_id_entity_last_cid,
               mom_id_entity.pid AS mom_id_entity_pid,
               mom_id_entity.type_name AS mom_id_entity_type_name,
               mom_id_entity.x_locked AS mom_id_entity_x_locked,
               srm__boat_class_.__raw_name AS srm__boat_class____raw_name,
               srm__boat_class_.name AS srm__boat_class__name,
               srm__boat_class_.pid AS srm__boat_class__pid,
               srm_boat_class.beam AS srm_boat_class_beam,
               srm_boat_class.loa AS srm_boat_class_loa,
               srm_boat_class.max_crew AS srm_boat_class_max_crew,
               srm_boat_class.pid AS srm_boat_class_pid,
               srm_boat_class.sail_area AS srm_boat_class_sail_area
        FROM mom_id_entity
           JOIN srm__boat_class_ ON mom_id_entity.pid = srm__boat_class_.pid
           LEFT OUTER JOIN srm_boat_class ON srm__boat_class_.pid = srm_boat_class.pid
    SRM.Boat_Class SRM._Boat_Class_
        SELECT mom_id_entity.electric AS mom_id_entity_electric,
               mom_id_entity.last_cid AS mom_id_entity_last_cid,
               mom_id_entity.pid AS mom_id_entity_pid,
               mom_id_entity.type_name AS mom_id_entity_type_name,
               mom_id_entity.x_locked AS mom_id_entity_x_locked,
               srm__boat_class_.__raw_name AS srm__boat_class____raw_name,
               srm__boat_class_.name AS srm__boat_class__name,
               srm__boat_class_.pid AS srm__boat_class__pid,
               srm_boat_class.beam AS srm_boat_class_beam,
               srm_boat_class.loa AS srm_boat_class_loa,
               srm_boat_class.max_crew AS srm_boat_class_max_crew,
               srm_boat_class.pid AS srm_boat_class_pid,
               srm_boat_class.sail_area AS srm_boat_class_sail_area
        FROM mom_id_entity
           JOIN srm__boat_class_ ON mom_id_entity.pid = srm__boat_class_.pid
           JOIN srm_boat_class ON srm__boat_class_.pid = srm_boat_class.pid
    SRM.Handicap SRM._Boat_Class_
        SELECT mom_id_entity.electric AS mom_id_entity_electric,
               mom_id_entity.last_cid AS mom_id_entity_last_cid,
               mom_id_entity.pid AS mom_id_entity_pid,
               mom_id_entity.type_name AS mom_id_entity_type_name,
               mom_id_entity.x_locked AS mom_id_entity_x_locked,
               srm__boat_class_.__raw_name AS srm__boat_class____raw_name,
               srm__boat_class_.name AS srm__boat_class__name,
               srm__boat_class_.pid AS srm__boat_class__pid,
               srm_handicap.pid AS srm_handicap_pid
        FROM mom_id_entity
           JOIN srm__boat_class_ ON mom_id_entity.pid = srm__boat_class_.pid
           JOIN srm_handicap ON srm__boat_class_.pid = srm_handicap.pid
    SRM.Link
        SELECT mom_id_entity.electric AS mom_id_entity_electric,
               mom_id_entity.last_cid AS mom_id_entity_last_cid,
               mom_id_entity.pid AS mom_id_entity_pid,
               mom_id_entity.type_name AS mom_id_entity_type_name,
               mom_id_entity.x_locked AS mom_id_entity_x_locked,
               srm_boat."left" AS srm_boat_left,
               srm_boat.__raw_sail_number AS srm_boat___raw_sail_number,
               srm_boat.__raw_sail_number_x AS srm_boat___raw_sail_number_x,
               srm_boat.name AS srm_boat_name,
               srm_boat.nation AS srm_boat_nation,
               srm_boat.pid AS srm_boat_pid,
               srm_boat.sail_number AS srm_boat_sail_number,
               srm_boat.sail_number_x AS srm_boat_sail_number_x,
               srm_boat_in_regatta."left" AS srm_boat_in_regatta_left,
               srm_boat_in_regatta."right" AS srm_boat_in_regatta_right,
               srm_boat_in_regatta.pid AS srm_boat_in_regatta_pid,
               srm_boat_in_regatta.place AS srm_boat_in_regatta_place,
               srm_boat_in_regatta.points AS srm_boat_in_regatta_points,
               srm_boat_in_regatta.rank AS srm_boat_in_regatta_rank,
               srm_boat_in_regatta.registration_date AS srm_boat_in_regatta_registration_date,
               srm_boat_in_regatta.skipper AS srm_boat_in_regatta_skipper,
               srm_crew_member."left" AS srm_crew_member_left,
               srm_crew_member."right" AS srm_crew_member_right,
               srm_crew_member.key AS srm_crew_member_key,
               srm_crew_member.pid AS srm_crew_member_pid,
               srm_crew_member.role AS srm_crew_member_role,
               srm_race_result."left" AS srm_race_result_left,
               srm_race_result.discarded AS srm_race_result_discarded,
               srm_race_result.pid AS srm_race_result_pid,
               srm_race_result.points AS srm_race_result_points,
               srm_race_result.race AS srm_race_result_race,
               srm_race_result.status AS srm_race_result_status,
               srm_regatta."left" AS srm_regatta_left,
               srm_regatta.boat_class AS srm_regatta_boat_class,
               srm_regatta.discards AS srm_regatta_discards,
               srm_regatta.is_cancelled AS srm_regatta_is_cancelled,
               srm_regatta.kind AS srm_regatta_kind,
               srm_regatta.perma_name AS srm_regatta_perma_name,
               srm_regatta.pid AS srm_regatta_pid,
               srm_regatta.races AS srm_regatta_races,
               srm_regatta.result__date AS srm_regatta_result__date,
               srm_regatta.result__software AS srm_regatta_result__software,
               srm_regatta.result__status AS srm_regatta_result__status,
               srm_regatta_c.is_team_race AS srm_regatta_c_is_team_race,
               srm_regatta_c.pid AS srm_regatta_c_pid,
               srm_sailor."left" AS srm_sailor_left,
               srm_sailor.__raw_mna_number AS srm_sailor___raw_mna_number,
               srm_sailor.club AS srm_sailor_club,
               srm_sailor.mna_number AS srm_sailor_mna_number,
               srm_sailor.nation AS srm_sailor_nation,
               srm_sailor.pid AS srm_sailor_pid,
               srm_team."desc" AS srm_team_desc,
               srm_team."left" AS srm_team_left,
               srm_team.__raw_name AS srm_team___raw_name,
               srm_team.club AS srm_team_club,
               srm_team.leader AS srm_team_leader,
               srm_team.name AS srm_team_name,
               srm_team.pid AS srm_team_pid,
               srm_team.place AS srm_team_place,
               srm_team.registration_date AS srm_team_registration_date,
               srm_team_has_boat_in_regatta."left" AS srm_team_has_boat_in_regatta_left,
               srm_team_has_boat_in_regatta."right" AS srm_team_has_boat_in_regatta_right,
               srm_team_has_boat_in_regatta.pid AS srm_team_has_boat_in_regatta_pid
        FROM mom_id_entity
           LEFT OUTER JOIN srm_boat ON mom_id_entity.pid = srm_boat.pid
           LEFT OUTER JOIN srm_regatta ON mom_id_entity.pid = srm_regatta.pid
           LEFT OUTER JOIN srm_regatta_c ON srm_regatta.pid = srm_regatta_c.pid
           LEFT OUTER JOIN srm_sailor ON mom_id_entity.pid = srm_sailor.pid
           LEFT OUTER JOIN srm_boat_in_regatta ON mom_id_entity.pid = srm_boat_in_regatta.pid
           LEFT OUTER JOIN srm_race_result ON mom_id_entity.pid = srm_race_result.pid
           LEFT OUTER JOIN srm_team ON mom_id_entity.pid = srm_team.pid
           LEFT OUTER JOIN srm_crew_member ON mom_id_entity.pid = srm_crew_member.pid
           LEFT OUTER JOIN srm_team_has_boat_in_regatta ON mom_id_entity.pid = srm_team_has_boat_in_regatta.pid
        WHERE mom_id_entity.pid = srm_boat.pid
            OR mom_id_entity.pid = srm_regatta.pid
            OR mom_id_entity.pid = srm_regatta_c.pid
            OR mom_id_entity.pid = srm_sailor.pid
            OR mom_id_entity.pid = srm_boat_in_regatta.pid
            OR mom_id_entity.pid = srm_race_result.pid
            OR mom_id_entity.pid = srm_team.pid
            OR mom_id_entity.pid = srm_crew_member.pid
            OR mom_id_entity.pid = srm_team_has_boat_in_regatta.pid
    SRM.Link1
        SELECT mom_id_entity.electric AS mom_id_entity_electric,
               mom_id_entity.last_cid AS mom_id_entity_last_cid,
               mom_id_entity.pid AS mom_id_entity_pid,
               mom_id_entity.type_name AS mom_id_entity_type_name,
               mom_id_entity.x_locked AS mom_id_entity_x_locked,
               srm_boat."left" AS srm_boat_left,
               srm_boat.__raw_sail_number AS srm_boat___raw_sail_number,
               srm_boat.__raw_sail_number_x AS srm_boat___raw_sail_number_x,
               srm_boat.name AS srm_boat_name,
               srm_boat.nation AS srm_boat_nation,
               srm_boat.pid AS srm_boat_pid,
               srm_boat.sail_number AS srm_boat_sail_number,
               srm_boat.sail_number_x AS srm_boat_sail_number_x,
               srm_race_result."left" AS srm_race_result_left,
               srm_race_result.discarded AS srm_race_result_discarded,
               srm_race_result.pid AS srm_race_result_pid,
               srm_race_result.points AS srm_race_result_points,
               srm_race_result.race AS srm_race_result_race,
               srm_race_result.status AS srm_race_result_status,
               srm_regatta."left" AS srm_regatta_left,
               srm_regatta.boat_class AS srm_regatta_boat_class,
               srm_regatta.discards AS srm_regatta_discards,
               srm_regatta.is_cancelled AS srm_regatta_is_cancelled,
               srm_regatta.kind AS srm_regatta_kind,
               srm_regatta.perma_name AS srm_regatta_perma_name,
               srm_regatta.pid AS srm_regatta_pid,
               srm_regatta.races AS srm_regatta_races,
               srm_regatta.result__date AS srm_regatta_result__date,
               srm_regatta.result__software AS srm_regatta_result__software,
               srm_regatta.result__status AS srm_regatta_result__status,
               srm_regatta_c.is_team_race AS srm_regatta_c_is_team_race,
               srm_regatta_c.pid AS srm_regatta_c_pid,
               srm_sailor."left" AS srm_sailor_left,
               srm_sailor.__raw_mna_number AS srm_sailor___raw_mna_number,
               srm_sailor.club AS srm_sailor_club,
               srm_sailor.mna_number AS srm_sailor_mna_number,
               srm_sailor.nation AS srm_sailor_nation,
               srm_sailor.pid AS srm_sailor_pid,
               srm_team."desc" AS srm_team_desc,
               srm_team."left" AS srm_team_left,
               srm_team.__raw_name AS srm_team___raw_name,
               srm_team.club AS srm_team_club,
               srm_team.leader AS srm_team_leader,
               srm_team.name AS srm_team_name,
               srm_team.pid AS srm_team_pid,
               srm_team.place AS srm_team_place,
               srm_team.registration_date AS srm_team_registration_date
        FROM mom_id_entity
           LEFT OUTER JOIN srm_boat ON mom_id_entity.pid = srm_boat.pid
           LEFT OUTER JOIN srm_regatta ON mom_id_entity.pid = srm_regatta.pid
           LEFT OUTER JOIN srm_regatta_c ON srm_regatta.pid = srm_regatta_c.pid
           LEFT OUTER JOIN srm_sailor ON mom_id_entity.pid = srm_sailor.pid
           LEFT OUTER JOIN srm_race_result ON mom_id_entity.pid = srm_race_result.pid
           LEFT OUTER JOIN srm_team ON mom_id_entity.pid = srm_team.pid
        WHERE mom_id_entity.pid = srm_boat.pid
            OR mom_id_entity.pid = srm_regatta.pid
            OR mom_id_entity.pid = srm_regatta_c.pid
            OR mom_id_entity.pid = srm_sailor.pid
            OR mom_id_entity.pid = srm_race_result.pid
            OR mom_id_entity.pid = srm_team.pid
    SRM.Boat
        SELECT mom_id_entity.electric AS mom_id_entity_electric,
               mom_id_entity.last_cid AS mom_id_entity_last_cid,
               mom_id_entity.pid AS mom_id_entity_pid,
               mom_id_entity.type_name AS mom_id_entity_type_name,
               mom_id_entity.x_locked AS mom_id_entity_x_locked,
               srm_boat."left" AS srm_boat_left,
               srm_boat.__raw_sail_number AS srm_boat___raw_sail_number,
               srm_boat.__raw_sail_number_x AS srm_boat___raw_sail_number_x,
               srm_boat.name AS srm_boat_name,
               srm_boat.nation AS srm_boat_nation,
               srm_boat.pid AS srm_boat_pid,
               srm_boat.sail_number AS srm_boat_sail_number,
               srm_boat.sail_number_x AS srm_boat_sail_number_x
        FROM mom_id_entity
           JOIN srm_boat ON mom_id_entity.pid = srm_boat.pid
    SRM.Club
        SELECT mom_id_entity.electric AS mom_id_entity_electric,
               mom_id_entity.last_cid AS mom_id_entity_last_cid,
               mom_id_entity.pid AS mom_id_entity_pid,
               mom_id_entity.type_name AS mom_id_entity_type_name,
               mom_id_entity.x_locked AS mom_id_entity_x_locked,
               srm_club.__raw_name AS srm_club___raw_name,
               srm_club.long_name AS srm_club_long_name,
               srm_club.name AS srm_club_name,
               srm_club.pid AS srm_club_pid
        FROM mom_id_entity
           JOIN srm_club ON mom_id_entity.pid = srm_club.pid
    SRM.Regatta_Event
        SELECT mom_id_entity.electric AS mom_id_entity_electric,
               mom_id_entity.last_cid AS mom_id_entity_last_cid,
               mom_id_entity.pid AS mom_id_entity_pid,
               mom_id_entity.type_name AS mom_id_entity_type_name,
               mom_id_entity.x_locked AS mom_id_entity_x_locked,
               srm_regatta_event."desc" AS srm_regatta_event_desc,
               srm_regatta_event.__raw_name AS srm_regatta_event___raw_name,
               srm_regatta_event.club AS srm_regatta_event_club,
               srm_regatta_event.date__finish AS srm_regatta_event_date__finish,
               srm_regatta_event.date__start AS srm_regatta_event_date__start,
               srm_regatta_event.is_cancelled AS srm_regatta_event_is_cancelled,
               srm_regatta_event.name AS srm_regatta_event_name,
               srm_regatta_event.perma_name AS srm_regatta_event_perma_name,
               srm_regatta_event.pid AS srm_regatta_event_pid
        FROM mom_id_entity
           JOIN srm_regatta_event ON mom_id_entity.pid = srm_regatta_event.pid
    SWP.Link
        SELECT mom_id_entity.electric AS mom_id_entity_electric,
               mom_id_entity.last_cid AS mom_id_entity_last_cid,
               mom_id_entity.pid AS mom_id_entity_pid,
               mom_id_entity.type_name AS mom_id_entity_type_name,
               mom_id_entity.x_locked AS mom_id_entity_x_locked,
               swp_clip_o."left" AS swp_clip_o_left,
               swp_clip_o.abstract AS swp_clip_o_abstract,
               swp_clip_o.contents AS swp_clip_o_contents,
               swp_clip_o.date__finish AS swp_clip_o_date__finish,
               swp_clip_o.date__start AS swp_clip_o_date__start,
               swp_clip_o.date_x__finish AS swp_clip_o_date_x__finish,
               swp_clip_o.date_x__start AS swp_clip_o_date_x__start,
               swp_clip_o.pid AS swp_clip_o_pid,
               swp_clip_o.prio AS swp_clip_o_prio,
               swp_picture."left" AS swp_picture_left,
               swp_picture.name AS swp_picture_name,
               swp_picture.number AS swp_picture_number,
               swp_picture.photo__extension AS swp_picture_photo__extension,
               swp_picture.photo__height AS swp_picture_photo__height,
               swp_picture.photo__width AS swp_picture_photo__width,
               swp_picture.pid AS swp_picture_pid,
               swp_picture.thumb__extension AS swp_picture_thumb__extension,
               swp_picture.thumb__height AS swp_picture_thumb__height,
               swp_picture.thumb__width AS swp_picture_thumb__width
        FROM mom_id_entity
           LEFT OUTER JOIN swp_clip_o ON mom_id_entity.pid = swp_clip_o.pid
           LEFT OUTER JOIN swp_picture ON mom_id_entity.pid = swp_picture.pid
        WHERE mom_id_entity.pid = swp_clip_o.pid
            OR mom_id_entity.pid = swp_picture.pid
    SWP.Link1
        SELECT mom_id_entity.electric AS mom_id_entity_electric,
               mom_id_entity.last_cid AS mom_id_entity_last_cid,
               mom_id_entity.pid AS mom_id_entity_pid,
               mom_id_entity.type_name AS mom_id_entity_type_name,
               mom_id_entity.x_locked AS mom_id_entity_x_locked,
               swp_clip_o."left" AS swp_clip_o_left,
               swp_clip_o.abstract AS swp_clip_o_abstract,
               swp_clip_o.contents AS swp_clip_o_contents,
               swp_clip_o.date__finish AS swp_clip_o_date__finish,
               swp_clip_o.date__start AS swp_clip_o_date__start,
               swp_clip_o.date_x__finish AS swp_clip_o_date_x__finish,
               swp_clip_o.date_x__start AS swp_clip_o_date_x__start,
               swp_clip_o.pid AS swp_clip_o_pid,
               swp_clip_o.prio AS swp_clip_o_prio,
               swp_picture."left" AS swp_picture_left,
               swp_picture.name AS swp_picture_name,
               swp_picture.number AS swp_picture_number,
               swp_picture.photo__extension AS swp_picture_photo__extension,
               swp_picture.photo__height AS swp_picture_photo__height,
               swp_picture.photo__width AS swp_picture_photo__width,
               swp_picture.pid AS swp_picture_pid,
               swp_picture.thumb__extension AS swp_picture_thumb__extension,
               swp_picture.thumb__height AS swp_picture_thumb__height,
               swp_picture.thumb__width AS swp_picture_thumb__width
        FROM mom_id_entity
           LEFT OUTER JOIN swp_clip_o ON mom_id_entity.pid = swp_clip_o.pid
           LEFT OUTER JOIN swp_picture ON mom_id_entity.pid = swp_picture.pid
        WHERE mom_id_entity.pid = swp_clip_o.pid
            OR mom_id_entity.pid = swp_picture.pid
    SWP.Clip_O
        SELECT mom_id_entity.electric AS mom_id_entity_electric,
               mom_id_entity.last_cid AS mom_id_entity_last_cid,
               mom_id_entity.pid AS mom_id_entity_pid,
               mom_id_entity.type_name AS mom_id_entity_type_name,
               mom_id_entity.x_locked AS mom_id_entity_x_locked,
               swp_clip_o."left" AS swp_clip_o_left,
               swp_clip_o.abstract AS swp_clip_o_abstract,
               swp_clip_o.contents AS swp_clip_o_contents,
               swp_clip_o.date__finish AS swp_clip_o_date__finish,
               swp_clip_o.date__start AS swp_clip_o_date__start,
               swp_clip_o.date_x__finish AS swp_clip_o_date_x__finish,
               swp_clip_o.date_x__start AS swp_clip_o_date_x__start,
               swp_clip_o.pid AS swp_clip_o_pid,
               swp_clip_o.prio AS swp_clip_o_prio
        FROM mom_id_entity
           JOIN swp_clip_o ON mom_id_entity.pid = swp_clip_o.pid
    SWP.Clip_X SWP.Page
        SELECT mom_id_entity.electric AS mom_id_entity_electric,
               mom_id_entity.last_cid AS mom_id_entity_last_cid,
               mom_id_entity.pid AS mom_id_entity_pid,
               mom_id_entity.type_name AS mom_id_entity_type_name,
               mom_id_entity.x_locked AS mom_id_entity_x_locked,
               swp_clip_x.link_to AS swp_clip_x_link_to,
               swp_clip_x.pid AS swp_clip_x_pid,
               swp_page.contents AS swp_page_contents,
               swp_page.date__finish AS swp_page_date__finish,
               swp_page.date__start AS swp_page_date__start,
               swp_page.format AS swp_page_format,
               swp_page.head_line AS swp_page_head_line,
               swp_page.hidden AS swp_page_hidden,
               swp_page.perma_name AS swp_page_perma_name,
               swp_page.pid AS swp_page_pid,
               swp_page.prio AS swp_page_prio,
               swp_page.short_title AS swp_page_short_title,
               swp_page.text AS swp_page_text,
               swp_page.title AS swp_page_title
        FROM mom_id_entity
           JOIN swp_page ON mom_id_entity.pid = swp_page.pid
           JOIN swp_clip_x ON swp_page.pid = swp_clip_x.pid
    SWP.Gallery
        SELECT mom_id_entity.electric AS mom_id_entity_electric,
               mom_id_entity.last_cid AS mom_id_entity_last_cid,
               mom_id_entity.pid AS mom_id_entity_pid,
               mom_id_entity.type_name AS mom_id_entity_type_name,
               mom_id_entity.x_locked AS mom_id_entity_x_locked,
               swp_gallery.date__finish AS swp_gallery_date__finish,
               swp_gallery.date__start AS swp_gallery_date__start,
               swp_gallery.directory AS swp_gallery_directory,
               swp_gallery.perma_name AS swp_gallery_perma_name,
               swp_gallery.pid AS swp_gallery_pid,
               swp_gallery.short_title AS swp_gallery_short_title,
               swp_gallery.title AS swp_gallery_title
        FROM mom_id_entity
           JOIN swp_gallery ON mom_id_entity.pid = swp_gallery.pid
    SWP.Picture
        SELECT mom_id_entity.electric AS mom_id_entity_electric,
               mom_id_entity.last_cid AS mom_id_entity_last_cid,
               mom_id_entity.pid AS mom_id_entity_pid,
               mom_id_entity.type_name AS mom_id_entity_type_name,
               mom_id_entity.x_locked AS mom_id_entity_x_locked,
               swp_picture."left" AS swp_picture_left,
               swp_picture.name AS swp_picture_name,
               swp_picture.number AS swp_picture_number,
               swp_picture.photo__extension AS swp_picture_photo__extension,
               swp_picture.photo__height AS swp_picture_photo__height,
               swp_picture.photo__width AS swp_picture_photo__width,
               swp_picture.pid AS swp_picture_pid,
               swp_picture.thumb__extension AS swp_picture_thumb__extension,
               swp_picture.thumb__height AS swp_picture_thumb__height,
               swp_picture.thumb__width AS swp_picture_thumb__width
        FROM mom_id_entity
           JOIN swp_picture ON mom_id_entity.pid = swp_picture.pid
    SRM.Page SWP.Page
        SELECT mom_id_entity.electric AS mom_id_entity_electric,
               mom_id_entity.last_cid AS mom_id_entity_last_cid,
               mom_id_entity.pid AS mom_id_entity_pid,
               mom_id_entity.type_name AS mom_id_entity_type_name,
               mom_id_entity.x_locked AS mom_id_entity_x_locked,
               srm_page."desc" AS srm_page_desc,
               srm_page.event AS srm_page_event,
               srm_page.pid AS srm_page_pid,
               swp_page.contents AS swp_page_contents,
               swp_page.date__finish AS swp_page_date__finish,
               swp_page.date__start AS swp_page_date__start,
               swp_page.format AS swp_page_format,
               swp_page.head_line AS swp_page_head_line,
               swp_page.hidden AS swp_page_hidden,
               swp_page.perma_name AS swp_page_perma_name,
               swp_page.pid AS swp_page_pid,
               swp_page.prio AS swp_page_prio,
               swp_page.short_title AS swp_page_short_title,
               swp_page.text AS swp_page_text,
               swp_page.title AS swp_page_title
        FROM mom_id_entity
           JOIN swp_page ON mom_id_entity.pid = swp_page.pid
           JOIN srm_page ON swp_page.pid = srm_page.pid
    SRM.Regatta
        SELECT mom_id_entity.electric AS mom_id_entity_electric,
               mom_id_entity.last_cid AS mom_id_entity_last_cid,
               mom_id_entity.pid AS mom_id_entity_pid,
               mom_id_entity.type_name AS mom_id_entity_type_name,
               mom_id_entity.x_locked AS mom_id_entity_x_locked,
               srm_regatta."left" AS srm_regatta_left,
               srm_regatta.boat_class AS srm_regatta_boat_class,
               srm_regatta.discards AS srm_regatta_discards,
               srm_regatta.is_cancelled AS srm_regatta_is_cancelled,
               srm_regatta.kind AS srm_regatta_kind,
               srm_regatta.perma_name AS srm_regatta_perma_name,
               srm_regatta.pid AS srm_regatta_pid,
               srm_regatta.races AS srm_regatta_races,
               srm_regatta.result__date AS srm_regatta_result__date,
               srm_regatta.result__software AS srm_regatta_result__software,
               srm_regatta.result__status AS srm_regatta_result__status,
               srm_regatta_c.is_team_race AS srm_regatta_c_is_team_race,
               srm_regatta_c.pid AS srm_regatta_c_pid
        FROM mom_id_entity
           JOIN srm_regatta ON mom_id_entity.pid = srm_regatta.pid
           LEFT OUTER JOIN srm_regatta_c ON srm_regatta.pid = srm_regatta_c.pid
    SRM.Regatta_C SRM.Regatta
        SELECT mom_id_entity.electric AS mom_id_entity_electric,
               mom_id_entity.last_cid AS mom_id_entity_last_cid,
               mom_id_entity.pid AS mom_id_entity_pid,
               mom_id_entity.type_name AS mom_id_entity_type_name,
               mom_id_entity.x_locked AS mom_id_entity_x_locked,
               srm_regatta."left" AS srm_regatta_left,
               srm_regatta.boat_class AS srm_regatta_boat_class,
               srm_regatta.discards AS srm_regatta_discards,
               srm_regatta.is_cancelled AS srm_regatta_is_cancelled,
               srm_regatta.kind AS srm_regatta_kind,
               srm_regatta.perma_name AS srm_regatta_perma_name,
               srm_regatta.pid AS srm_regatta_pid,
               srm_regatta.races AS srm_regatta_races,
               srm_regatta.result__date AS srm_regatta_result__date,
               srm_regatta.result__software AS srm_regatta_result__software,
               srm_regatta.result__status AS srm_regatta_result__status,
               srm_regatta_c.is_team_race AS srm_regatta_c_is_team_race,
               srm_regatta_c.pid AS srm_regatta_c_pid
        FROM mom_id_entity
           JOIN srm_regatta ON mom_id_entity.pid = srm_regatta.pid
           JOIN srm_regatta_c ON srm_regatta.pid = srm_regatta_c.pid
    SRM.Regatta_H SRM.Regatta
        SELECT mom_id_entity.electric AS mom_id_entity_electric,
               mom_id_entity.last_cid AS mom_id_entity_last_cid,
               mom_id_entity.pid AS mom_id_entity_pid,
               mom_id_entity.type_name AS mom_id_entity_type_name,
               mom_id_entity.x_locked AS mom_id_entity_x_locked,
               srm_regatta."left" AS srm_regatta_left,
               srm_regatta.boat_class AS srm_regatta_boat_class,
               srm_regatta.discards AS srm_regatta_discards,
               srm_regatta.is_cancelled AS srm_regatta_is_cancelled,
               srm_regatta.kind AS srm_regatta_kind,
               srm_regatta.perma_name AS srm_regatta_perma_name,
               srm_regatta.pid AS srm_regatta_pid,
               srm_regatta.races AS srm_regatta_races,
               srm_regatta.result__date AS srm_regatta_result__date,
               srm_regatta.result__software AS srm_regatta_result__software,
               srm_regatta.result__status AS srm_regatta_result__status,
               srm_regatta_h.pid AS srm_regatta_h_pid
        FROM mom_id_entity
           JOIN srm_regatta ON mom_id_entity.pid = srm_regatta.pid
           JOIN srm_regatta_h ON srm_regatta.pid = srm_regatta_h.pid
    SRM.Sailor
        SELECT mom_id_entity.electric AS mom_id_entity_electric,
               mom_id_entity.last_cid AS mom_id_entity_last_cid,
               mom_id_entity.pid AS mom_id_entity_pid,
               mom_id_entity.type_name AS mom_id_entity_type_name,
               mom_id_entity.x_locked AS mom_id_entity_x_locked,
               srm_sailor."left" AS srm_sailor_left,
               srm_sailor.__raw_mna_number AS srm_sailor___raw_mna_number,
               srm_sailor.club AS srm_sailor_club,
               srm_sailor.mna_number AS srm_sailor_mna_number,
               srm_sailor.nation AS srm_sailor_nation,
               srm_sailor.pid AS srm_sailor_pid
        FROM mom_id_entity
           JOIN srm_sailor ON mom_id_entity.pid = srm_sailor.pid
    SRM._MOM_Link_n_
        SELECT mom_id_entity.electric AS mom_id_entity_electric,
               mom_id_entity.last_cid AS mom_id_entity_last_cid,
               mom_id_entity.pid AS mom_id_entity_pid,
               mom_id_entity.type_name AS mom_id_entity_type_name,
               mom_id_entity.x_locked AS mom_id_entity_x_locked,
               srm_boat_in_regatta."left" AS srm_boat_in_regatta_left,
               srm_boat_in_regatta."right" AS srm_boat_in_regatta_right,
               srm_boat_in_regatta.pid AS srm_boat_in_regatta_pid,
               srm_boat_in_regatta.place AS srm_boat_in_regatta_place,
               srm_boat_in_regatta.points AS srm_boat_in_regatta_points,
               srm_boat_in_regatta.rank AS srm_boat_in_regatta_rank,
               srm_boat_in_regatta.registration_date AS srm_boat_in_regatta_registration_date,
               srm_boat_in_regatta.skipper AS srm_boat_in_regatta_skipper,
               srm_crew_member."left" AS srm_crew_member_left,
               srm_crew_member."right" AS srm_crew_member_right,
               srm_crew_member.key AS srm_crew_member_key,
               srm_crew_member.pid AS srm_crew_member_pid,
               srm_crew_member.role AS srm_crew_member_role,
               srm_team_has_boat_in_regatta."left" AS srm_team_has_boat_in_regatta_left,
               srm_team_has_boat_in_regatta."right" AS srm_team_has_boat_in_regatta_right,
               srm_team_has_boat_in_regatta.pid AS srm_team_has_boat_in_regatta_pid
        FROM mom_id_entity
           LEFT OUTER JOIN srm_boat_in_regatta ON mom_id_entity.pid = srm_boat_in_regatta.pid
           LEFT OUTER JOIN srm_crew_member ON mom_id_entity.pid = srm_crew_member.pid
           LEFT OUTER JOIN srm_team_has_boat_in_regatta ON mom_id_entity.pid = srm_team_has_boat_in_regatta.pid
        WHERE mom_id_entity.pid = srm_boat_in_regatta.pid
            OR mom_id_entity.pid = srm_crew_member.pid
            OR mom_id_entity.pid = srm_team_has_boat_in_regatta.pid
    SRM.Link2
        SELECT mom_id_entity.electric AS mom_id_entity_electric,
               mom_id_entity.last_cid AS mom_id_entity_last_cid,
               mom_id_entity.pid AS mom_id_entity_pid,
               mom_id_entity.type_name AS mom_id_entity_type_name,
               mom_id_entity.x_locked AS mom_id_entity_x_locked,
               srm_boat_in_regatta."left" AS srm_boat_in_regatta_left,
               srm_boat_in_regatta."right" AS srm_boat_in_regatta_right,
               srm_boat_in_regatta.pid AS srm_boat_in_regatta_pid,
               srm_boat_in_regatta.place AS srm_boat_in_regatta_place,
               srm_boat_in_regatta.points AS srm_boat_in_regatta_points,
               srm_boat_in_regatta.rank AS srm_boat_in_regatta_rank,
               srm_boat_in_regatta.registration_date AS srm_boat_in_regatta_registration_date,
               srm_boat_in_regatta.skipper AS srm_boat_in_regatta_skipper,
               srm_crew_member."left" AS srm_crew_member_left,
               srm_crew_member."right" AS srm_crew_member_right,
               srm_crew_member.key AS srm_crew_member_key,
               srm_crew_member.pid AS srm_crew_member_pid,
               srm_crew_member.role AS srm_crew_member_role,
               srm_team_has_boat_in_regatta."left" AS srm_team_has_boat_in_regatta_left,
               srm_team_has_boat_in_regatta."right" AS srm_team_has_boat_in_regatta_right,
               srm_team_has_boat_in_regatta.pid AS srm_team_has_boat_in_regatta_pid
        FROM mom_id_entity
           LEFT OUTER JOIN srm_boat_in_regatta ON mom_id_entity.pid = srm_boat_in_regatta.pid
           LEFT OUTER JOIN srm_crew_member ON mom_id_entity.pid = srm_crew_member.pid
           LEFT OUTER JOIN srm_team_has_boat_in_regatta ON mom_id_entity.pid = srm_team_has_boat_in_regatta.pid
        WHERE mom_id_entity.pid = srm_boat_in_regatta.pid
            OR mom_id_entity.pid = srm_crew_member.pid
            OR mom_id_entity.pid = srm_team_has_boat_in_regatta.pid
    SRM.Boat_in_Regatta
        SELECT mom_id_entity.electric AS mom_id_entity_electric,
               mom_id_entity.last_cid AS mom_id_entity_last_cid,
               mom_id_entity.pid AS mom_id_entity_pid,
               mom_id_entity.type_name AS mom_id_entity_type_name,
               mom_id_entity.x_locked AS mom_id_entity_x_locked,
               srm_boat_in_regatta."left" AS srm_boat_in_regatta_left,
               srm_boat_in_regatta."right" AS srm_boat_in_regatta_right,
               srm_boat_in_regatta.pid AS srm_boat_in_regatta_pid,
               srm_boat_in_regatta.place AS srm_boat_in_regatta_place,
               srm_boat_in_regatta.points AS srm_boat_in_regatta_points,
               srm_boat_in_regatta.rank AS srm_boat_in_regatta_rank,
               srm_boat_in_regatta.registration_date AS srm_boat_in_regatta_registration_date,
               srm_boat_in_regatta.skipper AS srm_boat_in_regatta_skipper
        FROM mom_id_entity
           JOIN srm_boat_in_regatta ON mom_id_entity.pid = srm_boat_in_regatta.pid
    SRM.Race_Result
        SELECT mom_id_entity.electric AS mom_id_entity_electric,
               mom_id_entity.last_cid AS mom_id_entity_last_cid,
               mom_id_entity.pid AS mom_id_entity_pid,
               mom_id_entity.type_name AS mom_id_entity_type_name,
               mom_id_entity.x_locked AS mom_id_entity_x_locked,
               srm_race_result."left" AS srm_race_result_left,
               srm_race_result.discarded AS srm_race_result_discarded,
               srm_race_result.pid AS srm_race_result_pid,
               srm_race_result.points AS srm_race_result_points,
               srm_race_result.race AS srm_race_result_race,
               srm_race_result.status AS srm_race_result_status
        FROM mom_id_entity
           JOIN srm_race_result ON mom_id_entity.pid = srm_race_result.pid
    SRM.Team
        SELECT mom_id_entity.electric AS mom_id_entity_electric,
               mom_id_entity.last_cid AS mom_id_entity_last_cid,
               mom_id_entity.pid AS mom_id_entity_pid,
               mom_id_entity.type_name AS mom_id_entity_type_name,
               mom_id_entity.x_locked AS mom_id_entity_x_locked,
               srm_team."desc" AS srm_team_desc,
               srm_team."left" AS srm_team_left,
               srm_team.__raw_name AS srm_team___raw_name,
               srm_team.club AS srm_team_club,
               srm_team.leader AS srm_team_leader,
               srm_team.name AS srm_team_name,
               srm_team.pid AS srm_team_pid,
               srm_team.place AS srm_team_place,
               srm_team.registration_date AS srm_team_registration_date
        FROM mom_id_entity
           JOIN srm_team ON mom_id_entity.pid = srm_team.pid
    SRM.Crew_Member
        SELECT mom_id_entity.electric AS mom_id_entity_electric,
               mom_id_entity.last_cid AS mom_id_entity_last_cid,
               mom_id_entity.pid AS mom_id_entity_pid,
               mom_id_entity.type_name AS mom_id_entity_type_name,
               mom_id_entity.x_locked AS mom_id_entity_x_locked,
               srm_crew_member."left" AS srm_crew_member_left,
               srm_crew_member."right" AS srm_crew_member_right,
               srm_crew_member.key AS srm_crew_member_key,
               srm_crew_member.pid AS srm_crew_member_pid,
               srm_crew_member.role AS srm_crew_member_role
        FROM mom_id_entity
           JOIN srm_crew_member ON mom_id_entity.pid = srm_crew_member.pid
    SRM.Team_has_Boat_in_Regatta
        SELECT mom_id_entity.electric AS mom_id_entity_electric,
               mom_id_entity.last_cid AS mom_id_entity_last_cid,
               mom_id_entity.pid AS mom_id_entity_pid,
               mom_id_entity.type_name AS mom_id_entity_type_name,
               mom_id_entity.x_locked AS mom_id_entity_x_locked,
               srm_team_has_boat_in_regatta."left" AS srm_team_has_boat_in_regatta_left,
               srm_team_has_boat_in_regatta."right" AS srm_team_has_boat_in_regatta_right,
               srm_team_has_boat_in_regatta.pid AS srm_team_has_boat_in_regatta_pid
        FROM mom_id_entity
           JOIN srm_team_has_boat_in_regatta ON mom_id_entity.pid = srm_team_has_boat_in_regatta.pid
    PAP.Subject_has_Address PAP.Subject_has_Property
        SELECT mom_id_entity.electric AS mom_id_entity_electric,
               mom_id_entity.last_cid AS mom_id_entity_last_cid,
               mom_id_entity.pid AS mom_id_entity_pid,
               mom_id_entity.type_name AS mom_id_entity_type_name,
               mom_id_entity.x_locked AS mom_id_entity_x_locked,
               pap_company_has_address.pid AS pap_company_has_address_pid,
               pap_person_has_address.pid AS pap_person_has_address_pid,
               pap_subject_has_property."desc" AS pap_subject_has_property_desc,
               pap_subject_has_property."left" AS pap_subject_has_property_left,
               pap_subject_has_property."right" AS pap_subject_has_property_right,
               pap_subject_has_property.pid AS pap_subject_has_property_pid
        FROM mom_id_entity
           JOIN pap_subject_has_property ON mom_id_entity.pid = pap_subject_has_property.pid
           LEFT OUTER JOIN pap_company_has_address ON pap_subject_has_property.pid = pap_company_has_address.pid
           LEFT OUTER JOIN pap_person_has_address ON pap_subject_has_property.pid = pap_person_has_address.pid
        WHERE mom_id_entity.pid = pap_company_has_address.pid
            OR mom_id_entity.pid = pap_person_has_address.pid
    PAP.Subject_has_Email PAP.Subject_has_Property
        SELECT mom_id_entity.electric AS mom_id_entity_electric,
               mom_id_entity.last_cid AS mom_id_entity_last_cid,
               mom_id_entity.pid AS mom_id_entity_pid,
               mom_id_entity.type_name AS mom_id_entity_type_name,
               mom_id_entity.x_locked AS mom_id_entity_x_locked,
               pap_company_has_email.pid AS pap_company_has_email_pid,
               pap_person_has_email.pid AS pap_person_has_email_pid,
               pap_subject_has_property."desc" AS pap_subject_has_property_desc,
               pap_subject_has_property."left" AS pap_subject_has_property_left,
               pap_subject_has_property."right" AS pap_subject_has_property_right,
               pap_subject_has_property.pid AS pap_subject_has_property_pid
        FROM mom_id_entity
           JOIN pap_subject_has_property ON mom_id_entity.pid = pap_subject_has_property.pid
           LEFT OUTER JOIN pap_company_has_email ON pap_subject_has_property.pid = pap_company_has_email.pid
           LEFT OUTER JOIN pap_person_has_email ON pap_subject_has_property.pid = pap_person_has_email.pid
        WHERE mom_id_entity.pid = pap_company_has_email.pid
            OR mom_id_entity.pid = pap_person_has_email.pid
    PAP.Subject_has_Phone PAP.Subject_has_Property
        SELECT mom_id_entity.electric AS mom_id_entity_electric,
               mom_id_entity.last_cid AS mom_id_entity_last_cid,
               mom_id_entity.pid AS mom_id_entity_pid,
               mom_id_entity.type_name AS mom_id_entity_type_name,
               mom_id_entity.x_locked AS mom_id_entity_x_locked,
               pap_subject_has_phone.extension AS pap_subject_has_phone_extension,
               pap_subject_has_phone.pid AS pap_subject_has_phone_pid,
               pap_subject_has_property."desc" AS pap_subject_has_property_desc,
               pap_subject_has_property."left" AS pap_subject_has_property_left,
               pap_subject_has_property."right" AS pap_subject_has_property_right,
               pap_subject_has_property.pid AS pap_subject_has_property_pid
        FROM mom_id_entity
           JOIN pap_subject_has_property ON mom_id_entity.pid = pap_subject_has_property.pid
           JOIN pap_subject_has_phone ON pap_subject_has_property.pid = pap_subject_has_phone.pid
    PAP.Subject_has_Url PAP.Subject_has_Property
        SELECT mom_id_entity.electric AS mom_id_entity_electric,
               mom_id_entity.last_cid AS mom_id_entity_last_cid,
               mom_id_entity.pid AS mom_id_entity_pid,
               mom_id_entity.type_name AS mom_id_entity_type_name,
               mom_id_entity.x_locked AS mom_id_entity_x_locked,
               pap_company_has_url.pid AS pap_company_has_url_pid,
               pap_person_has_url.pid AS pap_person_has_url_pid,
               pap_subject_has_property."desc" AS pap_subject_has_property_desc,
               pap_subject_has_property."left" AS pap_subject_has_property_left,
               pap_subject_has_property."right" AS pap_subject_has_property_right,
               pap_subject_has_property.pid AS pap_subject_has_property_pid
        FROM mom_id_entity
           JOIN pap_subject_has_property ON mom_id_entity.pid = pap_subject_has_property.pid
           LEFT OUTER JOIN pap_company_has_url ON pap_subject_has_property.pid = pap_company_has_url.pid
           LEFT OUTER JOIN pap_person_has_url ON pap_subject_has_property.pid = pap_person_has_url.pid
        WHERE mom_id_entity.pid = pap_company_has_url.pid
            OR mom_id_entity.pid = pap_person_has_url.pid
    PAP.Company_has_Url PAP.Subject_has_Property
        SELECT mom_id_entity.electric AS mom_id_entity_electric,
               mom_id_entity.last_cid AS mom_id_entity_last_cid,
               mom_id_entity.pid AS mom_id_entity_pid,
               mom_id_entity.type_name AS mom_id_entity_type_name,
               mom_id_entity.x_locked AS mom_id_entity_x_locked,
               pap_company_has_url.pid AS pap_company_has_url_pid,
               pap_subject_has_property."desc" AS pap_subject_has_property_desc,
               pap_subject_has_property."left" AS pap_subject_has_property_left,
               pap_subject_has_property."right" AS pap_subject_has_property_right,
               pap_subject_has_property.pid AS pap_subject_has_property_pid
        FROM mom_id_entity
           JOIN pap_subject_has_property ON mom_id_entity.pid = pap_subject_has_property.pid
           JOIN pap_company_has_url ON pap_subject_has_property.pid = pap_company_has_url.pid
    PAP.Person_has_Url PAP.Subject_has_Property
        SELECT mom_id_entity.electric AS mom_id_entity_electric,
               mom_id_entity.last_cid AS mom_id_entity_last_cid,
               mom_id_entity.pid AS mom_id_entity_pid,
               mom_id_entity.type_name AS mom_id_entity_type_name,
               mom_id_entity.x_locked AS mom_id_entity_x_locked,
               pap_person_has_url.pid AS pap_person_has_url_pid,
               pap_subject_has_property."desc" AS pap_subject_has_property_desc,
               pap_subject_has_property."left" AS pap_subject_has_property_left,
               pap_subject_has_property."right" AS pap_subject_has_property_right,
               pap_subject_has_property.pid AS pap_subject_has_property_pid
        FROM mom_id_entity
           JOIN pap_subject_has_property ON mom_id_entity.pid = pap_subject_has_property.pid
           JOIN pap_person_has_url ON pap_subject_has_property.pid = pap_person_has_url.pid
    PAP.Company_has_Phone PAP.Subject_has_Property
        SELECT mom_id_entity.electric AS mom_id_entity_electric,
               mom_id_entity.last_cid AS mom_id_entity_last_cid,
               mom_id_entity.pid AS mom_id_entity_pid,
               mom_id_entity.type_name AS mom_id_entity_type_name,
               mom_id_entity.x_locked AS mom_id_entity_x_locked,
               pap_company_has_phone.pid AS pap_company_has_phone_pid,
               pap_subject_has_phone.extension AS pap_subject_has_phone_extension,
               pap_subject_has_phone.pid AS pap_subject_has_phone_pid,
               pap_subject_has_property."desc" AS pap_subject_has_property_desc,
               pap_subject_has_property."left" AS pap_subject_has_property_left,
               pap_subject_has_property."right" AS pap_subject_has_property_right,
               pap_subject_has_property.pid AS pap_subject_has_property_pid
        FROM mom_id_entity
           JOIN pap_subject_has_property ON mom_id_entity.pid = pap_subject_has_property.pid
           JOIN pap_subject_has_phone ON pap_subject_has_property.pid = pap_subject_has_phone.pid
           JOIN pap_company_has_phone ON pap_subject_has_phone.pid = pap_company_has_phone.pid
    PAP.Person_has_Phone PAP.Subject_has_Property
        SELECT mom_id_entity.electric AS mom_id_entity_electric,
               mom_id_entity.last_cid AS mom_id_entity_last_cid,
               mom_id_entity.pid AS mom_id_entity_pid,
               mom_id_entity.type_name AS mom_id_entity_type_name,
               mom_id_entity.x_locked AS mom_id_entity_x_locked,
               pap_person_has_phone.pid AS pap_person_has_phone_pid,
               pap_subject_has_phone.extension AS pap_subject_has_phone_extension,
               pap_subject_has_phone.pid AS pap_subject_has_phone_pid,
               pap_subject_has_property."desc" AS pap_subject_has_property_desc,
               pap_subject_has_property."left" AS pap_subject_has_property_left,
               pap_subject_has_property."right" AS pap_subject_has_property_right,
               pap_subject_has_property.pid AS pap_subject_has_property_pid
        FROM mom_id_entity
           JOIN pap_subject_has_property ON mom_id_entity.pid = pap_subject_has_property.pid
           JOIN pap_subject_has_phone ON pap_subject_has_property.pid = pap_subject_has_phone.pid
           JOIN pap_person_has_phone ON pap_subject_has_phone.pid = pap_person_has_phone.pid
    PAP.Company_has_Email PAP.Subject_has_Property
        SELECT mom_id_entity.electric AS mom_id_entity_electric,
               mom_id_entity.last_cid AS mom_id_entity_last_cid,
               mom_id_entity.pid AS mom_id_entity_pid,
               mom_id_entity.type_name AS mom_id_entity_type_name,
               mom_id_entity.x_locked AS mom_id_entity_x_locked,
               pap_company_has_email.pid AS pap_company_has_email_pid,
               pap_subject_has_property."desc" AS pap_subject_has_property_desc,
               pap_subject_has_property."left" AS pap_subject_has_property_left,
               pap_subject_has_property."right" AS pap_subject_has_property_right,
               pap_subject_has_property.pid AS pap_subject_has_property_pid
        FROM mom_id_entity
           JOIN pap_subject_has_property ON mom_id_entity.pid = pap_subject_has_property.pid
           JOIN pap_company_has_email ON pap_subject_has_property.pid = pap_company_has_email.pid
    PAP.Person_has_Email PAP.Subject_has_Property
        SELECT mom_id_entity.electric AS mom_id_entity_electric,
               mom_id_entity.last_cid AS mom_id_entity_last_cid,
               mom_id_entity.pid AS mom_id_entity_pid,
               mom_id_entity.type_name AS mom_id_entity_type_name,
               mom_id_entity.x_locked AS mom_id_entity_x_locked,
               pap_person_has_email.pid AS pap_person_has_email_pid,
               pap_subject_has_property."desc" AS pap_subject_has_property_desc,
               pap_subject_has_property."left" AS pap_subject_has_property_left,
               pap_subject_has_property."right" AS pap_subject_has_property_right,
               pap_subject_has_property.pid AS pap_subject_has_property_pid
        FROM mom_id_entity
           JOIN pap_subject_has_property ON mom_id_entity.pid = pap_subject_has_property.pid
           JOIN pap_person_has_email ON pap_subject_has_property.pid = pap_person_has_email.pid
    PAP.Company_has_Address PAP.Subject_has_Property
        SELECT mom_id_entity.electric AS mom_id_entity_electric,
               mom_id_entity.last_cid AS mom_id_entity_last_cid,
               mom_id_entity.pid AS mom_id_entity_pid,
               mom_id_entity.type_name AS mom_id_entity_type_name,
               mom_id_entity.x_locked AS mom_id_entity_x_locked,
               pap_company_has_address.pid AS pap_company_has_address_pid,
               pap_subject_has_property."desc" AS pap_subject_has_property_desc,
               pap_subject_has_property."left" AS pap_subject_has_property_left,
               pap_subject_has_property."right" AS pap_subject_has_property_right,
               pap_subject_has_property.pid AS pap_subject_has_property_pid
        FROM mom_id_entity
           JOIN pap_subject_has_property ON mom_id_entity.pid = pap_subject_has_property.pid
           JOIN pap_company_has_address ON pap_subject_has_property.pid = pap_company_has_address.pid
    PAP.Person_has_Address PAP.Subject_has_Property
        SELECT mom_id_entity.electric AS mom_id_entity_electric,
               mom_id_entity.last_cid AS mom_id_entity_last_cid,
               mom_id_entity.pid AS mom_id_entity_pid,
               mom_id_entity.type_name AS mom_id_entity_type_name,
               mom_id_entity.x_locked AS mom_id_entity_x_locked,
               pap_person_has_address.pid AS pap_person_has_address_pid,
               pap_subject_has_property."desc" AS pap_subject_has_property_desc,
               pap_subject_has_property."left" AS pap_subject_has_property_left,
               pap_subject_has_property."right" AS pap_subject_has_property_right,
               pap_subject_has_property.pid AS pap_subject_has_property_pid
        FROM mom_id_entity
           JOIN pap_subject_has_property ON mom_id_entity.pid = pap_subject_has_property.pid
           JOIN pap_person_has_address ON pap_subject_has_property.pid = pap_person_has_address.pid

    >>> PET = apt ["PAP.Person"]
    >>> print (formatted_select (PET, select = PET._SAW.select.count ()))
    SELECT count(mom_id_entity_pid) AS tbl_row_count
        FROM (SELECT mom_id_entity.electric AS mom_id_entity_electric,
                     mom_id_entity.last_cid AS mom_id_entity_last_cid,
                     mom_id_entity.pid AS mom_id_entity_pid,
                     mom_id_entity.type_name AS mom_id_entity_type_name,
                     mom_id_entity.x_locked AS mom_id_entity_x_locked,
                     pap_person.__raw_first_name AS pap_person___raw_first_name,
                     pap_person.__raw_last_name AS pap_person___raw_last_name,
                     pap_person.__raw_middle_name AS pap_person___raw_middle_name,
                     pap_person.__raw_title AS pap_person___raw_title,
                     pap_person.first_name AS pap_person_first_name,
                     pap_person.last_name AS pap_person_last_name,
                     pap_person.lifetime__finish AS pap_person_lifetime__finish,
                     pap_person.lifetime__start AS pap_person_lifetime__start,
                     pap_person.middle_name AS pap_person_middle_name,
                     pap_person.pid AS pap_person_pid,
                     pap_person.sex AS pap_person_sex,
                     pap_person.title AS pap_person_title
              FROM mom_id_entity
                 JOIN pap_person ON mom_id_entity.pid = pap_person.pid
             )

    >>> SET = apt._SAW ["PAP.Subject"]
    >>> print (formatted_select (SET.e_type, select = SET.select.count ()))
    SELECT count(mom_id_entity_pid) AS tbl_row_count
        FROM (SELECT mom_id_entity.electric AS mom_id_entity_electric,
                     mom_id_entity.last_cid AS mom_id_entity_last_cid,
                     mom_id_entity.pid AS mom_id_entity_pid,
                     mom_id_entity.type_name AS mom_id_entity_type_name,
                     mom_id_entity.x_locked AS mom_id_entity_x_locked,
                     pap_company.__raw_name AS pap_company___raw_name,
                     pap_company.__raw_registered_in AS pap_company___raw_registered_in,
                     pap_company.__raw_short_name AS pap_company___raw_short_name,
                     pap_company.lifetime__finish AS pap_company_lifetime__finish,
                     pap_company.lifetime__start AS pap_company_lifetime__start,
                     pap_company.name AS pap_company_name,
                     pap_company.pid AS pap_company_pid,
                     pap_company.registered_in AS pap_company_registered_in,
                     pap_company.short_name AS pap_company_short_name,
                     pap_person.__raw_first_name AS pap_person___raw_first_name,
                     pap_person.__raw_last_name AS pap_person___raw_last_name,
                     pap_person.__raw_middle_name AS pap_person___raw_middle_name,
                     pap_person.__raw_title AS pap_person___raw_title,
                     pap_person.first_name AS pap_person_first_name,
                     pap_person.last_name AS pap_person_last_name,
                     pap_person.lifetime__finish AS pap_person_lifetime__finish,
                     pap_person.lifetime__start AS pap_person_lifetime__start,
                     pap_person.middle_name AS pap_person_middle_name,
                     pap_person.pid AS pap_person_pid,
                     pap_person.sex AS pap_person_sex,
                     pap_person.title AS pap_person_title
              FROM mom_id_entity
                 LEFT OUTER JOIN pap_company ON mom_id_entity.pid = pap_company.pid
                 LEFT OUTER JOIN pap_person ON mom_id_entity.pid = pap_person.pid
              WHERE mom_id_entity.pid = pap_company.pid
                  OR mom_id_entity.pid = pap_person.pid
             )

    >>> print (formatted_select (SET.e_type, select = SET.e_type.addresses.sqx (42)))
    SQ [PAP.Subject_has_Address]
            .filter (Q.left == 42)
            .attr (right)

"""

_test_select_strict = """
    >>> apt, url = Scaffold.app_type_and_url (%(p1)s, %(n1)s)

    >>> show_selects (apt, "select_strict")
    MOM.Id_Entity
        SELECT mom_id_entity.pid
        FROM mom_id_entity
        WHERE false
    MOM.MD_Change
        SELECT mom_md_change."user" AS mom_md_change_user,
               mom_md_change.c_time AS mom_md_change_c_time,
               mom_md_change.c_user AS mom_md_change_c_user,
               mom_md_change.cid AS mom_md_change_cid,
               mom_md_change.kind AS mom_md_change_kind,
               mom_md_change.parent_cid AS mom_md_change_parent_cid,
               mom_md_change.pid AS mom_md_change_pid,
               mom_md_change.scm_change AS mom_md_change_scm_change,
               mom_md_change.time AS mom_md_change_time,
               mom_md_change.type_name AS mom_md_change_type_name
        FROM mom_md_change
    MOM.Link
        SELECT mom_id_entity.pid
        FROM mom_id_entity
        WHERE false
    MOM.Link1
        SELECT mom_id_entity.pid
        FROM mom_id_entity
        WHERE false
    MOM._MOM_Link_n_
        SELECT mom_id_entity.pid
        FROM mom_id_entity
        WHERE false
    MOM.Link2
        SELECT mom_id_entity.pid
        FROM mom_id_entity
        WHERE false
    MOM.Object
        SELECT mom_id_entity.pid
        FROM mom_id_entity
        WHERE false
    Auth.Id_Entity
        SELECT mom_id_entity.pid
        FROM mom_id_entity
        WHERE false
    Auth.Object
        SELECT mom_id_entity.pid
        FROM mom_id_entity
        WHERE false
    Auth._Account_
        SELECT auth__account_.pid
        FROM auth__account_
        WHERE false
    Auth.Account_Anonymous Auth._Account_
        SELECT auth__account_.enabled AS auth__account__enabled,
               auth__account_.name AS auth__account__name,
               auth__account_.pid AS auth__account__pid,
               auth__account_.superuser AS auth__account__superuser,
               auth__account_.suspended AS auth__account__suspended,
               auth_account_anonymous.pid AS auth_account_anonymous_pid,
               mom_id_entity.electric AS mom_id_entity_electric,
               mom_id_entity.last_cid AS mom_id_entity_last_cid,
               mom_id_entity.pid AS mom_id_entity_pid,
               mom_id_entity.type_name AS mom_id_entity_type_name,
               mom_id_entity.x_locked AS mom_id_entity_x_locked
        FROM mom_id_entity
           JOIN auth__account_ ON mom_id_entity.pid = auth__account_.pid
           JOIN auth_account_anonymous ON auth__account_.pid = auth_account_anonymous.pid
        WHERE mom_id_entity.type_name = :type_name_1
    Auth.Account Auth._Account_
        SELECT auth__account_.enabled AS auth__account__enabled,
               auth__account_.name AS auth__account__name,
               auth__account_.pid AS auth__account__pid,
               auth__account_.superuser AS auth__account__superuser,
               auth__account_.suspended AS auth__account__suspended,
               auth_account.password AS auth_account_password,
               auth_account.ph_name AS auth_account_ph_name,
               auth_account.pid AS auth_account_pid,
               mom_id_entity.electric AS mom_id_entity_electric,
               mom_id_entity.last_cid AS mom_id_entity_last_cid,
               mom_id_entity.pid AS mom_id_entity_pid,
               mom_id_entity.type_name AS mom_id_entity_type_name,
               mom_id_entity.x_locked AS mom_id_entity_x_locked
        FROM mom_id_entity
           JOIN auth__account_ ON mom_id_entity.pid = auth__account_.pid
           JOIN auth_account ON auth__account_.pid = auth_account.pid
        WHERE mom_id_entity.type_name = :type_name_1
    Auth.Certificate
        SELECT auth_certificate."desc" AS auth_certificate_desc,
               auth_certificate.cert_id AS auth_certificate_cert_id,
               auth_certificate.email AS auth_certificate_email,
               auth_certificate.pem AS auth_certificate_pem,
               auth_certificate.pid AS auth_certificate_pid,
               auth_certificate.revocation_date AS auth_certificate_revocation_date,
               auth_certificate.validity__finish AS auth_certificate_validity__finish,
               auth_certificate.validity__start AS auth_certificate_validity__start,
               mom_id_entity.electric AS mom_id_entity_electric,
               mom_id_entity.last_cid AS mom_id_entity_last_cid,
               mom_id_entity.pid AS mom_id_entity_pid,
               mom_id_entity.type_name AS mom_id_entity_type_name,
               mom_id_entity.x_locked AS mom_id_entity_x_locked
        FROM mom_id_entity
           JOIN auth_certificate ON mom_id_entity.pid = auth_certificate.pid
        WHERE mom_id_entity.type_name = :type_name_1
    Auth.Group
        SELECT auth_group."desc" AS auth_group_desc,
               auth_group.name AS auth_group_name,
               auth_group.pid AS auth_group_pid,
               mom_id_entity.electric AS mom_id_entity_electric,
               mom_id_entity.last_cid AS mom_id_entity_last_cid,
               mom_id_entity.pid AS mom_id_entity_pid,
               mom_id_entity.type_name AS mom_id_entity_type_name,
               mom_id_entity.x_locked AS mom_id_entity_x_locked
        FROM mom_id_entity
           JOIN auth_group ON mom_id_entity.pid = auth_group.pid
        WHERE mom_id_entity.type_name = :type_name_1
    Auth.Link
        SELECT mom_id_entity.pid
        FROM mom_id_entity
        WHERE false
    Auth._MOM_Link_n_
        SELECT mom_id_entity.pid
        FROM mom_id_entity
        WHERE false
    Auth.Link2
        SELECT mom_id_entity.pid
        FROM mom_id_entity
        WHERE false
    Auth.Account_in_Group
        SELECT auth_account_in_group."left" AS auth_account_in_group_left,
               auth_account_in_group."right" AS auth_account_in_group_right,
               auth_account_in_group.pid AS auth_account_in_group_pid,
               mom_id_entity.electric AS mom_id_entity_electric,
               mom_id_entity.last_cid AS mom_id_entity_last_cid,
               mom_id_entity.pid AS mom_id_entity_pid,
               mom_id_entity.type_name AS mom_id_entity_type_name,
               mom_id_entity.x_locked AS mom_id_entity_x_locked
        FROM mom_id_entity
           JOIN auth_account_in_group ON mom_id_entity.pid = auth_account_in_group.pid
        WHERE mom_id_entity.type_name = :type_name_1
    Auth.Link1
        SELECT mom_id_entity.pid
        FROM mom_id_entity
        WHERE false
    Auth._Account_Action_
        SELECT mom_id_entity.pid
        FROM mom_id_entity
        WHERE false
    Auth.Account_Activation
        SELECT auth_account_activation."left" AS auth_account_activation_left,
               auth_account_activation.pid AS auth_account_activation_pid,
               mom_id_entity.electric AS mom_id_entity_electric,
               mom_id_entity.last_cid AS mom_id_entity_last_cid,
               mom_id_entity.pid AS mom_id_entity_pid,
               mom_id_entity.type_name AS mom_id_entity_type_name,
               mom_id_entity.x_locked AS mom_id_entity_x_locked
        FROM mom_id_entity
           JOIN auth_account_activation ON mom_id_entity.pid = auth_account_activation.pid
        WHERE mom_id_entity.type_name = :type_name_1
    Auth.Account_Password_Change_Required
        SELECT auth_account_password_change_required."left" AS auth_account_password_change_required_left,
               auth_account_password_change_required.pid AS auth_account_password_change_required_pid,
               mom_id_entity.electric AS mom_id_entity_electric,
               mom_id_entity.last_cid AS mom_id_entity_last_cid,
               mom_id_entity.pid AS mom_id_entity_pid,
               mom_id_entity.type_name AS mom_id_entity_type_name,
               mom_id_entity.x_locked AS mom_id_entity_x_locked
        FROM mom_id_entity
           JOIN auth_account_password_change_required ON mom_id_entity.pid = auth_account_password_change_required.pid
        WHERE mom_id_entity.type_name = :type_name_1
    Auth._Account_Token_Action_
        SELECT mom_id_entity.pid
        FROM mom_id_entity
        WHERE false
    Auth.Account_EMail_Verification
        SELECT auth_account_email_verification."left" AS auth_account_email_verification_left,
               auth_account_email_verification.expires AS auth_account_email_verification_expires,
               auth_account_email_verification.new_email AS auth_account_email_verification_new_email,
               auth_account_email_verification.pid AS auth_account_email_verification_pid,
               auth_account_email_verification.token AS auth_account_email_verification_token,
               mom_id_entity.electric AS mom_id_entity_electric,
               mom_id_entity.last_cid AS mom_id_entity_last_cid,
               mom_id_entity.pid AS mom_id_entity_pid,
               mom_id_entity.type_name AS mom_id_entity_type_name,
               mom_id_entity.x_locked AS mom_id_entity_x_locked
        FROM mom_id_entity
           JOIN auth_account_email_verification ON mom_id_entity.pid = auth_account_email_verification.pid
        WHERE mom_id_entity.type_name = :type_name_1
    Auth.Account_Password_Reset
        SELECT auth_account_password_reset."left" AS auth_account_password_reset_left,
               auth_account_password_reset.expires AS auth_account_password_reset_expires,
               auth_account_password_reset.password AS auth_account_password_reset_password,
               auth_account_password_reset.pid AS auth_account_password_reset_pid,
               auth_account_password_reset.token AS auth_account_password_reset_token,
               mom_id_entity.electric AS mom_id_entity_electric,
               mom_id_entity.last_cid AS mom_id_entity_last_cid,
               mom_id_entity.pid AS mom_id_entity_pid,
               mom_id_entity.type_name AS mom_id_entity_type_name,
               mom_id_entity.x_locked AS mom_id_entity_x_locked
        FROM mom_id_entity
           JOIN auth_account_password_reset ON mom_id_entity.pid = auth_account_password_reset.pid
        WHERE mom_id_entity.type_name = :type_name_1
    EVT.Id_Entity
        SELECT mom_id_entity.pid
        FROM mom_id_entity
        WHERE false
    EVT.Object
        SELECT mom_id_entity.pid
        FROM mom_id_entity
        WHERE false
    EVT.Calendar
        SELECT evt_calendar."desc" AS evt_calendar_desc,
               evt_calendar.name AS evt_calendar_name,
               evt_calendar.pid AS evt_calendar_pid,
               mom_id_entity.electric AS mom_id_entity_electric,
               mom_id_entity.last_cid AS mom_id_entity_last_cid,
               mom_id_entity.pid AS mom_id_entity_pid,
               mom_id_entity.type_name AS mom_id_entity_type_name,
               mom_id_entity.x_locked AS mom_id_entity_x_locked
        FROM mom_id_entity
           JOIN evt_calendar ON mom_id_entity.pid = evt_calendar.pid
        WHERE mom_id_entity.type_name = :type_name_1
    EVT.Link
        SELECT mom_id_entity.pid
        FROM mom_id_entity
        WHERE false
    EVT.Link1
        SELECT mom_id_entity.pid
        FROM mom_id_entity
        WHERE false
    SWP.Id_Entity
        SELECT mom_id_entity.pid
        FROM mom_id_entity
        WHERE false
    SWP.Object
        SELECT mom_id_entity.pid
        FROM mom_id_entity
        WHERE false
    SWP.Object_PN
        SELECT mom_id_entity.pid
        FROM mom_id_entity
        WHERE false
    SWP.Page
        SELECT mom_id_entity.electric AS mom_id_entity_electric,
               mom_id_entity.last_cid AS mom_id_entity_last_cid,
               mom_id_entity.pid AS mom_id_entity_pid,
               mom_id_entity.type_name AS mom_id_entity_type_name,
               mom_id_entity.x_locked AS mom_id_entity_x_locked,
               swp_page.contents AS swp_page_contents,
               swp_page.date__finish AS swp_page_date__finish,
               swp_page.date__start AS swp_page_date__start,
               swp_page.format AS swp_page_format,
               swp_page.head_line AS swp_page_head_line,
               swp_page.hidden AS swp_page_hidden,
               swp_page.perma_name AS swp_page_perma_name,
               swp_page.pid AS swp_page_pid,
               swp_page.prio AS swp_page_prio,
               swp_page.short_title AS swp_page_short_title,
               swp_page.text AS swp_page_text,
               swp_page.title AS swp_page_title
        FROM mom_id_entity
           JOIN swp_page ON mom_id_entity.pid = swp_page.pid
        WHERE mom_id_entity.type_name = :type_name_1
    SWP.Page_Y SWP.Page
        SELECT mom_id_entity.electric AS mom_id_entity_electric,
               mom_id_entity.last_cid AS mom_id_entity_last_cid,
               mom_id_entity.pid AS mom_id_entity_pid,
               mom_id_entity.type_name AS mom_id_entity_type_name,
               mom_id_entity.x_locked AS mom_id_entity_x_locked,
               swp_page.contents AS swp_page_contents,
               swp_page.date__finish AS swp_page_date__finish,
               swp_page.date__start AS swp_page_date__start,
               swp_page.format AS swp_page_format,
               swp_page.head_line AS swp_page_head_line,
               swp_page.hidden AS swp_page_hidden,
               swp_page.perma_name AS swp_page_perma_name,
               swp_page.pid AS swp_page_pid,
               swp_page.prio AS swp_page_prio,
               swp_page.short_title AS swp_page_short_title,
               swp_page.text AS swp_page_text,
               swp_page.title AS swp_page_title,
               swp_page_y.pid AS swp_page_y_pid,
               swp_page_y.year AS swp_page_y_year
        FROM mom_id_entity
           JOIN swp_page ON mom_id_entity.pid = swp_page.pid
           JOIN swp_page_y ON swp_page.pid = swp_page_y.pid
        WHERE mom_id_entity.type_name = :type_name_1
    EVT.Event
        SELECT evt_event."left" AS evt_event_left,
               evt_event.calendar AS evt_event_calendar,
               evt_event.date__finish AS evt_event_date__finish,
               evt_event.date__start AS evt_event_date__start,
               evt_event.detail AS evt_event_detail,
               evt_event.pid AS evt_event_pid,
               evt_event.short_title AS evt_event_short_title,
               evt_event.time__finish AS evt_event_time__finish,
               evt_event.time__start AS evt_event_time__start,
               mom_id_entity.electric AS mom_id_entity_electric,
               mom_id_entity.last_cid AS mom_id_entity_last_cid,
               mom_id_entity.pid AS mom_id_entity_pid,
               mom_id_entity.type_name AS mom_id_entity_type_name,
               mom_id_entity.x_locked AS mom_id_entity_x_locked
        FROM mom_id_entity
           JOIN evt_event ON mom_id_entity.pid = evt_event.pid
        WHERE mom_id_entity.type_name = :type_name_1
    EVT.Event_occurs
        SELECT evt_event_occurs."left" AS evt_event_occurs_left,
               evt_event_occurs.date AS evt_event_occurs_date,
               evt_event_occurs.pid AS evt_event_occurs_pid,
               evt_event_occurs.time__finish AS evt_event_occurs_time__finish,
               evt_event_occurs.time__start AS evt_event_occurs_time__start,
               mom_id_entity.electric AS mom_id_entity_electric,
               mom_id_entity.last_cid AS mom_id_entity_last_cid,
               mom_id_entity.pid AS mom_id_entity_pid,
               mom_id_entity.type_name AS mom_id_entity_type_name,
               mom_id_entity.x_locked AS mom_id_entity_x_locked
        FROM mom_id_entity
           JOIN evt_event_occurs ON mom_id_entity.pid = evt_event_occurs.pid
        WHERE mom_id_entity.type_name = :type_name_1
    EVT._Recurrence_Mixin_
        SELECT mom_id_entity.pid
        FROM mom_id_entity
        WHERE false
    EVT.Recurrence_Spec
        SELECT evt_recurrence_spec."left" AS evt_recurrence_spec_left,
               evt_recurrence_spec.date_exceptions AS evt_recurrence_spec_date_exceptions,
               evt_recurrence_spec.dates AS evt_recurrence_spec_dates,
               evt_recurrence_spec.pid AS evt_recurrence_spec_pid,
               mom_id_entity.electric AS mom_id_entity_electric,
               mom_id_entity.last_cid AS mom_id_entity_last_cid,
               mom_id_entity.pid AS mom_id_entity_pid,
               mom_id_entity.type_name AS mom_id_entity_type_name,
               mom_id_entity.x_locked AS mom_id_entity_x_locked
        FROM mom_id_entity
           JOIN evt_recurrence_spec ON mom_id_entity.pid = evt_recurrence_spec.pid
        WHERE mom_id_entity.type_name = :type_name_1
    EVT.Recurrence_Rule
        SELECT evt_recurrence_rule."desc" AS evt_recurrence_rule_desc,
               evt_recurrence_rule."left" AS evt_recurrence_rule_left,
               evt_recurrence_rule.count AS evt_recurrence_rule_count,
               evt_recurrence_rule.easter_offset AS evt_recurrence_rule_easter_offset,
               evt_recurrence_rule.finish AS evt_recurrence_rule_finish,
               evt_recurrence_rule.is_exception AS evt_recurrence_rule_is_exception,
               evt_recurrence_rule.month AS evt_recurrence_rule_month,
               evt_recurrence_rule.month_day AS evt_recurrence_rule_month_day,
               evt_recurrence_rule.period AS evt_recurrence_rule_period,
               evt_recurrence_rule.pid AS evt_recurrence_rule_pid,
               evt_recurrence_rule.restrict_pos AS evt_recurrence_rule_restrict_pos,
               evt_recurrence_rule.start AS evt_recurrence_rule_start,
               evt_recurrence_rule.unit AS evt_recurrence_rule_unit,
               evt_recurrence_rule.week AS evt_recurrence_rule_week,
               evt_recurrence_rule.week_day AS evt_recurrence_rule_week_day,
               evt_recurrence_rule.year_day AS evt_recurrence_rule_year_day,
               mom_id_entity.electric AS mom_id_entity_electric,
               mom_id_entity.last_cid AS mom_id_entity_last_cid,
               mom_id_entity.pid AS mom_id_entity_pid,
               mom_id_entity.type_name AS mom_id_entity_type_name,
               mom_id_entity.x_locked AS mom_id_entity_x_locked
        FROM mom_id_entity
           JOIN evt_recurrence_rule ON mom_id_entity.pid = evt_recurrence_rule.pid
        WHERE mom_id_entity.type_name = :type_name_1
    PAP.Id_Entity
        SELECT mom_id_entity.pid
        FROM mom_id_entity
        WHERE false
    PAP.Object
        SELECT mom_id_entity.pid
        FROM mom_id_entity
        WHERE false
    PAP.Property
        SELECT mom_id_entity.pid
        FROM mom_id_entity
        WHERE false
    PAP.Address
        SELECT mom_id_entity.electric AS mom_id_entity_electric,
               mom_id_entity.last_cid AS mom_id_entity_last_cid,
               mom_id_entity.pid AS mom_id_entity_pid,
               mom_id_entity.type_name AS mom_id_entity_type_name,
               mom_id_entity.x_locked AS mom_id_entity_x_locked,
               pap_address."desc" AS pap_address_desc,
               pap_address.__raw_city AS pap_address___raw_city,
               pap_address.__raw_country AS pap_address___raw_country,
               pap_address.__raw_region AS pap_address___raw_region,
               pap_address.__raw_street AS pap_address___raw_street,
               pap_address.__raw_zip AS pap_address___raw_zip,
               pap_address.city AS pap_address_city,
               pap_address.country AS pap_address_country,
               pap_address.pid AS pap_address_pid,
               pap_address.region AS pap_address_region,
               pap_address.street AS pap_address_street,
               pap_address.zip AS pap_address_zip
        FROM mom_id_entity
           JOIN pap_address ON mom_id_entity.pid = pap_address.pid
        WHERE mom_id_entity.type_name = :type_name_1
    PAP.Subject
        SELECT mom_id_entity.pid
        FROM mom_id_entity
        WHERE false
    PAP.Legal_Entity
        SELECT mom_id_entity.pid
        FROM mom_id_entity
        WHERE false
    PAP.Company
        SELECT mom_id_entity.electric AS mom_id_entity_electric,
               mom_id_entity.last_cid AS mom_id_entity_last_cid,
               mom_id_entity.pid AS mom_id_entity_pid,
               mom_id_entity.type_name AS mom_id_entity_type_name,
               mom_id_entity.x_locked AS mom_id_entity_x_locked,
               pap_company.__raw_name AS pap_company___raw_name,
               pap_company.__raw_registered_in AS pap_company___raw_registered_in,
               pap_company.__raw_short_name AS pap_company___raw_short_name,
               pap_company.lifetime__finish AS pap_company_lifetime__finish,
               pap_company.lifetime__start AS pap_company_lifetime__start,
               pap_company.name AS pap_company_name,
               pap_company.pid AS pap_company_pid,
               pap_company.registered_in AS pap_company_registered_in,
               pap_company.short_name AS pap_company_short_name
        FROM mom_id_entity
           JOIN pap_company ON mom_id_entity.pid = pap_company.pid
        WHERE mom_id_entity.type_name = :type_name_1
    PAP.Email
        SELECT mom_id_entity.electric AS mom_id_entity_electric,
               mom_id_entity.last_cid AS mom_id_entity_last_cid,
               mom_id_entity.pid AS mom_id_entity_pid,
               mom_id_entity.type_name AS mom_id_entity_type_name,
               mom_id_entity.x_locked AS mom_id_entity_x_locked,
               pap_email."desc" AS pap_email_desc,
               pap_email.__raw_address AS pap_email___raw_address,
               pap_email.address AS pap_email_address,
               pap_email.pid AS pap_email_pid
        FROM mom_id_entity
           JOIN pap_email ON mom_id_entity.pid = pap_email.pid
        WHERE mom_id_entity.type_name = :type_name_1
    PAP.Phone
        SELECT mom_id_entity.electric AS mom_id_entity_electric,
               mom_id_entity.last_cid AS mom_id_entity_last_cid,
               mom_id_entity.pid AS mom_id_entity_pid,
               mom_id_entity.type_name AS mom_id_entity_type_name,
               mom_id_entity.x_locked AS mom_id_entity_x_locked,
               pap_phone."desc" AS pap_phone_desc,
               pap_phone.area_code AS pap_phone_area_code,
               pap_phone.country_code AS pap_phone_country_code,
               pap_phone.number AS pap_phone_number,
               pap_phone.pid AS pap_phone_pid
        FROM mom_id_entity
           JOIN pap_phone ON mom_id_entity.pid = pap_phone.pid
        WHERE mom_id_entity.type_name = :type_name_1
    PAP.Person
        SELECT mom_id_entity.electric AS mom_id_entity_electric,
               mom_id_entity.last_cid AS mom_id_entity_last_cid,
               mom_id_entity.pid AS mom_id_entity_pid,
               mom_id_entity.type_name AS mom_id_entity_type_name,
               mom_id_entity.x_locked AS mom_id_entity_x_locked,
               pap_person.__raw_first_name AS pap_person___raw_first_name,
               pap_person.__raw_last_name AS pap_person___raw_last_name,
               pap_person.__raw_middle_name AS pap_person___raw_middle_name,
               pap_person.__raw_title AS pap_person___raw_title,
               pap_person.first_name AS pap_person_first_name,
               pap_person.last_name AS pap_person_last_name,
               pap_person.lifetime__finish AS pap_person_lifetime__finish,
               pap_person.lifetime__start AS pap_person_lifetime__start,
               pap_person.middle_name AS pap_person_middle_name,
               pap_person.pid AS pap_person_pid,
               pap_person.sex AS pap_person_sex,
               pap_person.title AS pap_person_title
        FROM mom_id_entity
           JOIN pap_person ON mom_id_entity.pid = pap_person.pid
        WHERE mom_id_entity.type_name = :type_name_1
    PAP.Url
        SELECT mom_id_entity.electric AS mom_id_entity_electric,
               mom_id_entity.last_cid AS mom_id_entity_last_cid,
               mom_id_entity.pid AS mom_id_entity_pid,
               mom_id_entity.type_name AS mom_id_entity_type_name,
               mom_id_entity.x_locked AS mom_id_entity_x_locked,
               pap_url."desc" AS pap_url_desc,
               pap_url.pid AS pap_url_pid,
               pap_url.value AS pap_url_value
        FROM mom_id_entity
           JOIN pap_url ON mom_id_entity.pid = pap_url.pid
        WHERE mom_id_entity.type_name = :type_name_1
    PAP.Link
        SELECT mom_id_entity.pid
        FROM mom_id_entity
        WHERE false
    PAP.Link1
        SELECT mom_id_entity.pid
        FROM mom_id_entity
        WHERE false
    PAP.Address_Position
        SELECT mom_id_entity.electric AS mom_id_entity_electric,
               mom_id_entity.last_cid AS mom_id_entity_last_cid,
               mom_id_entity.pid AS mom_id_entity_pid,
               mom_id_entity.type_name AS mom_id_entity_type_name,
               mom_id_entity.x_locked AS mom_id_entity_x_locked,
               pap_address_position."left" AS pap_address_position_left,
               pap_address_position.pid AS pap_address_position_pid,
               pap_address_position.position____raw_lat AS pap_address_position_position____raw_lat,
               pap_address_position.position____raw_lon AS pap_address_position_position____raw_lon,
               pap_address_position.position__height AS pap_address_position_position__height,
               pap_address_position.position__lat AS pap_address_position_position__lat,
               pap_address_position.position__lon AS pap_address_position_position__lon
        FROM mom_id_entity
           JOIN pap_address_position ON mom_id_entity.pid = pap_address_position.pid
        WHERE mom_id_entity.type_name = :type_name_1
    PAP._MOM_Link_n_
        SELECT mom_id_entity.pid
        FROM mom_id_entity
        WHERE false
    PAP.Link2
        SELECT mom_id_entity.pid
        FROM mom_id_entity
        WHERE false
    PAP.Subject_has_Property
        SELECT pap_subject_has_property.pid
        FROM pap_subject_has_property
        WHERE false
    PAP.Person_has_Account
        SELECT mom_id_entity.electric AS mom_id_entity_electric,
               mom_id_entity.last_cid AS mom_id_entity_last_cid,
               mom_id_entity.pid AS mom_id_entity_pid,
               mom_id_entity.type_name AS mom_id_entity_type_name,
               mom_id_entity.x_locked AS mom_id_entity_x_locked,
               pap_person_has_account."left" AS pap_person_has_account_left,
               pap_person_has_account."right" AS pap_person_has_account_right,
               pap_person_has_account.pid AS pap_person_has_account_pid
        FROM mom_id_entity
           JOIN pap_person_has_account ON mom_id_entity.pid = pap_person_has_account.pid
        WHERE mom_id_entity.type_name = :type_name_1
    SRM.Id_Entity
        SELECT mom_id_entity.pid
        FROM mom_id_entity
        WHERE false
    SRM.Object
        SELECT mom_id_entity.pid
        FROM mom_id_entity
        WHERE false
    SRM._Boat_Class_
        SELECT srm__boat_class_.pid
        FROM srm__boat_class_
        WHERE false
    SRM.Boat_Class SRM._Boat_Class_
        SELECT mom_id_entity.electric AS mom_id_entity_electric,
               mom_id_entity.last_cid AS mom_id_entity_last_cid,
               mom_id_entity.pid AS mom_id_entity_pid,
               mom_id_entity.type_name AS mom_id_entity_type_name,
               mom_id_entity.x_locked AS mom_id_entity_x_locked,
               srm__boat_class_.__raw_name AS srm__boat_class____raw_name,
               srm__boat_class_.name AS srm__boat_class__name,
               srm__boat_class_.pid AS srm__boat_class__pid,
               srm_boat_class.beam AS srm_boat_class_beam,
               srm_boat_class.loa AS srm_boat_class_loa,
               srm_boat_class.max_crew AS srm_boat_class_max_crew,
               srm_boat_class.pid AS srm_boat_class_pid,
               srm_boat_class.sail_area AS srm_boat_class_sail_area
        FROM mom_id_entity
           JOIN srm__boat_class_ ON mom_id_entity.pid = srm__boat_class_.pid
           JOIN srm_boat_class ON srm__boat_class_.pid = srm_boat_class.pid
        WHERE mom_id_entity.type_name = :type_name_1
    SRM.Handicap SRM._Boat_Class_
        SELECT mom_id_entity.electric AS mom_id_entity_electric,
               mom_id_entity.last_cid AS mom_id_entity_last_cid,
               mom_id_entity.pid AS mom_id_entity_pid,
               mom_id_entity.type_name AS mom_id_entity_type_name,
               mom_id_entity.x_locked AS mom_id_entity_x_locked,
               srm__boat_class_.__raw_name AS srm__boat_class____raw_name,
               srm__boat_class_.name AS srm__boat_class__name,
               srm__boat_class_.pid AS srm__boat_class__pid,
               srm_handicap.pid AS srm_handicap_pid
        FROM mom_id_entity
           JOIN srm__boat_class_ ON mom_id_entity.pid = srm__boat_class_.pid
           JOIN srm_handicap ON srm__boat_class_.pid = srm_handicap.pid
        WHERE mom_id_entity.type_name = :type_name_1
    SRM.Link
        SELECT mom_id_entity.pid
        FROM mom_id_entity
        WHERE false
    SRM.Link1
        SELECT mom_id_entity.pid
        FROM mom_id_entity
        WHERE false
    SRM.Boat
        SELECT mom_id_entity.electric AS mom_id_entity_electric,
               mom_id_entity.last_cid AS mom_id_entity_last_cid,
               mom_id_entity.pid AS mom_id_entity_pid,
               mom_id_entity.type_name AS mom_id_entity_type_name,
               mom_id_entity.x_locked AS mom_id_entity_x_locked,
               srm_boat."left" AS srm_boat_left,
               srm_boat.__raw_sail_number AS srm_boat___raw_sail_number,
               srm_boat.__raw_sail_number_x AS srm_boat___raw_sail_number_x,
               srm_boat.name AS srm_boat_name,
               srm_boat.nation AS srm_boat_nation,
               srm_boat.pid AS srm_boat_pid,
               srm_boat.sail_number AS srm_boat_sail_number,
               srm_boat.sail_number_x AS srm_boat_sail_number_x
        FROM mom_id_entity
           JOIN srm_boat ON mom_id_entity.pid = srm_boat.pid
        WHERE mom_id_entity.type_name = :type_name_1
    SRM.Club
        SELECT mom_id_entity.electric AS mom_id_entity_electric,
               mom_id_entity.last_cid AS mom_id_entity_last_cid,
               mom_id_entity.pid AS mom_id_entity_pid,
               mom_id_entity.type_name AS mom_id_entity_type_name,
               mom_id_entity.x_locked AS mom_id_entity_x_locked,
               srm_club.__raw_name AS srm_club___raw_name,
               srm_club.long_name AS srm_club_long_name,
               srm_club.name AS srm_club_name,
               srm_club.pid AS srm_club_pid
        FROM mom_id_entity
           JOIN srm_club ON mom_id_entity.pid = srm_club.pid
        WHERE mom_id_entity.type_name = :type_name_1
    SRM.Regatta_Event
        SELECT mom_id_entity.electric AS mom_id_entity_electric,
               mom_id_entity.last_cid AS mom_id_entity_last_cid,
               mom_id_entity.pid AS mom_id_entity_pid,
               mom_id_entity.type_name AS mom_id_entity_type_name,
               mom_id_entity.x_locked AS mom_id_entity_x_locked,
               srm_regatta_event."desc" AS srm_regatta_event_desc,
               srm_regatta_event.__raw_name AS srm_regatta_event___raw_name,
               srm_regatta_event.club AS srm_regatta_event_club,
               srm_regatta_event.date__finish AS srm_regatta_event_date__finish,
               srm_regatta_event.date__start AS srm_regatta_event_date__start,
               srm_regatta_event.is_cancelled AS srm_regatta_event_is_cancelled,
               srm_regatta_event.name AS srm_regatta_event_name,
               srm_regatta_event.perma_name AS srm_regatta_event_perma_name,
               srm_regatta_event.pid AS srm_regatta_event_pid
        FROM mom_id_entity
           JOIN srm_regatta_event ON mom_id_entity.pid = srm_regatta_event.pid
        WHERE mom_id_entity.type_name = :type_name_1
    SWP.Link
        SELECT mom_id_entity.pid
        FROM mom_id_entity
        WHERE false
    SWP.Link1
        SELECT mom_id_entity.pid
        FROM mom_id_entity
        WHERE false
    SWP.Clip_O
        SELECT mom_id_entity.electric AS mom_id_entity_electric,
               mom_id_entity.last_cid AS mom_id_entity_last_cid,
               mom_id_entity.pid AS mom_id_entity_pid,
               mom_id_entity.type_name AS mom_id_entity_type_name,
               mom_id_entity.x_locked AS mom_id_entity_x_locked,
               swp_clip_o."left" AS swp_clip_o_left,
               swp_clip_o.abstract AS swp_clip_o_abstract,
               swp_clip_o.contents AS swp_clip_o_contents,
               swp_clip_o.date__finish AS swp_clip_o_date__finish,
               swp_clip_o.date__start AS swp_clip_o_date__start,
               swp_clip_o.date_x__finish AS swp_clip_o_date_x__finish,
               swp_clip_o.date_x__start AS swp_clip_o_date_x__start,
               swp_clip_o.pid AS swp_clip_o_pid,
               swp_clip_o.prio AS swp_clip_o_prio
        FROM mom_id_entity
           JOIN swp_clip_o ON mom_id_entity.pid = swp_clip_o.pid
        WHERE mom_id_entity.type_name = :type_name_1
    SWP.Clip_X SWP.Page
        SELECT mom_id_entity.electric AS mom_id_entity_electric,
               mom_id_entity.last_cid AS mom_id_entity_last_cid,
               mom_id_entity.pid AS mom_id_entity_pid,
               mom_id_entity.type_name AS mom_id_entity_type_name,
               mom_id_entity.x_locked AS mom_id_entity_x_locked,
               swp_clip_x.link_to AS swp_clip_x_link_to,
               swp_clip_x.pid AS swp_clip_x_pid,
               swp_page.contents AS swp_page_contents,
               swp_page.date__finish AS swp_page_date__finish,
               swp_page.date__start AS swp_page_date__start,
               swp_page.format AS swp_page_format,
               swp_page.head_line AS swp_page_head_line,
               swp_page.hidden AS swp_page_hidden,
               swp_page.perma_name AS swp_page_perma_name,
               swp_page.pid AS swp_page_pid,
               swp_page.prio AS swp_page_prio,
               swp_page.short_title AS swp_page_short_title,
               swp_page.text AS swp_page_text,
               swp_page.title AS swp_page_title
        FROM mom_id_entity
           JOIN swp_page ON mom_id_entity.pid = swp_page.pid
           JOIN swp_clip_x ON swp_page.pid = swp_clip_x.pid
        WHERE mom_id_entity.type_name = :type_name_1
    SWP.Gallery
        SELECT mom_id_entity.electric AS mom_id_entity_electric,
               mom_id_entity.last_cid AS mom_id_entity_last_cid,
               mom_id_entity.pid AS mom_id_entity_pid,
               mom_id_entity.type_name AS mom_id_entity_type_name,
               mom_id_entity.x_locked AS mom_id_entity_x_locked,
               swp_gallery.date__finish AS swp_gallery_date__finish,
               swp_gallery.date__start AS swp_gallery_date__start,
               swp_gallery.directory AS swp_gallery_directory,
               swp_gallery.perma_name AS swp_gallery_perma_name,
               swp_gallery.pid AS swp_gallery_pid,
               swp_gallery.short_title AS swp_gallery_short_title,
               swp_gallery.title AS swp_gallery_title
        FROM mom_id_entity
           JOIN swp_gallery ON mom_id_entity.pid = swp_gallery.pid
        WHERE mom_id_entity.type_name = :type_name_1
    SWP.Picture
        SELECT mom_id_entity.electric AS mom_id_entity_electric,
               mom_id_entity.last_cid AS mom_id_entity_last_cid,
               mom_id_entity.pid AS mom_id_entity_pid,
               mom_id_entity.type_name AS mom_id_entity_type_name,
               mom_id_entity.x_locked AS mom_id_entity_x_locked,
               swp_picture."left" AS swp_picture_left,
               swp_picture.name AS swp_picture_name,
               swp_picture.number AS swp_picture_number,
               swp_picture.photo__extension AS swp_picture_photo__extension,
               swp_picture.photo__height AS swp_picture_photo__height,
               swp_picture.photo__width AS swp_picture_photo__width,
               swp_picture.pid AS swp_picture_pid,
               swp_picture.thumb__extension AS swp_picture_thumb__extension,
               swp_picture.thumb__height AS swp_picture_thumb__height,
               swp_picture.thumb__width AS swp_picture_thumb__width
        FROM mom_id_entity
           JOIN swp_picture ON mom_id_entity.pid = swp_picture.pid
        WHERE mom_id_entity.type_name = :type_name_1
    SRM.Page SWP.Page
        SELECT mom_id_entity.electric AS mom_id_entity_electric,
               mom_id_entity.last_cid AS mom_id_entity_last_cid,
               mom_id_entity.pid AS mom_id_entity_pid,
               mom_id_entity.type_name AS mom_id_entity_type_name,
               mom_id_entity.x_locked AS mom_id_entity_x_locked,
               srm_page."desc" AS srm_page_desc,
               srm_page.event AS srm_page_event,
               srm_page.pid AS srm_page_pid,
               swp_page.contents AS swp_page_contents,
               swp_page.date__finish AS swp_page_date__finish,
               swp_page.date__start AS swp_page_date__start,
               swp_page.format AS swp_page_format,
               swp_page.head_line AS swp_page_head_line,
               swp_page.hidden AS swp_page_hidden,
               swp_page.perma_name AS swp_page_perma_name,
               swp_page.pid AS swp_page_pid,
               swp_page.prio AS swp_page_prio,
               swp_page.short_title AS swp_page_short_title,
               swp_page.text AS swp_page_text,
               swp_page.title AS swp_page_title
        FROM mom_id_entity
           JOIN swp_page ON mom_id_entity.pid = swp_page.pid
           JOIN srm_page ON swp_page.pid = srm_page.pid
        WHERE mom_id_entity.type_name = :type_name_1
    SRM.Regatta
        SELECT srm_regatta.pid
        FROM srm_regatta
        WHERE false
    SRM.Regatta_C SRM.Regatta
        SELECT mom_id_entity.electric AS mom_id_entity_electric,
               mom_id_entity.last_cid AS mom_id_entity_last_cid,
               mom_id_entity.pid AS mom_id_entity_pid,
               mom_id_entity.type_name AS mom_id_entity_type_name,
               mom_id_entity.x_locked AS mom_id_entity_x_locked,
               srm_regatta."left" AS srm_regatta_left,
               srm_regatta.boat_class AS srm_regatta_boat_class,
               srm_regatta.discards AS srm_regatta_discards,
               srm_regatta.is_cancelled AS srm_regatta_is_cancelled,
               srm_regatta.kind AS srm_regatta_kind,
               srm_regatta.perma_name AS srm_regatta_perma_name,
               srm_regatta.pid AS srm_regatta_pid,
               srm_regatta.races AS srm_regatta_races,
               srm_regatta.result__date AS srm_regatta_result__date,
               srm_regatta.result__software AS srm_regatta_result__software,
               srm_regatta.result__status AS srm_regatta_result__status,
               srm_regatta_c.is_team_race AS srm_regatta_c_is_team_race,
               srm_regatta_c.pid AS srm_regatta_c_pid
        FROM mom_id_entity
           JOIN srm_regatta ON mom_id_entity.pid = srm_regatta.pid
           JOIN srm_regatta_c ON srm_regatta.pid = srm_regatta_c.pid
        WHERE mom_id_entity.type_name = :type_name_1
    SRM.Regatta_H SRM.Regatta
        SELECT mom_id_entity.electric AS mom_id_entity_electric,
               mom_id_entity.last_cid AS mom_id_entity_last_cid,
               mom_id_entity.pid AS mom_id_entity_pid,
               mom_id_entity.type_name AS mom_id_entity_type_name,
               mom_id_entity.x_locked AS mom_id_entity_x_locked,
               srm_regatta."left" AS srm_regatta_left,
               srm_regatta.boat_class AS srm_regatta_boat_class,
               srm_regatta.discards AS srm_regatta_discards,
               srm_regatta.is_cancelled AS srm_regatta_is_cancelled,
               srm_regatta.kind AS srm_regatta_kind,
               srm_regatta.perma_name AS srm_regatta_perma_name,
               srm_regatta.pid AS srm_regatta_pid,
               srm_regatta.races AS srm_regatta_races,
               srm_regatta.result__date AS srm_regatta_result__date,
               srm_regatta.result__software AS srm_regatta_result__software,
               srm_regatta.result__status AS srm_regatta_result__status,
               srm_regatta_h.pid AS srm_regatta_h_pid
        FROM mom_id_entity
           JOIN srm_regatta ON mom_id_entity.pid = srm_regatta.pid
           JOIN srm_regatta_h ON srm_regatta.pid = srm_regatta_h.pid
        WHERE mom_id_entity.type_name = :type_name_1
    SRM.Sailor
        SELECT mom_id_entity.electric AS mom_id_entity_electric,
               mom_id_entity.last_cid AS mom_id_entity_last_cid,
               mom_id_entity.pid AS mom_id_entity_pid,
               mom_id_entity.type_name AS mom_id_entity_type_name,
               mom_id_entity.x_locked AS mom_id_entity_x_locked,
               srm_sailor."left" AS srm_sailor_left,
               srm_sailor.__raw_mna_number AS srm_sailor___raw_mna_number,
               srm_sailor.club AS srm_sailor_club,
               srm_sailor.mna_number AS srm_sailor_mna_number,
               srm_sailor.nation AS srm_sailor_nation,
               srm_sailor.pid AS srm_sailor_pid
        FROM mom_id_entity
           JOIN srm_sailor ON mom_id_entity.pid = srm_sailor.pid
        WHERE mom_id_entity.type_name = :type_name_1
    SRM._MOM_Link_n_
        SELECT mom_id_entity.pid
        FROM mom_id_entity
        WHERE false
    SRM.Link2
        SELECT mom_id_entity.pid
        FROM mom_id_entity
        WHERE false
    SRM.Boat_in_Regatta
        SELECT mom_id_entity.electric AS mom_id_entity_electric,
               mom_id_entity.last_cid AS mom_id_entity_last_cid,
               mom_id_entity.pid AS mom_id_entity_pid,
               mom_id_entity.type_name AS mom_id_entity_type_name,
               mom_id_entity.x_locked AS mom_id_entity_x_locked,
               srm_boat_in_regatta."left" AS srm_boat_in_regatta_left,
               srm_boat_in_regatta."right" AS srm_boat_in_regatta_right,
               srm_boat_in_regatta.pid AS srm_boat_in_regatta_pid,
               srm_boat_in_regatta.place AS srm_boat_in_regatta_place,
               srm_boat_in_regatta.points AS srm_boat_in_regatta_points,
               srm_boat_in_regatta.rank AS srm_boat_in_regatta_rank,
               srm_boat_in_regatta.registration_date AS srm_boat_in_regatta_registration_date,
               srm_boat_in_regatta.skipper AS srm_boat_in_regatta_skipper
        FROM mom_id_entity
           JOIN srm_boat_in_regatta ON mom_id_entity.pid = srm_boat_in_regatta.pid
        WHERE mom_id_entity.type_name = :type_name_1
    SRM.Race_Result
        SELECT mom_id_entity.electric AS mom_id_entity_electric,
               mom_id_entity.last_cid AS mom_id_entity_last_cid,
               mom_id_entity.pid AS mom_id_entity_pid,
               mom_id_entity.type_name AS mom_id_entity_type_name,
               mom_id_entity.x_locked AS mom_id_entity_x_locked,
               srm_race_result."left" AS srm_race_result_left,
               srm_race_result.discarded AS srm_race_result_discarded,
               srm_race_result.pid AS srm_race_result_pid,
               srm_race_result.points AS srm_race_result_points,
               srm_race_result.race AS srm_race_result_race,
               srm_race_result.status AS srm_race_result_status
        FROM mom_id_entity
           JOIN srm_race_result ON mom_id_entity.pid = srm_race_result.pid
        WHERE mom_id_entity.type_name = :type_name_1
    SRM.Team
        SELECT mom_id_entity.electric AS mom_id_entity_electric,
               mom_id_entity.last_cid AS mom_id_entity_last_cid,
               mom_id_entity.pid AS mom_id_entity_pid,
               mom_id_entity.type_name AS mom_id_entity_type_name,
               mom_id_entity.x_locked AS mom_id_entity_x_locked,
               srm_team."desc" AS srm_team_desc,
               srm_team."left" AS srm_team_left,
               srm_team.__raw_name AS srm_team___raw_name,
               srm_team.club AS srm_team_club,
               srm_team.leader AS srm_team_leader,
               srm_team.name AS srm_team_name,
               srm_team.pid AS srm_team_pid,
               srm_team.place AS srm_team_place,
               srm_team.registration_date AS srm_team_registration_date
        FROM mom_id_entity
           JOIN srm_team ON mom_id_entity.pid = srm_team.pid
        WHERE mom_id_entity.type_name = :type_name_1
    SRM.Crew_Member
        SELECT mom_id_entity.electric AS mom_id_entity_electric,
               mom_id_entity.last_cid AS mom_id_entity_last_cid,
               mom_id_entity.pid AS mom_id_entity_pid,
               mom_id_entity.type_name AS mom_id_entity_type_name,
               mom_id_entity.x_locked AS mom_id_entity_x_locked,
               srm_crew_member."left" AS srm_crew_member_left,
               srm_crew_member."right" AS srm_crew_member_right,
               srm_crew_member.key AS srm_crew_member_key,
               srm_crew_member.pid AS srm_crew_member_pid,
               srm_crew_member.role AS srm_crew_member_role
        FROM mom_id_entity
           JOIN srm_crew_member ON mom_id_entity.pid = srm_crew_member.pid
        WHERE mom_id_entity.type_name = :type_name_1
    SRM.Team_has_Boat_in_Regatta
        SELECT mom_id_entity.electric AS mom_id_entity_electric,
               mom_id_entity.last_cid AS mom_id_entity_last_cid,
               mom_id_entity.pid AS mom_id_entity_pid,
               mom_id_entity.type_name AS mom_id_entity_type_name,
               mom_id_entity.x_locked AS mom_id_entity_x_locked,
               srm_team_has_boat_in_regatta."left" AS srm_team_has_boat_in_regatta_left,
               srm_team_has_boat_in_regatta."right" AS srm_team_has_boat_in_regatta_right,
               srm_team_has_boat_in_regatta.pid AS srm_team_has_boat_in_regatta_pid
        FROM mom_id_entity
           JOIN srm_team_has_boat_in_regatta ON mom_id_entity.pid = srm_team_has_boat_in_regatta.pid
        WHERE mom_id_entity.type_name = :type_name_1
    PAP.Subject_has_Address PAP.Subject_has_Property
        SELECT pap_subject_has_property.pid
        FROM pap_subject_has_property
        WHERE false
    PAP.Subject_has_Email PAP.Subject_has_Property
        SELECT pap_subject_has_property.pid
        FROM pap_subject_has_property
        WHERE false
    PAP.Subject_has_Phone PAP.Subject_has_Property
        SELECT pap_subject_has_phone.pid
        FROM pap_subject_has_phone
        WHERE false
    PAP.Subject_has_Url PAP.Subject_has_Property
        SELECT pap_subject_has_property.pid
        FROM pap_subject_has_property
        WHERE false
    PAP.Company_has_Url PAP.Subject_has_Property
        SELECT mom_id_entity.electric AS mom_id_entity_electric,
               mom_id_entity.last_cid AS mom_id_entity_last_cid,
               mom_id_entity.pid AS mom_id_entity_pid,
               mom_id_entity.type_name AS mom_id_entity_type_name,
               mom_id_entity.x_locked AS mom_id_entity_x_locked,
               pap_company_has_url.pid AS pap_company_has_url_pid,
               pap_subject_has_property."desc" AS pap_subject_has_property_desc,
               pap_subject_has_property."left" AS pap_subject_has_property_left,
               pap_subject_has_property."right" AS pap_subject_has_property_right,
               pap_subject_has_property.pid AS pap_subject_has_property_pid
        FROM mom_id_entity
           JOIN pap_subject_has_property ON mom_id_entity.pid = pap_subject_has_property.pid
           JOIN pap_company_has_url ON pap_subject_has_property.pid = pap_company_has_url.pid
        WHERE mom_id_entity.type_name = :type_name_1
    PAP.Person_has_Url PAP.Subject_has_Property
        SELECT mom_id_entity.electric AS mom_id_entity_electric,
               mom_id_entity.last_cid AS mom_id_entity_last_cid,
               mom_id_entity.pid AS mom_id_entity_pid,
               mom_id_entity.type_name AS mom_id_entity_type_name,
               mom_id_entity.x_locked AS mom_id_entity_x_locked,
               pap_person_has_url.pid AS pap_person_has_url_pid,
               pap_subject_has_property."desc" AS pap_subject_has_property_desc,
               pap_subject_has_property."left" AS pap_subject_has_property_left,
               pap_subject_has_property."right" AS pap_subject_has_property_right,
               pap_subject_has_property.pid AS pap_subject_has_property_pid
        FROM mom_id_entity
           JOIN pap_subject_has_property ON mom_id_entity.pid = pap_subject_has_property.pid
           JOIN pap_person_has_url ON pap_subject_has_property.pid = pap_person_has_url.pid
        WHERE mom_id_entity.type_name = :type_name_1
    PAP.Company_has_Phone PAP.Subject_has_Property
        SELECT mom_id_entity.electric AS mom_id_entity_electric,
               mom_id_entity.last_cid AS mom_id_entity_last_cid,
               mom_id_entity.pid AS mom_id_entity_pid,
               mom_id_entity.type_name AS mom_id_entity_type_name,
               mom_id_entity.x_locked AS mom_id_entity_x_locked,
               pap_company_has_phone.pid AS pap_company_has_phone_pid,
               pap_subject_has_phone.extension AS pap_subject_has_phone_extension,
               pap_subject_has_phone.pid AS pap_subject_has_phone_pid,
               pap_subject_has_property."desc" AS pap_subject_has_property_desc,
               pap_subject_has_property."left" AS pap_subject_has_property_left,
               pap_subject_has_property."right" AS pap_subject_has_property_right,
               pap_subject_has_property.pid AS pap_subject_has_property_pid
        FROM mom_id_entity
           JOIN pap_subject_has_property ON mom_id_entity.pid = pap_subject_has_property.pid
           JOIN pap_subject_has_phone ON pap_subject_has_property.pid = pap_subject_has_phone.pid
           JOIN pap_company_has_phone ON pap_subject_has_phone.pid = pap_company_has_phone.pid
        WHERE mom_id_entity.type_name = :type_name_1
    PAP.Person_has_Phone PAP.Subject_has_Property
        SELECT mom_id_entity.electric AS mom_id_entity_electric,
               mom_id_entity.last_cid AS mom_id_entity_last_cid,
               mom_id_entity.pid AS mom_id_entity_pid,
               mom_id_entity.type_name AS mom_id_entity_type_name,
               mom_id_entity.x_locked AS mom_id_entity_x_locked,
               pap_person_has_phone.pid AS pap_person_has_phone_pid,
               pap_subject_has_phone.extension AS pap_subject_has_phone_extension,
               pap_subject_has_phone.pid AS pap_subject_has_phone_pid,
               pap_subject_has_property."desc" AS pap_subject_has_property_desc,
               pap_subject_has_property."left" AS pap_subject_has_property_left,
               pap_subject_has_property."right" AS pap_subject_has_property_right,
               pap_subject_has_property.pid AS pap_subject_has_property_pid
        FROM mom_id_entity
           JOIN pap_subject_has_property ON mom_id_entity.pid = pap_subject_has_property.pid
           JOIN pap_subject_has_phone ON pap_subject_has_property.pid = pap_subject_has_phone.pid
           JOIN pap_person_has_phone ON pap_subject_has_phone.pid = pap_person_has_phone.pid
        WHERE mom_id_entity.type_name = :type_name_1
    PAP.Company_has_Email PAP.Subject_has_Property
        SELECT mom_id_entity.electric AS mom_id_entity_electric,
               mom_id_entity.last_cid AS mom_id_entity_last_cid,
               mom_id_entity.pid AS mom_id_entity_pid,
               mom_id_entity.type_name AS mom_id_entity_type_name,
               mom_id_entity.x_locked AS mom_id_entity_x_locked,
               pap_company_has_email.pid AS pap_company_has_email_pid,
               pap_subject_has_property."desc" AS pap_subject_has_property_desc,
               pap_subject_has_property."left" AS pap_subject_has_property_left,
               pap_subject_has_property."right" AS pap_subject_has_property_right,
               pap_subject_has_property.pid AS pap_subject_has_property_pid
        FROM mom_id_entity
           JOIN pap_subject_has_property ON mom_id_entity.pid = pap_subject_has_property.pid
           JOIN pap_company_has_email ON pap_subject_has_property.pid = pap_company_has_email.pid
        WHERE mom_id_entity.type_name = :type_name_1
    PAP.Person_has_Email PAP.Subject_has_Property
        SELECT mom_id_entity.electric AS mom_id_entity_electric,
               mom_id_entity.last_cid AS mom_id_entity_last_cid,
               mom_id_entity.pid AS mom_id_entity_pid,
               mom_id_entity.type_name AS mom_id_entity_type_name,
               mom_id_entity.x_locked AS mom_id_entity_x_locked,
               pap_person_has_email.pid AS pap_person_has_email_pid,
               pap_subject_has_property."desc" AS pap_subject_has_property_desc,
               pap_subject_has_property."left" AS pap_subject_has_property_left,
               pap_subject_has_property."right" AS pap_subject_has_property_right,
               pap_subject_has_property.pid AS pap_subject_has_property_pid
        FROM mom_id_entity
           JOIN pap_subject_has_property ON mom_id_entity.pid = pap_subject_has_property.pid
           JOIN pap_person_has_email ON pap_subject_has_property.pid = pap_person_has_email.pid
        WHERE mom_id_entity.type_name = :type_name_1
    PAP.Company_has_Address PAP.Subject_has_Property
        SELECT mom_id_entity.electric AS mom_id_entity_electric,
               mom_id_entity.last_cid AS mom_id_entity_last_cid,
               mom_id_entity.pid AS mom_id_entity_pid,
               mom_id_entity.type_name AS mom_id_entity_type_name,
               mom_id_entity.x_locked AS mom_id_entity_x_locked,
               pap_company_has_address.pid AS pap_company_has_address_pid,
               pap_subject_has_property."desc" AS pap_subject_has_property_desc,
               pap_subject_has_property."left" AS pap_subject_has_property_left,
               pap_subject_has_property."right" AS pap_subject_has_property_right,
               pap_subject_has_property.pid AS pap_subject_has_property_pid
        FROM mom_id_entity
           JOIN pap_subject_has_property ON mom_id_entity.pid = pap_subject_has_property.pid
           JOIN pap_company_has_address ON pap_subject_has_property.pid = pap_company_has_address.pid
        WHERE mom_id_entity.type_name = :type_name_1
    PAP.Person_has_Address PAP.Subject_has_Property
        SELECT mom_id_entity.electric AS mom_id_entity_electric,
               mom_id_entity.last_cid AS mom_id_entity_last_cid,
               mom_id_entity.pid AS mom_id_entity_pid,
               mom_id_entity.type_name AS mom_id_entity_type_name,
               mom_id_entity.x_locked AS mom_id_entity_x_locked,
               pap_person_has_address.pid AS pap_person_has_address_pid,
               pap_subject_has_property."desc" AS pap_subject_has_property_desc,
               pap_subject_has_property."left" AS pap_subject_has_property_left,
               pap_subject_has_property."right" AS pap_subject_has_property_right,
               pap_subject_has_property.pid AS pap_subject_has_property_pid
        FROM mom_id_entity
           JOIN pap_subject_has_property ON mom_id_entity.pid = pap_subject_has_property.pid
           JOIN pap_person_has_address ON pap_subject_has_property.pid = pap_person_has_address.pid
        WHERE mom_id_entity.type_name = :type_name_1


"""

_test_sequences = """
    >>> apt, url = Scaffold.app_type_and_url (%(p1)s, %(n1)s)

    >>> show_sequence (apt)
    MOM.Id_Entity                            : mom_id_entity_pid_seq
    MOM.MD_Change                            : mom_md_change_cid_seq
    Auth.Certificate                         : auth_certificate_cert_id_seq

    >>> show_sequences (apt)
    MOM.Id_Entity                            : mom_id_entity_pid_seq
    MOM.MD_Change                            : mom_md_change_cid_seq
    Auth._Account_                           : mom_id_entity_pid_seq
    Auth.Account_Anonymous                   : mom_id_entity_pid_seq
    Auth.Account                             : mom_id_entity_pid_seq
    Auth.Certificate                         : mom_id_entity_pid_seq, auth_certificate_cert_id_seq
    Auth.Group                               : mom_id_entity_pid_seq
    Auth.Account_in_Group                    : mom_id_entity_pid_seq
    Auth.Account_Activation                  : mom_id_entity_pid_seq
    Auth.Account_Password_Change_Required    : mom_id_entity_pid_seq
    Auth.Account_EMail_Verification          : mom_id_entity_pid_seq
    Auth.Account_Password_Reset              : mom_id_entity_pid_seq
    EVT.Calendar                             : mom_id_entity_pid_seq
    SWP.Page                                 : mom_id_entity_pid_seq
    SWP.Page_Y                               : mom_id_entity_pid_seq
    EVT.Event                                : mom_id_entity_pid_seq
    EVT.Event_occurs                         : mom_id_entity_pid_seq
    EVT.Recurrence_Spec                      : mom_id_entity_pid_seq
    EVT.Recurrence_Rule                      : mom_id_entity_pid_seq
    PAP.Address                              : mom_id_entity_pid_seq
    PAP.Company                              : mom_id_entity_pid_seq
    PAP.Email                                : mom_id_entity_pid_seq
    PAP.Phone                                : mom_id_entity_pid_seq
    PAP.Person                               : mom_id_entity_pid_seq
    PAP.Url                                  : mom_id_entity_pid_seq
    PAP.Address_Position                     : mom_id_entity_pid_seq
    PAP.Subject_has_Property                 : mom_id_entity_pid_seq
    PAP.Person_has_Account                   : mom_id_entity_pid_seq
    SRM._Boat_Class_                         : mom_id_entity_pid_seq
    SRM.Boat_Class                           : mom_id_entity_pid_seq
    SRM.Handicap                             : mom_id_entity_pid_seq
    SRM.Boat                                 : mom_id_entity_pid_seq
    SRM.Club                                 : mom_id_entity_pid_seq
    SRM.Regatta_Event                        : mom_id_entity_pid_seq
    SWP.Clip_O                               : mom_id_entity_pid_seq
    SWP.Clip_X                               : mom_id_entity_pid_seq
    SWP.Gallery                              : mom_id_entity_pid_seq
    SWP.Picture                              : mom_id_entity_pid_seq
    SRM.Page                                 : mom_id_entity_pid_seq
    SRM.Regatta                              : mom_id_entity_pid_seq
    SRM.Regatta_C                            : mom_id_entity_pid_seq
    SRM.Regatta_H                            : mom_id_entity_pid_seq
    SRM.Sailor                               : mom_id_entity_pid_seq
    SRM.Boat_in_Regatta                      : mom_id_entity_pid_seq
    SRM.Race_Result                          : mom_id_entity_pid_seq
    SRM.Team                                 : mom_id_entity_pid_seq
    SRM.Crew_Member                          : mom_id_entity_pid_seq
    SRM.Team_has_Boat_in_Regatta             : mom_id_entity_pid_seq
    PAP.Subject_has_Phone                    : mom_id_entity_pid_seq
    PAP.Company_has_Url                      : mom_id_entity_pid_seq
    PAP.Person_has_Url                       : mom_id_entity_pid_seq
    PAP.Company_has_Phone                    : mom_id_entity_pid_seq
    PAP.Person_has_Phone                     : mom_id_entity_pid_seq
    PAP.Company_has_Email                    : mom_id_entity_pid_seq
    PAP.Person_has_Email                     : mom_id_entity_pid_seq
    PAP.Company_has_Address                  : mom_id_entity_pid_seq
    PAP.Person_has_Address                   : mom_id_entity_pid_seq

"""

_test_tables = """
    >>> apt, url = Scaffold.app_type_and_url (%(p1)s, %(n1)s)

    >>> for ETW in apt._SAW.e_types_t :
    ...     print (ETW.type_name)
    MOM.Id_Entity
    MOM.MD_Change
    Auth._Account_
    Auth.Account_Anonymous
    Auth.Account
    Auth.Certificate
    Auth.Group
    Auth.Account_in_Group
    Auth.Account_Activation
    Auth.Account_Password_Change_Required
    Auth.Account_EMail_Verification
    Auth.Account_Password_Reset
    EVT.Calendar
    SWP.Page
    SWP.Page_Y
    EVT.Event
    EVT.Event_occurs
    EVT.Recurrence_Spec
    EVT.Recurrence_Rule
    PAP.Address
    PAP.Company
    PAP.Email
    PAP.Phone
    PAP.Person
    PAP.Url
    PAP.Address_Position
    PAP.Subject_has_Property
    PAP.Person_has_Account
    SRM._Boat_Class_
    SRM.Boat_Class
    SRM.Handicap
    SRM.Boat
    SRM.Club
    SRM.Regatta_Event
    SWP.Clip_O
    SWP.Clip_X
    SWP.Gallery
    SWP.Picture
    SRM.Page
    SRM.Regatta
    SRM.Regatta_C
    SRM.Regatta_H
    SRM.Sailor
    SRM.Boat_in_Regatta
    SRM.Race_Result
    SRM.Team
    SRM.Crew_Member
    SRM.Team_has_Boat_in_Regatta
    PAP.Subject_has_Phone
    PAP.Company_has_Url
    PAP.Person_has_Url
    PAP.Company_has_Phone
    PAP.Person_has_Phone
    PAP.Company_has_Email
    PAP.Person_has_Email
    PAP.Company_has_Address
    PAP.Person_has_Address

    >>> for k, w in sorted (pyk.iteritems (apt._SAW.et_map)) :
    ...     print ("%%-40s : %%s" %% (k, w.sa_table))
    Auth.Account                             : auth_account
    Auth.Account_Activation                  : auth_account_activation
    Auth.Account_Anonymous                   : auth_account_anonymous
    Auth.Account_EMail_Verification          : auth_account_email_verification
    Auth.Account_Password_Change_Required    : auth_account_password_change_required
    Auth.Account_Password_Reset              : auth_account_password_reset
    Auth.Account_in_Group                    : auth_account_in_group
    Auth.Certificate                         : auth_certificate
    Auth.Group                               : auth_group
    Auth.Id_Entity                           : None
    Auth.Link                                : None
    Auth.Link1                               : None
    Auth.Link2                               : None
    Auth.Object                              : None
    Auth._Account_                           : auth__account_
    Auth._Account_Action_                    : None
    Auth._Account_Token_Action_              : None
    Auth._MOM_Link_n_                        : None
    EVT.Calendar                             : evt_calendar
    EVT.Event                                : evt_event
    EVT.Event_occurs                         : evt_event_occurs
    EVT.Id_Entity                            : None
    EVT.Link                                 : None
    EVT.Link1                                : None
    EVT.Object                               : None
    EVT.Recurrence_Rule                      : evt_recurrence_rule
    EVT.Recurrence_Spec                      : evt_recurrence_spec
    EVT._Recurrence_Mixin_                   : None
    MOM.D2_Value_Float                       : None
    MOM.D2_Value_Int                         : None
    MOM.Date_Interval                        : None
    MOM.Date_Interval_C                      : None
    MOM.Date_Interval_N                      : None
    MOM.Date_Time_Interval                   : None
    MOM.Date_Time_Interval_C                 : None
    MOM.Date_Time_Interval_N                 : None
    MOM.Id_Entity                            : mom_id_entity
    MOM.Link                                 : None
    MOM.Link1                                : None
    MOM.Link2                                : None
    MOM.Link3                                : None
    MOM.MD_Change                     : mom_md_change
    MOM.Object                               : None
    MOM.Position                             : None
    MOM.Time_Interval                        : None
    MOM._MOM_Link_n_                         : None
    MOM._Pic_                                : None
    MOM._Thumb_                              : None
    PAP.Address                              : pap_address
    PAP.Address_Position                     : pap_address_position
    PAP.Company                              : pap_company
    PAP.Company_has_Address                  : pap_company_has_address
    PAP.Company_has_Email                    : pap_company_has_email
    PAP.Company_has_Phone                    : pap_company_has_phone
    PAP.Company_has_Url                      : pap_company_has_url
    PAP.Email                                : pap_email
    PAP.Id_Entity                            : None
    PAP.Legal_Entity                         : None
    PAP.Link                                 : None
    PAP.Link1                                : None
    PAP.Link2                                : None
    PAP.Object                               : None
    PAP.Person                               : pap_person
    PAP.Person_has_Account                   : pap_person_has_account
    PAP.Person_has_Address                   : pap_person_has_address
    PAP.Person_has_Email                     : pap_person_has_email
    PAP.Person_has_Phone                     : pap_person_has_phone
    PAP.Person_has_Url                       : pap_person_has_url
    PAP.Phone                                : pap_phone
    PAP.Property                             : None
    PAP.Subject                              : None
    PAP.Subject_has_Address                  : None
    PAP.Subject_has_Email                    : None
    PAP.Subject_has_Phone                    : pap_subject_has_phone
    PAP.Subject_has_Property                 : pap_subject_has_property
    PAP.Subject_has_Url                      : None
    PAP.Url                                  : pap_url
    PAP._MOM_Link_n_                         : None
    SRM.Boat                                 : srm_boat
    SRM.Boat_Class                           : srm_boat_class
    SRM.Boat_in_Regatta                      : srm_boat_in_regatta
    SRM.Club                                 : srm_club
    SRM.Crew_Member                          : srm_crew_member
    SRM.Handicap                             : srm_handicap
    SRM.Id_Entity                            : None
    SRM.Link                                 : None
    SRM.Link1                                : None
    SRM.Link2                                : None
    SRM.Object                               : None
    SRM.Page                                 : srm_page
    SRM.Race_Result                          : srm_race_result
    SRM.Regatta                              : srm_regatta
    SRM.Regatta_C                            : srm_regatta_c
    SRM.Regatta_Event                        : srm_regatta_event
    SRM.Regatta_H                            : srm_regatta_h
    SRM.Regatta_Result                       : None
    SRM.Sailor                               : srm_sailor
    SRM.Team                                 : srm_team
    SRM.Team_has_Boat_in_Regatta             : srm_team_has_boat_in_regatta
    SRM._Boat_Class_                         : srm__boat_class_
    SRM._MOM_Link_n_                         : None
    SWP.Clip_O                               : swp_clip_o
    SWP.Clip_X                               : swp_clip_x
    SWP.Gallery                              : swp_gallery
    SWP.Id_Entity                            : None
    SWP.Link                                 : None
    SWP.Link1                                : None
    SWP.Object                               : None
    SWP.Object_PN                            : None
    SWP.Page                                 : swp_page
    SWP.Page_Mixin                           : None
    SWP.Page_Y                               : swp_page_y
    SWP.Picture                              : swp_picture


    >>> show_tables (apt)
    MOM.Id_Entity <Table mom_id_entity>
        Column electric                  : Boolean              Internal Boolean electric
        Column last_cid                  : Integer              Internal Int last_cid
        Column pid                       : Integer              Internal__Just_Once Surrogate pid primary
        Column type_name                 : Smallint             Internal__Type_Name String type_name
        Column x_locked                  : Boolean              Internal Boolean x_locked
    MOM.MD_Change <Table mom_md_change>
        Column c_time                    : Datetime             Internal__Computed__Sync_Change Date-Time c_time
        Column c_user                    : Integer              Internal__Computed__Sync_Change__Id_Entity_Reference Entity c_user Id_Entity()
        Column cid                       : Integer              Internal__Computed__Sync_Change__Just_Once Surrogate cid primary
        Column kind                      : Varchar(10)          Internal__Computed__Sync_Change String kind
        Column parent_cid                : Integer              Internal__Computed__Sync_Change Int parent_cid
        Column pid                       : Integer              Internal__Computed__Sync_Change Int pid
        Column scm_change                : Blob                 Internal Blob scm_change
        Column time                      : Datetime             Internal__Computed__Sync_Change Date-Time time
        Column type_name                 : Smallint             Internal__Computed__Sync_Change String type_name
        Column user                      : Integer              Internal__Computed__Sync_Change__Id_Entity_Reference Entity user Id_Entity()
    Auth._Account_ (MOM.Id_Entity) <Table auth__account_>
        Column enabled                   : Boolean              Optional Boolean enabled
        Column name                      : Varchar(80)          Primary Email name
        Column pid                       : Integer              Internal__Just_Once Surrogate pid primary ForeignKey(u'mom_id_entity.pid')
        Column superuser                 : Boolean              Optional Boolean superuser
        Column suspended                 : Boolean              Internal Boolean suspended
    Auth.Account_Anonymous (Auth._Account_) Auth._Account_ <Table auth_account_anonymous>
        Column pid                       : Integer              Internal__Just_Once Surrogate pid primary ForeignKey(u'auth__account_.pid')
    Auth.Account (Auth._Account_) Auth._Account_ <Table auth_account>
        Column password                  : Varchar(120)         Internal String password
        Column ph_name                   : Varchar(64)          Internal__Sticky String ph_name
        Column pid                       : Integer              Internal__Just_Once Surrogate pid primary ForeignKey(u'auth__account_.pid')
    Auth.Certificate (MOM.Id_Entity) <Table auth_certificate>
        Column cert_id                   : Integer              Internal__Just_Once Surrogate cert_id primary
        Column desc                      : Varchar(40)          Primary_Optional String desc
        Column email                     : Varchar(80)          Primary Email email
        Column pem                       : Blob                 Internal None pem
        Column pid                       : Integer              Internal__Just_Once Surrogate pid ForeignKey(u'mom_id_entity.pid')
        Column revocation_date           : Datetime             Optional Date-Time revocation_date
        Column validity__finish          : Datetime             Optional__Nested Date-Time finish
        Column validity__start           : Datetime             Necessary__Nested Date-Time start
    Auth.Group (MOM.Id_Entity) <Table auth_group>
        Column desc                      : Varchar(20)          Optional String desc
        Column name                      : Varchar(32)          Primary String name
        Column pid                       : Integer              Internal__Just_Once Surrogate pid primary ForeignKey(u'mom_id_entity.pid')
    Auth.Account_in_Group (MOM.Id_Entity) <Table auth_account_in_group>
        Column left                      : Integer              Link_Role Account left Id_Entity()
        Column pid                       : Integer              Internal__Just_Once Surrogate pid primary ForeignKey(u'mom_id_entity.pid')
        Column right                     : Integer              Link_Role Group right Id_Entity()
    Auth.Account_Activation (MOM.Id_Entity) <Table auth_account_activation>
        Column left                      : Integer              Link_Role__Init_Only Account left Id_Entity()
        Column pid                       : Integer              Internal__Just_Once Surrogate pid primary ForeignKey(u'mom_id_entity.pid')
    Auth.Account_Password_Change_Required (MOM.Id_Entity) <Table auth_account_password_change_required>
        Column left                      : Integer              Link_Role__Init_Only Account left Id_Entity()
        Column pid                       : Integer              Internal__Just_Once Surrogate pid primary ForeignKey(u'mom_id_entity.pid')
    Auth.Account_EMail_Verification (MOM.Id_Entity) <Table auth_account_email_verification>
        Column expires                   : Datetime             Necessary Date-Time expires
        Column left                      : Integer              Link_Role__Init_Only Account left Id_Entity()
        Column new_email                 : Varchar(80)          Optional Email new_email
        Column pid                       : Integer              Internal__Just_Once Surrogate pid primary ForeignKey(u'mom_id_entity.pid')
        Column token                     : Varchar(64)          Primary__Init_Only String token
    Auth.Account_Password_Reset (MOM.Id_Entity) <Table auth_account_password_reset>
        Column expires                   : Datetime             Necessary Date-Time expires
        Column left                      : Integer              Link_Role__Init_Only Account left Id_Entity()
        Column password                  : Varchar(64)          Necessary String password
        Column pid                       : Integer              Internal__Just_Once Surrogate pid primary ForeignKey(u'mom_id_entity.pid')
        Column token                     : Varchar(64)          Primary__Init_Only String token
    EVT.Calendar (MOM.Id_Entity) <Table evt_calendar>
        Column desc                      : Varchar(80)          Optional String desc
        Column name                      : Varchar(32)          Primary Name name
        Column pid                       : Integer              Internal__Just_Once Surrogate pid primary ForeignKey(u'mom_id_entity.pid')
    SWP.Page (MOM.Id_Entity) <Table swp_page>
        Column contents                  : Text                 Internal__Auto_Update Text contents
        Column date__finish              : Date                 Optional__Nested Date finish
        Column date__start               : Date                 Necessary__Sticky__Nested Date start
        Column format                    : Varchar(8)           Optional__Sticky Format format
        Column head_line                 : Varchar(256)         Optional String head_line
        Column hidden                    : Boolean              Optional Boolean hidden
        Column perma_name                : Varchar(80)          Primary Date-Slug perma_name
        Column pid                       : Integer              Internal__Just_Once Surrogate pid primary ForeignKey(u'mom_id_entity.pid')
        Column prio                      : Integer              Optional__Sticky Int prio
        Column short_title               : Varchar(30)          Necessary String short_title
        Column text                      : Text                 Required Text text
        Column title                     : Varchar(120)         Necessary String title
    SWP.Page_Y (SWP.Page) SWP.Page <Table swp_page_y>
        Column pid                       : Integer              Internal__Just_Once Surrogate pid primary ForeignKey(u'swp_page.pid')
        Column year                      : Integer              Primary_Optional Int year
    EVT.Event (MOM.Id_Entity) <Table evt_event>
        Column calendar                  : Integer              Primary_Optional__Id_Entity_Reference Entity calendar Id_Entity()
        Column date__finish              : Date                 Optional__Nested Date finish
        Column date__start               : Date                 Necessary__Nested Date start
        Column detail                    : Varchar(160)         Optional String detail
        Column left                      : Integer              Link_Role__Init_Only Page left Id_Entity()
        Column pid                       : Integer              Internal__Just_Once Surrogate pid primary ForeignKey(u'mom_id_entity.pid')
        Column short_title               : Varchar(64)          Optional__Computed_Set String short_title
        Column time__finish              : Time                 Optional__Nested Time finish
        Column time__start               : Time                 Necessary__Nested Time start
    EVT.Event_occurs (MOM.Id_Entity) <Table evt_event_occurs>
        Column date                      : Date                 Primary Date date
        Column left                      : Integer              Link_Role__Init_Only Event left Id_Entity()
        Column pid                       : Integer              Internal__Just_Once Surrogate pid primary ForeignKey(u'mom_id_entity.pid')
        Column time__finish              : Time                 Optional__Nested Time finish
        Column time__start               : Time                 Necessary__Nested Time start
    EVT.Recurrence_Spec (MOM.Id_Entity) <Table evt_recurrence_spec>
        Column date_exceptions           : Blob                 Optional__Typed_Collection Date_List date_exceptions
        Column dates                     : Blob                 Optional__Typed_Collection Date_List dates
        Column left                      : Integer              Link_Role__Init_Only Event left Id_Entity()
        Column pid                       : Integer              Internal__Just_Once Surrogate pid primary ForeignKey(u'mom_id_entity.pid')
    EVT.Recurrence_Rule (MOM.Id_Entity) <Table evt_recurrence_rule>
        Column count                     : Integer              Optional Int count
        Column desc                      : Varchar(20)          Primary_Optional String desc
        Column easter_offset             : Blob                 Optional__Typed_Collection Int_List easter_offset
        Column finish                    : Date                 Optional__Computed_Set Date finish
        Column is_exception              : Boolean              Primary_Optional Boolean is_exception
        Column left                      : Integer              Link_Role__Init_Only Recurrence_Spec left Id_Entity()
        Column month                     : Blob                 Optional__Typed_Collection Int_List month
        Column month_day                 : Blob                 Optional__Typed_Collection Int_List month_day
        Column period                    : Integer              Optional Int period
        Column pid                       : Integer              Internal__Just_Once Surrogate pid primary ForeignKey(u'mom_id_entity.pid')
        Column restrict_pos              : Blob                 Optional__Typed_Collection Int_List restrict_pos
        Column start                     : Date                 Optional__Computed_Set Date start
        Column unit                      : Integer              Optional__Sticky Unit unit
        Column week                      : Blob                 Optional__Typed_Collection Int_List week
        Column week_day                  : Blob                 Optional__Typed_Collection Weekday_RR_List week_day
        Column year_day                  : Blob                 Optional__Typed_Collection Int_List year_day
    PAP.Address (MOM.Id_Entity) <Table pap_address>
        Column __raw_city                : Varchar(30)          Primary__Raw_Value String city
        Column __raw_country             : Varchar(20)          Primary__Raw_Value String country
        Column __raw_region              : Varchar(20)          Optional__Raw_Value String region
        Column __raw_street              : Varchar(60)          Primary__Raw_Value String street
        Column __raw_zip                 : Varchar(6)           Primary__Raw_Value String zip
        Column city                      : Varchar(30)          Primary__Raw_Value String city
        Column country                   : Varchar(20)          Primary__Raw_Value String country
        Column desc                      : Varchar(20)          Optional String desc
        Column pid                       : Integer              Internal__Just_Once Surrogate pid primary ForeignKey(u'mom_id_entity.pid')
        Column region                    : Varchar(20)          Optional__Raw_Value String region
        Column street                    : Varchar(60)          Primary__Raw_Value String street
        Column zip                       : Varchar(6)           Primary__Raw_Value String zip
    PAP.Company (MOM.Id_Entity) <Table pap_company>
        Column __raw_name                : Varchar(64)          Primary__Raw_Value String name
        Column __raw_registered_in       : Varchar(64)          Primary_Optional__Raw_Value String registered_in
        Column __raw_short_name          : Varchar(12)          Optional__Raw_Value String short_name
        Column lifetime__finish          : Date                 Optional__Nested Date finish
        Column lifetime__start           : Date                 Necessary__Nested Date start
        Column name                      : Varchar(64)          Primary__Raw_Value String name
        Column pid                       : Integer              Internal__Just_Once Surrogate pid primary ForeignKey(u'mom_id_entity.pid')
        Column registered_in             : Varchar(64)          Primary_Optional__Raw_Value String registered_in
        Column short_name                : Varchar(12)          Optional__Raw_Value String short_name
    PAP.Email (MOM.Id_Entity) <Table pap_email>
        Column __raw_address             : Varchar(80)          Primary__Raw_Value Email address
        Column address                   : Varchar(80)          Primary__Raw_Value Email address
        Column desc                      : Varchar(20)          Optional String desc
        Column pid                       : Integer              Internal__Just_Once Surrogate pid primary ForeignKey(u'mom_id_entity.pid')
    PAP.Phone (MOM.Id_Entity) <Table pap_phone>
        Column area_code                 : Varchar(5)           Primary Numeric_String area_code
        Column country_code              : Varchar(3)           Primary Numeric_String country_code
        Column desc                      : Varchar(20)          Optional String desc
        Column number                    : Varchar(14)          Primary Numeric_String number
        Column pid                       : Integer              Internal__Just_Once Surrogate pid primary ForeignKey(u'mom_id_entity.pid')
    PAP.Person (MOM.Id_Entity) <Table pap_person>
        Column __raw_first_name          : Varchar(32)          Primary__Raw_Value String first_name
        Column __raw_last_name           : Varchar(48)          Primary__Raw_Value String last_name
        Column __raw_middle_name         : Varchar(32)          Primary_Optional__Raw_Value String middle_name
        Column __raw_title               : Varchar(20)          Primary_Optional__Raw_Value String title
        Column first_name                : Varchar(32)          Primary__Raw_Value String first_name
        Column last_name                 : Varchar(48)          Primary__Raw_Value String last_name
        Column lifetime__finish          : Date                 Optional__Nested Date finish
        Column lifetime__start           : Date                 Necessary__Nested Date start
        Column middle_name               : Varchar(32)          Primary_Optional__Raw_Value String middle_name
        Column pid                       : Integer              Internal__Just_Once Surrogate pid primary ForeignKey(u'mom_id_entity.pid')
        Column sex                       : Varchar(1)           Necessary Sex sex
        Column title                     : Varchar(20)          Primary_Optional__Raw_Value String title
    PAP.Url (MOM.Id_Entity) <Table pap_url>
        Column desc                      : Varchar(20)          Optional String desc
        Column pid                       : Integer              Internal__Just_Once Surrogate pid primary ForeignKey(u'mom_id_entity.pid')
        Column value                     : Varchar(160)         Primary Url value
    PAP.Address_Position (MOM.Id_Entity) <Table pap_address_position>
        Column left                      : Integer              Link_Role__Init_Only Address left Id_Entity()
        Column pid                       : Integer              Internal__Just_Once Surrogate pid primary ForeignKey(u'mom_id_entity.pid')
        Column position____raw_lat       : Varchar(22)          Necessary__Raw_Value__Nested Angle lat
        Column position____raw_lon       : Varchar(22)          Necessary__Raw_Value__Nested Angle lon
        Column position__height          : Float                Optional__Nested Float height
        Column position__lat             : Float                Necessary__Raw_Value__Nested Angle lat
        Column position__lon             : Float                Necessary__Raw_Value__Nested Angle lon
    PAP.Subject_has_Property (MOM.Id_Entity) <Table pap_subject_has_property>
        Column desc                      : Varchar(20)          Optional__Computed_Set String desc
        Column left                      : Integer              Link_Role Subject left Id_Entity()
        Column pid                       : Integer              Internal__Just_Once Surrogate pid primary ForeignKey(u'mom_id_entity.pid')
        Column right                     : Integer              Link_Role Property right Id_Entity()
    PAP.Person_has_Account (MOM.Id_Entity) <Table pap_person_has_account>
        Column left                      : Integer              Link_Role Person left Id_Entity()
        Column pid                       : Integer              Internal__Just_Once Surrogate pid primary ForeignKey(u'mom_id_entity.pid')
        Column right                     : Integer              Link_Role Account right Id_Entity()
    SRM._Boat_Class_ (MOM.Id_Entity) <Table srm__boat_class_>
        Column __raw_name                : Varchar(48)          Primary__Raw_Value String name
        Column name                      : Varchar(48)          Primary__Raw_Value String name
        Column pid                       : Integer              Internal__Just_Once Surrogate pid primary ForeignKey(u'mom_id_entity.pid')
    SRM.Boat_Class (SRM._Boat_Class_) SRM._Boat_Class_ <Table srm_boat_class>
        Column beam                      : Float                Optional Float beam
        Column loa                       : Float                Optional Float loa
        Column max_crew                  : Smallint             Required Int max_crew
        Column pid                       : Integer              Internal__Just_Once Surrogate pid primary ForeignKey(u'srm__boat_class_.pid')
        Column sail_area                 : Float                Optional Float sail_area
    SRM.Handicap (SRM._Boat_Class_) SRM._Boat_Class_ <Table srm_handicap>
        Column pid                       : Integer              Internal__Just_Once Surrogate pid primary ForeignKey(u'srm__boat_class_.pid')
    SRM.Boat (MOM.Id_Entity) <Table srm_boat>
        Column __raw_sail_number         : Varchar(7)           Primary__Raw_Value Int sail_number
        Column __raw_sail_number_x       : Varchar(8)           Primary_Optional__Raw_Value String sail_number_x
        Column left                      : Integer              Link_Role__Init_Only Boat_Class left Id_Entity()
        Column name                      : Varchar(48)          Optional String name
        Column nation                    : Varchar(3)           Primary_Optional Nation nation
        Column pid                       : Integer              Internal__Just_Once Surrogate pid primary ForeignKey(u'mom_id_entity.pid')
        Column sail_number               : Integer              Primary__Raw_Value Int sail_number
        Column sail_number_x             : Varchar(8)           Primary_Optional__Raw_Value String sail_number_x
    SRM.Club (MOM.Id_Entity) <Table srm_club>
        Column __raw_name                : Varchar(8)           Primary__Raw_Value String name
        Column long_name                 : Varchar(64)          Optional String long_name
        Column name                      : Varchar(8)           Primary__Raw_Value String name
        Column pid                       : Integer              Internal__Just_Once Surrogate pid primary ForeignKey(u'mom_id_entity.pid')
    SRM.Regatta_Event (MOM.Id_Entity) <Table srm_regatta_event>
        Column __raw_name                : Varchar(64)          Primary__Raw_Value String name
        Column club                      : Integer              Optional__Id_Entity_Reference Entity club Id_Entity()
        Column date__finish              : Date                 Optional__Computed_Set__Nested Date finish
        Column date__start               : Date                 Necessary__Nested Date start
        Column desc                      : Varchar(160)         Optional String desc
        Column is_cancelled              : Boolean              Optional Boolean is_cancelled
        Column name                      : Varchar(64)          Primary__Raw_Value String name
        Column perma_name                : Varchar(64)          Internal__Auto_Update_Lazy__Computed_Set String perma_name
        Column pid                       : Integer              Internal__Just_Once Surrogate pid primary ForeignKey(u'mom_id_entity.pid')
    SWP.Clip_O (MOM.Id_Entity) <Table swp_clip_o>
        Column abstract                  : Text                 Required Text abstract
        Column contents                  : Text                 Internal__Auto_Update Text contents
        Column date__finish              : Date                 Optional__Nested Date finish
        Column date__start               : Date                 Necessary__Nested Date start
        Column date_x__finish            : Date                 Optional__Nested Date finish
        Column date_x__start             : Date                 Necessary__Nested Date start
        Column left                      : Integer              Link_Role__Init_Only Object_PN left Id_Entity()
        Column pid                       : Integer              Internal__Just_Once Surrogate pid primary ForeignKey(u'mom_id_entity.pid')
        Column prio                      : Integer              Optional__Sticky Int prio
    SWP.Clip_X (SWP.Page) SWP.Page <Table swp_clip_x>
        Column link_to                   : Varchar(160)         Optional Url link_to
        Column pid                       : Integer              Internal__Just_Once Surrogate pid primary ForeignKey(u'swp_page.pid')
    SWP.Gallery (MOM.Id_Entity) <Table swp_gallery>
        Column date__finish              : Date                 Optional__Nested Date finish
        Column date__start               : Date                 Necessary__Sticky__Nested Date start
        Column directory                 : Text                 Necessary Directory directory
        Column perma_name                : Varchar(80)          Primary Date-Slug perma_name
        Column pid                       : Integer              Internal__Just_Once Surrogate pid primary ForeignKey(u'mom_id_entity.pid')
        Column short_title               : Varchar(30)          Necessary String short_title
        Column title                     : Varchar(120)         Necessary String title
    SWP.Picture (MOM.Id_Entity) <Table swp_picture>
        Column left                      : Integer              Link_Role__Init_Only Gallery left Id_Entity()
        Column name                      : Varchar(100)         Optional__Computed_Set String name
        Column number                    : Integer              Primary Int number
        Column photo__extension          : Varchar(10)          Optional__Init_Only__Nested String extension
        Column photo__height             : Smallint             Necessary__Nested Y height
        Column photo__width              : Smallint             Necessary__Nested X width
        Column pid                       : Integer              Internal__Just_Once Surrogate pid primary ForeignKey(u'mom_id_entity.pid')
        Column thumb__extension          : Varchar(10)          Optional__Init_Only__Nested String extension
        Column thumb__height             : Smallint             Necessary__Nested Y height
        Column thumb__width              : Smallint             Necessary__Nested X width
    SRM.Page (SWP.Page) SWP.Page <Table srm_page>
        Column desc                      : Varchar(30)          Optional__Computed_Set String desc
        Column event                     : Integer              Primary__Id_Entity_Reference Entity event Id_Entity()
        Column pid                       : Integer              Internal__Just_Once Surrogate pid primary ForeignKey(u'swp_page.pid')
    SRM.Regatta (MOM.Id_Entity) <Table srm_regatta>
        Column boat_class                : Integer              Primary__Id_Entity_Reference Entity boat_class Id_Entity()
        Column discards                  : Integer              Optional Int discards
        Column is_cancelled              : Boolean              Optional__Computed_Set Boolean is_cancelled
        Column kind                      : Varchar(32)          Optional String kind
        Column left                      : Integer              Link_Role__Init_Only Regatta_Event left Id_Entity()
        Column perma_name                : Varchar(64)          Internal__Auto_Update_Lazy__Computed_Set String perma_name
        Column pid                       : Integer              Internal__Just_Once Surrogate pid primary ForeignKey(u'mom_id_entity.pid')
        Column races                     : Integer              Optional Int races
        Column result__date              : Datetime             Necessary__Nested Date-Time date
        Column result__software          : Varchar(64)          Optional__Nested String software
        Column result__status            : Varchar(64)          Optional__Nested String status
    SRM.Regatta_C (SRM.Regatta) SRM.Regatta <Table srm_regatta_c>
        Column is_team_race              : Boolean              Optional Boolean is_team_race
        Column pid                       : Integer              Internal__Just_Once Surrogate pid primary ForeignKey(u'srm_regatta.pid')
    SRM.Regatta_H (SRM.Regatta) SRM.Regatta <Table srm_regatta_h>
        Column pid                       : Integer              Internal__Just_Once Surrogate pid primary ForeignKey(u'srm_regatta.pid')
    SRM.Sailor (MOM.Id_Entity) <Table srm_sailor>
        Column __raw_mna_number          : Varchar(7)           Primary_Optional__Raw_Value Int mna_number
        Column club                      : Integer              Primary_Optional__Id_Entity_Reference Entity club Id_Entity()
        Column left                      : Integer              Link_Role__Init_Only Person left Id_Entity()
        Column mna_number                : Integer              Primary_Optional__Raw_Value Int mna_number
        Column nation                    : Varchar(3)           Primary_Optional Nation nation
        Column pid                       : Integer              Internal__Just_Once Surrogate pid primary ForeignKey(u'mom_id_entity.pid')
    SRM.Boat_in_Regatta (MOM.Id_Entity) <Table srm_boat_in_regatta>
        Column left                      : Integer              Link_Role Boat left Id_Entity()
        Column pid                       : Integer              Internal__Just_Once Surrogate pid primary ForeignKey(u'mom_id_entity.pid')
        Column place                     : Integer              Optional Int place
        Column points                    : Integer              Optional Int points
        Column rank                      : Integer              Internal Int rank
        Column registration_date         : Date                 Internal__Init_Only Date registration_date
        Column right                     : Integer              Link_Role Regatta right Id_Entity()
        Column skipper                   : Integer              Required__Id_Entity_Reference Entity skipper Id_Entity()
    SRM.Race_Result (MOM.Id_Entity) <Table srm_race_result>
        Column discarded                 : Boolean              Optional__Sticky Boolean discarded
        Column left                      : Integer              Link_Role__Init_Only Boat_in_Regatta left Id_Entity()
        Column pid                       : Integer              Internal__Just_Once Surrogate pid primary ForeignKey(u'mom_id_entity.pid')
        Column points                    : Integer              Necessary Int points
        Column race                      : Smallint             Primary Int race
        Column status                    : Varchar(8)           Optional String status
    SRM.Team (MOM.Id_Entity) <Table srm_team>
        Column __raw_name                : Varchar(64)          Primary__Raw_Value String name
        Column club                      : Integer              Optional__Id_Entity_Reference Entity club Id_Entity()
        Column desc                      : Varchar(160)         Optional String desc
        Column leader                    : Integer              Optional__Id_Entity_Reference Entity leader Id_Entity()
        Column left                      : Integer              Link_Role__Init_Only Regatta_C left Id_Entity()
        Column name                      : Varchar(64)          Primary__Raw_Value String name
        Column pid                       : Integer              Internal__Just_Once Surrogate pid primary ForeignKey(u'mom_id_entity.pid')
        Column place                     : Integer              Optional Int place
        Column registration_date         : Date                 Internal Date registration_date
    SRM.Crew_Member (MOM.Id_Entity) <Table srm_crew_member>
        Column key                       : Integer              Optional__Sticky Int key
        Column left                      : Integer              Link_Role Boat_in_Regatta left Id_Entity()
        Column pid                       : Integer              Internal__Just_Once Surrogate pid primary ForeignKey(u'mom_id_entity.pid')
        Column right                     : Integer              Link_Role Sailor right Id_Entity()
        Column role                      : Varchar(32)          Optional String role
    SRM.Team_has_Boat_in_Regatta (MOM.Id_Entity) <Table srm_team_has_boat_in_regatta>
        Column left                      : Integer              Link_Role Team left Id_Entity()
        Column pid                       : Integer              Internal__Just_Once Surrogate pid primary ForeignKey(u'mom_id_entity.pid')
        Column right                     : Integer              Link_Role Boat_in_Regatta right Id_Entity()
    PAP.Subject_has_Phone (PAP.Subject_has_Property) PAP.Subject_has_Property <Table pap_subject_has_phone>
        Column extension                 : Varchar(5)           Primary_Optional Numeric_String extension
        Column pid                       : Integer              Internal__Just_Once Surrogate pid primary ForeignKey(u'pap_subject_has_property.pid')
    PAP.Company_has_Url (PAP.Subject_has_Property) PAP.Subject_has_Property <Table pap_company_has_url>
        Column pid                       : Integer              Internal__Just_Once Surrogate pid primary ForeignKey(u'pap_subject_has_property.pid')
    PAP.Person_has_Url (PAP.Subject_has_Property) PAP.Subject_has_Property <Table pap_person_has_url>
        Column pid                       : Integer              Internal__Just_Once Surrogate pid primary ForeignKey(u'pap_subject_has_property.pid')
    PAP.Company_has_Phone (PAP.Subject_has_Phone) PAP.Subject_has_Property <Table pap_company_has_phone>
        Column pid                       : Integer              Internal__Just_Once Surrogate pid primary ForeignKey(u'pap_subject_has_phone.pid')
    PAP.Person_has_Phone (PAP.Subject_has_Phone) PAP.Subject_has_Property <Table pap_person_has_phone>
        Column pid                       : Integer              Internal__Just_Once Surrogate pid primary ForeignKey(u'pap_subject_has_phone.pid')
    PAP.Company_has_Email (PAP.Subject_has_Property) PAP.Subject_has_Property <Table pap_company_has_email>
        Column pid                       : Integer              Internal__Just_Once Surrogate pid primary ForeignKey(u'pap_subject_has_property.pid')
    PAP.Person_has_Email (PAP.Subject_has_Property) PAP.Subject_has_Property <Table pap_person_has_email>
        Column pid                       : Integer              Internal__Just_Once Surrogate pid primary ForeignKey(u'pap_subject_has_property.pid')
    PAP.Company_has_Address (PAP.Subject_has_Property) PAP.Subject_has_Property <Table pap_company_has_address>
        Column pid                       : Integer              Internal__Just_Once Surrogate pid primary ForeignKey(u'pap_subject_has_property.pid')
    PAP.Person_has_Address (PAP.Subject_has_Property) PAP.Subject_has_Property <Table pap_person_has_address>
        Column pid                       : Integer              Internal__Just_Once Surrogate pid primary ForeignKey(u'pap_subject_has_property.pid')
    <Table for Surrogate `pid`>
        Column electric                  : Boolean              Internal Boolean electric
        Column last_cid                  : Integer              Internal Int last_cid
        Column pid                       : Integer              Internal__Just_Once Surrogate pid primary
        Column type_name                 : Smallint             Internal__Type_Name String type_name
        Column x_locked                  : Boolean              Internal Boolean x_locked
    <Table for Surrogate `cid`>
        Column c_time                    : Datetime             Internal__Computed__Sync_Change Date-Time c_time
        Column c_user                    : Integer              Internal__Computed__Sync_Change__Id_Entity_Reference Entity c_user Id_Entity()
        Column cid                       : Integer              Internal__Computed__Sync_Change__Just_Once Surrogate cid primary
        Column kind                      : Varchar(10)          Internal__Computed__Sync_Change String kind
        Column parent_cid                : Integer              Internal__Computed__Sync_Change Int parent_cid
        Column pid                       : Integer              Internal__Computed__Sync_Change Int pid
        Column scm_change                : Blob                 Internal Blob scm_change
        Column time                      : Datetime             Internal__Computed__Sync_Change Date-Time time
        Column type_name                 : Smallint             Internal__Computed__Sync_Change String type_name
        Column user                      : Integer              Internal__Computed__Sync_Change__Id_Entity_Reference Entity user Id_Entity()
    <Table for Surrogate `cert_id`>
        Column cert_id                   : Integer              ---------- primary


"""

_test_unique = """
    >>> apt, url = Scaffold.app_type_and_url (%(p1)s, %(n1)s)

    >>> for ETW in apt._SAW.e_types_t :
    ...     T  = ETW.e_type
    ...     ui = ETW.unique_i
    ...     uo = ETW.unique_o
    ...     if T.show_in_ui and ETW.unique :
    ...         tail = "" if ui == uo else \\
    ...             (((" + " if ui else "") + ", ".join (uo)) if uo else " =")
    ...         print (("%%-30s %%s%%s" %% (ETW.type_name, ", ".join (ui), tail)).strip ())
    Auth._Account_                 name
    Auth.Account                   name =
    Auth.Certificate               desc, email, validity__finish, validity__start
    Auth.Group                     name
    Auth.Account_in_Group          left, right
    EVT.Calendar                   name
    SWP.Page                       perma_name
    SWP.Page_Y                     perma_name + year
    EVT.Event                      calendar, date__finish, date__start, left, time__finish, time__start
    EVT.Event_occurs               date, left, time__finish, time__start
    EVT.Recurrence_Spec            left
    EVT.Recurrence_Rule            desc, is_exception, left
    PAP.Address                    city, country, street, zip
    PAP.Company                    name, registered_in
    PAP.Email                      address
    PAP.Phone                      area_code, country_code, number
    PAP.Person                     first_name, last_name, middle_name, title
    PAP.Url                        value
    PAP.Address_Position           left, position__height, position__lat, position__lon
    PAP.Subject_has_Property       left, right
    PAP.Person_has_Account         left, right
    SRM._Boat_Class_               name
    SRM.Boat_Class                 name =
    SRM.Handicap                   name =
    SRM.Boat                       left, nation, sail_number, sail_number_x
    SRM.Club                       name
    SRM.Regatta_Event              date__finish, date__start, name
    SWP.Clip_O                     date_x__finish, date_x__start, left
    SWP.Clip_X                     perma_name =
    SWP.Gallery                    perma_name
    SWP.Picture                    left, number
    SRM.Page                       perma_name + event
    SRM.Regatta                    boat_class, left
    SRM.Regatta_C                  boat_class, left =
    SRM.Regatta_H                  boat_class, left =
    SRM.Sailor                     club, left, mna_number, nation
    SRM.Boat_in_Regatta            left, right
    SRM.Race_Result                left, race
    SRM.Team                       left, name
    SRM.Crew_Member                left, right
    SRM.Team_has_Boat_in_Regatta   left, right
    PAP.Subject_has_Phone          left, right + extension
    PAP.Company_has_Url            left, right =
    PAP.Person_has_Url             left, right =
    PAP.Company_has_Phone          extension, left, right =
    PAP.Person_has_Phone           extension, left, right =
    PAP.Company_has_Email          left, right =
    PAP.Person_has_Email           left, right =
    PAP.Company_has_Address        left, right =
    PAP.Person_has_Address         left, right =

"""

_test_date_extraction_pg = """
    >>> apt, url = Scaffold.app_type_and_url (%(p1)s, %(n1)s)

    >>> ET = apt ["SRM.Regatta_C"]
    >>> qrt = apt.DBW.PNS.Q_Result.E_Type (ET, _strict = False)

    >>> print (qrt.filter (Q.left.date.start.year == 2013)) ### SRM.Regatta_C
    SQL: SELECT
           mom_id_entity.electric AS mom_id_entity_electric,
           mom_id_entity.last_cid AS mom_id_entity_last_cid,
           mom_id_entity.pid AS mom_id_entity_pid,
           mom_id_entity.type_name AS mom_id_entity_type_name,
           mom_id_entity.x_locked AS mom_id_entity_x_locked,
           srm_regatta."left" AS srm_regatta_left,
           srm_regatta.boat_class AS srm_regatta_boat_class,
           srm_regatta.discards AS srm_regatta_discards,
           srm_regatta.is_cancelled AS srm_regatta_is_cancelled,
           srm_regatta.kind AS srm_regatta_kind,
           srm_regatta.perma_name AS srm_regatta_perma_name,
           srm_regatta.pid AS srm_regatta_pid,
           srm_regatta.races AS srm_regatta_races,
           srm_regatta.result__date AS srm_regatta_result__date,
           srm_regatta.result__software AS srm_regatta_result__software,
           srm_regatta.result__status AS srm_regatta_result__status,
           srm_regatta_c.is_team_race AS srm_regatta_c_is_team_race,
           srm_regatta_c.pid AS srm_regatta_c_pid
         FROM mom_id_entity
           JOIN srm_regatta ON mom_id_entity.pid = srm_regatta.pid
           JOIN srm_regatta_c ON srm_regatta.pid = srm_regatta_c.pid
           JOIN srm_regatta_event AS srm_regatta_event__1 ON srm_regatta_event__1.pid = srm_regatta."left"
         WHERE EXTRACT(year FROM srm_regatta_event__1.date__start) = :param_1

    >>> show_query (qrt.filter (Q.event.date.start.year == 2010)) ### SRM.Regatta_C
    SQL: SELECT
           mom_id_entity.electric AS mom_id_entity_electric,
           mom_id_entity.last_cid AS mom_id_entity_last_cid,
           mom_id_entity.pid AS mom_id_entity_pid,
           mom_id_entity.type_name AS mom_id_entity_type_name,
           mom_id_entity.x_locked AS mom_id_entity_x_locked,
           srm_regatta."left" AS srm_regatta_left,
           srm_regatta.boat_class AS srm_regatta_boat_class,
           srm_regatta.discards AS srm_regatta_discards,
           srm_regatta.is_cancelled AS srm_regatta_is_cancelled,
           srm_regatta.kind AS srm_regatta_kind,
           srm_regatta.perma_name AS srm_regatta_perma_name,
           srm_regatta.pid AS srm_regatta_pid,
           srm_regatta.races AS srm_regatta_races,
           srm_regatta.result__date AS srm_regatta_result__date,
           srm_regatta.result__software AS srm_regatta_result__software,
           srm_regatta.result__status AS srm_regatta_result__status,
           srm_regatta_c.is_team_race AS srm_regatta_c_is_team_race,
           srm_regatta_c.pid AS srm_regatta_c_pid
         FROM mom_id_entity
           JOIN srm_regatta ON mom_id_entity.pid = srm_regatta.pid
           JOIN srm_regatta_c ON srm_regatta.pid = srm_regatta_c.pid
           JOIN srm_regatta_event AS srm_regatta_event__1 ON srm_regatta_event__1.pid = srm_regatta."left"
         WHERE EXTRACT(year FROM srm_regatta_event__1.date__start) = :param_1
    Parameters:
         param_1              : 2010

"""

_test_date_extraction_sq = """
    >>> apt, url = Scaffold.app_type_and_url (%(p1)s, %(n1)s)

    >>> ET = apt ["SRM.Regatta_C"]
    >>> qrt = apt.DBW.PNS.Q_Result.E_Type (ET, _strict = False)

    >>> print (qrt.filter (Q.left.date.start.year == 2013)) ### SRM.Regatta_C
    SQL: SELECT
           mom_id_entity.electric AS mom_id_entity_electric,
           mom_id_entity.last_cid AS mom_id_entity_last_cid,
           mom_id_entity.pid AS mom_id_entity_pid,
           mom_id_entity.type_name AS mom_id_entity_type_name,
           mom_id_entity.x_locked AS mom_id_entity_x_locked,
           srm_regatta."left" AS srm_regatta_left,
           srm_regatta.boat_class AS srm_regatta_boat_class,
           srm_regatta.discards AS srm_regatta_discards,
           srm_regatta.is_cancelled AS srm_regatta_is_cancelled,
           srm_regatta.kind AS srm_regatta_kind,
           srm_regatta.perma_name AS srm_regatta_perma_name,
           srm_regatta.pid AS srm_regatta_pid,
           srm_regatta.races AS srm_regatta_races,
           srm_regatta.result__date AS srm_regatta_result__date,
           srm_regatta.result__software AS srm_regatta_result__software,
           srm_regatta.result__status AS srm_regatta_result__status,
           srm_regatta_c.is_team_race AS srm_regatta_c_is_team_race,
           srm_regatta_c.pid AS srm_regatta_c_pid
         FROM mom_id_entity
           JOIN srm_regatta ON mom_id_entity.pid = srm_regatta.pid
           JOIN srm_regatta_c ON srm_regatta.pid = srm_regatta_c.pid
           JOIN srm_regatta_event AS srm_regatta_event__1 ON srm_regatta_event__1.pid = srm_regatta."left"
         WHERE CAST(strftime(:strftime_1, srm_regatta_event__1.date__start) AS INTEGER) = :param_1

    >>> show_query (qrt.filter (Q.event.date.start.year == 2010)) ### SRM.Regatta_C
    SQL: SELECT
           mom_id_entity.electric AS mom_id_entity_electric,
           mom_id_entity.last_cid AS mom_id_entity_last_cid,
           mom_id_entity.pid AS mom_id_entity_pid,
           mom_id_entity.type_name AS mom_id_entity_type_name,
           mom_id_entity.x_locked AS mom_id_entity_x_locked,
           srm_regatta."left" AS srm_regatta_left,
           srm_regatta.boat_class AS srm_regatta_boat_class,
           srm_regatta.discards AS srm_regatta_discards,
           srm_regatta.is_cancelled AS srm_regatta_is_cancelled,
           srm_regatta.kind AS srm_regatta_kind,
           srm_regatta.perma_name AS srm_regatta_perma_name,
           srm_regatta.pid AS srm_regatta_pid,
           srm_regatta.races AS srm_regatta_races,
           srm_regatta.result__date AS srm_regatta_result__date,
           srm_regatta.result__software AS srm_regatta_result__software,
           srm_regatta.result__status AS srm_regatta_result__status,
           srm_regatta_c.is_team_race AS srm_regatta_c_is_team_race,
           srm_regatta_c.pid AS srm_regatta_c_pid
         FROM mom_id_entity
           JOIN srm_regatta ON mom_id_entity.pid = srm_regatta.pid
           JOIN srm_regatta_c ON srm_regatta.pid = srm_regatta_c.pid
           JOIN srm_regatta_event AS srm_regatta_event__1 ON srm_regatta_event__1.pid = srm_regatta."left"
         WHERE CAST(strftime(:strftime_1, srm_regatta_event__1.date__start) AS INTEGER) = :param_1
    Parameters:
         param_1              : 2010
         strftime_1           : u'%%Y'

"""

_debug = """
    >>> apt, url = Scaffold.app_type_and_url (%(p1)s, %(n1)s)


"""

__test__ = Scaffold.create_test_dict \
    ( dict
        ( test_ancestors        = _test_ancestors
        , test_attr_wrappers    = _test_attr_wrappers
        , test_fk_cols          = _test_fk_cols
        , test_key_o_p          = _test_key_o_p
        , test_parents          = _test_parents
        , test_q_able           = _test_q_able
        , test_qc_map           = _test_qc_map
        , test_select           = _test_select
        , test_select_strict    = _test_select_strict
        , test_sequences        = _test_sequences
        , test_tables           = _test_tables
        , test_unique           = _test_unique
        )
    , ignore = ("HPS", )
    )

import sqlalchemy
if sqlalchemy.__version__ >= "0.8" :
    __test__.update \
        ( Scaffold.create_test_dict
            ( dict
                ( test_q_result   = _test_q_result
                , test_q_result_x = _test_q_result_x
                )
              , ignore = ("HPS", )
            )
        )

__test__.update \
    ( Scaffold.create_test_dict
        ( dict
            ( test_date_extraction = _test_date_extraction_pg
            )
        , ignore = ("HPS", "MYS", "SQL", "sq")
        )
    )

__test__.update \
    ( Scaffold.create_test_dict
        ( dict
            ( test_date_extraction = _test_date_extraction_sq
            )
        , ignore = ("HPS", "MYS", "POS", "pg")
        )
    )

X__test__ = Scaffold.create_test_dict \
    ( dict (debug = _debug)
    , ignore = ("HPS", )
    )

if __name__ == "__main__" :
    db_url = sos.environ.get ("GTW_test_backends", "sq")
    if db_url in Scaffold.Backend_Parameters :
        db_url = Scaffold.Backend_Parameters [db_url].strip ("'")
    db_opt = "-db_url=%s" % db_url
    Scaffold (["create", db_opt])
    Scaffold (["shell", "-wsgi", db_opt])
### __END__ GTW.__test__.SAW_ATW
