# -*- coding: iso-8859-15 -*-
# Copyright (C) 2010-2013 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# ****************************************************************************
# This module is part of the package GTW.__test__.
#
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
# ****************************************************************************
#
#++
# Name
#    GTW.__test__.Boat
#
# Purpose
#    Test SRM.Boat creation and querying
#
# Revision Dates
#    27-Apr-2010 (CT) Creation
#    29-Mar-2011 (CT) Test for change of `Init_Only_Mixin` attribute added
#     9-Nov-2011 (CT) Add test for `sail_number_head` and `sail_number_tail`
#    10-Nov-2011 (CT) Add test for `Name_Clash`
#    19-Mar-2012 (CT) Adapt to `Boat_Class.name.ignore_case` now being `True`
#    12-Apr-2012 (CT) Add tests for `max_crew` predicate
#    12-Apr-2012 (CT) Add tests for `on_error`
#    15-Apr-2012 (CT) Adapt to changes of `MOM.Error`
#    17-Apr-2012 (CT) Adapt to more changes of `MOM.Error`
#     2-Jul-2012 (MG) Additional tests for handling of execptions added
#     9-Sep-2012 (MG) Test for `convert_creation_change` added
#     9-Sep-2012 (RS) Add `last_changed` and `creation_date` checks
#    30-Jan-2013 (CT) Adapt to `Unique` predicates
#    ««revision-date»»···
#--

