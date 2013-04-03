# -*- coding: iso-8859-15 -*-
# Copyright (C) 2011-2013 Mag. Christian Tanzer All rights reserved
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
#    GTW.__test__.Query_Restriction
#
# Purpose
#    Test cases for GTW.RST.TOP.MOM.Query_Restriction
#
# Revision Dates
#    14-Nov-2011 (CT) Creation
#     2-Dec-2011 (CT) Creation continued..
#    19-Mar-2012 (CT) Adapt to reification of `SRM.Handicap`
#    30-Jul-2012 (CT) Change to test `GTW.RST.TOP.MOM` instead of `GTW.NAV`
#    25-Mar-2013 (CT) Add `test_pepk`
#    27-Mar-2013 (CT) Add `test_request_get` and real query to `test_pepk`
#    ««revision-date»»···
#--

from   __future__  import unicode_literals

import _GTW.Request_Data

from   _TFL.Record      import Record

def f_req (** kw) :
    return Record \
        ( req_data      = GTW.Request_Data      (kw)
        , req_data_list = GTW.Request_Data_List (kw)
        )

_test_code = """
    >>> scope = Scaffold.scope (%(p1)s, %(n1)s) # doctest:+ELLIPSIS
    Creating new scope MOMT__...
    >>> PAP = scope.PAP
    >>> SRM = scope.SRM

    >>> qe = QR.from_request (scope, PAP.Person.E_Type, f_req (qux = "42", qix = "Miles"))
    >>> print qe.limit, qe.offset, qe.filters
    0 0 ()

    >>> rd = f_req (
    ...   limit = 24, last_name___GE = "Qux", lifetime__start___EQ = "2008", foo = "bar")
    >>> qr = QR.from_request (scope, PAP.Person.E_Type, rd)
    >>> print qr.limit, qr.offset
    24 0

    >>> print formatted (qr.filters_q)
    ( Q.last_name >= qux
    , Q.lifetime.start.between (datetime.date(2008, 1, 1), datetime.date(2008, 12, 31))
    )

    >>> print formatted (qr.filters)
    ( Record
      ( AQ = <last_name.AQ [Attr.Type.Querier String_FL]>
      , attr = String `last_name`
      , edit = 'Qux'
      , full_name = 'last_name'
      , id = 'last_name___GE'
      , name = 'last_name___GE'
      , op = Record
          ( desc = 'Select entities where the attribute is greater than, or equal to, the specified value'
          , label = '&ge;'
          )
      , sig_key = 3
      , ui_name = 'Last name'
      , value = 'Qux'
      )
    , Record
      ( AQ = <lifetime.start.AQ [Attr.Type.Querier Date]>
      , attr = Date `start`
      , edit = '2008'
      , full_name = 'lifetime.start'
      , id = 'lifetime__start___EQ'
      , name = 'lifetime__start___EQ'
      , op = Record
          ( desc = 'Select entities where the attribute is equal to the specified value'
          , label = '&equiv;'
          )
      , sig_key = 0
      , ui_name = 'Lifetime/Start'
      , value = '2008'
      )
    )

    >>> print formatted (qr.Filter (PAP.Person.E_Type, "last_name"))
    Record
    ( AQ = <last_name.AQ [Attr.Type.Querier String_FL]>
    , attr = String `last_name`
    , edit = None
    , full_name = 'last_name'
    , id = 'last_name___AC'
    , name = 'last_name___AC'
    , op = Record
        ( desc = 'Select entities where the attribute value starts with the specified value'
        , label = 'auto-complete'
        )
    , sig_key = 3
    , ui_name = 'Last name'
    , value = None
    )
    >>> print formatted (qr.Filter (PAP.Person.E_Type, "last_name___GE"))
    Record
    ( AQ = <last_name.AQ [Attr.Type.Querier String_FL]>
    , attr = String `last_name`
    , edit = None
    , full_name = 'last_name'
    , id = 'last_name___GE'
    , name = 'last_name___GE'
    , op = Record
        ( desc = 'Select entities where the attribute is greater than, or equal to, the specified value'
        , label = '&ge;'
        )
    , sig_key = 3
    , ui_name = 'Last name'
    , value = None
    )

    >>> print formatted (qr.filters)
    ( Record
      ( AQ = <last_name.AQ [Attr.Type.Querier String_FL]>
      , attr = String `last_name`
      , edit = 'Qux'
      , full_name = 'last_name'
      , id = 'last_name___GE'
      , name = 'last_name___GE'
      , op = Record
          ( desc = 'Select entities where the attribute is greater than, or equal to, the specified value'
          , label = '&ge;'
          )
      , sig_key = 3
      , ui_name = 'Last name'
      , value = 'Qux'
      )
    , Record
      ( AQ = <lifetime.start.AQ [Attr.Type.Querier Date]>
      , attr = Date `start`
      , edit = '2008'
      , full_name = 'lifetime.start'
      , id = 'lifetime__start___EQ'
      , name = 'lifetime__start___EQ'
      , op = Record
          ( desc = 'Select entities where the attribute is equal to the specified value'
          , label = '&equiv;'
          )
      , sig_key = 0
      , ui_name = 'Lifetime/Start'
      , value = '2008'
      )
    )

    >>> print qr.filters_q
    (Q.last_name >= qux, Q.lifetime.start.between (datetime.date(2008, 1, 1), datetime.date(2008, 12, 31)))

    >>> qo = QR.from_request (scope, PAP.Person.E_Type, f_req (order_by = "-lifetime,last_name"))
    >>> print formatted (qo.order_by)
    ( Record
      ( attr = Date_Interval `lifetime`
      , attrs =
          [ Record
            ( attr = Date `start`
            , full_name = 'lifetime.start'
            , id = 'lifetime__start'
            , name = 'start'
            , sig_key = 0
            , ui_name = 'Lifetime/Start'
            )
          , Record
            ( attr = Date `finish`
            , full_name = 'lifetime.finish'
            , id = 'lifetime__finish'
            , name = 'finish'
            , sig_key = 0
            , ui_name = 'Lifetime/Finish'
            )
          , Record
            ( attr = Boolean `alive`
            , choices =
                [ 'no'
                , 'yes'
                ]
            , full_name = 'lifetime.alive'
            , id = 'lifetime__alive'
            , name = 'alive'
            , sig_key = 1
            , ui_name = 'Lifetime/Alive'
            )
          ]
      , full_name = 'lifetime'
      , id = 'lifetime'
      , name = '-lifetime'
      , sign = '-'
      , ui_name = '-Lifetime'
      )
    , Record
      ( attr = String `last_name`
      , full_name = 'last_name'
      , id = 'last_name'
      , name = 'last_name'
      , sig_key = 3
      , sign = ''
      , ui_name = 'Last name'
      )
    )

    >>> print qo.order_by_q
    <Sorted_By: Descending-Getter function for `.lifetime.start`, Descending-Getter function for `.lifetime.finish`, Getter function for `.last_name`>

    >>> AS  = MOM.Attr.Selector
    >>> BiR = SRM.Boat_in_Regatta.E_Type
    >>> fns = AS.List (AS.primary, AS.Name ("points", "place")) (BiR).names
    >>> qrs = QRS (BiR, fns)

    >>> print formatted (qrs.As_Json_Cargo)
    { 'filters' :
        [ { 'Class' : 'Entity'
          , 'attrs' :
              [ { 'Class' : 'Entity'
                , 'attrs' :
                    [ { 'name' : 'name'
                      , 'sig_key' : 3
                      , 'ui_name' : 'Name'
                      }
                    ]
                , 'name' : 'left'
                , 'sig_key' : 2
                , 'ui_name' : 'Class'
                }
              , { 'name' : 'nation'
                , 'sig_key' : 0
                , 'ui_name' : 'Nation'
                }
              , { 'name' : 'sail_number'
                , 'sig_key' : 4
                , 'ui_name' : 'Sail number'
                }
              , { 'name' : 'sail_number_x'
                , 'sig_key' : 3
                , 'ui_name' : 'Sail number x'
                }
              ]
          , 'name' : 'left'
          , 'sig_key' : 2
          , 'ui_name' : 'Boat'
          }
        , { 'Class' : 'Entity'
          , 'attrs' :
              [ { 'Class' : 'Entity'
                , 'attrs' :
                    [ { 'name' : 'name'
                      , 'sig_key' : 3
                      , 'ui_name' : 'Name'
                      }
                    , { 'attrs' :
                          [ { 'name' : 'start'
                            , 'sig_key' : 0
                            , 'ui_name' : 'Start'
                            }
                          , { 'name' : 'finish'
                            , 'sig_key' : 0
                            , 'ui_name' : 'Finish'
                            }
                          ]
                      , 'name' : 'date'
                      , 'ui_name' : 'Date'
                      }
                    ]
                , 'name' : 'left'
                , 'sig_key' : 2
                , 'ui_name' : 'Event'
                }
              , { 'Class' : 'Entity'
                , 'attrs' :
                    [ { 'name' : 'name'
                      , 'sig_key' : 3
                      , 'ui_name' : 'Name'
                      }
                    ]
                , 'name' : 'boat_class'
                , 'sig_key' : 2
                , 'ui_name' : 'Boat class'
                }
              ]
          , 'name' : 'right'
          , 'sig_key' : 2
          , 'ui_name' : 'Regatta'
          }
        , { 'name' : 'points'
          , 'sig_key' : 0
          , 'ui_name' : 'Points'
          }
        , { 'name' : 'place'
          , 'sig_key' : 0
          , 'ui_name' : 'Place'
          }
        ]
    , 'name_sep' : '__'
    , 'op_map' :
        { 'CONTAINS' :
            { 'desc' : 'Select entities where the attribute contains the specified value'
            , 'label' : 'contains'
            , 'sym' : 'contains'
            }
        , 'ENDSWITH' :
            { 'desc' : 'Select entities where the attribute value ends with the specified value'
            , 'label' : 'ends-with'
            , 'sym' : 'ends-with'
            }
        , 'EQ' :
            { 'desc' : 'Select entities where the attribute is equal to the specified value'
            , 'label' : '&equiv;'
            , 'sym' : '=='
            }
        , 'EQS' :
            { 'desc' : 'Select entities where the attribute is equal to the specified string value'
            , 'label' : 'EQS'
            , 'sym' : 'EQS'
            }
        , 'GE' :
            { 'desc' : 'Select entities where the attribute is greater than, or equal to, the specified value'
            , 'label' : '&ge;'
            , 'sym' : '>='
            }
        , 'GT' :
            { 'desc' : 'Select entities where the attribute is greater than the specified value'
            , 'label' : '&gt;'
            , 'sym' : '>'
            }
        , 'IN' :
            { 'desc' : 'Select entities where the attribute is a member of the specified list of values'
            , 'label' : 'in'
            , 'sym' : 'in'
            }
        , 'LE' :
            { 'desc' : 'Select entities where the attribute is less than, or equal to, the specified value'
            , 'label' : '&le;'
            , 'sym' : '<='
            }
        , 'LT' :
            { 'desc' : 'Select entities where the attribute is less than the specified value'
            , 'label' : '&lt;'
            , 'sym' : '<'
            }
        , 'NE' :
            { 'desc' : 'Select entities where the attribute is not equal to the specified value'
            , 'label' : '&ne;'
            , 'sym' : '!='
            }
        , 'NES' :
            { 'desc' : 'Select entities where the attribute is not equal to the specified string value'
            , 'label' : 'NES'
            , 'sym' : 'NES'
              }
        , 'STARTSWITH' :
            { 'desc' : 'Select entities where the attribute value starts with the specified value'
            , 'label' : 'starts-with'
            , 'sym' : 'starts-with'
            }
        }
    , 'op_sep' : '___'
    , 'sig_map' :
        { 0 :
            ( 'EQ'
            , 'GE'
            , 'GT'
            , 'IN'
            , 'LE'
            , 'LT'
            , 'NE'
            )
        , 2 :
            ( 'EQ'
            , 'IN'
            , 'NE'
            )
        , 3 :
            ( 'CONTAINS'
            , 'ENDSWITH'
            , 'EQ'
            , 'GE'
            , 'GT'
            , 'IN'
            , 'LE'
            , 'LT'
            , 'NE'
            , 'STARTSWITH'
            )
        , 4 :
            ( 'CONTAINS'
            , 'ENDSWITH'
            , 'EQ'
            , 'EQS'
            , 'GE'
            , 'GT'
            , 'IN'
            , 'LE'
            , 'LT'
            , 'NE'
            , 'NES'
            , 'STARTSWITH'
            )
        }
    , 'ui_sep' : '/'
    }

    >>> def show_f (f, indent = "") :
    ...     print "%%s%%s" %% (indent, f), f._outer
    ...     for c in f.Attrs :
    ...         show_f (c, indent + "    ")

    >>> for f in qrs.Attrs :
    ...     show_f (f)
    <left.AQ [Attr.Type.Querier Id_Entity]> <SRM.Boat_in_Regatta.AQ>
        <left.left.AQ [Attr.Type.Querier Id_Entity]> <left.AQ [Attr.Type.Querier Id_Entity]>
            <left.left.name.AQ [Attr.Type.Querier String]> <left.left.AQ [Attr.Type.Querier Id_Entity]>
        <left.nation.AQ [Attr.Type.Querier Ckd]> <left.AQ [Attr.Type.Querier Id_Entity]>
        <left.sail_number.AQ [Attr.Type.Querier Raw]> <left.AQ [Attr.Type.Querier Id_Entity]>
        <left.sail_number_x.AQ [Attr.Type.Querier String]> <left.AQ [Attr.Type.Querier Id_Entity]>
    <right.AQ [Attr.Type.Querier Id_Entity]> <SRM.Boat_in_Regatta.AQ>
        <right.left.AQ [Attr.Type.Querier Id_Entity]> <right.AQ [Attr.Type.Querier Id_Entity]>
            <right.left.name.AQ [Attr.Type.Querier String]> <right.left.AQ [Attr.Type.Querier Id_Entity]>
            <right.left.date.AQ [Attr.Type.Querier Composite]> <right.left.AQ [Attr.Type.Querier Id_Entity]>
                <right.left.date.start.AQ [Attr.Type.Querier Date]> <right.left.date.AQ [Attr.Type.Querier Composite]>
                <right.left.date.finish.AQ [Attr.Type.Querier Date]> <right.left.date.AQ [Attr.Type.Querier Composite]>
        <right.boat_class.AQ [Attr.Type.Querier Id_Entity]> <right.AQ [Attr.Type.Querier Id_Entity]>
            <right.boat_class.name.AQ [Attr.Type.Querier String]> <right.boat_class.AQ [Attr.Type.Querier Id_Entity]>
    <points.AQ [Attr.Type.Querier Ckd]> <SRM.Boat_in_Regatta.AQ>
    <place.AQ [Attr.Type.Querier Ckd]> <SRM.Boat_in_Regatta.AQ>

    >>> print formatted (list (f.As_Template_Elem for f in qrs.Attrs))
    [ Record
      ( Class = 'Entity'
      , attr = Boat `left`
      , attrs =
          [ Record
            ( Class = 'Entity'
            , attr = Boat_Class `left`
            , attrs =
                [ Record
                  ( attr = String `name`
                  , full_name = 'left.left.name'
                  , id = 'left__left__name'
                  , name = 'name'
                  , sig_key = 3
                  , ui_name = 'Boat/Class/Name'
                  )
                ]
            , full_name = 'left.left'
            , id = 'left__left'
            , name = 'left'
            , sig_key = 2
            , type_name = 'SRM.Boat_Class'
            , ui_name = 'Boat/Class'
            , ui_type_name = 'Boat_Class'
            )
          , Record
            ( attr = Nation `nation`
            , choices =
                [
                  ( 'AUS'
                  , 'AUS [Australia]'
                  )
                ,
                  ( 'AUT'
                  , 'AUT [Austria]'
                  )
                ,
                  ( 'BEL'
                  , 'BEL [Belgium]'
                  )
                ,
                  ( 'CAN'
                  , 'CAN [Canada]'
                  )
                ,
                  ( 'CRO'
                  , 'CRO [Croatia]'
                  )
                ,
                  ( 'CYP'
                  , 'CYP [Cyprus]'
                  )
                ,
                  ( 'CZE'
                  , 'CZE [Czech Republic]'
                  )
                ,
                  ( 'DEN'
                  , 'DEN [Denmark]'
                  )
                ,
                  ( 'ESP'
                  , 'ESP [Spain]'
                  )
                ,
                  ( 'EST'
                  , 'EST [Estonia]'
                  )
                ,
                  ( 'FIN'
                  , 'FIN [Finland]'
                  )
                ,
                  ( 'FRA'
                  , 'FRA [France]'
                  )
                ,
                  ( 'GBR'
                  , 'GBR [Great Britain]'
                  )
                ,
                  ( 'GER'
                  , 'GER [Germany]'
                  )
                ,
                  ( 'GRE'
                  , 'GRE [Greece]'
                  )
                ,
                  ( 'HUN'
                  , 'HUN [Hungary]'
                  )
                ,
                  ( 'IRL'
                  , 'IRL [Ireland]'
                  )
                ,
                  ( 'ISL'
                  , 'ISL [Iceland]'
                  )
                ,
                  ( 'ITA'
                  , 'ITA [Italy]'
                  )
                ,
                  ( 'LAT'
                  , 'LAT [Latvia]'
                  )
                ,
                  ( 'LIE'
                  , 'LIE [Lichtenstein]'
                  )
                ,
                  ( 'LTU'
                  , 'LTU [Lithuania]'
                  )
                ,
                  ( 'LUX'
                  , 'LUX [Luxembourg]'
                  )
                ,
                  ( 'MLT'
                  , 'MLT [Malta]'
                  )
                ,
                  ( 'MNE'
                  , 'MNE [Montenegro]'
                  )
                ,
                  ( 'MON'
                  , 'MON [Monaco]'
                  )
                ,
                  ( 'NED'
                  , 'NED [Netherlands]'
                  )
                ,
                  ( 'NOR'
                  , 'NOR [Norway]'
                  )
                ,
                  ( 'NZL'
                  , 'NZL [New Zealand]'
                  )
                ,
                  ( 'POL'
                  , 'POL [Poland]'
                  )
                ,
                  ( 'POR'
                  , 'POR [Portugal]'
                  )
                ,
                  ( 'ROU'
                  , 'ROU [Romania]'
                  )
                ,
                  ( 'RSA'
                  , 'RSA [South Africa]'
                  )
                ,
                  ( 'RUS'
                  , 'RUS [Russia]'
                  )
                ,
                  ( 'SLO'
                  , 'SLO [Slovenia]'
                  )
                ,
                  ( 'SRB'
                  , 'SRB [Serbia]'
                  )
                ,
                  ( 'SUI'
                  , 'SUI [Switzerland]'
                  )
                ,
                  ( 'SVK'
                  , 'SVK [Slovakia]'
                  )
                ,
                  ( 'SWE'
                  , 'SWE [Sweden]'
                  )
                ,
                  ( 'UKR'
                  , 'UKR [Ukraine]'
                  )
                ,
                  ( 'USA'
                  , 'USA [United States]'
                  )
                ]
            , full_name = 'left.nation'
            , id = 'left__nation'
            , name = 'nation'
            , sig_key = 0
            , ui_name = 'Boat/Nation'
            )
          , Record
            ( attr = Int `sail_number`
            , full_name = 'left.sail_number'
            , id = 'left__sail_number'
            , name = 'sail_number'
            , sig_key = 4
            , ui_name = 'Boat/Sail number'
            )
          , Record
            ( attr = String `sail_number_x`
            , full_name = 'left.sail_number_x'
            , id = 'left__sail_number_x'
            , name = 'sail_number_x'
            , sig_key = 3
            , ui_name = 'Boat/Sail number x'
            )
          ]
      , full_name = 'left'
      , id = 'left'
      , name = 'left'
      , sig_key = 2
      , type_name = 'SRM.Boat'
      , ui_name = 'Boat'
      , ui_type_name = 'Boat'
      )
    , Record
      ( Class = 'Entity'
      , attr = Regatta `right`
      , attrs =
          [ Record
            ( Class = 'Entity'
            , attr = Regatta_Event `left`
            , attrs =
                [ Record
                  ( attr = String `name`
                  , full_name = 'right.left.name'
                  , id = 'right__left__name'
                  , name = 'name'
                  , sig_key = 3
                  , ui_name = 'Regatta/Event/Name'
                  )
                , Record
                  ( attr = Date_Interval `date`
                  , attrs =
                      [ Record
                        ( attr = Date `start`
                        , full_name = 'right.left.date.start'
                        , id = 'right__left__date__start'
                        , name = 'start'
                        , sig_key = 0
                        , ui_name = 'Regatta/Event/Date/Start'
                        )
                      , Record
                        ( attr = Date `finish`
                        , full_name = 'right.left.date.finish'
                        , id = 'right__left__date__finish'
                        , name = 'finish'
                        , sig_key = 0
                        , ui_name = 'Regatta/Event/Date/Finish'
                        )
                      ]
                  , full_name = 'right.left.date'
                  , id = 'right__left__date'
                  , name = 'date'
                  , ui_name = 'Regatta/Event/Date'
                  )
                ]
            , full_name = 'right.left'
            , id = 'right__left'
            , name = 'left'
            , sig_key = 2
            , type_name = 'SRM.Regatta_Event'
            , ui_name = 'Regatta/Event'
            , ui_type_name = 'Regatta_Event'
            )
          , Record
            ( Class = 'Entity'
            , attr = Entity `boat_class`
            , attrs =
                [ Record
                  ( attr = String `name`
                  , full_name = 'right.boat_class.name'
                  , id = 'right__boat_class__name'
                  , name = 'name'
                  , sig_key = 3
                  , ui_name = 'Regatta/Boat class/Name'
                  )
                ]
            , full_name = 'right.boat_class'
            , id = 'right__boat_class'
            , name = 'boat_class'
            , sig_key = 2
            , type_name = 'SRM._Boat_Class_'
            , ui_name = 'Regatta/Boat class'
            , ui_type_name = '_Boat_Class_'
            )
          ]
      , full_name = 'right'
      , id = 'right'
      , name = 'right'
      , sig_key = 2
      , type_name = 'SRM.Regatta'
      , ui_name = 'Regatta'
      , ui_type_name = 'Regatta'
      )
    , Record
      ( attr = Int `points`
      , full_name = 'points'
      , id = 'points'
      , name = 'points'
      , sig_key = 0
      , ui_name = 'Points'
      )
    , Record
      ( attr = Int `place`
      , full_name = 'place'
      , id = 'place'
      , name = 'place'
      , sig_key = 0
      , ui_name = 'Place'
      )
    ]

"""

