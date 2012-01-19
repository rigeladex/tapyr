# -*- coding: iso-8859-15 -*-
# Copyright (C) 2011-2012 Mag. Christian Tanzer All rights reserved
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
    >>> x = S (scope.PAP.Person.E_Type)
    >>> print repr (x)
    <Entity None 'Person' 'GTW.OMP.PAP.Person'>
     <Fieldset None 'primary'>
      <Field None 'last_name'>
      <Field None 'first_name'>
      <Field None 'middle_name'>
      <Field None 'title'>
     <Fieldset None 'necessary'>
      <Field None 'sex'>
     <Fieldset None 'optional'>
      <Field_Composite None 'lifetime' 'MOM.Date_Interval'>
       <Field None 'start'>
       <Field None 'finish'>
      <Field None 'salutation'>

    >>> SL = Spec.Entity (include_links = ("addresses", "emails", "phones"))
    >>> xl = SL (scope.PAP.Person.E_Type)
    >>> print repr (xl)
    <Entity None 'Person' 'GTW.OMP.PAP.Person'>
     <Fieldset None 'primary'>
      <Field None 'last_name'>
      <Field None 'first_name'>
      <Field None 'middle_name'>
      <Field None 'title'>
     <Fieldset None 'necessary'>
      <Field None 'sex'>
     <Fieldset None 'optional'>
      <Field_Composite None 'lifetime' 'MOM.Date_Interval'>
       <Field None 'start'>
       <Field None 'finish'>
      <Field None 'salutation'>
     <Entity_List None 'Person_has_Address' <Entity_Link None 'Person_has_Address' 'GTW.OMP.PAP.Person_has_Address'>>
      <Entity_Link None 'Person_has_Address' 'GTW.OMP.PAP.Person_has_Address'>
       <Field_Role_Hidden None 'left' 'GTW.OMP.PAP.Person'>
       <Fieldset None 'primary'>
        <Field_Entity None 'right' 'GTW.OMP.PAP.Address'>
         <Field None 'street'>
         <Field None 'zip'>
         <Field None 'city'>
         <Field None 'country'>
       <Fieldset None 'optional'>
        <Field None 'desc'>
     <Entity_List None 'Person_has_Email' <Entity_Link None 'Person_has_Email' 'GTW.OMP.PAP.Person_has_Email'>>
      <Entity_Link None 'Person_has_Email' 'GTW.OMP.PAP.Person_has_Email'>
       <Field_Role_Hidden None 'left' 'GTW.OMP.PAP.Person'>
       <Fieldset None 'primary'>
        <Field_Entity None 'right' 'GTW.OMP.PAP.Email'>
         <Field None 'address'>
       <Fieldset None 'optional'>
        <Field None 'desc'>
     <Entity_List None 'Person_has_Phone' <Entity_Link None 'Person_has_Phone' 'GTW.OMP.PAP.Person_has_Phone'>>
      <Entity_Link None 'Person_has_Phone' 'GTW.OMP.PAP.Person_has_Phone'>
       <Field_Role_Hidden None 'left' 'GTW.OMP.PAP.Person'>
       <Fieldset None 'primary'>
        <Field_Entity None 'right' 'GTW.OMP.PAP.Phone'>
         <Field None 'country_code'>
         <Field None 'area_code'>
         <Field None 'number'>
        <Field None 'extension'>
       <Fieldset None 'optional'>
        <Field None 'desc'>

    >>> NL = chr (10)
    >>> for e in xl.transitive_iter () :
    ...   print e.__class__.__name__, e._name, getattr (e, "ui_name", None), repr (getattr (e, "description", "").replace (NL, " ")), e.renderer
    Entity Person Person u'Model a person.' afs_div_seq
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
    Entity_List Person_has_Address Person_has_Address u'Model the link between a person and an address' afs_div_seq
    Entity_Link Person_has_Address Person_has_Address u'Model the link between a person and an address' afs_div_seq
    Field_Role_Hidden left Person u'' afs_div_seq
    Fieldset primary None u'' afs_div_seq
    Field_Entity right Address u'Address where person lives or works' afs_div_seq
    Field street Street u'Street (or place) and house number' None
    Field zip Zip code u'Zip code of address' None
    Field city City u'City, town, or village' None
    Field country Country u'Country' None
    Fieldset optional None u'' afs_div_seq
    Field desc Description u'Short description of the link' None
    Entity_List Person_has_Email Person_has_Email u'Model the link between a person and an email address' afs_div_seq
    Entity_Link Person_has_Email Person_has_Email u'Model the link between a person and an email address' afs_div_seq
    Field_Role_Hidden left Person u'' afs_div_seq
    Fieldset primary None u'' afs_div_seq
    Field_Entity right Email u'Email address of person' afs_div_seq
    Field address Email address u'Email address (including domain)' None
    Fieldset optional None u'' afs_div_seq
    Field desc Description u'Short description of the link' None
    Entity_List Person_has_Phone Person_has_Phone u'Model the link between a person and a phone number' afs_div_seq
    Entity_Link Person_has_Phone Person_has_Phone u'Model the link between a person and a phone number' afs_div_seq
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
    >>> y = T (scope.SWP.Page.E_Type)
    >>> print repr (y)
    <Entity None 'Page' 'GTW.OMP.SWP.Page'>
     <Fieldset None 'primary'>
      <Field None 'perma_name'>
     <Fieldset None 'required'>
      <Field None 'text'>
     <Fieldset None 'necessary'>
      <Field None 'short_title'>
      <Field None 'title'>
     <Fieldset None 'optional'>
      <Field_Composite None 'date' 'MOM.Date_Interval_N'>
       <Field None 'start'>
       <Field None 'finish'>
      <Field None 'format'>
      <Field None 'head_line'>
      <Field None 'hidden'>
      <Field None 'prio'>
     <Entity_List None 'Event' <Entity_Link None 'Event' 'GTW.OMP.EVT.Event'>>
      <Entity_Link None 'Event' 'GTW.OMP.EVT.Event'>
       <Field_Role_Hidden None 'left' 'GTW.OMP.SWP.Page'>
       <Fieldset None 'primary'>
        <Field_Composite None 'date' 'MOM.Date_Interval'>
         <Field None 'start'>
         <Field None 'finish'>
        <Field_Composite None 'time' 'MOM.Time_Interval'>
         <Field None 'start'>
         <Field None 'finish'>
        <Field_Entity None 'calendar' 'GTW.OMP.EVT.Calendar'>
         <Field None 'name'>
       <Fieldset None 'optional'>
        <Field None 'detail'>
        <Field None 'short_title'>
       <Entity_Link None 'Recurrence_Spec' 'GTW.OMP.EVT.Recurrence_Spec'>
        <Field_Role_Hidden None 'left' 'GTW.OMP.EVT.Event'>
        <Fieldset None 'optional'>
         <Field None 'dates'>
         <Field None 'date_exceptions'>
        <Entity_List None 'Recurrence_Rule' <Entity_Link None 'Recurrence_Rule' 'GTW.OMP.EVT.Recurrence_Rule'>>
         <Entity_Link None 'Recurrence_Rule' 'GTW.OMP.EVT.Recurrence_Rule'>
          <Field_Role_Hidden None 'left' 'GTW.OMP.EVT.Recurrence_Spec'>
          <Fieldset None 'primary'>
           <Field None 'is_exception'>
           <Field None 'desc'>
          <Fieldset None 'optional'>
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
      <Fieldset F-0:0 'primary'>
       <Field F-0:0:0 'perma_name'>
      <Fieldset F-0:1 'required'>
       <Field F-0:1:0 'text'>
      <Fieldset F-0:2 'necessary'>
       <Field F-0:2:0 'short_title'>
       <Field F-0:2:1 'title'>
      <Fieldset F-0:3 'optional'>
       <Field_Composite F-0:3:0 'date' 'MOM.Date_Interval_N'>
        <Field F-0:3:0.0 'start'>
        <Field F-0:3:0.1 'finish'>
       <Field F-0:3:1 'format'>
       <Field F-0:3:2 'head_line'>
       <Field F-0:3:3 'hidden'>
       <Field F-0:3:4 'prio'>
      <Entity_List F-0:4 'Event' <Entity_Link F-0:4::p 'Event' 'GTW.OMP.EVT.Event'>>
       <Entity_Link F-0:4::p 'Event' 'GTW.OMP.EVT.Event'>
        <Field_Role_Hidden F-0:4::p-0 'left' 'GTW.OMP.SWP.Page'>
        <Fieldset F-0:4::p-1 'primary'>
         <Field_Composite F-0:4::p-1:0 'date' 'MOM.Date_Interval'>
          <Field F-0:4::p-1:0.0 'start'>
          <Field F-0:4::p-1:0.1 'finish'>
         <Field_Composite F-0:4::p-1:1 'time' 'MOM.Time_Interval'>
          <Field F-0:4::p-1:1.0 'start'>
          <Field F-0:4::p-1:1.1 'finish'>
         <Field_Entity F-0:4::p-1:2 'calendar' 'GTW.OMP.EVT.Calendar'>
          <Field F-0:4::p-1:2:0 'name'>
        <Fieldset F-0:4::p-2 'optional'>
         <Field F-0:4::p-2:0 'detail'>
         <Field F-0:4::p-2:1 'short_title'>
        <Entity_Link F-0:4::p-3 'Recurrence_Spec' 'GTW.OMP.EVT.Recurrence_Spec'>
         <Field_Role_Hidden F-0:4::p-3:0 'left' 'GTW.OMP.EVT.Event'>
         <Fieldset F-0:4::p-3:1 'optional'>
          <Field F-0:4::p-3:1:0 'dates'>
          <Field F-0:4::p-3:1:1 'date_exceptions'>
         <Entity_List F-0:4::p-3:2 'Recurrence_Rule' <Entity_Link F-0:4::p-3:2::p 'Recurrence_Rule' 'GTW.OMP.EVT.Recurrence_Rule'>>
          <Entity_Link F-0:4::p-3:2::p 'Recurrence_Rule' 'GTW.OMP.EVT.Recurrence_Rule'>
           <Field_Role_Hidden F-0:4::p-3:2::p-0 'left' 'GTW.OMP.EVT.Recurrence_Spec'>
           <Fieldset F-0:4::p-3:2::p-1 'primary'>
            <Field F-0:4::p-3:2::p-1:0 'is_exception'>
            <Field F-0:4::p-3:2::p-1:1 'desc'>
           <Fieldset F-0:4::p-3:2::p-2 'optional'>
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
      <Fieldset X-0:0 'primary'>
       <Field X-0:0:0 'last_name'>
       <Field X-0:0:1 'first_name'>
       <Field X-0:0:2 'middle_name'>
       <Field X-0:0:3 'title'>
      <Fieldset X-0:1 'necessary'>
       <Field X-0:1:0 'sex'>
      <Fieldset X-0:2 'optional'>
       <Field_Composite X-0:2:0 'lifetime' 'MOM.Date_Interval'>
        <Field X-0:2:0.0 'start'>
        <Field X-0:2:0.1 'finish'>
       <Field X-0:2:1 'salutation'>
     <Entity X-1 'Page' 'GTW.OMP.SWP.Page'>
      <Fieldset X-1:0 'primary'>
       <Field X-1:0:0 'perma_name'>
      <Fieldset X-1:1 'required'>
       <Field X-1:1:0 'text'>
      <Fieldset X-1:2 'necessary'>
       <Field X-1:2:0 'short_title'>
       <Field X-1:2:1 'title'>
      <Fieldset X-1:3 'optional'>
       <Field_Composite X-1:3:0 'date' 'MOM.Date_Interval_N'>
        <Field X-1:3:0.0 'start'>
        <Field X-1:3:0.1 'finish'>
       <Field X-1:3:1 'format'>
       <Field X-1:3:2 'head_line'>
       <Field X-1:3:3 'hidden'>
       <Field X-1:3:4 'prio'>
      <Entity_List X-1:4 'Event' <Entity_Link X-1:4::p 'Event' 'GTW.OMP.EVT.Event'>>
       <Entity_Link X-1:4::p 'Event' 'GTW.OMP.EVT.Event'>
        <Field_Role_Hidden X-1:4::p-0 'left' 'GTW.OMP.SWP.Page'>
        <Fieldset X-1:4::p-1 'primary'>
         <Field_Composite X-1:4::p-1:0 'date' 'MOM.Date_Interval'>
          <Field X-1:4::p-1:0.0 'start'>
          <Field X-1:4::p-1:0.1 'finish'>
         <Field_Composite X-1:4::p-1:1 'time' 'MOM.Time_Interval'>
          <Field X-1:4::p-1:1.0 'start'>
          <Field X-1:4::p-1:1.1 'finish'>
         <Field_Entity X-1:4::p-1:2 'calendar' 'GTW.OMP.EVT.Calendar'>
          <Field X-1:4::p-1:2:0 'name'>
        <Fieldset X-1:4::p-2 'optional'>
         <Field X-1:4::p-2:0 'detail'>
         <Field X-1:4::p-2:1 'short_title'>
        <Entity_Link X-1:4::p-3 'Recurrence_Spec' 'GTW.OMP.EVT.Recurrence_Spec'>
         <Field_Role_Hidden X-1:4::p-3:0 'left' 'GTW.OMP.EVT.Event'>
         <Fieldset X-1:4::p-3:1 'optional'>
          <Field X-1:4::p-3:1:0 'dates'>
          <Field X-1:4::p-3:1:1 'date_exceptions'>
         <Entity_List X-1:4::p-3:2 'Recurrence_Rule' <Entity_Link X-1:4::p-3:2::p 'Recurrence_Rule' 'GTW.OMP.EVT.Recurrence_Rule'>>
          <Entity_Link X-1:4::p-3:2::p 'Recurrence_Rule' 'GTW.OMP.EVT.Recurrence_Rule'>
           <Field_Role_Hidden X-1:4::p-3:2::p-0 'left' 'GTW.OMP.EVT.Recurrence_Spec'>
           <Fieldset X-1:4::p-3:2::p-1 'primary'>
            <Field X-1:4::p-3:2::p-1:0 'is_exception'>
            <Field X-1:4::p-3:2::p-1:1 'desc'>
           <Fieldset X-1:4::p-3:2::p-2 'optional'>
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
      <Fieldset FB-0:0 'primary'>
       <Field_Entity FB-0:0:0 'left' 'GTW.OMP.SRM.Boat_Class'>
        <Field FB-0:0:0:0 'name'>
       <Field FB-0:0:1 'nation'>
       <Field FB-0:0:2 'sail_number'>
       <Field FB-0:0:3 'sail_number_x'>
      <Fieldset FB-0:1 'optional'>
       <Field FB-0:1:0 'name'>
      <Entity_List FB-0:2 'Boat_in_Regatta' <Entity_Link FB-0:2::p 'Boat_in_Regatta' 'GTW.OMP.SRM.Boat_in_Regatta'>>
       <Entity_Link FB-0:2::p 'Boat_in_Regatta' 'GTW.OMP.SRM.Boat_in_Regatta'>
        <Field_Role_Hidden FB-0:2::p-0 'left' 'GTW.OMP.SRM.Boat'>
        <Fieldset FB-0:2::p-1 'primary'>
         <Field_Entity FB-0:2::p-1:0 'right' 'GTW.OMP.SRM.Regatta'>
          <Field_Entity FB-0:2::p-1:0:0 'left' 'GTW.OMP.SRM.Regatta_Event'>
           <Field FB-0:2::p-1:0:0:0 'name'>
           <Field_Composite FB-0:2::p-1:0:0:1 'date' 'MOM.Date_Interval_C'>
            <Field FB-0:2::p-1:0:0:1.0 'start'>
            <Field FB-0:2::p-1:0:0:1.1 'finish'>
        <Fieldset FB-0:2::p-2 'required'>
         <Field_Entity FB-0:2::p-2:0 'skipper' 'GTW.OMP.SRM.Sailor'>
          <Field_Entity FB-0:2::p-2:0:0 'left' 'GTW.OMP.PAP.Person'>
           <Field FB-0:2::p-2:0:0:0 'last_name'>
           <Field FB-0:2::p-2:0:0:1 'first_name'>
           <Field FB-0:2::p-2:0:0:2 'middle_name'>
           <Field FB-0:2::p-2:0:0:3 'title'>
          <Field FB-0:2::p-2:0:1 'nation'>
          <Field FB-0:2::p-2:0:2 'mna_number'>
          <Field_Entity FB-0:2::p-2:0:3 'club' 'GTW.OMP.SRM.Club'>
           <Field FB-0:2::p-2:0:3:0 'name'>
        <Fieldset FB-0:2::p-3 'optional'>
         <Field FB-0:2::p-3:0 'place'>
         <Field FB-0:2::p-3:1 'points'>

    >>> PAP = scope.PAP
    >>> SRM = scope.SRM
    >>> bc  = SRM.Boat_Class ("Optimist", max_crew = 1)
    >>> b   = SRM.Boat.instance_or_new (u"Optimist", u"AUT", u"1107", raw = True)
    >>> p   = PAP.Person.instance_or_new (u"Tanzer", u"Laurens")
    >>> s   = SRM.Sailor.instance_or_new (p, nation = u"AUT", mna_number = u"29676", raw = True)
    >>> rev = SRM.Regatta_Event (u"Himmelfahrt", dict (start = u"20080501", raw = True), raw = True)
    >>> reg = SRM.Regatta_C (rev, boat_class = bc)
    >>> bir = SRM.Boat_in_Regatta (b, reg, skipper = s)

    >>> scope.commit ()
    >>> fi  = fb (SRM.Boat, b)
    >>> fic = fb (SRM.Boat, b, copy = True)

    >>> ff_ln = fb ['FB-0:2::0-2:0:0:0']
    >>> print ff_ln
    <Field FB-0:2::p-2:0:0:0 'last_name'>
    >>> print ff_ln.name, ff_ln.required
    last_name True
    >>> print formatted (ff_ln.kw)
    { 'kind' : 'primary'
    , 'label' : 'Last name'
    , 'name' : 'last_name'
    }

    >>> print formatted (fi.as_json_cargo, level = 1)
      { '$id' : 'FB'
      , 'children' :
          [ { '$id' : 'FB-0'
            , 'allow_new' : True
            , 'children' :
                [ { '$id' : 'FB-0:0'
                  , 'children' :
                      [ { '$id' : 'FB-0:0:0'
                        , 'allow_new' : True
                        , 'children' :
                            [ { '$id' : 'FB-0:0:0:0'
                              , 'completer' :
                                  { 'entity_p' : True
                                  , 'names' :
    [ 'name' ]
                                  , 'treshold' : 1
                                  }
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
                                , 'uid' : 'Optimist'
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
                        , 'completer' :
                            { 'entity_p' : True
                            , 'names' :
                                [ 'sail_number'
                                , 'left'
                                , 'nation'
                                , 'sail_number_x'
                                ]
                            , 'treshold' : 1
                            }
                        , 'kind' : 'primary'
                        , 'label' : 'Sail number'
                        , 'name' : 'sail_number'
                        , 'type' : 'Field'
                        , 'value' :
                            { 'init' : '1107' }
                        }
                      , { '$id' : 'FB-0:0:3'
                        , 'completer' :
                            { 'entity_p' : True
                            , 'names' :
                                [ 'sail_number_x'
                                , 'left'
                                , 'nation'
                                , 'sail_number'
                                ]
                            , 'treshold' : 1
                            }
                        , 'kind' : 'primary'
                        , 'label' : 'Sail number x'
                        , 'name' : 'sail_number_x'
                        , 'type' : 'Field'
                        , 'value' :
                            {}
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
                      ]
                  , 'collapsed' : True
                  , 'name' : 'optional'
                  , 'type' : 'Fieldset'
                  }
                , { '$id' : 'FB-0:2'
                  , 'allow_new' : True
                  , 'children' :
                      [ { '$id' : 'FB-0:2::0'
                        , 'allow_new' : True
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
                                      , 'uid' : 'Optimist, AUT 1107'
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
                                                , 'completer' :
                                                    { 'entity_p' : True
                                                    , 'names' :
                                                        [ 'name'
                                                        , 'date'
                                                        ]
                                                    , 'treshold' : 1
                                                    }
                                                , 'kind' : 'primary'
                                                , 'label' : 'Name'
                                                , 'name' : 'name'
                                                , 'required' : True
                                                , 'type' : 'Field'
                                                , 'value' :
                                                    { 'init' : 'Himmelfahrt' }
                                                }
                                              , { '$id' : 'FB-0:2::0-1:0:0:1'
                                                , 'children' :
                                                    [ { '$id' : 'FB-0:2::0-1:0:0:1.0'
                                                      , 'completer' :
                                                          { 'embedded_p' : True
                                                          , 'entity_p' : False
                                                          , 'names' :
    [ 'start' ]
                                                          , 'treshold' : 4
                                                          }
                                                      , 'kind' : 'necessary'
                                                      , 'label' : 'Start'
                                                      , 'name' : 'start'
                                                      , 'type' : 'Field'
                                                      , 'value' :
                                                          { 'init' : '2008/05/01' }
                                                      }
                                                    , { '$id' : 'FB-0:2::0-1:0:0:1.1'
                                                      , 'completer' :
                                                          { 'embedded_p' : True
                                                          , 'entity_p' : False
                                                          , 'names' :
    [ 'finish' ]
                                                          , 'treshold' : 4
                                                          }
                                                      , 'kind' : 'optional'
                                                      , 'label' : 'Finish'
                                                      , 'name' : 'finish'
                                                      , 'type' : 'Field'
                                                      , 'value' :
                                                          { 'init' : '2008/05/01' }
                                                      }
                                                    ]
                                                , 'collapsed' : True
                                                , 'completer' :
                                                    { 'entity_p' : True
                                                    , 'names' :
                                                        [ 'date'
                                                        , 'name'
                                                        ]
                                                    , 'treshold' : 1
                                                    }
                                                , 'kind' : 'primary'
                                                , 'label' : 'Date'
                                                , 'name' : 'date'
                                                , 'required' : True
                                                , 'type' : 'Field_Composite'
                                                , 'type_name' : 'MOM.Date_Interval_C'
                                                , 'value' :
                                                    {}
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
                                                  , 'uid' : 'Himmelfahrt 2008/05/01'
                                                  }
                                              , 'sid' : 'siR36p3Hsut0dtJQl-h3TjrWxG6qhX9soaq6:g'
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
                                            , 'uid' : 'Himmelfahrt 2008/05/01, Optimist'
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
                                                    { 'embedded_p' : True
                                                    , 'entity_p' : True
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
                                                    { 'embedded_p' : True
                                                    , 'entity_p' : True
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
                                                    { 'embedded_p' : True
                                                    , 'entity_p' : True
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
                                                    { 'embedded_p' : True
                                                    , 'entity_p' : False
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
                                          , 'completer' :
                                              { 'entity_p' : True
                                              , 'names' :
                                                  [ 'left'
                                                  , 'nation'
                                                  , 'mna_number'
                                                  , 'club'
                                                  ]
                                              , 'treshold' : 1
                                              }
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
                                                  , 'uid' : 'Tanzer Laurens'
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
                                          , 'completer' :
                                              { 'entity_p' : True
                                              , 'names' :
                                                  [ 'mna_number'
                                                  , 'left'
                                                  , 'nation'
                                                  , 'club'
                                                  ]
                                              , 'treshold' : 1
                                              }
                                          , 'kind' : 'primary'
                                          , 'label' : 'Mna number'
                                          , 'name' : 'mna_number'
                                          , 'type' : 'Field'
                                          , 'value' :
                                              { 'init' : '29676' }
                                          }
                                        , { '$id' : 'FB-0:2::0-2:0:3'
                                          , 'allow_new' : True
                                          , 'children' :
                                              [ { '$id' : 'FB-0:2::0-2:0:3:0'
                                                , 'completer' :
                                                    { 'entity_p' : True
                                                    , 'names' :
    [ 'name' ]
                                                    , 'treshold' : 1
                                                    }
                                                , 'kind' : 'primary'
                                                , 'label' : 'Name'
                                                , 'name' : 'name'
                                                , 'required' : True
                                                , 'type' : 'Field'
                                                , 'value' :
                                                    {}
                                                }
                                              ]
                                          , 'collapsed' : True
                                          , 'kind' : 'primary'
                                          , 'label' : 'Club'
                                          , 'name' : 'club'
                                          , 'type' : 'Field_Entity'
                                          , 'type_name' : 'GTW.OMP.SRM.Club'
                                          , 'value' :
                                              { 'init' :
                                                  { 'cid' : None
                                                  , 'pid' : None
                                                  , 'uid' : None
                                                  }
                                              , 'sid' : 'diNMsTC-2yU41VucKcBWUSQGe1b0O2mYXb8WjQ'
                                              }
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
                                            , 'uid' : 'Tanzer Laurens, AUT, 29676'
                                            }
                                        , 'sid' : 'fDjH5uIO03Wdnc5gX3D7C88Msxfp807Dd15LdA'
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
                                , 'uid' : 'Optimist, AUT 1107, Himmelfahrt 2008/05/01, Optimist'
                                }
                            , 'sid' : 'WL-78I4-zhVeNm1-xWrXjotyN8mcfb-yZGgf6A'
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
                    , 'uid' : 'Optimist, AUT 1107'
                    }
                , 'sid' : 'hr-jUx4QHTv6rHr09XNKhgpG8von21skUQ4C9Q'
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
            , 'allow_new' : True
            , 'children' :
                [ { '$id' : 'FB-0:0'
                  , 'children' :
                      [ { '$id' : 'FB-0:0:0'
                        , 'allow_new' : True
                        , 'children' :
                            [ { '$id' : 'FB-0:0:0:0'
                              , 'completer' :
                                  { 'entity_p' : True
                                  , 'names' :
    [ 'name' ]
                                  , 'treshold' : 1
                                  }
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
                        , 'completer' :
                            { 'entity_p' : True
                            , 'names' :
                                [ 'sail_number'
                                , 'left'
                                , 'nation'
                                , 'sail_number_x'
                                ]
                            , 'treshold' : 1
                            }
                        , 'kind' : 'primary'
                        , 'label' : 'Sail number'
                        , 'name' : 'sail_number'
                        , 'type' : 'Field'
                        , 'value' :
                            { 'edit' : '1107' }
                        }
                      , { '$id' : 'FB-0:0:3'
                        , 'completer' :
                            { 'entity_p' : True
                            , 'names' :
                                [ 'sail_number_x'
                                , 'left'
                                , 'nation'
                                , 'sail_number'
                                ]
                            , 'treshold' : 1
                            }
                        , 'kind' : 'primary'
                        , 'label' : 'Sail number x'
                        , 'name' : 'sail_number_x'
                        , 'type' : 'Field'
                        , 'value' :
                            {}
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
                      ]
                  , 'collapsed' : True
                  , 'name' : 'optional'
                  , 'type' : 'Fieldset'
                  }
                , { '$id' : 'FB-0:2'
                  , 'allow_new' : True
                  , 'children' :
                      [ { '$id' : 'FB-0:2::0'
                        , 'allow_new' : True
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
                                                , 'completer' :
                                                    { 'entity_p' : True
                                                    , 'names' :
                                                        [ 'name'
                                                        , 'date'
                                                        ]
                                                    , 'treshold' : 1
                                                    }
                                                , 'kind' : 'primary'
                                                , 'label' : 'Name'
                                                , 'name' : 'name'
                                                , 'required' : True
                                                , 'type' : 'Field'
                                                , 'value' :
                                                    { 'edit' : 'Himmelfahrt' }
                                                }
                                              , { '$id' : 'FB-0:2::0-1:0:0:1'
                                                , 'children' :
                                                    [ { '$id' : 'FB-0:2::0-1:0:0:1.0'
                                                      , 'completer' :
                                                          { 'embedded_p' : True
                                                          , 'entity_p' : False
                                                          , 'names' :
    [ 'start' ]
                                                          , 'treshold' : 4
                                                          }
                                                      , 'kind' : 'necessary'
                                                      , 'label' : 'Start'
                                                      , 'name' : 'start'
                                                      , 'type' : 'Field'
                                                      , 'value' :
                                                          { 'edit' : '2008/05/01' }
                                                      }
                                                    , { '$id' : 'FB-0:2::0-1:0:0:1.1'
                                                      , 'completer' :
                                                          { 'embedded_p' : True
                                                          , 'entity_p' : False
                                                          , 'names' :
    [ 'finish' ]
                                                          , 'treshold' : 4
                                                          }
                                                      , 'kind' : 'optional'
                                                      , 'label' : 'Finish'
                                                      , 'name' : 'finish'
                                                      , 'type' : 'Field'
                                                      , 'value' :
                                                          { 'edit' : '2008/05/01' }
                                                      }
                                                    ]
                                                , 'collapsed' : True
                                                , 'completer' :
                                                    { 'entity_p' : True
                                                    , 'names' :
                                                        [ 'date'
                                                        , 'name'
                                                        ]
                                                    , 'treshold' : 1
                                                    }
                                                , 'kind' : 'primary'
                                                , 'label' : 'Date'
                                                , 'name' : 'date'
                                                , 'required' : True
                                                , 'type' : 'Field_Composite'
                                                , 'type_name' : 'MOM.Date_Interval_C'
                                                , 'value' :
                                                    {}
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
                                              , 'sid' : 'EgH8LtkA05g5MO-6ez4Hbj7J:Lb-almSesfpGQ'
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
                                                    { 'embedded_p' : True
                                                    , 'entity_p' : True
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
                                                    { 'embedded_p' : True
                                                    , 'entity_p' : True
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
                                                    { 'embedded_p' : True
                                                    , 'entity_p' : True
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
                                                    { 'embedded_p' : True
                                                    , 'entity_p' : False
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
                                          , 'completer' :
                                              { 'entity_p' : True
                                              , 'names' :
                                                  [ 'left'
                                                  , 'nation'
                                                  , 'mna_number'
                                                  , 'club'
                                                  ]
                                              , 'treshold' : 1
                                              }
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
                                          , 'completer' :
                                              { 'entity_p' : True
                                              , 'names' :
                                                  [ 'mna_number'
                                                  , 'left'
                                                  , 'nation'
                                                  , 'club'
                                                  ]
                                              , 'treshold' : 1
                                              }
                                          , 'kind' : 'primary'
                                          , 'label' : 'Mna number'
                                          , 'name' : 'mna_number'
                                          , 'type' : 'Field'
                                          , 'value' :
                                              { 'edit' : '29676' }
                                          }
                                        , { '$id' : 'FB-0:2::0-2:0:3'
                                          , 'allow_new' : True
                                          , 'children' :
                                              [ { '$id' : 'FB-0:2::0-2:0:3:0'
                                                , 'completer' :
                                                    { 'entity_p' : True
                                                    , 'names' :
    [ 'name' ]
                                                    , 'treshold' : 1
                                                    }
                                                , 'kind' : 'primary'
                                                , 'label' : 'Name'
                                                , 'name' : 'name'
                                                , 'required' : True
                                                , 'type' : 'Field'
                                                , 'value' :
                                                    {}
                                                }
                                              ]
                                          , 'collapsed' : True
                                          , 'kind' : 'primary'
                                          , 'label' : 'Club'
                                          , 'name' : 'club'
                                          , 'type' : 'Field_Entity'
                                          , 'type_name' : 'GTW.OMP.SRM.Club'
                                          , 'value' :
                                              { 'init' :
                                                  {}
                                              , 'sid' : 'diNMsTC-2yU41VucKcBWUSQGe1b0O2mYXb8WjQ'
                                              }
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
                                        , 'sid' : 'VdaPLnEfWE8YrlzFrGXYLZgp5jLgdQt1avEw7A'
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
                            , 'sid' : 'MilQWW-BQ:1Kfxi2ptEelkCAqwhaXWaRbFloTA'
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
                , 'sid' : 'NlcOLOnkFT9tdwf027AmLo5cyc8NKlL6iEVddg'
                }
            }
          ]
      , 'type' : 'Form'
      , 'value' :
          { 'sid' : 0 }
      }

    >>> print "var f =", fi.as_js, ";"
    var f = new $GTW.AFS.Form ({"$id": "FB", "children": [{"$id": "FB-0", "allow_new": true, "children": [{"$id": "FB-0:0", "children": [{"$id": "FB-0:0:0", "allow_new": true, "children": [{"$id": "FB-0:0:0:0", "completer": {"entity_p": true, "names": ["name"], "treshold": 1}, "kind": "primary", "label": "Name", "name": "name", "required": true, "type": "Field", "value": {"init": "Optimist"}}], "collapsed": true, "kind": "primary", "label": "Class", "name": "left", "required": true, "type": "Field_Entity", "type_name": "GTW.OMP.SRM.Boat_Class", "value": {"init": {"cid": 1, "pid": 1, "uid": "Optimist"}, "sid": "qPzMz88f1x3RjbWOPHj4PR2ZthTO:EW:MNddnA"}}, {"$id": "FB-0:0:1", "kind": "primary", "label": "Nation", "name": "nation", "type": "Field", "value": {"init": "AUT"}}, {"$id": "FB-0:0:2", "completer": {"entity_p": true, "names": ["sail_number", "left", "nation", "sail_number_x"], "treshold": 1}, "kind": "primary", "label": "Sail number", "name": "sail_number", "type": "Field", "value": {"init": "1107"}}, {"$id": "FB-0:0:3", "completer": {"entity_p": true, "names": ["sail_number_x", "left", "nation", "sail_number"], "treshold": 1}, "kind": "primary", "label": "Sail number x", "name": "sail_number_x", "type": "Field", "value": {}}], "collapsed": false, "name": "primary", "type": "Fieldset"}, {"$id": "FB-0:1", "children": [{"$id": "FB-0:1:0", "kind": "optional", "label": "Name", "name": "name", "type": "Field", "value": {}}], "collapsed": true, "name": "optional", "type": "Fieldset"}, {"$id": "FB-0:2", "allow_new": true, "children": [{"$id": "FB-0:2::0", "allow_new": true, "children": [{"$id": "FB-0:2::0-0", "allow_new": false, "collapsed": true, "hidden": true, "kind": "primary", "label": "Boat", "name": "left", "required": true, "type": "Field_Role_Hidden", "type_name": "GTW.OMP.SRM.Boat", "value": {"init": {"cid": 2, "pid": 2, "uid": "Optimist, AUT 1107"}, "sid": "ORsB0LFjw5hzuHauaOA1M3usp415XdhUdQ0tfQ"}}, {"$id": "FB-0:2::0-1", "children": [{"$id": "FB-0:2::0-1:0", "allow_new": false, "children": [{"$id": "FB-0:2::0-1:0:0", "allow_new": false, "children": [{"$id": "FB-0:2::0-1:0:0:0", "completer": {"entity_p": true, "names": ["name", "date"], "treshold": 1}, "kind": "primary", "label": "Name", "name": "name", "required": true, "type": "Field", "value": {"init": "Himmelfahrt"}}, {"$id": "FB-0:2::0-1:0:0:1", "children": [{"$id": "FB-0:2::0-1:0:0:1.0", "completer": {"embedded_p": true, "entity_p": false, "names": ["start"], "treshold": 4}, "kind": "necessary", "label": "Start", "name": "start", "type": "Field", "value": {"init": "2008/05/01"}}, {"$id": "FB-0:2::0-1:0:0:1.1", "completer": {"embedded_p": true, "entity_p": false, "names": ["finish"], "treshold": 4}, "kind": "optional", "label": "Finish", "name": "finish", "type": "Field", "value": {"init": "2008/05/01"}}], "collapsed": true, "completer": {"entity_p": true, "names": ["date", "name"], "treshold": 1}, "kind": "primary", "label": "Date", "name": "date", "required": true, "type": "Field_Composite", "type_name": "MOM.Date_Interval_C", "value": {}}], "collapsed": true, "kind": "primary", "label": "Event", "name": "left", "required": true, "type": "Field_Entity", "type_name": "GTW.OMP.SRM.Regatta_Event", "value": {"init": {"cid": 5, "pid": 5, "uid": "Himmelfahrt 2008/05/01"}, "sid": "siR36p3Hsut0dtJQl-h3TjrWxG6qhX9soaq6:g"}}], "collapsed": true, "kind": "primary", "label": "Regatta", "name": "right", "required": true, "type": "Field_Entity", "type_name": "GTW.OMP.SRM.Regatta", "value": {"init": {"cid": 6, "pid": 6, "uid": "Himmelfahrt 2008/05/01, Optimist"}, "sid": "t0nRFI5GFozOgzRVAMlfEVZeU9oCHiVfFTBuWw"}}], "collapsed": false, "name": "primary", "type": "Fieldset"}, {"$id": "FB-0:2::0-2", "children": [{"$id": "FB-0:2::0-2:0", "allow_new": true, "children": [{"$id": "FB-0:2::0-2:0:0", "allow_new": true, "children": [{"$id": "FB-0:2::0-2:0:0:0", "completer": {"embedded_p": true, "entity_p": true, "names": ["last_name", "first_name", "middle_name", "title"], "treshold": 2}, "kind": "primary", "label": "Last name", "name": "last_name", "required": true, "type": "Field", "value": {"init": "Tanzer"}}, {"$id": "FB-0:2::0-2:0:0:1", "completer": {"embedded_p": true, "entity_p": true, "names": ["first_name", "last_name", "middle_name", "title"], "treshold": 3}, "kind": "primary", "label": "First name", "name": "first_name", "required": true, "type": "Field", "value": {"init": "Laurens"}}, {"$id": "FB-0:2::0-2:0:0:2", "completer": {"embedded_p": true, "entity_p": true, "names": ["middle_name", "last_name", "first_name", "title"], "treshold": 2}, "kind": "primary", "label": "Middle name", "name": "middle_name", "type": "Field", "value": {}}, {"$id": "FB-0:2::0-2:0:0:3", "completer": {"embedded_p": true, "entity_p": false, "names": ["title"], "treshold": 1}, "kind": "primary", "label": "Academic title", "name": "title", "type": "Field", "value": {}}], "collapsed": true, "completer": {"entity_p": true, "names": ["left", "nation", "mna_number", "club"], "treshold": 1}, "kind": "primary", "label": "Person", "name": "left", "required": true, "type": "Field_Entity", "type_name": "GTW.OMP.PAP.Person", "value": {"init": {"cid": 3, "pid": 3, "uid": "Tanzer Laurens"}, "sid": "jCVvrVL7cxthrwL4:mPenABA:H4vtKSITQhTuA"}}, {"$id": "FB-0:2::0-2:0:1", "kind": "primary", "label": "Nation", "name": "nation", "type": "Field", "value": {"init": "AUT"}}, {"$id": "FB-0:2::0-2:0:2", "completer": {"entity_p": true, "names": ["mna_number", "left", "nation", "club"], "treshold": 1}, "kind": "primary", "label": "Mna number", "name": "mna_number", "type": "Field", "value": {"init": "29676"}}, {"$id": "FB-0:2::0-2:0:3", "allow_new": true, "children": [{"$id": "FB-0:2::0-2:0:3:0", "completer": {"entity_p": true, "names": ["name"], "treshold": 1}, "kind": "primary", "label": "Name", "name": "name", "required": true, "type": "Field", "value": {}}], "collapsed": true, "kind": "primary", "label": "Club", "name": "club", "type": "Field_Entity", "type_name": "GTW.OMP.SRM.Club", "value": {"init": {"cid": null, "pid": null, "uid": null}, "sid": "diNMsTC-2yU41VucKcBWUSQGe1b0O2mYXb8WjQ"}}], "collapsed": true, "kind": "required", "label": "Skipper", "name": "skipper", "required": true, "type": "Field_Entity", "type_name": "GTW.OMP.SRM.Sailor", "value": {"init": {"cid": 4, "pid": 4, "uid": "Tanzer Laurens, AUT, 29676"}, "sid": "fDjH5uIO03Wdnc5gX3D7C88Msxfp807Dd15LdA"}}], "collapsed": true, "name": "required", "type": "Fieldset"}, {"$id": "FB-0:2::0-3", "children": [{"$id": "FB-0:2::0-3:0", "kind": "optional", "label": "Place", "name": "place", "type": "Field", "value": {}}, {"$id": "FB-0:2::0-3:1", "kind": "optional", "label": "Points", "name": "points", "type": "Field", "value": {}}], "collapsed": true, "name": "optional", "type": "Fieldset"}], "collapsed": true, "name": "Boat_in_Regatta", "role_name": "left", "type": "Entity_Link", "type_name": "GTW.OMP.SRM.Boat_in_Regatta", "value": {"init": {"cid": 7, "pid": 7, "uid": "Optimist, AUT 1107, Himmelfahrt 2008/05/01, Optimist"}, "sid": "WL-78I4-zhVeNm1-xWrXjotyN8mcfb-yZGgf6A"}}], "name": "Boat_in_Regatta", "type": "Entity_List", "type_name": "GTW.OMP.SRM.Boat_in_Regatta"}], "name": "Boat", "type": "Entity", "type_name": "GTW.OMP.SRM.Boat", "value": {"init": {"cid": 2, "pid": 2, "uid": "Optimist, AUT 1107"}, "sid": "hr-jUx4QHTv6rHr09XNKhgpG8von21skUQ4C9Q"}}], "type": "Form", "value": {"sid": 0}}) ;
    >>> print "var g =", fic.as_js, ";"
    var g = new $GTW.AFS.Form ({"$id": "FB", "children": [{"$id": "FB-0", "allow_new": true, "children": [{"$id": "FB-0:0", "children": [{"$id": "FB-0:0:0", "allow_new": true, "children": [{"$id": "FB-0:0:0:0", "completer": {"entity_p": true, "names": ["name"], "treshold": 1}, "kind": "primary", "label": "Name", "name": "name", "required": true, "type": "Field", "value": {"edit": "Optimist"}}], "collapsed": true, "kind": "primary", "label": "Class", "name": "left", "required": true, "type": "Field_Entity", "type_name": "GTW.OMP.SRM.Boat_Class", "value": {"init": {}, "sid": "2SMjmpittgN68fuUf1yK7xN-uRxHK4q2kDJOlA"}}, {"$id": "FB-0:0:1", "kind": "primary", "label": "Nation", "name": "nation", "type": "Field", "value": {"edit": "AUT"}}, {"$id": "FB-0:0:2", "completer": {"entity_p": true, "names": ["sail_number", "left", "nation", "sail_number_x"], "treshold": 1}, "kind": "primary", "label": "Sail number", "name": "sail_number", "type": "Field", "value": {"edit": "1107"}}, {"$id": "FB-0:0:3", "completer": {"entity_p": true, "names": ["sail_number_x", "left", "nation", "sail_number"], "treshold": 1}, "kind": "primary", "label": "Sail number x", "name": "sail_number_x", "type": "Field", "value": {}}], "collapsed": false, "name": "primary", "type": "Fieldset"}, {"$id": "FB-0:1", "children": [{"$id": "FB-0:1:0", "kind": "optional", "label": "Name", "name": "name", "type": "Field", "value": {}}], "collapsed": true, "name": "optional", "type": "Fieldset"}, {"$id": "FB-0:2", "allow_new": true, "children": [{"$id": "FB-0:2::0", "allow_new": true, "children": [{"$id": "FB-0:2::0-0", "allow_new": false, "collapsed": true, "hidden": true, "kind": "primary", "label": "Boat", "name": "left", "required": true, "type": "Field_Role_Hidden", "type_name": "GTW.OMP.SRM.Boat", "value": {"init": {}, "sid": "emH:n2fr5Vojp8:mNyEhadFeTvrt0Hb26l7S4Q"}}, {"$id": "FB-0:2::0-1", "children": [{"$id": "FB-0:2::0-1:0", "allow_new": false, "children": [{"$id": "FB-0:2::0-1:0:0", "allow_new": false, "children": [{"$id": "FB-0:2::0-1:0:0:0", "completer": {"entity_p": true, "names": ["name", "date"], "treshold": 1}, "kind": "primary", "label": "Name", "name": "name", "required": true, "type": "Field", "value": {"edit": "Himmelfahrt"}}, {"$id": "FB-0:2::0-1:0:0:1", "children": [{"$id": "FB-0:2::0-1:0:0:1.0", "completer": {"embedded_p": true, "entity_p": false, "names": ["start"], "treshold": 4}, "kind": "necessary", "label": "Start", "name": "start", "type": "Field", "value": {"edit": "2008/05/01"}}, {"$id": "FB-0:2::0-1:0:0:1.1", "completer": {"embedded_p": true, "entity_p": false, "names": ["finish"], "treshold": 4}, "kind": "optional", "label": "Finish", "name": "finish", "type": "Field", "value": {"edit": "2008/05/01"}}], "collapsed": true, "completer": {"entity_p": true, "names": ["date", "name"], "treshold": 1}, "kind": "primary", "label": "Date", "name": "date", "required": true, "type": "Field_Composite", "type_name": "MOM.Date_Interval_C", "value": {}}], "collapsed": true, "kind": "primary", "label": "Event", "name": "left", "required": true, "type": "Field_Entity", "type_name": "GTW.OMP.SRM.Regatta_Event", "value": {"init": {}, "sid": "EgH8LtkA05g5MO-6ez4Hbj7J:Lb-almSesfpGQ"}}], "collapsed": true, "kind": "primary", "label": "Regatta", "name": "right", "required": true, "type": "Field_Entity", "type_name": "GTW.OMP.SRM.Regatta", "value": {"init": {}, "sid": "n4dFoUTWL2ZKZ1e-igGdLTtkVfW3LOxorspVfw"}}], "collapsed": false, "name": "primary", "type": "Fieldset"}, {"$id": "FB-0:2::0-2", "children": [{"$id": "FB-0:2::0-2:0", "allow_new": true, "children": [{"$id": "FB-0:2::0-2:0:0", "allow_new": true, "children": [{"$id": "FB-0:2::0-2:0:0:0", "completer": {"embedded_p": true, "entity_p": true, "names": ["last_name", "first_name", "middle_name", "title"], "treshold": 2}, "kind": "primary", "label": "Last name", "name": "last_name", "required": true, "type": "Field", "value": {"edit": "Tanzer"}}, {"$id": "FB-0:2::0-2:0:0:1", "completer": {"embedded_p": true, "entity_p": true, "names": ["first_name", "last_name", "middle_name", "title"], "treshold": 3}, "kind": "primary", "label": "First name", "name": "first_name", "required": true, "type": "Field", "value": {"edit": "Laurens"}}, {"$id": "FB-0:2::0-2:0:0:2", "completer": {"embedded_p": true, "entity_p": true, "names": ["middle_name", "last_name", "first_name", "title"], "treshold": 2}, "kind": "primary", "label": "Middle name", "name": "middle_name", "type": "Field", "value": {}}, {"$id": "FB-0:2::0-2:0:0:3", "completer": {"embedded_p": true, "entity_p": false, "names": ["title"], "treshold": 1}, "kind": "primary", "label": "Academic title", "name": "title", "type": "Field", "value": {}}], "collapsed": true, "completer": {"entity_p": true, "names": ["left", "nation", "mna_number", "club"], "treshold": 1}, "kind": "primary", "label": "Person", "name": "left", "required": true, "type": "Field_Entity", "type_name": "GTW.OMP.PAP.Person", "value": {"init": {}, "sid": "Z:YWrkrkIu19OHcrW0W6DFmkEXuuZ7TAjiV5qQ"}}, {"$id": "FB-0:2::0-2:0:1", "kind": "primary", "label": "Nation", "name": "nation", "type": "Field", "value": {"edit": "AUT"}}, {"$id": "FB-0:2::0-2:0:2", "completer": {"entity_p": true, "names": ["mna_number", "left", "nation", "club"], "treshold": 1}, "kind": "primary", "label": "Mna number", "name": "mna_number", "type": "Field", "value": {"edit": "29676"}}, {"$id": "FB-0:2::0-2:0:3", "allow_new": true, "children": [{"$id": "FB-0:2::0-2:0:3:0", "completer": {"entity_p": true, "names": ["name"], "treshold": 1}, "kind": "primary", "label": "Name", "name": "name", "required": true, "type": "Field", "value": {}}], "collapsed": true, "kind": "primary", "label": "Club", "name": "club", "type": "Field_Entity", "type_name": "GTW.OMP.SRM.Club", "value": {"init": {}, "sid": "diNMsTC-2yU41VucKcBWUSQGe1b0O2mYXb8WjQ"}}], "collapsed": true, "kind": "required", "label": "Skipper", "name": "skipper", "required": true, "type": "Field_Entity", "type_name": "GTW.OMP.SRM.Sailor", "value": {"init": {}, "sid": "VdaPLnEfWE8YrlzFrGXYLZgp5jLgdQt1avEw7A"}}], "collapsed": true, "name": "required", "type": "Fieldset"}, {"$id": "FB-0:2::0-3", "children": [{"$id": "FB-0:2::0-3:0", "kind": "optional", "label": "Place", "name": "place", "type": "Field", "value": {}}, {"$id": "FB-0:2::0-3:1", "kind": "optional", "label": "Points", "name": "points", "type": "Field", "value": {}}], "collapsed": true, "name": "optional", "type": "Fieldset"}], "collapsed": true, "name": "Boat_in_Regatta", "role_name": "left", "type": "Entity_Link", "type_name": "GTW.OMP.SRM.Boat_in_Regatta", "value": {"init": {}, "sid": "MilQWW-BQ:1Kfxi2ptEelkCAqwhaXWaRbFloTA"}}], "name": "Boat_in_Regatta", "type": "Entity_List", "type_name": "GTW.OMP.SRM.Boat_in_Regatta"}], "name": "Boat", "type": "Entity", "type_name": "GTW.OMP.SRM.Boat", "value": {"init": {}, "sid": "NlcOLOnkFT9tdwf027AmLo5cyc8NKlL6iEVddg"}}], "type": "Form", "value": {"sid": 0}}) ;

    >>> for i in fi.transitive_iter () :
    ...     print i.elem, sorted (i.value or ())
    <Form FB> ['sid']
    <Entity FB-0 'Boat' 'GTW.OMP.SRM.Boat'> [u'init', 'sid']
    <Fieldset FB-0:0 'primary'> []
    <Field_Entity FB-0:0:0 'left' 'GTW.OMP.SRM.Boat_Class'> [u'init', 'sid']
    <Field FB-0:0:0:0 'name'> [u'init']
    <Field FB-0:0:1 'nation'> [u'init']
    <Field FB-0:0:2 'sail_number'> [u'init']
    <Field FB-0:0:3 'sail_number_x'> []
    <Fieldset FB-0:1 'optional'> []
    <Field FB-0:1:0 'name'> []
    <Entity_List FB-0:2 'Boat_in_Regatta' <Entity_Link FB-0:2::p 'Boat_in_Regatta' 'GTW.OMP.SRM.Boat_in_Regatta'>> []
    <Entity_Link FB-0:2::0 'Boat_in_Regatta' 'GTW.OMP.SRM.Boat_in_Regatta'> [u'init', 'sid']
    <Field_Role_Hidden FB-0:2::0-0 'left' 'GTW.OMP.SRM.Boat'> [u'init', 'sid']
    <Fieldset FB-0:2::0-1 'primary'> []
    <Field_Entity FB-0:2::0-1:0 'right' 'GTW.OMP.SRM.Regatta'> [u'init', 'sid']
    <Field_Entity FB-0:2::0-1:0:0 'left' 'GTW.OMP.SRM.Regatta_Event'> [u'init', 'sid']
    <Field FB-0:2::0-1:0:0:0 'name'> [u'init']
    <Field_Composite FB-0:2::0-1:0:0:1 'date' 'MOM.Date_Interval_C'> []
    <Field FB-0:2::0-1:0:0:1.0 'start'> [u'init']
    <Field FB-0:2::0-1:0:0:1.1 'finish'> [u'init']
    <Fieldset FB-0:2::0-2 'required'> []
    <Field_Entity FB-0:2::0-2:0 'skipper' 'GTW.OMP.SRM.Sailor'> [u'init', 'sid']
    <Field_Entity FB-0:2::0-2:0:0 'left' 'GTW.OMP.PAP.Person'> [u'init', 'sid']
    <Field FB-0:2::0-2:0:0:0 'last_name'> [u'init']
    <Field FB-0:2::0-2:0:0:1 'first_name'> [u'init']
    <Field FB-0:2::0-2:0:0:2 'middle_name'> []
    <Field FB-0:2::0-2:0:0:3 'title'> []
    <Field FB-0:2::0-2:0:1 'nation'> [u'init']
    <Field FB-0:2::0-2:0:2 'mna_number'> [u'init']
    <Field_Entity FB-0:2::0-2:0:3 'club' 'GTW.OMP.SRM.Club'> [u'init', 'sid']
    <Field FB-0:2::0-2:0:3:0 'name'> []
    <Fieldset FB-0:2::0-3 'optional'> []
    <Field FB-0:2::0-3:0 'place'> []
    <Field FB-0:2::0-3:1 'points'> []

    >>> for i in fi.entities () :
    ...     print i.elem
    <Entity FB-0 'Boat' 'GTW.OMP.SRM.Boat'>

    >>> f_sig_map = {}
    >>> for i in fi.entity_children () :
    ...     f_sig_map [i.id] = i, i.sig
    ...     print i.elem, ", pid =", i.init.get ("pid"), ", sid =", i.sid
    <Entity FB-0 'Boat' 'GTW.OMP.SRM.Boat'> , pid = 2 , sid = hr-jUx4QHTv6rHr09XNKhgpG8von21skUQ4C9Q
    <Field_Entity FB-0:0:0 'left' 'GTW.OMP.SRM.Boat_Class'> , pid = 1 , sid = qPzMz88f1x3RjbWOPHj4PR2ZthTO:EW:MNddnA
    <Entity_Link FB-0:2::0 'Boat_in_Regatta' 'GTW.OMP.SRM.Boat_in_Regatta'> , pid = 7 , sid = WL-78I4-zhVeNm1-xWrXjotyN8mcfb-yZGgf6A
    <Field_Role_Hidden FB-0:2::0-0 'left' 'GTW.OMP.SRM.Boat'> , pid = 2 , sid = ORsB0LFjw5hzuHauaOA1M3usp415XdhUdQ0tfQ
    <Field_Entity FB-0:2::0-1:0 'right' 'GTW.OMP.SRM.Regatta'> , pid = 6 , sid = t0nRFI5GFozOgzRVAMlfEVZeU9oCHiVfFTBuWw
    <Field_Entity FB-0:2::0-1:0:0 'left' 'GTW.OMP.SRM.Regatta_Event'> , pid = 5 , sid = siR36p3Hsut0dtJQl-h3TjrWxG6qhX9soaq6:g
    <Field_Entity FB-0:2::0-2:0 'skipper' 'GTW.OMP.SRM.Sailor'> , pid = 4 , sid = fDjH5uIO03Wdnc5gX3D7C88Msxfp807Dd15LdA
    <Field_Entity FB-0:2::0-2:0:0 'left' 'GTW.OMP.PAP.Person'> , pid = 3 , sid = jCVvrVL7cxthrwL4:mPenABA:H4vtKSITQhTuA
    <Field_Entity FB-0:2::0-2:0:3 'club' 'GTW.OMP.SRM.Club'> , pid = None , sid = diNMsTC-2yU41VucKcBWUSQGe1b0O2mYXb8WjQ

    >>> def show_instance (i) :
    ...   def show_entity (i, name) :
    ...     e = getattr (i, name)
    ...     return "%1.1s = %s" % (name, getattr (e, "pid", "-"))
    ...   return "%-72s %s %s %s" % (i.elem, show_entity (i, "entity"), show_entity (i, "outer_entity"), show_entity (i, "role_entity"))
    >>> for i in fi.entity_children () :
    ...     print show_instance (i)
    <Entity FB-0 'Boat' 'GTW.OMP.SRM.Boat'>                                  e = 2 o = - r = -
    <Field_Entity FB-0:0:0 'left' 'GTW.OMP.SRM.Boat_Class'>                  e = 1 o = 2 r = -
    <Entity_Link FB-0:2::0 'Boat_in_Regatta' 'GTW.OMP.SRM.Boat_in_Regatta'>  e = 7 o = - r = 2
    <Field_Role_Hidden FB-0:2::0-0 'left' 'GTW.OMP.SRM.Boat'>                e = 2 o = 7 r = -
    <Field_Entity FB-0:2::0-1:0 'right' 'GTW.OMP.SRM.Regatta'>               e = 6 o = 7 r = -
    <Field_Entity FB-0:2::0-1:0:0 'left' 'GTW.OMP.SRM.Regatta_Event'>        e = 5 o = 6 r = -
    <Field_Entity FB-0:2::0-2:0 'skipper' 'GTW.OMP.SRM.Sailor'>              e = 4 o = 7 r = -
    <Field_Entity FB-0:2::0-2:0:0 'left' 'GTW.OMP.PAP.Person'>               e = 3 o = 4 r = -
    <Field_Entity FB-0:2::0-2:0:3 'club' 'GTW.OMP.SRM.Club'>                 e = - o = 4 r = -

    >>> g_sig_map = {}
    >>> for i in fic.entity_children () :
    ...     g_sig_map [i.id] = i, i.sig
    ...     print i.elem, ", pid =", i.init.get ("pid"), ", sid =", i.sid
    <Entity FB-0 'Boat' 'GTW.OMP.SRM.Boat'> , pid = None , sid = NlcOLOnkFT9tdwf027AmLo5cyc8NKlL6iEVddg
    <Field_Entity FB-0:0:0 'left' 'GTW.OMP.SRM.Boat_Class'> , pid = None , sid = 2SMjmpittgN68fuUf1yK7xN-uRxHK4q2kDJOlA
    <Entity_Link FB-0:2::0 'Boat_in_Regatta' 'GTW.OMP.SRM.Boat_in_Regatta'> , pid = None , sid = MilQWW-BQ:1Kfxi2ptEelkCAqwhaXWaRbFloTA
    <Field_Role_Hidden FB-0:2::0-0 'left' 'GTW.OMP.SRM.Boat'> , pid = None , sid = emH:n2fr5Vojp8:mNyEhadFeTvrt0Hb26l7S4Q
    <Field_Entity FB-0:2::0-1:0 'right' 'GTW.OMP.SRM.Regatta'> , pid = None , sid = n4dFoUTWL2ZKZ1e-igGdLTtkVfW3LOxorspVfw
    <Field_Entity FB-0:2::0-1:0:0 'left' 'GTW.OMP.SRM.Regatta_Event'> , pid = None , sid = EgH8LtkA05g5MO-6ez4Hbj7J:Lb-almSesfpGQ
    <Field_Entity FB-0:2::0-2:0 'skipper' 'GTW.OMP.SRM.Sailor'> , pid = None , sid = VdaPLnEfWE8YrlzFrGXYLZgp5jLgdQt1avEw7A
    <Field_Entity FB-0:2::0-2:0:0 'left' 'GTW.OMP.PAP.Person'> , pid = None , sid = Z:YWrkrkIu19OHcrW0W6DFmkEXuuZ7TAjiV5qQ
    <Field_Entity FB-0:2::0-2:0:3 'club' 'GTW.OMP.SRM.Club'> , pid = None , sid = diNMsTC-2yU41VucKcBWUSQGe1b0O2mYXb8WjQ

    >>> Value.from_json (json_bad)
    Traceback (most recent call last):
      ...
    Unknown: Form/element is unknown (unknown id: FC)

    >>> fv = Value.from_json (json_edit)
    >>> fv.changes_t
    1
    >>> for i in fv.transitive_iter () :
    ...     print i
    <Form FB>, init-v = '', sid = 0, changes = 0
    <Entity FB-0 'Boat' 'GTW.OMP.SRM.Boat'>, init-v = [(u'cid', 2), (u'pid', 2)], sid = hr-jUx4QHTv6rHr09XNKhgpG8von21skUQ4C9Q, changes = 0
    <Field_Entity FB-0:0:0 'left' 'GTW.OMP.SRM.Boat_Class'>, init-v = [(u'cid', 1), (u'pid', 1)], sid = qPzMz88f1x3RjbWOPHj4PR2ZthTO:EW:MNddnA, changes = 0
    <Field FB-0:0:0:0 'name'>, init-v = 'Optimist', changes = 0
    <Field FB-0:0:1 'nation'>, init-v = 'AUT', changes = 0
    <Field FB-0:0:2 'sail_number'>, init-v = '1107', changes = 0
    <Field FB-0:0:3 'sail_number_x'>, init-v = '', changes = 0
    <Field FB-0:1:0 'name'>, init-v = '', changes = 0
    <Entity_Link FB-0:2::p 'Boat_in_Regatta' 'GTW.OMP.SRM.Boat_in_Regatta'>, init-v = [(u'cid', 7), (u'pid', 7)], sid = WL-78I4-zhVeNm1-xWrXjotyN8mcfb-yZGgf6A, changes = 0
    <Field_Role_Hidden FB-0:2::p-0 'left' 'GTW.OMP.SRM.Boat'>, init-v = [(u'cid', 2), (u'pid', 2)], sid = ORsB0LFjw5hzuHauaOA1M3usp415XdhUdQ0tfQ, changes = 0, role_id = FB-0
    <Field_Entity FB-0:2::p-1:0 'right' 'GTW.OMP.SRM.Regatta'>, init-v = [(u'cid', 6), (u'pid', 6)], sid = t0nRFI5GFozOgzRVAMlfEVZeU9oCHiVfFTBuWw, changes = 0
    <Field_Entity FB-0:2::p-1:0:0 'left' 'GTW.OMP.SRM.Regatta_Event'>, init-v = [(u'cid', 5), (u'pid', 5)], sid = siR36p3Hsut0dtJQl-h3TjrWxG6qhX9soaq6:g, changes = 0
    <Field FB-0:2::p-1:0:0:0 'name'>, init-v = 'Himmelfahrt', changes = 0
    <Field_Composite FB-0:2::p-1:0:0:1 'date' 'MOM.Date_Interval_C'>, init-v = '', changes = 0
    <Field FB-0:2::p-1:0:0:1.0 'start'>, init-v = '2008/05/01', changes = 0
    <Field FB-0:2::p-1:0:0:1.1 'finish'>, init-v = '2008/05/01', changes = 0
    <Field_Entity FB-0:2::p-2:0 'skipper' 'GTW.OMP.SRM.Sailor'>, init-v = [(u'cid', 4), (u'pid', 4)], sid = fDjH5uIO03Wdnc5gX3D7C88Msxfp807Dd15LdA, changes = 0
    <Field_Entity FB-0:2::p-2:0:0 'left' 'GTW.OMP.PAP.Person'>, init-v = [(u'cid', 3), (u'pid', 3)], sid = jCVvrVL7cxthrwL4:mPenABA:H4vtKSITQhTuA, changes = 1
    <Field FB-0:2::p-2:0:0:0 'last_name'>, init-v = 'Tanzer', changes = 0
    <Field FB-0:2::p-2:0:0:1 'first_name'>, init-v = 'Laurens', changes = 0
    <Field FB-0:2::p-2:0:0:2 'middle_name'>, init-v = '', edit-v = 'William', changes = 1
    <Field FB-0:2::p-2:0:0:3 'title'>, init-v = '', changes = 0
    <Field FB-0:2::p-2:0:1 'nation'>, init-v = 'AUT', changes = 0
    <Field FB-0:2::p-2:0:2 'mna_number'>, init-v = '29676', changes = 0
    <Field_Entity FB-0:2::p-2:0:3 'club' 'GTW.OMP.SRM.Club'>, init-v = [(u'cid', None), (u'pid', None)], sid = diNMsTC-2yU41VucKcBWUSQGe1b0O2mYXb8WjQ, changes = 0
    <Field FB-0:2::p-2:0:3:0 'name'>, init-v = '', changes = 0
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
      > hr-jUx4QHTv6rHr09XNKhgpG8von21skUQ4C9Q
      < hr-jUx4QHTv6rHr09XNKhgpG8von21skUQ4C9Q
      > (((u'pid', 2), (u'cid', 2), 'FB-0', 'GTW.OMP.SRM.Boat'), ('FB-0:0:0', 'left'), ('FB-0:0:1', 'nation', u'AUT'), ('FB-0:0:2', 'sail_number', u'1107'), ('FB-0:0:3', 'sail_number_x', u''), ('FB-0:1:0', 'name', u''), 0)
      < (((u'pid', 2), (u'cid', 2), 'FB-0', 'GTW.OMP.SRM.Boat'), ('FB-0:0:0', 'left'), ('FB-0:0:1', 'nation', u'AUT'), ('FB-0:0:2', 'sail_number', u'1107'), ('FB-0:0:3', 'sail_number_x', u''), ('FB-0:1:0', 'name', u''), 0)
    <Field_Entity FB-0:0:0 'left' 'GTW.OMP.SRM.Boat_Class'> True True
      > qPzMz88f1x3RjbWOPHj4PR2ZthTO:EW:MNddnA
      < qPzMz88f1x3RjbWOPHj4PR2ZthTO:EW:MNddnA
      > (((u'pid', 1), (u'cid', 1), 'FB-0:0:0', 'GTW.OMP.SRM.Boat_Class'), ('FB-0:0:0:0', 'name', u'Optimist'), 0)
      < (((u'pid', 1), (u'cid', 1), 'FB-0:0:0', 'GTW.OMP.SRM.Boat_Class'), ('FB-0:0:0:0', 'name', u'Optimist'), 0)
    <Entity_Link FB-0:2::0 'Boat_in_Regatta' 'GTW.OMP.SRM.Boat_in_Regatta'> True True
      > WL-78I4-zhVeNm1-xWrXjotyN8mcfb-yZGgf6A
      < WL-78I4-zhVeNm1-xWrXjotyN8mcfb-yZGgf6A
      > (((u'pid', 7), (u'cid', 7), 'FB-0:2::0', 'GTW.OMP.SRM.Boat_in_Regatta'), ('FB-0:2::0-0', 'left'), ('FB-0:2::0-1:0', 'right'), ('FB-0:2::0-2:0', 'skipper'), ('FB-0:2::0-3:0', 'place', u''), ('FB-0:2::0-3:1', 'points', u''), 0)
      < (((u'pid', 7), (u'cid', 7), 'FB-0:2::0', 'GTW.OMP.SRM.Boat_in_Regatta'), ('FB-0:2::0-0', 'left'), ('FB-0:2::0-1:0', 'right'), ('FB-0:2::0-2:0', 'skipper'), ('FB-0:2::0-3:0', 'place', u''), ('FB-0:2::0-3:1', 'points', u''), 0)
    <Field_Role_Hidden FB-0:2::0-0 'left' 'GTW.OMP.SRM.Boat'> True True
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
      > siR36p3Hsut0dtJQl-h3TjrWxG6qhX9soaq6:g
      < siR36p3Hsut0dtJQl-h3TjrWxG6qhX9soaq6:g
      > (((u'pid', 5), (u'cid', 5), 'FB-0:2::0-1:0:0', 'GTW.OMP.SRM.Regatta_Event'), ('FB-0:2::0-1:0:0:0', 'name', u'Himmelfahrt'), ('FB-0:2::0-1:0:0:1', 'date', (('FB-0:2::0-1:0:0:1.0', 'start', u'2008/05/01'), ('FB-0:2::0-1:0:0:1.1', 'finish', u'2008/05/01'))), 0)
      < (((u'pid', 5), (u'cid', 5), 'FB-0:2::0-1:0:0', 'GTW.OMP.SRM.Regatta_Event'), ('FB-0:2::0-1:0:0:0', 'name', u'Himmelfahrt'), ('FB-0:2::0-1:0:0:1', 'date', (('FB-0:2::0-1:0:0:1.0', 'start', u'2008/05/01'), ('FB-0:2::0-1:0:0:1.1', 'finish', u'2008/05/01'))), 0)
    <Field_Entity FB-0:2::0-2:0 'skipper' 'GTW.OMP.SRM.Sailor'> True True
      > fDjH5uIO03Wdnc5gX3D7C88Msxfp807Dd15LdA
      < fDjH5uIO03Wdnc5gX3D7C88Msxfp807Dd15LdA
      > (((u'pid', 4), (u'cid', 4), 'FB-0:2::0-2:0', 'GTW.OMP.SRM.Sailor'), ('FB-0:2::0-2:0:0', 'left'), ('FB-0:2::0-2:0:1', 'nation', u'AUT'), ('FB-0:2::0-2:0:2', 'mna_number', u'29676'), ('FB-0:2::0-2:0:3', 'club'), 0)
      < (((u'pid', 4), (u'cid', 4), 'FB-0:2::0-2:0', 'GTW.OMP.SRM.Sailor'), ('FB-0:2::0-2:0:0', 'left'), ('FB-0:2::0-2:0:1', 'nation', u'AUT'), ('FB-0:2::0-2:0:2', 'mna_number', u'29676'), ('FB-0:2::0-2:0:3', 'club'), 0)
    <Field_Entity FB-0:2::0-2:0:0 'left' 'GTW.OMP.PAP.Person'> True True
      > jCVvrVL7cxthrwL4:mPenABA:H4vtKSITQhTuA
      < jCVvrVL7cxthrwL4:mPenABA:H4vtKSITQhTuA
      > (((u'pid', 3), (u'cid', 3), 'FB-0:2::0-2:0:0', 'GTW.OMP.PAP.Person'), ('FB-0:2::0-2:0:0:0', 'last_name', u'Tanzer'), ('FB-0:2::0-2:0:0:1', 'first_name', u'Laurens'), ('FB-0:2::0-2:0:0:2', 'middle_name', u''), ('FB-0:2::0-2:0:0:3', 'title', u''), 0)
      < (((u'pid', 3), (u'cid', 3), 'FB-0:2::0-2:0:0', 'GTW.OMP.PAP.Person'), ('FB-0:2::0-2:0:0:0', 'last_name', u'Tanzer'), ('FB-0:2::0-2:0:0:1', 'first_name', u'Laurens'), ('FB-0:2::0-2:0:0:2', 'middle_name', u''), ('FB-0:2::0-2:0:0:3', 'title', u''), 0)
    <Field_Entity FB-0:2::0-2:0:3 'club' 'GTW.OMP.SRM.Club'> True True
      > diNMsTC-2yU41VucKcBWUSQGe1b0O2mYXb8WjQ
      < diNMsTC-2yU41VucKcBWUSQGe1b0O2mYXb8WjQ
      > (((u'pid', None), (u'cid', None), 'FB-0:2::0-2:0:3', 'GTW.OMP.SRM.Club'), ('FB-0:2::0-2:0:3:0', 'name', u''), 0)
      < (((u'pid', None), (u'cid', None), 'FB-0:2::0-2:0:3', 'GTW.OMP.SRM.Club'), ('FB-0:2::0-2:0:3:0', 'name', u''), 0)

    >>> v.edit.get ("pid")

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
    Conflict: Edit conflict: at least one value was changed asynchronously by another request.
    >>> p ### after `p.set (middle_name = "w.")`
    GTW.OMP.PAP.Person (u'tanzer', u'laurens', u'w.', u'')

    >>> fv.apply (scope, _sid = 1)
    Traceback (most recent call last):
      ...
    Corrupted: The edit session has expired or the form values are corrupted.

    >>> gv = Value.from_json (json_copy)
    >>> gv.changes_t
    11
    >>> for v in gv.transitive_iter () :
    ...     print v
    <Form FB>, init-v = '', sid = 0, changes = 0
    <Entity FB-0 'Boat' 'GTW.OMP.SRM.Boat'>, init-v = [], sid = NlcOLOnkFT9tdwf027AmLo5cyc8NKlL6iEVddg, changes = 2
    <Field_Entity FB-0:0:0 'left' 'GTW.OMP.SRM.Boat_Class'>, init-v = [], sid = 2SMjmpittgN68fuUf1yK7xN-uRxHK4q2kDJOlA, changes = 1
    <Field FB-0:0:0:0 'name'>, init-v = '', edit-v = 'Optimist', changes = 1
    <Field FB-0:0:1 'nation'>, init-v = '', edit-v = 'AUT', changes = 1
    <Field FB-0:0:2 'sail_number'>, init-v = '', edit-v = '1107', changes = 1
    <Field FB-0:0:3 'sail_number_x'>, init-v = '', changes = 0
    <Field FB-0:1:0 'name'>, init-v = '', changes = 0
    <Entity_Link FB-0:2::p 'Boat_in_Regatta' 'GTW.OMP.SRM.Boat_in_Regatta'>, init-v = [], sid = MilQWW-BQ:1Kfxi2ptEelkCAqwhaXWaRbFloTA, changes = 0
    <Field_Role_Hidden FB-0:2::p-0 'left' 'GTW.OMP.SRM.Boat'>, init-v = [], sid = emH:n2fr5Vojp8:mNyEhadFeTvrt0Hb26l7S4Q, changes = 0, role_id = FB-0
    <Field_Entity FB-0:2::p-1:0 'right' 'GTW.OMP.SRM.Regatta'>, init-v = [], sid = n4dFoUTWL2ZKZ1e-igGdLTtkVfW3LOxorspVfw, changes = 0
    <Field_Entity FB-0:2::p-1:0:0 'left' 'GTW.OMP.SRM.Regatta_Event'>, init-v = [], sid = EgH8LtkA05g5MO-6ez4Hbj7J:Lb-almSesfpGQ, changes = 1
    <Field FB-0:2::p-1:0:0:0 'name'>, init-v = '', edit-v = 'Himmelfahrt', changes = 1
    <Field_Composite FB-0:2::p-1:0:0:1 'date' 'MOM.Date_Interval_C'>, init-v = '', changes = 2
    <Field FB-0:2::p-1:0:0:1.0 'start'>, init-v = '', edit-v = '2008/05/01', changes = 1
    <Field FB-0:2::p-1:0:0:1.1 'finish'>, init-v = '', edit-v = '2008/05/01', changes = 1
    <Field_Entity FB-0:2::p-2:0 'skipper' 'GTW.OMP.SRM.Sailor'>, init-v = [], sid = VdaPLnEfWE8YrlzFrGXYLZgp5jLgdQt1avEw7A, changes = 2
    <Field_Entity FB-0:2::p-2:0:0 'left' 'GTW.OMP.PAP.Person'>, init-v = [], sid = Z:YWrkrkIu19OHcrW0W6DFmkEXuuZ7TAjiV5qQ, changes = 3
    <Field FB-0:2::p-2:0:0:0 'last_name'>, init-v = '', edit-v = 'Tanzer', changes = 1
    <Field FB-0:2::p-2:0:0:1 'first_name'>, init-v = '', edit-v = 'Laurens', changes = 1
    <Field FB-0:2::p-2:0:0:2 'middle_name'>, init-v = '', edit-v = 'William II', changes = 1
    <Field FB-0:2::p-2:0:0:3 'title'>, init-v = '', changes = 0
    <Field FB-0:2::p-2:0:1 'nation'>, init-v = '', edit-v = 'AUT', changes = 1
    <Field FB-0:2::p-2:0:2 'mna_number'>, init-v = '', edit-v = '29676', changes = 1
    <Field_Entity FB-0:2::p-2:0:3 'club' 'GTW.OMP.SRM.Club'>, init-v = [], sid = diNMsTC-2yU41VucKcBWUSQGe1b0O2mYXb8WjQ, changes = 0
    <Field FB-0:2::p-2:0:3:0 'name'>, init-v = '', changes = 0
    <Field FB-0:2::p-3:0 'place'>, init-v = '', changes = 0
    <Field FB-0:2::p-3:1 'points'>, init-v = '', changes = 0

    >>> key = TFL.Sorted_By ("elem.rank", "-id")
    >>> for v in sorted (gv.entity_children (), key = key) :
    ...     print v.elem
    <Field_Entity FB-0:2::p-2:0:3 'club' 'GTW.OMP.SRM.Club'>
    <Field_Entity FB-0:2::p-2:0:0 'left' 'GTW.OMP.PAP.Person'>
    <Field_Entity FB-0:2::p-2:0 'skipper' 'GTW.OMP.SRM.Sailor'>
    <Field_Entity FB-0:2::p-1:0:0 'left' 'GTW.OMP.SRM.Regatta_Event'>
    <Field_Entity FB-0:2::p-1:0 'right' 'GTW.OMP.SRM.Regatta'>
    <Field_Role_Hidden FB-0:2::p-0 'left' 'GTW.OMP.SRM.Boat'>
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
                , { '$id' : 'FB-0:0:3'
                  , 'value' :
                      {}
                  }
                , { '$id' : 'FB-0:1:0'
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
                              , 'value' :
                                  { 'edit' : 'Himmelfahrt' }
                              }
                            , { '$id' : 'FB-0:2::p-1:0:0:1'
                              , 'children' :
                                  [ { '$id' : 'FB-0:2::p-1:0:0:1.0'
                                    , 'value' :
                                        { 'edit' : '2008/05/01' }
                                    }
                                  , { '$id' : 'FB-0:2::p-1:0:0:1.1'
                                    , 'value' :
                                        { 'edit' : '2008/05/01' }
                                    }
                                  ]
                              , 'value' :
                                  { 'edit' : '' }
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
                      , { '$id' : 'FB-0:2::p-2:0:3'
                        , 'children' :
                            [ { '$id' : 'FB-0:2::p-2:0:3:0'
                              , 'value' :
                                  {}
                              }
                            ]
                        , 'value' :
                            {}
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
      > NlcOLOnkFT9tdwf027AmLo5cyc8NKlL6iEVddg
      < NlcOLOnkFT9tdwf027AmLo5cyc8NKlL6iEVddg
      > (((u'pid', None), (u'cid', None), 'FB-0', 'GTW.OMP.SRM.Boat'), ('FB-0:0:0', 'left'), ('FB-0:0:1', 'nation', u''), ('FB-0:0:2', 'sail_number', u''), ('FB-0:0:3', 'sail_number_x', u''), ('FB-0:1:0', 'name', u''), 0)
      < (((u'pid', None), (u'cid', None), 'FB-0', 'GTW.OMP.SRM.Boat'), ('FB-0:0:0', 'left'), ('FB-0:0:1', 'nation', u''), ('FB-0:0:2', 'sail_number', u''), ('FB-0:0:3', 'sail_number_x', u''), ('FB-0:1:0', 'name', u''), 0)
    <Field_Entity FB-0:0:0 'left' 'GTW.OMP.SRM.Boat_Class'> True True
      > 2SMjmpittgN68fuUf1yK7xN-uRxHK4q2kDJOlA
      < 2SMjmpittgN68fuUf1yK7xN-uRxHK4q2kDJOlA
      > (((u'pid', None), (u'cid', None), 'FB-0:0:0', 'GTW.OMP.SRM.Boat_Class'), ('FB-0:0:0:0', 'name', u''), 0)
      < (((u'pid', None), (u'cid', None), 'FB-0:0:0', 'GTW.OMP.SRM.Boat_Class'), ('FB-0:0:0:0', 'name', u''), 0)
    <Entity_Link FB-0:2::0 'Boat_in_Regatta' 'GTW.OMP.SRM.Boat_in_Regatta'> True True
      > MilQWW-BQ:1Kfxi2ptEelkCAqwhaXWaRbFloTA
      < MilQWW-BQ:1Kfxi2ptEelkCAqwhaXWaRbFloTA
      > (((u'pid', None), (u'cid', None), 'FB-0:2::0', 'GTW.OMP.SRM.Boat_in_Regatta'), ('FB-0:2::0-0', 'left'), ('FB-0:2::0-1:0', 'right'), ('FB-0:2::0-2:0', 'skipper'), ('FB-0:2::0-3:0', 'place', u''), ('FB-0:2::0-3:1', 'points', u''), 0)
      < (((u'pid', None), (u'cid', None), 'FB-0:2::0', 'GTW.OMP.SRM.Boat_in_Regatta'), ('FB-0:2::0-0', 'left'), ('FB-0:2::0-1:0', 'right'), ('FB-0:2::0-2:0', 'skipper'), ('FB-0:2::0-3:0', 'place', u''), ('FB-0:2::0-3:1', 'points', u''), 0)
    <Field_Role_Hidden FB-0:2::0-0 'left' 'GTW.OMP.SRM.Boat'> True True
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
      > EgH8LtkA05g5MO-6ez4Hbj7J:Lb-almSesfpGQ
      < EgH8LtkA05g5MO-6ez4Hbj7J:Lb-almSesfpGQ
      > (((u'pid', None), (u'cid', None), 'FB-0:2::0-1:0:0', 'GTW.OMP.SRM.Regatta_Event'), ('FB-0:2::0-1:0:0:0', 'name', u''), ('FB-0:2::0-1:0:0:1', 'date', (('FB-0:2::0-1:0:0:1.0', 'start', u''), ('FB-0:2::0-1:0:0:1.1', 'finish', u''))), 0)
      < (((u'pid', None), (u'cid', None), 'FB-0:2::0-1:0:0', 'GTW.OMP.SRM.Regatta_Event'), ('FB-0:2::0-1:0:0:0', 'name', u''), ('FB-0:2::0-1:0:0:1', 'date', (('FB-0:2::0-1:0:0:1.0', 'start', u''), ('FB-0:2::0-1:0:0:1.1', 'finish', u''))), 0)
    <Field_Entity FB-0:2::0-2:0 'skipper' 'GTW.OMP.SRM.Sailor'> True True
      > VdaPLnEfWE8YrlzFrGXYLZgp5jLgdQt1avEw7A
      < VdaPLnEfWE8YrlzFrGXYLZgp5jLgdQt1avEw7A
      > (((u'pid', None), (u'cid', None), 'FB-0:2::0-2:0', 'GTW.OMP.SRM.Sailor'), ('FB-0:2::0-2:0:0', 'left'), ('FB-0:2::0-2:0:1', 'nation', u''), ('FB-0:2::0-2:0:2', 'mna_number', u''), ('FB-0:2::0-2:0:3', 'club'), 0)
      < (((u'pid', None), (u'cid', None), 'FB-0:2::0-2:0', 'GTW.OMP.SRM.Sailor'), ('FB-0:2::0-2:0:0', 'left'), ('FB-0:2::0-2:0:1', 'nation', u''), ('FB-0:2::0-2:0:2', 'mna_number', u''), ('FB-0:2::0-2:0:3', 'club'), 0)
    <Field_Entity FB-0:2::0-2:0:0 'left' 'GTW.OMP.PAP.Person'> True True
      > Z:YWrkrkIu19OHcrW0W6DFmkEXuuZ7TAjiV5qQ
      < Z:YWrkrkIu19OHcrW0W6DFmkEXuuZ7TAjiV5qQ
      > (((u'pid', None), (u'cid', None), 'FB-0:2::0-2:0:0', 'GTW.OMP.PAP.Person'), ('FB-0:2::0-2:0:0:0', 'last_name', u''), ('FB-0:2::0-2:0:0:1', 'first_name', u''), ('FB-0:2::0-2:0:0:2', 'middle_name', u''), ('FB-0:2::0-2:0:0:3', 'title', u''), 0)
      < (((u'pid', None), (u'cid', None), 'FB-0:2::0-2:0:0', 'GTW.OMP.PAP.Person'), ('FB-0:2::0-2:0:0:0', 'last_name', u''), ('FB-0:2::0-2:0:0:1', 'first_name', u''), ('FB-0:2::0-2:0:0:2', 'middle_name', u''), ('FB-0:2::0-2:0:0:3', 'title', u''), 0)
    <Field_Entity FB-0:2::0-2:0:3 'club' 'GTW.OMP.SRM.Club'> True True
      > diNMsTC-2yU41VucKcBWUSQGe1b0O2mYXb8WjQ
      < diNMsTC-2yU41VucKcBWUSQGe1b0O2mYXb8WjQ
      > (((u'pid', None), (u'cid', None), 'FB-0:2::0-2:0:3', 'GTW.OMP.SRM.Club'), ('FB-0:2::0-2:0:3:0', 'name', u''), 0)
      < (((u'pid', None), (u'cid', None), 'FB-0:2::0-2:0:3', 'GTW.OMP.SRM.Club'), ('FB-0:2::0-2:0:3:0', 'name', u''), 0)

    >>> em  = PAP.Email ("laurens.tanzer@gmail.com")
    >>> phe = PAP.Person_has_Email (p, em)
    >>> scope.commit ()
    >>> fp  = Form ("FP", children = [xl])
    >>> fip = fp (PAP.Person, p)

    >>> for i in fip.transitive_iter () :
    ...     print i.elem, sorted ((i.value or {}).iteritems ())
    <Form FP> [('sid', 0)]
    <Entity FP-0 'Person' 'GTW.OMP.PAP.Person'> [(u'init', {'pid': 3, 'uid': u'Tanzer Laurens w.', 'cid': 14}), ('sid', '4Gp-GodgH3Th6drkjYZW-MMO11Gj2tVjwN2:Fw')]
    <Fieldset FP-0:0 'primary'> []
    <Field FP-0:0:0 'last_name'> [(u'init', u'Tanzer')]
    <Field FP-0:0:1 'first_name'> [(u'init', u'Laurens')]
    <Field FP-0:0:2 'middle_name'> [(u'init', u'w.')]
    <Field FP-0:0:3 'title'> []
    <Fieldset FP-0:1 'necessary'> []
    <Field FP-0:1:0 'sex'> []
    <Fieldset FP-0:2 'optional'> []
    <Field_Composite FP-0:2:0 'lifetime' 'MOM.Date_Interval'> []
    <Field FP-0:2:0.0 'start'> []
    <Field FP-0:2:0.1 'finish'> []
    <Field FP-0:2:1 'salutation'> []
    <Entity_List FP-0:3 'Person_has_Address' <Entity_Link FP-0:3::p 'Person_has_Address' 'GTW.OMP.PAP.Person_has_Address'>> []
    <Entity_List FP-0:4 'Person_has_Email' <Entity_Link FP-0:4::p 'Person_has_Email' 'GTW.OMP.PAP.Person_has_Email'>> []
    <Entity_Link FP-0:4::0 'Person_has_Email' 'GTW.OMP.PAP.Person_has_Email'> [(u'init', {'pid': 9, 'uid': u'Tanzer Laurens w., laurens.tanzer@gmail.com', 'cid': 21}), ('sid', '0h-NmC95N:Y:4uztMBxanDk2LEG2uquvQnQ-RQ')]
    <Field_Role_Hidden FP-0:4::0-0 'left' 'GTW.OMP.PAP.Person'> [(u'init', {'pid': 3, 'uid': u'Tanzer Laurens w.', 'cid': 14}), ('sid', '2MaKwqFALvptOXWHXpjCUdAh6mbHpOTbVoQREQ')]
    <Fieldset FP-0:4::0-1 'primary'> []
    <Field_Entity FP-0:4::0-1:0 'right' 'GTW.OMP.PAP.Email'> [(u'init', {'pid': 8, 'uid': u'laurens.tanzer@gmail.com', 'cid': 20}), ('sid', '3n3GioDrGc5OaUvxfFCZFOfE8jTv:CQJd7vsnA')]
    <Field FP-0:4::0-1:0:0 'address'> [(u'init', u'laurens.tanzer@gmail.com')]
    <Fieldset FP-0:4::0-2 'optional'> []
    <Field FP-0:4::0-2:0 'desc'> []
    <Entity_List FP-0:5 'Person_has_Phone' <Entity_Link FP-0:5::p 'Person_has_Phone' 'GTW.OMP.PAP.Person_has_Phone'>> []

    >>> for i in fip.transitive_iter () :
    ...     e = i.elem
    ...     print e.__class__.__name__, e._name, getattr (e, "ui_name", ""), repr (getattr (e, "description", "").replace (NL, " ")), e.renderer
    Form None  u'' afs_div_seq
    Entity Person Person u'Model a person.' afs_div_seq
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
    Entity_List Person_has_Address Person_has_Address u'Model the link between a person and an address' afs_div_seq
    Entity_List Person_has_Email Person_has_Email u'Model the link between a person and an email address' afs_div_seq
    Entity_Link Person_has_Email Person_has_Email u'Model the link between a person and an email address' afs_div_seq
    Field_Role_Hidden left Person u'' afs_div_seq
    Fieldset primary  u'' afs_div_seq
    Field_Entity right Email u'Email address of person' afs_div_seq
    Field address Email address u'Email address (including domain)' None
    Fieldset optional  u'' afs_div_seq
    Field desc Description u'Short description of the link' None
    Entity_List Person_has_Phone Person_has_Phone u'Model the link between a person and a phone number' afs_div_seq

"""

_entity_links_group = """
    >>> scope = Scaffold.scope ("hps://") # doctest:+ELLIPSIS
    Creating new scope MOMT__...
    >>> from _GTW._AFS._MOM import Spec
    >>> S = Spec.Entity (include_links = ("addresses", ), entity_links_group = "Entity_Links_Group")
    >>> x = S (scope.PAP.Person.E_Type)
    >>> print repr (x)
    <Entity None 'Person' 'GTW.OMP.PAP.Person'>
     <Fieldset None 'primary'>
      <Field None 'last_name'>
      <Field None 'first_name'>
      <Field None 'middle_name'>
      <Field None 'title'>
     <Fieldset None 'necessary'>
      <Field None 'sex'>
     <Fieldset None 'optional'>
      <Field_Composite None 'lifetime' 'MOM.Date_Interval'>
       <Field None 'start'>
       <Field None 'finish'>
      <Field None 'salutation'>
     <Group None>
      <Entity_List None 'Person_has_Address' <Entity_Link None 'Person_has_Address' 'GTW.OMP.PAP.Person_has_Address'>>
       <Entity_Link None 'Person_has_Address' 'GTW.OMP.PAP.Person_has_Address'>
        <Field_Role_Hidden None 'left' 'GTW.OMP.PAP.Person'>
        <Fieldset None 'primary'>
         <Field_Entity None 'right' 'GTW.OMP.PAP.Address'>
          <Field None 'street'>
          <Field None 'zip'>
          <Field None 'city'>
          <Field None 'country'>
        <Fieldset None 'optional'>
         <Field None 'desc'>
    >>> print repr (Form ("ELG", children = [x]))
    <Form ELG>
     <Entity ELG-0 'Person' 'GTW.OMP.PAP.Person'>
      <Fieldset ELG-0:0 'primary'>
       <Field ELG-0:0:0 'last_name'>
       <Field ELG-0:0:1 'first_name'>
       <Field ELG-0:0:2 'middle_name'>
       <Field ELG-0:0:3 'title'>
      <Fieldset ELG-0:1 'necessary'>
       <Field ELG-0:1:0 'sex'>
      <Fieldset ELG-0:2 'optional'>
       <Field_Composite ELG-0:2:0 'lifetime' 'MOM.Date_Interval'>
        <Field ELG-0:2:0.0 'start'>
        <Field ELG-0:2:0.1 'finish'>
       <Field ELG-0:2:1 'salutation'>
      <Group ELG-0:3>
       <Entity_List ELG-0:3:0 'Person_has_Address' <Entity_Link ELG-0:3:0::p 'Person_has_Address' 'GTW.OMP.PAP.Person_has_Address'>>
        <Entity_Link ELG-0:3:0::p 'Person_has_Address' 'GTW.OMP.PAP.Person_has_Address'>
         <Field_Role_Hidden ELG-0:3:0::p-0 'left' 'GTW.OMP.PAP.Person'>
         <Fieldset ELG-0:3:0::p-1 'primary'>
          <Field_Entity ELG-0:3:0::p-1:0 'right' 'GTW.OMP.PAP.Address'>
           <Field ELG-0:3:0::p-1:0:0 'street'>
           <Field ELG-0:3:0::p-1:0:1 'zip'>
           <Field ELG-0:3:0::p-1:0:2 'city'>
           <Field ELG-0:3:0::p-1:0:3 'country'>
         <Fieldset ELG-0:3:0::p-2 'optional'>
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
{"$id":"FB","sid":0,"$child_ids":["FB-0","FB-0:2::0"],"FB-0":{"init":{"cid":2,"pid":2},"sid":"hr-jUx4QHTv6rHr09XNKhgpG8von21skUQ4C9Q","$id":"FB-0","$child_ids":["FB-0:0:0","FB-0:0:1","FB-0:0:2","FB-0:0:3","FB-0:1:0"],"edit":{"cid":2,"pid":2},"FB-0:0:0":{"init":{"cid":1,"pid":1},"sid":"qPzMz88f1x3RjbWOPHj4PR2ZthTO:EW:MNddnA","$id":"FB-0:0:0","$child_ids":["FB-0:0:0:0"],"edit":{"cid":1,"pid":1},"anchor_id":"FB-0","FB-0:0:0:0":{"init":"Optimist"}},"FB-0:0:1":{"init":"AUT"},"FB-0:0:2":{"init":"1107"},"FB-0:0:3":{"init":""},"FB-0:1:0":{"init":""}},"FB-0:2::0":{"init":{"cid":7,"pid":7},"sid":"WL-78I4-zhVeNm1-xWrXjotyN8mcfb-yZGgf6A","$id":"FB-0:2::0","$child_ids":["FB-0:2::0-0","FB-0:2::0-1:0","FB-0:2::0-2:0","FB-0:2::0-3:0","FB-0:2::0-3:1"],"edit":{"cid":7,"pid":7},"FB-0:2::0-0":{"init":{"cid":2,"pid":2},"sid":"ORsB0LFjw5hzuHauaOA1M3usp415XdhUdQ0tfQ","role_id":"FB-0","edit":{"cid":2,"pid":2}},"FB-0:2::0-1:0":{"init":{"cid":6,"pid":6},"sid":"t0nRFI5GFozOgzRVAMlfEVZeU9oCHiVfFTBuWw","$id":"FB-0:2::0-1:0","$child_ids":["FB-0:2::0-1:0:0"],"edit":{"cid":6,"pid":6},"anchor_id":"FB-0:2::0","FB-0:2::0-1:0:0":{"init":{"cid":5,"pid":5},"sid":"siR36p3Hsut0dtJQl-h3TjrWxG6qhX9soaq6:g","$id":"FB-0:2::0-1:0:0","$child_ids":["FB-0:2::0-1:0:0:0","FB-0:2::0-1:0:0:1"],"edit":{"cid":5,"pid":5},"anchor_id":"FB-0:2::0-1:0","FB-0:2::0-1:0:0:0":{"init":"Himmelfahrt"},"FB-0:2::0-1:0:0:1":{"$id":"FB-0:2::0-1:0:0:1","$child_ids":["FB-0:2::0-1:0:0:1.0","FB-0:2::0-1:0:0:1.1"],"anchor_id":"FB-0:2::0-1:0:0","FB-0:2::0-1:0:0:1.0":{"init":"2008/05/01"},"FB-0:2::0-1:0:0:1.1":{"init":"2008/05/01"}}}},"FB-0:2::0-2:0":{"init":{"cid":4,"pid":4},"sid":"fDjH5uIO03Wdnc5gX3D7C88Msxfp807Dd15LdA","$id":"FB-0:2::0-2:0","$child_ids":["FB-0:2::0-2:0:0","FB-0:2::0-2:0:1","FB-0:2::0-2:0:2","FB-0:2::0-2:0:3"],"edit":{"cid":4,"pid":4},"anchor_id":"FB-0:2::0","FB-0:2::0-2:0:0":{"init":{"cid":3,"pid":3},"sid":"jCVvrVL7cxthrwL4:mPenABA:H4vtKSITQhTuA","$id":"FB-0:2::0-2:0:0","$child_ids":["FB-0:2::0-2:0:0:0","FB-0:2::0-2:0:0:1","FB-0:2::0-2:0:0:2","FB-0:2::0-2:0:0:3"],"edit":{"cid":3,"pid":3},"anchor_id":"FB-0:2::0-2:0","FB-0:2::0-2:0:0:0":{"init":"Tanzer"},"FB-0:2::0-2:0:0:1":{"init":"Laurens"},"FB-0:2::0-2:0:0:2":{"init":"","edit":"William"},"FB-0:2::0-2:0:0:3":{"init":""}},"FB-0:2::0-2:0:1":{"init":"AUT"},"FB-0:2::0-2:0:2":{"init":"29676"},"FB-0:2::0-2:0:3":{"init":{"cid":null,"pid":null},"sid":"diNMsTC-2yU41VucKcBWUSQGe1b0O2mYXb8WjQ","$id":"FB-0:2::0-2:0:3","$child_ids":["FB-0:2::0-2:0:3:0"],"edit":{"cid":null,"pid":null},"anchor_id":"FB-0:2::0-2:0","FB-0:2::0-2:0:3:0":{"init":""}}},"FB-0:2::0-3:0":{"init":""},"FB-0:2::0-3:1":{"init":""}}}
"""
json_copy = """\
{"$id":"FB","sid":0,"$child_ids":["FB-0","FB-0:2::0"],"FB-0":{"init":{},"sid":"NlcOLOnkFT9tdwf027AmLo5cyc8NKlL6iEVddg","$id":"FB-0","$child_ids":["FB-0:0:0","FB-0:0:1","FB-0:0:2","FB-0:0:3","FB-0:1:0"],"edit":{},"FB-0:0:0":{"init":{},"sid":"2SMjmpittgN68fuUf1yK7xN-uRxHK4q2kDJOlA","$id":"FB-0:0:0","$child_ids":["FB-0:0:0:0"],"edit":{},"anchor_id":"FB-0","FB-0:0:0:0":{"edit":"Optimist","init":""}},"FB-0:0:1":{"edit":"AUT","init":""},"FB-0:0:2":{"edit":"1107","init":""},"FB-0:0:3":{"init":""},"FB-0:1:0":{"init":""}},"FB-0:2::0":{"init":{},"sid":"MilQWW-BQ:1Kfxi2ptEelkCAqwhaXWaRbFloTA","$id":"FB-0:2::0","$child_ids":["FB-0:2::0-0","FB-0:2::0-1:0","FB-0:2::0-2:0","FB-0:2::0-3:0","FB-0:2::0-3:1"],"edit":{},"FB-0:2::0-0":{"init":{},"sid":"emH:n2fr5Vojp8:mNyEhadFeTvrt0Hb26l7S4Q","role_id":"FB-0","edit":{}},"FB-0:2::0-1:0":{"init":{},"sid":"n4dFoUTWL2ZKZ1e-igGdLTtkVfW3LOxorspVfw","$id":"FB-0:2::0-1:0","$child_ids":["FB-0:2::0-1:0:0"],"edit":{},"anchor_id":"FB-0:2::0","FB-0:2::0-1:0:0":{"init":{},"sid":"EgH8LtkA05g5MO-6ez4Hbj7J:Lb-almSesfpGQ","$id":"FB-0:2::0-1:0:0","$child_ids":["FB-0:2::0-1:0:0:0","FB-0:2::0-1:0:0:1"],"edit":{},"anchor_id":"FB-0:2::0-1:0","FB-0:2::0-1:0:0:0":{"edit":"Himmelfahrt","init":""},"FB-0:2::0-1:0:0:1":{"$id":"FB-0:2::0-1:0:0:1","$child_ids":["FB-0:2::0-1:0:0:1.0","FB-0:2::0-1:0:0:1.1"],"anchor_id":"FB-0:2::0-1:0:0","FB-0:2::0-1:0:0:1.0":{"edit":"2008/05/01","init":""},"FB-0:2::0-1:0:0:1.1":{"edit":"2008/05/01","init":""}}}},"FB-0:2::0-2:0":{"init":{},"sid":"VdaPLnEfWE8YrlzFrGXYLZgp5jLgdQt1avEw7A","$id":"FB-0:2::0-2:0","$child_ids":["FB-0:2::0-2:0:0","FB-0:2::0-2:0:1","FB-0:2::0-2:0:2","FB-0:2::0-2:0:3"],"edit":{},"anchor_id":"FB-0:2::0","FB-0:2::0-2:0:0":{"init":{},"sid":"Z:YWrkrkIu19OHcrW0W6DFmkEXuuZ7TAjiV5qQ","$id":"FB-0:2::0-2:0:0","$child_ids":["FB-0:2::0-2:0:0:0","FB-0:2::0-2:0:0:1","FB-0:2::0-2:0:0:2","FB-0:2::0-2:0:0:3"],"edit":{},"anchor_id":"FB-0:2::0-2:0","FB-0:2::0-2:0:0:0":{"edit":"Tanzer","init":""},"FB-0:2::0-2:0:0:1":{"edit":"Laurens","init":""},"FB-0:2::0-2:0:0:2":{"init":"","edit":"William II"},"FB-0:2::0-2:0:0:3":{"init":""}},"FB-0:2::0-2:0:1":{"edit":"AUT","init":""},"FB-0:2::0-2:0:2":{"edit":"29676","init":""},"FB-0:2::0-2:0:3":{"init":{},"sid":"diNMsTC-2yU41VucKcBWUSQGe1b0O2mYXb8WjQ","$id":"FB-0:2::0-2:0:3","$child_ids":["FB-0:2::0-2:0:3:0"],"edit":{},"anchor_id":"FB-0:2::0-2:0","FB-0:2::0-2:0:3:0":{"init":""}}},"FB-0:2::0-3:0":{"init":""},"FB-0:2::0-3:1":{"init":""}}}
"""
json_bad  = """{"$id":"FC"}"""

__test__ = dict \
    ( AFS_Spec           = _test_code
    , Entity_Links_Group = _entity_links_group
    )

### __END__ AFS_Spec
