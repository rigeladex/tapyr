# -*- coding: iso-8859-15 -*-
# Copyright (C) 2011-2012 Martin Glueck All rights reserved
# Langstrasse 4, A--2244 Spannberg, Austria. martin@mangari.org
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
#    GTW.__test__.ac_query
#
# Purpose
#    Testcases for the auto completion interface
#
# Revision Dates
#     8-Jun-2011 (MG) Creation
#    12-Sep-2011 (CT) Tests for `lifetime` added
#    11-Nov-2011 (CT) Add tests for `Q.__eq__` and `Q.CONTAINS`
#     5-Dec-2011 (CT) Add tests for `Sailor.AQ.left.AC(dict(last_name = "Tan"))`
#    15-Apr-2012 (CT) Adapt to change of `MOM.Attr.Filter.Composite`
#    10-Oct-2012 (CT) Add test for `position`
#    10-Oct-2012 (CT) Add test for `raw_query_attrs`
#    12-Oct-2012 (CT) Adapt to repr change of `An_Entity`
#    ««revision-date»»···
#--

from   __future__  import unicode_literals

_attr_ac_query = """
    >>> scope = Scaffold.scope (%(p1)s, %(n1)s) # doctest:+ELLIPSIS
    Creating new scope MOMT__...
    >>> PAP = scope.PAP
    >>> SRM = scope.SRM
    >>> p1 = PAP.Person ("Glueck",          "Martin")
    >>> p2 = PAP.Person ("Tanzer",          "Christian", "", "Mag.", lifetime = dict (start = u"26.9.1959", raw = True))
    >>> p3 = PAP.Person ("Franz-Ferdinand", "Karl")
    >>> p4 = PAP.Person ("Tanzer", "Egon", lifetime = dict (start = u"1907/03/08", finish = "1994/08/04", raw = True))
    >>> s2 = SRM.Sailor (p2)
    >>> for value in "Ma", "martin", "CHRi" :
    ...    q = PAP.Person.AQ.first_name.AC (value)
    ...    for o in (p1, p2, p3) :
    ...        print value, o.first_name, q (o)
    Ma martin True
    Ma christian False
    Ma karl False
    martin martin True
    martin christian False
    martin karl False
    CHRi martin False
    CHRi christian True
    CHRi karl False

    >>> for value in "Gl", "Glueck", "Ferdinand" :
    ...    q = PAP.Person.AQ.last_name.AC (value)
    ...    for o in (p1, p2, p3) :
    ...        print value, o.last_name, q (o)
    Gl glueck True
    Gl tanzer False
    Gl franz-ferdinand False
    Glueck glueck True
    Glueck tanzer False
    Glueck franz-ferdinand False
    Ferdinand glueck False
    Ferdinand tanzer False
    Ferdinand franz-ferdinand True

    >>> q1  = PAP.Person.AQ.lifetime.AC (dict (start = "1959/09/26"))
    >>> q2  = PAP.Person.AQ.lifetime.AC (dict (start = "1907/03/08", finish = "1994/08/04"))
    >>> q3  = PAP.Person.AQ.lifetime.AC (dict (finish = "1994/08/04"))
    >>> q4  = PAP.Person.lifetime.AQ.EQ (dict (start = "1907", finish = "1994"))
    >>> q5  = PAP.Person.first_name.AQ.CONTAINS ("ti")
    >>> q6  = PAP.Person.AQ.lifetime.AC (dict (start = "1959"))
    >>> q7 = PAP.Person.AQ.lifetime.start.AC ("1959/09/26")

    >>> print q1
    Q.lifetime.start == 1959-09-26
    >>> print q2
    <Filter_And [Q.lifetime.finish == 1994-08-04, Q.lifetime.start == 1907-03-08]>
    >>> print q4
    <Filter_And [Q.lifetime.finish.between (datetime.date(1994, 1, 1), datetime.date(1994, 12, 31)), Q.lifetime.start.between (datetime.date(1907, 1, 1), datetime.date(1907, 12, 31))]>
    >>> print q5
    Q.first_name.contains (u'ti',)
    >>> print q6
    Q.lifetime.start.between (datetime.date(1959, 1, 1), datetime.date(1959, 12, 31))

    >>> print q7
    Q.lifetime.start == 1959-09-26

    >>> print " and ".join (str (p) for p in q2.predicates)
    Q.lifetime.finish == 1994-08-04 and Q.lifetime.start == 1907-03-08

    >>> PAP.Person.query_s (q1).all ()
    [PAP.Person (u'tanzer', u'christian', u'', u'mag.')]
    >>> PAP.Person.query_s (q2).all ()
    [PAP.Person (u'tanzer', u'egon', u'', u'')]
    >>> PAP.Person.query_s (q1 | q3).all ()
    [PAP.Person (u'tanzer', u'christian', u'', u'mag.'), PAP.Person (u'tanzer', u'egon', u'', u'')]
    >>> PAP.Person.query_s (q4).all ()
    [PAP.Person (u'tanzer', u'egon', u'', u'')]
    >>> list (p.ui_display for p in PAP.Person.query_s (q5))
    [u'Glueck Martin', u'Tanzer Christian, Mag.']

    >>> PAP.Person.query_s (q6).all ()
    [PAP.Person (u'tanzer', u'christian', u'', u'mag.')]

    >>> PAP.Person.query_s (q7).all ()
    [PAP.Person (u'tanzer', u'christian', u'', u'mag.')]

    >>> q = PAP.Person.AQ.last_name.AC ("Franz")
    >>> print " or ".join (str (p) for p in q.predicates)
    Q.last_name.startswith (u'franz',) or Q.last_name.contains (u'-franz',)
    >>> q = PAP.Person.AQ.last_name.AC ("Franz-F")
    >>> print q
    Q.last_name.startswith (u'franz-f',)

    >>> qs1  = SRM.Sailor.AQ.left.AC (dict (last_name = "Tan"))
    >>> qs2  = SRM.Sailor.AQ.left.last_name.AC ("Tan")

    >>> print qs1
    <Filter_Or [Q.left.last_name.startswith (u'tan',), Q.left.last_name.contains (u'-tan',)]>
    >>> print qs2
    <Filter_Or [Q.left.last_name.startswith (u'tan',), Q.left.last_name.contains (u'-tan',)]>

    >>> SRM.Sailor.query_s (qs1).all ()
    [SRM.Sailor ((u'tanzer', u'christian', u'', u'mag.'), '', None, u'')]
    >>> SRM.Sailor.query_s (qs2).all ()
    [SRM.Sailor ((u'tanzer', u'christian', u'', u'mag.'), '', None, u'')]

    >>> a1 = PAP.Address ("Langstrasse 4",    "2244", "Spannberg", "Austria")
    >>> a2 = PAP.Address ("Glasauergasse 32", "1130", "Wien",      "Austria")
    >>> for value in "22", "11", "10" :
    ...    q = PAP.Address.AQ.zip.AC (value)
    ...    for o in (a1, a2) :
    ...        print value, o.zip, q (o)
    22 2244 True
    22 1130 False
    11 2244 False
    11 1130 True
    10 2244 False
    10 1130 False

    >>> SRM   = scope.SRM
    >>> opti  = SRM.Boat_Class ("Optimist", max_crew = 1)
    >>> b1    = SRM.Boat.instance_or_new (u'Optimist', u"AUT", u"1107", raw = True) ### 1
    >>> b2    = SRM.Boat.instance_or_new (u'Optimist', u"AUT", u"1208", raw = True) ### 2
    >>> for value in "11", "12" :
    ...    q = SRM.Boat.AQ.sail_number.AC (value)
    ...    for o in (b1, b2) :
    ...        print value, o.sail_number, q (o)
    11 1107 True
    11 1208 False
    12 1107 False
    12 1208 True

    >>> a3 = PAP.Address ("Glasauergasse 32/3", "1130", "Wien", "Austria", raw = True)
    >>> a3p = PAP.Address_Position (a3, position = dict (lat = "48.190111", lon = "16.26867"), raw = True)
    >>> a3p.position
    MOM.Position (48.190111, 16.26867)
    >>> a3.gps
    PAP.Address_Position ((u'glasauergasse 32/3', u'1130', u'wien', u'austria'), (48.190111, 16.26867))

    >>> a4 = PAP.Address ("Glasauergasse 32/2", "1130", "Wien", "Austria", raw = True)
    >>> a4p = PAP.Address_Position (a4, position = ("48d 11m 25s", "16d 16m 7s"), raw = True)
    >>> a4p.position
    MOM.Position (48.1902777778, 16.2686111111)
    >>> print a4p
    ((u'glasauergasse 32/2', u'1130', u'wien', u'austria'), (48.1902777778, 16.2686111111))
    >>> print a4p.position
    (48.1902777778, 16.2686111111)
    >>> print a4p.__class__.position.as_code (a4p.position)
    (48.1902777778, 16.2686111111)

    >>> p42 = scope.MOM.Position (42.4242, 137.137137)
    >>> p42
    MOM.Position (42.4242, 137.137137)
    >>> print p42.as_code ()
    MOM.Position (42.4242, 137.137137)
    >>> print p42.attr_as_code ()
    42.4242, 137.137137

    >>> p42r = scope.MOM.Position ("42d42m42s", "137d13m7.137s", raw = True)
    >>> p42r
    MOM.Position (42.7116666667, 137.218649167)

    >>> list (PAP.Person.raw_query_attrs (["first_name"], dict (first_name = "Martin")))
    [Q.first_name == martin]

    >>> list (PAP.Address_Position.raw_query_attrs (["position"], dict (position = dict (lat = "48.190111"))))
    [Q.position.lat == 48.190111]

    >>> list (PAP.Address_Position.raw_query_attrs (["position"], dict (position = dict (lat = "48d 11m 25s"))))
    [Q.position.lat == 48.1902777778]

    >>> scope.destroy ()
"""

