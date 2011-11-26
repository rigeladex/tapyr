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
    >>> print formatted_1 (qr.filters)
    (Record (attr = String `last_name`, key = 'last_name___GE', name = 'last_name', op = '>=', op_desc = 'Select entities where the attribute is greater than, or equal to, the specified value', op_nam = 'greater-equal', ui_names = ('Last name',), value = 'Lee'), Record (attr = Date `start`, key = 'lifetime__start___EQ', name = 'lifetime.start', op = '==', op_desc = 'Select entities where the attribute is equal to the specified value', op_nam = 'equal', ui_names = ('Lifetime', 'Start'), value = '2008'))
    >>> print qr.filters_q
    (Q.last_name >= lee, Q.lifetime.start.between (datetime.date(2008, 1, 1), datetime.date(2008, 12, 31)))
    >>> print formatted_1 (sorted (qr.other_req_data.items ()))
    [('foo', 'bar')]
    >>> print sorted (rd)
    ['foo', 'last_name___GE', 'lifetime__start___EQ', 'limit']

    >>> qo = QR.from_request_data (PAP.Person.E_Type, dict (order_by = "-lifetime,last_name"))
    >>> print formatted_1 (qo.order_by)
    (Record (attr = Date_Interval `lifetime`, name = '-lifetime', sign = '-', ui_names = ('Lifetime',)), Record (attr = String `last_name`, name = 'last_name', sign = '', ui_names = ('Last name',)))
    >>> print qo.order_by_q
    <Sorted_By: Descending-Getter function for `.lifetime.start`, Descending-Getter function for `.lifetime.finish`, Getter function for `.last_name`>

    >>> AS  = MOM.Attr.Selector
    >>> BiR = SRM.Boat_in_Regatta.E_Type
    >>> qrs = QRS (BiR, AS.List (AS.primary, AS.Name ("points", "place")) (BiR))
    >>> print formatted (qrs.as_json_cargo)
    { 'filters' :
        [ { 'children' :
              [ { 'children' :
                    [ { 'name' : 'name'
                      , 'sig_key' : 2
                      , 'ui_name' : 'Name'
                      }
                    ]
                , 'deep' : True
                , 'name' : 'left'
                , 'sig_key' : 1
                , 'ui_name' : 'Class'
                }
              , { 'name' : 'nation'
                , 'sig_key' : 0
                , 'ui_name' : 'Nation'
                }
              , { 'name' : 'sail_number'
                , 'sig_key' : 2
                , 'ui_name' : 'Sail number'
                }
              , { 'name' : 'sail_number_x'
                , 'sig_key' : 2
                , 'ui_name' : 'Sail number x'
                }
              ]
          , 'deep' : True
          , 'name' : 'left'
          , 'sig_key' : 1
          , 'ui_name' : 'Boat'
          }
        , { 'children' :
              [ { 'children' :
                    [ { 'name' : 'name'
                      , 'sig_key' : 2
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
                , 'sig_key' : 1
                , 'ui_name' : 'Event'
                }
              ]
          , 'deep' : True
          , 'name' : 'right'
          , 'sig_key' : 1
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
            , 'sym' : 'contains'
            }
        , 'ENDSWITH' :
            { 'desc' : 'Select entities where the attribute value ends with the specified value'
            , 'sym' : 'ends-with'
            }
        , 'EQ' :
            { 'desc' : 'Select entities where the attribute is equal to the specified value'
            , 'sym' : '=='
            }
        , 'GE' :
            { 'desc' : 'Select entities where the attribute is greater than, or equal to, the specified value'
            , 'sym' : '>='
            }
        , 'GT' :
            { 'desc' : 'Select entities where the attribute is greater than the specified value'
            , 'sym' : '>'
            }
        , 'LE' :
            { 'desc' : 'Select entities where the attribute is less than, or equal to, the specified value'
            , 'sym' : '<='
            }
        , 'LT' :
            { 'desc' : 'Select entities where the attribute is less than the specified value'
            , 'sym' : '<'
            }
        , 'NE' :
            { 'desc' : 'Select entities where the attribute is not equal to the specified value'
            , 'sym' : '!='
            }
        , 'STARTSWITH' :
            { 'desc' : 'Select entities where the attribute value starts with the specified value'
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
        , 1 :
            ( 'EQ'
            , 'NE'
            )
        , 2 :
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
