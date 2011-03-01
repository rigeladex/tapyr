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
     <Entity F-0 'GTW.OMP.SWP.Page'>
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
       <Field F-0:3:3 'prio'>
      <Entity_List F-0:4 <Entity_Link F-0:4::p 'GTW.OMP.EVT.Event'>>
       <Entity_Link F-0:4::p 'GTW.OMP.EVT.Event'>
        <Fieldset F-0:4::p-0 'primary'>
         <Field_Composite F-0:4::p-0:0 'date' 'MOM.Date_Interval'>
          <Field F-0:4::p-0:0.0 'start'>
          <Field F-0:4::p-0:0.1 'finish'>
         <Field_Composite F-0:4::p-0:1 'time' 'MOM.Time_Interval'>
          <Field F-0:4::p-0:1.0 'start'>
          <Field F-0:4::p-0:1.1 'finish'>
        <Fieldset F-0:4::p-1 'optional'>
         <Field F-0:4::p-1:0 'detail'>
         <Field F-0:4::p-1:1 'short_title'>
        <Entity_Link F-0:4::p-2 'GTW.OMP.EVT.Recurrence_Spec'>
         <Fieldset F-0:4::p-2:0 'optional'>
          <Field F-0:4::p-2:0:0 'dates'>
          <Field F-0:4::p-2:0:1 'date_exceptions'>
         <Entity_List F-0:4::p-2:1 <Entity_Link F-0:4::p-2:1::p 'GTW.OMP.EVT.Recurrence_Rule'>>
          <Entity_Link F-0:4::p-2:1::p 'GTW.OMP.EVT.Recurrence_Rule'>
           <Fieldset F-0:4::p-2:1::p-0 'primary'>
            <Field F-0:4::p-2:1::p-0:0 'is_exception'>
            <Field F-0:4::p-2:1::p-0:1 'desc'>
           <Fieldset F-0:4::p-2:1::p-1 'optional'>
            <Field F-0:4::p-2:1::p-1:0 'start'>
            <Field F-0:4::p-2:1::p-1:1 'finish'>
            <Field F-0:4::p-2:1::p-1:2 'period'>
            <Field F-0:4::p-2:1::p-1:3 'unit'>
            <Field F-0:4::p-2:1::p-1:4 'week_day'>
            <Field F-0:4::p-2:1::p-1:5 'count'>
            <Field F-0:4::p-2:1::p-1:6 'restrict_pos'>
            <Field F-0:4::p-2:1::p-1:7 'month_day'>
            <Field F-0:4::p-2:1::p-1:8 'month'>
            <Field F-0:4::p-2:1::p-1:9 'week'>
            <Field F-0:4::p-2:1::p-1:10 'year_day'>
            <Field F-0:4::p-2:1::p-1:11 'easter_offset'>

    >>> f = Form ("X", children = [x, y])
    >>> print repr (f)
    <Form X>
     <Entity X-0 'GTW.OMP.PAP.Person'>
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
     <Entity X-1 'GTW.OMP.SWP.Page'>
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
       <Field X-1:3:3 'prio'>
      <Entity_List X-1:4 <Entity_Link X-1:4::p 'GTW.OMP.EVT.Event'>>
       <Entity_Link X-1:4::p 'GTW.OMP.EVT.Event'>
        <Fieldset X-1:4::p-0 'primary'>
         <Field_Composite X-1:4::p-0:0 'date' 'MOM.Date_Interval'>
          <Field X-1:4::p-0:0.0 'start'>
          <Field X-1:4::p-0:0.1 'finish'>
         <Field_Composite X-1:4::p-0:1 'time' 'MOM.Time_Interval'>
          <Field X-1:4::p-0:1.0 'start'>
          <Field X-1:4::p-0:1.1 'finish'>
        <Fieldset X-1:4::p-1 'optional'>
         <Field X-1:4::p-1:0 'detail'>
         <Field X-1:4::p-1:1 'short_title'>
        <Entity_Link X-1:4::p-2 'GTW.OMP.EVT.Recurrence_Spec'>
         <Fieldset X-1:4::p-2:0 'optional'>
          <Field X-1:4::p-2:0:0 'dates'>
          <Field X-1:4::p-2:0:1 'date_exceptions'>
         <Entity_List X-1:4::p-2:1 <Entity_Link X-1:4::p-2:1::p 'GTW.OMP.EVT.Recurrence_Rule'>>
          <Entity_Link X-1:4::p-2:1::p 'GTW.OMP.EVT.Recurrence_Rule'>
           <Fieldset X-1:4::p-2:1::p-0 'primary'>
            <Field X-1:4::p-2:1::p-0:0 'is_exception'>
            <Field X-1:4::p-2:1::p-0:1 'desc'>
           <Fieldset X-1:4::p-2:1::p-1 'optional'>
            <Field X-1:4::p-2:1::p-1:0 'start'>
            <Field X-1:4::p-2:1::p-1:1 'finish'>
            <Field X-1:4::p-2:1::p-1:2 'period'>
            <Field X-1:4::p-2:1::p-1:3 'unit'>
            <Field X-1:4::p-2:1::p-1:4 'week_day'>
            <Field X-1:4::p-2:1::p-1:5 'count'>
            <Field X-1:4::p-2:1::p-1:6 'restrict_pos'>
            <Field X-1:4::p-2:1::p-1:7 'month_day'>
            <Field X-1:4::p-2:1::p-1:8 'month'>
            <Field X-1:4::p-2:1::p-1:9 'week'>
            <Field X-1:4::p-2:1::p-1:10 'year_day'>
            <Field X-1:4::p-2:1::p-1:11 'easter_offset'>


    >>> SB = Spec.Entity (Spec.Entity_Link ("GTW.OMP.SRM.Boat_in_Regatta"))
    >>> fb = Form ("FB", children = [SB (scope.SRM.Boat)])
    >>> print repr (fb)
    <Form FB>
     <Entity FB-0 'GTW.OMP.SRM.Boat'>
      <Fieldset FB-0:0 'primary'>
       <Field_Entity FB-0:0:0 'left' 'GTW.OMP.SRM.Boat_Class'>
        <Field FB-0:0:0:0 'name'>
       <Field FB-0:0:1 'nation'>
       <Field FB-0:0:2 'sail_number'>
      <Fieldset FB-0:1 'optional'>
       <Field FB-0:1:0 'name'>
      <Entity_List FB-0:2 <Entity_Link FB-0:2::p 'GTW.OMP.SRM.Boat_in_Regatta'>>
       <Entity_Link FB-0:2::p 'GTW.OMP.SRM.Boat_in_Regatta'>
        <Fieldset FB-0:2::p-0 'primary'>
         <Field_Entity FB-0:2::p-0:0 'right' 'GTW.OMP.SRM.Regatta'>
          <Field_Entity FB-0:2::p-0:0:0 'left' 'GTW.OMP.SRM.Regatta_Event'>
           <Field_Composite FB-0:2::p-0:0:0:0 'date' 'MOM.Date_Interval_C'>
            <Field FB-0:2::p-0:0:0:0.0 'start'>
            <Field FB-0:2::p-0:0:0:0.1 'finish'>
           <Field FB-0:2::p-0:0:0:1 'name'>
        <Fieldset FB-0:2::p-1 'required'>
         <Field_Entity FB-0:2::p-1:0 'skipper' 'GTW.OMP.SRM.Sailor'>
          <Field_Entity FB-0:2::p-1:0:0 'left' 'GTW.OMP.PAP.Person'>
           <Field FB-0:2::p-1:0:0:0 'last_name'>
           <Field FB-0:2::p-1:0:0:1 'first_name'>
           <Field FB-0:2::p-1:0:0:2 'middle_name'>
           <Field FB-0:2::p-1:0:0:3 'title'>
          <Field FB-0:2::p-1:0:1 'nation'>
          <Field FB-0:2::p-1:0:2 'mna_number'>
        <Fieldset FB-0:2::p-2 'optional'>
         <Field FB-0:2::p-2:0 'place'>
         <Field FB-0:2::p-2:1 'points'>

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
    >>> print formatted (fi.as_json_cargo, level = 1)
      { '$id' : 'FB'
      , 'children' :
          [ { '$id' : 'FB-0'
            , 'children' :
                [ { '$id' : 'FB-0:0'
                  , 'children' :
                      [ { '$id' : 'FB-0:0:0'
                        , 'children' :
                            [ { '$id' : 'FB-0:0:0:0'
                              , 'name' : 'name'
                              , 'type' : 'Field'
                              , 'ui_name' : 'Name'
                              , 'value' :
                                  { 'init' : 'Optimist' }
                              }
                            ]
                        , 'name' : 'left'
                        , 'type' : 'Field_Entity'
                        , 'type_name' : 'GTW.OMP.SRM.Boat_Class'
                        , 'ui_name' : 'Class'
                        , 'value' :
                            { 'init' :
                                { 'cid' : 1
                                , 'pid' : 1
                                }
                            }
                        }
                      , { '$id' : 'FB-0:0:1'
                        , 'name' : 'nation'
                        , 'type' : 'Field'
                        , 'ui_name' : 'Nation'
                        , 'value' :
                            { 'init' : 'AUT' }
                        }
                      , { '$id' : 'FB-0:0:2'
                        , 'name' : 'sail_number'
                        , 'type' : 'Field'
                        , 'ui_name' : 'Sail number'
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
                        , 'name' : 'name'
                        , 'type' : 'Field'
                        , 'ui_name' : 'Name'
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
                              , 'children' :
                                  [ { '$id' : 'FB-0:2::0-0:0'
                                    , 'children' :
                                        [ { '$id' : 'FB-0:2::0-0:0:0'
                                          , 'children' :
                                              [ { '$id' : 'FB-0:2::0-0:0:0:0'
                                                , 'children' :
                                                    [ { '$id' : 'FB-0:2::0-0:0:0:0.0'
                                                      , 'name' : 'start'
                                                      , 'type' : 'Field'
                                                      , 'ui_name' : 'Start'
                                                      , 'value' :
                                                          { 'init' : '2008/05/01' }
                                                      }
                                                    , { '$id' : 'FB-0:2::0-0:0:0:0.1'
                                                      , 'name' : 'finish'
                                                      , 'type' : 'Field'
                                                      , 'ui_name' : 'Finish'
                                                      , 'value' :
                                                          { 'init' : '2008/05/01' }
                                                      }
                                                    ]
                                                , 'name' : 'date'
                                                , 'type' : 'Field_Composite'
                                                , 'type_name' : 'MOM.Date_Interval_C'
                                                , 'ui_name' : 'Date'
                                                , 'value' :
                                                    {}
                                                }
                                              , { '$id' : 'FB-0:2::0-0:0:0:1'
                                                , 'name' : 'name'
                                                , 'type' : 'Field'
                                                , 'ui_name' : 'Name'
                                                , 'value' :
                                                    { 'init' : 'Himmelfahrt' }
                                                }
                                              ]
                                          , 'name' : 'left'
                                          , 'type' : 'Field_Entity'
                                          , 'type_name' : 'GTW.OMP.SRM.Regatta_Event'
                                          , 'ui_name' : 'Event'
                                          , 'value' :
                                              { 'init' :
                                                  { 'cid' : 5
                                                  , 'pid' : 5
                                                  }
                                              }
                                          }
                                        ]
                                    , 'name' : 'right'
                                    , 'type' : 'Field_Entity'
                                    , 'type_name' : 'GTW.OMP.SRM.Regatta'
                                    , 'ui_name' : 'Regatta'
                                    , 'value' :
                                        { 'init' :
                                            { 'cid' : 6
                                            , 'pid' : 6
                                            }
                                        }
                                    }
                                  ]
                              , 'collapsed' : False
                              , 'name' : 'primary'
                              , 'type' : 'Fieldset'
                              }
                            , { '$id' : 'FB-0:2::0-1'
                              , 'children' :
                                  [ { '$id' : 'FB-0:2::0-1:0'
                                    , 'children' :
                                        [ { '$id' : 'FB-0:2::0-1:0:0'
                                          , 'children' :
                                              [ { '$id' : 'FB-0:2::0-1:0:0:0'
                                                , 'name' : 'last_name'
                                                , 'type' : 'Field'
                                                , 'ui_name' : 'Last name'
                                                , 'value' :
                                                    { 'init' : 'Tanzer' }
                                                }
                                              , { '$id' : 'FB-0:2::0-1:0:0:1'
                                                , 'name' : 'first_name'
                                                , 'type' : 'Field'
                                                , 'ui_name' : 'First name'
                                                , 'value' :
                                                    { 'init' : 'Laurens' }
                                                }
                                              , { '$id' : 'FB-0:2::0-1:0:0:2'
                                                , 'name' : 'middle_name'
                                                , 'type' : 'Field'
                                                , 'ui_name' : 'Middle name'
                                                , 'value' :
                                                    {}
                                                }
                                              , { '$id' : 'FB-0:2::0-1:0:0:3'
                                                , 'name' : 'title'
                                                , 'type' : 'Field'
                                                , 'ui_name' : 'Academic title'
                                                , 'value' :
                                                    {}
                                                }
                                              ]
                                          , 'name' : 'left'
                                          , 'type' : 'Field_Entity'
                                          , 'type_name' : 'GTW.OMP.PAP.Person'
                                          , 'ui_name' : 'Person'
                                          , 'value' :
                                              { 'init' :
                                                  { 'cid' : 3
                                                  , 'pid' : 3
                                                  }
                                              }
                                          }
                                        , { '$id' : 'FB-0:2::0-1:0:1'
                                          , 'name' : 'nation'
                                          , 'type' : 'Field'
                                          , 'ui_name' : 'Nation'
                                          , 'value' :
                                              { 'init' : 'AUT' }
                                          }
                                        , { '$id' : 'FB-0:2::0-1:0:2'
                                          , 'name' : 'mna_number'
                                          , 'type' : 'Field'
                                          , 'ui_name' : 'Mna number'
                                          , 'value' :
                                              { 'init' : '29676' }
                                          }
                                        ]
                                    , 'name' : 'skipper'
                                    , 'type' : 'Field_Entity'
                                    , 'type_name' : 'GTW.OMP.SRM.Sailor'
                                    , 'ui_name' : 'Skipper'
                                    , 'value' :
                                        { 'init' :
                                            { 'cid' : 4
                                            , 'pid' : 4
                                            }
                                        }
                                    }
                                  ]
                              , 'collapsed' : True
                              , 'name' : 'required'
                              , 'type' : 'Fieldset'
                              }
                            , { '$id' : 'FB-0:2::0-2'
                              , 'children' :
                                  [ { '$id' : 'FB-0:2::0-2:0'
                                    , 'name' : 'place'
                                    , 'type' : 'Field'
                                    , 'ui_name' : 'Place'
                                    , 'value' :
                                        {}
                                    }
                                  , { '$id' : 'FB-0:2::0-2:1'
                                    , 'name' : 'points'
                                    , 'type' : 'Field'
                                    , 'ui_name' : 'Points'
                                    , 'value' :
                                        {}
                                    }
                                  ]
                              , 'collapsed' : True
                              , 'name' : 'optional'
                              , 'type' : 'Fieldset'
                              }
                            ]
                        , 'name' : 'GTW.OMP.SRM.Boat_in_Regatta'
                        , 'role_name' : 'left'
                        , 'type' : 'Entity_Link'
                        , 'type_name' : 'GTW.OMP.SRM.Boat_in_Regatta'
                        , 'value' :
                            { 'init' :
                                { 'cid' : 7
                                , 'pid' : 7
                                }
                            }
                        }
                      ]
                  , 'type' : 'Entity_List'
                  }
                ]
            , 'name' : 'GTW.OMP.SRM.Boat'
            , 'type' : 'Entity'
            , 'type_name' : 'GTW.OMP.SRM.Boat'
            , 'value' :
                { 'init' :
                    { 'cid' : 2
                    , 'pid' : 2
                    }
                }
            }
          ]
      , 'type' : 'Form'
      }

    >>> print "var f =", fi.as_js, ";"
    var f = new $GTW.AFS.Form ({"$id": "FB", "type": "Form", "children": [{"name": "GTW.OMP.SRM.Boat", "$id": "FB-0", "type_name": "GTW.OMP.SRM.Boat", "value": {"init": {"pid": 2, "cid": 2}}, "type": "Entity", "children": [{"$id": "FB-0:0", "collapsed": false, "type": "Fieldset", "name": "primary", "children": [{"name": "left", "$id": "FB-0:0:0", "type_name": "GTW.OMP.SRM.Boat_Class", "value": {"init": {"pid": 1, "cid": 1}}, "ui_name": "Class", "type": "Field_Entity", "children": [{"$id": "FB-0:0:0:0", "ui_name": "Name", "type": "Field", "name": "name", "value": {"init": "Optimist"}}]}, {"$id": "FB-0:0:1", "ui_name": "Nation", "type": "Field", "name": "nation", "value": {"init": "AUT"}}, {"$id": "FB-0:0:2", "ui_name": "Sail number", "type": "Field", "name": "sail_number", "value": {"init": "1107"}}]}, {"$id": "FB-0:1", "collapsed": true, "type": "Fieldset", "name": "optional", "children": [{"$id": "FB-0:1:0", "ui_name": "Name", "type": "Field", "name": "name", "value": {}}]}, {"$id": "FB-0:2", "type": "Entity_List", "children": [{"name": "GTW.OMP.SRM.Boat_in_Regatta", "$id": "FB-0:2::0", "type_name": "GTW.OMP.SRM.Boat_in_Regatta", "value": {"init": {"pid": 7, "cid": 7}}, "role_name": "left", "type": "Entity_Link", "children": [{"$id": "FB-0:2::0-0", "collapsed": false, "type": "Fieldset", "name": "primary", "children": [{"name": "right", "$id": "FB-0:2::0-0:0", "type_name": "GTW.OMP.SRM.Regatta", "value": {"init": {"pid": 6, "cid": 6}}, "ui_name": "Regatta", "type": "Field_Entity", "children": [{"name": "left", "$id": "FB-0:2::0-0:0:0", "type_name": "GTW.OMP.SRM.Regatta_Event", "value": {"init": {"pid": 5, "cid": 5}}, "ui_name": "Event", "type": "Field_Entity", "children": [{"name": "date", "$id": "FB-0:2::0-0:0:0:0", "type_name": "MOM.Date_Interval_C", "value": {}, "ui_name": "Date", "type": "Field_Composite", "children": [{"$id": "FB-0:2::0-0:0:0:0.0", "ui_name": "Start", "type": "Field", "name": "start", "value": {"init": "2008/05/01"}}, {"$id": "FB-0:2::0-0:0:0:0.1", "ui_name": "Finish", "type": "Field", "name": "finish", "value": {"init": "2008/05/01"}}]}, {"$id": "FB-0:2::0-0:0:0:1", "ui_name": "Name", "type": "Field", "name": "name", "value": {"init": "Himmelfahrt"}}]}]}]}, {"$id": "FB-0:2::0-1", "collapsed": true, "type": "Fieldset", "name": "required", "children": [{"name": "skipper", "$id": "FB-0:2::0-1:0", "type_name": "GTW.OMP.SRM.Sailor", "value": {"init": {"pid": 4, "cid": 4}}, "ui_name": "Skipper", "type": "Field_Entity", "children": [{"name": "left", "$id": "FB-0:2::0-1:0:0", "type_name": "GTW.OMP.PAP.Person", "value": {"init": {"pid": 3, "cid": 3}}, "ui_name": "Person", "type": "Field_Entity", "children": [{"$id": "FB-0:2::0-1:0:0:0", "ui_name": "Last name", "type": "Field", "name": "last_name", "value": {"init": "Tanzer"}}, {"$id": "FB-0:2::0-1:0:0:1", "ui_name": "First name", "type": "Field", "name": "first_name", "value": {"init": "Laurens"}}, {"$id": "FB-0:2::0-1:0:0:2", "ui_name": "Middle name", "type": "Field", "name": "middle_name", "value": {}}, {"$id": "FB-0:2::0-1:0:0:3", "ui_name": "Academic title", "type": "Field", "name": "title", "value": {}}]}, {"$id": "FB-0:2::0-1:0:1", "ui_name": "Nation", "type": "Field", "name": "nation", "value": {"init": "AUT"}}, {"$id": "FB-0:2::0-1:0:2", "ui_name": "Mna number", "type": "Field", "name": "mna_number", "value": {"init": "29676"}}]}]}, {"$id": "FB-0:2::0-2", "collapsed": true, "type": "Fieldset", "name": "optional", "children": [{"$id": "FB-0:2::0-2:0", "ui_name": "Place", "type": "Field", "name": "place", "value": {}}, {"$id": "FB-0:2::0-2:1", "ui_name": "Points", "type": "Field", "name": "points", "value": {}}]}]}]}]}]}) ;

    >>> for i in fi.transitive_iter () :
    ...     print i.elem, sorted (i.value or ())
    <Form FB> []
    <Entity FB-0 'GTW.OMP.SRM.Boat'> ['init']
    <Fieldset FB-0:0 'primary'> []
    <Field_Entity FB-0:0:0 'left' 'GTW.OMP.SRM.Boat_Class'> ['init']
    <Field FB-0:0:0:0 'name'> ['init']
    <Field FB-0:0:1 'nation'> ['init']
    <Field FB-0:0:2 'sail_number'> ['init']
    <Fieldset FB-0:1 'optional'> []
    <Field FB-0:1:0 'name'> []
    <Entity_List FB-0:2 <Entity_Link FB-0:2::p 'GTW.OMP.SRM.Boat_in_Regatta'>> []
    <Entity_Link FB-0:2::0 'GTW.OMP.SRM.Boat_in_Regatta'> ['init']
    <Fieldset FB-0:2::0-0 'primary'> []
    <Field_Entity FB-0:2::0-0:0 'right' 'GTW.OMP.SRM.Regatta'> ['init']
    <Field_Entity FB-0:2::0-0:0:0 'left' 'GTW.OMP.SRM.Regatta_Event'> ['init']
    <Field_Composite FB-0:2::0-0:0:0:0 'date' 'MOM.Date_Interval_C'> []
    <Field FB-0:2::0-0:0:0:0.0 'start'> ['init']
    <Field FB-0:2::0-0:0:0:0.1 'finish'> ['init']
    <Field FB-0:2::0-0:0:0:1 'name'> ['init']
    <Fieldset FB-0:2::0-1 'required'> []
    <Field_Entity FB-0:2::0-1:0 'skipper' 'GTW.OMP.SRM.Sailor'> ['init']
    <Field_Entity FB-0:2::0-1:0:0 'left' 'GTW.OMP.PAP.Person'> ['init']
    <Field FB-0:2::0-1:0:0:0 'last_name'> ['init']
    <Field FB-0:2::0-1:0:0:1 'first_name'> ['init']
    <Field FB-0:2::0-1:0:0:2 'middle_name'> []
    <Field FB-0:2::0-1:0:0:3 'title'> []
    <Field FB-0:2::0-1:0:1 'nation'> ['init']
    <Field FB-0:2::0-1:0:2 'mna_number'> ['init']
    <Fieldset FB-0:2::0-2 'optional'> []
    <Field FB-0:2::0-2:0 'place'> []
    <Field FB-0:2::0-2:1 'points'> []

    >>> for i in fi.transitive_iter () :
    ...     v = i.value and i.value.get ("init")
    ...     if isinstance (v, dict) and v.get ("pid") :
    ...         print i.elem, "pid =", v ["pid"]
    <Entity FB-0 'GTW.OMP.SRM.Boat'> pid = 2
    <Field_Entity FB-0:0:0 'left' 'GTW.OMP.SRM.Boat_Class'> pid = 1
    <Entity_Link FB-0:2::0 'GTW.OMP.SRM.Boat_in_Regatta'> pid = 7
    <Field_Entity FB-0:2::0-0:0 'right' 'GTW.OMP.SRM.Regatta'> pid = 6
    <Field_Entity FB-0:2::0-0:0:0 'left' 'GTW.OMP.SRM.Regatta_Event'> pid = 5
    <Field_Entity FB-0:2::0-1:0 'skipper' 'GTW.OMP.SRM.Sailor'> pid = 4
    <Field_Entity FB-0:2::0-1:0:0 'left' 'GTW.OMP.PAP.Person'> pid = 3
    >>> for i in fic.transitive_iter () :
    ...     v = i.value and i.value.get ("init")
    ...     if isinstance (v, dict) and v.get ("pid") :
    ...         print i.elem, "pid =", v ["pid"]

    >>> v = Value.from_json (json_data)
    >>> v.changes
    1
    >>> for i in v.transitive_iter () :
    ...     print i
    <Form FB> init-v = '' 1
    <Entity FB-0 'GTW.OMP.SRM.Boat'> init-v = [(u'cid', 2), (u'pid', 2)] 0
    <Field_Entity FB-0:0:0 'left' 'GTW.OMP.SRM.Boat_Class'> init-v = [(u'cid', 1), (u'pid', 1)] 0
    <Field FB-0:0:0:0 'name'> init-v = 'Optimist' 0
    <Field FB-0:0:1 'nation'> init-v = 'AUT' 0
    <Field FB-0:0:2 'sail_number'> init-v = '1107' 0
    <Field FB-0:1:0 'name'> init-v = '' 0
    <Entity_Link FB-0:2::p 'GTW.OMP.SRM.Boat_in_Regatta'> init-v = [(u'cid', 7), (u'pid', 7)] 1
    <Field_Entity FB-0:2::p-0:0 'right' 'GTW.OMP.SRM.Regatta'> init-v = [(u'cid', 6), (u'pid', 6)] 0
    <Field_Entity FB-0:2::p-0:0:0 'left' 'GTW.OMP.SRM.Regatta_Event'> init-v = [(u'cid', 5), (u'pid', 5)] 0
    <Field_Composite FB-0:2::p-0:0:0:0 'date' 'MOM.Date_Interval_C'> init-v = '' 0
    <Field FB-0:2::p-0:0:0:0.0 'start'> init-v = '2008/05/01' 0
    <Field FB-0:2::p-0:0:0:0.1 'finish'> init-v = '2008/05/01' 0
    <Field FB-0:2::p-0:0:0:1 'name'> init-v = 'Himmelfahrt' 0
    <Field_Entity FB-0:2::p-1:0 'skipper' 'GTW.OMP.SRM.Sailor'> init-v = [(u'cid', 4), (u'pid', 4)] 1
    <Field_Entity FB-0:2::p-1:0:0 'left' 'GTW.OMP.PAP.Person'> init-v = [(u'cid', 3), (u'pid', 3)] 1
    <Field FB-0:2::p-1:0:0:0 'last_name'> init-v = 'Tanzer' 0
    <Field FB-0:2::p-1:0:0:1 'first_name'> init-v = 'Laurens' 0
    <Field FB-0:2::p-1:0:0:2 'middle_name'> init-v = '' user-v = 'William' 1
    <Field FB-0:2::p-1:0:0:3 'title'> init-v = '' 0
    <Field FB-0:2::p-1:0:1 'nation'> init-v = 'AUT' 0
    <Field FB-0:2::p-1:0:2 'mna_number'> init-v = '29676' 0
    <Field FB-0:2::p-2:0 'place'> init-v = '' 0
    <Field FB-0:2::p-2:1 'points'> init-v = '' 0

