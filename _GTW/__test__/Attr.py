# -*- coding: iso-8859-15 -*-
# Copyright (C) 2013 Mag. Christian Tanzer All rights reserved
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
#    GTW.__test__.Attr
#
# Purpose
#    Test attribute framework
#
# Revision Dates
#    11-Jun-2013 (CT) Creation
#    ««revision-date»»···
#--

from   __future__ import division, print_function
from   __future__ import absolute_import, unicode_literals

### enforce import order
import _GTW._OMP._Auth.import_Auth
import _GTW._OMP._PAP.import_PAP
import _GTW._OMP._EVT.import_EVT
import _GTW._OMP._SWP.import_SWP
import _GTW._OMP._SRM.import_SRM

from   _GTW.__test__.model import *
from   _MOM.inspect        import children_trans_iter

_test_e_type = """
    >>> scope = Scaffold.scope (%(p1)s, %(n1)s) # doctest:+ELLIPSIS
    Creating new scope MOMT__...

    >>> MOM = scope.MOM
    >>> nl  = pyk.unichr (10)

    >>> a_map = TFL.defaultdict (list)
    >>> for T, l in children_trans_iter (MOM.Id_Entity) :
    ...     ET = T.E_Type
    ...     for name, kind in sorted (pyk.iteritems (ET.attributes)) :
    ...         if kind.q_able and (ET.children_np or not ET.is_partial) :
    ...             if not ET.type_name.startswith ("Auth") :
    ...                 k  = (name, kind.DET_Root)
    ...                 a_map [k].append ((kind, ET))

    >>> for (name, DT), xs in sorted (pyk.iteritems (a_map)) :
    ...     if len (xs) > 1 :
    ...         print ("%%s [%%s]" %% (name, DT))
    ...         for kind, ET in sorted (xs, key = lambda x : x [1].i_rank) :
    ...             flag = "*" if not ET.is_partial else ""
    ...             print ("    %%-30s%%-2s %%s" %% (ET.type_name, flag, kind.e_type.type_name))
    boat_class [SRM.Regatta]
        SRM.Regatta                      SRM.Regatta
        SRM.Regatta_C                 *  SRM.Regatta_C
        SRM.Regatta_H                 *  SRM.Regatta_H
    contents [SWP.Page_Mixin]
        SWP.Page                      *  SWP.Page_Mixin
        SWP.Page_Y                    *  SWP.Page_Mixin
        SWP.Clip_X                    *  SWP.Page_Mixin
        SRM.Page                      *  SWP.Page_Mixin
    date [SWP.Object_PN]
        SWP.Object_PN                    SWP.Object_PN
        SWP.Page                      *  SWP.Object_PN
        SWP.Page_Y                    *  SWP.Object_PN
        SWP.Clip_X                    *  SWP.Object_PN
        SWP.Gallery                   *  SWP.Object_PN
        SRM.Page                      *  SWP.Object_PN
    desc [PAP.Property]
        PAP.Property                     PAP.Property
        PAP.Address                   *  PAP.Address
        PAP.Email                     *  PAP.Email
        PAP.Phone                     *  PAP.Phone
        PAP.Url                       *  PAP.Url
    desc [PAP.Subject_has_Property]
        PAP.Subject_has_Property         PAP.Subject_has_Property
        PAP.Subject_has_Address          PAP.Subject_has_Property
        PAP.Subject_has_Email            PAP.Subject_has_Property
        PAP.Subject_has_Phone            PAP.Subject_has_Property
        PAP.Subject_has_Url              PAP.Subject_has_Property
        PAP.Company_has_Url           *  PAP.Subject_has_Property
        PAP.Person_has_Url            *  PAP.Subject_has_Property
        PAP.Company_has_Phone         *  PAP.Subject_has_Property
        PAP.Person_has_Phone          *  PAP.Subject_has_Property
        PAP.Company_has_Email         *  PAP.Subject_has_Property
        PAP.Person_has_Email          *  PAP.Subject_has_Property
        PAP.Company_has_Address       *  PAP.Subject_has_Property
        PAP.Person_has_Address        *  PAP.Subject_has_Property
    discards [SRM.Regatta]
        SRM.Regatta                      SRM.Regatta
        SRM.Regatta_C                 *  SRM.Regatta
        SRM.Regatta_H                 *  SRM.Regatta
    electric [MOM.Id_Entity]
        MOM.Id_Entity                    MOM.Id_Entity
        MOM.Link                         MOM.Id_Entity
        MOM.Link1                        MOM.Id_Entity
        MOM._MOM_Link_n_                 MOM.Id_Entity
        MOM.Link2                        MOM.Id_Entity
        MOM.Object                       MOM.Id_Entity
        MOM.Named_Object                 MOM.Id_Entity
        PAP.Id_Entity                    MOM.Id_Entity
        PAP.Link1                        MOM.Id_Entity
        PAP.Link2                        MOM.Id_Entity
        PAP.Object                       MOM.Id_Entity
        PAP.Property                     MOM.Id_Entity
        PAP.Address                   *  MOM.Id_Entity
        PAP.Subject                      MOM.Id_Entity
        PAP.Legal_Entity                 MOM.Id_Entity
        PAP.Company                   *  MOM.Id_Entity
        PAP.Email                     *  MOM.Id_Entity
        PAP.Phone                     *  MOM.Id_Entity
        PAP.Person                    *  MOM.Id_Entity
        PAP.Url                       *  MOM.Id_Entity
        PAP.Address_Position          *  MOM.Id_Entity
        PAP.Subject_has_Property         MOM.Id_Entity
        PAP.Person_has_Account        *  MOM.Id_Entity
        EVT.Id_Entity                    MOM.Id_Entity
        EVT.Link1                        MOM.Id_Entity
        EVT.Object                       MOM.Id_Entity
        EVT.Calendar                  *  MOM.Id_Entity
        SWP.Id_Entity                    MOM.Id_Entity
        SWP.Link1                        MOM.Id_Entity
        SWP.Object                       MOM.Id_Entity
        SWP.Object_PN                    MOM.Id_Entity
        SWP.Page                      *  MOM.Id_Entity
        SWP.Page_Y                    *  MOM.Id_Entity
        EVT.Event                     *  MOM.Id_Entity
        EVT._Recurrence_Mixin_           MOM.Id_Entity
        EVT.Recurrence_Spec           *  MOM.Id_Entity
        EVT.Recurrence_Rule           *  MOM.Id_Entity
        SWP.Clip_O                    *  MOM.Id_Entity
        SWP.Clip_X                    *  MOM.Id_Entity
        SWP.Gallery                   *  MOM.Id_Entity
        SWP.Picture                   *  MOM.Id_Entity
        SRM.Id_Entity                    MOM.Id_Entity
        SRM.Link1                        MOM.Id_Entity
        SRM.Link2                        MOM.Id_Entity
        SRM.Object                       MOM.Id_Entity
        SRM._Boat_Class_                 MOM.Id_Entity
        SRM.Boat_Class                *  MOM.Id_Entity
        SRM.Handicap                  *  MOM.Id_Entity
        SRM.Boat                      *  MOM.Id_Entity
        SRM.Club                      *  MOM.Id_Entity
        SRM.Regatta_Event             *  MOM.Id_Entity
        SRM.Page                      *  MOM.Id_Entity
        SRM.Regatta                      MOM.Id_Entity
        SRM.Regatta_C                 *  MOM.Id_Entity
        SRM.Regatta_H                 *  MOM.Id_Entity
        SRM.Sailor                    *  MOM.Id_Entity
        SRM.Boat_in_Regatta           *  MOM.Id_Entity
        SRM.Race_Result               *  MOM.Id_Entity
        SRM.Team                      *  MOM.Id_Entity
        SRM.Crew_Member               *  MOM.Id_Entity
        SRM.Team_has_Boat_in_Regatta  *  MOM.Id_Entity
        PAP.Subject_has_Address          MOM.Id_Entity
        PAP.Subject_has_Email            MOM.Id_Entity
        PAP.Subject_has_Phone            MOM.Id_Entity
        PAP.Subject_has_Url              MOM.Id_Entity
        PAP.Company_has_Url           *  MOM.Id_Entity
        PAP.Person_has_Url            *  MOM.Id_Entity
        PAP.Company_has_Phone         *  MOM.Id_Entity
        PAP.Person_has_Phone          *  MOM.Id_Entity
        PAP.Company_has_Email         *  MOM.Id_Entity
        PAP.Person_has_Email          *  MOM.Id_Entity
        PAP.Company_has_Address       *  MOM.Id_Entity
        PAP.Person_has_Address        *  MOM.Id_Entity
    extension [PAP.Subject_has_Phone]
        PAP.Subject_has_Phone            PAP.Subject_has_Phone
        PAP.Company_has_Phone         *  PAP.Subject_has_Phone
        PAP.Person_has_Phone          *  PAP.Subject_has_Phone
    format [SWP.Page_Mixin]
        SWP.Page                      *  SWP.Page_Mixin
        SWP.Page_Y                    *  SWP.Page_Mixin
        SWP.Clip_X                    *  SWP.Page_Mixin
        SRM.Page                      *  SWP.Page_Mixin
    head_line [SWP.Page_Mixin]
        SWP.Page                      *  SWP.Page_Mixin
        SWP.Page_Y                    *  SWP.Page_Mixin
        SWP.Clip_X                    *  SWP.Page_Mixin
        SRM.Page                      *  SWP.Page_Mixin
    hidden [SWP.Page_Mixin]
        SWP.Page                      *  SWP.Page_Mixin
        SWP.Page_Y                    *  SWP.Page_Mixin
        SWP.Clip_X                    *  SWP.Page_Mixin
        SRM.Page                      *  SWP.Page_Mixin
    is_cancelled [SRM.Regatta]
        SRM.Regatta                      SRM.Regatta
        SRM.Regatta_C                 *  SRM.Regatta
        SRM.Regatta_H                 *  SRM.Regatta
    kind [SRM.Regatta]
        SRM.Regatta                      SRM.Regatta
        SRM.Regatta_C                 *  SRM.Regatta
        SRM.Regatta_H                 *  SRM.Regatta
    last_cid [MOM.Id_Entity]
        MOM.Id_Entity                    MOM.Id_Entity
        MOM.Link                         MOM.Id_Entity
        MOM.Link1                        MOM.Id_Entity
        MOM._MOM_Link_n_                 MOM.Id_Entity
        MOM.Link2                        MOM.Id_Entity
        MOM.Object                       MOM.Id_Entity
        MOM.Named_Object                 MOM.Id_Entity
        PAP.Id_Entity                    MOM.Id_Entity
        PAP.Link1                        MOM.Id_Entity
        PAP.Link2                        MOM.Id_Entity
        PAP.Object                       MOM.Id_Entity
        PAP.Property                     MOM.Id_Entity
        PAP.Address                   *  MOM.Id_Entity
        PAP.Subject                      MOM.Id_Entity
        PAP.Legal_Entity                 MOM.Id_Entity
        PAP.Company                   *  MOM.Id_Entity
        PAP.Email                     *  MOM.Id_Entity
        PAP.Phone                     *  MOM.Id_Entity
        PAP.Person                    *  MOM.Id_Entity
        PAP.Url                       *  MOM.Id_Entity
        PAP.Address_Position          *  MOM.Id_Entity
        PAP.Subject_has_Property         MOM.Id_Entity
        PAP.Person_has_Account        *  MOM.Id_Entity
        EVT.Id_Entity                    MOM.Id_Entity
        EVT.Link1                        MOM.Id_Entity
        EVT.Object                       MOM.Id_Entity
        EVT.Calendar                  *  MOM.Id_Entity
        SWP.Id_Entity                    MOM.Id_Entity
        SWP.Link1                        MOM.Id_Entity
        SWP.Object                       MOM.Id_Entity
        SWP.Object_PN                    MOM.Id_Entity
        SWP.Page                      *  MOM.Id_Entity
        SWP.Page_Y                    *  MOM.Id_Entity
        EVT.Event                     *  MOM.Id_Entity
        EVT.Event_occurs              *  MOM.Id_Entity
        EVT._Recurrence_Mixin_           MOM.Id_Entity
        EVT.Recurrence_Spec           *  MOM.Id_Entity
        EVT.Recurrence_Rule           *  MOM.Id_Entity
        SWP.Clip_O                    *  MOM.Id_Entity
        SWP.Clip_X                    *  MOM.Id_Entity
        SWP.Gallery                   *  MOM.Id_Entity
        SWP.Picture                   *  MOM.Id_Entity
        SRM.Id_Entity                    MOM.Id_Entity
        SRM.Link1                        MOM.Id_Entity
        SRM.Link2                        MOM.Id_Entity
        SRM.Object                       MOM.Id_Entity
        SRM._Boat_Class_                 MOM.Id_Entity
        SRM.Boat_Class                *  MOM.Id_Entity
        SRM.Handicap                  *  MOM.Id_Entity
        SRM.Boat                      *  MOM.Id_Entity
        SRM.Club                      *  MOM.Id_Entity
        SRM.Regatta_Event             *  MOM.Id_Entity
        SRM.Page                      *  MOM.Id_Entity
        SRM.Regatta                      MOM.Id_Entity
        SRM.Regatta_C                 *  MOM.Id_Entity
        SRM.Regatta_H                 *  MOM.Id_Entity
        SRM.Sailor                    *  MOM.Id_Entity
        SRM.Boat_in_Regatta           *  MOM.Id_Entity
        SRM.Race_Result               *  MOM.Id_Entity
        SRM.Team                      *  MOM.Id_Entity
        SRM.Crew_Member               *  MOM.Id_Entity
        SRM.Team_has_Boat_in_Regatta  *  MOM.Id_Entity
        PAP.Subject_has_Address          MOM.Id_Entity
        PAP.Subject_has_Email            MOM.Id_Entity
        PAP.Subject_has_Phone            MOM.Id_Entity
        PAP.Subject_has_Url              MOM.Id_Entity
        PAP.Company_has_Url           *  MOM.Id_Entity
        PAP.Person_has_Url            *  MOM.Id_Entity
        PAP.Company_has_Phone         *  MOM.Id_Entity
        PAP.Person_has_Phone          *  MOM.Id_Entity
        PAP.Company_has_Email         *  MOM.Id_Entity
        PAP.Person_has_Email          *  MOM.Id_Entity
        PAP.Company_has_Address       *  MOM.Id_Entity
        PAP.Person_has_Address        *  MOM.Id_Entity
    left [MOM.Link]
        MOM.Link                         MOM.Link
        MOM.Link1                        MOM.Link1
        MOM._MOM_Link_n_                 MOM.Link
        MOM.Link2                        MOM.Link
        PAP.Link1                        MOM.Link1
        PAP.Link2                        MOM.Link
        PAP.Address_Position          *  PAP.Address_Position
        PAP.Subject_has_Property         PAP.Subject_has_Property
        PAP.Person_has_Account        *  PAP.Person_has_Account
        EVT.Link1                        MOM.Link1
        SWP.Link1                        MOM.Link1
        EVT.Event                     *  EVT.Event
        EVT.Event_occurs              *  EVT.Event_occurs
        EVT._Recurrence_Mixin_           MOM.Link1
        EVT.Recurrence_Spec           *  EVT.Recurrence_Spec
        EVT.Recurrence_Rule           *  EVT.Recurrence_Rule
        SWP.Clip_O                    *  SWP.Clip_O
        SWP.Picture                   *  SWP.Picture
        SRM.Link1                        MOM.Link1
        SRM.Link2                        MOM.Link
        SRM.Boat                      *  SRM.Boat
        SRM.Regatta                      SRM.Regatta
        SRM.Regatta_C                 *  SRM.Regatta
        SRM.Regatta_H                 *  SRM.Regatta
        SRM.Sailor                    *  SRM.Sailor
        SRM.Boat_in_Regatta           *  SRM.Boat_in_Regatta
        SRM.Race_Result               *  SRM.Race_Result
        SRM.Team                      *  SRM.Team
        SRM.Crew_Member               *  SRM.Crew_Member
        SRM.Team_has_Boat_in_Regatta  *  SRM.Team_has_Boat_in_Regatta
        PAP.Subject_has_Address          PAP.Subject_has_Address
        PAP.Subject_has_Email            PAP.Subject_has_Email
        PAP.Subject_has_Phone            PAP.Subject_has_Phone
        PAP.Subject_has_Url              PAP.Subject_has_Url
        PAP.Company_has_Url           *  PAP.Company_has_Url
        PAP.Person_has_Url            *  PAP.Person_has_Url
        PAP.Company_has_Phone         *  PAP.Company_has_Phone
        PAP.Person_has_Phone          *  PAP.Person_has_Phone
        PAP.Company_has_Email         *  PAP.Company_has_Email
        PAP.Person_has_Email          *  PAP.Person_has_Email
        PAP.Company_has_Address       *  PAP.Company_has_Address
        PAP.Person_has_Address        *  PAP.Person_has_Address
    lifetime [PAP.Subject]
        PAP.Subject                      PAP.Subject
        PAP.Legal_Entity                 PAP.Subject
        PAP.Company                   *  PAP.Subject
        PAP.Person                    *  PAP.Subject
    name [PAP.Legal_Entity]
        PAP.Legal_Entity                 PAP.Legal_Entity
        PAP.Company                   *  PAP.Company
    name [SRM._Boat_Class_]
        SRM._Boat_Class_                 SRM._Boat_Class_
        SRM.Boat_Class                *  SRM.Boat_Class
        SRM.Handicap                  *  SRM.Handicap
    perma_name [SRM.Regatta]
        SRM.Regatta                      SRM.Regatta
        SRM.Regatta_C                 *  SRM.Regatta
        SRM.Regatta_H                 *  SRM.Regatta
    perma_name [SWP.Object_PN]
        SWP.Object_PN                    SWP.Object_PN
        SWP.Page                      *  SWP.Object_PN
        SWP.Page_Y                    *  SWP.Object_PN
        SWP.Clip_X                    *  SWP.Object_PN
        SWP.Gallery                   *  SWP.Object_PN
        SRM.Page                      *  SWP.Object_PN
    pid [MOM.Id_Entity]
        MOM.Id_Entity                    MOM.Id_Entity
        MOM.Link                         MOM.Id_Entity
        MOM.Link1                        MOM.Id_Entity
        MOM._MOM_Link_n_                 MOM.Id_Entity
        MOM.Link2                        MOM.Id_Entity
        MOM.Object                       MOM.Id_Entity
        MOM.Named_Object                 MOM.Id_Entity
        PAP.Id_Entity                    MOM.Id_Entity
        PAP.Link1                        MOM.Id_Entity
        PAP.Link2                        MOM.Id_Entity
        PAP.Object                       MOM.Id_Entity
        PAP.Property                     MOM.Id_Entity
        PAP.Address                   *  MOM.Id_Entity
        PAP.Subject                      MOM.Id_Entity
        PAP.Legal_Entity                 MOM.Id_Entity
        PAP.Company                   *  MOM.Id_Entity
        PAP.Email                     *  MOM.Id_Entity
        PAP.Phone                     *  MOM.Id_Entity
        PAP.Person                    *  MOM.Id_Entity
        PAP.Url                       *  MOM.Id_Entity
        PAP.Address_Position          *  MOM.Id_Entity
        PAP.Subject_has_Property         MOM.Id_Entity
        PAP.Person_has_Account        *  MOM.Id_Entity
        EVT.Id_Entity                    MOM.Id_Entity
        EVT.Link1                        MOM.Id_Entity
        EVT.Object                       MOM.Id_Entity
        EVT.Calendar                  *  MOM.Id_Entity
        SWP.Id_Entity                    MOM.Id_Entity
        SWP.Link1                        MOM.Id_Entity
        SWP.Object                       MOM.Id_Entity
        SWP.Object_PN                    MOM.Id_Entity
        SWP.Page                      *  MOM.Id_Entity
        SWP.Page_Y                    *  MOM.Id_Entity
        EVT.Event                     *  MOM.Id_Entity
        EVT.Event_occurs              *  MOM.Id_Entity
        EVT._Recurrence_Mixin_           MOM.Id_Entity
        EVT.Recurrence_Spec           *  MOM.Id_Entity
        EVT.Recurrence_Rule           *  MOM.Id_Entity
        SWP.Clip_O                    *  MOM.Id_Entity
        SWP.Clip_X                    *  MOM.Id_Entity
        SWP.Gallery                   *  MOM.Id_Entity
        SWP.Picture                   *  MOM.Id_Entity
        SRM.Id_Entity                    MOM.Id_Entity
        SRM.Link1                        MOM.Id_Entity
        SRM.Link2                        MOM.Id_Entity
        SRM.Object                       MOM.Id_Entity
        SRM._Boat_Class_                 MOM.Id_Entity
        SRM.Boat_Class                *  MOM.Id_Entity
        SRM.Handicap                  *  MOM.Id_Entity
        SRM.Boat                      *  MOM.Id_Entity
        SRM.Club                      *  MOM.Id_Entity
        SRM.Regatta_Event             *  MOM.Id_Entity
        SRM.Page                      *  MOM.Id_Entity
        SRM.Regatta                      MOM.Id_Entity
        SRM.Regatta_C                 *  MOM.Id_Entity
        SRM.Regatta_H                 *  MOM.Id_Entity
        SRM.Sailor                    *  MOM.Id_Entity
        SRM.Boat_in_Regatta           *  MOM.Id_Entity
        SRM.Race_Result               *  MOM.Id_Entity
        SRM.Team                      *  MOM.Id_Entity
        SRM.Crew_Member               *  MOM.Id_Entity
        SRM.Team_has_Boat_in_Regatta  *  MOM.Id_Entity
        PAP.Subject_has_Address          MOM.Id_Entity
        PAP.Subject_has_Email            MOM.Id_Entity
        PAP.Subject_has_Phone            MOM.Id_Entity
        PAP.Subject_has_Url              MOM.Id_Entity
        PAP.Company_has_Url           *  MOM.Id_Entity
        PAP.Person_has_Url            *  MOM.Id_Entity
        PAP.Company_has_Phone         *  MOM.Id_Entity
        PAP.Person_has_Phone          *  MOM.Id_Entity
        PAP.Company_has_Email         *  MOM.Id_Entity
        PAP.Person_has_Email          *  MOM.Id_Entity
        PAP.Company_has_Address       *  MOM.Id_Entity
        PAP.Person_has_Address        *  MOM.Id_Entity
    prio [SWP.Page_Mixin]
        SWP.Page                      *  SWP.Page_Mixin
        SWP.Page_Y                    *  SWP.Page_Mixin
        SWP.Clip_X                    *  SWP.Page_Mixin
        SRM.Page                      *  SWP.Page_Mixin
    races [SRM.Regatta]
        SRM.Regatta                      SRM.Regatta
        SRM.Regatta_C                 *  SRM.Regatta
        SRM.Regatta_H                 *  SRM.Regatta
    result [SRM.Regatta]
        SRM.Regatta                      SRM.Regatta
        SRM.Regatta_C                 *  SRM.Regatta
        SRM.Regatta_H                 *  SRM.Regatta
    right [MOM._MOM_Link_n_]
        MOM._MOM_Link_n_                 MOM._MOM_Link_n_
        MOM.Link2                        MOM._MOM_Link_n_
        PAP.Link2                        MOM._MOM_Link_n_
        PAP.Subject_has_Property         PAP.Subject_has_Property
        PAP.Person_has_Account        *  PAP.Person_has_Account
        SRM.Link2                        MOM._MOM_Link_n_
        SRM.Boat_in_Regatta           *  SRM.Boat_in_Regatta
        SRM.Crew_Member               *  SRM.Crew_Member
        SRM.Team_has_Boat_in_Regatta  *  SRM.Team_has_Boat_in_Regatta
        PAP.Subject_has_Address          PAP.Subject_has_Address
        PAP.Subject_has_Email            PAP.Subject_has_Email
        PAP.Subject_has_Phone            PAP.Subject_has_Phone
        PAP.Subject_has_Url              PAP.Subject_has_Url
        PAP.Company_has_Url           *  PAP.Company_has_Url
        PAP.Person_has_Url            *  PAP.Person_has_Url
        PAP.Company_has_Phone         *  PAP.Company_has_Phone
        PAP.Person_has_Phone          *  PAP.Person_has_Phone
        PAP.Company_has_Email         *  PAP.Company_has_Email
        PAP.Person_has_Email          *  PAP.Person_has_Email
        PAP.Company_has_Address       *  PAP.Company_has_Address
        PAP.Person_has_Address        *  PAP.Person_has_Address
    short_name [PAP.Legal_Entity]
        PAP.Legal_Entity                 PAP.Legal_Entity
        PAP.Company                   *  PAP.Company
    short_title [SWP.Object_PN]
        SWP.Object_PN                    SWP.Object_PN
        SWP.Page                      *  SWP.Object_PN
        SWP.Page_Y                    *  SWP.Object_PN
        SWP.Clip_X                    *  SWP.Object_PN
        SWP.Gallery                   *  SWP.Object_PN
    text [SWP.Page_Mixin]
        SWP.Page                      *  SWP.Page_Mixin
        SWP.Page_Y                    *  SWP.Page_Mixin
        SWP.Clip_X                    *  SWP.Clip_X
        SRM.Page                      *  SWP.Page_Mixin
    title [SWP.Object_PN]
        SWP.Object_PN                    SWP.Object_PN
        SWP.Page                      *  SWP.Object_PN
        SWP.Page_Y                    *  SWP.Object_PN
        SWP.Clip_X                    *  SWP.Clip_X
        SWP.Gallery                   *  SWP.Object_PN
    type_name [MOM.Id_Entity]
        MOM.Id_Entity                    MOM.Id_Entity
        MOM.Link                         MOM.Id_Entity
        MOM.Link1                        MOM.Id_Entity
        MOM._MOM_Link_n_                 MOM.Id_Entity
        MOM.Link2                        MOM.Id_Entity
        MOM.Object                       MOM.Id_Entity
        MOM.Named_Object                 MOM.Id_Entity
        PAP.Id_Entity                    MOM.Id_Entity
        PAP.Link1                        MOM.Id_Entity
        PAP.Link2                        MOM.Id_Entity
        PAP.Object                       MOM.Id_Entity
        PAP.Property                     MOM.Id_Entity
        PAP.Address                   *  MOM.Id_Entity
        PAP.Subject                      MOM.Id_Entity
        PAP.Legal_Entity                 MOM.Id_Entity
        PAP.Company                   *  MOM.Id_Entity
        PAP.Email                     *  MOM.Id_Entity
        PAP.Phone                     *  MOM.Id_Entity
        PAP.Person                    *  MOM.Id_Entity
        PAP.Url                       *  MOM.Id_Entity
        PAP.Address_Position          *  MOM.Id_Entity
        PAP.Subject_has_Property         MOM.Id_Entity
        PAP.Person_has_Account        *  MOM.Id_Entity
        EVT.Id_Entity                    MOM.Id_Entity
        EVT.Link1                        MOM.Id_Entity
        EVT.Object                       MOM.Id_Entity
        EVT.Calendar                  *  MOM.Id_Entity
        SWP.Id_Entity                    MOM.Id_Entity
        SWP.Link1                        MOM.Id_Entity
        SWP.Object                       MOM.Id_Entity
        SWP.Object_PN                    MOM.Id_Entity
        SWP.Page                      *  MOM.Id_Entity
        SWP.Page_Y                    *  MOM.Id_Entity
        EVT.Event                     *  MOM.Id_Entity
        EVT.Event_occurs              *  MOM.Id_Entity
        EVT._Recurrence_Mixin_           MOM.Id_Entity
        EVT.Recurrence_Spec           *  MOM.Id_Entity
        EVT.Recurrence_Rule           *  MOM.Id_Entity
        SWP.Clip_O                    *  MOM.Id_Entity
        SWP.Clip_X                    *  MOM.Id_Entity
        SWP.Gallery                   *  MOM.Id_Entity
        SWP.Picture                   *  MOM.Id_Entity
        SRM.Id_Entity                    MOM.Id_Entity
        SRM.Link1                        MOM.Id_Entity
        SRM.Link2                        MOM.Id_Entity
        SRM.Object                       MOM.Id_Entity
        SRM._Boat_Class_                 MOM.Id_Entity
        SRM.Boat_Class                *  MOM.Id_Entity
        SRM.Handicap                  *  MOM.Id_Entity
        SRM.Boat                      *  MOM.Id_Entity
        SRM.Club                      *  MOM.Id_Entity
        SRM.Regatta_Event             *  MOM.Id_Entity
        SRM.Page                      *  MOM.Id_Entity
        SRM.Regatta                      MOM.Id_Entity
        SRM.Regatta_C                 *  MOM.Id_Entity
        SRM.Regatta_H                 *  MOM.Id_Entity
        SRM.Sailor                    *  MOM.Id_Entity
        SRM.Boat_in_Regatta           *  MOM.Id_Entity
        SRM.Race_Result               *  MOM.Id_Entity
        SRM.Team                      *  MOM.Id_Entity
        SRM.Crew_Member               *  MOM.Id_Entity
        SRM.Team_has_Boat_in_Regatta  *  MOM.Id_Entity
        PAP.Subject_has_Address          MOM.Id_Entity
        PAP.Subject_has_Email            MOM.Id_Entity
        PAP.Subject_has_Phone            MOM.Id_Entity
        PAP.Subject_has_Url              MOM.Id_Entity
        PAP.Company_has_Url           *  MOM.Id_Entity
        PAP.Person_has_Url            *  MOM.Id_Entity
        PAP.Company_has_Phone         *  MOM.Id_Entity
        PAP.Person_has_Phone          *  MOM.Id_Entity
        PAP.Company_has_Email         *  MOM.Id_Entity
        PAP.Person_has_Email          *  MOM.Id_Entity
        PAP.Company_has_Address       *  MOM.Id_Entity
        PAP.Person_has_Address        *  MOM.Id_Entity


    >>> name, DT = ("left", "MOM.Link")
    >>> xs       = a_map [name, DT]
    >>> for kind, ET in sorted (xs, key = lambda x : x [1].i_rank) :
    ...     print ("%%-30s %%-30s %%s" %% (ET.type_name, kind.attr.DET, kind.attr.DET_Base))
    MOM.Link                       MOM.Link                       None
    MOM.Link1                      MOM.Link1                      MOM.Link
    MOM._MOM_Link_n_               MOM.Link                       None
    MOM.Link2                      MOM.Link                       None
    PAP.Link1                      MOM.Link1                      MOM.Link
    PAP.Link2                      MOM.Link                       None
    PAP.Address_Position           PAP.Address_Position           MOM.Link1
    PAP.Subject_has_Property       PAP.Subject_has_Property       MOM.Link
    PAP.Person_has_Account         PAP.Person_has_Account         MOM.Link
    EVT.Link1                      MOM.Link1                      MOM.Link
    SWP.Link1                      MOM.Link1                      MOM.Link
    EVT.Event                      EVT.Event                      MOM.Link1
    EVT.Event_occurs               EVT.Event_occurs               MOM.Link1
    EVT._Recurrence_Mixin_         MOM.Link1                      MOM.Link
    EVT.Recurrence_Spec            EVT.Recurrence_Spec            MOM.Link1
    EVT.Recurrence_Rule            EVT.Recurrence_Rule            MOM.Link1
    SWP.Clip_O                     SWP.Clip_O                     MOM.Link1
    SWP.Picture                    SWP.Picture                    MOM.Link1
    SRM.Link1                      MOM.Link1                      MOM.Link
    SRM.Link2                      MOM.Link                       None
    SRM.Boat                       SRM.Boat                       MOM.Link1
    SRM.Regatta                    SRM.Regatta                    MOM.Link1
    SRM.Regatta_C                  SRM.Regatta                    MOM.Link1
    SRM.Regatta_H                  SRM.Regatta                    MOM.Link1
    SRM.Sailor                     SRM.Sailor                     MOM.Link1
    SRM.Boat_in_Regatta            SRM.Boat_in_Regatta            MOM.Link
    SRM.Race_Result                SRM.Race_Result                MOM.Link1
    SRM.Team                       SRM.Team                       MOM.Link1
    SRM.Crew_Member                SRM.Crew_Member                MOM.Link
    SRM.Team_has_Boat_in_Regatta   SRM.Team_has_Boat_in_Regatta   MOM.Link
    PAP.Subject_has_Address        PAP.Subject_has_Property       MOM.Link
    PAP.Subject_has_Email          PAP.Subject_has_Property       MOM.Link
    PAP.Subject_has_Phone          PAP.Subject_has_Property       MOM.Link
    PAP.Subject_has_Url            PAP.Subject_has_Property       MOM.Link
    PAP.Company_has_Url            PAP.Company_has_Url            PAP.Subject_has_Property
    PAP.Person_has_Url             PAP.Person_has_Url             PAP.Subject_has_Property
    PAP.Company_has_Phone          PAP.Company_has_Phone          PAP.Subject_has_Property
    PAP.Person_has_Phone           PAP.Person_has_Phone           PAP.Subject_has_Property
    PAP.Company_has_Email          PAP.Company_has_Email          PAP.Subject_has_Property
    PAP.Person_has_Email           PAP.Person_has_Email           PAP.Subject_has_Property
    PAP.Company_has_Address        PAP.Company_has_Address        PAP.Subject_has_Property
    PAP.Person_has_Address         PAP.Person_has_Address         PAP.Subject_has_Property

    >>> name, DT = ("left", "MOM.Link")
    >>> xs       = a_map [name, DT]
    >>> for ak, ET in sorted (xs, key = lambda x : x [1].i_rank) : ### left
    ...   if len (ET.Roles) > 1 :
    ...     db = ak.det_base.type_name if ak.det_base else None
    ...     dr = ak.det_root.type_name if ak.det_root else None
    ...     print ("%%-30s %%-30s %%s" %% (ET.type_name, ak.e_type.type_name, db))
    MOM._MOM_Link_n_               MOM.Link                       None
    MOM.Link2                      MOM.Link                       None
    PAP.Link2                      MOM.Link                       None
    PAP.Subject_has_Property       PAP.Subject_has_Property       MOM.Link
    PAP.Person_has_Account         PAP.Person_has_Account         MOM.Link
    SRM.Link2                      MOM.Link                       None
    SRM.Boat_in_Regatta            SRM.Boat_in_Regatta            MOM.Link
    SRM.Crew_Member                SRM.Crew_Member                MOM.Link
    SRM.Team_has_Boat_in_Regatta   SRM.Team_has_Boat_in_Regatta   MOM.Link
    PAP.Subject_has_Address        PAP.Subject_has_Address        MOM.Link
    PAP.Subject_has_Email          PAP.Subject_has_Email          MOM.Link
    PAP.Subject_has_Phone          PAP.Subject_has_Phone          MOM.Link
    PAP.Subject_has_Url            PAP.Subject_has_Url            MOM.Link
    PAP.Company_has_Url            PAP.Company_has_Url            PAP.Subject_has_Property
    PAP.Person_has_Url             PAP.Person_has_Url             PAP.Subject_has_Property
    PAP.Company_has_Phone          PAP.Company_has_Phone          PAP.Subject_has_Property
    PAP.Person_has_Phone           PAP.Person_has_Phone           PAP.Subject_has_Property
    PAP.Company_has_Email          PAP.Company_has_Email          PAP.Subject_has_Property
    PAP.Person_has_Email           PAP.Person_has_Email           PAP.Subject_has_Property
    PAP.Company_has_Address        PAP.Company_has_Address        PAP.Subject_has_Property
    PAP.Person_has_Address         PAP.Person_has_Address         PAP.Subject_has_Property

    >>> name, DT = ("right", "MOM._MOM_Link_n_")
    >>> xs       = a_map [name, DT]
    >>> for ak, ET in sorted (xs, key = lambda x : x [1].i_rank) : ### right
    ...     db = ak.det_base.type_name if ak.det_base else None
    ...     dr = ak.det_root.type_name if ak.det_root else None
    ...     print ("%%-30s %%-30s %%s" %% (ET.type_name, ak.e_type.type_name, db))
    MOM._MOM_Link_n_               MOM._MOM_Link_n_               None
    MOM.Link2                      MOM._MOM_Link_n_               None
    PAP.Link2                      MOM._MOM_Link_n_               None
    PAP.Subject_has_Property       PAP.Subject_has_Property       MOM._MOM_Link_n_
    PAP.Person_has_Account         PAP.Person_has_Account         MOM._MOM_Link_n_
    SRM.Link2                      MOM._MOM_Link_n_               None
    SRM.Boat_in_Regatta            SRM.Boat_in_Regatta            MOM._MOM_Link_n_
    SRM.Crew_Member                SRM.Crew_Member                MOM._MOM_Link_n_
    SRM.Team_has_Boat_in_Regatta   SRM.Team_has_Boat_in_Regatta   MOM._MOM_Link_n_
    PAP.Subject_has_Address        PAP.Subject_has_Address        PAP.Subject_has_Property
    PAP.Subject_has_Email          PAP.Subject_has_Email          PAP.Subject_has_Property
    PAP.Subject_has_Phone          PAP.Subject_has_Phone          PAP.Subject_has_Property
    PAP.Subject_has_Url            PAP.Subject_has_Url            PAP.Subject_has_Property
    PAP.Company_has_Url            PAP.Company_has_Url            PAP.Subject_has_Property
    PAP.Person_has_Url             PAP.Person_has_Url             PAP.Subject_has_Property
    PAP.Company_has_Phone          PAP.Company_has_Phone          PAP.Subject_has_Property
    PAP.Person_has_Phone           PAP.Person_has_Phone           PAP.Subject_has_Property
    PAP.Company_has_Email          PAP.Company_has_Email          PAP.Subject_has_Property
    PAP.Person_has_Email           PAP.Person_has_Email           PAP.Subject_has_Property
    PAP.Company_has_Address        PAP.Company_has_Address        PAP.Subject_has_Property
    PAP.Person_has_Address         PAP.Person_has_Address         PAP.Subject_has_Property

"""