_epk_splitter_test = """
    >>> scope = Scaffold.scope (%(p1)s, %(n1)s) # doctest:+ELLIPSIS
    Creating new scope MOMT__...
    >>> PAP = scope.PAP
    >>> scope.PAP.Person.epk_splitter ("Ma")
    [(u'Ma',)]
    >>> scope.PAP.Person.epk_splitter ("Martin G")
    [(u'Martin G',), (u'Martin', u'G')]
    >>> scope.PAP.Person.epk_splitter ("Gl Ma")
    [(u'Gl Ma',), (u'Gl', u'Ma')]
    >>> scope.PAP.Person.epk_splitter ("Van der Bel")
    [(u'Van der Bel',), (u'Van der', u'Bel'), (u'Van', u'der Bel')]
    >>> scope.destroy ()
"""

_ac_query = """
    >>> scope = Scaffold.scope (%(p1)s, %(n1)s) # doctest:+ELLIPSIS
    Creating new scope MOMT__...
    >>> PAP = scope.PAP
    >>> _ = PAP.Person ("Glueck",          "Martin")
    >>> _ = PAP.Person ("Tanzer",          "Christian", "", "Mag.")
    >>> _ = PAP.Person ("Franz-Ferdinand", "Karl")
    >>> _ = PAP.Person ("Van der Bellen",  "Alexander")
    >>> _ = PAP.Person ("van Persie",      "Robin")
    >>> scope.commit    ()

    >>> for acs in ("Ma", "Ta", "Van", "Van der B") :
    ...     for p, qs in enumerate (PAP.Person.ac_query_auto_split (acs)) :
    ...         print p, acs
    ...         for o in sorted (qs, key = lambda p : p.last_name) :
    ...             print " ", o
    0 Ma
      (u'glueck', u'martin', u'', u'')
      (u'tanzer', u'christian', u'', u'mag.')
    0 Ta
      (u'tanzer', u'christian', u'', u'mag.')
    0 Van
      (u'van der bellen', u'alexander', u'', u'')
      (u'van persie', u'robin', u'', u'')
    0 Van der B
      (u'van der bellen', u'alexander', u'', u'')
    1 Van der B
    2 Van der B
    >>> scope.destroy ()
"""

from _GTW.__test__.model import *

__test__ = dict \
    ( Scaffold.create_test_dict
        ( dict
            ( attr_ac_query = _attr_ac_query
            , ac_query      = _ac_query
            )
        )
    , ** Scaffold.create_test_dict
        (dict (ekp_splitter = _epk_splitter_test), backends = ("HPS", ))
    )

### __END__ GTW.__test__.ac_query
