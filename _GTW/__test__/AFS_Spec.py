# -*- coding: iso-8859-15 -*-
# Copyright (C) 2011-2013 Mag. Christian Tanzer All rights reserved
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
#    26-Jan-2012 (CT) Add `_prefilled_test`
#    15-Feb-2012 (CT) Add `Crew_Member.max_links` to `_prefilled_test`
#    27-Feb-2012 (CT) Add tests for `.names`
#    29-Feb-2012 (CT) Add tests for `anchor_id`
#     5-Mar-2012 (CT) Add tests for `allow_new`
#     8-Mar-2012 (CT) Adapt tests to changes in AFS handling (allow_new...)
#     9-Mar-2012 (CT) Add tests for `allow_new`
#    19-Mar-2012 (CT) Adapt to reification of `SRM.Handicap`
#    15-Apr-2012 (CT) Use `formatted_1` instead of `sorted` to guarantee
#                     determistic order of nested dicts
#    ««revision-date»»···
#--

from __future__ import unicode_literals

_test_code = """
    >>> scope = Scaffold.scope ("hps://") # doctest:+ELLIPSIS
    Creating new scope MOMT__...
    >>> from _GTW._AFS._MOM import Spec
    >>> S = Spec.Entity ()
    >>> x = S (scope.PAP.Person.E_Type)
    >>> print x.formatted ()
    <Entity None 'Person' 'PAP.Person'>
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
    >>> print xl.formatted ()
    <Entity None 'Person' 'PAP.Person'>
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
     <Entity_List None 'Person_has_Address' <Entity_Link None 'Person_has_Address' 'PAP.Person_has_Address'>>
      <Entity_Link None 'Person_has_Address' 'PAP.Person_has_Address'>
       <Field_Role_Hidden None 'left' 'PAP.Person'>
       <Fieldset None 'primary'>
        <Field_Entity None 'right' 'PAP.Address'>
         <Field None 'street'>
         <Field None 'zip'>
         <Field None 'city'>
         <Field None 'country'>
       <Fieldset None 'optional'>
        <Field None 'desc'>
     <Entity_List None 'Person_has_Email' <Entity_Link None 'Person_has_Email' 'PAP.Person_has_Email'>>
      <Entity_Link None 'Person_has_Email' 'PAP.Person_has_Email'>
       <Field_Role_Hidden None 'left' 'PAP.Person'>
       <Fieldset None 'primary'>
        <Field_Entity None 'right' 'PAP.Email'>
         <Field None 'address'>
       <Fieldset None 'optional'>
        <Field None 'desc'>
     <Entity_List None 'Person_has_Phone' <Entity_Link None 'Person_has_Phone' 'PAP.Person_has_Phone'>>
      <Entity_Link None 'Person_has_Phone' 'PAP.Person_has_Phone'>
       <Field_Role_Hidden None 'left' 'PAP.Person'>
       <Fieldset None 'primary'>
        <Field_Entity None 'right' 'PAP.Phone'>
         <Field None 'country_code'>
         <Field None 'area_code'>
         <Field None 'number'>
        <Field None 'extension'>
       <Fieldset None 'optional'>
        <Field None 'desc'>

    >>> NL = chr (10)
    >>> for e in xl.transitive_iter () :
    ...   print e.__class__.__name__, e._name, getattr (e, "ui_name", None), repr ((getattr (e, "description", "")or "").replace (NL, " ")), e.renderer
    Entity Person Person u'Model a person.' afs_div_seq
    Fieldset primary None u'' afs_div_seq
    Field last_name Last name u'Last name of person' None
    Field first_name First name u'First name of person' None
    Field middle_name Middle name u'Middle name of person' None
    Field title Academic title u'Academic title.' None
    Fieldset necessary None u'' afs_div_seq
    Field sex Sex u'Sex of a person.' None
    Fieldset optional None u'' afs_div_seq
    Field_Composite lifetime Lifetime u'Date of birth [`start`] (and death [`finish`])' afs_fc_horizo
    Field start Start u'Start date of interval' None
    Field finish Finish u'Finish date of interval' None
    Field salutation Salutation u'Salutation to be used when communicating with person (e.g., in a letter or email).' None
    Entity_List Person_has_Address Person_has_Address u'Link a person to a address' afs_div_seq
    Entity_Link Person_has_Address Person_has_Address u'Link a person to a address' afs_div_seq
    Field_Role_Hidden left Person u'Person linked to Address' afs_div_seq
    Fieldset primary None u'' afs_div_seq
    Field_Entity right Address u'Address of person' afs_div_seq
    Field street Street u'Street (or place) and house number' None
    Field zip Zip code u'Zip code of address' None
    Field city City u'City, town, or village' None
    Field country Country u'Country' None
    Fieldset optional None u'' afs_div_seq
    Field desc Description u'Short description of the link' None
    Entity_List Person_has_Email Person_has_Email u'Link a person to a email' afs_div_seq
    Entity_Link Person_has_Email Person_has_Email u'Link a person to a email' afs_div_seq
    Field_Role_Hidden left Person u'Person linked to Email' afs_div_seq
    Fieldset primary None u'' afs_div_seq
    Field_Entity right Email u'Email of person' afs_div_seq
    Field address Email address u'Email address (including domain)' None
    Fieldset optional None u'' afs_div_seq
    Field desc Description u'Short description of the link' None
    Entity_List Person_has_Phone Person_has_Phone u'Link a person to a phone number' afs_div_seq
    Entity_Link Person_has_Phone Person_has_Phone u'Link a person to a phone number' afs_div_seq
    Field_Role_Hidden left Person u'Person linked to Phone' afs_div_seq
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
    >>> print y.formatted ()
    <Entity None 'Page' 'SWP.Page'>
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
     <Entity_List None 'Event' <Entity_Link None 'Event' 'EVT.Event'>>
      <Entity_Link None 'Event' 'EVT.Event'>
       <Field_Role_Hidden None 'left' 'SWP.Page'>
       <Fieldset None 'primary'>
        <Field_Composite None 'date' 'MOM.Date_Interval'>
         <Field None 'start'>
         <Field None 'finish'>
        <Field_Composite None 'time' 'MOM.Time_Interval'>
         <Field None 'start'>
         <Field None 'finish'>
        <Field_Entity None 'calendar' 'EVT.Calendar'>
         <Field None 'name'>
       <Fieldset None 'optional'>
        <Field None 'detail'>
        <Field None 'short_title'>
       <Entity_Link None 'Recurrence_Spec' 'EVT.Recurrence_Spec'>
        <Field_Role_Hidden None 'left' 'EVT.Event'>
        <Fieldset None 'optional'>
         <Field None 'dates'>
         <Field None 'date_exceptions'>
        <Entity_List None 'Recurrence_Rule' <Entity_Link None 'Recurrence_Rule' 'EVT.Recurrence_Rule'>>
         <Entity_Link None 'Recurrence_Rule' 'EVT.Recurrence_Rule'>
          <Field_Role_Hidden None 'left' 'EVT.Recurrence_Spec'>
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

    >>> print Form ("F", children = [y]).formatted ()
    <Form F>
     <Entity F-0 'Page' 'SWP.Page'>
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
      <Entity_List F-0:4 'Event' <Entity_Link F-0:4::p 'Event' 'EVT.Event'>>
       <Entity_Link F-0:4::p 'Event' 'EVT.Event'>
        <Field_Role_Hidden F-0:4::p-0 'left' 'SWP.Page'>
        <Fieldset F-0:4::p-1 'primary'>
         <Field_Composite F-0:4::p-1:0 'date' 'MOM.Date_Interval'>
          <Field F-0:4::p-1:0.0 'start'>
          <Field F-0:4::p-1:0.1 'finish'>
         <Field_Composite F-0:4::p-1:1 'time' 'MOM.Time_Interval'>
          <Field F-0:4::p-1:1.0 'start'>
          <Field F-0:4::p-1:1.1 'finish'>
         <Field_Entity F-0:4::p-1:2 'calendar' 'EVT.Calendar'>
          <Field F-0:4::p-1:2:0 'name'>
        <Fieldset F-0:4::p-2 'optional'>
         <Field F-0:4::p-2:0 'detail'>
         <Field F-0:4::p-2:1 'short_title'>
        <Entity_Link F-0:4::p-3 'Recurrence_Spec' 'EVT.Recurrence_Spec'>
         <Field_Role_Hidden F-0:4::p-3:0 'left' 'EVT.Event'>
         <Fieldset F-0:4::p-3:1 'optional'>
          <Field F-0:4::p-3:1:0 'dates'>
          <Field F-0:4::p-3:1:1 'date_exceptions'>
         <Entity_List F-0:4::p-3:2 'Recurrence_Rule' <Entity_Link F-0:4::p-3:2::p 'Recurrence_Rule' 'EVT.Recurrence_Rule'>>
          <Entity_Link F-0:4::p-3:2::p 'Recurrence_Rule' 'EVT.Recurrence_Rule'>
           <Field_Role_Hidden F-0:4::p-3:2::p-0 'left' 'EVT.Recurrence_Spec'>
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
    >>> print f.formatted ()
    <Form X>
     <Entity X-0 'Person' 'PAP.Person'>
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
     <Entity X-1 'Page' 'SWP.Page'>
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
      <Entity_List X-1:4 'Event' <Entity_Link X-1:4::p 'Event' 'EVT.Event'>>
       <Entity_Link X-1:4::p 'Event' 'EVT.Event'>
        <Field_Role_Hidden X-1:4::p-0 'left' 'SWP.Page'>
        <Fieldset X-1:4::p-1 'primary'>
         <Field_Composite X-1:4::p-1:0 'date' 'MOM.Date_Interval'>
          <Field X-1:4::p-1:0.0 'start'>
          <Field X-1:4::p-1:0.1 'finish'>
         <Field_Composite X-1:4::p-1:1 'time' 'MOM.Time_Interval'>
          <Field X-1:4::p-1:1.0 'start'>
          <Field X-1:4::p-1:1.1 'finish'>
         <Field_Entity X-1:4::p-1:2 'calendar' 'EVT.Calendar'>
          <Field X-1:4::p-1:2:0 'name'>
        <Fieldset X-1:4::p-2 'optional'>
         <Field X-1:4::p-2:0 'detail'>
         <Field X-1:4::p-2:1 'short_title'>
        <Entity_Link X-1:4::p-3 'Recurrence_Spec' 'EVT.Recurrence_Spec'>
         <Field_Role_Hidden X-1:4::p-3:0 'left' 'EVT.Event'>
         <Fieldset X-1:4::p-3:1 'optional'>
          <Field X-1:4::p-3:1:0 'dates'>
          <Field X-1:4::p-3:1:1 'date_exceptions'>
         <Entity_List X-1:4::p-3:2 'Recurrence_Rule' <Entity_Link X-1:4::p-3:2::p 'Recurrence_Rule' 'EVT.Recurrence_Rule'>>
          <Entity_Link X-1:4::p-3:2::p 'Recurrence_Rule' 'EVT.Recurrence_Rule'>
           <Field_Role_Hidden X-1:4::p-3:2::p-0 'left' 'EVT.Recurrence_Spec'>
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

    >>> SB = Spec.Entity (Spec.Entity_Link ("SRM.Boat_in_Regatta"))
    >>> fb = Form ("FB", children = [SB (scope.SRM.Boat)])
    >>> print fb.formatted ()
    <Form FB>
     <Entity FB-0 'Boat' 'SRM.Boat'>
      <Fieldset FB-0:0 'primary'>
       <Field_Entity FB-0:0:0 'left' 'SRM.Boat_Class'>
        <Field FB-0:0:0:0 'name'>
        <Field FB-0:0:0:1 'max_crew'>
       <Field FB-0:0:1 'sail_number'>
       <Field FB-0:0:2 'nation'>
       <Field FB-0:0:3 'sail_number_x'>
      <Fieldset FB-0:1 'optional'>
       <Field FB-0:1:0 'name'>
      <Entity_List FB-0:2 'Boat_in_Regatta' <Entity_Link FB-0:2::p 'Boat_in_Regatta' 'SRM.Boat_in_Regatta'>>
       <Entity_Link FB-0:2::p 'Boat_in_Regatta' 'SRM.Boat_in_Regatta'>
        <Field_Role_Hidden FB-0:2::p-0 'left' 'SRM.Boat'>
        <Fieldset FB-0:2::p-1 'primary'>
         <Field_Entity FB-0:2::p-1:0 'right' 'SRM.Regatta'>
          <Field_Entity FB-0:2::p-1:0:0 'left' 'SRM.Regatta_Event'>
           <Field FB-0:2::p-1:0:0:0 'name'>
           <Field_Composite FB-0:2::p-1:0:0:1 'date' 'MOM.Date_Interval_C'>
            <Field FB-0:2::p-1:0:0:1.0 'start'>
            <Field FB-0:2::p-1:0:0:1.1 'finish'>
          <Field_Entity FB-0:2::p-1:0:1 'boat_class' 'SRM._Boat_Class_'>
           <Field FB-0:2::p-1:0:1:0 'name'>
        <Fieldset FB-0:2::p-2 'required'>
         <Field_Entity FB-0:2::p-2:0 'skipper' 'SRM.Sailor'>
          <Field_Entity FB-0:2::p-2:0:0 'left' 'PAP.Person'>
           <Field FB-0:2::p-2:0:0:0 'last_name'>
           <Field FB-0:2::p-2:0:0:1 'first_name'>
           <Field FB-0:2::p-2:0:0:2 'middle_name'>
           <Field FB-0:2::p-2:0:0:3 'title'>
          <Field FB-0:2::p-2:0:1 'nation'>
          <Field FB-0:2::p-2:0:2 'mna_number'>
          <Field_Entity FB-0:2::p-2:0:3 'club' 'SRM.Club'>
           <Field FB-0:2::p-2:0:3:0 'name'>
        <Fieldset FB-0:2::p-3 'optional'>
         <Field FB-0:2::p-3:0 'place'>
         <Field FB-0:2::p-3:1 'points'>

    >>> PAP = scope.PAP
    >>> SRM = scope.SRM
    >>> bc  = SRM.Boat_Class ("Optimist", max_crew = 1)
    >>> b   = SRM.Boat.instance_or_new (u"Optimist", u"1107", u"AUT", raw = True)
    >>> p   = PAP.Person.instance_or_new (u"Tanzer", u"Laurens")
    >>> s   = SRM.Sailor.instance_or_new (p, nation = u"AUT", mna_number = u"29676", raw = True)
    >>> rev = SRM.Regatta_Event (u"Himmelfahrt", dict (start = u"20080501", raw = True), raw = True)
    >>> reo = SRM.Regatta_C (rev, boat_class = bc)
    >>> bir = SRM.Boat_in_Regatta (b, reo, skipper = s)

    >>> scope.commit ()

    >>> fi  = fb (SRM.Boat, b, form_kw = dict (Boat_in_Regatta = dict (skipper = dict (left = dict (allow_new = False)))))
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

    >>> for e in fb.transitive_iter () :
    ...   if hasattr (e, "allow_new") :
    ...     print "%-20s %-20s %-20s %s" % (e.id, e.type_base_name, e.__class__.__name__, e.allow_new)
    FB-0:0:0             Boat_Class           Field_Entity         True
    FB-0:2::p-0          Boat                 Field_Role_Hidden    False
    FB-0:2::p-1:0        Regatta              Field_Entity         False
    FB-0:2::p-1:0:0      Regatta_Event        Field_Entity         False
    FB-0:2::p-1:0:1      _Boat_Class_         Field_Entity         True
    FB-0:2::p-2:0        Sailor               Field_Entity         True
    FB-0:2::p-2:0:0      Person               Field_Entity         True
    FB-0:2::p-2:0:3      Club                 Field_Entity         True

    >>> for e in fi.transitive_iter () :
    ...   if hasattr (e, "allow_new") :
    ...     print "%-20s %-20s %-20s %s" % (e.id, e.type_base_name, e.elem.__class__.__name__, e.allow_new)
    FB-0:0:0             Boat_Class           Field_Entity         True
    FB-0:2::0-0          Boat                 Field_Role_Hidden    False
    FB-0:2::0-1:0        Regatta              Field_Entity         False
    FB-0:2::0-2:0        Sailor               Field_Entity         True
    FB-0:2::0-2:0:0      Person               Field_Entity         False
    FB-0:2::0-2:0:3      Club                 Field_Entity         True

    >>> for e in fb.transitive_iter () :
    ...   if e.root is not fb :
    ...     print e, e.root
    ...   if e.anchor_id != getattr (e.anchor, "id", None) :
    ...     print e, e.anchor_id, e.anchor
    >>> print e, e.root
    <Field FB-0:2::p-3:1 'points'> <Form FB>

    >>> for e in fb.transitive_iter () :
    ...   if e.names and e.anchor_id :
    ...     print "%-20s %-20s %-20s %-20s %s" % (e.id, e.anchor_id, e.type_base_name, e.__class__.__name__, e.names)
    FB-0:0:0             FB-0                 Boat_Class           Field_Entity         ['left']
    FB-0:2::p            FB-0                 Boat_in_Regatta      Entity_Link          ['Boat_in_Regatta']
    FB-0:2::p-0          FB-0                 Boat                 Field_Role_Hidden    ['Boat_in_Regatta', u'left']
    FB-0:2::p-1:0        FB-0:2::p            Regatta              Field_Entity         ['Boat_in_Regatta', 'right']
    FB-0:2::p-1:0:0      FB-0:2::p-1:0        Regatta_Event        Field_Entity         ['Boat_in_Regatta', 'right', 'left']
    FB-0:2::p-1:0:0:1    FB-0:2::p-1:0:0      Date_Interval_C      Field_Composite      ['Boat_in_Regatta', 'right', 'left', 'date']
    FB-0:2::p-1:0:1      FB-0:2::p-1:0        _Boat_Class_         Field_Entity         ['Boat_in_Regatta', 'right', 'boat_class']
    FB-0:2::p-2:0        FB-0:2::p            Sailor               Field_Entity         ['Boat_in_Regatta', 'skipper']
    FB-0:2::p-2:0:0      FB-0:2::p-2:0        Person               Field_Entity         ['Boat_in_Regatta', 'skipper', 'left']
    FB-0:2::p-2:0:3      FB-0:2::p-2:0        Club                 Field_Entity         ['Boat_in_Regatta', 'skipper', 'club']

    >>> for e in fi.transitive_iter () :
    ...   if e.names and e.anchor_id :
    ...     print "%-20s %-20s %-20s %-20s %s" % (e.id, e.anchor_id, e.type_base_name, e.elem.__class__.__name__, e.names)
    FB-0:0:0             FB-0                 Boat_Class           Field_Entity         ['left']
    FB-0:2::0            FB-0                 Boat_in_Regatta      Entity_Link          ['Boat_in_Regatta']
    FB-0:2::0-0          FB-0                 Boat                 Field_Role_Hidden    ['Boat_in_Regatta', u'left']
    FB-0:2::0-1:0        FB-0:2::0            Regatta              Field_Entity         ['Boat_in_Regatta', 'right']
    FB-0:2::0-2:0        FB-0:2::0            Sailor               Field_Entity         ['Boat_in_Regatta', 'skipper']
    FB-0:2::0-2:0:0      FB-0:2::0-2:0        Person               Field_Entity         ['Boat_in_Regatta', 'skipper', 'left']
    FB-0:2::0-2:0:3      FB-0:2::0-2:0        Club                 Field_Entity         ['Boat_in_Regatta', 'skipper', 'club']

    >>> print formatted (fi.as_json_cargo, level = 1)
      { '$id' : 'FB'
      , 'children' :
          [ { '$id' : 'FB-0'
            , 'children' :
                [ { '$id' : 'FB-0:0'
                  , 'children' :
                      [ { '$id' : 'FB-0:0:0'
                        , 'allow_new' : True
                        , 'collapsed' : True
                        , 'kind' : 'primary'
                        , 'label' : 'Class'
                        , 'name' : 'left'
                        , 'readonly' : True
                        , 'required' : True
                        , 'type' : 'Field_Entity'
                        , 'type_name' : 'SRM.Boat_Class'
                        , 'value' :
                            { 'init' :
                                { 'cid' : 1
                                , 'pid' : 1
                                }
                            , 'sid' : 'qhCKKsimOo:3Hla747-HuSlL5hzwvBqKojyvIg'
                            }
                        }
                      , { '$id' : 'FB-0:0:1'
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
                        , 'required' : True
                        , 'type' : 'Field'
                        , 'value' :
                            { 'init' : '1107' }
                        }
                      , { '$id' : 'FB-0:0:2'
                        , 'kind' : 'primary'
                        , 'label' : 'Nation'
                        , 'name' : 'nation'
                        , 'type' : 'Field'
                        , 'value' :
                            { 'init' : 'AUT' }
                        }
                      , { '$id' : 'FB-0:0:3'
                        , 'completer' :
                            { 'entity_p' : True
                            , 'names' :
                                [ 'sail_number_x'
                                , 'left'
                                , 'sail_number'
                                , 'nation'
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
                              , 'type_name' : 'SRM.Boat'
                              , 'value' :
                                  { 'init' :
                                      { 'cid' : 2
                                      , 'pid' : 2
                                      }
                                  , 'sid' : '73AhMKVvgduSBcdc9J-WeU1hPS8BJa7jWlFOkw'
                                  }
                              }
                            , { '$id' : 'FB-0:2::0-1'
                              , 'children' :
                                  [ { '$id' : 'FB-0:2::0-1:0'
                                    , 'allow_new' : False
                                    , 'collapsed' : True
                                    , 'kind' : 'primary'
                                    , 'label' : 'Regatta'
                                    , 'name' : 'right'
                                    , 'required' : True
                                    , 'type' : 'Field_Entity'
                                    , 'type_name' : 'SRM.Regatta'
                                    , 'value' :
                                        { 'init' :
                                            { 'cid' : 6
                                            , 'pid' : 6
                                            }
                                        , 'sid' : 's:FQz-HZIl9NAA:-YHx4IFRn3WMzvWHFWK:b5Q'
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
                                          , 'allow_new' : False
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
                                          , 'readonly' : True
                                          , 'required' : True
                                          , 'type' : 'Field_Entity'
                                          , 'type_name' : 'PAP.Person'
                                          , 'value' :
                                              { 'init' :
                                                  { 'cid' : 3
                                                  , 'pid' : 3
                                                  }
                                              , 'sid' : 'Fy2PPgkt0OF-ExUfoga3fcrKvv3qjOABiCN9rQ'
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
                                          , 'collapsed' : False
                                          , 'kind' : 'primary'
                                          , 'label' : 'Club'
                                          , 'name' : 'club'
                                          , 'type' : 'Field_Entity'
                                          , 'type_name' : 'SRM.Club'
                                          , 'value' :
                                              { 'init' :
                                                  {}
                                              , 'sid' : 'vPwcc9Gqe25rUmpJ7cBwLBH9yc6iGCbRVfNrEg'
                                              }
                                          }
                                        ]
                                    , 'collapsed' : True
                                    , 'kind' : 'required'
                                    , 'label' : 'Skipper'
                                    , 'name' : 'skipper'
                                    , 'required' : True
                                    , 'type' : 'Field_Entity'
                                    , 'type_name' : 'SRM.Sailor'
                                    , 'value' :
                                        { 'init' :
                                            { 'cid' : 4
                                            , 'pid' : 4
                                            }
                                        , 'sid' : 'OMXS5mItieYGgFiLVGNgcS:zMWmtL8cV6qw9CA'
                                        }
                                    }
                                  ]
                              , 'collapsed' : False
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
                        , 'type_name' : 'SRM.Boat_in_Regatta'
                        , 'value' :
                            { 'init' :
                                { 'cid' : 7
                                , 'pid' : 7
                                }
                            , 'sid' : 'QSvku2fc3JI02:LH5rBsLqrXDzWvSbNZ-hXkBQ'
                            }
                        }
                      ]
                  , 'name' : 'Boat_in_Regatta'
                  , 'type' : 'Entity_List'
                  , 'type_name' : 'SRM.Boat_in_Regatta'
                  }
                ]
            , 'name' : 'Boat'
            , 'type' : 'Entity'
            , 'type_name' : 'SRM.Boat'
            , 'value' :
                { 'init' :
                    { 'cid' : 2
                    , 'pid' : 2
                    }
                , 'sid' : 'ZE5i0RV4B6i6wEn0wszdszAuXDu121dutn0uEg'
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
                        , 'collapsed' : True
                        , 'kind' : 'primary'
                        , 'label' : 'Class'
                        , 'name' : 'left'
                        , 'readonly' : True
                        , 'required' : True
                        , 'type' : 'Field_Entity'
                        , 'type_name' : 'SRM.Boat_Class'
                        , 'value' :
                            { 'init' :
                                {}
                            , 'sid' : 'qhCKKsimOo:3Hla747-HuSlL5hzwvBqKojyvIg'
                            }
                        }
                      , { '$id' : 'FB-0:0:1'
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
                        , 'required' : True
                        , 'type' : 'Field'
                        , 'value' :
                            { 'edit' : '1107' }
                        }
                      , { '$id' : 'FB-0:0:2'
                        , 'kind' : 'primary'
                        , 'label' : 'Nation'
                        , 'name' : 'nation'
                        , 'type' : 'Field'
                        , 'value' :
                            { 'edit' : 'AUT' }
                        }
                      , { '$id' : 'FB-0:0:3'
                        , 'completer' :
                            { 'entity_p' : True
                            , 'names' :
                                [ 'sail_number_x'
                                , 'left'
                                , 'sail_number'
                                , 'nation'
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
                              , 'type_name' : 'SRM.Boat'
                              , 'value' :
                                  { 'init' :
                                      {}
                                  , 'sid' : '73AhMKVvgduSBcdc9J-WeU1hPS8BJa7jWlFOkw'
                                  }
                              }
                            , { '$id' : 'FB-0:2::0-1'
                              , 'children' :
                                  [ { '$id' : 'FB-0:2::0-1:0'
                                    , 'allow_new' : False
                                    , 'collapsed' : True
                                    , 'kind' : 'primary'
                                    , 'label' : 'Regatta'
                                    , 'name' : 'right'
                                    , 'required' : True
                                    , 'type' : 'Field_Entity'
                                    , 'type_name' : 'SRM.Regatta'
                                    , 'value' :
                                        { 'init' :
                                            {}
                                        , 'sid' : 's:FQz-HZIl9NAA:-YHx4IFRn3WMzvWHFWK:b5Q'
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
                                          , 'readonly' : True
                                          , 'required' : True
                                          , 'type' : 'Field_Entity'
                                          , 'type_name' : 'PAP.Person'
                                          , 'value' :
                                              { 'init' :
                                                  {}
                                              , 'sid' : 'Fy2PPgkt0OF-ExUfoga3fcrKvv3qjOABiCN9rQ'
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
                                          , 'collapsed' : False
                                          , 'kind' : 'primary'
                                          , 'label' : 'Club'
                                          , 'name' : 'club'
                                          , 'type' : 'Field_Entity'
                                          , 'type_name' : 'SRM.Club'
                                          , 'value' :
                                              { 'init' :
                                                  {}
                                              , 'sid' : 'vPwcc9Gqe25rUmpJ7cBwLBH9yc6iGCbRVfNrEg'
                                              }
                                          }
                                        ]
                                    , 'collapsed' : True
                                    , 'kind' : 'required'
                                    , 'label' : 'Skipper'
                                    , 'name' : 'skipper'
                                    , 'required' : True
                                    , 'type' : 'Field_Entity'
                                    , 'type_name' : 'SRM.Sailor'
                                    , 'value' :
                                        { 'init' :
                                            {}
                                        , 'sid' : 'OMXS5mItieYGgFiLVGNgcS:zMWmtL8cV6qw9CA'
                                        }
                                    }
                                  ]
                              , 'collapsed' : False
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
                        , 'type_name' : 'SRM.Boat_in_Regatta'
                        , 'value' :
                            { 'init' :
                                {}
                            , 'sid' : 'QSvku2fc3JI02:LH5rBsLqrXDzWvSbNZ-hXkBQ'
                            }
                        }
                      ]
                  , 'name' : 'Boat_in_Regatta'
                  , 'type' : 'Entity_List'
                  , 'type_name' : 'SRM.Boat_in_Regatta'
                  }
                ]
            , 'name' : 'Boat'
            , 'type' : 'Entity'
            , 'type_name' : 'SRM.Boat'
            , 'value' :
                { 'init' :
                    {}
                , 'sid' : 'h9S98nt46at68AICB3hJbRAfJQ18ERSyjDPLdg'
                }
            }
          ]
      , 'type' : 'Form'
      , 'value' :
          { 'sid' : 0 }
      }

    >>> print "var f =", fi.as_js, ";"
    var f = new $GTW.AFS.Form ({"$id": "FB", "children": [{"$id": "FB-0", "children": [{"$id": "FB-0:0", "children": [{"$id": "FB-0:0:0", "allow_new": true, "collapsed": true, "kind": "primary", "label": "Class", "name": "left", "readonly": true, "required": true, "type": "Field_Entity", "type_name": "SRM.Boat_Class", "value": {"init": {"cid": 1, "pid": 1}, "sid": "qhCKKsimOo:3Hla747-HuSlL5hzwvBqKojyvIg"}}, {"$id": "FB-0:0:1", "completer": {"entity_p": true, "names": ["sail_number", "left", "nation", "sail_number_x"], "treshold": 1}, "kind": "primary", "label": "Sail number", "name": "sail_number", "required": true, "type": "Field", "value": {"init": "1107"}}, {"$id": "FB-0:0:2", "kind": "primary", "label": "Nation", "name": "nation", "type": "Field", "value": {"init": "AUT"}}, {"$id": "FB-0:0:3", "completer": {"entity_p": true, "names": ["sail_number_x", "left", "sail_number", "nation"], "treshold": 1}, "kind": "primary", "label": "Sail number x", "name": "sail_number_x", "type": "Field", "value": {}}], "collapsed": false, "name": "primary", "type": "Fieldset"}, {"$id": "FB-0:1", "children": [{"$id": "FB-0:1:0", "kind": "optional", "label": "Name", "name": "name", "type": "Field", "value": {}}], "collapsed": true, "name": "optional", "type": "Fieldset"}, {"$id": "FB-0:2", "children": [{"$id": "FB-0:2::0", "children": [{"$id": "FB-0:2::0-0", "allow_new": false, "collapsed": true, "hidden": true, "kind": "primary", "label": "Boat", "name": "left", "required": true, "type": "Field_Role_Hidden", "type_name": "SRM.Boat", "value": {"init": {"cid": 2, "pid": 2}, "sid": "73AhMKVvgduSBcdc9J-WeU1hPS8BJa7jWlFOkw"}}, {"$id": "FB-0:2::0-1", "children": [{"$id": "FB-0:2::0-1:0", "allow_new": false, "collapsed": true, "kind": "primary", "label": "Regatta", "name": "right", "required": true, "type": "Field_Entity", "type_name": "SRM.Regatta", "value": {"init": {"cid": 6, "pid": 6}, "sid": "s:FQz-HZIl9NAA:-YHx4IFRn3WMzvWHFWK:b5Q"}}], "collapsed": false, "name": "primary", "type": "Fieldset"}, {"$id": "FB-0:2::0-2", "children": [{"$id": "FB-0:2::0-2:0", "allow_new": true, "children": [{"$id": "FB-0:2::0-2:0:0", "allow_new": false, "collapsed": true, "completer": {"entity_p": true, "names": ["left", "nation", "mna_number", "club"], "treshold": 1}, "kind": "primary", "label": "Person", "name": "left", "readonly": true, "required": true, "type": "Field_Entity", "type_name": "PAP.Person", "value": {"init": {"cid": 3, "pid": 3}, "sid": "Fy2PPgkt0OF-ExUfoga3fcrKvv3qjOABiCN9rQ"}}, {"$id": "FB-0:2::0-2:0:1", "kind": "primary", "label": "Nation", "name": "nation", "type": "Field", "value": {"init": "AUT"}}, {"$id": "FB-0:2::0-2:0:2", "completer": {"entity_p": true, "names": ["mna_number", "left", "nation", "club"], "treshold": 1}, "kind": "primary", "label": "Mna number", "name": "mna_number", "type": "Field", "value": {"init": "29676"}}, {"$id": "FB-0:2::0-2:0:3", "allow_new": true, "children": [{"$id": "FB-0:2::0-2:0:3:0", "completer": {"entity_p": true, "names": ["name"], "treshold": 1}, "kind": "primary", "label": "Name", "name": "name", "required": true, "type": "Field", "value": {}}], "collapsed": false, "kind": "primary", "label": "Club", "name": "club", "type": "Field_Entity", "type_name": "SRM.Club", "value": {"init": {}, "sid": "vPwcc9Gqe25rUmpJ7cBwLBH9yc6iGCbRVfNrEg"}}], "collapsed": true, "kind": "required", "label": "Skipper", "name": "skipper", "required": true, "type": "Field_Entity", "type_name": "SRM.Sailor", "value": {"init": {"cid": 4, "pid": 4}, "sid": "OMXS5mItieYGgFiLVGNgcS:zMWmtL8cV6qw9CA"}}], "collapsed": false, "name": "required", "type": "Fieldset"}, {"$id": "FB-0:2::0-3", "children": [{"$id": "FB-0:2::0-3:0", "kind": "optional", "label": "Place", "name": "place", "type": "Field", "value": {}}, {"$id": "FB-0:2::0-3:1", "kind": "optional", "label": "Points", "name": "points", "type": "Field", "value": {}}], "collapsed": true, "name": "optional", "type": "Fieldset"}], "collapsed": true, "name": "Boat_in_Regatta", "role_name": "left", "type": "Entity_Link", "type_name": "SRM.Boat_in_Regatta", "value": {"init": {"cid": 7, "pid": 7}, "sid": "QSvku2fc3JI02:LH5rBsLqrXDzWvSbNZ-hXkBQ"}}], "name": "Boat_in_Regatta", "type": "Entity_List", "type_name": "SRM.Boat_in_Regatta"}], "name": "Boat", "type": "Entity", "type_name": "SRM.Boat", "value": {"init": {"cid": 2, "pid": 2}, "sid": "ZE5i0RV4B6i6wEn0wszdszAuXDu121dutn0uEg"}}], "type": "Form", "value": {"sid": 0}}) ;
    >>> print "var g =", fic.as_js, ";"
    var g = new $GTW.AFS.Form ({"$id": "FB", "children": [{"$id": "FB-0", "children": [{"$id": "FB-0:0", "children": [{"$id": "FB-0:0:0", "allow_new": true, "collapsed": true, "kind": "primary", "label": "Class", "name": "left", "readonly": true, "required": true, "type": "Field_Entity", "type_name": "SRM.Boat_Class", "value": {"init": {}, "sid": "qhCKKsimOo:3Hla747-HuSlL5hzwvBqKojyvIg"}}, {"$id": "FB-0:0:1", "completer": {"entity_p": true, "names": ["sail_number", "left", "nation", "sail_number_x"], "treshold": 1}, "kind": "primary", "label": "Sail number", "name": "sail_number", "required": true, "type": "Field", "value": {"edit": "1107"}}, {"$id": "FB-0:0:2", "kind": "primary", "label": "Nation", "name": "nation", "type": "Field", "value": {"edit": "AUT"}}, {"$id": "FB-0:0:3", "completer": {"entity_p": true, "names": ["sail_number_x", "left", "sail_number", "nation"], "treshold": 1}, "kind": "primary", "label": "Sail number x", "name": "sail_number_x", "type": "Field", "value": {}}], "collapsed": false, "name": "primary", "type": "Fieldset"}, {"$id": "FB-0:1", "children": [{"$id": "FB-0:1:0", "kind": "optional", "label": "Name", "name": "name", "type": "Field", "value": {}}], "collapsed": true, "name": "optional", "type": "Fieldset"}, {"$id": "FB-0:2", "children": [{"$id": "FB-0:2::0", "children": [{"$id": "FB-0:2::0-0", "allow_new": false, "collapsed": true, "hidden": true, "kind": "primary", "label": "Boat", "name": "left", "required": true, "type": "Field_Role_Hidden", "type_name": "SRM.Boat", "value": {"init": {}, "sid": "73AhMKVvgduSBcdc9J-WeU1hPS8BJa7jWlFOkw"}}, {"$id": "FB-0:2::0-1", "children": [{"$id": "FB-0:2::0-1:0", "allow_new": false, "collapsed": true, "kind": "primary", "label": "Regatta", "name": "right", "required": true, "type": "Field_Entity", "type_name": "SRM.Regatta", "value": {"init": {}, "sid": "s:FQz-HZIl9NAA:-YHx4IFRn3WMzvWHFWK:b5Q"}}], "collapsed": false, "name": "primary", "type": "Fieldset"}, {"$id": "FB-0:2::0-2", "children": [{"$id": "FB-0:2::0-2:0", "allow_new": true, "children": [{"$id": "FB-0:2::0-2:0:0", "allow_new": true, "collapsed": true, "completer": {"entity_p": true, "names": ["left", "nation", "mna_number", "club"], "treshold": 1}, "kind": "primary", "label": "Person", "name": "left", "readonly": true, "required": true, "type": "Field_Entity", "type_name": "PAP.Person", "value": {"init": {}, "sid": "Fy2PPgkt0OF-ExUfoga3fcrKvv3qjOABiCN9rQ"}}, {"$id": "FB-0:2::0-2:0:1", "kind": "primary", "label": "Nation", "name": "nation", "type": "Field", "value": {"edit": "AUT"}}, {"$id": "FB-0:2::0-2:0:2", "completer": {"entity_p": true, "names": ["mna_number", "left", "nation", "club"], "treshold": 1}, "kind": "primary", "label": "Mna number", "name": "mna_number", "type": "Field", "value": {"edit": "29676"}}, {"$id": "FB-0:2::0-2:0:3", "allow_new": true, "children": [{"$id": "FB-0:2::0-2:0:3:0", "completer": {"entity_p": true, "names": ["name"], "treshold": 1}, "kind": "primary", "label": "Name", "name": "name", "required": true, "type": "Field", "value": {}}], "collapsed": false, "kind": "primary", "label": "Club", "name": "club", "type": "Field_Entity", "type_name": "SRM.Club", "value": {"init": {}, "sid": "vPwcc9Gqe25rUmpJ7cBwLBH9yc6iGCbRVfNrEg"}}], "collapsed": true, "kind": "required", "label": "Skipper", "name": "skipper", "required": true, "type": "Field_Entity", "type_name": "SRM.Sailor", "value": {"init": {}, "sid": "OMXS5mItieYGgFiLVGNgcS:zMWmtL8cV6qw9CA"}}], "collapsed": false, "name": "required", "type": "Fieldset"}, {"$id": "FB-0:2::0-3", "children": [{"$id": "FB-0:2::0-3:0", "kind": "optional", "label": "Place", "name": "place", "type": "Field", "value": {}}, {"$id": "FB-0:2::0-3:1", "kind": "optional", "label": "Points", "name": "points", "type": "Field", "value": {}}], "collapsed": true, "name": "optional", "type": "Fieldset"}], "collapsed": true, "name": "Boat_in_Regatta", "role_name": "left", "type": "Entity_Link", "type_name": "SRM.Boat_in_Regatta", "value": {"init": {}, "sid": "QSvku2fc3JI02:LH5rBsLqrXDzWvSbNZ-hXkBQ"}}], "name": "Boat_in_Regatta", "type": "Entity_List", "type_name": "SRM.Boat_in_Regatta"}], "name": "Boat", "type": "Entity", "type_name": "SRM.Boat", "value": {"init": {}, "sid": "h9S98nt46at68AICB3hJbRAfJQ18ERSyjDPLdg"}}], "type": "Form", "value": {"sid": 0}}) ;

    >>> for i in fi.transitive_iter () :
    ...     print i.elem, sorted (i.value or ())
    <Form FB> ['sid']
    <Entity FB-0 'Boat' 'SRM.Boat'> [u'init', 'sid']
    <Fieldset FB-0:0 'primary'> []
    <Field_Entity FB-0:0:0 'left' 'SRM.Boat_Class'> [u'init', 'sid']
    <Field FB-0:0:1 'sail_number'> [u'init']
    <Field FB-0:0:2 'nation'> [u'init']
    <Field FB-0:0:3 'sail_number_x'> []
    <Fieldset FB-0:1 'optional'> []
    <Field FB-0:1:0 'name'> []
    <Entity_List FB-0:2 'Boat_in_Regatta' <Entity_Link FB-0:2::p 'Boat_in_Regatta' 'SRM.Boat_in_Regatta'>> []
    <Entity_Link FB-0:2::0 'Boat_in_Regatta' 'SRM.Boat_in_Regatta'> [u'init', 'sid']
    <Field_Role_Hidden FB-0:2::0-0 'left' 'SRM.Boat'> [u'init', 'sid']
    <Fieldset FB-0:2::0-1 'primary'> []
    <Field_Entity FB-0:2::0-1:0 'right' 'SRM.Regatta'> [u'init', 'sid']
    <Fieldset FB-0:2::0-2 'required'> []
    <Field_Entity FB-0:2::0-2:0 'skipper' 'SRM.Sailor'> [u'init', 'sid']
    <Field_Entity FB-0:2::0-2:0:0 'left' 'PAP.Person'> [u'init', 'sid']
    <Field FB-0:2::0-2:0:1 'nation'> [u'init']
    <Field FB-0:2::0-2:0:2 'mna_number'> [u'init']
    <Field_Entity FB-0:2::0-2:0:3 'club' 'SRM.Club'> [u'init', 'sid']
    <Field FB-0:2::0-2:0:3:0 'name'> []
    <Fieldset FB-0:2::0-3 'optional'> []
    <Field FB-0:2::0-3:0 'place'> []
    <Field FB-0:2::0-3:1 'points'> []

    >>> for i in fi.entities () :
    ...     print i.elem
    <Entity FB-0 'Boat' 'SRM.Boat'>

    >>> f_sig_map = {}
    >>> for i in fi.entity_children () :
    ...     f_sig_map [i.id] = i, i.sig
    ...     print i.elem, ", pid =", i.init.get ("pid"), ", sid =", i.sid
    <Entity FB-0 'Boat' 'SRM.Boat'> , pid = 2 , sid = ZE5i0RV4B6i6wEn0wszdszAuXDu121dutn0uEg
    <Field_Entity FB-0:0:0 'left' 'SRM.Boat_Class'> , pid = 1 , sid = qhCKKsimOo:3Hla747-HuSlL5hzwvBqKojyvIg
    <Entity_Link FB-0:2::0 'Boat_in_Regatta' 'SRM.Boat_in_Regatta'> , pid = 7 , sid = QSvku2fc3JI02:LH5rBsLqrXDzWvSbNZ-hXkBQ
    <Field_Role_Hidden FB-0:2::0-0 'left' 'SRM.Boat'> , pid = 2 , sid = 73AhMKVvgduSBcdc9J-WeU1hPS8BJa7jWlFOkw
    <Field_Entity FB-0:2::0-1:0 'right' 'SRM.Regatta'> , pid = 6 , sid = s:FQz-HZIl9NAA:-YHx4IFRn3WMzvWHFWK:b5Q
    <Field_Entity FB-0:2::0-2:0 'skipper' 'SRM.Sailor'> , pid = 4 , sid = OMXS5mItieYGgFiLVGNgcS:zMWmtL8cV6qw9CA
    <Field_Entity FB-0:2::0-2:0:0 'left' 'PAP.Person'> , pid = 3 , sid = Fy2PPgkt0OF-ExUfoga3fcrKvv3qjOABiCN9rQ
    <Field_Entity FB-0:2::0-2:0:3 'club' 'SRM.Club'> , pid = None , sid = vPwcc9Gqe25rUmpJ7cBwLBH9yc6iGCbRVfNrEg

    >>> for i in fi.entity_children () :
    ...     print "%-72s %r" % (i.elem, i.ui_display)
    <Entity FB-0 'Boat' 'SRM.Boat'>                                  u'Optimist, AUT 1107'
    <Field_Entity FB-0:0:0 'left' 'SRM.Boat_Class'>                  u'Optimist'
    <Entity_Link FB-0:2::0 'Boat_in_Regatta' 'SRM.Boat_in_Regatta'>  u'Optimist, AUT 1107, Himmelfahrt 2008/05/01, Optimist'
    <Field_Role_Hidden FB-0:2::0-0 'left' 'SRM.Boat'>                u'Optimist, AUT 1107'
    <Field_Entity FB-0:2::0-1:0 'right' 'SRM.Regatta'>               u'Himmelfahrt 2008/05/01, Optimist'
    <Field_Entity FB-0:2::0-2:0 'skipper' 'SRM.Sailor'>              u'Tanzer Laurens, AUT, 29676'
    <Field_Entity FB-0:2::0-2:0:0 'left' 'PAP.Person'>               u'Tanzer Laurens'
    <Field_Entity FB-0:2::0-2:0:3 'club' 'SRM.Club'>                 u''

    >>> for i in fi.entity_children () :
    ...     print show_instance (i)
    <Entity FB-0 'Boat' 'SRM.Boat'>                                  e = 2 o = - r = -
    <Field_Entity FB-0:0:0 'left' 'SRM.Boat_Class'>                  e = 1 o = 2 r = -
    <Entity_Link FB-0:2::0 'Boat_in_Regatta' 'SRM.Boat_in_Regatta'>  e = 7 o = - r = 2
    <Field_Role_Hidden FB-0:2::0-0 'left' 'SRM.Boat'>                e = 2 o = 7 r = -
    <Field_Entity FB-0:2::0-1:0 'right' 'SRM.Regatta'>               e = 6 o = 7 r = -
    <Field_Entity FB-0:2::0-2:0 'skipper' 'SRM.Sailor'>              e = 4 o = 7 r = -
    <Field_Entity FB-0:2::0-2:0:0 'left' 'PAP.Person'>               e = 3 o = 4 r = -
    <Field_Entity FB-0:2::0-2:0:3 'club' 'SRM.Club'>                 e = - o = 4 r = -

    >>> for i in fi.entity_children () :
    ...     print "%-72s %s" % (i.elem, getattr (i, "allow_new", ""))
    <Entity FB-0 'Boat' 'SRM.Boat'>
    <Field_Entity FB-0:0:0 'left' 'SRM.Boat_Class'>                  True
    <Entity_Link FB-0:2::0 'Boat_in_Regatta' 'SRM.Boat_in_Regatta'>
    <Field_Role_Hidden FB-0:2::0-0 'left' 'SRM.Boat'>                False
    <Field_Entity FB-0:2::0-1:0 'right' 'SRM.Regatta'>               False
    <Field_Entity FB-0:2::0-2:0 'skipper' 'SRM.Sailor'>              True
    <Field_Entity FB-0:2::0-2:0:0 'left' 'PAP.Person'>               False
    <Field_Entity FB-0:2::0-2:0:3 'club' 'SRM.Club'>                 True

    >>> g_sig_map = {}
    >>> for i in fic.entity_children () :
    ...     g_sig_map [i.id] = i, i.sig
    ...     print i.elem, ", pid =", i.init.get ("pid"), ", sid =", i.sid
    <Entity FB-0 'Boat' 'SRM.Boat'> , pid = None , sid = h9S98nt46at68AICB3hJbRAfJQ18ERSyjDPLdg
    <Field_Entity FB-0:0:0 'left' 'SRM.Boat_Class'> , pid = None , sid = qhCKKsimOo:3Hla747-HuSlL5hzwvBqKojyvIg
    <Entity_Link FB-0:2::0 'Boat_in_Regatta' 'SRM.Boat_in_Regatta'> , pid = None , sid = QSvku2fc3JI02:LH5rBsLqrXDzWvSbNZ-hXkBQ
    <Field_Role_Hidden FB-0:2::0-0 'left' 'SRM.Boat'> , pid = None , sid = 73AhMKVvgduSBcdc9J-WeU1hPS8BJa7jWlFOkw
    <Field_Entity FB-0:2::0-1:0 'right' 'SRM.Regatta'> , pid = None , sid = s:FQz-HZIl9NAA:-YHx4IFRn3WMzvWHFWK:b5Q
    <Field_Entity FB-0:2::0-2:0 'skipper' 'SRM.Sailor'> , pid = None , sid = OMXS5mItieYGgFiLVGNgcS:zMWmtL8cV6qw9CA
    <Field_Entity FB-0:2::0-2:0:0 'left' 'PAP.Person'> , pid = None , sid = Fy2PPgkt0OF-ExUfoga3fcrKvv3qjOABiCN9rQ
    <Field_Entity FB-0:2::0-2:0:3 'club' 'SRM.Club'> , pid = None , sid = vPwcc9Gqe25rUmpJ7cBwLBH9yc6iGCbRVfNrEg

    >>> Value.from_json (json_bad)
    Traceback (most recent call last):
      ...
    Unknown: Form/element is unknown (unknown id: FC)

    >>> fv = Value.from_json (json_value)
    >>> fv.changes_t
    0
    >>> for i in fv.transitive_iter () :
    ...     print i
    <Form FB>, init-v = '', sid = 0, changes = 0
    <Entity FB-0 'Boat' 'SRM.Boat'>, init-v = [(u'cid', 2), (u'pid', 2)], sid = ZE5i0RV4B6i6wEn0wszdszAuXDu121dutn0uEg, changes = 0
    <Field_Entity FB-0:0:0 'left' 'SRM.Boat_Class'>, init-v = [(u'cid', 1), (u'pid', 1)], sid = qhCKKsimOo:3Hla747-HuSlL5hzwvBqKojyvIg, changes = 0
    <Field FB-0:0:1 'sail_number'>, init-v = '1107', changes = 0
    <Field FB-0:0:2 'nation'>, init-v = 'AUT', changes = 0
    <Field FB-0:0:3 'sail_number_x'>, init-v = '', changes = 0
    <Field FB-0:1:0 'name'>, init-v = '', changes = 0
    <Entity_Link FB-0:2::p 'Boat_in_Regatta' 'SRM.Boat_in_Regatta'>, init-v = [(u'cid', 7), (u'pid', 7)], sid = QSvku2fc3JI02:LH5rBsLqrXDzWvSbNZ-hXkBQ, changes = 0
    <Field_Role_Hidden FB-0:2::p-0 'left' 'SRM.Boat'>, init-v = [(u'cid', 2), (u'pid', 2)], sid = 73AhMKVvgduSBcdc9J-WeU1hPS8BJa7jWlFOkw, changes = 0, role_id = FB-0
    <Field_Entity FB-0:2::p-1:0 'right' 'SRM.Regatta'>, init-v = [(u'cid', 6), (u'pid', 6)], sid = s:FQz-HZIl9NAA:-YHx4IFRn3WMzvWHFWK:b5Q, changes = 0
    <Field_Entity FB-0:2::p-2:0 'skipper' 'SRM.Sailor'>, init-v = [(u'cid', 4), (u'pid', 4)], sid = OMXS5mItieYGgFiLVGNgcS:zMWmtL8cV6qw9CA, changes = 0
    <Field_Entity FB-0:2::p-2:0:0 'left' 'PAP.Person'>, init-v = [(u'cid', 3), (u'pid', 3)], sid = Fy2PPgkt0OF-ExUfoga3fcrKvv3qjOABiCN9rQ, changes = 0
    <Field FB-0:2::p-2:0:1 'nation'>, init-v = 'AUT', changes = 0
    <Field FB-0:2::p-2:0:2 'mna_number'>, init-v = '29676', changes = 0
    <Field_Entity FB-0:2::p-2:0:3 'club' 'SRM.Club'>, init-v = [], sid = vPwcc9Gqe25rUmpJ7cBwLBH9yc6iGCbRVfNrEg, changes = 0
    <Field FB-0:2::p-2:0:3:0 'name'>, init-v = '', changes = 0
    <Field FB-0:2::p-3:0 'place'>, init-v = '', changes = 0
    <Field FB-0:2::p-3:1 'points'>, init-v = '', changes = 0

    >>> for v in fv.entities () :
    ...     print v.elem, v.changes_t
    <Entity FB-0 'Boat' 'SRM.Boat'> 0
    <Entity_Link FB-0:2::p 'Boat_in_Regatta' 'SRM.Boat_in_Regatta'> 0

    >>> for e in fi.transitive_iter () :
    ...   if hasattr (e, "allow_new") :
    ...     print "%-20s %-20s %-20s %s" % (e.id, e.type_base_name, e.elem.__class__.__name__, e.allow_new)
    FB-0:0:0             Boat_Class           Field_Entity         True
    FB-0:2::0-0          Boat                 Field_Role_Hidden    False
    FB-0:2::0-1:0        Regatta              Field_Entity         False
    FB-0:2::0-2:0        Sailor               Field_Entity         True
    FB-0:2::0-2:0:0      Person               Field_Entity         False
    FB-0:2::0-2:0:3      Club                 Field_Entity         True

    >>> for e in fv.transitive_iter () :
    ...   if hasattr (e, "allow_new") :
    ...     print "%-20s %-20s %-20s %s" % (e.id, e.type_base_name, e.elem.__class__.__name__, e.allow_new)
    FB-0:0:0             Boat_Class           Field_Entity         True
    FB-0:2::0-0          Boat                 Field_Role_Hidden    False
    FB-0:2::0-1:0        Regatta              Field_Entity         False
    FB-0:2::0-2:0        Sailor               Field_Entity         True
    FB-0:2::0-2:0:0      Person               Field_Entity         False
    FB-0:2::0-2:0:3      Club                 Field_Entity         True

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
    <Entity FB-0 'Boat' 'SRM.Boat'> True True
      > ZE5i0RV4B6i6wEn0wszdszAuXDu121dutn0uEg
      < ZE5i0RV4B6i6wEn0wszdszAuXDu121dutn0uEg
      > (((u'pid', 2), (u'cid', 2), 'FB-0', 'SRM.Boat'), ('FB-0:0:0', 'left'), ('FB-0:0:1', 'sail_number'), ('FB-0:0:2', 'nation'), ('FB-0:0:3', 'sail_number_x'), ('FB-0:1:0', 'name'), 0)
      < (((u'pid', 2), (u'cid', 2), 'FB-0', 'SRM.Boat'), ('FB-0:0:0', 'left'), ('FB-0:0:1', 'sail_number'), ('FB-0:0:2', 'nation'), ('FB-0:0:3', 'sail_number_x'), ('FB-0:1:0', 'name'), 0)
    <Field_Entity FB-0:0:0 'left' 'SRM.Boat_Class'> True True
      > qhCKKsimOo:3Hla747-HuSlL5hzwvBqKojyvIg
      < qhCKKsimOo:3Hla747-HuSlL5hzwvBqKojyvIg
      > (('FB-0:0:0', 'SRM.Boat_Class'), 0)
      < (('FB-0:0:0', 'SRM.Boat_Class'), 0)
    <Entity_Link FB-0:2::0 'Boat_in_Regatta' 'SRM.Boat_in_Regatta'> True True
      > QSvku2fc3JI02:LH5rBsLqrXDzWvSbNZ-hXkBQ
      < QSvku2fc3JI02:LH5rBsLqrXDzWvSbNZ-hXkBQ
      > (('FB-0:2::0', 'SRM.Boat_in_Regatta'), ('FB-0:2::0-0', 'left'), ('FB-0:2::0-1:0', 'right'), ('FB-0:2::0-2:0', 'skipper'), ('FB-0:2::0-3:0', 'place'), ('FB-0:2::0-3:1', 'points'), 0)
      < (('FB-0:2::0', 'SRM.Boat_in_Regatta'), ('FB-0:2::0-0', 'left'), ('FB-0:2::0-1:0', 'right'), ('FB-0:2::0-2:0', 'skipper'), ('FB-0:2::0-3:0', 'place'), ('FB-0:2::0-3:1', 'points'), 0)
    <Field_Role_Hidden FB-0:2::0-0 'left' 'SRM.Boat'> True True
      > 73AhMKVvgduSBcdc9J-WeU1hPS8BJa7jWlFOkw
      < 73AhMKVvgduSBcdc9J-WeU1hPS8BJa7jWlFOkw
      > (('FB-0:2::0-0', 'SRM.Boat'), 0)
      < (('FB-0:2::0-0', 'SRM.Boat'), 0)
    <Field_Entity FB-0:2::0-1:0 'right' 'SRM.Regatta'> True True
      > s:FQz-HZIl9NAA:-YHx4IFRn3WMzvWHFWK:b5Q
      < s:FQz-HZIl9NAA:-YHx4IFRn3WMzvWHFWK:b5Q
      > (('FB-0:2::0-1:0', 'SRM.Regatta'), 0)
      < (('FB-0:2::0-1:0', 'SRM.Regatta'), 0)
    <Field_Entity FB-0:2::0-2:0 'skipper' 'SRM.Sailor'> True True
      > OMXS5mItieYGgFiLVGNgcS:zMWmtL8cV6qw9CA
      < OMXS5mItieYGgFiLVGNgcS:zMWmtL8cV6qw9CA
      > (('FB-0:2::0-2:0', 'SRM.Sailor'), ('FB-0:2::0-2:0:0', 'left'), ('FB-0:2::0-2:0:1', 'nation'), ('FB-0:2::0-2:0:2', 'mna_number'), ('FB-0:2::0-2:0:3', 'club'), 0)
      < (('FB-0:2::0-2:0', 'SRM.Sailor'), ('FB-0:2::0-2:0:0', 'left'), ('FB-0:2::0-2:0:1', 'nation'), ('FB-0:2::0-2:0:2', 'mna_number'), ('FB-0:2::0-2:0:3', 'club'), 0)
    <Field_Entity FB-0:2::0-2:0:0 'left' 'PAP.Person'> True True
      > Fy2PPgkt0OF-ExUfoga3fcrKvv3qjOABiCN9rQ
      < Fy2PPgkt0OF-ExUfoga3fcrKvv3qjOABiCN9rQ
      > (('FB-0:2::0-2:0:0', 'PAP.Person'), 0)
      < (('FB-0:2::0-2:0:0', 'PAP.Person'), 0)
    <Field_Entity FB-0:2::0-2:0:3 'club' 'SRM.Club'> True True
      > vPwcc9Gqe25rUmpJ7cBwLBH9yc6iGCbRVfNrEg
      < vPwcc9Gqe25rUmpJ7cBwLBH9yc6iGCbRVfNrEg
      > (('FB-0:2::0-2:0:3', 'SRM.Club'), ('FB-0:2::0-2:0:3:0', 'name'), 0)
      < (('FB-0:2::0-2:0:3', 'SRM.Club'), ('FB-0:2::0-2:0:3:0', 'name'), 0)

    >>> v.edit.get ("pid")

    >>> for e in fv.transitive_iter () :
    ...   if e.names and e.anchor_id :
    ...     print "%-20s %-20s %-20s %-20s %s" % (e.id, e.anchor_id, e.type_base_name, e.elem.__class__.__name__, e.names)
    FB-0:0:0             FB-0                 Boat_Class           Field_Entity         ['left']
    FB-0:2::0            FB-0                 Boat_in_Regatta      Entity_Link          ['Boat_in_Regatta']
    FB-0:2::0-0          FB-0                 Boat                 Field_Role_Hidden    ['Boat_in_Regatta', u'left']
    FB-0:2::0-1:0        FB-0:2::0            Regatta              Field_Entity         ['Boat_in_Regatta', 'right']
    FB-0:2::0-2:0        FB-0:2::0            Sailor               Field_Entity         ['Boat_in_Regatta', 'skipper']
    FB-0:2::0-2:0:0      FB-0:2::0-2:0        Person               Field_Entity         ['Boat_in_Regatta', 'skipper', 'left']
    FB-0:2::0-2:0:3      FB-0:2::0-2:0        Club                 Field_Entity         ['Boat_in_Regatta', 'skipper', 'club']

    >>> for e in sorted (fv.entity_children (), key = fv.apply_key) :
    ...     print "%4d %-20s %-20s %-20s %s" % (e.rank, e.id, e.anchor_id or "", e.elem.type_base_name, e.elem.__class__.__name__)
       0 FB-0:2::0-2:0:3      FB-0:2::0-2:0        Club                 Field_Entity
       0 FB-0:2::0-2:0:0      FB-0:2::0-2:0        Person               Field_Entity
       0 FB-0:2::0-2:0        FB-0:2::0            Sailor               Field_Entity
       0 FB-0:2::0-1:0        FB-0:2::0            Regatta              Field_Entity
       0 FB-0:0:0             FB-0                 Boat_Class           Field_Entity
       0 FB-0                                      Boat                 Entity
      99 FB-0:2::0-0          FB-0                 Boat                 Field_Role_Hidden
     100 FB-0:2::0            FB-0                 Boat_in_Regatta      Entity_Link

    >>> for e in sorted (fv.entity_children (), key = fv.apply_key) :
    ...  if e.role_id :
    ...    print "%-20s %-20s %-20s %-20s %s" % (e.id, e.anchor_id or "", e.role_id, e.elem.type_base_name, e.elem.__class__.__name__)
    FB-0:2::0-0          FB-0                 FB-0                 Boat                 Field_Role_Hidden

    >>> for v in fv.entity_children () :
    ...     print "%-72s %s" % (v.elem, getattr (v, "allow_new", ""))
    <Entity FB-0 'Boat' 'SRM.Boat'>
    <Field_Entity FB-0:0:0 'left' 'SRM.Boat_Class'>                  True
    <Entity_Link FB-0:2::p 'Boat_in_Regatta' 'SRM.Boat_in_Regatta'>
    <Field_Role_Hidden FB-0:2::p-0 'left' 'SRM.Boat'>                False
    <Field_Entity FB-0:2::p-1:0 'right' 'SRM.Regatta'>               False
    <Field_Entity FB-0:2::p-2:0 'skipper' 'SRM.Sailor'>              True
    <Field_Entity FB-0:2::p-2:0:0 'left' 'PAP.Person'>               False
    <Field_Entity FB-0:2::p-2:0:3 'club' 'SRM.Club'>                 True

    >>> p ### before `fv.apply`
    PAP.Person (u'tanzer', u'laurens', u'', u'')
    >>> fv.apply (scope, _sid = 0)

    >>> fv.apply (scope, _sid = 1)
    Traceback (most recent call last):
      ...
    Corrupted: The edit session has expired or the form values are corrupted.

"""

