# -*- coding: iso-8859-15 -*-
# Copyright (C) 2012 Mag. Christian Tanzer All rights reserved
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
#    GTW.__test__.Subjects
#
# Purpose
#    Test GTW.OMP.PAP.Subject subclasses and links
#
# Revision Dates
#    24-Mar-2012 (CT) Creation
#    ««revision-date»»···
#--

from   __future__  import absolute_import, division, print_function, unicode_literals

_test_code = """
    >>> scope = Scaffold.scope (%(p1)s, %(n1)s) # doctest:+ELLIPSIS
    Creating new scope MOMT__...
    >>> PAP = scope.PAP

    >>> print (PAP.Subject.count_transitive, PAP.Company.count, PAP.Person.count)
    0 0 0

    >>> pg = PAP.Person ("Glueck", "Martin")
    >>> ps = PAP.Person ("Schlatterbeck", "Ralf")
    >>> pt = PAP.Person ("Tanzer", "Christian")
    >>> print (PAP.Subject.count_transitive, PAP.Company.count, PAP.Person.count)
    3 0 3

    >>> cl = PAP.Company ("Lucky Software", short_name = "LS")
    >>> co = PAP.Company ("Open Source Consulting", short_name = "OSC")
    >>> print (PAP.Subject.count_transitive, PAP.Company.count, PAP.Person.count)
    5 2 3

    >>> PAP.Subject.query_s ().all ()
    [GTW.OMP.PAP.Person (u'glueck', u'martin', u'', u''), GTW.OMP.PAP.Company (u'lucky software'), GTW.OMP.PAP.Company (u'open source consulting'), GTW.OMP.PAP.Person (u'schlatterbeck', u'ralf', u'', u''), GTW.OMP.PAP.Person (u'tanzer', u'christian', u'', u'')]
    >>> PAP.Company.query_s ().all ()
    [GTW.OMP.PAP.Company (u'lucky software'), GTW.OMP.PAP.Company (u'open source consulting')]
    >>> PAP.Person.query_s ().all ()
    [GTW.OMP.PAP.Person (u'glueck', u'martin', u'', u''), GTW.OMP.PAP.Person (u'schlatterbeck', u'ralf', u'', u''), GTW.OMP.PAP.Person (u'tanzer', u'christian', u'', u'')]

    >>> _ = PAP.Person_has_Email (pg, PAP.Email ("martin@mangari.org"))
    >>> _ = PAP.Person_has_Email (ps, PAP.Email ("ralf@runtux.com"))
    >>> _ = PAP.Person_has_Email (pt, PAP.Email ("tanzer@swing.co.at"))
    >>> _ = PAP.Person_has_Email (pt, PAP.Email ("tanzer@gg32.com"))

    >>> _ = PAP.Company_has_Email (cl, PAP.Email ("lucky@mangari.org"))
    >>> _ = PAP.Company_has_Email (co, PAP.Email ("office@runtux.com"))

    >>> PAP.Subject_has_Email.query_s ().all ()
    [GTW.OMP.PAP.Person_has_Email ((u'glueck', u'martin', u'', u''), (u'martin@mangari.org', )), GTW.OMP.PAP.Company_has_Email ((u'lucky software', ), (u'lucky@mangari.org', )), GTW.OMP.PAP.Company_has_Email ((u'open source consulting', ), (u'office@runtux.com', )), GTW.OMP.PAP.Person_has_Email ((u'schlatterbeck', u'ralf', u'', u''), (u'ralf@runtux.com', )), GTW.OMP.PAP.Person_has_Email ((u'tanzer', u'christian', u'', u''), (u'tanzer@gg32.com', )), GTW.OMP.PAP.Person_has_Email ((u'tanzer', u'christian', u'', u''), (u'tanzer@swing.co.at', ))]
    >>> PAP.Company_has_Email.query_s ().all ()
    [GTW.OMP.PAP.Company_has_Email ((u'lucky software', ), (u'lucky@mangari.org', )), GTW.OMP.PAP.Company_has_Email ((u'open source consulting', ), (u'office@runtux.com', ))]
    >>> PAP.Person_has_Email.query_s ().all ()
    [GTW.OMP.PAP.Person_has_Email ((u'glueck', u'martin', u'', u''), (u'martin@mangari.org', )), GTW.OMP.PAP.Person_has_Email ((u'schlatterbeck', u'ralf', u'', u''), (u'ralf@runtux.com', )), GTW.OMP.PAP.Person_has_Email ((u'tanzer', u'christian', u'', u''), (u'tanzer@gg32.com', )), GTW.OMP.PAP.Person_has_Email ((u'tanzer', u'christian', u'', u''), (u'tanzer@swing.co.at', ))]

    >>> PAP.Subject_has_Email.query_s (Q.right.address.ENDSWITH ("@mangari.org")).all ()
    [GTW.OMP.PAP.Person_has_Email ((u'glueck', u'martin', u'', u''), (u'martin@mangari.org', )), GTW.OMP.PAP.Company_has_Email ((u'lucky software', ), (u'lucky@mangari.org', ))]
    >>> PAP.Subject_has_Email.query_s (Q.right.address.CONTAINS (".co")).all ()
    [GTW.OMP.PAP.Company_has_Email ((u'open source consulting', ), (u'office@runtux.com', )), GTW.OMP.PAP.Person_has_Email ((u'schlatterbeck', u'ralf', u'', u''), (u'ralf@runtux.com', )), GTW.OMP.PAP.Person_has_Email ((u'tanzer', u'christian', u'', u''), (u'tanzer@gg32.com', )), GTW.OMP.PAP.Person_has_Email ((u'tanzer', u'christian', u'', u''), (u'tanzer@swing.co.at', ))]
    >>> PAP.Person_has_Email.query_s (Q.right.address.ENDSWITH ("@mangari.org")).all ()
    [GTW.OMP.PAP.Person_has_Email ((u'glueck', u'martin', u'', u''), (u'martin@mangari.org', ))]
    >>> PAP.Person_has_Email.query_s (Q.right.address.CONTAINS (".co")).all ()
    [GTW.OMP.PAP.Person_has_Email ((u'schlatterbeck', u'ralf', u'', u''), (u'ralf@runtux.com', )), GTW.OMP.PAP.Person_has_Email ((u'tanzer', u'christian', u'', u''), (u'tanzer@gg32.com', )), GTW.OMP.PAP.Person_has_Email ((u'tanzer', u'christian', u'', u''), (u'tanzer@swing.co.at', ))]

    >>> sorted (pg.emails, key = PAP.Email.sorted_by)
    [GTW.OMP.PAP.Email (u'martin@mangari.org')]
    >>> sorted (ps.emails, key = PAP.Email.sorted_by)
    [GTW.OMP.PAP.Email (u'ralf@runtux.com')]
    >>> sorted (pt.emails, key = PAP.Email.sorted_by)
    [GTW.OMP.PAP.Email (u'tanzer@gg32.com'), GTW.OMP.PAP.Email (u'tanzer@swing.co.at')]

    >>> _ = PAP.Company_has_Email (co, "ralf@runtux.com")

    >>> sorted (cl.emails, key = PAP.Email.sorted_by)
    [GTW.OMP.PAP.Email (u'lucky@mangari.org')]
    >>> sorted (co.emails, key = PAP.Email.sorted_by)
    [GTW.OMP.PAP.Email (u'office@runtux.com'), GTW.OMP.PAP.Email (u'ralf@runtux.com')]

    >>> rr = PAP.Email.instance ("ralf@runtux.com")
    >>> sorted (rr.persons, key = PAP.Person.sorted_by)
    [GTW.OMP.PAP.Person (u'schlatterbeck', u'ralf', u'', u'')]
    >>> sorted (rr.companies, key = PAP.Company.sorted_by)
    [GTW.OMP.PAP.Company (u'open source consulting')]

    >>> PAP.Subject_has_Email.acr_map.get ("left", False)
    False
    >>> PAP.Company_has_Email.acr_map.get ("left", False)
    <Role_Cacher_n (GTW.OMP.PAP.Company_has_Email) company --> companies [GTW.OMP.PAP.Email]>
    >>> PAP.Person_has_Email.acr_map.get ("left", False)
    <Role_Cacher_n (GTW.OMP.PAP.Person_has_Email) person --> persons [GTW.OMP.PAP.Email]>

    >>> PAP.Subject_has_Email.acr_map.get ("right", False)
    <Role_Cacher_n (GTW.OMP.PAP.Subject_has_Email) email --> emails [GTW.OMP.PAP.Subject]>
    >>> PAP.Company_has_Email.acr_map.get ("right", False)
    <Role_Cacher_n (GTW.OMP.PAP.Company_has_Email) email --> emails [GTW.OMP.PAP.Company]>
    >>> PAP.Person_has_Email.acr_map.get ("right", False)
    <Role_Cacher_n (GTW.OMP.PAP.Person_has_Email) email --> emails [GTW.OMP.PAP.Person]>

    >>> sorted (PAP.Subject_has_Email.acr_map.values ())
    [<Role_Cacher_n (GTW.OMP.PAP.Subject_has_Email) email --> emails [GTW.OMP.PAP.Subject]>]
    >>> sorted (PAP.Company_has_Email.acr_map.values ())
    [<Role_Cacher_n (GTW.OMP.PAP.Company_has_Email) email --> emails [GTW.OMP.PAP.Company]>, <Role_Cacher_n (GTW.OMP.PAP.Company_has_Email) company --> companies [GTW.OMP.PAP.Email]>]
    >>> sorted (PAP.Person_has_Email.acr_map.values ())
    [<Role_Cacher_n (GTW.OMP.PAP.Person_has_Email) email --> emails [GTW.OMP.PAP.Person]>, <Role_Cacher_n (GTW.OMP.PAP.Person_has_Email) person --> persons [GTW.OMP.PAP.Email]>]

    >>> def show_emails (ET) :
    ...     attr = ET._Attributes._own_names.get ("emails")
    ...     print (attr, attr and attr.assoc, ":", attr and attr.description)
    >>> show_emails (PAP.Subject)
    <class '_GTW._OMP._PAP.Subject.emails'> GTW.OMP.PAP.Subject_has_Email : `Email` linked to `subject`

    >>> show_emails (PAP.Company)
    <class '_GTW._OMP._PAP.Company.emails'> GTW.OMP.PAP.Company_has_Email : `Email` linked to `company`

    >>> show_emails (PAP.Person)
    <class '_GTW._OMP._PAP.Person.emails'> GTW.OMP.PAP.Person_has_Email : `Email` linked to `person`


"""

from   _GTW.__test__.model      import *
from   _MOM.import_MOM          import Q

from   itertools                import chain as ichain

__test__ = Scaffold.create_test_dict (_test_code)

### __END__ GTW.__test__.Subjects
