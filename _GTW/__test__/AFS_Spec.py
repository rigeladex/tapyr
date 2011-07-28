# -*- coding: iso-8859-15 -*-
# Copyright (C) 2011 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# #*** <License> ************************************************************
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
#    AFS_Spec
#
# Purpose
#    Test GTW.AFS.MOM.Spec
#
# Revision Dates
#    17-Feb-2011 (CT) Creation
#    10-Jun-2011 (MG) `_entity_links_group` test added
#     6-Jul-2011 (CT) `_entity_links_group` test fixed (and `_test_code`
#                     enabled, again)
#    ««revision-date»»···
#--

from __future__ import unicode_literals

_test_code = """
    >>> scope = Scaffold.scope ("hps://") # doctest:+ELLIPSIS
    Creating new scope MOMT__...
    >>> from _GTW._AFS._MOM import Spec
    >>> S = Spec.Entity ()
    >>> x = S (scope.PAP.Person._etype)
    >>> print repr (x)
    <Entity None 'Person' 'GTW.OMP.PAP.Person'>
     <Fieldset None u'primary'>
      <Field None 'last_name'>
      <Field None 'first_name'>
      <Field None 'middle_name'>
      <Field None 'title'>
     <Fieldset None u'necessary'>
      <Field None 'sex'>
     <Fieldset None u'optional'>
      <Field_Composite None 'lifetime' 'MOM.Date_Interval'>
       <Field None 'start'>
       <Field None 'finish'>
      <Field None 'salutation'>

    >>> SL = Spec.Entity (include_links = ("addresses", "emails", "phones"))
    >>> xl = SL (scope.PAP.Person._etype)
    >>> print repr (xl)
    <Entity None 'Person' 'GTW.OMP.PAP.Person'>
     <Fieldset None u'primary'>
      <Field None 'last_name'>
      <Field None 'first_name'>
      <Field None 'middle_name'>
      <Field None 'title'>
     <Fieldset None u'necessary'>
      <Field None 'sex'>
     <Fieldset None u'optional'>
      <Field_Composite None 'lifetime' 'MOM.Date_Interval'>
       <Field None 'start'>
       <Field None 'finish'>
      <Field None 'salutation'>
     <Entity_List None 'Person_has_Address' <Entity_Link None 'Person_has_Address' 'GTW.OMP.PAP.Person_has_Address'>>
      <Entity_Link None 'Person_has_Address' 'GTW.OMP.PAP.Person_has_Address'>
       <Field_Role_Hidden None u'left' 'GTW.OMP.PAP.Person'>
       <Fieldset None u'primary'>
        <Field_Entity None 'right' 'GTW.OMP.PAP.Address'>
         <Field None 'street'>
         <Field None 'zip'>
         <Field None 'city'>
         <Field None 'country'>
       <Fieldset None u'optional'>
        <Field None 'desc'>
     <Entity_List None 'Person_has_Email' <Entity_Link None 'Person_has_Email' 'GTW.OMP.PAP.Person_has_Email'>>
      <Entity_Link None 'Person_has_Email' 'GTW.OMP.PAP.Person_has_Email'>
       <Field_Role_Hidden None u'left' 'GTW.OMP.PAP.Person'>
       <Fieldset None u'primary'>
        <Field_Entity None 'right' 'GTW.OMP.PAP.Email'>
         <Field None 'address'>
       <Fieldset None u'optional'>
        <Field None 'desc'>
     <Entity_List None 'Person_has_Phone' <Entity_Link None 'Person_has_Phone' 'GTW.OMP.PAP.Person_has_Phone'>>
      <Entity_Link None 'Person_has_Phone' 'GTW.OMP.PAP.Person_has_Phone'>
       <Field_Role_Hidden None u'left' 'GTW.OMP.PAP.Person'>
       <Fieldset None u'primary'>
        <Field_Entity None 'right' 'GTW.OMP.PAP.Phone'>
         <Field None 'country_code'>
         <Field None 'area_code'>
         <Field None 'number'>
        <Field None 'extension'>
       <Fieldset None u'optional'>
        <Field None 'desc'>

    >>> NL = chr (10)
    >>> for e in xl.transitive_iter () :
    ...   print e.__class__.__name__, e._name, getattr (e, "ui_name", None), repr (getattr (e, "description", "").replace (NL, " ")), e.renderer
    Entity Person Person u'' afs_div_seq
    Fieldset primary None u'' afs_div_seq
    Field last_name Last name u'Last name of person' None
    Field first_name First name u'First name of person' None
    Field middle_name Middle name u'Middle name of person' None
    Field title Academic title u'Academic title.' None
    Fieldset necessary None u'' afs_div_seq
    Field sex Sex u'Sex of a person.' None
    Fieldset optional None u'' afs_div_seq
    Field_Composite lifetime Lifetime u'Date of birth [`start`] (and death [`finish`])' afs_div_seq
    Field start Start u'Start date of interval' None
    Field finish Finish u'Finish date of interval' None
    Field salutation Salutation u'Salutation to be used when communicating with person (e.g., in a letter or email).' None
    Entity_List Person_has_Address Person_has_Address u'' afs_div_seq
    Entity_Link Person_has_Address Person_has_Address u'' afs_div_seq
    Field_Role_Hidden left Person u'' afs_div_seq
    Fieldset primary None u'' afs_div_seq
    Field_Entity right Address u'Address where person lives or works' afs_div_seq
    Field street Street u'Street (or place) and house number' None
    Field zip Zip code u'Zip code of address' None
    Field city City u'City, town, or village' None
    Field country Country u'Country' None
    Fieldset optional None u'' afs_div_seq
    Field desc Description u'Short description of the link' None
    Entity_List Person_has_Email Person_has_Email u'' afs_div_seq
    Entity_Link Person_has_Email Person_has_Email u'' afs_div_seq
    Field_Role_Hidden left Person u'' afs_div_seq
    Fieldset primary None u'' afs_div_seq
    Field_Entity right Email u'Email address of person' afs_div_seq
    Field address Email address u'Email address (including domain)' None
    Fieldset optional None u'' afs_div_seq
    Field desc Description u'Short description of the link' None
    Entity_List Person_has_Phone Person_has_Phone u'' afs_div_seq
    Entity_Link Person_has_Phone Person_has_Phone u'' afs_div_seq
    Field_Role_Hidden left Person u'' afs_div_seq
    Fieldset primary None u'' afs_div_seq
    Field_Entity right Phone u'Phone number of person' afs_div_seq
    Field country_code Country code u'International country code of phone number (without prefix)' None
    Field area_code Area code u'National area code of phone number (without prefix)' None
    Field number Number u'Phone number proper (without country code, area code, extension)' None
    Field extension Extension u'Extension number used in PBX' None
    Fieldset optional None u'' afs_div_seq
    Field desc Description u'Short description of the link' None

    >>> T = Spec.Entity (Spec.Entity_Link ("events",
    ...   Spec.Entity_Link ("recurrence", Spec.Entity_Link ("rules"))))
    >>> y = T (scope.SWP.Page._etype)
    >>> print repr (y)
    <Entity None 'Page' 'GTW.OMP.SWP.Page'>
     <Fieldset None u'primary'>
      <Field None 'perma_name'>
     <Fieldset None u'required'>
      <Field None 'text'>
     <Fieldset None u'necessary'>
      <Field None 'short_title'>
      <Field None 'title'>
     <Fieldset None u'optional'>
      <Field_Composite None 'date' 'MOM.Date_Interval_N'>
       <Field None 'start'>
       <Field None 'finish'>
      <Field None 'format'>
      <Field None 'head_line'>
      <Field None 'hidden'>
      <Field None 'prio'>
     <Entity_List None 'Event' <Entity_Link None 'Event' 'GTW.OMP.EVT.Event'>>
      <Entity_Link None 'Event' 'GTW.OMP.EVT.Event'>
       <Field_Role_Hidden None u'left' 'GTW.OMP.SWP.Page'>
       <Fieldset None u'primary'>
        <Field_Composite None 'date' 'MOM.Date_Interval'>
         <Field None 'start'>
         <Field None 'finish'>
        <Field_Composite None 'time' 'MOM.Time_Interval'>
         <Field None 'start'>
         <Field None 'finish'>
       <Fieldset None u'optional'>
        <Field None 'detail'>
        <Field None 'short_title'>
       <Entity_Link None 'Recurrence_Spec' 'GTW.OMP.EVT.Recurrence_Spec'>
        <Field_Role_Hidden None u'left' 'GTW.OMP.EVT.Event'>
        <Fieldset None u'optional'>
         <Field None 'dates'>
         <Field None 'date_exceptions'>
        <Entity_List None 'Recurrence_Rule' <Entity_Link None 'Recurrence_Rule' 'GTW.OMP.EVT.Recurrence_Rule'>>
         <Entity_Link None 'Recurrence_Rule' 'GTW.OMP.EVT.Recurrence_Rule'>
          <Field_Role_Hidden None u'left' 'GTW.OMP.EVT.Recurrence_Spec'>
          <Fieldset None u'primary'>
           <Field None 'is_exception'>
           <Field None 'desc'>
          <Fieldset None u'optional'>
           <Field None 'start'>
           <Field None 'finish'>
           <Field None 'period'>
           <Field None 'unit'>
           <Field None 'week_day'>
           <Field None 'count'>
           <Field None 'restrict_pos'>
           <Field None 'month_day'>
           <Field None 'month'>
           <Field None 'week'>
           <Field None 'year_day'>
           <Field None 'easter_offset'>

    >>> print repr (Form ("F", children = [y]))
    <Form F>
     <Entity F-0 'Page' 'GTW.OMP.SWP.Page'>
      <Fieldset F-0:0 u'primary'>
       <Field F-0:0:0 'perma_name'>
      <Fieldset F-0:1 u'required'>
       <Field F-0:1:0 'text'>
      <Fieldset F-0:2 u'necessary'>
       <Field F-0:2:0 'short_title'>
       <Field F-0:2:1 'title'>
      <Fieldset F-0:3 u'optional'>
       <Field_Composite F-0:3:0 'date' 'MOM.Date_Interval_N'>
        <Field F-0:3:0.0 'start'>
        <Field F-0:3:0.1 'finish'>
       <Field F-0:3:1 'format'>
       <Field F-0:3:2 'head_line'>
       <Field F-0:3:3 'hidden'>
       <Field F-0:3:4 'prio'>
      <Entity_List F-0:4 'Event' <Entity_Link F-0:4::p 'Event' 'GTW.OMP.EVT.Event'>>
       <Entity_Link F-0:4::p 'Event' 'GTW.OMP.EVT.Event'>
        <Field_Role_Hidden F-0:4::p-0 u'left' 'GTW.OMP.SWP.Page'>
        <Fieldset F-0:4::p-1 u'primary'>
         <Field_Composite F-0:4::p-1:0 'date' 'MOM.Date_Interval'>
          <Field F-0:4::p-1:0.0 'start'>
          <Field F-0:4::p-1:0.1 'finish'>
         <Field_Composite F-0:4::p-1:1 'time' 'MOM.Time_Interval'>
          <Field F-0:4::p-1:1.0 'start'>
          <Field F-0:4::p-1:1.1 'finish'>
        <Fieldset F-0:4::p-2 u'optional'>
         <Field F-0:4::p-2:0 'detail'>
         <Field F-0:4::p-2:1 'short_title'>
        <Entity_Link F-0:4::p-3 'Recurrence_Spec' 'GTW.OMP.EVT.Recurrence_Spec'>
         <Field_Role_Hidden F-0:4::p-3:0 u'left' 'GTW.OMP.EVT.Event'>
         <Fieldset F-0:4::p-3:1 u'optional'>
          <Field F-0:4::p-3:1:0 'dates'>
          <Field F-0:4::p-3:1:1 'date_exceptions'>
         <Entity_List F-0:4::p-3:2 'Recurrence_Rule' <Entity_Link F-0:4::p-3:2::p 'Recurrence_Rule' 'GTW.OMP.EVT.Recurrence_Rule'>>
          <Entity_Link F-0:4::p-3:2::p 'Recurrence_Rule' 'GTW.OMP.EVT.Recurrence_Rule'>
           <Field_Role_Hidden F-0:4::p-3:2::p-0 u'left' 'GTW.OMP.EVT.Recurrence_Spec'>
           <Fieldset F-0:4::p-3:2::p-1 u'primary'>
            <Field F-0:4::p-3:2::p-1:0 'is_exception'>
            <Field F-0:4::p-3:2::p-1:1 'desc'>
           <Fieldset F-0:4::p-3:2::p-2 u'optional'>
            <Field F-0:4::p-3:2::p-2:0 'start'>
            <Field F-0:4::p-3:2::p-2:1 'finish'>
            <Field F-0:4::p-3:2::p-2:2 'period'>
            <Field F-0:4::p-3:2::p-2:3 'unit'>
            <Field F-0:4::p-3:2::p-2:4 'week_day'>
            <Field F-0:4::p-3:2::p-2:5 'count'>
            <Field F-0:4::p-3:2::p-2:6 'restrict_pos'>
            <Field F-0:4::p-3:2::p-2:7 'month_day'>
            <Field F-0:4::p-3:2::p-2:8 'month'>
            <Field F-0:4::p-3:2::p-2:9 'week'>
            <Field F-0:4::p-3:2::p-2:10 'year_day'>
            <Field F-0:4::p-3:2::p-2:11 'easter_offset'>

    >>> f = Form ("X", children = [x, y])
    >>> print repr (f)
    <Form X>
     <Entity X-0 'Person' 'GTW.OMP.PAP.Person'>
      <Fieldset X-0:0 u'primary'>
       <Field X-0:0:0 'last_name'>
       <Field X-0:0:1 'first_name'>
       <Field X-0:0:2 'middle_name'>
       <Field X-0:0:3 'title'>
      <Fieldset X-0:1 u'necessary'>
       <Field X-0:1:0 'sex'>
      <Fieldset X-0:2 u'optional'>
       <Field_Composite X-0:2:0 'lifetime' 'MOM.Date_Interval'>
        <Field X-0:2:0.0 'start'>
        <Field X-0:2:0.1 'finish'>
       <Field X-0:2:1 'salutation'>
     <Entity X-1 'Page' 'GTW.OMP.SWP.Page'>
      <Fieldset X-1:0 u'primary'>
       <Field X-1:0:0 'perma_name'>
      <Fieldset X-1:1 u'required'>
       <Field X-1:1:0 'text'>
      <Fieldset X-1:2 u'necessary'>
       <Field X-1:2:0 'short_title'>
       <Field X-1:2:1 'title'>
      <Fieldset X-1:3 u'optional'>
       <Field_Composite X-1:3:0 'date' 'MOM.Date_Interval_N'>
        <Field X-1:3:0.0 'start'>
        <Field X-1:3:0.1 'finish'>
       <Field X-1:3:1 'format'>
       <Field X-1:3:2 'head_line'>
       <Field X-1:3:3 'hidden'>
       <Field X-1:3:4 'prio'>
      <Entity_List X-1:4 'Event' <Entity_Link X-1:4::p 'Event' 'GTW.OMP.EVT.Event'>>
       <Entity_Link X-1:4::p 'Event' 'GTW.OMP.EVT.Event'>
        <Field_Role_Hidden X-1:4::p-0 u'left' 'GTW.OMP.SWP.Page'>
        <Fieldset X-1:4::p-1 u'primary'>
         <Field_Composite X-1:4::p-1:0 'date' 'MOM.Date_Interval'>
          <Field X-1:4::p-1:0.0 'start'>
          <Field X-1:4::p-1:0.1 'finish'>
         <Field_Composite X-1:4::p-1:1 'time' 'MOM.Time_Interval'>
          <Field X-1:4::p-1:1.0 'start'>
          <Field X-1:4::p-1:1.1 'finish'>
        <Fieldset X-1:4::p-2 u'optional'>
         <Field X-1:4::p-2:0 'detail'>
         <Field X-1:4::p-2:1 'short_title'>
        <Entity_Link X-1:4::p-3 'Recurrence_Spec' 'GTW.OMP.EVT.Recurrence_Spec'>
         <Field_Role_Hidden X-1:4::p-3:0 u'left' 'GTW.OMP.EVT.Event'>
         <Fieldset X-1:4::p-3:1 u'optional'>
          <Field X-1:4::p-3:1:0 'dates'>
          <Field X-1:4::p-3:1:1 'date_exceptions'>
         <Entity_List X-1:4::p-3:2 'Recurrence_Rule' <Entity_Link X-1:4::p-3:2::p 'Recurrence_Rule' 'GTW.OMP.EVT.Recurrence_Rule'>>
          <Entity_Link X-1:4::p-3:2::p 'Recurrence_Rule' 'GTW.OMP.EVT.Recurrence_Rule'>
           <Field_Role_Hidden X-1:4::p-3:2::p-0 u'left' 'GTW.OMP.EVT.Recurrence_Spec'>
           <Fieldset X-1:4::p-3:2::p-1 u'primary'>
            <Field X-1:4::p-3:2::p-1:0 'is_exception'>
            <Field X-1:4::p-3:2::p-1:1 'desc'>
           <Fieldset X-1:4::p-3:2::p-2 u'optional'>
            <Field X-1:4::p-3:2::p-2:0 'start'>
            <Field X-1:4::p-3:2::p-2:1 'finish'>
            <Field X-1:4::p-3:2::p-2:2 'period'>
            <Field X-1:4::p-3:2::p-2:3 'unit'>
            <Field X-1:4::p-3:2::p-2:4 'week_day'>
            <Field X-1:4::p-3:2::p-2:5 'count'>
            <Field X-1:4::p-3:2::p-2:6 'restrict_pos'>
            <Field X-1:4::p-3:2::p-2:7 'month_day'>
            <Field X-1:4::p-3:2::p-2:8 'month'>
            <Field X-1:4::p-3:2::p-2:9 'week'>
            <Field X-1:4::p-3:2::p-2:10 'year_day'>
            <Field X-1:4::p-3:2::p-2:11 'easter_offset'>

    >>> SB = Spec.Entity (Spec.Entity_Link ("GTW.OMP.SRM.Boat_in_Regatta"))
    >>> fb = Form ("FB", children = [SB (scope.SRM.Boat)])
    >>> print repr (fb)
    <Form FB>
     <Entity FB-0 'Boat' 'GTW.OMP.SRM.Boat'>
      <Fieldset FB-0:0 u'primary'>
       <Field_Entity FB-0:0:0 'left' 'GTW.OMP.SRM.Boat_Class'>
        <Field FB-0:0:0:0 'name'>
       <Field FB-0:0:1 'nation'>
       <Field FB-0:0:2 'sail_number'>
      <Fieldset FB-0:1 u'optional'>
       <Field FB-0:1:0 'name'>
       <Field FB-0:1:1 'sail_number_x'>
      <Entity_List FB-0:2 'Boat_in_Regatta' <Entity_Link FB-0:2::p 'Boat_in_Regatta' 'GTW.OMP.SRM.Boat_in_Regatta'>>
       <Entity_Link FB-0:2::p 'Boat_in_Regatta' 'GTW.OMP.SRM.Boat_in_Regatta'>
        <Field_Role_Hidden FB-0:2::p-0 u'left' 'GTW.OMP.SRM.Boat'>
        <Fieldset FB-0:2::p-1 u'primary'>
         <Field_Entity FB-0:2::p-1:0 'right' 'GTW.OMP.SRM.Regatta'>
          <Field_Entity FB-0:2::p-1:0:0 'left' 'GTW.OMP.SRM.Regatta_Event'>
           <Field_Composite FB-0:2::p-1:0:0:0 'date' 'MOM.Date_Interval_C'>
            <Field FB-0:2::p-1:0:0:0.0 'start'>
            <Field FB-0:2::p-1:0:0:0.1 'finish'>
           <Field FB-0:2::p-1:0:0:1 'name'>
        <Fieldset FB-0:2::p-2 u'required'>
         <Field_Entity FB-0:2::p-2:0 'skipper' 'GTW.OMP.SRM.Sailor'>
          <Field_Entity FB-0:2::p-2:0:0 'left' 'GTW.OMP.PAP.Person'>
           <Field FB-0:2::p-2:0:0:0 'last_name'>
           <Field FB-0:2::p-2:0:0:1 'first_name'>
           <Field FB-0:2::p-2:0:0:2 'middle_name'>
           <Field FB-0:2::p-2:0:0:3 'title'>
          <Field FB-0:2::p-2:0:1 'nation'>
          <Field FB-0:2::p-2:0:2 'mna_number'>
        <Fieldset FB-0:2::p-3 u'optional'>
         <Field FB-0:2::p-3:0 'place'>
         <Field FB-0:2::p-3:1 'points'>

    >>> PAP = scope.PAP
    >>> SRM = scope.SRM
    >>> bc  = SRM.Boat_Class ("Optimist", max_crew = 1)
    >>> b   = SRM.Boat.instance_or_new (u"Optimist", u"AUT", u"1107", raw = True)
    >>> p   = PAP.Person.instance_or_new (u"Tanzer", u"Laurens")
    >>> s   = SRM.Sailor.instance_or_new (p, nation = u"AUT", mna_number = u"29676", raw = True)
    >>> rev = SRM.Regatta_Event (dict (start = u"20080501", raw = True), u"Himmelfahrt", raw = True)
    >>> reg = SRM.Regatta_C (rev, boat_class = bc)
    >>> bir = SRM.Boat_in_Regatta (b, reg, skipper = s)

    >>> scope.commit ()
    >>> fi  = fb (SRM.Boat, b)
    >>> fic = fb (SRM.Boat, b, copy = True)

    >>> ff_ln = fb ['FB-0:2::0-2:0:0:0']
    >>> print ff_ln
    <Field FB-0:2::p-2:0:0:0 'last_name'>
    >>> print formatted (ff_ln.kw)
    { 'completer' :
        { 'entity_p' : True
        , 'names' :
            [ 'last_name'
            , 'first_name'
            , 'middle_name'
            , 'title'
            ]
        , 'treshold' : 2
        }
    , 'kind' : 'primary'
    , 'label' : 'Last name'
    , 'name' : 'last_name'
    }

    >>> print formatted (fi.as_json_cargo, level = 1)
      { '$id' : 'FB'
      , 'children' :
          [ { '$id' : 'FB-0'
            , 'children' :
                [ { '$id' : 'FB-0:0'
                  , 'children' :
                      [ { '$id' : 'FB-0:0:0'
                        , 'allow_new' : True
                        , 'children' :
                            [ { '$id' : 'FB-0:0:0:0'
                              , 'kind' : 'primary'
                              , 'label' : 'Name'
                              , 'name' : 'name'
                              , 'required' : True
                              , 'type' : 'Field'
                              , 'value' :
                                  { 'init' : 'Optimist' }
                              }
                            ]
                        , 'collapsed' : True
                        , 'kind' : 'primary'
                        , 'label' : 'Class'
                        , 'name' : 'left'
                        , 'required' : True
                        , 'type' : 'Field_Entity'
                        , 'type_name' : 'GTW.OMP.SRM.Boat_Class'
                        , 'value' :
                            { 'init' :
                                { 'cid' : 1
                                , 'pid' : 1
                                }
                            , 'sid' : 'qPzMz88f1x3RjbWOPHj4PR2ZthTO:EW:MNddnA'
                            }
                        }
                      , { '$id' : 'FB-0:0:1'
                        , 'kind' : 'primary'
                        , 'label' : 'Nation'
                        , 'name' : 'nation'
                        , 'type' : 'Field'
                        , 'value' :
                            { 'init' : 'AUT' }
                        }
                      , { '$id' : 'FB-0:0:2'
                        , 'kind' : 'primary'
                        , 'label' : 'Sail number'
                        , 'name' : 'sail_number'
                        , 'type' : 'Field'
                        , 'value' :
                            { 'init' : '1107' }
                        }
                      ]
                  , 'collapsed' : False
                  , 'name' : 'primary'
                  , 'type' : 'Fieldset'
                  }
                , { '$id' : 'FB-0:1'
                  , 'children' :
                      [ { '$id' : 'FB-0:1:0'
                        , 'kind' : 'optional'
                        , 'label' : 'Name'
                        , 'name' : 'name'
                        , 'type' : 'Field'
                        , 'value' :
                            {}
                        }
                      , { '$id' : 'FB-0:1:1'
                        , 'kind' : 'optional'
                        , 'label' : 'Sail number x'
                        , 'name' : 'sail_number_x'
                        , 'type' : 'Field'
                        , 'value' :
                            {}
                        }
                      ]
                  , 'collapsed' : True
                  , 'name' : 'optional'
                  , 'type' : 'Fieldset'
                  }
                , { '$id' : 'FB-0:2'
                  , 'children' :
                      [ { '$id' : 'FB-0:2::0'
                        , 'children' :
                            [ { '$id' : 'FB-0:2::0-0'
                              , 'allow_new' : False
                              , 'collapsed' : True
                              , 'hidden' : True
                              , 'kind' : 'primary'
                              , 'label' : 'Boat'
                              , 'name' : 'left'
                              , 'required' : True
                              , 'type' : 'Field_Role_Hidden'
                              , 'type_name' : 'GTW.OMP.SRM.Boat'
                              , 'value' :
                                  { 'init' :
                                      { 'cid' : 2
                                      , 'pid' : 2
                                      }
                                  , 'sid' : 'ORsB0LFjw5hzuHauaOA1M3usp415XdhUdQ0tfQ'
                                  }
                              }
                            , { '$id' : 'FB-0:2::0-1'
                              , 'children' :
                                  [ { '$id' : 'FB-0:2::0-1:0'
                                    , 'allow_new' : False
                                    , 'children' :
                                        [ { '$id' : 'FB-0:2::0-1:0:0'
                                          , 'allow_new' : False
                                          , 'children' :
                                              [ { '$id' : 'FB-0:2::0-1:0:0:0'
                                                , 'children' :
                                                    [ { '$id' : 'FB-0:2::0-1:0:0:0.0'
                                                      , 'kind' : 'necessary'
                                                      , 'label' : 'Start'
                                                      , 'name' : 'start'
                                                      , 'type' : 'Field'
                                                      , 'value' :
                                                          { 'init' : '2008/05/01' }
                                                      }
                                                    , { '$id' : 'FB-0:2::0-1:0:0:0.1'
                                                      , 'kind' : 'optional'
                                                      , 'label' : 'Finish'
                                                      , 'name' : 'finish'
                                                      , 'type' : 'Field'
                                                      , 'value' :
                                                          { 'init' : '2008/05/01' }
                                                      }
                                                    ]
                                                , 'collapsed' : True
                                                , 'kind' : 'primary'
                                                , 'label' : 'Date'
                                                , 'name' : 'date'
                                                , 'required' : True
                                                , 'type' : 'Field_Composite'
                                                , 'type_name' : 'MOM.Date_Interval_C'
                                                , 'value' :
                                                    {}
                                                }
                                              , { '$id' : 'FB-0:2::0-1:0:0:1'
                                                , 'kind' : 'primary'
                                                , 'label' : 'Name'
                                                , 'name' : 'name'
                                                , 'required' : True
                                                , 'type' : 'Field'
                                                , 'value' :
                                                    { 'init' : 'Himmelfahrt' }
                                                }
                                              ]
                                          , 'collapsed' : True
                                          , 'kind' : 'primary'
                                          , 'label' : 'Event'
                                          , 'name' : 'left'
                                          , 'required' : True
                                          , 'type' : 'Field_Entity'
                                          , 'type_name' : 'GTW.OMP.SRM.Regatta_Event'
                                          , 'value' :
                                              { 'init' :
                                                  { 'cid' : 5
                                                  , 'pid' : 5
                                                  }
                                              , 'sid' : 'w6pfZ9cV126kdzebJWKIfT6QasZLd2e6dh7O4g'
                                              }
                                          }
                                        ]
                                    , 'collapsed' : True
                                    , 'kind' : 'primary'
                                    , 'label' : 'Regatta'
                                    , 'name' : 'right'
                                    , 'required' : True
                                    , 'type' : 'Field_Entity'
                                    , 'type_name' : 'GTW.OMP.SRM.Regatta'
                                    , 'value' :
                                        { 'init' :
                                            { 'cid' : 6
                                            , 'pid' : 6
                                            }
                                        , 'sid' : 't0nRFI5GFozOgzRVAMlfEVZeU9oCHiVfFTBuWw'
                                        }
                                    }
                                  ]
                              , 'collapsed' : False
                              , 'name' : 'primary'
                              , 'type' : 'Fieldset'
                              }
                            , { '$id' : 'FB-0:2::0-2'
                              , 'children' :
                                  [ { '$id' : 'FB-0:2::0-2:0'
                                    , 'allow_new' : True
                                    , 'children' :
                                        [ { '$id' : 'FB-0:2::0-2:0:0'
                                          , 'allow_new' : True
                                          , 'children' :
                                              [ { '$id' : 'FB-0:2::0-2:0:0:0'
                                                , 'completer' :
                                                    { 'entity_p' : True
                                                    , 'names' :
                                                        [ 'last_name'
                                                        , 'first_name'
                                                        , 'middle_name'
                                                        , 'title'
                                                        ]
                                                    , 'treshold' : 2
                                                    }
                                                , 'kind' : 'primary'
                                                , 'label' : 'Last name'
                                                , 'name' : 'last_name'
                                                , 'required' : True
                                                , 'type' : 'Field'
                                                , 'value' :
                                                    { 'init' : 'Tanzer' }
                                                }
                                              , { '$id' : 'FB-0:2::0-2:0:0:1'
                                                , 'completer' :
                                                    { 'entity_p' : True
                                                    , 'names' :
                                                        [ 'first_name'
                                                        , 'last_name'
                                                        , 'middle_name'
                                                        , 'title'
                                                        ]
                                                    , 'treshold' : 3
                                                    }
                                                , 'kind' : 'primary'
                                                , 'label' : 'First name'
                                                , 'name' : 'first_name'
                                                , 'required' : True
                                                , 'type' : 'Field'
                                                , 'value' :
                                                    { 'init' : 'Laurens' }
                                                }
                                              , { '$id' : 'FB-0:2::0-2:0:0:2'
                                                , 'completer' :
                                                    { 'entity_p' : True
                                                    , 'names' :
                                                        [ 'middle_name'
                                                        , 'last_name'
                                                        , 'first_name'
                                                        , 'title'
                                                        ]
                                                    , 'treshold' : 2
                                                    }
                                                , 'kind' : 'primary'
                                                , 'label' : 'Middle name'
                                                , 'name' : 'middle_name'
                                                , 'type' : 'Field'
                                                , 'value' :
                                                    {}
                                                }
                                              , { '$id' : 'FB-0:2::0-2:0:0:3'
                                                , 'completer' :
                                                    { 'entity_p' : False
                                                    , 'names' :
    [ 'title' ]
                                                    , 'treshold' : 1
                                                    }
                                                , 'kind' : 'primary'
                                                , 'label' : 'Academic title'
                                                , 'name' : 'title'
                                                , 'type' : 'Field'
                                                , 'value' :
                                                    {}
                                                }
                                              ]
                                          , 'collapsed' : True
                                          , 'kind' : 'primary'
                                          , 'label' : 'Person'
                                          , 'name' : 'left'
                                          , 'required' : True
                                          , 'type' : 'Field_Entity'
                                          , 'type_name' : 'GTW.OMP.PAP.Person'
                                          , 'value' :
                                              { 'init' :
                                                  { 'cid' : 3
                                                  , 'pid' : 3
                                                  }
                                              , 'sid' : 'jCVvrVL7cxthrwL4:mPenABA:H4vtKSITQhTuA'
                                              }
                                          }
                                        , { '$id' : 'FB-0:2::0-2:0:1'
                                          , 'kind' : 'primary'
                                          , 'label' : 'Nation'
                                          , 'name' : 'nation'
                                          , 'type' : 'Field'
                                          , 'value' :
                                              { 'init' : 'AUT' }
                                          }
                                        , { '$id' : 'FB-0:2::0-2:0:2'
                                          , 'kind' : 'primary'
                                          , 'label' : 'Mna number'
                                          , 'name' : 'mna_number'
                                          , 'type' : 'Field'
                                          , 'value' :
                                              { 'init' : '29676' }
                                          }
                                        ]
                                    , 'collapsed' : True
                                    , 'kind' : 'required'
                                    , 'label' : 'Skipper'
                                    , 'name' : 'skipper'
                                    , 'required' : True
                                    , 'type' : 'Field_Entity'
                                    , 'type_name' : 'GTW.OMP.SRM.Sailor'
                                    , 'value' :
                                        { 'init' :
                                            { 'cid' : 4
                                            , 'pid' : 4
                                            }
                                        , 'sid' : 'eW12pOklOQqAlV9CsVuZLsdwncWDlF6FYe3Mig'
                                        }
                                    }
                                  ]
                              , 'collapsed' : True
                              , 'name' : 'required'
                              , 'type' : 'Fieldset'
                              }
                            , { '$id' : 'FB-0:2::0-3'
                              , 'children' :
                                  [ { '$id' : 'FB-0:2::0-3:0'
                                    , 'kind' : 'optional'
                                    , 'label' : 'Place'
                                    , 'name' : 'place'
                                    , 'type' : 'Field'
                                    , 'value' :
                                        {}
                                    }
                                  , { '$id' : 'FB-0:2::0-3:1'
                                    , 'kind' : 'optional'
                                    , 'label' : 'Points'
                                    , 'name' : 'points'
                                    , 'type' : 'Field'
                                    , 'value' :
                                        {}
                                    }
                                  ]
                              , 'collapsed' : True
                              , 'name' : 'optional'
                              , 'type' : 'Fieldset'
                              }
                            ]
                        , 'collapsed' : True
                        , 'name' : 'Boat_in_Regatta'
                        , 'role_name' : 'left'
                        , 'type' : 'Entity_Link'
                        , 'type_name' : 'GTW.OMP.SRM.Boat_in_Regatta'
                        , 'value' :
                            { 'init' :
                                { 'cid' : 7
                                , 'pid' : 7
                                }
                            , 'sid' : 'z2Wp1P:S-4gBkqNEMci0tQJ-anqXaOToH7ZK7g'
                            }
                        }
                      ]
                  , 'name' : 'Boat_in_Regatta'
                  , 'type' : 'Entity_List'
                  , 'type_name' : 'GTW.OMP.SRM.Boat_in_Regatta'
                  }
                ]
            , 'name' : 'Boat'
            , 'type' : 'Entity'
            , 'type_name' : 'GTW.OMP.SRM.Boat'
            , 'value' :
                { 'init' :
                    { 'cid' : 2
                    , 'pid' : 2
                    }
                , 'sid' : 'LjJ-MkYSz6QxselaD8NeT-5G:2a5YHFTbpYNig'
                }
            }
          ]
      , 'type' : 'Form'
      , 'value' :
          { 'sid' : 0 }
      }

    >>> print formatted (fic.as_json_cargo, level = 1)
      { '$id' : 'FB'
      , 'children' :
          [ { '$id' : 'FB-0'
            , 'children' :
                [ { '$id' : 'FB-0:0'
                  , 'children' :
                      [ { '$id' : 'FB-0:0:0'
                        , 'allow_new' : True
                        , 'children' :
                            [ { '$id' : 'FB-0:0:0:0'
                              , 'kind' : 'primary'
                              , 'label' : 'Name'
                              , 'name' : 'name'
                              , 'required' : True
                              , 'type' : 'Field'
                              , 'value' :
                                  { 'edit' : 'Optimist' }
                              }
                            ]
                        , 'collapsed' : True
                        , 'kind' : 'primary'
                        , 'label' : 'Class'
                        , 'name' : 'left'
                        , 'required' : True
                        , 'type' : 'Field_Entity'
                        , 'type_name' : 'GTW.OMP.SRM.Boat_Class'
                        , 'value' :
                            { 'init' :
                                {}
                            , 'sid' : '2SMjmpittgN68fuUf1yK7xN-uRxHK4q2kDJOlA'
                            }
                        }
                      , { '$id' : 'FB-0:0:1'
                        , 'kind' : 'primary'
                        , 'label' : 'Nation'
                        , 'name' : 'nation'
                        , 'type' : 'Field'
                        , 'value' :
                            { 'edit' : 'AUT' }
                        }
                      , { '$id' : 'FB-0:0:2'
                        , 'kind' : 'primary'
                        , 'label' : 'Sail number'
                        , 'name' : 'sail_number'
                        , 'type' : 'Field'
                        , 'value' :
                            { 'edit' : '1107' }
                        }
                      ]
                  , 'collapsed' : False
                  , 'name' : 'primary'
                  , 'type' : 'Fieldset'
                  }
                , { '$id' : 'FB-0:1'
                  , 'children' :
                      [ { '$id' : 'FB-0:1:0'
                        , 'kind' : 'optional'
                        , 'label' : 'Name'
                        , 'name' : 'name'
                        , 'type' : 'Field'
                        , 'value' :
                            {}
                        }
                      , { '$id' : 'FB-0:1:1'
                        , 'kind' : 'optional'
                        , 'label' : 'Sail number x'
                        , 'name' : 'sail_number_x'
                        , 'type' : 'Field'
                        , 'value' :
                            {}
                        }
                      ]
                  , 'collapsed' : True
                  , 'name' : 'optional'
                  , 'type' : 'Fieldset'
                  }
                , { '$id' : 'FB-0:2'
                  , 'children' :
                      [ { '$id' : 'FB-0:2::0'
                        , 'children' :
                            [ { '$id' : 'FB-0:2::0-0'
                              , 'allow_new' : False
                              , 'collapsed' : True
                              , 'hidden' : True
                              , 'kind' : 'primary'
                              , 'label' : 'Boat'
                              , 'name' : 'left'
                              , 'required' : True
                              , 'type' : 'Field_Role_Hidden'
                              , 'type_name' : 'GTW.OMP.SRM.Boat'
                              , 'value' :
                                  { 'init' :
                                      {}
                                  , 'sid' : 'emH:n2fr5Vojp8:mNyEhadFeTvrt0Hb26l7S4Q'
                                  }
                              }
                            , { '$id' : 'FB-0:2::0-1'
                              , 'children' :
                                  [ { '$id' : 'FB-0:2::0-1:0'
                                    , 'allow_new' : False
                                    , 'children' :
                                        [ { '$id' : 'FB-0:2::0-1:0:0'
                                          , 'allow_new' : False
                                          , 'children' :
                                              [ { '$id' : 'FB-0:2::0-1:0:0:0'
                                                , 'children' :
                                                    [ { '$id' : 'FB-0:2::0-1:0:0:0.0'
                                                      , 'kind' : 'necessary'
                                                      , 'label' : 'Start'
                                                      , 'name' : 'start'
                                                      , 'type' : 'Field'
                                                      , 'value' :
                                                          { 'edit' : '2008/05/01' }
                                                      }
                                                    , { '$id' : 'FB-0:2::0-1:0:0:0.1'
                                                      , 'kind' : 'optional'
                                                      , 'label' : 'Finish'
                                                      , 'name' : 'finish'
                                                      , 'type' : 'Field'
                                                      , 'value' :
                                                          { 'edit' : '2008/05/01' }
                                                      }
                                                    ]
                                                , 'collapsed' : True
                                                , 'kind' : 'primary'
                                                , 'label' : 'Date'
                                                , 'name' : 'date'
                                                , 'required' : True
                                                , 'type' : 'Field_Composite'
                                                , 'type_name' : 'MOM.Date_Interval_C'
                                                , 'value' :
                                                    {}
                                                }
                                              , { '$id' : 'FB-0:2::0-1:0:0:1'
                                                , 'kind' : 'primary'
                                                , 'label' : 'Name'
                                                , 'name' : 'name'
                                                , 'required' : True
                                                , 'type' : 'Field'
                                                , 'value' :
                                                    { 'edit' : 'Himmelfahrt' }
                                                }
                                              ]
                                          , 'collapsed' : True
                                          , 'kind' : 'primary'
                                          , 'label' : 'Event'
                                          , 'name' : 'left'
                                          , 'required' : True
                                          , 'type' : 'Field_Entity'
                                          , 'type_name' : 'GTW.OMP.SRM.Regatta_Event'
                                          , 'value' :
                                              { 'init' :
                                                  {}
                                              , 'sid' : ':Zy-KiCVwPDIlN-Zvcq7gVx6E2rK0frgII402w'
                                              }
                                          }
                                        ]
                                    , 'collapsed' : True
                                    , 'kind' : 'primary'
                                    , 'label' : 'Regatta'
                                    , 'name' : 'right'
                                    , 'required' : True
                                    , 'type' : 'Field_Entity'
                                    , 'type_name' : 'GTW.OMP.SRM.Regatta'
                                    , 'value' :
                                        { 'init' :
                                            {}
                                        , 'sid' : 'n4dFoUTWL2ZKZ1e-igGdLTtkVfW3LOxorspVfw'
                                        }
                                    }
                                  ]
                              , 'collapsed' : False
                              , 'name' : 'primary'
                              , 'type' : 'Fieldset'
                              }
                            , { '$id' : 'FB-0:2::0-2'
                              , 'children' :
                                  [ { '$id' : 'FB-0:2::0-2:0'
                                    , 'allow_new' : True
                                    , 'children' :
                                        [ { '$id' : 'FB-0:2::0-2:0:0'
                                          , 'allow_new' : True
                                          , 'children' :
                                              [ { '$id' : 'FB-0:2::0-2:0:0:0'
                                                , 'completer' :
                                                    { 'entity_p' : True
                                                    , 'names' :
                                                        [ 'last_name'
                                                        , 'first_name'
                                                        , 'middle_name'
                                                        , 'title'
                                                        ]
                                                    , 'treshold' : 2
                                                    }
                                                , 'kind' : 'primary'
                                                , 'label' : 'Last name'
                                                , 'name' : 'last_name'
                                                , 'required' : True
                                                , 'type' : 'Field'
                                                , 'value' :
                                                    { 'edit' : 'Tanzer' }
                                                }
                                              , { '$id' : 'FB-0:2::0-2:0:0:1'
                                                , 'completer' :
                                                    { 'entity_p' : True
                                                    , 'names' :
                                                        [ 'first_name'
                                                        , 'last_name'
                                                        , 'middle_name'
                                                        , 'title'
                                                        ]
                                                    , 'treshold' : 3
                                                    }
                                                , 'kind' : 'primary'
                                                , 'label' : 'First name'
                                                , 'name' : 'first_name'
                                                , 'required' : True
                                                , 'type' : 'Field'
                                                , 'value' :
                                                    { 'edit' : 'Laurens' }
                                                }
                                              , { '$id' : 'FB-0:2::0-2:0:0:2'
                                                , 'completer' :
                                                    { 'entity_p' : True
                                                    , 'names' :
                                                        [ 'middle_name'
                                                        , 'last_name'
                                                        , 'first_name'
                                                        , 'title'
                                                        ]
                                                    , 'treshold' : 2
                                                    }
                                                , 'kind' : 'primary'
                                                , 'label' : 'Middle name'
                                                , 'name' : 'middle_name'
                                                , 'type' : 'Field'
                                                , 'value' :
                                                    {}
                                                }
                                              , { '$id' : 'FB-0:2::0-2:0:0:3'
                                                , 'completer' :
                                                    { 'entity_p' : False
                                                    , 'names' :
    [ 'title' ]
                                                    , 'treshold' : 1
                                                    }
                                                , 'kind' : 'primary'
                                                , 'label' : 'Academic title'
                                                , 'name' : 'title'
                                                , 'type' : 'Field'
                                                , 'value' :
                                                    {}
                                                }
                                              ]
                                          , 'collapsed' : True
                                          , 'kind' : 'primary'
                                          , 'label' : 'Person'
                                          , 'name' : 'left'
                                          , 'required' : True
                                          , 'type' : 'Field_Entity'
                                          , 'type_name' : 'GTW.OMP.PAP.Person'
                                          , 'value' :
                                              { 'init' :
                                                  {}
                                              , 'sid' : 'Z:YWrkrkIu19OHcrW0W6DFmkEXuuZ7TAjiV5qQ'
                                              }
                                          }
                                        , { '$id' : 'FB-0:2::0-2:0:1'
                                          , 'kind' : 'primary'
                                          , 'label' : 'Nation'
                                          , 'name' : 'nation'
                                          , 'type' : 'Field'
                                          , 'value' :
                                              { 'edit' : 'AUT' }
                                          }
                                        , { '$id' : 'FB-0:2::0-2:0:2'
                                          , 'kind' : 'primary'
                                          , 'label' : 'Mna number'
                                          , 'name' : 'mna_number'
                                          , 'type' : 'Field'
                                          , 'value' :
                                              { 'edit' : '29676' }
                                          }
                                        ]
                                    , 'collapsed' : True
                                    , 'kind' : 'required'
                                    , 'label' : 'Skipper'
                                    , 'name' : 'skipper'
                                    , 'required' : True
                                    , 'type' : 'Field_Entity'
                                    , 'type_name' : 'GTW.OMP.SRM.Sailor'
                                    , 'value' :
                                        { 'init' :
                                            {}
                                        , 'sid' : 'olYDjjANTpCXJXfp80i93QNzK2-ZYMVkSmrv:w'
                                        }
                                    }
                                  ]
                              , 'collapsed' : True
                              , 'name' : 'required'
                              , 'type' : 'Fieldset'
                              }
                            , { '$id' : 'FB-0:2::0-3'
                              , 'children' :
                                  [ { '$id' : 'FB-0:2::0-3:0'
                                    , 'kind' : 'optional'
                                    , 'label' : 'Place'
                                    , 'name' : 'place'
                                    , 'type' : 'Field'
                                    , 'value' :
                                        {}
                                    }
                                  , { '$id' : 'FB-0:2::0-3:1'
                                    , 'kind' : 'optional'
                                    , 'label' : 'Points'
                                    , 'name' : 'points'
                                    , 'type' : 'Field'
                                    , 'value' :
                                        {}
                                    }
                                  ]
                              , 'collapsed' : True
                              , 'name' : 'optional'
                              , 'type' : 'Fieldset'
                              }
                            ]
                        , 'collapsed' : True
                        , 'name' : 'Boat_in_Regatta'
                        , 'role_name' : 'left'
                        , 'type' : 'Entity_Link'
                        , 'type_name' : 'GTW.OMP.SRM.Boat_in_Regatta'
                        , 'value' :
                            { 'init' :
                                {}
                            , 'sid' : 'UtcUyWMVWMEfZeA9RSCEBsCSnrbfeND6VYcmIw'
                            }
                        }
                      ]
                  , 'name' : 'Boat_in_Regatta'
                  , 'type' : 'Entity_List'
                  , 'type_name' : 'GTW.OMP.SRM.Boat_in_Regatta'
                  }
                ]
            , 'name' : 'Boat'
            , 'type' : 'Entity'
            , 'type_name' : 'GTW.OMP.SRM.Boat'
            , 'value' :
                { 'init' :
                    {}
                , 'sid' : '3VDfUb:0kn9ux5Abs2QtfjSwttsyL6T7BTPRJw'
                }
            }
          ]
      , 'type' : 'Form'
      , 'value' :
          { 'sid' : 0 }
      }

    >>> print "var f =", fi.as_js, ";"
    var f = new $GTW.AFS.Form ({"$id": "FB", "children": [{"$id": "FB-0", "children": [{"$id": "FB-0:0", "children": [{"$id": "FB-0:0:0", "allow_new": true, "children": [{"$id": "FB-0:0:0:0", "kind": "primary", "label": "Name", "name": "name", "required": true, "type": "Field", "value": {"init": "Optimist"}}], "collapsed": true, "kind": "primary", "label": "Class", "name": "left", "required": true, "type": "Field_Entity", "type_name": "GTW.OMP.SRM.Boat_Class", "value": {"init": {"cid": 1, "pid": 1}, "sid": "qPzMz88f1x3RjbWOPHj4PR2ZthTO:EW:MNddnA"}}, {"$id": "FB-0:0:1", "kind": "primary", "label": "Nation", "name": "nation", "type": "Field", "value": {"init": "AUT"}}, {"$id": "FB-0:0:2", "kind": "primary", "label": "Sail number", "name": "sail_number", "type": "Field", "value": {"init": "1107"}}], "collapsed": false, "name": "primary", "type": "Fieldset"}, {"$id": "FB-0:1", "children": [{"$id": "FB-0:1:0", "kind": "optional", "label": "Name", "name": "name", "type": "Field", "value": {}}, {"$id": "FB-0:1:1", "kind": "optional", "label": "Sail number x", "name": "sail_number_x", "type": "Field", "value": {}}], "collapsed": true, "name": "optional", "type": "Fieldset"}, {"$id": "FB-0:2", "children": [{"$id": "FB-0:2::0", "children": [{"$id": "FB-0:2::0-0", "allow_new": false, "collapsed": true, "hidden": true, "kind": "primary", "label": "Boat", "name": "left", "required": true, "type": "Field_Role_Hidden", "type_name": "GTW.OMP.SRM.Boat", "value": {"init": {"cid": 2, "pid": 2}, "sid": "ORsB0LFjw5hzuHauaOA1M3usp415XdhUdQ0tfQ"}}, {"$id": "FB-0:2::0-1", "children": [{"$id": "FB-0:2::0-1:0", "allow_new": false, "children": [{"$id": "FB-0:2::0-1:0:0", "allow_new": false, "children": [{"$id": "FB-0:2::0-1:0:0:0", "children": [{"$id": "FB-0:2::0-1:0:0:0.0", "kind": "necessary", "label": "Start", "name": "start", "type": "Field", "value": {"init": "2008/05/01"}}, {"$id": "FB-0:2::0-1:0:0:0.1", "kind": "optional", "label": "Finish", "name": "finish", "type": "Field", "value": {"init": "2008/05/01"}}], "collapsed": true, "kind": "primary", "label": "Date", "name": "date", "required": true, "type": "Field_Composite", "type_name": "MOM.Date_Interval_C", "value": {}}, {"$id": "FB-0:2::0-1:0:0:1", "kind": "primary", "label": "Name", "name": "name", "required": true, "type": "Field", "value": {"init": "Himmelfahrt"}}], "collapsed": true, "kind": "primary", "label": "Event", "name": "left", "required": true, "type": "Field_Entity", "type_name": "GTW.OMP.SRM.Regatta_Event", "value": {"init": {"cid": 5, "pid": 5}, "sid": "w6pfZ9cV126kdzebJWKIfT6QasZLd2e6dh7O4g"}}], "collapsed": true, "kind": "primary", "label": "Regatta", "name": "right", "required": true, "type": "Field_Entity", "type_name": "GTW.OMP.SRM.Regatta", "value": {"init": {"cid": 6, "pid": 6}, "sid": "t0nRFI5GFozOgzRVAMlfEVZeU9oCHiVfFTBuWw"}}], "collapsed": false, "name": "primary", "type": "Fieldset"}, {"$id": "FB-0:2::0-2", "children": [{"$id": "FB-0:2::0-2:0", "allow_new": true, "children": [{"$id": "FB-0:2::0-2:0:0", "allow_new": true, "children": [{"$id": "FB-0:2::0-2:0:0:0", "completer": {"entity_p": true, "names": ["last_name", "first_name", "middle_name", "title"], "treshold": 2}, "kind": "primary", "label": "Last name", "name": "last_name", "required": true, "type": "Field", "value": {"init": "Tanzer"}}, {"$id": "FB-0:2::0-2:0:0:1", "completer": {"entity_p": true, "names": ["first_name", "last_name", "middle_name", "title"], "treshold": 3}, "kind": "primary", "label": "First name", "name": "first_name", "required": true, "type": "Field", "value": {"init": "Laurens"}}, {"$id": "FB-0:2::0-2:0:0:2", "completer": {"entity_p": true, "names": ["middle_name", "last_name", "first_name", "title"], "treshold": 2}, "kind": "primary", "label": "Middle name", "name": "middle_name", "type": "Field", "value": {}}, {"$id": "FB-0:2::0-2:0:0:3", "completer": {"entity_p": false, "names": ["title"], "treshold": 1}, "kind": "primary", "label": "Academic title", "name": "title", "type": "Field", "value": {}}], "collapsed": true, "kind": "primary", "label": "Person", "name": "left", "required": true, "type": "Field_Entity", "type_name": "GTW.OMP.PAP.Person", "value": {"init": {"cid": 3, "pid": 3}, "sid": "jCVvrVL7cxthrwL4:mPenABA:H4vtKSITQhTuA"}}, {"$id": "FB-0:2::0-2:0:1", "kind": "primary", "label": "Nation", "name": "nation", "type": "Field", "value": {"init": "AUT"}}, {"$id": "FB-0:2::0-2:0:2", "kind": "primary", "label": "Mna number", "name": "mna_number", "type": "Field", "value": {"init": "29676"}}], "collapsed": true, "kind": "required", "label": "Skipper", "name": "skipper", "required": true, "type": "Field_Entity", "type_name": "GTW.OMP.SRM.Sailor", "value": {"init": {"cid": 4, "pid": 4}, "sid": "eW12pOklOQqAlV9CsVuZLsdwncWDlF6FYe3Mig"}}], "collapsed": true, "name": "required", "type": "Fieldset"}, {"$id": "FB-0:2::0-3", "children": [{"$id": "FB-0:2::0-3:0", "kind": "optional", "label": "Place", "name": "place", "type": "Field", "value": {}}, {"$id": "FB-0:2::0-3:1", "kind": "optional", "label": "Points", "name": "points", "type": "Field", "value": {}}], "collapsed": true, "name": "optional", "type": "Fieldset"}], "collapsed": true, "name": "Boat_in_Regatta", "role_name": "left", "type": "Entity_Link", "type_name": "GTW.OMP.SRM.Boat_in_Regatta", "value": {"init": {"cid": 7, "pid": 7}, "sid": "z2Wp1P:S-4gBkqNEMci0tQJ-anqXaOToH7ZK7g"}}], "name": "Boat_in_Regatta", "type": "Entity_List", "type_name": "GTW.OMP.SRM.Boat_in_Regatta"}], "name": "Boat", "type": "Entity", "type_name": "GTW.OMP.SRM.Boat", "value": {"init": {"cid": 2, "pid": 2}, "sid": "LjJ-MkYSz6QxselaD8NeT-5G:2a5YHFTbpYNig"}}], "type": "Form", "value": {"sid": 0}}) ;
    >>> print "var g =", fic.as_js, ";"
    var g = new $GTW.AFS.Form ({"$id": "FB", "children": [{"$id": "FB-0", "children": [{"$id": "FB-0:0", "children": [{"$id": "FB-0:0:0", "allow_new": true, "children": [{"$id": "FB-0:0:0:0", "kind": "primary", "label": "Name", "name": "name", "required": true, "type": "Field", "value": {"edit": "Optimist"}}], "collapsed": true, "kind": "primary", "label": "Class", "name": "left", "required": true, "type": "Field_Entity", "type_name": "GTW.OMP.SRM.Boat_Class", "value": {"init": {}, "sid": "2SMjmpittgN68fuUf1yK7xN-uRxHK4q2kDJOlA"}}, {"$id": "FB-0:0:1", "kind": "primary", "label": "Nation", "name": "nation", "type": "Field", "value": {"edit": "AUT"}}, {"$id": "FB-0:0:2", "kind": "primary", "label": "Sail number", "name": "sail_number", "type": "Field", "value": {"edit": "1107"}}], "collapsed": false, "name": "primary", "type": "Fieldset"}, {"$id": "FB-0:1", "children": [{"$id": "FB-0:1:0", "kind": "optional", "label": "Name", "name": "name", "type": "Field", "value": {}}, {"$id": "FB-0:1:1", "kind": "optional", "label": "Sail number x", "name": "sail_number_x", "type": "Field", "value": {}}], "collapsed": true, "name": "optional", "type": "Fieldset"}, {"$id": "FB-0:2", "children": [{"$id": "FB-0:2::0", "children": [{"$id": "FB-0:2::0-0", "allow_new": false, "collapsed": true, "hidden": true, "kind": "primary", "label": "Boat", "name": "left", "required": true, "type": "Field_Role_Hidden", "type_name": "GTW.OMP.SRM.Boat", "value": {"init": {}, "sid": "emH:n2fr5Vojp8:mNyEhadFeTvrt0Hb26l7S4Q"}}, {"$id": "FB-0:2::0-1", "children": [{"$id": "FB-0:2::0-1:0", "allow_new": false, "children": [{"$id": "FB-0:2::0-1:0:0", "allow_new": false, "children": [{"$id": "FB-0:2::0-1:0:0:0", "children": [{"$id": "FB-0:2::0-1:0:0:0.0", "kind": "necessary", "label": "Start", "name": "start", "type": "Field", "value": {"edit": "2008/05/01"}}, {"$id": "FB-0:2::0-1:0:0:0.1", "kind": "optional", "label": "Finish", "name": "finish", "type": "Field", "value": {"edit": "2008/05/01"}}], "collapsed": true, "kind": "primary", "label": "Date", "name": "date", "required": true, "type": "Field_Composite", "type_name": "MOM.Date_Interval_C", "value": {}}, {"$id": "FB-0:2::0-1:0:0:1", "kind": "primary", "label": "Name", "name": "name", "required": true, "type": "Field", "value": {"edit": "Himmelfahrt"}}], "collapsed": true, "kind": "primary", "label": "Event", "name": "left", "required": true, "type": "Field_Entity", "type_name": "GTW.OMP.SRM.Regatta_Event", "value": {"init": {}, "sid": ":Zy-KiCVwPDIlN-Zvcq7gVx6E2rK0frgII402w"}}], "collapsed": true, "kind": "primary", "label": "Regatta", "name": "right", "required": true, "type": "Field_Entity", "type_name": "GTW.OMP.SRM.Regatta", "value": {"init": {}, "sid": "n4dFoUTWL2ZKZ1e-igGdLTtkVfW3LOxorspVfw"}}], "collapsed": false, "name": "primary", "type": "Fieldset"}, {"$id": "FB-0:2::0-2", "children": [{"$id": "FB-0:2::0-2:0", "allow_new": true, "children": [{"$id": "FB-0:2::0-2:0:0", "allow_new": true, "children": [{"$id": "FB-0:2::0-2:0:0:0", "completer": {"entity_p": true, "names": ["last_name", "first_name", "middle_name", "title"], "treshold": 2}, "kind": "primary", "label": "Last name", "name": "last_name", "required": true, "type": "Field", "value": {"edit": "Tanzer"}}, {"$id": "FB-0:2::0-2:0:0:1", "completer": {"entity_p": true, "names": ["first_name", "last_name", "middle_name", "title"], "treshold": 3}, "kind": "primary", "label": "First name", "name": "first_name", "required": true, "type": "Field", "value": {"edit": "Laurens"}}, {"$id": "FB-0:2::0-2:0:0:2", "completer": {"entity_p": true, "names": ["middle_name", "last_name", "first_name", "title"], "treshold": 2}, "kind": "primary", "label": "Middle name", "name": "middle_name", "type": "Field", "value": {}}, {"$id": "FB-0:2::0-2:0:0:3", "completer": {"entity_p": false, "names": ["title"], "treshold": 1}, "kind": "primary", "label": "Academic title", "name": "title", "type": "Field", "value": {}}], "collapsed": true, "kind": "primary", "label": "Person", "name": "left", "required": true, "type": "Field_Entity", "type_name": "GTW.OMP.PAP.Person", "value": {"init": {}, "sid": "Z:YWrkrkIu19OHcrW0W6DFmkEXuuZ7TAjiV5qQ"}}, {"$id": "FB-0:2::0-2:0:1", "kind": "primary", "label": "Nation", "name": "nation", "type": "Field", "value": {"edit": "AUT"}}, {"$id": "FB-0:2::0-2:0:2", "kind": "primary", "label": "Mna number", "name": "mna_number", "type": "Field", "value": {"edit": "29676"}}], "collapsed": true, "kind": "required", "label": "Skipper", "name": "skipper", "required": true, "type": "Field_Entity", "type_name": "GTW.OMP.SRM.Sailor", "value": {"init": {}, "sid": "olYDjjANTpCXJXfp80i93QNzK2-ZYMVkSmrv:w"}}], "collapsed": true, "name": "required", "type": "Fieldset"}, {"$id": "FB-0:2::0-3", "children": [{"$id": "FB-0:2::0-3:0", "kind": "optional", "label": "Place", "name": "place", "type": "Field", "value": {}}, {"$id": "FB-0:2::0-3:1", "kind": "optional", "label": "Points", "name": "points", "type": "Field", "value": {}}], "collapsed": true, "name": "optional", "type": "Fieldset"}], "collapsed": true, "name": "Boat_in_Regatta", "role_name": "left", "type": "Entity_Link", "type_name": "GTW.OMP.SRM.Boat_in_Regatta", "value": {"init": {}, "sid": "UtcUyWMVWMEfZeA9RSCEBsCSnrbfeND6VYcmIw"}}], "name": "Boat_in_Regatta", "type": "Entity_List", "type_name": "GTW.OMP.SRM.Boat_in_Regatta"}], "name": "Boat", "type": "Entity", "type_name": "GTW.OMP.SRM.Boat", "value": {"init": {}, "sid": "3VDfUb:0kn9ux5Abs2QtfjSwttsyL6T7BTPRJw"}}], "type": "Form", "value": {"sid": 0}}) ;

    >>> for i in fi.transitive_iter () :
    ...     print i.elem, sorted (i.value or ())
    <Form FB> ['sid']
    <Entity FB-0 'Boat' 'GTW.OMP.SRM.Boat'> [u'init', 'sid']
    <Fieldset FB-0:0 u'primary'> []
    <Field_Entity FB-0:0:0 'left' 'GTW.OMP.SRM.Boat_Class'> [u'init', 'sid']
    <Field FB-0:0:0:0 'name'> [u'init']
    <Field FB-0:0:1 'nation'> [u'init']
    <Field FB-0:0:2 'sail_number'> [u'init']
    <Fieldset FB-0:1 u'optional'> []
    <Field FB-0:1:0 'name'> []
    <Field FB-0:1:1 'sail_number_x'> []
    <Entity_List FB-0:2 'Boat_in_Regatta' <Entity_Link FB-0:2::p 'Boat_in_Regatta' 'GTW.OMP.SRM.Boat_in_Regatta'>> []
    <Entity_Link FB-0:2::0 'Boat_in_Regatta' 'GTW.OMP.SRM.Boat_in_Regatta'> [u'init', 'sid']
    <Field_Role_Hidden FB-0:2::0-0 u'left' 'GTW.OMP.SRM.Boat'> [u'init', 'sid']
    <Fieldset FB-0:2::0-1 u'primary'> []
    <Field_Entity FB-0:2::0-1:0 'right' 'GTW.OMP.SRM.Regatta'> [u'init', 'sid']
    <Field_Entity FB-0:2::0-1:0:0 'left' 'GTW.OMP.SRM.Regatta_Event'> [u'init', 'sid']
    <Field_Composite FB-0:2::0-1:0:0:0 'date' 'MOM.Date_Interval_C'> []
    <Field FB-0:2::0-1:0:0:0.0 'start'> [u'init']
    <Field FB-0:2::0-1:0:0:0.1 'finish'> [u'init']
    <Field FB-0:2::0-1:0:0:1 'name'> [u'init']
    <Fieldset FB-0:2::0-2 u'required'> []
    <Field_Entity FB-0:2::0-2:0 'skipper' 'GTW.OMP.SRM.Sailor'> [u'init', 'sid']
    <Field_Entity FB-0:2::0-2:0:0 'left' 'GTW.OMP.PAP.Person'> [u'init', 'sid']
    <Field FB-0:2::0-2:0:0:0 'last_name'> [u'init']
    <Field FB-0:2::0-2:0:0:1 'first_name'> [u'init']
    <Field FB-0:2::0-2:0:0:2 'middle_name'> []
    <Field FB-0:2::0-2:0:0:3 'title'> []
    <Field FB-0:2::0-2:0:1 'nation'> [u'init']
    <Field FB-0:2::0-2:0:2 'mna_number'> [u'init']
    <Fieldset FB-0:2::0-3 u'optional'> []
    <Field FB-0:2::0-3:0 'place'> []
    <Field FB-0:2::0-3:1 'points'> []

    >>> for i in fi.entities () :
    ...     print i.elem
    <Entity FB-0 'Boat' 'GTW.OMP.SRM.Boat'>

    >>> f_sig_map = {}
    >>> for i in fi.entity_children () :
    ...     f_sig_map [i.id] = i, i.sig
    ...     print i.elem, ", pid =", i.init.get ("pid"), ", sid =", i.sid
    <Entity FB-0 'Boat' 'GTW.OMP.SRM.Boat'> , pid = 2 , sid = LjJ-MkYSz6QxselaD8NeT-5G:2a5YHFTbpYNig
    <Field_Entity FB-0:0:0 'left' 'GTW.OMP.SRM.Boat_Class'> , pid = 1 , sid = qPzMz88f1x3RjbWOPHj4PR2ZthTO:EW:MNddnA
    <Entity_Link FB-0:2::0 'Boat_in_Regatta' 'GTW.OMP.SRM.Boat_in_Regatta'> , pid = 7 , sid = z2Wp1P:S-4gBkqNEMci0tQJ-anqXaOToH7ZK7g
    <Field_Role_Hidden FB-0:2::0-0 u'left' 'GTW.OMP.SRM.Boat'> , pid = 2 , sid = ORsB0LFjw5hzuHauaOA1M3usp415XdhUdQ0tfQ
    <Field_Entity FB-0:2::0-1:0 'right' 'GTW.OMP.SRM.Regatta'> , pid = 6 , sid = t0nRFI5GFozOgzRVAMlfEVZeU9oCHiVfFTBuWw
    <Field_Entity FB-0:2::0-1:0:0 'left' 'GTW.OMP.SRM.Regatta_Event'> , pid = 5 , sid = w6pfZ9cV126kdzebJWKIfT6QasZLd2e6dh7O4g
    <Field_Entity FB-0:2::0-2:0 'skipper' 'GTW.OMP.SRM.Sailor'> , pid = 4 , sid = eW12pOklOQqAlV9CsVuZLsdwncWDlF6FYe3Mig
    <Field_Entity FB-0:2::0-2:0:0 'left' 'GTW.OMP.PAP.Person'> , pid = 3 , sid = jCVvrVL7cxthrwL4:mPenABA:H4vtKSITQhTuA

    >>> g_sig_map = {}
    >>> for i in fic.entity_children () :
    ...     g_sig_map [i.id] = i, i.sig
    ...     print i.elem, ", pid =", i.init.get ("pid"), ", sid =", i.sid
    <Entity FB-0 'Boat' 'GTW.OMP.SRM.Boat'> , pid = None , sid = 3VDfUb:0kn9ux5Abs2QtfjSwttsyL6T7BTPRJw
    <Field_Entity FB-0:0:0 'left' 'GTW.OMP.SRM.Boat_Class'> , pid = None , sid = 2SMjmpittgN68fuUf1yK7xN-uRxHK4q2kDJOlA
    <Entity_Link FB-0:2::0 'Boat_in_Regatta' 'GTW.OMP.SRM.Boat_in_Regatta'> , pid = None , sid = UtcUyWMVWMEfZeA9RSCEBsCSnrbfeND6VYcmIw
    <Field_Role_Hidden FB-0:2::0-0 u'left' 'GTW.OMP.SRM.Boat'> , pid = None , sid = emH:n2fr5Vojp8:mNyEhadFeTvrt0Hb26l7S4Q
    <Field_Entity FB-0:2::0-1:0 'right' 'GTW.OMP.SRM.Regatta'> , pid = None , sid = n4dFoUTWL2ZKZ1e-igGdLTtkVfW3LOxorspVfw
    <Field_Entity FB-0:2::0-1:0:0 'left' 'GTW.OMP.SRM.Regatta_Event'> , pid = None , sid = :Zy-KiCVwPDIlN-Zvcq7gVx6E2rK0frgII402w
    <Field_Entity FB-0:2::0-2:0 'skipper' 'GTW.OMP.SRM.Sailor'> , pid = None , sid = olYDjjANTpCXJXfp80i93QNzK2-ZYMVkSmrv:w
    <Field_Entity FB-0:2::0-2:0:0 'left' 'GTW.OMP.PAP.Person'> , pid = None , sid = Z:YWrkrkIu19OHcrW0W6DFmkEXuuZ7TAjiV5qQ

    >>> Value.from_json (json_bad)
    Traceback (most recent call last):
      ...
    Unknown: (u'Form/element is unknown', 404, {'unknown_id': u'FC'})

    >>> fv = Value.from_json (json_edit)
    >>> fv.changes_t
    1
    >>> for i in fv.transitive_iter () :
    ...     print i
    <Form FB>, init-v = '', sid = 0, changes = 0
    <Entity FB-0 'Boat' 'GTW.OMP.SRM.Boat'>, init-v = [(u'cid', 2), (u'pid', 2)], sid = LjJ-MkYSz6QxselaD8NeT-5G:2a5YHFTbpYNig, changes = 0
    <Field_Entity FB-0:0:0 'left' 'GTW.OMP.SRM.Boat_Class'>, init-v = [(u'cid', 1), (u'pid', 1)], sid = qPzMz88f1x3RjbWOPHj4PR2ZthTO:EW:MNddnA, changes = 0
    <Field FB-0:0:0:0 'name'>, init-v = 'Optimist', changes = 0
    <Field FB-0:0:1 'nation'>, init-v = 'AUT', changes = 0
    <Field FB-0:0:2 'sail_number'>, init-v = '1107', changes = 0
    <Field FB-0:1:0 'name'>, init-v = '', changes = 0
    <Field FB-0:1:1 'sail_number_x'>, init-v = '', changes = 0
    <Entity_Link FB-0:2::p 'Boat_in_Regatta' 'GTW.OMP.SRM.Boat_in_Regatta'>, init-v = [(u'cid', 7), (u'pid', 7)], sid = z2Wp1P:S-4gBkqNEMci0tQJ-anqXaOToH7ZK7g, changes = 0
    <Field_Role_Hidden FB-0:2::p-0 u'left' 'GTW.OMP.SRM.Boat'>, init-v = [(u'cid', 2), (u'pid', 2)], sid = ORsB0LFjw5hzuHauaOA1M3usp415XdhUdQ0tfQ, changes = 0, role_id = FB-0
    <Field_Entity FB-0:2::p-1:0 'right' 'GTW.OMP.SRM.Regatta'>, init-v = [(u'cid', 6), (u'pid', 6)], sid = t0nRFI5GFozOgzRVAMlfEVZeU9oCHiVfFTBuWw, changes = 0
    <Field_Entity FB-0:2::p-1:0:0 'left' 'GTW.OMP.SRM.Regatta_Event'>, init-v = [(u'cid', 5), (u'pid', 5)], sid = w6pfZ9cV126kdzebJWKIfT6QasZLd2e6dh7O4g, changes = 0
    <Field_Composite FB-0:2::p-1:0:0:0 'date' 'MOM.Date_Interval_C'>, init-v = '', changes = 0
    <Field FB-0:2::p-1:0:0:0.0 'start'>, init-v = '2008/05/01', changes = 0
    <Field FB-0:2::p-1:0:0:0.1 'finish'>, init-v = '2008/05/01', changes = 0
    <Field FB-0:2::p-1:0:0:1 'name'>, init-v = 'Himmelfahrt', changes = 0
    <Field_Entity FB-0:2::p-2:0 'skipper' 'GTW.OMP.SRM.Sailor'>, init-v = [(u'cid', 4), (u'pid', 4)], sid = eW12pOklOQqAlV9CsVuZLsdwncWDlF6FYe3Mig, changes = 0
    <Field_Entity FB-0:2::p-2:0:0 'left' 'GTW.OMP.PAP.Person'>, init-v = [(u'cid', 3), (u'pid', 3)], sid = jCVvrVL7cxthrwL4:mPenABA:H4vtKSITQhTuA, changes = 1
    <Field FB-0:2::p-2:0:0:0 'last_name'>, init-v = 'Tanzer', changes = 0
    <Field FB-0:2::p-2:0:0:1 'first_name'>, init-v = 'Laurens', changes = 0
    <Field FB-0:2::p-2:0:0:2 'middle_name'>, init-v = '', edit-v = 'William', changes = 1
    <Field FB-0:2::p-2:0:0:3 'title'>, init-v = '', changes = 0
    <Field FB-0:2::p-2:0:1 'nation'>, init-v = 'AUT', changes = 0
    <Field FB-0:2::p-2:0:2 'mna_number'>, init-v = '29676', changes = 0
    <Field FB-0:2::p-3:0 'place'>, init-v = '', changes = 0
    <Field FB-0:2::p-3:1 'points'>, init-v = '', changes = 0

    >>> for v in fv.entities () :
    ...     print v.elem, v.changes_t
    <Entity FB-0 'Boat' 'GTW.OMP.SRM.Boat'> 0
    <Entity_Link FB-0:2::p 'Boat_in_Regatta' 'GTW.OMP.SRM.Boat_in_Regatta'> 1

    >>> v_sig_map = {}
    >>> for v in fv.entity_children () :
    ...     vh = v.elem.form_hash (v)
    ...     v_sig_map [v.id] = v, v.sig, vh

    >>> for id, (i, i_sig) in sorted (f_sig_map.iteritems ()) :
    ...    (v, v_sig, vh) = v_sig_map [id]
    ...    print i.elem, i.sid == vh, i_sig == v_sig
    ...    print "  >", i.sid
    ...    print "  <", vh
    ...    print "  >", i_sig
    ...    print "  <", v_sig
    <Entity FB-0 'Boat' 'GTW.OMP.SRM.Boat'> True True
      > LjJ-MkYSz6QxselaD8NeT-5G:2a5YHFTbpYNig
      < LjJ-MkYSz6QxselaD8NeT-5G:2a5YHFTbpYNig
      > (((u'pid', 2), (u'cid', 2), 'FB-0', 'GTW.OMP.SRM.Boat'), ('FB-0:0:0', 'left'), ('FB-0:0:1', 'nation', u'AUT'), ('FB-0:0:2', 'sail_number', u'1107'), ('FB-0:1:0', 'name', u''), ('FB-0:1:1', 'sail_number_x', u''), 0)
      < (((u'pid', 2), (u'cid', 2), 'FB-0', 'GTW.OMP.SRM.Boat'), ('FB-0:0:0', 'left'), ('FB-0:0:1', 'nation', u'AUT'), ('FB-0:0:2', 'sail_number', u'1107'), ('FB-0:1:0', 'name', u''), ('FB-0:1:1', 'sail_number_x', u''), 0)
    <Field_Entity FB-0:0:0 'left' 'GTW.OMP.SRM.Boat_Class'> True True
      > qPzMz88f1x3RjbWOPHj4PR2ZthTO:EW:MNddnA
      < qPzMz88f1x3RjbWOPHj4PR2ZthTO:EW:MNddnA
      > (((u'pid', 1), (u'cid', 1), 'FB-0:0:0', 'GTW.OMP.SRM.Boat_Class'), ('FB-0:0:0:0', 'name', u'Optimist'), 0)
      < (((u'pid', 1), (u'cid', 1), 'FB-0:0:0', 'GTW.OMP.SRM.Boat_Class'), ('FB-0:0:0:0', 'name', u'Optimist'), 0)
    <Entity_Link FB-0:2::0 'Boat_in_Regatta' 'GTW.OMP.SRM.Boat_in_Regatta'> True True
      > z2Wp1P:S-4gBkqNEMci0tQJ-anqXaOToH7ZK7g
      < z2Wp1P:S-4gBkqNEMci0tQJ-anqXaOToH7ZK7g
      > (((u'pid', 7), (u'cid', 7), 'FB-0:2::0', 'GTW.OMP.SRM.Boat_in_Regatta'), ('FB-0:2::0-0', u'left'), ('FB-0:2::0-1:0', 'right'), ('FB-0:2::0-2:0', 'skipper'), ('FB-0:2::0-3:0', 'place', u''), ('FB-0:2::0-3:1', 'points', u''), 0)
      < (((u'pid', 7), (u'cid', 7), 'FB-0:2::0', 'GTW.OMP.SRM.Boat_in_Regatta'), ('FB-0:2::0-0', u'left'), ('FB-0:2::0-1:0', 'right'), ('FB-0:2::0-2:0', 'skipper'), ('FB-0:2::0-3:0', 'place', u''), ('FB-0:2::0-3:1', 'points', u''), 0)
    <Field_Role_Hidden FB-0:2::0-0 u'left' 'GTW.OMP.SRM.Boat'> True True
      > ORsB0LFjw5hzuHauaOA1M3usp415XdhUdQ0tfQ
      < ORsB0LFjw5hzuHauaOA1M3usp415XdhUdQ0tfQ
      > (((u'pid', 2), (u'cid', 2), 'FB-0:2::0-0', 'GTW.OMP.SRM.Boat'), 0)
      < (((u'pid', 2), (u'cid', 2), 'FB-0:2::0-0', 'GTW.OMP.SRM.Boat'), 0)
    <Field_Entity FB-0:2::0-1:0 'right' 'GTW.OMP.SRM.Regatta'> True True
      > t0nRFI5GFozOgzRVAMlfEVZeU9oCHiVfFTBuWw
      < t0nRFI5GFozOgzRVAMlfEVZeU9oCHiVfFTBuWw
      > (((u'pid', 6), (u'cid', 6), 'FB-0:2::0-1:0', 'GTW.OMP.SRM.Regatta'), ('FB-0:2::0-1:0:0', 'left'), 0)
      < (((u'pid', 6), (u'cid', 6), 'FB-0:2::0-1:0', 'GTW.OMP.SRM.Regatta'), ('FB-0:2::0-1:0:0', 'left'), 0)
    <Field_Entity FB-0:2::0-1:0:0 'left' 'GTW.OMP.SRM.Regatta_Event'> True True
      > w6pfZ9cV126kdzebJWKIfT6QasZLd2e6dh7O4g
      < w6pfZ9cV126kdzebJWKIfT6QasZLd2e6dh7O4g
      > (((u'pid', 5), (u'cid', 5), 'FB-0:2::0-1:0:0', 'GTW.OMP.SRM.Regatta_Event'), ('FB-0:2::0-1:0:0:0', 'date', (('FB-0:2::0-1:0:0:0.0', 'start', u'2008/05/01'), ('FB-0:2::0-1:0:0:0.1', 'finish', u'2008/05/01'))), ('FB-0:2::0-1:0:0:1', 'name', u'Himmelfahrt'), 0)
      < (((u'pid', 5), (u'cid', 5), 'FB-0:2::0-1:0:0', 'GTW.OMP.SRM.Regatta_Event'), ('FB-0:2::0-1:0:0:0', 'date', (('FB-0:2::0-1:0:0:0.0', 'start', u'2008/05/01'), ('FB-0:2::0-1:0:0:0.1', 'finish', u'2008/05/01'))), ('FB-0:2::0-1:0:0:1', 'name', u'Himmelfahrt'), 0)
    <Field_Entity FB-0:2::0-2:0 'skipper' 'GTW.OMP.SRM.Sailor'> True True
      > eW12pOklOQqAlV9CsVuZLsdwncWDlF6FYe3Mig
      < eW12pOklOQqAlV9CsVuZLsdwncWDlF6FYe3Mig
      > (((u'pid', 4), (u'cid', 4), 'FB-0:2::0-2:0', 'GTW.OMP.SRM.Sailor'), ('FB-0:2::0-2:0:0', 'left'), ('FB-0:2::0-2:0:1', 'nation', u'AUT'), ('FB-0:2::0-2:0:2', 'mna_number', u'29676'), 0)
      < (((u'pid', 4), (u'cid', 4), 'FB-0:2::0-2:0', 'GTW.OMP.SRM.Sailor'), ('FB-0:2::0-2:0:0', 'left'), ('FB-0:2::0-2:0:1', 'nation', u'AUT'), ('FB-0:2::0-2:0:2', 'mna_number', u'29676'), 0)
    <Field_Entity FB-0:2::0-2:0:0 'left' 'GTW.OMP.PAP.Person'> True True
      > jCVvrVL7cxthrwL4:mPenABA:H4vtKSITQhTuA
      < jCVvrVL7cxthrwL4:mPenABA:H4vtKSITQhTuA
      > (((u'pid', 3), (u'cid', 3), 'FB-0:2::0-2:0:0', 'GTW.OMP.PAP.Person'), ('FB-0:2::0-2:0:0:0', 'last_name', u'Tanzer'), ('FB-0:2::0-2:0:0:1', 'first_name', u'Laurens'), ('FB-0:2::0-2:0:0:2', 'middle_name', u''), ('FB-0:2::0-2:0:0:3', 'title', u''), 0)
      < (((u'pid', 3), (u'cid', 3), 'FB-0:2::0-2:0:0', 'GTW.OMP.PAP.Person'), ('FB-0:2::0-2:0:0:0', 'last_name', u'Tanzer'), ('FB-0:2::0-2:0:0:1', 'first_name', u'Laurens'), ('FB-0:2::0-2:0:0:2', 'middle_name', u''), ('FB-0:2::0-2:0:0:3', 'title', u''), 0)

    >>> v.edit.get ("pid")
    3

    >>> p ### before `fv.apply`
    GTW.OMP.PAP.Person (u'tanzer', u'laurens', u'', u'')
    >>> fv.apply (scope, _sid = 0)
    >>> p ### after `fv.apply`
    GTW.OMP.PAP.Person (u'tanzer', u'laurens', u'william', u'')
    >>> _ = p.set (middle_name = "w.")
    >>> p
    GTW.OMP.PAP.Person (u'tanzer', u'laurens', u'w.', u'')
    >>> fv.apply (scope, _sid = 0)
    Traceback (most recent call last):
      ...
    Conflict: (u'Edit conflict: at least one value was changed asynchronously by another request.', 409)
    >>> p ### after `p.set (middle_name = "w.")`
    GTW.OMP.PAP.Person (u'tanzer', u'laurens', u'w.', u'')

    >>> fv.apply (scope, _sid = 1)
    Traceback (most recent call last):
      ...
    Corrupted: (u'The form values are corrupted.', 404)

    >>> gv = Value.from_json (json_copy)
    >>> gv.changes_t
    11
    >>> for v in gv.transitive_iter () :
    ...     print v
    <Form FB>, init-v = '', sid = 0, changes = 0
    <Entity FB-0 'Boat' 'GTW.OMP.SRM.Boat'>, init-v = [], sid = 3VDfUb:0kn9ux5Abs2QtfjSwttsyL6T7BTPRJw, changes = 2
    <Field_Entity FB-0:0:0 'left' 'GTW.OMP.SRM.Boat_Class'>, init-v = [], sid = 2SMjmpittgN68fuUf1yK7xN-uRxHK4q2kDJOlA, changes = 1
    <Field FB-0:0:0:0 'name'>, init-v = '', edit-v = 'Optimist', changes = 1
    <Field FB-0:0:1 'nation'>, init-v = '', edit-v = 'AUT', changes = 1
    <Field FB-0:0:2 'sail_number'>, init-v = '', edit-v = '1107', changes = 1
    <Field FB-0:1:0 'name'>, init-v = '', changes = 0
    <Field FB-0:1:1 'sail_number_x'>, init-v = '', changes = 0
    <Entity_Link FB-0:2::p 'Boat_in_Regatta' 'GTW.OMP.SRM.Boat_in_Regatta'>, init-v = [], sid = UtcUyWMVWMEfZeA9RSCEBsCSnrbfeND6VYcmIw, changes = 0
    <Field_Role_Hidden FB-0:2::p-0 u'left' 'GTW.OMP.SRM.Boat'>, init-v = [], sid = emH:n2fr5Vojp8:mNyEhadFeTvrt0Hb26l7S4Q, changes = 0, role_id = FB-0
    <Field_Entity FB-0:2::p-1:0 'right' 'GTW.OMP.SRM.Regatta'>, init-v = [], sid = n4dFoUTWL2ZKZ1e-igGdLTtkVfW3LOxorspVfw, changes = 0
    <Field_Entity FB-0:2::p-1:0:0 'left' 'GTW.OMP.SRM.Regatta_Event'>, init-v = [], sid = :Zy-KiCVwPDIlN-Zvcq7gVx6E2rK0frgII402w, changes = 1
    <Field_Composite FB-0:2::p-1:0:0:0 'date' 'MOM.Date_Interval_C'>, init-v = '', changes = 2
    <Field FB-0:2::p-1:0:0:0.0 'start'>, init-v = '', edit-v = '2008/05/01', changes = 1
    <Field FB-0:2::p-1:0:0:0.1 'finish'>, init-v = '', edit-v = '2008/05/01', changes = 1
    <Field FB-0:2::p-1:0:0:1 'name'>, init-v = '', edit-v = 'Himmelfahrt', changes = 1
    <Field_Entity FB-0:2::p-2:0 'skipper' 'GTW.OMP.SRM.Sailor'>, init-v = [], sid = olYDjjANTpCXJXfp80i93QNzK2-ZYMVkSmrv:w, changes = 2
    <Field_Entity FB-0:2::p-2:0:0 'left' 'GTW.OMP.PAP.Person'>, init-v = [], sid = Z:YWrkrkIu19OHcrW0W6DFmkEXuuZ7TAjiV5qQ, changes = 3
    <Field FB-0:2::p-2:0:0:0 'last_name'>, init-v = '', edit-v = 'Tanzer', changes = 1
    <Field FB-0:2::p-2:0:0:1 'first_name'>, init-v = '', edit-v = 'Laurens', changes = 1
    <Field FB-0:2::p-2:0:0:2 'middle_name'>, init-v = '', edit-v = 'William II', changes = 1
    <Field FB-0:2::p-2:0:0:3 'title'>, init-v = '', changes = 0
    <Field FB-0:2::p-2:0:1 'nation'>, init-v = '', edit-v = 'AUT', changes = 1
    <Field FB-0:2::p-2:0:2 'mna_number'>, init-v = '', edit-v = '29676', changes = 1
    <Field FB-0:2::p-3:0 'place'>, init-v = '', changes = 0
    <Field FB-0:2::p-3:1 'points'>, init-v = '', changes = 0

    >>> key = TFL.Sorted_By ("elem.rank", "-id")
    >>> for v in sorted (gv.entity_children (), key = key) :
    ...     print v.elem
    <Field_Entity FB-0:2::p-2:0:0 'left' 'GTW.OMP.PAP.Person'>
    <Field_Entity FB-0:2::p-2:0 'skipper' 'GTW.OMP.SRM.Sailor'>
    <Field_Entity FB-0:2::p-1:0:0 'left' 'GTW.OMP.SRM.Regatta_Event'>
    <Field_Entity FB-0:2::p-1:0 'right' 'GTW.OMP.SRM.Regatta'>
    <Field_Role_Hidden FB-0:2::p-0 u'left' 'GTW.OMP.SRM.Boat'>
    <Field_Entity FB-0:0:0 'left' 'GTW.OMP.SRM.Boat_Class'>
    <Entity FB-0 'Boat' 'GTW.OMP.SRM.Boat'>
    <Entity_Link FB-0:2::p 'Boat_in_Regatta' 'GTW.OMP.SRM.Boat_in_Regatta'>

    >>> for v in gv.entities () :
    ...     print v.elem, v.changes_t
    <Entity FB-0 'Boat' 'GTW.OMP.SRM.Boat'> 3
    <Entity_Link FB-0:2::p 'Boat_in_Regatta' 'GTW.OMP.SRM.Boat_in_Regatta'> 8

    >>> print formatted (gv.as_json_cargo, level = 1)
      { '$id' : 'FB'
      , 'children' :
          [ { '$id' : 'FB-0'
            , 'children' :
                [ { '$id' : 'FB-0:0:0'
                  , 'children' :
                      [ { '$id' : 'FB-0:0:0:0'
                        , 'value' :
                            { 'edit' : 'Optimist' }
                        }
                      ]
                  , 'value' :
                      { 'edit' :
                          {}
                      }
                  }
                , { '$id' : 'FB-0:0:1'
                  , 'value' :
                      { 'edit' : 'AUT' }
                  }
                , { '$id' : 'FB-0:0:2'
                  , 'value' :
                      { 'edit' : '1107' }
                  }
                , { '$id' : 'FB-0:1:0'
                  , 'value' :
                      {}
                  }
                , { '$id' : 'FB-0:1:1'
                  , 'value' :
                      {}
                  }
                ]
            , 'value' :
                { 'edit' :
                    {}
                }
            }
          , { '$id' : 'FB-0:2::p'
            , 'children' :
                [ { '$id' : 'FB-0:2::p-0'
                  , 'value' :
                      {}
                  }
                , { '$id' : 'FB-0:2::p-1:0'
                  , 'children' :
                      [ { '$id' : 'FB-0:2::p-1:0:0'
                        , 'children' :
                            [ { '$id' : 'FB-0:2::p-1:0:0:0'
                              , 'children' :
                                  [ { '$id' : 'FB-0:2::p-1:0:0:0.0'
                                    , 'value' :
                                        { 'edit' : '2008/05/01' }
                                    }
                                  , { '$id' : 'FB-0:2::p-1:0:0:0.1'
                                    , 'value' :
                                        { 'edit' : '2008/05/01' }
                                    }
                                  ]
                              , 'value' :
                                  { 'edit' : '' }
                              }
                            , { '$id' : 'FB-0:2::p-1:0:0:1'
                              , 'value' :
                                  { 'edit' : 'Himmelfahrt' }
                              }
                            ]
                        , 'value' :
                            { 'edit' :
                                {}
                            }
                        }
                      ]
                  , 'value' :
                      {}
                  }
                , { '$id' : 'FB-0:2::p-2:0'
                  , 'children' :
                      [ { '$id' : 'FB-0:2::p-2:0:0'
                        , 'children' :
                            [ { '$id' : 'FB-0:2::p-2:0:0:0'
                              , 'value' :
                                  { 'edit' : 'Tanzer' }
                              }
                            , { '$id' : 'FB-0:2::p-2:0:0:1'
                              , 'value' :
                                  { 'edit' : 'Laurens' }
                              }
                            , { '$id' : 'FB-0:2::p-2:0:0:2'
                              , 'value' :
                                  { 'edit' : 'William II' }
                              }
                            , { '$id' : 'FB-0:2::p-2:0:0:3'
                              , 'value' :
                                  {}
                              }
                            ]
                        , 'value' :
                            { 'edit' :
                                {}
                            }
                        }
                      , { '$id' : 'FB-0:2::p-2:0:1'
                        , 'value' :
                            { 'edit' : 'AUT' }
                        }
                      , { '$id' : 'FB-0:2::p-2:0:2'
                        , 'value' :
                            { 'edit' : '29676' }
                        }
                      ]
                  , 'value' :
                      { 'edit' :
                          {}
                      }
                  }
                , { '$id' : 'FB-0:2::p-3:0'
                  , 'value' :
                      {}
                  }
                , { '$id' : 'FB-0:2::p-3:1'
                  , 'value' :
                      {}
                  }
                ]
            , 'value' :
                {}
            }
          ]
      , 'value' :
          {}
      }

    >>> w_sig_map = {}
    >>> for w in gv.entity_children () :
    ...     wh = w.elem.form_hash (w)
    ...     w_sig_map [w.id] = w, w.sig, wh

    >>> for id, (i, i_sig) in sorted (g_sig_map.iteritems ()) :
    ...    (w, w_sig, wh) = w_sig_map [id]
    ...    print i.elem, i.sid == wh, i_sig == w_sig
    ...    print "  >", i.sid
    ...    print "  <", wh
    ...    print "  >", i_sig
    ...    print "  <", w_sig
    <Entity FB-0 'Boat' 'GTW.OMP.SRM.Boat'> True True
      > 3VDfUb:0kn9ux5Abs2QtfjSwttsyL6T7BTPRJw
      < 3VDfUb:0kn9ux5Abs2QtfjSwttsyL6T7BTPRJw
      > (((u'pid', None), (u'cid', None), 'FB-0', 'GTW.OMP.SRM.Boat'), ('FB-0:0:0', 'left'), ('FB-0:0:1', 'nation', u''), ('FB-0:0:2', 'sail_number', u''), ('FB-0:1:0', 'name', u''), ('FB-0:1:1', 'sail_number_x', u''), 0)
      < (((u'pid', None), (u'cid', None), 'FB-0', 'GTW.OMP.SRM.Boat'), ('FB-0:0:0', 'left'), ('FB-0:0:1', 'nation', u''), ('FB-0:0:2', 'sail_number', u''), ('FB-0:1:0', 'name', u''), ('FB-0:1:1', 'sail_number_x', u''), 0)
    <Field_Entity FB-0:0:0 'left' 'GTW.OMP.SRM.Boat_Class'> True True
      > 2SMjmpittgN68fuUf1yK7xN-uRxHK4q2kDJOlA
      < 2SMjmpittgN68fuUf1yK7xN-uRxHK4q2kDJOlA
      > (((u'pid', None), (u'cid', None), 'FB-0:0:0', 'GTW.OMP.SRM.Boat_Class'), ('FB-0:0:0:0', 'name', u''), 0)
      < (((u'pid', None), (u'cid', None), 'FB-0:0:0', 'GTW.OMP.SRM.Boat_Class'), ('FB-0:0:0:0', 'name', u''), 0)
    <Entity_Link FB-0:2::0 'Boat_in_Regatta' 'GTW.OMP.SRM.Boat_in_Regatta'> True True
      > UtcUyWMVWMEfZeA9RSCEBsCSnrbfeND6VYcmIw
      < UtcUyWMVWMEfZeA9RSCEBsCSnrbfeND6VYcmIw
      > (((u'pid', None), (u'cid', None), 'FB-0:2::0', 'GTW.OMP.SRM.Boat_in_Regatta'), ('FB-0:2::0-0', u'left'), ('FB-0:2::0-1:0', 'right'), ('FB-0:2::0-2:0', 'skipper'), ('FB-0:2::0-3:0', 'place', u''), ('FB-0:2::0-3:1', 'points', u''), 0)
      < (((u'pid', None), (u'cid', None), 'FB-0:2::0', 'GTW.OMP.SRM.Boat_in_Regatta'), ('FB-0:2::0-0', u'left'), ('FB-0:2::0-1:0', 'right'), ('FB-0:2::0-2:0', 'skipper'), ('FB-0:2::0-3:0', 'place', u''), ('FB-0:2::0-3:1', 'points', u''), 0)
    <Field_Role_Hidden FB-0:2::0-0 u'left' 'GTW.OMP.SRM.Boat'> True True
      > emH:n2fr5Vojp8:mNyEhadFeTvrt0Hb26l7S4Q
      < emH:n2fr5Vojp8:mNyEhadFeTvrt0Hb26l7S4Q
      > (((u'pid', None), (u'cid', None), 'FB-0:2::0-0', 'GTW.OMP.SRM.Boat'), 0)
      < (((u'pid', None), (u'cid', None), 'FB-0:2::0-0', 'GTW.OMP.SRM.Boat'), 0)
    <Field_Entity FB-0:2::0-1:0 'right' 'GTW.OMP.SRM.Regatta'> True True
      > n4dFoUTWL2ZKZ1e-igGdLTtkVfW3LOxorspVfw
      < n4dFoUTWL2ZKZ1e-igGdLTtkVfW3LOxorspVfw
      > (((u'pid', None), (u'cid', None), 'FB-0:2::0-1:0', 'GTW.OMP.SRM.Regatta'), ('FB-0:2::0-1:0:0', 'left'), 0)
      < (((u'pid', None), (u'cid', None), 'FB-0:2::0-1:0', 'GTW.OMP.SRM.Regatta'), ('FB-0:2::0-1:0:0', 'left'), 0)
    <Field_Entity FB-0:2::0-1:0:0 'left' 'GTW.OMP.SRM.Regatta_Event'> True True
      > :Zy-KiCVwPDIlN-Zvcq7gVx6E2rK0frgII402w
      < :Zy-KiCVwPDIlN-Zvcq7gVx6E2rK0frgII402w
      > (((u'pid', None), (u'cid', None), 'FB-0:2::0-1:0:0', 'GTW.OMP.SRM.Regatta_Event'), ('FB-0:2::0-1:0:0:0', 'date', (('FB-0:2::0-1:0:0:0.0', 'start', u''), ('FB-0:2::0-1:0:0:0.1', 'finish', u''))), ('FB-0:2::0-1:0:0:1', 'name', u''), 0)
      < (((u'pid', None), (u'cid', None), 'FB-0:2::0-1:0:0', 'GTW.OMP.SRM.Regatta_Event'), ('FB-0:2::0-1:0:0:0', 'date', (('FB-0:2::0-1:0:0:0.0', 'start', u''), ('FB-0:2::0-1:0:0:0.1', 'finish', u''))), ('FB-0:2::0-1:0:0:1', 'name', u''), 0)
    <Field_Entity FB-0:2::0-2:0 'skipper' 'GTW.OMP.SRM.Sailor'> True True
      > olYDjjANTpCXJXfp80i93QNzK2-ZYMVkSmrv:w
      < olYDjjANTpCXJXfp80i93QNzK2-ZYMVkSmrv:w
      > (((u'pid', None), (u'cid', None), 'FB-0:2::0-2:0', 'GTW.OMP.SRM.Sailor'), ('FB-0:2::0-2:0:0', 'left'), ('FB-0:2::0-2:0:1', 'nation', u''), ('FB-0:2::0-2:0:2', 'mna_number', u''), 0)
      < (((u'pid', None), (u'cid', None), 'FB-0:2::0-2:0', 'GTW.OMP.SRM.Sailor'), ('FB-0:2::0-2:0:0', 'left'), ('FB-0:2::0-2:0:1', 'nation', u''), ('FB-0:2::0-2:0:2', 'mna_number', u''), 0)
    <Field_Entity FB-0:2::0-2:0:0 'left' 'GTW.OMP.PAP.Person'> True True
      > Z:YWrkrkIu19OHcrW0W6DFmkEXuuZ7TAjiV5qQ
      < Z:YWrkrkIu19OHcrW0W6DFmkEXuuZ7TAjiV5qQ
      > (((u'pid', None), (u'cid', None), 'FB-0:2::0-2:0:0', 'GTW.OMP.PAP.Person'), ('FB-0:2::0-2:0:0:0', 'last_name', u''), ('FB-0:2::0-2:0:0:1', 'first_name', u''), ('FB-0:2::0-2:0:0:2', 'middle_name', u''), ('FB-0:2::0-2:0:0:3', 'title', u''), 0)
      < (((u'pid', None), (u'cid', None), 'FB-0:2::0-2:0:0', 'GTW.OMP.PAP.Person'), ('FB-0:2::0-2:0:0:0', 'last_name', u''), ('FB-0:2::0-2:0:0:1', 'first_name', u''), ('FB-0:2::0-2:0:0:2', 'middle_name', u''), ('FB-0:2::0-2:0:0:3', 'title', u''), 0)

    >>> em  = PAP.Email ("laurens.tanzer@gmail.com")
    >>> phe = PAP.Person_has_Email (p, em)
    >>> scope.commit ()
    >>> fp  = Form ("FP", children = [xl])
    >>> fip = fp (PAP.Person, p)

    >>> for i in fip.transitive_iter () :
    ...     print i.elem, sorted ((i.value or {}).iteritems ())
    <Form FP> [('sid', 0)]
    <Entity FP-0 'Person' 'GTW.OMP.PAP.Person'> [(u'init', {'pid': 3, 'cid': 13}), ('sid', 'vxYJv8BmTKSxB29Aesc7g78eHgRFld4VeZ9gGA')]
    <Fieldset FP-0:0 u'primary'> []
    <Field FP-0:0:0 'last_name'> [(u'init', u'Tanzer')]
    <Field FP-0:0:1 'first_name'> [(u'init', u'Laurens')]
    <Field FP-0:0:2 'middle_name'> [(u'init', u'w.')]
    <Field FP-0:0:3 'title'> []
    <Fieldset FP-0:1 u'necessary'> []
    <Field FP-0:1:0 'sex'> []
    <Fieldset FP-0:2 u'optional'> []
    <Field_Composite FP-0:2:0 'lifetime' 'MOM.Date_Interval'> []
    <Field FP-0:2:0.0 'start'> []
    <Field FP-0:2:0.1 'finish'> []
    <Field FP-0:2:1 'salutation'> []
    <Entity_List FP-0:3 'Person_has_Address' <Entity_Link FP-0:3::p 'Person_has_Address' 'GTW.OMP.PAP.Person_has_Address'>> []
    <Entity_List FP-0:4 'Person_has_Email' <Entity_Link FP-0:4::p 'Person_has_Email' 'GTW.OMP.PAP.Person_has_Email'>> []
    <Entity_Link FP-0:4::0 'Person_has_Email' 'GTW.OMP.PAP.Person_has_Email'> [(u'init', {'pid': 9, 'cid': 19}), ('sid', 'PBIMhIxHY22pBYGyYmS7CYZI8GaZgT23usy8VA')]
    <Field_Role_Hidden FP-0:4::0-0 u'left' 'GTW.OMP.PAP.Person'> [(u'init', {'pid': 3, 'cid': 13}), ('sid', 'wKjvBWwkYT1t4GwlOdZNiM6uMD9JjbNM5Q:d7Q')]
    <Fieldset FP-0:4::0-1 u'primary'> []
    <Field_Entity FP-0:4::0-1:0 'right' 'GTW.OMP.PAP.Email'> [(u'init', {'pid': 8, 'cid': 18}), ('sid', 'gbhf0Xv80pbhGMzTD1uFjuKXtTP:FU1XGZpGBQ')]
    <Field FP-0:4::0-1:0:0 'address'> [(u'init', u'laurens.tanzer@gmail.com')]
    <Fieldset FP-0:4::0-2 u'optional'> []
    <Field FP-0:4::0-2:0 'desc'> []
    <Entity_List FP-0:5 'Person_has_Phone' <Entity_Link FP-0:5::p 'Person_has_Phone' 'GTW.OMP.PAP.Person_has_Phone'>> []

    >>> for i in fip.transitive_iter () :
    ...     e = i.elem
    ...     print e.__class__.__name__, e._name, getattr (e, "ui_name", ""), repr (getattr (e, "description", "").replace (NL, " ")), e.renderer
    Form None  u'' afs_div_seq
    Entity Person Person u'' afs_div_seq
    Fieldset primary  u'' afs_div_seq
    Field last_name Last name u'Last name of person' None
    Field first_name First name u'First name of person' None
    Field middle_name Middle name u'Middle name of person' None
    Field title Academic title u'Academic title.' None
    Fieldset necessary  u'' afs_div_seq
    Field sex Sex u'Sex of a person.' None
    Fieldset optional  u'' afs_div_seq
    Field_Composite lifetime Lifetime u'Date of birth [`start`] (and death [`finish`])' afs_div_seq
    Field start Start u'Start date of interval' None
    Field finish Finish u'Finish date of interval' None
    Field salutation Salutation u'Salutation to be used when communicating with person (e.g., in a letter or email).' None
    Entity_List Person_has_Address Person_has_Address u'' afs_div_seq
    Entity_List Person_has_Email Person_has_Email u'' afs_div_seq
    Entity_Link Person_has_Email Person_has_Email u'' afs_div_seq
    Field_Role_Hidden left Person u'' afs_div_seq
    Fieldset primary  u'' afs_div_seq
    Field_Entity right Email u'Email address of person' afs_div_seq
    Field address Email address u'Email address (including domain)' None
    Fieldset optional  u'' afs_div_seq
    Field desc Description u'Short description of the link' None
    Entity_List Person_has_Phone Person_has_Phone u'' afs_div_seq

"""