_person_test = """
    >>> NL = chr (10)

    >>> scope = Scaffold.scope ("hps://") # doctest:+ELLIPSIS
    Creating new scope MOMT__...
    >>> from _GTW._AFS._MOM import Spec
    >>> SL = Spec.Entity (include_links = ("addresses", "emails", "phones"))
    >>> xl = SL (scope.PAP.Person.E_Type)

    >>> PAP = scope.PAP
    >>> SRM = scope.SRM
    >>> bc  = SRM.Boat_Class ("Optimist", max_crew = 1)
    >>> b   = SRM.Boat.instance_or_new (u"Optimist", u"1107", u"AUT", raw = True)
    >>> p   = PAP.Person.instance_or_new (u"Tanzer", u"Laurens")
    >>> s   = SRM.Sailor.instance_or_new (p, nation = u"AUT", mna_number = u"29676", raw = True)
    >>> rev = SRM.Regatta_Event (u"Himmelfahrt", dict (start = u"20080501", raw = True), raw = True)
    >>> reo = SRM.Regatta_C (rev, boat_class = bc)
    >>> bir = SRM.Boat_in_Regatta (b, reo, skipper = s)

    >>> em  = PAP.Email ("laurens.tanzer@gmail.com")
    >>> phe = PAP.Person_has_Email (p, em)
    >>> scope.commit ()

    >>> fp  = Form ("FP", children = [xl])
    >>> fip = fp (PAP.Person, p)

    >>> for i in fip.transitive_iter () :
    ...     print i.elem, formatted_1 ((i.value or {}))
    <Form FP> {'sid' : 0}
    <Entity FP-0 'Person' 'PAP.Person'> {'init' : {'cid' : 3, 'pid' : 3}, 'sid' : 'wNiC50py6OkmZ5hytWmsg24JTOK-MQQIWGTnTA'}
    <Fieldset FP-0:0 'primary'> {}
    <Field FP-0:0:0 'last_name'> {'init' : 'Tanzer'}
    <Field FP-0:0:1 'first_name'> {'init' : 'Laurens'}
    <Field FP-0:0:2 'middle_name'> {}
    <Field FP-0:0:3 'title'> {}
    <Fieldset FP-0:1 'necessary'> {}
    <Field FP-0:1:0 'sex'> {}
    <Fieldset FP-0:2 'optional'> {}
    <Field_Composite FP-0:2:0 'lifetime' 'MOM.Date_Interval'> {}
    <Field FP-0:2:0.0 'start'> {}
    <Field FP-0:2:0.1 'finish'> {}
    <Field FP-0:2:1 'salutation'> {}
    <Entity_List FP-0:3 'Person_has_Address' <Entity_Link FP-0:3::p 'Person_has_Address' 'PAP.Person_has_Address'>> {}
    <Entity_List FP-0:4 'Person_has_Email' <Entity_Link FP-0:4::p 'Person_has_Email' 'PAP.Person_has_Email'>> {}
    <Entity_Link FP-0:4::0 'Person_has_Email' 'PAP.Person_has_Email'> {'init' : {'cid' : 9, 'pid' : 9}, 'sid' : 'xTiSJZqsC15bC8kav1a6jfjUWvO1Bm-v6EWVkQ'}
    <Field_Role_Hidden FP-0:4::0-0 'left' 'PAP.Person'> {'init' : {'cid' : 3, 'pid' : 3}, 'sid' : 'YmOxRDiewyNXO8T-Bynom0QEzpyiE2eTyOjCpA'}
    <Fieldset FP-0:4::0-1 'primary'> {}
    <Field_Entity FP-0:4::0-1:0 'right' 'PAP.Email'> {'init' : {'cid' : 8, 'pid' : 8}, 'sid' : 'cjVwPHGkwTTAQBIEPJ5VbshxioAQV-hIYv0Ycg'}
    <Field FP-0:4::0-1:0:0 'address'> {'init' : 'laurens.tanzer@gmail.com'}
    <Fieldset FP-0:4::0-2 'optional'> {}
    <Field FP-0:4::0-2:0 'desc'> {}
    <Entity_List FP-0:5 'Person_has_Phone' <Entity_Link FP-0:5::p 'Person_has_Phone' 'PAP.Person_has_Phone'>> {}

    >>> for i in fip.transitive_iter () :
    ...     e = i.elem
    ...     print e.__class__.__name__, e._name, getattr (e, "ui_name", ""), repr ((getattr (e, "description", "")or "").replace (NL, " ")), e.renderer
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
    Field_Composite lifetime Lifetime u'Date of birth [`start`] (and death [`finish`])' afs_fc_horizo
    Field start Start u'Start date of interval' None
    Field finish Finish u'Finish date of interval' None
    Field salutation Salutation u'Salutation to be used when communicating with person (e.g., in a letter or email).' None
    Entity_List Person_has_Address Person_has_Address u'Link a person to a address' afs_div_seq
    Entity_List Person_has_Email Person_has_Email u'Link a person to a email' afs_div_seq
    Entity_Link Person_has_Email Person_has_Email u'Link a person to a email' afs_div_seq
    Field_Role_Hidden left Person u'Person linked to Email' afs_div_seq
    Fieldset primary  u'' afs_div_seq
    Field_Entity right Email u'Email of person' afs_div_seq
    Field address Email address u'Email address (including domain)' None
    Fieldset optional  u'' afs_div_seq
    Field desc Description u'Short description of the link' None
    Entity_List Person_has_Phone Person_has_Phone u'Link a person to a phone number' afs_div_seq

"""

