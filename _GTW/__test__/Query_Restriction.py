# -*- coding: iso-8859-15 -*-
# Copyright (C) 2011 Mag. Christian Tanzer All rights reserved
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
#    Test cases for GTW.NAV.E_Type.Query_Restriction
#
# Revision Dates
#    14-Nov-2011 (CT) Creation
#     2-Dec-2011 (CT) Creation continued..
#    ««revision-date»»···
#--

from   __future__  import unicode_literals

_test_code = """
    >>> scope = Scaffold.scope (%(p1)s, %(n1)s) # doctest:+ELLIPSIS
    Creating new scope MOMT__...
    >>> PAP = scope.PAP
    >>> SRM = scope.SRM

    >>> qe = QR.from_request_data (PAP.Person.E_Type, dict (qux = "42", qix = "Miles"))
    >>> print qe.limit, qe.offset, qe.filters, formatted_1 (sorted (qe.other_req_data.items ()))
    0 0 () [('qix', 'Miles'), ('qux', '42')]

    >>> rd = dict (
    ...   limit = 24, last_name___GE = "Lee", lifetime__start___EQ = "2008", foo = "bar")
    >>> qr = QR.from_request_data (PAP.Person.E_Type, rd)
    >>> print qr.limit, qr.offset
    24 0

    >>> print formatted (qr.Filter (PAP.Person.E_Type, "last_name"))
    Record
    ( attr = String `last_name`
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
    ( attr = String `last_name`
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
      ( attr = String `last_name`
      , edit = 'Lee'
      , full_name = 'last_name'
      , id = 'last_name___GE'
      , name = 'last_name___GE'
      , op = Record
          ( desc = 'Select entities where the attribute is greater than, or equal to, the specified value'
          , label = '&ge;'
          )
      , sig_key = 3
      , ui_name = 'Last name'
      , value = 'Lee'
      )
    , Record
      ( attr = Date `start`
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
    (Q.last_name >= lee, Q.lifetime.start.between (datetime.date(2008, 1, 1), datetime.date(2008, 12, 31)))
    >>> print formatted_1 (sorted (qr.other_req_data.items ()))
    [('foo', 'bar')]
    >>> print sorted (rd)
    ['foo', 'last_name___GE', 'lifetime__start___EQ', 'limit']

    >>> qo = QR.from_request_data (PAP.Person.E_Type, dict (order_by = "-lifetime,last_name"))
    >>> print formatted (qo.order_by)
    ( Record
      ( attr = Date_Interval `lifetime`
      , children =
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
    >>> print formatted (qrs.as_json_cargo)
    { 'filters' :
        [ { 'children' :
              [ { 'children' :
                    [ { 'name' : 'name'
                      , 'sig_key' : 3
                      , 'ui_name' : 'Name'
                      }
                    ]
                , 'deep' : True
                , 'name' : 'left'
                , 'sig_key' : 2
                , 'ui_name' : 'Class'
                }
              , { 'name' : 'nation'
                , 'sig_key' : 0
                , 'ui_name' : 'Nation'
                }
              , { 'name' : 'sail_number'
                , 'sig_key' : 3
                , 'ui_name' : 'Sail number'
                }
              , { 'name' : 'sail_number_x'
                , 'sig_key' : 3
                , 'ui_name' : 'Sail number x'
                }
              ]
          , 'deep' : True
          , 'name' : 'left'
          , 'sig_key' : 2
          , 'ui_name' : 'Boat'
          }
        , { 'children' :
              [ { 'children' :
                    [ { 'name' : 'name'
                      , 'sig_key' : 3
                      , 'ui_name' : 'Name'
                      }
                    , { 'children' :
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
                , 'deep' : True
                , 'name' : 'left'
                , 'sig_key' : 2
                , 'ui_name' : 'Event'
                }
              ]
          , 'deep' : True
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
            , 'LE'
            , 'LT'
            , 'NE'
            )
        , 2 :
            ( 'EQ'
            , 'NE'
            )
        , 3 :
            ( 'CONTAINS'
            , 'ENDSWITH'
            , 'EQ'
            , 'GE'
            , 'GT'
            , 'LE'
            , 'LT'
            , 'NE'
            , 'STARTSWITH'
            )
        }
    , 'ui_sep' : '/'
    }

    >>> def show_f (f, indent = "") :
    ...     print "%%s%%s" %% (indent, f), f._outer
    ...     for c in f.Children :
    ...         show_f (c, indent + "    ")

    >>> for f in qrs.filters :
    ...     show_f (f)
    <left.Q [Attr.Type.Querier Id_Entity]> None
        <left.left.Q [Attr.Type.Querier Id_Entity]> <left.Q [Attr.Type.Querier Id_Entity]>
            <left.left.name.Q [Attr.Type.Querier String]> <left.left.Q [Attr.Type.Querier Id_Entity]>
        <left.nation.Q [Attr.Type.Querier Ckd]> <left.Q [Attr.Type.Querier Id_Entity]>
        <left.__raw_sail_number.Q [Attr.Type.Querier Raw]> <left.Q [Attr.Type.Querier Id_Entity]>
        <left.sail_number_x.Q [Attr.Type.Querier String]> <left.Q [Attr.Type.Querier Id_Entity]>
    <right.Q [Attr.Type.Querier Id_Entity]> None
        <right.left.Q [Attr.Type.Querier Id_Entity]> <right.Q [Attr.Type.Querier Id_Entity]>
            <right.left.name.Q [Attr.Type.Querier String]> <right.left.Q [Attr.Type.Querier Id_Entity]>
            <right.left.date.Q [Attr.Type.Querier Composite]> <right.left.Q [Attr.Type.Querier Id_Entity]>
                <right.left.date.start.Q [Attr.Type.Querier Date]> <right.left.date.Q [Attr.Type.Querier Composite]>
                <right.left.date.finish.Q [Attr.Type.Querier Date]> <right.left.date.Q [Attr.Type.Querier Composite]>
    <points.Q [Attr.Type.Querier Ckd]> None
    <place.Q [Attr.Type.Querier Ckd]> None

    >>> print formatted (list (f.as_template_elem for f in qrs.filters))
    [ Record
      ( attr = Boat `left`
      , children =
          [ Record
            ( attr = Boat_Class `left`
            , children =
                [ Record
                  ( attr = String `name`
                  , full_name = 'left.left.name'
                  , id = 'left__left__name'
                  , name = 'name'
                  , sig_key = 3
                  , ui_name = 'Boat/Class/Name'
                  )
                ]
            , deep = True
            , full_name = 'left.left'
            , id = 'left__left'
            , name = 'left'
            , sig_key = 2
            , ui_name = 'Boat/Class'
            )
          , Record
            ( attr = Nation `nation`
            , choices =
                [
                  ( 'AUS'
                  , 'Australia'
                  )
                ,
                  ( 'AUT'
                  , 'Austria'
                  )
                ,
                  ( 'BEL'
                  , 'Belgium'
                  )
                ,
                  ( 'CAN'
                  , 'Canada'
                  )
                ,
                  ( 'CRO'
                  , 'Croatia'
                  )
                ,
                  ( 'CYP'
                  , 'Cyprus'
                  )
                ,
                  ( 'CZE'
                  , 'Czech Republic'
                  )
                ,
                  ( 'DEN'
                  , 'Denmark'
                  )
                ,
                  ( 'EST'
                  , 'Estonia'
                  )
                ,
                  ( 'FIN'
                  , 'Finland'
                  )
                ,
                  ( 'FRA'
                  , 'France'
                  )
                ,
                  ( 'GER'
                  , 'Germany'
                  )
                ,
                  ( 'GBR'
                  , 'Great Britain'
                  )
                ,
                  ( 'GRE'
                  , 'Greece'
                  )
                ,
                  ( 'HUN'
                  , 'Hungary'
                  )
                ,
                  ( 'ISL'
                  , 'Iceland'
                  )
                ,
                  ( 'IRL'
                  , 'Ireland'
                  )
                ,
                  ( 'ITA'
                  , 'Italy'
                  )
                ,
                  ( 'LAT'
                  , 'Latvia'
                  )
                ,
                  ( 'LIE'
                  , 'Lichtenstein'
                  )
                ,
                  ( 'LTU'
                  , 'Lithuania'
                  )
                ,
                  ( 'LUX'
                  , 'Luxembourg'
                  )
                ,
                  ( 'MLT'
                  , 'Malta'
                  )
                ,
                  ( 'MON'
                  , 'Monaco'
                  )
                ,
                  ( 'MNE'
                  , 'Montenegro'
                  )
                ,
                  ( 'NED'
                  , 'Netherlands'
                  )
                ,
                  ( 'NZL'
                  , 'New Zealand'
                  )
                ,
                  ( 'NOR'
                  , 'Norway'
                  )
                ,
                  ( 'POL'
                  , 'Poland'
                  )
                ,
                  ( 'POR'
                  , 'Portugal'
                  )
                ,
                  ( 'ROU'
                  , 'Romania'
                  )
                ,
                  ( 'RUS'
                  , 'Russia'
                  )
                ,
                  ( 'SRB'
                  , 'Serbia'
                  )
                ,
                  ( 'SVK'
                  , 'Slovakia'
                  )
                ,
                  ( 'SLO'
                  , 'Slovenia'
                  )
                ,
                  ( 'ESP'
                  , 'Spain'
                  )
                ,
                  ( 'SWE'
                  , 'Sweden'
                  )
                ,
                  ( 'SUI'
                  , 'Switzerland'
                  )
                ,
                  ( 'UKR'
                  , 'Ukraine'
                  )
                ,
                  ( 'USA'
                  , 'United States'
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
            , sig_key = 3
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
      , deep = True
      , full_name = 'left'
      , id = 'left'
      , name = 'left'
      , sig_key = 2
      , ui_name = 'Boat'
      )
    , Record
      ( attr = Regatta `right`
      , children =
          [ Record
            ( attr = Regatta_Event `left`
            , children =
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
                  , children =
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
            , deep = True
            , full_name = 'right.left'
            , id = 'right__left'
            , name = 'left'
            , sig_key = 2
            , ui_name = 'Regatta/Event'
            )
          ]
      , deep = True
      , full_name = 'right'
      , id = 'right'
      , name = 'right'
      , sig_key = 2
      , ui_name = 'Regatta'
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

    >>> scope.destroy ()

"""

from   _GTW.__test__.model                 import *
from   _GTW._NAV._E_Type.Query_Restriction import \
     ( Query_Restriction      as QR
     , Query_Restriction_Spec as QRS
     )
from   _TFL.Formatter                      import Formatter, formatted_1
formatted = Formatter (width = 240)

__test__ = Scaffold.create_test_dict (_test_code)

### __END__ GTW.__test__.Query_Restriction