"""

from   _GTW.__test__.model      import *
from   _GTW._AFS._MOM.Element   import Form
from   _GTW._AFS.Value          import Value

from   _TFL.Formatter      import Formatter
formatted = Formatter (width = 240)

json_data = """{"$id":"FB","$child_ids":["FB-0","FB-0:2::0"],"FB-0":{"init":{"cid":2,"pid":2},"$id":"FB-0","$child_ids":["FB-0:0:0","FB-0:0:1","FB-0:0:2","FB-0:1:0"],"FB-0:0:0":{"init":{"cid":1,"pid":1},"$id":"FB-0:0:0","$child_ids":["FB-0:0:0:0"],"$anchor_id":"FB-0","FB-0:0:0:0":{"init":"Optimist"}},"FB-0:0:1":{"init":"AUT"},"FB-0:0:2":{"init":"1107"},"FB-0:1:0":{}},"FB-0:2::0":{"init":{"cid":7,"pid":7},"$id":"FB-0:2::0","$child_ids":["FB-0:2::0-0:0","FB-0:2::0-1:0","FB-0:2::0-2:0","FB-0:2::0-2:1"],"FB-0:2::0-0:0":{"init":{"cid":6,"pid":6},"$id":"FB-0:2::0-0:0","$child_ids":["FB-0:2::0-0:0:0"],"$anchor_id":"FB-0:2::0","FB-0:2::0-0:0:0":{"init":{"cid":5,"pid":5},"$id":"FB-0:2::0-0:0:0","$child_ids":["FB-0:2::0-0:0:0:0","FB-0:2::0-0:0:0:1"],"$anchor_id":"FB-0:2::0-0:0","FB-0:2::0-0:0:0:0":{"$id":"FB-0:2::0-0:0:0:0","$child_ids":["FB-0:2::0-0:0:0:0.0","FB-0:2::0-0:0:0:0.1"],"$anchor_id":"FB-0:2::0-0:0:0","FB-0:2::0-0:0:0:0.0":{"init":"2008/05/01"},"FB-0:2::0-0:0:0:0.1":{"init":"2008/05/01"}},"FB-0:2::0-0:0:0:1":{"init":"Himmelfahrt"}}},"FB-0:2::0-1:0":{"init":{"cid":4,"pid":4},"$id":"FB-0:2::0-1:0","$child_ids":["FB-0:2::0-1:0:0","FB-0:2::0-1:0:1","FB-0:2::0-1:0:2"],"$anchor_id":"FB-0:2::0","FB-0:2::0-1:0:0":{"init":{"cid":3,"pid":3},"$id":"FB-0:2::0-1:0:0","$child_ids":["FB-0:2::0-1:0:0:0","FB-0:2::0-1:0:0:1","FB-0:2::0-1:0:0:2","FB-0:2::0-1:0:0:3"],"$anchor_id":"FB-0:2::0-1:0","FB-0:2::0-1:0:0:0":{"init":"Tanzer"},"FB-0:2::0-1:0:0:1":{"init":"Laurens"},"FB-0:2::0-1:0:0:2":{"user":"William"},"FB-0:2::0-1:0:0:3":{}},"FB-0:2::0-1:0:1":{"init":"AUT"},"FB-0:2::0-1:0:2":{"init":"29676"}},"FB-0:2::0-2:0":{},"FB-0:2::0-2:1":{}}}"""

__test__ = dict (AFS_Spec = _test_code)

### __END__ AFS_Spec