_test_code = """
    >>> scope = Scaffold.scope (%(p1)s, %(n1)s) # doctest:+ELLIPSIS
    Creating new scope MOMT__...
    >>> SRM = scope.SRM

    >>> bc = SRM.Boat_Class ("Optimist", max_crew = 1)
    >>> bc
    SRM.Boat_Class (u'optimist')
    >>> change = scope.query_changes (pid = bc.pid).one ()
    >>> change.c_time == change.time, change.c_user ==change.user
    (True, True)
    >>> c_time = datetime.datetime (2012, 1, 1,  0, 0, 0)
    >>> time   = datetime.datetime (2012, 4, 1, 10, 0, 0)
    >>> scope.ems.convert_creation_change \
        (bc.pid, c_time = c_time, time = time, user = "changed", c_user = "created")
    >>> print formatted_1 ((change.c_user, change.c_time, change.user, change.time))
    ('created', datetime.datetime(2012, 1, 1, 0, 0), 'changed', datetime.datetime(2012, 4, 1, 10, 0))

    >>> bc.last_changed
    datetime.datetime(2012, 4, 1, 10, 0)
    >>> bc.creation_date
    datetime.datetime(2012, 1, 1, 0, 0)
    >>> print scope.SRM.Boat_Class.count ### 1
    1
    >>> laser = SRM.Boat_Class ("Laser", max_crew = 1)
    >>> print scope.SRM.Boat_Class.count ### 2
    2

    >>> scope.SRM.Boat_Class.query (name = u'optimist').all ()
    [SRM.Boat_Class (u'optimist')]
    >>> scope.SRM.Boat_Class.instance (u'Optimist')
    SRM.Boat_Class (u'optimist')
    >>> SRM.Boat.instance_or_new (u'Optimist', u"AUT", u"1107", raw = True) ### 1
    SRM.Boat ((u'optimist', ), u'AUT', 1107, u'')
    >>> print scope.SRM.Boat.count ### 3
    1
    >>> scope.SRM.Boat.query_s ().all ()
    [SRM.Boat ((u'optimist', ), u'AUT', 1107, u'')]
    >>> scope.commit ()

    >>> change = scope.query_changes (pid = bc.pid).one ()
    >>> print formatted_1 ((change.c_user, change.c_time, change.user, change.time))
    ('created', datetime.datetime(2012, 1, 1, 0, 0), 'changed', datetime.datetime(2012, 4, 1, 10, 0))

    >>> SRM.Boat.instance_or_new (u'Optimist', u"AUT", u"1107", raw = True) ### 2
    SRM.Boat ((u'optimist', ), u'AUT', 1107, u'')
    >>> print scope.SRM.Boat.count ### 4
    1
    >>> scope.SRM.Boat.query_s ().all ()
    [SRM.Boat ((u'optimist', ), u'AUT', 1107, u'')]

    >>> b = SRM.Boat.instance_or_new (u'Optimist', u"AUT", u"1107", raw = True) ### 3
    >>> c = SRM.Boat (u"Optimist", None, "42", "OE", raw = True)

    >>> print scope.SRM.Boat.count ### 5
    2
    >>> scope.SRM.Boat.query_s ().all ()
    [SRM.Boat ((u'optimist', ), '', 42, u'OE'), SRM.Boat ((u'optimist', ), u'AUT', 1107, u'')]

    >>> print (c.sail_number, c.sail_number_head, c.sail_number_tail)
    (42, u'OE', u'42')
    >>> print (c.FO.sail_number, c.FO.sail_number_head, c.FO.sail_number_tail)
    (u'42', u'OE', u'42')
    >>> print (b.sail_number, b.sail_number_head, b.sail_number_tail)
    (1107, u'', u'1107')

    >>> s1 = TFL.Sorted_By ("name")
    >>> s2 = TFL.Sorted_By ("-name")
    >>> SRM.Boat_Class.query ().order_by (s1).all ()
    [SRM.Boat_Class (u'laser'), SRM.Boat_Class (u'optimist')]
    >>> SRM.Boat_Class.query ().order_by (s1).order_by (s2).all ()
    [SRM.Boat_Class (u'optimist'), SRM.Boat_Class (u'laser')]

    >>> print SRM.Boat.sail_number.Q_Raw.EQ
    <Attr.Equal sail_number.EQ [==]>
    >>> rf = SRM.Boat.sail_number.Q_Raw.EQ ("1107")
    >>> rf (b)
    True

    >>> getattr (b, "__raw_sail_number", "No raw value???")
    u'1107'

    >>> print SRM.Boat.sail_number.Q_Raw.EQ  ("1107")
    Q.sail_number == 1107
    >>> print SRM.Boat.sail_number.Q_Raw.EQS ("1107")
    Q.__raw_sail_number == 1107
    >>> print SRM.Boat.sail_number.Q_Raw.AC  ("11")
    Q.__raw_sail_number.startswith (u'11',)

    >>> bq = SRM.Boat.query_s ()
    >>> bq.all ()
    [SRM.Boat ((u'optimist', ), '', 42, u'OE'), SRM.Boat ((u'optimist', ), u'AUT', 1107, u'')]
    >>> SRM.Boat.query_s (SRM.Boat.sail_number.Q_Raw.EQ ("1107")).all ()
    [SRM.Boat ((u'optimist', ), u'AUT', 1107, u'')]
    >>> SRM.Boat.query_s (SRM.Boat.sail_number.Q_Raw.AC ("11")).all ()
    [SRM.Boat ((u'optimist', ), u'AUT', 1107, u'')]

    >>> print scope.SRM.Boat.count ### 6
    2

    >>> b.set (left = laser)
    Traceback (most recent call last):
      ...
    AttributeError: Init-only attribute `Boat.left` cannot be changed from `(u'optimist')` to `(u'laser')` after object creation

    >>> print scope.SRM.Boat.count ### 7
    2
    >>> scope.commit ()

    >>> SRM.Boat.query_s ().all () ### before Name_Clash
    [SRM.Boat ((u'optimist', ), '', 42, u'OE'), SRM.Boat ((u'optimist', ), u'AUT', 1107, u'')]

    >>> laser.max_crew ### before name clash, before change
    1
    >>> laser.max_crew = 2
    >>> laser.max_crew ### before name clash, after change
    2
    >>> d = SRM.Boat (SRM.Boat_Class ("Optimist", max_crew = 1), "AUT", "1134")
    Traceback (most recent call last):
      ...
    Invariants: The attribute values for ('name',) must be unique for each object
      The new definition of Boat_Class SRM.Boat_Class (u'Optimist',) would clash with 1 existing entities
      Already existing:
        SRM.Boat_Class (u'Optimist',)

    >>> print scope.SRM.Boat.count ### 8
    2
    >>> laser.max_crew ### after name clash
    2

    >>> SRM.Boat.query_s ().all () ### after Name_Clash
    [SRM.Boat ((u'optimist', ), '', 42, u'OE'), SRM.Boat ((u'optimist', ), u'AUT', 1107, u'')]

    >>> print sorted (b.b_class._pred_man.errors.items ()) ### before invariant errors
    [('object', []), ('region', []), ('system', []), ('uniqueness', [])]

    >>> b.b_class.max_crew = 0
    Traceback (most recent call last):
      ...
    Invariant: Condition `AC_check_max_crew_1` : 1 <= max_crew <= 4
        max_crew = 0
    >>> print sorted (b.b_class._pred_man.errors.items ()) ### after invariant error from `setattr`
    [('object', []), ('region', []), ('system', []), ('uniqueness', [])]


    >>> errors = []
    >>> b.b_class.set (max_crew = 0)
    Traceback (most recent call last):
      ...
    Invariants: Condition `AC_check_max_crew_1` : 1 <= max_crew <= 4
        max_crew = 0
    >>> print sorted (b.b_class._pred_man.errors.items ()) ### after invariant error from `.set (max_crew = 0)`
    [('object', [Invariant(SRM.Boat_Class (u'optimist'), Condition `AC_check_max_crew_1` : 1 <= max_crew <= 4
        max_crew = 0)]), ('region', []), ('system', []), ('uniqueness', [])]
    >>> errors
    []
    >>> b.b_class.set (max_crew = 5, on_error = errors.append)
    0
    >>> print sorted (b.b_class._pred_man.errors.items ()) ### after invariant error from `.set (max_crew = 5)`
    [('object', [Invariant(SRM.Boat_Class (u'optimist'), Condition `AC_check_max_crew_1` : 1 <= max_crew <= 4
        max_crew = 5)]), ('region', []), ('system', []), ('uniqueness', [])]
    >>> errors
    [Invariants(Invariant(SRM.Boat_Class (u'optimist'), Condition `AC_check_max_crew_1` : 1 <= max_crew <= 4
        max_crew = 5),)]
    >>> print formatted (MOM.Error.as_json_cargo (* errors))
    [ { 'attributes' :
    [ 'max_crew' ]
      , 'bindings' :
          [
            ( 'max_crew'
            , '5'
            )
          ]
      , 'head' : '1 <= max_crew <= 4'
      , 'is_required' : True
      }
    ]

    >>> b.b_class.set (max_crew = None)
    Traceback (most recent call last):
      ...
    Invariants: Condition `max_crew_not_empty` : max_crew is not None and max_crew != ''
        max_crew = None
    >>> print sorted (b.b_class._pred_man.errors.items ()) ### after invariant error from `.set (max_crew = None)`
    [('object', [Required_Empty(SRM.Boat_Class (u'optimist'), Condition `max_crew_not_empty` : max_crew is not None and max_crew != ''
        max_crew = None)]), ('region', []), ('system', []), ('uniqueness', [])]

    >>> b.b_class.max_crew = None
    Traceback (most recent call last):
      ...
    Required_Empty: Condition `max_crew_not_empty` : max_crew is not None and max_crew != ''
        max_crew = None

    >>> errors = []
    >>> SRM.Boat_Class ("Seascape 18", on_error = errors.append)
    Traceback (most recent call last):
      ...
    Invariants: Boat_Class needs the required attributes: ('name', 'max_crew')
      Instead it got: (name = 'Seascape 18')
    >>> errors
    [Required_Missing(u"Boat_Class needs the required attributes: ('name', 'max_crew')", u"Instead it got: (name = 'Seascape 18')")]

    >>> errors = []
    >>> SRM.Boat_Class (max_crew = 4, on_error = errors.append)
    Traceback (most recent call last):
      ...
    Invariants: Boat_Class needs the primary attribute: ('name',)
      Instead it got: (max_crew = 4)
    >>> errors
    [Required_Missing(u"Boat_Class needs the primary attribute: ('name',)", u'Instead it got: (max_crew = 4)')]
    >>> print formatted (MOM.Error.as_json_cargo (* errors))
    [ { 'attributes' :
    ( 'name' ,)
      , 'bindings' :
          [
            ( 'name'
            , None
            )
          ]
      , 'description' : 'Instead it got: (max_crew = 4)'
      , 'explanation' : 'All required attributes must be supplied'
      , 'head' : "Boat_Class needs the primary attribute: ('name',)"
      , 'is_required' : True
      }
    ]

    >>> errors = []
    >>> SRM.Boat_Class (on_error = errors.append)
    Traceback (most recent call last):
      ...
    Invariants: Boat_Class needs the primary attribute: ('name',)
      Instead it got: ()
      Condition `max_crew_not_empty` : max_crew is not None and max_crew != ''
        max_crew = None
      Condition `name_not_empty` : name is not None and name != ''
        name = ''
    >>> errors
    [Required_Missing(u"Boat_Class needs the primary attribute: ('name',)", u'Instead it got: ()'), Invariants(Required_Empty(u'Boat_Class', Condition `max_crew_not_empty` : max_crew is not None and max_crew != ''
        max_crew = None), Required_Empty(u'Boat_Class', Condition `name_not_empty` : name is not None and name != ''
        name = ''))]

    >>> errors = []
    >>> SRM.Boat (sail_number = "187042", raw = True, on_error = errors.append)
    Traceback (most recent call last):
      ...
    Invariants: Boat needs the primary attribute: ('left',)
      Instead it got: (sail_number = 187042)
    >>> print formatted (MOM.Error.as_json_cargo (* errors))
    [ { 'attributes' :
    ( 'left' ,)
      , 'bindings' :
          [
            ( 'left'
            , None
            )
          ]
      , 'description' : 'Instead it got: (sail_number = 187042)'
      , 'explanation' : 'All required attributes must be supplied'
      , 'head' : "Boat needs the primary attribute: ('left',)"
      , 'is_required' : True
      , 'missing_t' :
          { 'left' :
              [ 'name'
              , 'max_crew'
              ]
          }
      }
    ]

    >>> errors = []
    >>> SRM.Boat (sail_number = "-187042", raw = True, on_error = errors.append)
    Traceback (most recent call last):
      ...
    Invariants: Condition `AC_check_sail_number_0` : 0 <= sail_number <= 999999
        sail_number = -187042
      Boat needs the primary attribute: ('left',)
      Instead it got: (sail_number = -187042)

    >>> print formatted (MOM.Error.as_json_cargo (* errors))
    [ { 'attributes' :
    ( 'left' ,)
      , 'bindings' :
          [
            ( 'left'
            , None
            )
          ]
      , 'description' : 'Instead it got: (sail_number = -187042)'
      , 'explanation' : 'All required attributes must be supplied'
      , 'head' : "Boat needs the primary attribute: ('left',)"
      , 'is_required' : True
      , 'missing_t' :
          { 'left' :
              [ 'name'
              , 'max_crew'
              ]
          }
      }
    , { 'attributes' :
    [ 'sail_number' ]
      , 'bindings' :
          [
            ( 'sail_number'
            , '-187042'
            )
          ]
      , 'head' : '0 <= sail_number <= 999999'
      }
    ]

"""

from _GTW.__test__.model import *
import datetime

__test__ = Scaffold.create_test_dict (_test_code)

### __END__ GTW.__test__.Boat
