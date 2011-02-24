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
      <Field_Composite None 'lifetime' 'MOM.Date_Interval'>
       <Field None 'start'>
       <Field None 'finish'>
      <Field None 'salutation'>

    >>> T = Spec.Entity (Spec.Entity_Link ("events",
    ...   Spec.Entity_Link ("recurrence", Spec.Entity_Link ("rules"))))
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
      <Field_Composite None 'date' 'MOM.Date_Interval_N'>
       <Field None 'start'>
       <Field None 'finish'>
      <Field None 'format'>
      <Field None 'head_line'>
      <Field None 'prio'>
     <Entity_List None <Entity_Link None 'GTW.OMP.EVT.Event'>>
      <Entity_Link None 'GTW.OMP.EVT.Event'>
       <Fieldset None 'primary'>
        <Field_Composite None 'date' 'MOM.Date_Interval'>
         <Field None 'start'>
         <Field None 'finish'>
        <Field_Composite None 'time' 'MOM.Time_Interval'>
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
       <Field_Composite F-1:4:1 'date' 'MOM.Date_Interval_N'>
        <Field F-1:4:1.1 'start'>
        <Field F-1:4:1.2 'finish'>
       <Field F-1:4:2 'format'>
       <Field F-1:4:3 'head_line'>
       <Field F-1:4:4 'prio'>
      <Entity_List F-1:5 <Entity_Link F-1:5::0 'GTW.OMP.EVT.Event'>>
       <Entity_Link F-1:5::0 'GTW.OMP.EVT.Event'>
        <Fieldset F-1:5::0-1 'primary'>
         <Field_Composite F-1:5::0-1:1 'date' 'MOM.Date_Interval'>
          <Field F-1:5::0-1:1.1 'start'>
          <Field F-1:5::0-1:1.2 'finish'>
         <Field_Composite F-1:5::0-1:2 'time' 'MOM.Time_Interval'>
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
       <Field_Composite X-1:3:1 'lifetime' 'MOM.Date_Interval'>
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
       <Field_Composite X-2:4:1 'date' 'MOM.Date_Interval_N'>
        <Field X-2:4:1.1 'start'>
        <Field X-2:4:1.2 'finish'>
       <Field X-2:4:2 'format'>
       <Field X-2:4:3 'head_line'>
       <Field X-2:4:4 'prio'>
      <Entity_List X-2:5 <Entity_Link X-2:5::0 'GTW.OMP.EVT.Event'>>
       <Entity_Link X-2:5::0 'GTW.OMP.EVT.Event'>
        <Fieldset X-2:5::0-1 'primary'>
         <Field_Composite X-2:5::0-1:1 'date' 'MOM.Date_Interval'>
          <Field X-2:5::0-1:1.1 'start'>
          <Field X-2:5::0-1:1.2 'finish'>
         <Field_Composite X-2:5::0-1:2 'time' 'MOM.Time_Interval'>
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
    >>> print formatted (f.as_json_cargo)
    { '$id' : 'X'
    , 'children' :
        [ { '$id' : 'X-1'
          , 'children' :
              [ { '$id' : 'X-1:1'
                , 'children' :
                    [ { '$id' : 'X-1:1:1'
                      , 'name' : 'last_name'
                      , 'type' : 'Field'
                      , 'ui_name' : u'Last name'
                      }
                    , { '$id' : 'X-1:1:2'
                      , 'name' : 'first_name'
                      , 'type' : 'Field'
                      , 'ui_name' : u'First name'
                      }
                    , { '$id' : 'X-1:1:3'
                      , 'name' : 'middle_name'
                      , 'type' : 'Field'
                      , 'ui_name' : u'Middle name'
                      }
                    , { '$id' : 'X-1:1:4'
                      , 'name' : 'title'
                      , 'type' : 'Field'
                      , 'ui_name' : u'Academic title'
                      }
                    ]
                , 'collapsed' : False
                , 'name' : 'primary'
                , 'type' : 'Fieldset'
                }
              , { '$id' : 'X-1:2'
                , 'children' :
                    [ { '$id' : 'X-1:2:1'
                      , 'name' : 'sex'
                      , 'type' : 'Field'
                      , 'ui_name' : u'Sex'
                      }
                    ]
                , 'collapsed' : True
                , 'name' : 'necessary'
                , 'type' : 'Fieldset'
                }
              , { '$id' : 'X-1:3'
                , 'children' :
                    [ { '$id' : 'X-1:3:1'
                      , 'children' :
                          [ { '$id' : 'X-1:3:1.1'
                            , 'name' : 'start'
                            , 'type' : 'Field'
                            , 'ui_name' : u'Start'
                            }
                          , { '$id' : 'X-1:3:1.2'
                            , 'name' : 'finish'
                            , 'type' : 'Field'
                            , 'ui_name' : u'Finish'
                            }
                          ]
                      , 'name' : 'lifetime'
                      , 'type' : 'Field_Composite'
                      , 'type_name' : 'MOM.Date_Interval'
                      , 'ui_name' : u'Lifetime'
                      }
                    , { '$id' : 'X-1:3:2'
                      , 'name' : 'salutation'
                      , 'type' : 'Field'
                      , 'ui_name' : u'Salutation'
                      }
                    ]
                , 'collapsed' : True
                , 'name' : 'optional'
                , 'type' : 'Fieldset'
                }
              ]
          , 'name' : 'GTW.OMP.PAP.Person'
          , 'type' : 'Entity'
          , 'type_name' : 'GTW.OMP.PAP.Person'
          }
        , { '$id' : 'X-2'
          , 'children' :
              [ { '$id' : 'X-2:1'
                , 'children' :
                    [ { '$id' : 'X-2:1:1'
                      , 'name' : 'perma_name'
                      , 'type' : 'Field'
                      , 'ui_name' : 'Name'
                      }
                    ]
                , 'collapsed' : False
                , 'name' : 'primary'
                , 'type' : 'Fieldset'
                }
              , { '$id' : 'X-2:2'
                , 'children' :
                    [ { '$id' : 'X-2:2:1'
                      , 'name' : 'text'
                      , 'type' : 'Field'
                      , 'ui_name' : u'Text'
                      }
                    ]
                , 'collapsed' : True
                , 'name' : 'required'
                , 'type' : 'Fieldset'
                }
              , { '$id' : 'X-2:3'
                , 'children' :
                    [ { '$id' : 'X-2:3:1'
                      , 'name' : 'short_title'
                      , 'type' : 'Field'
                      , 'ui_name' : u'Short title'
                      }
                    , { '$id' : 'X-2:3:2'
                      , 'name' : 'title'
                      , 'type' : 'Field'
                      , 'ui_name' : u'Title'
                      }
                    ]
                , 'collapsed' : True
                , 'name' : 'necessary'
                , 'type' : 'Fieldset'
                }
              , { '$id' : 'X-2:4'
                , 'children' :
                    [ { '$id' : 'X-2:4:1'
                      , 'children' :
                          [ { '$id' : 'X-2:4:1.1'
                            , 'name' : 'start'
                            , 'type' : 'Field'
                            , 'ui_name' : u'Start'
                            }
                          , { '$id' : 'X-2:4:1.2'
                            , 'name' : 'finish'
                            , 'type' : 'Field'
                            , 'ui_name' : u'Finish'
                            }
                          ]
                      , 'name' : 'date'
                      , 'type' : 'Field_Composite'
                      , 'type_name' : 'MOM.Date_Interval_N'
                      , 'ui_name' : u'Date'
                      }
                    , { '$id' : 'X-2:4:2'
                      , 'name' : 'format'
                      , 'type' : 'Field'
                      , 'ui_name' : u'Format'
                      }
                    , { '$id' : 'X-2:4:3'
                      , 'name' : 'head_line'
                      , 'type' : 'Field'
                      , 'ui_name' : u'Head line'
                      }
                    , { '$id' : 'X-2:4:4'
                      , 'name' : 'prio'
                      , 'type' : 'Field'
                      , 'ui_name' : u'Prio'
                      }
                    ]
                , 'collapsed' : True
                , 'name' : 'optional'
                , 'type' : 'Fieldset'
                }
              , { '$id' : 'X-2:5'
                , 'proto' : { '$id' : 'X-2:5::0'
                    , 'children' :
                        [ { '$id' : 'X-2:5::0-1'
                          , 'children' :
                              [ { '$id' : 'X-2:5::0-1:1'
                                , 'children' :
                                    [ { '$id' : 'X-2:5::0-1:1.1'
                                      , 'name' : 'start'
                                      , 'type' : 'Field'
                                      , 'ui_name' : u'Start'
                                      }
                                    , { '$id' : 'X-2:5::0-1:1.2'
                                      , 'name' : 'finish'
                                      , 'type' : 'Field'
                                      , 'ui_name' : u'Finish'
                                      }
                                    ]
                                , 'name' : 'date'
                                , 'type' : 'Field_Composite'
                                , 'type_name' : 'MOM.Date_Interval'
                                , 'ui_name' : u'Date'
                                }
                              , { '$id' : 'X-2:5::0-1:2'
                                , 'children' :
                                    [ { '$id' : 'X-2:5::0-1:2.1'
                                      , 'name' : 'start'
                                      , 'type' : 'Field'
                                      , 'ui_name' : u'Start'
                                      }
                                    , { '$id' : 'X-2:5::0-1:2.2'
                                      , 'name' : 'finish'
                                      , 'type' : 'Field'
                                      , 'ui_name' : u'Finish'
                                      }
                                    ]
                                , 'name' : 'time'
                                , 'type' : 'Field_Composite'
                                , 'type_name' : 'MOM.Time_Interval'
                                , 'ui_name' : u'Time'
                                }
                              ]
                          , 'collapsed' : False
                          , 'name' : 'primary'
                          , 'type' : 'Fieldset'
                          }
                        , { '$id' : 'X-2:5::0-2'
                          , 'children' :
                              [ { '$id' : 'X-2:5::0-2:1'
                                , 'name' : 'detail'
                                , 'type' : 'Field'
                                , 'ui_name' : u'Detail'
                                }
                              , { '$id' : 'X-2:5::0-2:2'
                                , 'name' : 'short_title'
                                , 'type' : 'Field'
                                , 'ui_name' : u'Short title'
                                }
                              ]
                          , 'collapsed' : True
                          , 'name' : 'optional'
                          , 'type' : 'Fieldset'
                          }
                        , { '$id' : 'X-2:5::0-3'
                          , 'children' :
                              [ { '$id' : 'X-2:5::0-3:1'
                                , 'children' :
                                    [ { '$id' : 'X-2:5::0-3:1:1'
                                      , 'name' : 'dates'
                                      , 'type' : 'Field'
                                      , 'ui_name' : u'Dates'
                                      }
                                    , { '$id' : 'X-2:5::0-3:1:2'
                                      , 'name' : 'date_exceptions'
                                      , 'type' : 'Field'
                                      , 'ui_name' : u'Date exceptions'
                                      }
                                    ]
                                , 'collapsed' : True
                                , 'name' : 'optional'
                                , 'type' : 'Fieldset'
                                }
                              , { '$id' : 'X-2:5::0-3:2'
                                , 'proto' : { '$id' : 'X-2:5::0-3:2::0'
                                    , 'children' :
                                        [ { '$id' : 'X-2:5::0-3:2::0-1'
                                          , 'children' :
                                              [ { '$id' : 'X-2:5::0-3:2::0-1:1'
                                                , 'name' : 'is_exception'
                                                , 'type' : 'Field'
                                                , 'ui_name' : u'Is exception'
                                                }
                                              , { '$id' : 'X-2:5::0-3:2::0-1:2'
                                                , 'name' : 'desc'
                                                , 'type' : 'Field'
                                                , 'ui_name' : 'Description'
                                                }
                                              ]
                                          , 'collapsed' : False
                                          , 'name' : 'primary'
                                          , 'type' : 'Fieldset'
                                          }
                                        , { '$id' : 'X-2:5::0-3:2::0-2'
                                          , 'children' :
                                              [ { '$id' : 'X-2:5::0-3:2::0-2:1'
                                                , 'name' : 'start'
                                                , 'type' : 'Field'
                                                , 'ui_name' : u'Start'
                                                }
                                              , { '$id' : 'X-2:5::0-3:2::0-2:2'
                                                , 'name' : 'finish'
                                                , 'type' : 'Field'
                                                , 'ui_name' : u'Finish'
                                                }
                                              , { '$id' : 'X-2:5::0-3:2::0-2:3'
                                                , 'name' : 'period'
                                                , 'type' : 'Field'
                                                , 'ui_name' : u'Period'
                                                }
                                              , { '$id' : 'X-2:5::0-3:2::0-2:4'
                                                , 'name' : 'unit'
                                                , 'type' : 'Field'
                                                , 'ui_name' : u'Unit'
                                                }
                                              , { '$id' : 'X-2:5::0-3:2::0-2:5'
                                                , 'name' : 'week_day'
                                                , 'type' : 'Field'
                                                , 'ui_name' : u'Week day'
                                                }
                                              , { '$id' : 'X-2:5::0-3:2::0-2:6'
                                                , 'name' : 'count'
                                                , 'type' : 'Field'
                                                , 'ui_name' : u'Count'
                                                }
                                              , { '$id' : 'X-2:5::0-3:2::0-2:7'
                                                , 'name' : 'restrict_pos'
                                                , 'type' : 'Field'
                                                , 'ui_name' : u'Restrict pos'
                                                }
                                              , { '$id' : 'X-2:5::0-3:2::0-2:8'
                                                , 'name' : 'month_day'
                                                , 'type' : 'Field'
                                                , 'ui_name' : u'Month day'
                                                }
                                              , { '$id' : 'X-2:5::0-3:2::0-2:9'
                                                , 'name' : 'month'
                                                , 'type' : 'Field'
                                                , 'ui_name' : u'Month'
                                                }
                                              , { '$id' : 'X-2:5::0-3:2::0-2:10'
                                                , 'name' : 'week'
                                                , 'type' : 'Field'
                                                , 'ui_name' : u'Week'
                                                }
                                              , { '$id' : 'X-2:5::0-3:2::0-2:11'
                                                , 'name' : 'year_day'
                                                , 'type' : 'Field'
                                                , 'ui_name' : u'Year day'
                                                }
                                              , { '$id' : 'X-2:5::0-3:2::0-2:12'
                                                , 'name' : 'easter_offset'
                                                , 'type' : 'Field'
                                                , 'ui_name' : u'Easter offset'
                                                }
                                              ]
                                          , 'collapsed' : True
                                          , 'name' : 'optional'
                                          , 'type' : 'Fieldset'
                                          }
                                        ]
                                    , 'name' : 'GTW.OMP.EVT.Recurrence_Rule'
                                    , 'role_name' : 'left'
                                    , 'type' : 'Entity_Link'
                                    , 'type_name' : 'GTW.OMP.EVT.Recurrence_Rule'
                                    }
                                , 'type' : 'Entity_List'
                                }
                              ]
                          , 'name' : 'GTW.OMP.EVT.Recurrence_Spec'
                          , 'role_name' : 'left'
                          , 'type' : 'Entity_Link'
                          , 'type_name' : 'GTW.OMP.EVT.Recurrence_Spec'
                          }
                        ]
                    , 'name' : 'GTW.OMP.EVT.Event'
                    , 'role_name' : 'left'
                    , 'type' : 'Entity_Link'
                    , 'type_name' : 'GTW.OMP.EVT.Event'
                    }
                , 'type' : 'Entity_List'
                }
              ]
          , 'name' : 'GTW.OMP.SWP.Page'
          , 'type' : 'Entity'
          , 'type_name' : 'GTW.OMP.SWP.Page'
          }
        ]
    , 'type' : 'Form'
    }
    >>> SB = Spec.Entity (Spec.Entity_Link ("GTW.OMP.SRM.Boat_in_Regatta"))
    >>> fb = Form ("FB", children = [SB (scope.SRM.Boat)])
    >>> print repr (fb)
    <Form FB>
     <Entity FB-1 'GTW.OMP.SRM.Boat'>
      <Fieldset FB-1:1 'primary'>
       <Field_Entity FB-1:1:1 'left' 'GTW.OMP.SRM.Boat_Class'>
        <Field FB-1:1:1:1 'name'>
       <Field FB-1:1:2 'nation'>
       <Field FB-1:1:3 'sail_number'>
      <Fieldset FB-1:2 'optional'>
       <Field FB-1:2:1 'name'>
      <Entity_List FB-1:3 <Entity_Link FB-1:3::0 'GTW.OMP.SRM.Boat_in_Regatta'>>
       <Entity_Link FB-1:3::0 'GTW.OMP.SRM.Boat_in_Regatta'>
        <Fieldset FB-1:3::0-1 'primary'>
         <Field_Entity FB-1:3::0-1:1 'right' 'GTW.OMP.SRM.Regatta'>
          <Field_Entity FB-1:3::0-1:1:1 'left' 'GTW.OMP.SRM.Regatta_Event'>
           <Field_Composite FB-1:3::0-1:1:1:1 'date' 'MOM.Date_Interval_C'>
            <Field FB-1:3::0-1:1:1:1.1 'start'>
            <Field FB-1:3::0-1:1:1:1.2 'finish'>
           <Field FB-1:3::0-1:1:1:2 'name'>
        <Fieldset FB-1:3::0-2 'required'>
         <Field_Entity FB-1:3::0-2:1 'skipper' 'GTW.OMP.SRM.Sailor'>
          <Field_Entity FB-1:3::0-2:1:1 'left' 'GTW.OMP.PAP.Person'>
           <Field FB-1:3::0-2:1:1:1 'last_name'>
           <Field FB-1:3::0-2:1:1:2 'first_name'>
           <Field FB-1:3::0-2:1:1:3 'middle_name'>
           <Field FB-1:3::0-2:1:1:4 'title'>
          <Field FB-1:3::0-2:1:2 'nation'>
          <Field FB-1:3::0-2:1:3 'mna_number'>
        <Fieldset FB-1:3::0-3 'optional'>
         <Field FB-1:3::0-3:1 'place'>
         <Field FB-1:3::0-3:2 'points'>

    >>> PAP = scope.PAP
    >>> SRM = scope.SRM
    >>> bc  = SRM.Boat_Class ("Optimist", max_crew = 1)
    >>> b   = SRM.Boat.instance_or_new (u'Optimist', u"AUT", u"1107", raw = True)
    >>> p   = PAP.Person.instance_or_new (u"Tanzer", u"Laurens")
    >>> s   = SRM.Sailor.instance_or_new (p, nation = u"AUT", mna_number = u"29676", raw = True)
    >>> rev = SRM.Regatta_Event (dict (start = u"20080501", raw = True), u"Himmelfahrt", raw = True)
    >>> reg = SRM.Regatta_C (rev, boat_class = bc)
    >>> bir = SRM.Boat_in_Regatta (b, reg, skipper = s)
    >>> scope.commit ()
    >>> print formatted (fb (SRM.Boat, b))
    { 'FB-1' :
        { 'FB-1:1' :
            { 'FB-1:1:1' :
                { 'FB-1:1:1:1' :
                    { 'init' : u'Optimist'
                    }
                , 'cid' : None
                , 'pid' : 1
                }
            , 'FB-1:1:2' :
                { 'init' : u'AUT'
                }
            , 'FB-1:1:3' :
                { 'init' : u'1107'
                }
            }
        , 'FB-1:2' :
            { 'FB-1:2:1' :
                { 'init' : u''
                }
            }
        , 'FB-1:3' :
            { 'FB-1:3::1' :
                { 'FB-1:3::1:1' :
                    { 'FB-1:3::1:1:1' :
                        { 'FB-1:3::1:1:1:1' :
                            { 'FB-1:3::1:1:1:1:1' :
                                { 'FB-1:3::1:1:1:1:1.1' :
                                    { 'init' : '2008/05/01'
                                    }
                                , 'FB-1:3::1:1:1:1:1.2' :
                                    { 'init' : '2008/05/01'
                                    }
                                }
                            , 'FB-1:3::1:1:1:1:2' :
                                { 'init' : u'Himmelfahrt'
                                }
                            , 'cid' : None
                            , 'pid' : 5
                            }
                        , 'cid' : None
                        , 'pid' : 6
                        }
                    }
                , 'FB-1:3::1:2' :
                    { 'FB-1:3::1:2:1' :
                        { 'FB-1:3::1:2:1:1' :
                            { 'FB-1:3::1:2:1:1:1' :
                                { 'init' : u'Tanzer'
                                }
                            , 'FB-1:3::1:2:1:1:2' :
                                { 'init' : u'Laurens'
                                }
                            , 'FB-1:3::1:2:1:1:3' :
                                { 'init' : u''
                                }
                            , 'FB-1:3::1:2:1:1:4' :
                                { 'init' : u''
                                }
                            , 'cid' : None
                            , 'pid' : 3
                            }
                        , 'FB-1:3::1:2:1:2' :
                            { 'init' : u'AUT'
                            }
                        , 'FB-1:3::1:2:1:3' :
                            { 'init' : u'29676'
                            }
                        , 'cid' : None
                        , 'pid' : 4
                        }
                    }
                , 'FB-1:3::1:3' :
                    { 'FB-1:3::1:3:1' :
                        { 'init' : u''
                        }
                    , 'FB-1:3::1:3:2' :
                        { 'init' : u''
                        }
                    }
                , 'cid' : None
                , 'pid' : 7
                }
            }
        , 'cid' : None
        , 'pid' : 2
        }
    }

"""

from   _GTW.__test__.model      import *
from   _GTW._AFS._MOM.Element   import Form

from   _TFL.Formatter      import formatted

__test__ = dict (AFS_Spec = _test_code)

### __END__ AFS_Spec