_prefilled_test = """
    >>> scope = Scaffold.scope ("hps://") # doctest:+ELLIPSIS
    Creating new scope MOMT__...

    >>> from _GTW._AFS._MOM import Spec
    >>> SB = Spec.Entity (
    ...       attr_spec  = dict
    ...           ( place       = dict (show_in_ui = False)
    ...           , points      = dict (show_in_ui = False)
    ...           )
    ...     , include_links = ("_crew", )
    ...     )
    >>> fb = Form ("FBR", children = [SB (scope.SRM.Boat_in_Regatta)])

    >>> print fb.formatted ()
    <Form FBR>
     <Entity FBR-0 'Boat_in_Regatta' 'SRM.Boat_in_Regatta'>
      <Fieldset FBR-0:0 'primary'>
       <Field_Entity FBR-0:0:0 'left' 'SRM.Boat'>
        <Field_Entity FBR-0:0:0:0 'left' 'SRM.Boat_Class'>
         <Field FBR-0:0:0:0:0 'name'>
         <Field FBR-0:0:0:0:1 'max_crew'>
        <Field FBR-0:0:0:1 'sail_number'>
        <Field FBR-0:0:0:2 'nation'>
        <Field FBR-0:0:0:3 'sail_number_x'>
       <Field_Entity FBR-0:0:1 'right' 'SRM.Regatta'>
        <Field_Entity FBR-0:0:1:0 'left' 'SRM.Regatta_Event'>
         <Field FBR-0:0:1:0:0 'name'>
         <Field_Composite FBR-0:0:1:0:1 'date' 'MOM.Date_Interval_C'>
          <Field FBR-0:0:1:0:1.0 'start'>
          <Field FBR-0:0:1:0:1.1 'finish'>
        <Field_Entity FBR-0:0:1:1 'boat_class' 'SRM._Boat_Class_'>
         <Field FBR-0:0:1:1:0 'name'>
      <Fieldset FBR-0:1 'required'>
       <Field_Entity FBR-0:1:0 'skipper' 'SRM.Sailor'>
        <Field_Entity FBR-0:1:0:0 'left' 'PAP.Person'>
         <Field FBR-0:1:0:0:0 'last_name'>
         <Field FBR-0:1:0:0:1 'first_name'>
         <Field FBR-0:1:0:0:2 'middle_name'>
         <Field FBR-0:1:0:0:3 'title'>
        <Field FBR-0:1:0:1 'nation'>
        <Field FBR-0:1:0:2 'mna_number'>
        <Field_Entity FBR-0:1:0:3 'club' 'SRM.Club'>
         <Field FBR-0:1:0:3:0 'name'>
      <Entity_List FBR-0:2 'Crew_Member' <Entity_Link FBR-0:2::p 'Crew_Member' 'SRM.Crew_Member'>>
       <Entity_Link FBR-0:2::p 'Crew_Member' 'SRM.Crew_Member'>
        <Field_Role_Hidden FBR-0:2::p-0 'left' 'SRM.Boat_in_Regatta'>
        <Fieldset FBR-0:2::p-1 'primary'>
         <Field_Entity FBR-0:2::p-1:0 'right' 'SRM.Sailor'>
          <Field_Entity FBR-0:2::p-1:0:0 'left' 'PAP.Person'>
           <Field FBR-0:2::p-1:0:0:0 'last_name'>
           <Field FBR-0:2::p-1:0:0:1 'first_name'>
           <Field FBR-0:2::p-1:0:0:2 'middle_name'>
           <Field FBR-0:2::p-1:0:0:3 'title'>
          <Field FBR-0:2::p-1:0:1 'nation'>
          <Field FBR-0:2::p-1:0:2 'mna_number'>
          <Field_Entity FBR-0:2::p-1:0:3 'club' 'SRM.Club'>
           <Field FBR-0:2::p-1:0:3:0 'name'>
        <Fieldset FBR-0:2::p-2 'optional'>
         <Field FBR-0:2::p-2:0 'key'>
         <Field FBR-0:2::p-2:1 'role'>

    >>> PAP = scope.PAP
    >>> SRM = scope.SRM
    >>> bc  = SRM.Boat_Class ("Optimist", max_crew = 1)
    >>> ys  = SRM.Handicap ("Yardstick")
    >>> b   = SRM.Boat.instance_or_new (u"Optimist", u"1107", u"AUT", raw = True)
    >>> p   = PAP.Person.instance_or_new (u"Tanzer", u"Laurens")
    >>> s   = SRM.Sailor.instance_or_new (p,  nation = u"AUT", mna_number = u"29676", raw = True)
    >>> rev = SRM.Regatta_Event (u"Himmelfahrt", dict (start = u"20080501", raw = True), raw = True)
    >>> reo = SRM.Regatta_C (rev, bc)
    >>> bio = SRM.Boat_in_Regatta (b, reo, skipper = s)

    >>> bc2 = SRM.Boat_Class ("Laser2",   max_crew = 2)
    >>> b2  = SRM.Boat.instance_or_new (u"Laser2",   u"4321", u"AUT", raw = True)
    >>> p2  = PAP.Person.instance_or_new (u"Tanzer", u"Christian")
    >>> p3  = PAP.Person.instance_or_new (u"Tanzer", u"Clarissa")
    >>> s2  = SRM.Sailor.instance_or_new (p2, nation = u"AUT", raw = True)
    >>> s3  = SRM.Sailor.instance_or_new (p3, nation = u"AUT", raw = True)
    >>> rey = SRM.Regatta_H (rev, ys)
    >>> biy = SRM.Boat_in_Regatta (b2, rey, skipper = s3)
    >>> crw = SRM.Crew_Member (biy, s2)

    >>> scope.commit ()

    >>> fob = fb (SRM.Boat_in_Regatta, None, form_kw = dict (right = dict (init = reo), Crew_Member = dict (max_links = 1)))
    >>> fyb = fb (SRM.Boat_in_Regatta, biy)

    >>> for e in fb.transitive_iter () :
    ...   if hasattr (e, "allow_new") :
    ...     print "%-20s %-20s %-20s %s" % (e.id, e.type_base_name, e.__class__.__name__, e.allow_new)
    FBR-0:0:0            Boat                 Field_Entity         True
    FBR-0:0:0:0          Boat_Class           Field_Entity         True
    FBR-0:0:1            Regatta              Field_Entity         False
    FBR-0:0:1:0          Regatta_Event        Field_Entity         False
    FBR-0:0:1:1          _Boat_Class_         Field_Entity         True
    FBR-0:1:0            Sailor               Field_Entity         True
    FBR-0:1:0:0          Person               Field_Entity         True
    FBR-0:1:0:3          Club                 Field_Entity         True
    FBR-0:2::p-0         Boat_in_Regatta      Field_Role_Hidden    False
    FBR-0:2::p-1:0       Sailor               Field_Entity         True
    FBR-0:2::p-1:0:0     Person               Field_Entity         True
    FBR-0:2::p-1:0:3     Club                 Field_Entity         True

    >>> for e in fob.transitive_iter () :
    ...   if hasattr (e, "allow_new") :
    ...     print "%-20s %-20s %-20s %s" % (e.id, e.type_base_name, e.elem.__class__.__name__, e.allow_new)
    FBR-0:0:0            Boat                 Field_Entity         True
    FBR-0:0:0:0          Boat_Class           Field_Entity         True
    FBR-0:0:1            Regatta              Field_Entity         False
    FBR-0:1:0            Sailor               Field_Entity         True
    FBR-0:1:0:0          Person               Field_Entity         True
    FBR-0:1:0:3          Club                 Field_Entity         True

    >>> for e in fyb.transitive_iter () :
    ...   if hasattr (e, "allow_new") :
    ...     print "%-20s %-20s %-20s %s" % (e.id, e.type_base_name, e.elem.__class__.__name__, e.allow_new)
    FBR-0:0:0            Boat                 Field_Entity         True
    FBR-0:0:0:0          Boat_Class           Field_Entity         True
    FBR-0:0:1            Regatta              Field_Entity         False
    FBR-0:1:0            Sailor               Field_Entity         True
    FBR-0:1:0:0          Person               Field_Entity         True
    FBR-0:1:0:3          Club                 Field_Entity         True
    FBR-0:2::0-0         Boat_in_Regatta      Field_Role_Hidden    False
    FBR-0:2::0-1:0       Sailor               Field_Entity         True
    FBR-0:2::0-1:0:0     Person               Field_Entity         True
    FBR-0:2::0-1:0:3     Club                 Field_Entity         True

    >>> for i in fob.entity_children () :
    ...     print show_instance (i)
    <Entity FBR-0 'Boat_in_Regatta' 'SRM.Boat_in_Regatta'>           e = - o = - r = -
    <Field_Entity FBR-0:0:0 'left' 'SRM.Boat'>                       e = - o = - r = -
    <Field_Entity FBR-0:0:0:0 'left' 'SRM.Boat_Class'>               e = - o = - r = -
    <Field_Entity FBR-0:0:1 'right' 'SRM.Regatta'>                   e = 7 o = - r = -
    <Field_Entity FBR-0:1:0 'skipper' 'SRM.Sailor'>                  e = - o = - r = -
    <Field_Entity FBR-0:1:0:0 'left' 'PAP.Person'>                   e = - o = - r = -
    <Field_Entity FBR-0:1:0:3 'club' 'SRM.Club'>                     e = - o = - r = -

    >>> for i in fob.transitive_iter () :
    ...     print i.elem, formatted_1 ((i.value or {}))
    <Form FBR> {'sid' : 0}
    <Entity FBR-0 'Boat_in_Regatta' 'SRM.Boat_in_Regatta'> {'init' : {}, 'sid' : 'Zd-41gyogBtgIl:FljVdT-XsP4QdQ5PvnfspOQ'}
    <Fieldset FBR-0:0 'primary'> {}
    <Field_Entity FBR-0:0:0 'left' 'SRM.Boat'> {'init' : {}, 'sid' : '7eZfTalEbnWQKhrWTGYRAWI23bzdhrxoJ:o9Yg'}
    <Field_Entity FBR-0:0:0:0 'left' 'SRM.Boat_Class'> {'init' : {}, 'sid' : '5va8qZo2FVKY:CuEUr8VS9GAXagmzXzE1swrgg'}
    <Field FBR-0:0:0:0:0 'name'> {}
    <Field FBR-0:0:0:0:1 'max_crew'> {}
    <Field FBR-0:0:0:1 'sail_number'> {}
    <Field FBR-0:0:0:2 'nation'> {}
    <Field FBR-0:0:0:3 'sail_number_x'> {}
    <Field_Entity FBR-0:0:1 'right' 'SRM.Regatta'> {'init' : {'cid' : 7, 'pid' : 7}, 'sid' : 'HbQG8obzF891nbd6TGYS0hfKFy2U6jAJ7tWr4Q'}
    <Fieldset FBR-0:1 'required'> {}
    <Field_Entity FBR-0:1:0 'skipper' 'SRM.Sailor'> {'init' : {}, 'sid' : 'O6djzZZY-XLRt90aGDzBVdH9lc3GoDJnzHHZYg'}
    <Field_Entity FBR-0:1:0:0 'left' 'PAP.Person'> {'init' : {}, 'sid' : 'i7:14b70s9:Pb8AZRF1YZ3WM6pvyHBdjJIpQ5A'}
    <Field FBR-0:1:0:0:0 'last_name'> {}
    <Field FBR-0:1:0:0:1 'first_name'> {}
    <Field FBR-0:1:0:0:2 'middle_name'> {}
    <Field FBR-0:1:0:0:3 'title'> {}
    <Field FBR-0:1:0:1 'nation'> {}
    <Field FBR-0:1:0:2 'mna_number'> {}
    <Field_Entity FBR-0:1:0:3 'club' 'SRM.Club'> {'init' : {}, 'sid' : 'Hq6M2e8Vp3oXZJdAOUcwowo-EP1JwjoU1cqqIA'}
    <Field FBR-0:1:0:3:0 'name'> {}
    <Entity_List FBR-0:2 'Crew_Member' <Entity_Link FBR-0:2::p 'Crew_Member' 'SRM.Crew_Member'>> {}

    >>> fob_p = fb (SRM.Boat_in_Regatta, None, form_kw = dict (right = dict (prefilled = True, init = reo), Crew_Member = dict (max_links   = 1)))
    >>> for i in fob_p.transitive_iter () :
    ...     print i.elem, formatted_1 ((i.value or {}))
    <Form FBR> {'sid' : 0}
    <Entity FBR-0 'Boat_in_Regatta' 'SRM.Boat_in_Regatta'> {'init' : {}, 'sid' : 'Zd-41gyogBtgIl:FljVdT-XsP4QdQ5PvnfspOQ'}
    <Fieldset FBR-0:0 'primary'> {}
    <Field_Entity FBR-0:0:0 'left' 'SRM.Boat'> {'init' : {}, 'sid' : '7eZfTalEbnWQKhrWTGYRAWI23bzdhrxoJ:o9Yg'}
    <Field_Entity FBR-0:0:0:0 'left' 'SRM.Boat_Class'> {'init' : {}, 'sid' : '5va8qZo2FVKY:CuEUr8VS9GAXagmzXzE1swrgg'}
    <Field FBR-0:0:0:0:0 'name'> {}
    <Field FBR-0:0:0:0:1 'max_crew'> {}
    <Field FBR-0:0:0:1 'sail_number'> {}
    <Field FBR-0:0:0:2 'nation'> {}
    <Field FBR-0:0:0:3 'sail_number_x'> {}
    <Field_Entity FBR-0:0:1 'right' 'SRM.Regatta'> {'edit' : {'cid' : 7, 'pid' : 7}, 'prefilled' : True, 'sid' : 'P-9h9ZN5LkBldyXc5Kk:errFxKH2ZAdzjqWJ:Q'}
    <Fieldset FBR-0:1 'required'> {}
    <Field_Entity FBR-0:1:0 'skipper' 'SRM.Sailor'> {'init' : {}, 'sid' : 'O6djzZZY-XLRt90aGDzBVdH9lc3GoDJnzHHZYg'}
    <Field_Entity FBR-0:1:0:0 'left' 'PAP.Person'> {'init' : {}, 'sid' : 'i7:14b70s9:Pb8AZRF1YZ3WM6pvyHBdjJIpQ5A'}
    <Field FBR-0:1:0:0:0 'last_name'> {}
    <Field FBR-0:1:0:0:1 'first_name'> {}
    <Field FBR-0:1:0:0:2 'middle_name'> {}
    <Field FBR-0:1:0:0:3 'title'> {}
    <Field FBR-0:1:0:1 'nation'> {}
    <Field FBR-0:1:0:2 'mna_number'> {}
    <Field_Entity FBR-0:1:0:3 'club' 'SRM.Club'> {'init' : {}, 'sid' : 'Hq6M2e8Vp3oXZJdAOUcwowo-EP1JwjoU1cqqIA'}
    <Field FBR-0:1:0:3:0 'name'> {}
    <Entity_List FBR-0:2 'Crew_Member' <Entity_Link FBR-0:2::p 'Crew_Member' 'SRM.Crew_Member'>> {}

    >>> print formatted (fob.as_json_cargo, level = 1)
      { '$id' : 'FBR'
      , 'children' :
          [ { '$id' : 'FBR-0'
            , 'children' :
                [ { '$id' : 'FBR-0:0'
                  , 'children' :
                      [ { '$id' : 'FBR-0:0:0'
                        , 'allow_new' : True
                        , 'children' :
                            [ { '$id' : 'FBR-0:0:0:0'
                              , 'allow_new' : True
                              , 'children' :
                                  [ { '$id' : 'FBR-0:0:0:0:0'
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
                                  , { '$id' : 'FBR-0:0:0:0:1'
                                    , 'kind' : 'required'
                                    , 'label' : 'Max crew'
                                    , 'name' : 'max_crew'
                                    , 'required' : True
                                    , 'type' : 'Field'
                                    , 'value' :
                                        {}
                                    }
                                  ]
                              , 'collapsed' : False
                              , 'kind' : 'primary'
                              , 'label' : 'Class'
                              , 'name' : 'left'
                              , 'required' : True
                              , 'type' : 'Field_Entity'
                              , 'type_name' : 'SRM.Boat_Class'
                              , 'value' :
                                  { 'init' :
                                      {}
                                  , 'sid' : '5va8qZo2FVKY:CuEUr8VS9GAXagmzXzE1swrgg'
                                  }
                              }
                            , { '$id' : 'FBR-0:0:0:1'
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
                              , 'required' : True
                              , 'type' : 'Field'
                              , 'value' :
                                  {}
                              }
                            , { '$id' : 'FBR-0:0:0:2'
                              , 'kind' : 'primary'
                              , 'label' : 'Nation'
                              , 'name' : 'nation'
                              , 'type' : 'Field'
                              , 'value' :
                                  {}
                              }
                            , { '$id' : 'FBR-0:0:0:3'
                              , 'completer' :
                                  { 'entity_p' : True
                                  , 'names' :
                                      [ 'sail_number_x'
                                      , 'left'
                                      , 'sail_number'
                                      , 'nation'
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
                        , 'kind' : 'primary'
                        , 'label' : 'Boat'
                        , 'name' : 'left'
                        , 'required' : True
                        , 'type' : 'Field_Entity'
                        , 'type_name' : 'SRM.Boat'
                        , 'value' :
                            { 'init' :
                                {}
                            , 'sid' : '7eZfTalEbnWQKhrWTGYRAWI23bzdhrxoJ:o9Yg'
                            }
                        }
                      , { '$id' : 'FBR-0:0:1'
                        , 'allow_new' : False
                        , 'collapsed' : True
                        , 'kind' : 'primary'
                        , 'label' : 'Regatta'
                        , 'name' : 'right'
                        , 'required' : True
                        , 'type' : 'Field_Entity'
                        , 'type_name' : 'SRM.Regatta'
                        , 'value' :
                            { 'init' :
                                { 'cid' : 7
                                , 'pid' : 7
                                }
                            , 'sid' : 'HbQG8obzF891nbd6TGYS0hfKFy2U6jAJ7tWr4Q'
                            }
                        }
                      ]
                  , 'collapsed' : False
                  , 'name' : 'primary'
                  , 'type' : 'Fieldset'
                  }
                , { '$id' : 'FBR-0:1'
                  , 'children' :
                      [ { '$id' : 'FBR-0:1:0'
                        , 'allow_new' : True
                        , 'children' :
                            [ { '$id' : 'FBR-0:1:0:0'
                              , 'allow_new' : True
                              , 'children' :
                                  [ { '$id' : 'FBR-0:1:0:0:0'
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
                                        {}
                                    }
                                  , { '$id' : 'FBR-0:1:0:0:1'
                                    , 'completer' :
                                        { 'embedded_p' : True
                                        , 'entity_p' : True
                                        , 'names' :
                                            [ 'first_name'
                                            , 'last_name'
                                            , 'middle_name'
                                            , 'title'
                                            ]
                                        , 'treshold' : 2
                                        }
                                    , 'kind' : 'primary'
                                    , 'label' : 'First name'
                                    , 'name' : 'first_name'
                                    , 'required' : True
                                    , 'type' : 'Field'
                                    , 'value' :
                                        {}
                                    }
                                  , { '$id' : 'FBR-0:1:0:0:2'
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
                                  , { '$id' : 'FBR-0:1:0:0:3'
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
                              , 'collapsed' : False
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
                              , 'type_name' : 'PAP.Person'
                              , 'value' :
                                  { 'init' :
                                      {}
                                  , 'sid' : 'i7:14b70s9:Pb8AZRF1YZ3WM6pvyHBdjJIpQ5A'
                                  }
                              }
                            , { '$id' : 'FBR-0:1:0:1'
                              , 'kind' : 'primary'
                              , 'label' : 'Nation'
                              , 'name' : 'nation'
                              , 'type' : 'Field'
                              , 'value' :
                                  {}
                              }
                            , { '$id' : 'FBR-0:1:0:2'
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
                                  {}
                              }
                            , { '$id' : 'FBR-0:1:0:3'
                              , 'allow_new' : True
                              , 'children' :
                                  [ { '$id' : 'FBR-0:1:0:3:0'
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
                              , 'collapsed' : False
                              , 'kind' : 'primary'
                              , 'label' : 'Club'
                              , 'name' : 'club'
                              , 'type' : 'Field_Entity'
                              , 'type_name' : 'SRM.Club'
                              , 'value' :
                                  { 'init' :
                                      {}
                                  , 'sid' : 'Hq6M2e8Vp3oXZJdAOUcwowo-EP1JwjoU1cqqIA'
                                  }
                              }
                            ]
                        , 'collapsed' : False
                        , 'kind' : 'required'
                        , 'label' : 'Skipper'
                        , 'name' : 'skipper'
                        , 'required' : True
                        , 'type' : 'Field_Entity'
                        , 'type_name' : 'SRM.Sailor'
                        , 'value' :
                            { 'init' :
                                {}
                            , 'sid' : 'O6djzZZY-XLRt90aGDzBVdH9lc3GoDJnzHHZYg'
                            }
                        }
                      ]
                  , 'collapsed' : False
                  , 'name' : 'required'
                  , 'type' : 'Fieldset'
                  }
                , { '$id' : 'FBR-0:2'
                  , 'max_links' : 1
                  , 'name' : 'Crew_Member'
                  , 'type' : 'Entity_List'
                  , 'type_name' : 'SRM.Crew_Member'
                  }
                ]
            , 'name' : 'Boat_in_Regatta'
            , 'type' : 'Entity'
            , 'type_name' : 'SRM.Boat_in_Regatta'
            , 'value' :
                { 'init' :
                    {}
                , 'sid' : 'Zd-41gyogBtgIl:FljVdT-XsP4QdQ5PvnfspOQ'
                }
            }
          ]
      , 'type' : 'Form'
      , 'value' :
          { 'sid' : 0 }
      }



    >>> print formatted (fob_p.as_json_cargo, level = 1)
      { '$id' : 'FBR'
      , 'children' :
          [ { '$id' : 'FBR-0'
            , 'children' :
                [ { '$id' : 'FBR-0:0'
                  , 'children' :
                      [ { '$id' : 'FBR-0:0:0'
                        , 'allow_new' : True
                        , 'children' :
                            [ { '$id' : 'FBR-0:0:0:0'
                              , 'allow_new' : True
                              , 'children' :
                                  [ { '$id' : 'FBR-0:0:0:0:0'
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
                                  , { '$id' : 'FBR-0:0:0:0:1'
                                    , 'kind' : 'required'
                                    , 'label' : 'Max crew'
                                    , 'name' : 'max_crew'
                                    , 'required' : True
                                    , 'type' : 'Field'
                                    , 'value' :
                                        {}
                                    }
                                  ]
                              , 'collapsed' : False
                              , 'kind' : 'primary'
                              , 'label' : 'Class'
                              , 'name' : 'left'
                              , 'required' : True
                              , 'type' : 'Field_Entity'
                              , 'type_name' : 'SRM.Boat_Class'
                              , 'value' :
                                  { 'init' :
                                      {}
                                  , 'sid' : '5va8qZo2FVKY:CuEUr8VS9GAXagmzXzE1swrgg'
                                  }
                              }
                            , { '$id' : 'FBR-0:0:0:1'
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
                              , 'required' : True
                              , 'type' : 'Field'
                              , 'value' :
                                  {}
                              }
                            , { '$id' : 'FBR-0:0:0:2'
                              , 'kind' : 'primary'
                              , 'label' : 'Nation'
                              , 'name' : 'nation'
                              , 'type' : 'Field'
                              , 'value' :
                                  {}
                              }
                            , { '$id' : 'FBR-0:0:0:3'
                              , 'completer' :
                                  { 'entity_p' : True
                                  , 'names' :
                                      [ 'sail_number_x'
                                      , 'left'
                                      , 'sail_number'
                                      , 'nation'
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
                        , 'kind' : 'primary'
                        , 'label' : 'Boat'
                        , 'name' : 'left'
                        , 'required' : True
                        , 'type' : 'Field_Entity'
                        , 'type_name' : 'SRM.Boat'
                        , 'value' :
                            { 'init' :
                                {}
                            , 'sid' : '7eZfTalEbnWQKhrWTGYRAWI23bzdhrxoJ:o9Yg'
                            }
                        }
                      , { '$id' : 'FBR-0:0:1'
                        , 'allow_new' : False
                        , 'collapsed' : True
                        , 'kind' : 'primary'
                        , 'label' : 'Regatta'
                        , 'name' : 'right'
                        , 'prefilled' : True
                        , 'required' : True
                        , 'type' : 'Field_Entity'
                        , 'type_name' : 'SRM.Regatta'
                        , 'value' :
                            { 'edit' :
                                { 'cid' : 7
                                , 'pid' : 7
                                }
                            , 'prefilled' : True
                            , 'sid' : 'P-9h9ZN5LkBldyXc5Kk:errFxKH2ZAdzjqWJ:Q'
                            }
                        }
                      ]
                  , 'collapsed' : False
                  , 'name' : 'primary'
                  , 'type' : 'Fieldset'
                  }
                , { '$id' : 'FBR-0:1'
                  , 'children' :
                      [ { '$id' : 'FBR-0:1:0'
                        , 'allow_new' : True
                        , 'children' :
                            [ { '$id' : 'FBR-0:1:0:0'
                              , 'allow_new' : True
                              , 'children' :
                                  [ { '$id' : 'FBR-0:1:0:0:0'
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
                                        {}
                                    }
                                  , { '$id' : 'FBR-0:1:0:0:1'
                                    , 'completer' :
                                        { 'embedded_p' : True
                                        , 'entity_p' : True
                                        , 'names' :
                                            [ 'first_name'
                                            , 'last_name'
                                            , 'middle_name'
                                            , 'title'
                                            ]
                                        , 'treshold' : 2
                                        }
                                    , 'kind' : 'primary'
                                    , 'label' : 'First name'
                                    , 'name' : 'first_name'
                                    , 'required' : True
                                    , 'type' : 'Field'
                                    , 'value' :
                                        {}
                                    }
                                  , { '$id' : 'FBR-0:1:0:0:2'
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
                                  , { '$id' : 'FBR-0:1:0:0:3'
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
                              , 'collapsed' : False
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
                              , 'type_name' : 'PAP.Person'
                              , 'value' :
                                  { 'init' :
                                      {}
                                  , 'sid' : 'i7:14b70s9:Pb8AZRF1YZ3WM6pvyHBdjJIpQ5A'
                                  }
                              }
                            , { '$id' : 'FBR-0:1:0:1'
                              , 'kind' : 'primary'
                              , 'label' : 'Nation'
                              , 'name' : 'nation'
                              , 'type' : 'Field'
                              , 'value' :
                                  {}
                              }
                            , { '$id' : 'FBR-0:1:0:2'
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
                                  {}
                              }
                            , { '$id' : 'FBR-0:1:0:3'
                              , 'allow_new' : True
                              , 'children' :
                                  [ { '$id' : 'FBR-0:1:0:3:0'
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
                              , 'collapsed' : False
                              , 'kind' : 'primary'
                              , 'label' : 'Club'
                              , 'name' : 'club'
                              , 'type' : 'Field_Entity'
                              , 'type_name' : 'SRM.Club'
                              , 'value' :
                                  { 'init' :
                                      {}
                                  , 'sid' : 'Hq6M2e8Vp3oXZJdAOUcwowo-EP1JwjoU1cqqIA'
                                  }
                              }
                            ]
                        , 'collapsed' : False
                        , 'kind' : 'required'
                        , 'label' : 'Skipper'
                        , 'name' : 'skipper'
                        , 'required' : True
                        , 'type' : 'Field_Entity'
                        , 'type_name' : 'SRM.Sailor'
                        , 'value' :
                            { 'init' :
                                {}
                            , 'sid' : 'O6djzZZY-XLRt90aGDzBVdH9lc3GoDJnzHHZYg'
                            }
                        }
                      ]
                  , 'collapsed' : False
                  , 'name' : 'required'
                  , 'type' : 'Fieldset'
                  }
                , { '$id' : 'FBR-0:2'
                  , 'max_links' : 1
                  , 'name' : 'Crew_Member'
                  , 'type' : 'Entity_List'
                  , 'type_name' : 'SRM.Crew_Member'
                  }
                ]
            , 'name' : 'Boat_in_Regatta'
            , 'type' : 'Entity'
            , 'type_name' : 'SRM.Boat_in_Regatta'
            , 'value' :
                { 'init' :
                    {}
                , 'sid' : 'Zd-41gyogBtgIl:FljVdT-XsP4QdQ5PvnfspOQ'
                }
            }
          ]
      , 'type' : 'Form'
      , 'value' :
          { 'sid' : 0 }
      }

"""