_test_pepk = """
    >>> root  = Scaffold (["wsgi", "-db_url", %(p1)s, "-db_name", %(n1)s or ("test." + %(bn1)s)]) # doctest:+ELLIPSIS
    >>> scope = root.scope
    >>> PAP   = scope.PAP

    >>> rd = f_req (last_name = "Qux")
    >>> for afa in QR.af_args_fif (rd.req_data, QR._a_pat_opt) :
    ...    print afa
    (u'last_name___EQ', u'last_name', '', u'', u'EQ', u'Qux')

    >>> print formatted (QR.Filter (PAP.Person.E_Type, "last_name", "Qux"))
    Record
    ( AQ = <last_name.AQ [Attr.Type.Querier String_FL]>
    , attr = String `last_name`
    , edit = 'Qux'
    , full_name = 'last_name'
    , id = 'last_name___AC'
    , name = 'last_name___AC'
    , op = Record
        ( desc = 'Select entities where the attribute value starts with the specified value'
        , label = 'auto-complete'
        )
    , sig_key = 3
    , ui_name = 'Last name'
    , value = 'Qux'
    )

    >>> rdd = \\
    ...   { "spouse[PAP.Person]__last_name___GE" : "Qux"
    ...   , "spouse[PAP.Person]__lifetime__start___EQ" : "2008"
    ...   , "title___EQ" : "Dr."
    ...   , "foo" : "bar"
    ...   }
    >>> rdx = Record (req_data = GTW.Request_Data (rdd), req_data_list = GTW.Request_Data_List (rdd))

    >>> for afa in QR.af_args_fif (rdx.req_data) :
    ...    print afa
    (u'spouse[PAP.Person]__last_name___GE', u'spouse', u'PAP.Person', u'last_name', u'GE', u'Qux')
    (u'spouse[PAP.Person]__lifetime__start___EQ', u'spouse', u'PAP.Person', u'lifetime.start', u'EQ', u'2008')
    (u'title___EQ', u'title', '', u'', u'EQ', u'Dr.')

    >>> qrx = QR.from_request (scope, PAP.Person_M.E_Type, rdx)
    >>> print formatted (qrx.filters)
    ( Record
      ( AQ = <title.AQ [Attr.Type.Querier String]>
      , attr = String `title`
      , edit = 'Dr.'
      , full_name = 'title'
      , id = 'title___EQ'
      , name = 'title___EQ'
      , op = Record
          ( desc = 'Select entities where the attribute is equal to the specified value'
          , label = '&equiv;'
          )
      , sig_key = 3
      , ui_name = 'Academic title'
      , value = 'Dr.'
      )
    , Record
      ( AQ = <last_name.AQ [Attr.Type.Querier String_FL]>
      , attr = String `last_name`
      , edit = 'Qux'
      , full_name = 'spouse[PAP.Person].last_name'
      , id = 'spouse[PAP.Person]__last_name___GE'
      , name = 'spouse[PAP.Person]__last_name___GE'
      , op = Record
          ( desc = 'Select entities where the attribute is greater than, or equal to, the specified value'
          , label = '&ge;'
          )
      , sig_key = 3
      , ui_name = 'Spouse/Last name'
      , value = 'Qux'
      )
    , Record
      ( AQ = <lifetime.start.AQ [Attr.Type.Querier Date]>
      , attr = Date `start`
      , edit = '2008'
      , full_name = 'spouse[PAP.Person].lifetime.start'
      , id = 'spouse[PAP.Person]__lifetime__start___EQ'
      , name = 'spouse[PAP.Person]__lifetime__start___EQ'
      , op = Record
          ( desc = 'Select entities where the attribute is equal to the specified value'
          , label = '&equiv;'
          )
      , sig_key = 0
      , ui_name = 'Spouse/Lifetime/Start'
      , value = '2008'
      )
    )

    >>> p1  = PAP.Person_M ("Qux", "Foo", lifetime = ("20080327",), raw = True)
    >>> p2  = PAP.Person_M ("Bar", "Baz", title = "Dr.", spouse = p1, raw = True)

    >>> PAP.Person_M.query (sort_key = TFL.Sorted_By ("pid")).all ()
    [PAP.Person_M (u'qux', u'foo', u'', u''), PAP.Person_M (u'bar', u'baz', u'', u'dr.')]
    >>> pids = PAP.Person_M.query (sort_key = TFL.Sorted_By ("pid")).attr ("pid").all ()
    >>> list (int (p) for p in pids)
    [1, 2]

    >>> p1.pid, p1 in pids, p1 in [1, 2], p1 == p1.pid, p1.pid == p1
    (1, True, True, True, True)
    >>> p2.pid, p2 in pids, p2 in [1, 2], p2 == p2.pid, p2.pid == p2
    (2, True, True, True, True)
    >>> p1.spouse and p1.spouse.pid, p1.spouse in [1]
    (None, False)
    >>> p2.spouse and p2.spouse.pid, p2.spouse in [1], p2.spouse == p1.pid, p1.pid == p2.spouse
    (1, True, True, True)

    >>> req = Scaffold.test_request_get ("/Admin/Person?spouse[PAP.Person]__last_name___GE=Qux&spouse[PAP.Person]__lifetime__start___EQ=2008&title___EQ=Dr.")
    >>> qr  = QR.from_request (scope, PAP.Person_M.E_Type, req)
    >>> print (formatted (qr.filters))
    ( Record
      ( AQ = <title.AQ [Attr.Type.Querier String]>
      , attr = String `title`
      , edit = 'Dr.'
      , full_name = 'title'
      , id = 'title___EQ'
      , name = 'title___EQ'
      , op = Record
          ( desc = 'Select entities where the attribute is equal to the specified value'
          , label = '&equiv;'
          )
      , sig_key = 3
      , ui_name = 'Academic title'
      , value = 'Dr.'
      )
    , Record
      ( AQ = <last_name.AQ [Attr.Type.Querier String_FL]>
      , attr = String `last_name`
      , edit = 'Qux'
      , full_name = 'spouse[PAP.Person].last_name'
      , id = 'spouse[PAP.Person]__last_name___GE'
      , name = 'spouse[PAP.Person]__last_name___GE'
      , op = Record
          ( desc = 'Select entities where the attribute is greater than, or equal to, the specified value'
          , label = '&ge;'
          )
      , sig_key = 3
      , ui_name = 'Spouse/Last name'
      , value = 'Qux'
      )
    , Record
      ( AQ = <lifetime.start.AQ [Attr.Type.Querier Date]>
      , attr = Date `start`
      , edit = '2008'
      , full_name = 'spouse[PAP.Person].lifetime.start'
      , id = 'spouse[PAP.Person]__lifetime__start___EQ'
      , name = 'spouse[PAP.Person]__lifetime__start___EQ'
      , op = Record
          ( desc = 'Select entities where the attribute is equal to the specified value'
          , label = '&equiv;'
          )
      , sig_key = 0
      , ui_name = 'Spouse/Lifetime/Start'
      , value = '2008'
      )
    )

    >>> list (int (p) for p in PAP.Person_M.query (sort_key = TFL.Sorted_By ("pid")).attr ("pid"))
    [1, 2]

    >>> list (int (p) for p in PAP.Person_M.query (* qr.filters_q, sort_key = TFL.Sorted_By ("pid")).attr ("pid"))
    [2]

    >>> qr.filters_q # doctest:+ELLIPSIS
    (Q.title == dr., Q.spouse.in_ (...,))

    >>> qr (PAP.Person_M.query (sort_key = TFL.Sorted_By ("pid"))).all ()
    [PAP.Person_M (u'bar', u'baz', u'', u'dr.')]

"""

from   _GTW.__test__.model                   import *
from   _GTW._RST._TOP._MOM.Query_Restriction import \
     ( Query_Restriction      as QR
     , Query_Restriction_Spec as QRS
     )
import _GTW._OMP._PAP.Association

_Ancestor_Essence = GTW.OMP.PAP.Person

class Person_M (_Ancestor_Essence) :
    """Married person"""

    class _Attributes (_Ancestor_Essence._Attributes) :

        _Ancestor = _Ancestor_Essence._Attributes

        class spouse (A_Id_Entity) :
            """Spouse of this person"""

            kind               = Attr.Necessary
            P_Type             = "GTW.OMP.PAP.Subject"

        # end class spouse

    # end class _Attributes

# end class Person_M

from   _TFL.Formatter                        import Formatter, formatted_1
formatted = Formatter (width = 240)

from   itertools                             import chain as ichain

__test__ = Scaffold.create_test_dict \
    ( dict
      ( main       = _test_code
      , test_pepk  = _test_pepk
      )
    )

### __END__ GTW.__test__.Query_Restriction
