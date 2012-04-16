# -*- coding: iso-8859-15 -*-
# Copyright (C) 2010-2012 Mag. Christian Tanzer All rights reserved
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
#    15-Apr-2012 (CT) Adapted to changes of `MOM.Error`
#    ««revision-date»»···
#--

_test_code = """
    >>> scope = Scaffold.scope (%(p1)s, %(n1)s) # doctest:+ELLIPSIS
    Creating new scope MOMT__...
    >>> SRM = scope.SRM
    >>> SRM.Boat_Class ("Optimist", max_crew = 1)
    GTW.OMP.SRM.Boat_Class (u'optimist')
    >>> print scope.SRM.Boat_Class.count ### 1
    1
    >>> laser = SRM.Boat_Class ("Laser", max_crew = 1)
    >>> print scope.SRM.Boat_Class.count ### 2
    2

    >>> scope.SRM.Boat_Class.query (name = u'optimist').all ()
    [GTW.OMP.SRM.Boat_Class (u'optimist')]
    >>> scope.SRM.Boat_Class.instance (u'Optimist')
    GTW.OMP.SRM.Boat_Class (u'optimist')
    >>> SRM.Boat.instance_or_new (u'Optimist', u"AUT", u"1107", raw = True) ### 1
    GTW.OMP.SRM.Boat ((u'optimist', ), u'AUT', 1107, u'')
    >>> print scope.SRM.Boat.count ### 3
    1
    >>> scope.SRM.Boat.query_s ().all ()
    [GTW.OMP.SRM.Boat ((u'optimist', ), u'AUT', 1107, u'')]
    >>> scope.commit ()

    >>> SRM.Boat.instance_or_new (u'Optimist', u"AUT", u"1107", raw = True) ### 2
    GTW.OMP.SRM.Boat ((u'optimist', ), u'AUT', 1107, u'')
    >>> print scope.SRM.Boat.count ### 4
    1
    >>> scope.SRM.Boat.query_s ().all ()
    [GTW.OMP.SRM.Boat ((u'optimist', ), u'AUT', 1107, u'')]

    >>> b = SRM.Boat.instance_or_new (u'Optimist', u"AUT", u"1107", raw = True) ### 3
    >>> c = SRM.Boat (u"Optimist", None, "42", "OE", raw = True)

    >>> print scope.SRM.Boat.count ### 5
    2
    >>> scope.SRM.Boat.query_s ().all ()
    [GTW.OMP.SRM.Boat ((u'optimist', ), '', 42, u'oe'), GTW.OMP.SRM.Boat ((u'optimist', ), u'AUT', 1107, u'')]

    >>> print (c.sail_number, c.sail_number_head, c.sail_number_tail)
    (42, u'OE', u'42')
    >>> print (c.FO.sail_number, c.FO.sail_number_head, c.FO.sail_number_tail)
    ('42', u'OE', u'42')
    >>> print (b.sail_number, b.sail_number_head, b.sail_number_tail)
    (1107, u'', u'1107')

    >>> s1 = TFL.Sorted_By ("name")
    >>> s2 = TFL.Sorted_By ("-name")
    >>> SRM.Boat_Class.query ().order_by (s1).all ()
    [GTW.OMP.SRM.Boat_Class (u'laser'), GTW.OMP.SRM.Boat_Class (u'optimist')]
    >>> SRM.Boat_Class.query ().order_by (s1).order_by (s2).all ()
    [GTW.OMP.SRM.Boat_Class (u'optimist'), GTW.OMP.SRM.Boat_Class (u'laser')]

    >>> print SRM.Boat.sail_number.Q_Raw.EQ
    <Attr.Equal __raw_sail_number.EQ [==]>
    >>> rf = SRM.Boat.sail_number.Q_Raw.EQ ("1107")
    >>> print rf
    Q.__raw_sail_number == 1107

    >>> rf (b)
    True

    >>> getattr (b, "__raw_sail_number", "No raw value???")
    u'1107'

    >>> bq = SRM.Boat.query_s ()
    >>> bq.all ()
    [GTW.OMP.SRM.Boat ((u'optimist', ), '', 42, u'oe'), GTW.OMP.SRM.Boat ((u'optimist', ), u'AUT', 1107, u'')]
    >>> SRM.Boat.query_s (SRM.Boat.sail_number.Q_Raw.EQ ("1107")).all ()
    [GTW.OMP.SRM.Boat ((u'optimist', ), u'AUT', 1107, u'')]
    >>> SRM.Boat.query_s (SRM.Boat.sail_number.Q_Raw.AC ("11")).all ()
    [GTW.OMP.SRM.Boat ((u'optimist', ), u'AUT', 1107, u'')]

    >>> print scope.SRM.Boat.count ### 6
    2

    >>> b.set (left = laser)
    Traceback (most recent call last):
      ...
    AttributeError: Init-only attribute `GTW.OMP.SRM.Boat.left` cannot be changed from `(u'optimist')` to `(u'laser')` after object creation

    >>> print scope.SRM.Boat.count ### 7
    2
    >>> scope.commit ()

    >>> SRM.Boat.query_s ().all () ### before Name_Clash
    [GTW.OMP.SRM.Boat ((u'optimist', ), '', 42, u'oe'), GTW.OMP.SRM.Boat ((u'optimist', ), u'AUT', 1107, u'')]

    >>> d = SRM.Boat (SRM.Boat_Class ("Optimist", max_crew = 1), "AUT", "1134")
    Traceback (most recent call last):
      ...
    Name_Clash: new definition of GTW.OMP.SRM.Boat_Class (u'optimist') clashes with existing GTW.OMP.SRM.Boat_Class (u'optimist')

    >>> print scope.SRM.Boat.count ### 8
    2

    >>> SRM.Boat.query_s ().all () ### after Name_Clash
    [GTW.OMP.SRM.Boat ((u'optimist', ), '', 42, u'oe'), GTW.OMP.SRM.Boat ((u'optimist', ), u'AUT', 1107, u'')]

    >>> print sorted (b.b_class._pred_man.errors.items ()) ### before invariant errors
    [('object', []), ('region', []), ('system', [])]

    >>> b.b_class.max_crew = 0
    Traceback (most recent call last):
      ...
    Invariant: Condition `AC_check_max_crew_1` : 1 <= max_crew <= 4
        max_crew = 0
    >>> print sorted (b.b_class._pred_man.errors.items ()) ### after invariant error from `setattr`
    [('object', []), ('region', []), ('system', [])]


    >>> errors = []
    >>> b.b_class.set (max_crew = 0)
    Traceback (most recent call last):
      ...
    Invariants: Condition `AC_check_max_crew_1` : 1 <= max_crew <= 4
        max_crew = 0
    >>> print sorted (b.b_class._pred_man.errors.items ()) ### after invariant error from `.set (max_crew = 0)`
    [('object', [Invariant(GTW.OMP.SRM.Boat_Class (u'optimist'), Condition `AC_check_max_crew_1` : 1 <= max_crew <= 4
        max_crew = 0)]), ('region', []), ('system', [])]
    >>> errors
    []
    >>> b.b_class.set (max_crew = 5, on_error = errors.append)
    1
    >>> print sorted (b.b_class._pred_man.errors.items ()) ### after invariant error from `.set (max_crew = 5)`
    [('object', [Invariant(GTW.OMP.SRM.Boat_Class (u'optimist'), Condition `AC_check_max_crew_1` : 1 <= max_crew <= 4
        max_crew = 5)]), ('region', []), ('system', [])]
    >>> errors
    [Invariants(Invariant(GTW.OMP.SRM.Boat_Class (u'optimist'), Condition `AC_check_max_crew_1` : 1 <= max_crew <= 4
        max_crew = 5),)]

    >>> b.b_class.set (max_crew = None)
    Traceback (most recent call last):
      ...
    Invariants: Condition `max_crew_not_empty` : max_crew is not None and max_crew != ''
        max_crew = None
    >>> print sorted (b.b_class._pred_man.errors.items ()) ### after invariant error from `.set (max_crew = None)`
    [('object', [Required_Empty(GTW.OMP.SRM.Boat_Class (u'optimist'), Condition `max_crew_not_empty` : max_crew is not None and max_crew != ''
        max_crew = None)]), ('region', []), ('system', [])]

    >>> b.b_class.max_crew = None
    Traceback (most recent call last):
      ...
    Required_Empty: Condition `max_crew_not_empty` : max_crew is not None and max_crew != ''
        max_crew = None

    >>> errors = []
    >>> SRM.Boat_Class ("Seascape 18", on_error = errors.append)
    Traceback (most recent call last):
      ...
    Invariants: GTW.OMP.SRM.Boat_Class needs the required attributes: ('max_crew',); Instead it got: ('Seascape 18')
    >>> errors
    [Required_Missing(u"GTW.OMP.SRM.Boat_Class needs the required attributes: ('max_crew',)", u"Instead it got: ('Seascape 18')")]

    >>> errors = []
    >>> SRM.Boat_Class (max_crew = 4, on_error = errors.append)
    Traceback (most recent call last):
      ...
    Required_Missing: GTW.OMP.SRM.Boat_Class needs the required attributes: ('name',); Instead it got: (max_crew = 4)
    >>> errors
    [Required_Missing(u"GTW.OMP.SRM.Boat_Class needs the required attributes: ('name',)", u'Instead it got: (max_crew = 4)')]

    >>> errors = []
    >>> SRM.Boat_Class (on_error = errors.append)
    Traceback (most recent call last):
      ...
    Required_Missing: GTW.OMP.SRM.Boat_Class needs the required attributes: ('name',); Instead it got: ()
    >>> errors
    [Required_Missing(u"GTW.OMP.SRM.Boat_Class needs the required attributes: ('name',)", u'Instead it got: ()')]

    >>> scope.destroy ()

"""

from _GTW.__test__.model import *

__test__ = Scaffold.create_test_dict (_test_code)

### __END__ GTW.__test__.Boat