_test_types = """
    >>> scope = Scaffold.scope (%(p1)s, %(n1)s) # doctest:+ELLIPSIS
    Creating new scope MOMT__...

    >>> MOM = scope.MOM
    >>> for T, l in children_trans_iter (MOM.Id_Entity) :
    ...     ET = T.E_Type
    ...     print ("%%s%%s" %% ("  " * l, ET.type_name))
    MOM.Id_Entity
      MOM.Link
        MOM.Link1
          Auth.Link1
            Auth._Account_Action_
              Auth.Account_Activation
              Auth.Account_Password_Change_Required
              Auth._Account_Token_Action_
                Auth.Account_EMail_Verification
                Auth.Account_Password_Reset
          PAP.Link1
            PAP.Address_Position
          EVT.Link1
            EVT.Event
            EVT.Event_occurs
            EVT._Recurrence_Mixin_
              EVT.Recurrence_Spec
              EVT.Recurrence_Rule
          SWP.Link1
            SWP.Clip_O
            SWP.Picture
          SRM.Link1
            SRM.Boat
            SRM.Regatta
              SRM.Regatta_C
              SRM.Regatta_H
            SRM.Sailor
            SRM.Race_Result
            SRM.Team
        MOM._MOM_Link_n_
          MOM.Link2
            Auth.Link2
              Auth.Account_in_Group
            PAP.Link2
              PAP.Subject_has_Property
                PAP.Subject_has_Address
                  PAP.Company_has_Address
                  PAP.Person_has_Address
                PAP.Subject_has_Email
                  PAP.Company_has_Email
                  PAP.Person_has_Email
                PAP.Subject_has_Phone
                  PAP.Company_has_Phone
                  PAP.Person_has_Phone
                PAP.Subject_has_Url
                  PAP.Company_has_Url
                  PAP.Person_has_Url
              PAP.Person_has_Account
            EVT.Link2
            SWP.Link2
            SRM.Link2
              SRM.Boat_in_Regatta
              SRM.Crew_Member
              SRM.Team_has_Boat_in_Regatta
          MOM.Link3
            Auth.Link3
            PAP.Link3
            EVT.Link3
            SWP.Link3
            SRM.Link3
      MOM.Object
        MOM.Named_Object
          Auth.Named_Object
            Auth.Group
          PAP.Named_Object
          EVT.Named_Object
          SWP.Named_Object
          SRM.Named_Object
        Auth.Object
          Auth._Account_
            Auth.Account_Anonymous
            Auth.Account
          Auth.Certificate
        PAP.Object
          PAP.Property
            PAP.Address
            PAP.Email
            PAP.Phone
            PAP.Url
          PAP.Subject
            PAP.Legal_Entity
              PAP.Company
            PAP.Person
        EVT.Object
          EVT.Calendar
        SWP.Object
          SWP.Object_PN
            SWP.Page
              SWP.Page_Y
              SWP.Clip_X
              SRM.Page
            SWP.Gallery
        SRM.Object
          SRM._Boat_Class_
            SRM.Boat_Class
            SRM.Handicap
          SRM.Club
          SRM.Regatta_Event
      Auth.Id_Entity
      PAP.Id_Entity
      EVT.Id_Entity
      SWP.Id_Entity
      SRM.Id_Entity


"""

__test__ = Scaffold.create_test_dict \
    ( dict
        ( test_e_type = _test_e_type
        , test_types  = _test_types
        )
    )

XX__test__ = Scaffold.create_test_dict \
    ( dict
        ( test_types  = _test_types
        )
    )

### __END__ GTW.__test__.Attr