_entity_links_group = """
    >>> scope = Scaffold.scope ("hps://") # doctest:+ELLIPSIS
    Creating new scope MOMT__...
    >>> from _GTW._AFS._MOM import Spec
    >>> S = Spec.Entity (include_links = ("addresses", ), entity_links_group = "Entity_Links_Group")
    >>> x = S (scope.PAP.Person.E_Type)
    >>> print x.formatted ()
    <Entity None 'Person' 'PAP.Person'>
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
      <Entity_List None 'Person_has_Address' <Entity_Link None 'Person_has_Address' 'PAP.Person_has_Address'>>
       <Entity_Link None 'Person_has_Address' 'PAP.Person_has_Address'>
        <Field_Role_Hidden None 'left' 'PAP.Person'>
        <Fieldset None 'primary'>
         <Field_Entity None 'right' 'PAP.Address'>
          <Field None 'street'>
          <Field None 'zip'>
          <Field None 'city'>
          <Field None 'country'>
        <Fieldset None 'optional'>
         <Field None 'desc'>
    >>> print Form ("ELG", children = [x]).formatted ()
    <Form ELG>
     <Entity ELG-0 'Person' 'PAP.Person'>
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
       <Entity_List ELG-0:3:0 'Person_has_Address' <Entity_Link ELG-0:3:0::p 'Person_has_Address' 'PAP.Person_has_Address'>>
        <Entity_Link ELG-0:3:0::p 'Person_has_Address' 'PAP.Person_has_Address'>
         <Field_Role_Hidden ELG-0:3:0::p-0 'left' 'PAP.Person'>
         <Fieldset ELG-0:3:0::p-1 'primary'>
          <Field_Entity ELG-0:3:0::p-1:0 'right' 'PAP.Address'>
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

Instance.sort_json = True

def show_instance (i) :
    def show_entity (i, name) :
        e = getattr (i, name)
        return "%1.1s = %s" % (name, getattr (e, "pid", "-"))
    return "%-72s %s %s %s" % \
        ( i.elem
        , show_entity (i, "entity")
        , show_entity (i, "outer_entity")
        , show_entity (i, "role_entity")
        )

### `json_value` copied from output of::
###     /usr/bin/js -s -f GTW/AFS/Elements.test
json_value = """\
  {"$id":"FB","sid":0,"$child_ids":["FB-0","FB-0:2::0"],"FB-0":{"init":{"cid":2,"pid":2},"sid":"ZE5i0RV4B6i6wEn0wszdszAuXDu121dutn0uEg","$id":"FB-0","$child_ids":["FB-0:0:0","FB-0:0:1","FB-0:0:2","FB-0:0:3","FB-0:1:0"],"edit":{"cid":2,"pid":2},"FB-0:0:0":{"init":{"cid":1,"pid":1},"sid":"qhCKKsimOo:3Hla747-HuSlL5hzwvBqKojyvIg","$id":"FB-0:0:0","$child_ids":[],"edit":{"cid":1,"pid":1},"anchor_id":"FB-0","allow_new":true},"FB-0:0:1":{"init":"1107"},"FB-0:0:2":{"init":"AUT"},"FB-0:0:3":{"init":""},"FB-0:1:0":{"init":""}},"FB-0:2::0":{"init":{"cid":7,"pid":7},"sid":"QSvku2fc3JI02:LH5rBsLqrXDzWvSbNZ-hXkBQ","$id":"FB-0:2::0","$child_ids":["FB-0:2::0-0","FB-0:2::0-1:0","FB-0:2::0-2:0","FB-0:2::0-3:0","FB-0:2::0-3:1"],"edit":{"cid":7,"pid":7},"FB-0:2::0-0":{"init":{"cid":2,"pid":2},"sid":"73AhMKVvgduSBcdc9J-WeU1hPS8BJa7jWlFOkw","role_id":"FB-0","edit":{"cid":2,"pid":2},"allow_new":false},"FB-0:2::0-1:0":{"init":{"cid":6,"pid":6},"sid":"s:FQz-HZIl9NAA:-YHx4IFRn3WMzvWHFWK:b5Q","$id":"FB-0:2::0-1:0","$child_ids":[],"edit":{"cid":6,"pid":6},"anchor_id":"FB-0:2::0","allow_new":false},"FB-0:2::0-2:0":{"init":{"cid":4,"pid":4},"sid":"OMXS5mItieYGgFiLVGNgcS:zMWmtL8cV6qw9CA","$id":"FB-0:2::0-2:0","$child_ids":["FB-0:2::0-2:0:0","FB-0:2::0-2:0:1","FB-0:2::0-2:0:2","FB-0:2::0-2:0:3"],"edit":{"cid":4,"pid":4},"anchor_id":"FB-0:2::0","allow_new":true,"FB-0:2::0-2:0:0":{"init":{"cid":3,"pid":3},"sid":"Fy2PPgkt0OF-ExUfoga3fcrKvv3qjOABiCN9rQ","$id":"FB-0:2::0-2:0:0","$child_ids":[],"edit":{"cid":3,"pid":3},"anchor_id":"FB-0:2::0-2:0","allow_new":false},"FB-0:2::0-2:0:1":{"init":"AUT"},"FB-0:2::0-2:0:2":{"init":"29676"},"FB-0:2::0-2:0:3":{"init":{},"sid":"vPwcc9Gqe25rUmpJ7cBwLBH9yc6iGCbRVfNrEg","$id":"FB-0:2::0-2:0:3","$child_ids":["FB-0:2::0-2:0:3:0"],"edit":{},"anchor_id":"FB-0:2::0-2:0","allow_new":true,"FB-0:2::0-2:0:3:0":{"init":""}}},"FB-0:2::0-3:0":{"init":""},"FB-0:2::0-3:1":{"init":""}}}
"""
json_bad  = """{"$id":"FC"}"""

__test__ = dict \
    ( AFS_Spec           = _test_code
    , Entity_Links_Group = _entity_links_group
    , Person             = _person_test
    , Prefilled          = _prefilled_test
    )

### __END__ AFS_Spec
