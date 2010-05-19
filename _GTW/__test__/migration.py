# -*- coding: iso-8859-1 -*-
# Copyright (C) 2010 Mag. Christian Tanzer All rights reserved
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
#    migration
#
# Purpose
#    Test scope migrations
#
# Revision Dates
#    19-May-2010 (CT) Creation
#    ««revision-date»»···
#--

from _GTW.__test__.model import *

_test_code = r"""
    >>> scope = Scaffold.scope (%(p1)s, %(n1)s) # doctest:+ELLIPSIS
    Creating new scope MOMT__...
    >>> SRM = scope.SRM

    >>> x = SRM.Boat_Class ("29er",              max_crew = 2)
    >>> x = SRM.Boat_Class ("420er",             max_crew = 2)
    >>> x = SRM.Boat_Class ("470er",             max_crew = 2)
    >>> x = SRM.Boat_Class ("49er",              max_crew = 2)
    >>> x = SRM.Boat_Class ("Aquila Kiel",       max_crew = 3)
    >>> x = SRM.Boat_Class ("Aquila Schwert",    max_crew = 3)
    >>> x = SRM.Boat_Class ("Fam",               max_crew = 3)
    >>> x = SRM.Boat_Class ("Finn-Dinghy",       max_crew = 1)
    >>> x = SRM.Boat_Class ("Korsar",            max_crew = 2)
    >>> x = SRM.Boat_Class ("Laser",             max_crew = 1)
    >>> x = SRM.Boat_Class ("Laser 4.7",         max_crew = 1)
    >>> x = SRM.Boat_Class ("Laser Master",      max_crew = 1)
    >>> x = SRM.Boat_Class ("Laser Radial",      max_crew = 1)
    >>> x = SRM.Boat_Class ("O-Jolle",           max_crew = 1)
    >>> x = SRM.Boat_Class ("Optimist",          max_crew = 1)
    >>> x = SRM.Boat_Class ("Pirat Regatta",     max_crew = 2)
    >>> x = SRM.Boat_Class ("Pirat Klassik",     max_crew = 2)
    >>> x = SRM.Boat_Class ("Pirat Schulboot",   max_crew = 2)
    >>> x = SRM.Boat_Class ("Pirat",             max_crew = 2)
    >>> x = SRM.Boat_Class ("Robby Jolle",       max_crew = 2)
    >>> x = SRM.Boat_Class ("Seascape 18",       max_crew = 4)
    >>> x = SRM.Boat_Class ("Zoom8",             max_crew = 1)

    >>> scope.commit ()

    >>> x = SRM.Boat ((u'Optimist',),    "Austria", 1)
    >>> x = SRM.Boat ((u'Optimist',),    "Austria", 2)
    >>> x = SRM.Boat ((u'Laser',),       "Austria", 3)
    >>> x = SRM.Boat ((u'Seascape 18',), "Austria", 14)

    >>> scope.commit ()

    >>> bc  = SRM.Boat_Class.instance ("Optimist")
    >>> rev = SRM.Regatta_Event (dict (start = "20080501", raw = True), u"Himmelfahrt", raw = True)
    >>> reg = SRM.Regatta_C (rev.epk_raw, boat_class = bc.epk_raw, raw = True)
    >>> reh = SRM.Regatta_H (rev.epk_raw, handicap = u"Yardstick",  raw = True)

    >>> scope.commit ()
    >>> scope.MOM.Id_Entity.count_transitive
    29
    >>> int (scope.query_changes ().count ())
    29
    >>> scope.ems.max_cid
    29

    >>> bc.set (loa = 2.43)
    1
    >>> SRM.Boat_Class.instance ("Laser").set (sail_area = 7.06, loa = 4.064, beam = 1.422)
    3
    >>> SRM.Boat_Class.instance ("Seascape 18").set (loa = 5.45, beam = 2.45, sail_area = 23)
    3
    >>> scope.commit ()

    >>> scope.MOM.Id_Entity.count_transitive
    29
    >>> int (scope.query_changes ().count ())
    32
    >>> int (scope.ems.max_cid)
    32

    Now, we migrate all objects and the change history to a new scope. All
    entities, changes, cids, and pids should be identical::

    >>> db_uri = "/tmp/gtw_test.gtw"
    >>> apt, uri = Scaffold.app_type_and_uri (None, db_uri)
    >>> scop2 = scope.migrate (apt, uri)
    >>> tuple (s.MOM.Id_Entity.count_transitive for s in (scope, scop2))
    (29, 29)
    >>> sorted (scope.user_diff (scop2).iteritems ())
    []
    >>> scope.user_equal (scop2)
    True
    >>> all (s.as_pickle_cargo () == t.as_pickle_cargo () for (s, t) in zip (scope, scop2))
    True
    >>> int (scop2.ems.max_cid)
    32

    >>> scop2.destroy ()

    After saving and restoring from `db_uri`, all entities, changes, cids,
    and pids should still be identical::

    >>> scop3 = MOM.Scope.load (apt, db_uri)
    >>> tuple (s.MOM.Id_Entity.count_transitive for s in (scope, scop3))
    (29, 29)
    >>> sorted (scope.user_diff (scop3).iteritems ())
    []
    >>> scope.user_equal (scop3)
    True
    >>> all (s.as_pickle_cargo () == t.as_pickle_cargo () for (s, t) in zip (scope, scop3))
    True
    >>> int (scop3.ems.max_cid)
    32

    Now we delete the original database and then migrate back from `scop3`
    into that app-type/backend. Again, all entities, changes, cids,
    and pids should still be identical::

    >>> apt, db_uri = scope.app_type, scope.db_uri
    >>> scope.destroy ()
    >>> if db_uri :
    ...    apt.delete_database (db_uri)
    >>> scop4 = scop3.migrate (apt, db_uri)

    >>> tuple (s.MOM.Id_Entity.count_transitive for s in (scop3, scop4))
    (29, 29)
    >>> sorted (scop3.user_diff (scop4).iteritems ())
    []
    >>> scop3.user_equal (scop4)
    True
    >>> all (s.as_pickle_cargo () == t.as_pickle_cargo () for (s, t) in zip (scop3, scop4))
    True
    >>> int (scop4.ems.max_cid)
    32

    Lets clean up::

    >>> scop3.destroy ()
    >>> scop4.destroy ()
"""

__test__ = Scaffold.create_test_dict (_test_code)

### __END__ migration
