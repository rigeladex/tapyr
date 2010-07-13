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
#     1-Jul-2010 (CT) `race_results` as example of composite-collection added
#    13-Jul-2010 (CT) Changed to use `DB_Man` for migration
#                     (instead of `Scope.copy`)
#    ««revision-date»»···
#--

from _GTW.__test__.model import *

class _migration_Scaffold_ (Scaffold) :

    _real_name = "Scaffold"

    Backend_Parameters = dict \
        ( HPS = "'hps:///test.hps'"
        , SQL = "'sqlite:///test.sql'"
        , POS = "'postgresql://regtest:regtest@localhost/test'"
        , MYS = "'mysql://:@localhost/test'"
        )

Scaffold = _migration_Scaffold_ # end class

_test_code = r"""
    >>> scope = Scaffold.scope (%(p1)s, %(n1)s) # doctest:+ELLIPSIS
    Creating new scope MOMT__...
    >>> apt_s, url_s = scope.app_type, scope.db_url
    >>> PAP = scope.PAP
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
    >>> b   = SRM.Boat.instance_or_new (u'Optimist', u"AUT", u"1107", raw = True)
    >>> p   = PAP.Person.instance_or_new (u"Tanzer", u"Christian")
    >>> s   = SRM.Sailor.instance_or_new (p.epk_raw, nation = u"AUT", mna_number = u"29676", raw = True) ### 1
    >>> rev = SRM.Regatta_Event (dict (start = "20080501", raw = True), u"Himmelfahrt", raw = True)
    >>> reg = SRM.Regatta_C (rev.epk_raw, boat_class = bc.epk_raw, raw = True)
    >>> reh = SRM.Regatta_H (rev.epk_raw, handicap = u"Yardstick",  raw = True)
    >>> bir = SRM.Boat_in_Regatta (b.epk_raw, reg.epk_raw, skipper = s.epk_raw, raw = True)

    >>> bir.set (race_results = \
    ... [SRM.Race_Result (points = 8), SRM.Race_Result (points = 4)])
    1

    >>> scope.commit ()
    >>> scope.MOM.Id_Entity.count_transitive
    33
    >>> int (scope.query_changes ().count ())
    34
    >>> int (scope.ems.max_cid)
    34

    >>> bc.set (loa = 2.43)
    1
    >>> SRM.Boat_Class.instance ("Laser").set (sail_area = 7.06, loa = 4.064, beam = 1.422)
    3
    >>> SRM.Boat_Class.instance ("Seascape 18").set (loa = 5.45, beam = 2.45, sail_area = 23)
    3
    >>> scope.commit ()

    >>> scope.MOM.Id_Entity.count_transitive
    33
    >>> int (scope.query_changes ().count ())
    37
    >>> int (scope.ems.max_cid)
    37
    >>> len (scope.SRM.Regatta_Event.query ().first ().regattas)
    2

    Save contents of scope to database and destroy scope:

    >>> scope.ems.compact ()
    >>> scope.destroy ()

    Now, we migrate all objects and the change history to a new backend. All
    entities, changes, cids, and pids should be identical afterwards:

    >>> db_url = "hps:////tmp/gtw_test_migration.gtw"
    >>> apt_t, url_t = Scaffold.app_type_and_url (db_url)
    >>> apt_t.delete_database (url_t)
    >>> db_man_s = Scaffold.DB_Man.connect (apt_s, url_s)
    >>> db_man_t = Scaffold.DB_Man.create  (apt_t, url_t, db_man_s)
    >>> db_man_s.destroy ()
    >>> db_man_t.destroy ()

    >>> scope_s = Scaffold.scope (url_s, create = False) # doctest:+ELLIPSIS
    Loading scope MOMT__...
    >>> scope_t = Scaffold.scope (url_t, create = False) # doctest:+ELLIPSIS
    Loading scope MOMT__...

    >>> tuple (s.MOM.Id_Entity.count_transitive for s in (scope_s, scope_t))
    (33, 33)
    >>> all (s.as_pickle_cargo () == t.as_pickle_cargo () for (s, t) in zip (scope_s, scope_t))
    True
    >>> int (scope_t.ems.max_cid)
    37
    >>> len (scope_t.SRM.Regatta_Event.query ().first ().regattas)
    2

    Now we delete the original database and then migrate back into the
    original app-type/backend. Again, all entities, changes, cids,
    and pids should still be identical:

    >>> scope_s.destroy ()
    >>> scope_t.destroy ()
    >>> apt_s.delete_database (url_s)
    >>> db_man_t = Scaffold.DB_Man.connect (apt_t, url_t)
    >>> db_man_u = Scaffold.DB_Man.create  (apt_s, url_s, db_man_t)
    >>> db_man_t.destroy ()
    >>> db_man_u.destroy ()

    >>> scope_t = Scaffold.scope (url_t, create = False) # doctest:+ELLIPSIS
    Loading scope MOMT__...
    >>> scope_u = Scaffold.scope (url_s, create = False) # doctest:+ELLIPSIS
    Loading scope MOMT__...

    >>> tuple (s.MOM.Id_Entity.count_transitive for s in (scope_t, scope_u))
    (33, 33)
    >>> all (s.as_pickle_cargo () == t.as_pickle_cargo () for (s, t) in zip (scope_t, scope_u))
    True
    >>> int (scope_u.ems.max_cid)
    37
    >>> len (scope_u.SRM.Regatta_Event.query ().first ().regattas)
    2

    Lets clean up::

    >>> scope_t.destroy ()
    >>> scope_u.destroy ()

    >>> apt_s.delete_database (url_s)
    >>> apt_t.delete_database (url_t)

"""

__test__ = Scaffold.create_test_dict (_test_code)

### __END__ migration