_entity_links_group = """
    >>> scope = Scaffold.scope ("hps://") # doctest:+ELLIPSIS
    Creating new scope MOMT__...
    >>> from _GTW._AFS._MOM import Spec
    >>> S = Spec.Entity (include_links = ("addresses", ), entity_links_group = "Entity_Links_Group")
    >>> x = S (scope.PAP.Person._etype)
    >>> print repr (x)
    <Entity None 'Person' 'GTW.OMP.PAP.Person'>
     <Fieldset None u'primary'>
      <Field None 'last_name'>
      <Field None 'first_name'>
      <Field None 'middle_name'>
      <Field None 'title'>
     <Fieldset None u'necessary'>
      <Field None 'sex'>
     <Fieldset None u'optional'>
      <Field_Composite None 'lifetime' 'MOM.Date_Interval'>
       <Field None 'start'>
       <Field None 'finish'>
      <Field None 'salutation'>
     <Group None>
      <Entity_List None 'Person_has_Address' <Entity_Link None 'Person_has_Address' 'GTW.OMP.PAP.Person_has_Address'>>
       <Entity_Link None 'Person_has_Address' 'GTW.OMP.PAP.Person_has_Address'>
        <Field_Role_Hidden None u'left' 'GTW.OMP.PAP.Person'>
        <Fieldset None u'primary'>
         <Field_Entity None 'right' 'GTW.OMP.PAP.Address'>
          <Field None 'street'>
          <Field None 'zip'>
          <Field None 'city'>
          <Field None 'country'>
        <Fieldset None u'optional'>
         <Field None 'desc'>
    >>> print repr (Form ("ELG", children = [x]))
    <Form ELG>
     <Entity ELG-0 'Person' 'GTW.OMP.PAP.Person'>
      <Fieldset ELG-0:0 u'primary'>
       <Field ELG-0:0:0 'last_name'>
       <Field ELG-0:0:1 'first_name'>
       <Field ELG-0:0:2 'middle_name'>
       <Field ELG-0:0:3 'title'>
      <Fieldset ELG-0:1 u'necessary'>
       <Field ELG-0:1:0 'sex'>
      <Fieldset ELG-0:2 u'optional'>
       <Field_Composite ELG-0:2:0 'lifetime' 'MOM.Date_Interval'>
        <Field ELG-0:2:0.0 'start'>
        <Field ELG-0:2:0.1 'finish'>
       <Field ELG-0:2:1 'salutation'>
      <Group ELG-0:3>
       <Entity_List ELG-0:3:0 'Person_has_Address' <Entity_Link ELG-0:3:0::p 'Person_has_Address' 'GTW.OMP.PAP.Person_has_Address'>>
        <Entity_Link ELG-0:3:0::p 'Person_has_Address' 'GTW.OMP.PAP.Person_has_Address'>
         <Field_Role_Hidden ELG-0:3:0::p-0 u'left' 'GTW.OMP.PAP.Person'>
         <Fieldset ELG-0:3:0::p-1 u'primary'>
          <Field_Entity ELG-0:3:0::p-1:0 'right' 'GTW.OMP.PAP.Address'>
           <Field ELG-0:3:0::p-1:0:0 'street'>
           <Field ELG-0:3:0::p-1:0:1 'zip'>
           <Field ELG-0:3:0::p-1:0:2 'city'>
           <Field ELG-0:3:0::p-1:0:3 'country'>
         <Fieldset ELG-0:3:0::p-2 u'optional'>
          <Field ELG-0:3:0::p-2:0 'desc'>
"""
from   _GTW.__test__.model      import *
from   _GTW._AFS._MOM.Element   import Form
from   _GTW._AFS.Instance       import Instance
from   _GTW._AFS.Value          import Value

