# -*- coding: iso-8859-1 -*-
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
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
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
#    ««revision-date»»···
#--

_test_code = """
    >>> scope = Scaffold.scope ("hps://") # doctest:+ELLIPSIS
    Creating new scope MOMT__...
    >>> from _GTW._AFS._MOM import Spec
    >>> S = Spec.Entity ()
    >>> x = S (scope.PAP.Person._etype)
    >>> print repr (x)
    <Entity None 'GTW.OMP.PAP.Person'>
     <Fieldset None 'primary'>
      <Field None 'last_name'>
      <Field None 'first_name'>
      <Field None 'middle_name'>
      <Field None 'title'>
     <Fieldset None 'necessary'>
      <Field None 'sex'>
     <Fieldset None 'optional'>
      <Field_Composite None 'lifetime'>
       <Field None 'start'>
       <Field None 'finish'>
      <Field None 'salutation'>

    >>> T = Spec.Entity ( Spec.Entity_Link ("events",
    ...   Spec.Entity_Link
    ...     ( "recurrence", Spec.Entity_Link ("rules")
    ...     , include_kind_groups = True), include_kind_groups = True
    ...     ) , include_kind_groups = True)
    >>> y = T (scope.SWP.Page._etype)
    >>> print repr (y)
    <Entity None 'GTW.OMP.SWP.Page'>
     <Fieldset None 'primary'>
      <Field None 'perma_name'>
     <Fieldset None 'required'>
      <Field None 'text'>
     <Fieldset None 'necessary'>
      <Field None 'short_title'>
      <Field None 'title'>
     <Fieldset None 'optional'>
      <Field_Composite None 'date'>
       <Field None 'start'>
       <Field None 'finish'>
      <Field None 'format'>
      <Field None 'head_line'>
      <Field None 'prio'>
     <Entity_List None <Entity_Link None 'GTW.OMP.EVT.Event'>>
      <Entity_Link None 'GTW.OMP.EVT.Event'>
       <Fieldset None 'primary'>
        <Field_Composite None 'date'>
         <Field None 'start'>
         <Field None 'finish'>
        <Field_Composite None 'time'>
         <Field None 'start'>
         <Field None 'finish'>
       <Fieldset None 'optional'>
        <Field None 'detail'>
        <Field None 'short_title'>
       <Entity_Link None 'GTW.OMP.EVT.Recurrence_Spec'>
        <Fieldset None 'optional'>
         <Field None 'dates'>
         <Field None 'date_exceptions'>
        <Entity_List None <Entity_Link None 'GTW.OMP.EVT.Recurrence_Rule'>>
         <Entity_Link None 'GTW.OMP.EVT.Recurrence_Rule'>
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
     <Entity F-1 'GTW.OMP.SWP.Page'>
      <Fieldset F-1:1 'primary'>
       <Field F-1:1:1 'perma_name'>
      <Fieldset F-1:2 'required'>
       <Field F-1:2:1 'text'>
      <Fieldset F-1:3 'necessary'>
       <Field F-1:3:1 'short_title'>
       <Field F-1:3:2 'title'>
      <Fieldset F-1:4 'optional'>
       <Field_Composite F-1:4:1 'date'>
        <Field F-1:4:1.1 'start'>
        <Field F-1:4:1.2 'finish'>
       <Field F-1:4:2 'format'>
       <Field F-1:4:3 'head_line'>
       <Field F-1:4:4 'prio'>
      <Entity_List F-1:5 <Entity_Link F-1:5::0 'GTW.OMP.EVT.Event'>>
       <Entity_Link F-1:5::0 'GTW.OMP.EVT.Event'>
        <Fieldset F-1:5::0-1 'primary'>
         <Field_Composite F-1:5::0-1:1 'date'>
          <Field F-1:5::0-1:1.1 'start'>
          <Field F-1:5::0-1:1.2 'finish'>
         <Field_Composite F-1:5::0-1:2 'time'>
          <Field F-1:5::0-1:2.1 'start'>
          <Field F-1:5::0-1:2.2 'finish'>
        <Fieldset F-1:5::0-2 'optional'>
         <Field F-1:5::0-2:1 'detail'>
         <Field F-1:5::0-2:2 'short_title'>
        <Entity_Link F-1:5::0-3 'GTW.OMP.EVT.Recurrence_Spec'>
         <Fieldset F-1:5::0-3:1 'optional'>
          <Field F-1:5::0-3:1:1 'dates'>
          <Field F-1:5::0-3:1:2 'date_exceptions'>
         <Entity_List F-1:5::0-3:2 <Entity_Link F-1:5::0-3:2::0 'GTW.OMP.EVT.Recurrence_Rule'>>
          <Entity_Link F-1:5::0-3:2::0 'GTW.OMP.EVT.Recurrence_Rule'>
           <Fieldset F-1:5::0-3:2::0-1 'primary'>
            <Field F-1:5::0-3:2::0-1:1 'is_exception'>
            <Field F-1:5::0-3:2::0-1:2 'desc'>
           <Fieldset F-1:5::0-3:2::0-2 'optional'>
            <Field F-1:5::0-3:2::0-2:1 'start'>
            <Field F-1:5::0-3:2::0-2:2 'finish'>
            <Field F-1:5::0-3:2::0-2:3 'period'>
            <Field F-1:5::0-3:2::0-2:4 'unit'>
            <Field F-1:5::0-3:2::0-2:5 'week_day'>
            <Field F-1:5::0-3:2::0-2:6 'count'>
            <Field F-1:5::0-3:2::0-2:7 'restrict_pos'>
            <Field F-1:5::0-3:2::0-2:8 'month_day'>
            <Field F-1:5::0-3:2::0-2:9 'month'>
            <Field F-1:5::0-3:2::0-2:10 'week'>
            <Field F-1:5::0-3:2::0-2:11 'year_day'>
            <Field F-1:5::0-3:2::0-2:12 'easter_offset'>
    >>> f = Form ("X", children = [x, y])
    >>> print repr (f)
    <Form X>
     <Entity X-1 'GTW.OMP.PAP.Person'>
      <Fieldset X-1:1 'primary'>
       <Field X-1:1:1 'last_name'>
       <Field X-1:1:2 'first_name'>
       <Field X-1:1:3 'middle_name'>
       <Field X-1:1:4 'title'>
      <Fieldset X-1:2 'necessary'>
       <Field X-1:2:1 'sex'>
      <Fieldset X-1:3 'optional'>
       <Field_Composite X-1:3:1 'lifetime'>
        <Field X-1:3:1.1 'start'>
        <Field X-1:3:1.2 'finish'>
       <Field X-1:3:2 'salutation'>
     <Entity X-2 'GTW.OMP.SWP.Page'>
      <Fieldset X-2:1 'primary'>
       <Field X-2:1:1 'perma_name'>
      <Fieldset X-2:2 'required'>
       <Field X-2:2:1 'text'>
      <Fieldset X-2:3 'necessary'>
       <Field X-2:3:1 'short_title'>
       <Field X-2:3:2 'title'>
      <Fieldset X-2:4 'optional'>
       <Field_Composite X-2:4:1 'date'>
        <Field X-2:4:1.1 'start'>
        <Field X-2:4:1.2 'finish'>
       <Field X-2:4:2 'format'>
       <Field X-2:4:3 'head_line'>
       <Field X-2:4:4 'prio'>
      <Entity_List X-2:5 <Entity_Link X-2:5::0 'GTW.OMP.EVT.Event'>>
       <Entity_Link X-2:5::0 'GTW.OMP.EVT.Event'>
        <Fieldset X-2:5::0-1 'primary'>
         <Field_Composite X-2:5::0-1:1 'date'>
          <Field X-2:5::0-1:1.1 'start'>
          <Field X-2:5::0-1:1.2 'finish'>
         <Field_Composite X-2:5::0-1:2 'time'>
          <Field X-2:5::0-1:2.1 'start'>
          <Field X-2:5::0-1:2.2 'finish'>
        <Fieldset X-2:5::0-2 'optional'>
         <Field X-2:5::0-2:1 'detail'>
         <Field X-2:5::0-2:2 'short_title'>
        <Entity_Link X-2:5::0-3 'GTW.OMP.EVT.Recurrence_Spec'>
         <Fieldset X-2:5::0-3:1 'optional'>
          <Field X-2:5::0-3:1:1 'dates'>
          <Field X-2:5::0-3:1:2 'date_exceptions'>
         <Entity_List X-2:5::0-3:2 <Entity_Link X-2:5::0-3:2::0 'GTW.OMP.EVT.Recurrence_Rule'>>
          <Entity_Link X-2:5::0-3:2::0 'GTW.OMP.EVT.Recurrence_Rule'>
           <Fieldset X-2:5::0-3:2::0-1 'primary'>
            <Field X-2:5::0-3:2::0-1:1 'is_exception'>
            <Field X-2:5::0-3:2::0-1:2 'desc'>
           <Fieldset X-2:5::0-3:2::0-2 'optional'>
            <Field X-2:5::0-3:2::0-2:1 'start'>
            <Field X-2:5::0-3:2::0-2:2 'finish'>
            <Field X-2:5::0-3:2::0-2:3 'period'>
            <Field X-2:5::0-3:2::0-2:4 'unit'>
            <Field X-2:5::0-3:2::0-2:5 'week_day'>
            <Field X-2:5::0-3:2::0-2:6 'count'>
            <Field X-2:5::0-3:2::0-2:7 'restrict_pos'>
            <Field X-2:5::0-3:2::0-2:8 'month_day'>
            <Field X-2:5::0-3:2::0-2:9 'month'>
            <Field X-2:5::0-3:2::0-2:10 'week'>
            <Field X-2:5::0-3:2::0-2:11 'year_day'>
            <Field X-2:5::0-3:2::0-2:12 'easter_offset'>
    >>> pprint.pprint (f.as_json_cargo)
    {'$id': 'X',
     'children': [{'$id': 'X-1',
                   'children': [{'$id': 'X-1:1',
                                 'children': [{'$id': 'X-1:1:1',
                                               'description': 'Last name of person',
                                               'name': 'last_name',
                                               'type': 'Field',
                                               'ui_name': u'Last name'},
                                              {'$id': 'X-1:1:2',
                                               'description': 'First name of person',
                                               'name': 'first_name',
                                               'type': 'Field',
                                               'ui_name': u'First name'},
                                              {'$id': 'X-1:1:3',
                                               'description': 'Middle name of person',
                                               'name': 'middle_name',
                                               'type': 'Field',
                                               'ui_name': u'Middle name'},
                                              {'$id': 'X-1:1:4',
                                               'description': 'Academic title.',
                                               'name': 'title',
                                               'type': 'Field',
                                               'ui_name': u'Academic title'}],
                                 'collapsed': False,
                                 'name': 'primary',
                                 'type': 'Fieldset'},
                                {'$id': 'X-1:2',
                                 'children': [{'$id': 'X-1:2:1',
                                               'description': 'Sex of a person.',
                                               'name': 'sex',
                                               'type': 'Field',
                                               'ui_name': u'Sex'}],
                                 'collapsed': True,
                                 'name': 'necessary',
                                 'type': 'Fieldset'},
                                {'$id': 'X-1:3',
                                 'children': [{'$id': 'X-1:3:1',
                                               'children': [{'$id': 'X-1:3:1.1',
                                                             'description': 'Start date of interval',
                                                             'name': 'start',
                                                             'type': 'Field',
                                                             'ui_name': u'Start'},
                                                            {'$id': 'X-1:3:1.2',
                                                             'description': 'Finish date of interval',
                                                             'name': 'finish',
                                                             'type': 'Field',
                                                             'ui_name': u'Finish'}],
                                               'description': 'Date of birth [`start`] (and death [`finish`])',
                                               'name': 'lifetime',
                                               'type': 'Field_Composite',
                                               'type_name': 'MOM.Date_Interval',
                                               'ui_name': u'Lifetime'},
                                              {'$id': 'X-1:3:2',
                                               'description': 'Salutation to be used when communicating with person (e.g., in a letter or email).',
                                               'name': 'salutation',
                                               'type': 'Field',
                                               'ui_name': u'Salutation'}],
                                 'collapsed': True,
                                 'name': 'optional',
                                 'type': 'Fieldset'}],
                   'name': 'GTW.OMP.PAP.Person',
                   'type': 'Entity',
                   'type_name': 'GTW.OMP.PAP.Person'},
                  {'$id': 'X-2',
                   'children': [{'$id': 'X-2:1',
                                 'children': [{'$id': 'X-2:1:1',
                                               'description': 'Name used for perma-link.',
                                               'name': 'perma_name',
                                               'type': 'Field',
                                               'ui_name': 'Name'}],
                                 'collapsed': False,
                                 'name': 'primary',
                                 'type': 'Fieldset'},
                                {'$id': 'X-2:2',
                                 'children': [{'$id': 'X-2:2:1',
                                               'description': 'Text for web page in markup specified by `format`.',
                                               'name': 'text',
                                               'type': 'Field',
                                               'ui_name': u'Text'}],
                                 'collapsed': True,
                                 'name': 'required',
                                 'type': 'Fieldset'},
                                {'$id': 'X-2:3',
                                 'children': [{'$id': 'X-2:3:1',
                                               'description': 'Short title (used in navigation).',
                                               'name': 'short_title',
                                               'type': 'Field',
                                               'ui_name': u'Short title'},
                                              {'$id': 'X-2:3:2',
                                               'description': 'Title of the web page',
                                               'name': 'title',
                                               'type': 'Field',
                                               'ui_name': u'Title'}],
                                 'collapsed': True,
                                 'name': 'necessary',
                                 'type': 'Fieldset'},
                                {'$id': 'X-2:4',
                                 'children': [{'$id': 'X-2:4:1',
                                               'children': [{'$id': 'X-2:4:1.1',
                                                             'description': 'Start date of interval',
                                                             'name': 'start',
                                                             'type': 'Field',
                                                             'ui_name': u'Start'},
                                                            {'$id': 'X-2:4:1.2',
                                                             'description': 'Finish date of interval',
                                                             'name': 'finish',
                                                             'type': 'Field',
                                                             'ui_name': u'Finish'}],
                                               'description': 'Publication (`start`) and expiration date (`finish`)',
                                               'explanation': "The page won't be visible before the start date.<br>After the finish date, the page won't be displayed (except possibly in an archive).",
                                               'name': 'date',
                                               'type': 'Field_Composite',
                                               'type_name': 'MOM.Date_Interval_N',
                                               'ui_name': u'Date'},
                                              {'$id': 'X-2:4:2',
                                               'description': 'Markup format used for `text`',
                                               'name': 'format',
                                               'type': 'Field',
                                               'ui_name': u'Format'},
                                              {'$id': 'X-2:4:3',
                                               'description': 'Head line of the web page',
                                               'name': 'head_line',
                                               'type': 'Field',
                                               'ui_name': u'Head line'},
                                              {'$id': 'X-2:4:4',
                                               'description': 'Higher prio sorts before lower prio.',
                                               'name': 'prio',
                                               'type': 'Field',
                                               'ui_name': u'Prio'}],
                                 'collapsed': True,
                                 'name': 'optional',
                                 'type': 'Fieldset'},
                                {'$id': 'X-2:5',
                                 'proto': {'$id': 'X-2:5::0',
                                           'children': [{'$id': 'X-2:5::0-1',
                                                         'children': [{'$id': 'X-2:5::0-1:1',
                                                                       'children': [{'$id': 'X-2:5::0-1:1.1',
                                                                                     'description': 'Start date of interval',
                                                                                     'name': 'start',
                                                                                     'type': 'Field',
                                                                                     'ui_name': u'Start'},
                                                                                    {'$id': 'X-2:5::0-1:1.2',
                                                                                     'description': 'Finish date of interval',
                                                                                     'name': 'finish',
                                                                                     'type': 'Field',
                                                                                     'ui_name': u'Finish'}],
                                                                       'description': 'Date interval of event (for non-recurring events, only `start` is relevant)',
                                                                       'name': 'date',
                                                                       'type': 'Field_Composite',
                                                                       'type_name': 'MOM.Date_Interval',
                                                                       'ui_name': u'Date'},
                                                                      {'$id': 'X-2:5::0-1:2',
                                                                       'children': [{'$id': 'X-2:5::0-1:2.1',
                                                                                     'description': 'Start time of interval',
                                                                                     'name': 'start',
                                                                                     'type': 'Field',
                                                                                     'ui_name': u'Start'},
                                                                                    {'$id': 'X-2:5::0-1:2.2',
                                                                                     'description': 'Finish time of interval',
                                                                                     'name': 'finish',
                                                                                     'type': 'Field',
                                                                                     'ui_name': u'Finish'}],
                                                                       'description': 'Time interval of event (for a full-day event, this is empty)',
                                                                       'name': 'time',
                                                                       'type': 'Field_Composite',
                                                                       'type_name': 'MOM.Time_Interval',
                                                                       'ui_name': u'Time'}],
                                                         'collapsed': False,
                                                         'name': 'primary',
                                                         'type': 'Fieldset'},
                                                        {'$id': 'X-2:5::0-2',
                                                         'children': [{'$id': 'X-2:5::0-2:1',
                                                                       'description': 'Information about event.',
                                                                       'name': 'detail',
                                                                       'type': 'Field',
                                                                       'ui_name': u'Detail'},
                                                                      {'$id': 'X-2:5::0-2:2',
                                                                       'description': u'Models a string-valued attribute of an object.',
                                                                       'name': 'short_title',
                                                                       'type': 'Field',
                                                                       'ui_name': u'Short title'}],
                                                         'collapsed': True,
                                                         'name': 'optional',
                                                         'type': 'Fieldset'},
                                                        {'$id': 'X-2:5::0-3',
                                                         'children': [{'$id': 'X-2:5::0-3:1',
                                                                       'children': [{'$id': 'X-2:5::0-3:1:1',
                                                                                     'description': 'Dates included in the recurrence rule set.',
                                                                                     'name': 'dates',
                                                                                     'type': 'Field',
                                                                                     'ui_name': u'Dates'},
                                                                                    {'$id': 'X-2:5::0-3:1:2',
                                                                                     'description': 'Dates excluded from the recurrence rule set.',
                                                                                     'name': 'date_exceptions',
                                                                                     'type': 'Field',
                                                                                     'ui_name': u'Date exceptions'}],
                                                                       'collapsed': True,
                                                                       'name': 'optional',
                                                                       'type': 'Fieldset'},
                                                                      {'$id': 'X-2:5::0-3:2',
                                                                       'proto': {'$id': 'X-2:5::0-3:2::0',
                                                                                 'children': [{'$id': 'X-2:5::0-3:2::0-1',
                                                                                               'children': [{'$id': 'X-2:5::0-3:2::0-1:1',
                                                                                                             'description': 'If true, exclude the dates specified by this rule.',
                                                                                                             'name': 'is_exception',
                                                                                                             'type': 'Field',
                                                                                                             'ui_name': u'Is exception'},
                                                                                                            {'$id': 'X-2:5::0-3:2::0-1:2',
                                                                                                             'description': 'Short description of the rule',
                                                                                                             'name': 'desc',
                                                                                                             'type': 'Field',
                                                                                                             'ui_name': 'Description'}],
                                                                                               'collapsed': False,
                                                                                               'name': 'primary',
                                                                                               'type': 'Fieldset'},
                                                                                              {'$id': 'X-2:5::0-3:2::0-2',
                                                                                               'children': [{'$id': 'X-2:5::0-3:2::0-2:1',
                                                                                                             'description': 'Start date of the recurrence.',
                                                                                                             'name': 'start',
                                                                                                             'type': 'Field',
                                                                                                             'ui_name': u'Start'},
                                                                                                            {'$id': 'X-2:5::0-3:2::0-2:2',
                                                                                                             'description': 'Finish date of the recurrence.',
                                                                                                             'name': 'finish',
                                                                                                             'type': 'Field',
                                                                                                             'ui_name': u'Finish'},
                                                                                                            {'$id': 'X-2:5::0-3:2::0-2:3',
                                                                                                             'description': 'The interval (measured in `units`) between successive recurrences of an event.',
                                                                                                             'name': 'period',
                                                                                                             'type': 'Field',
                                                                                                             'ui_name': u'Period'},
                                                                                                            {'$id': 'X-2:5::0-3:2::0-2:4',
                                                                                                             'description': 'Unit of recurrence. `period` is interpreted in units of `unit`.',
                                                                                                             'name': 'unit',
                                                                                                             'type': 'Field',
                                                                                                             'ui_name': u'Unit'},
                                                                                                            {'$id': 'X-2:5::0-3:2::0-2:5',
                                                                                                             'description': 'Restrict the recurrences to the days of the week specified. (0 means monday, 6 means sunday).',
                                                                                                             'name': 'week_day',
                                                                                                             'type': 'Field',
                                                                                                             'ui_name': u'Week day'},
                                                                                                            {'$id': 'X-2:5::0-3:2::0-2:6',
                                                                                                             'description': 'Maximum number of recurrences.',
                                                                                                             'name': 'count',
                                                                                                             'type': 'Field',
                                                                                                             'ui_name': u'Count'},
                                                                                                            {'$id': 'X-2:5::0-3:2::0-2:7',
                                                                                                             'description': 'Restrict recurrences to the numbers given. Negative numbers count from the last occurrence (-1 meaning the last occurrence).',
                                                                                                             'name': 'restrict_pos',
                                                                                                             'type': 'Field',
                                                                                                             'ui_name': u'Restrict pos'},
                                                                                                            {'$id': 'X-2:5::0-3:2::0-2:8',
                                                                                                             'description': 'Restrict the recurrences to the days of the month specified. Negative numbers count from the end of the month (-1 means the last day of the month).',
                                                                                                             'name': 'month_day',
                                                                                                             'type': 'Field',
                                                                                                             'ui_name': u'Month day'},
                                                                                                            {'$id': 'X-2:5::0-3:2::0-2:9',
                                                                                                             'description': 'Restrict the recurrences to the months specified (1 means January, ...).',
                                                                                                             'name': 'month',
                                                                                                             'type': 'Field',
                                                                                                             'ui_name': u'Month'},
                                                                                                            {'$id': 'X-2:5::0-3:2::0-2:10',
                                                                                                             'description': 'Restrict the recurrences to the week numbers specified.',
                                                                                                             'name': 'week',
                                                                                                             'type': 'Field',
                                                                                                             'ui_name': u'Week'},
                                                                                                            {'$id': 'X-2:5::0-3:2::0-2:11',
                                                                                                             'description': 'Restrict the recurrences to the days of the year specified. Negative numbers count from the end of the year (-1 means the last day of the year).',
                                                                                                             'name': 'year_day',
                                                                                                             'type': 'Field',
                                                                                                             'ui_name': u'Year day'},
                                                                                                            {'$id': 'X-2:5::0-3:2::0-2:12',
                                                                                                             'description': 'Offset to Easter sunday (positive or negative, 0 means the Easter sunday itself).',
                                                                                                             'name': 'easter_offset',
                                                                                                             'type': 'Field',
                                                                                                             'ui_name': u'Easter offset'}],
                                                                                               'collapsed': True,
                                                                                               'name': 'optional',
                                                                                               'type': 'Fieldset'}],
                                                                                 'name': 'GTW.OMP.EVT.Recurrence_Rule',
                                                                                 'role_name': 'left',
                                                                                 'type': 'Entity_Link',
                                                                                 'type_name': 'GTW.OMP.EVT.Recurrence_Rule'},
                                                                       'type': 'Entity_List'}],
                                                         'name': 'GTW.OMP.EVT.Recurrence_Spec',
                                                         'role_name': 'left',
                                                         'type': 'Entity_Link',
                                                         'type_name': 'GTW.OMP.EVT.Recurrence_Spec'}],
                                           'name': 'GTW.OMP.EVT.Event',
                                           'role_name': 'left',
                                           'type': 'Entity_Link',
                                           'type_name': 'GTW.OMP.EVT.Event'},
                                 'type': 'Entity_List'}],
                   'name': 'GTW.OMP.SWP.Page',
                   'type': 'Entity',
                   'type_name': 'GTW.OMP.SWP.Page'}],
     'type': 'Form'}

"""

from   _GTW.__test__.model import *
from   _GTW._AFS.Element   import Form

import pprint

__test__ = dict (AFS_Spec = _test_code)

### __END__ AFS_Spec