from   _TFL.Formatter           import Formatter

formatted = Formatter (width = 240)

Instance.sort_json = True

### `json_edit` and `json_copy` copied from output of::
###     /usr/bin/js -s -f GTW/AFS/Elements.test
json_edit = """\
{"$id":"FB","sid":0,"$child_ids":["FB-0","FB-0:2::0"],"FB-0":{"init":{"cid":2,"pid":2},"sid":"LjJ-MkYSz6QxselaD8NeT-5G:2a5YHFTbpYNig","$id":"FB-0","$child_ids":["FB-0:0:0","FB-0:0:1","FB-0:0:2","FB-0:1:0","FB-0:1:1"],"edit":{"cid":2,"pid":2},"FB-0:0:0":{"init":{"cid":1,"pid":1},"sid":"qPzMz88f1x3RjbWOPHj4PR2ZthTO:EW:MNddnA","$id":"FB-0:0:0","$child_ids":["FB-0:0:0:0"],"edit":{"cid":1,"pid":1},"anchor_id":"FB-0","FB-0:0:0:0":{"init":"Optimist"}},"FB-0:0:1":{"init":"AUT"},"FB-0:0:2":{"init":"1107"},"FB-0:1:0":{"init":""},"FB-0:1:1":{"init":""}},"FB-0:2::0":{"init":{"cid":7,"pid":7},"sid":"z2Wp1P:S-4gBkqNEMci0tQJ-anqXaOToH7ZK7g","$id":"FB-0:2::0","$child_ids":["FB-0:2::0-0","FB-0:2::0-1:0","FB-0:2::0-2:0","FB-0:2::0-3:0","FB-0:2::0-3:1"],"edit":{"cid":7,"pid":7},"FB-0:2::0-0":{"init":{"cid":2,"pid":2},"sid":"ORsB0LFjw5hzuHauaOA1M3usp415XdhUdQ0tfQ","role_id":"FB-0","edit":{"cid":2,"pid":2}},"FB-0:2::0-1:0":{"init":{"cid":6,"pid":6},"sid":"t0nRFI5GFozOgzRVAMlfEVZeU9oCHiVfFTBuWw","$id":"FB-0:2::0-1:0","$child_ids":["FB-0:2::0-1:0:0"],"edit":{"cid":6,"pid":6},"anchor_id":"FB-0:2::0","FB-0:2::0-1:0:0":{"init":{"cid":5,"pid":5},"sid":"w6pfZ9cV126kdzebJWKIfT6QasZLd2e6dh7O4g","$id":"FB-0:2::0-1:0:0","$child_ids":["FB-0:2::0-1:0:0:0","FB-0:2::0-1:0:0:1"],"edit":{"cid":5,"pid":5},"anchor_id":"FB-0:2::0-1:0","FB-0:2::0-1:0:0:0":{"$id":"FB-0:2::0-1:0:0:0","$child_ids":["FB-0:2::0-1:0:0:0.0","FB-0:2::0-1:0:0:0.1"],"anchor_id":"FB-0:2::0-1:0:0","FB-0:2::0-1:0:0:0.0":{"init":"2008/05/01"},"FB-0:2::0-1:0:0:0.1":{"init":"2008/05/01"}},"FB-0:2::0-1:0:0:1":{"init":"Himmelfahrt"}}},"FB-0:2::0-2:0":{"init":{"cid":4,"pid":4},"sid":"eW12pOklOQqAlV9CsVuZLsdwncWDlF6FYe3Mig","$id":"FB-0:2::0-2:0","$child_ids":["FB-0:2::0-2:0:0","FB-0:2::0-2:0:1","FB-0:2::0-2:0:2"],"edit":{"cid":4,"pid":4},"anchor_id":"FB-0:2::0","FB-0:2::0-2:0:0":{"init":{"cid":3,"pid":3},"sid":"jCVvrVL7cxthrwL4:mPenABA:H4vtKSITQhTuA","$id":"FB-0:2::0-2:0:0","$child_ids":["FB-0:2::0-2:0:0:0","FB-0:2::0-2:0:0:1","FB-0:2::0-2:0:0:2","FB-0:2::0-2:0:0:3"],"edit":{"cid":3,"pid":3},"anchor_id":"FB-0:2::0-2:0","FB-0:2::0-2:0:0:0":{"init":"Tanzer"},"FB-0:2::0-2:0:0:1":{"init":"Laurens"},"FB-0:2::0-2:0:0:2":{"init":"","edit":"William"},"FB-0:2::0-2:0:0:3":{"init":""}},"FB-0:2::0-2:0:1":{"init":"AUT"},"FB-0:2::0-2:0:2":{"init":"29676"}},"FB-0:2::0-3:0":{"init":""},"FB-0:2::0-3:1":{"init":""}}}
"""
json_copy = """\
{"$id":"FB","sid":0,"$child_ids":["FB-0","FB-0:2::0"],"FB-0":{"init":{},"sid":"3VDfUb:0kn9ux5Abs2QtfjSwttsyL6T7BTPRJw","$id":"FB-0","$child_ids":["FB-0:0:0","FB-0:0:1","FB-0:0:2","FB-0:1:0","FB-0:1:1"],"edit":{},"FB-0:0:0":{"init":{},"sid":"2SMjmpittgN68fuUf1yK7xN-uRxHK4q2kDJOlA","$id":"FB-0:0:0","$child_ids":["FB-0:0:0:0"],"edit":{},"anchor_id":"FB-0","FB-0:0:0:0":{"edit":"Optimist","init":""}},"FB-0:0:1":{"edit":"AUT","init":""},"FB-0:0:2":{"edit":"1107","init":""},"FB-0:1:0":{"init":""},"FB-0:1:1":{"init":""}},"FB-0:2::0":{"init":{},"sid":"UtcUyWMVWMEfZeA9RSCEBsCSnrbfeND6VYcmIw","$id":"FB-0:2::0","$child_ids":["FB-0:2::0-0","FB-0:2::0-1:0","FB-0:2::0-2:0","FB-0:2::0-3:0","FB-0:2::0-3:1"],"edit":{},"FB-0:2::0-0":{"init":{},"sid":"emH:n2fr5Vojp8:mNyEhadFeTvrt0Hb26l7S4Q","role_id":"FB-0","edit":{}},"FB-0:2::0-1:0":{"init":{},"sid":"n4dFoUTWL2ZKZ1e-igGdLTtkVfW3LOxorspVfw","$id":"FB-0:2::0-1:0","$child_ids":["FB-0:2::0-1:0:0"],"edit":{},"anchor_id":"FB-0:2::0","FB-0:2::0-1:0:0":{"init":{},"sid":":Zy-KiCVwPDIlN-Zvcq7gVx6E2rK0frgII402w","$id":"FB-0:2::0-1:0:0","$child_ids":["FB-0:2::0-1:0:0:0","FB-0:2::0-1:0:0:1"],"edit":{},"anchor_id":"FB-0:2::0-1:0","FB-0:2::0-1:0:0:0":{"$id":"FB-0:2::0-1:0:0:0","$child_ids":["FB-0:2::0-1:0:0:0.0","FB-0:2::0-1:0:0:0.1"],"anchor_id":"FB-0:2::0-1:0:0","FB-0:2::0-1:0:0:0.0":{"edit":"2008/05/01","init":""},"FB-0:2::0-1:0:0:0.1":{"edit":"2008/05/01","init":""}},"FB-0:2::0-1:0:0:1":{"edit":"Himmelfahrt","init":""}}},"FB-0:2::0-2:0":{"init":{},"sid":"olYDjjANTpCXJXfp80i93QNzK2-ZYMVkSmrv:w","$id":"FB-0:2::0-2:0","$child_ids":["FB-0:2::0-2:0:0","FB-0:2::0-2:0:1","FB-0:2::0-2:0:2"],"edit":{},"anchor_id":"FB-0:2::0","FB-0:2::0-2:0:0":{"init":{},"sid":"Z:YWrkrkIu19OHcrW0W6DFmkEXuuZ7TAjiV5qQ","$id":"FB-0:2::0-2:0:0","$child_ids":["FB-0:2::0-2:0:0:0","FB-0:2::0-2:0:0:1","FB-0:2::0-2:0:0:2","FB-0:2::0-2:0:0:3"],"edit":{},"anchor_id":"FB-0:2::0-2:0","FB-0:2::0-2:0:0:0":{"edit":"Tanzer","init":""},"FB-0:2::0-2:0:0:1":{"edit":"Laurens","init":""},"FB-0:2::0-2:0:0:2":{"init":"","edit":"William II"},"FB-0:2::0-2:0:0:3":{"init":""}},"FB-0:2::0-2:0:1":{"edit":"AUT","init":""},"FB-0:2::0-2:0:2":{"edit":"29676","init":""}},"FB-0:2::0-3:0":{"init":""},"FB-0:2::0-3:1":{"init":""}}}
"""
json_bad  = """{"$id":"FC"}"""

__test__ = dict \
    ( AFS_Spec           = _test_code
    , Entity_Links_Group = _entity_links_group
    )

### __END__ AFS_Spec
