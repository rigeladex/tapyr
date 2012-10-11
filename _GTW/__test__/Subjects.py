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
#    Test PAP.Subject subclasses and links
#
# Revision Dates
#    24-Mar-2012 (CT) Creation
#    14-Sep-2012 (CT) Add test for role attributes of `Person_has_Address`
#    20-Sep-2012 (CT) Add tests for `Person_has_Phone`, `Subject_has_Property`
#    21-Sep-2012 (CT) Add test for polymorphic link creation
#    ««revision-date»»···
#--

from   __future__  import absolute_import, division, print_function, unicode_literals

_test_code = """
    >>> scope = Scaffold.scope (%(p1)s, %(n1)s) # doctest:+ELLIPSIS
    Creating new scope MOMT__...
    >>> PAP = scope.PAP

    >>> print (PAP.Subject.count, PAP.Company.count_strict, PAP.Person.count_strict)
    0 0 0

    >>> pg = PAP.Person ("Glueck", "Martin")
    >>> ps = PAP.Person ("Schlatterbeck", "Ralf")
    >>> pt = PAP.Person ("Tanzer", "Christian")
    >>> print (PAP.Subject.count, PAP.Company.count_strict, PAP.Person.count_strict)
    3 0 3

    >>> cl = PAP.Company ("Lucky Software", short_name = "LS")
    >>> co = PAP.Company ("Open Source Consulting", short_name = "OSC")
    >>> print (PAP.Subject.count, PAP.Company.count_strict, PAP.Person.count_strict)
    5 2 3

    >>> PAP.Subject.query_s ().all ()
    [PAP.Person (u'glueck', u'martin', u'', u''), PAP.Company (u'lucky software'), PAP.Company (u'open source consulting'), PAP.Person (u'schlatterbeck', u'ralf', u'', u''), PAP.Person (u'tanzer', u'christian', u'', u'')]
    >>> PAP.Company.query_s ().all ()
    [PAP.Company (u'lucky software'), PAP.Company (u'open source consulting')]
    >>> PAP.Person.query_s ().all ()
    [PAP.Person (u'glueck', u'martin', u'', u''), PAP.Person (u'schlatterbeck', u'ralf', u'', u''), PAP.Person (u'tanzer', u'christian', u'', u'')]

    >>> eg  = PAP.Email ("martin@mangari.org")
    >>> es  = PAP.Email ("ralf@runtux.com")
    >>> et1 = PAP.Email ("tanzer@swing.co.at")
    >>> et2 = PAP.Email ("tanzer@gg32.com")

    >>> _ = PAP.Subject_has_Property (pg, eg)
    >>> _ = PAP.Subject_has_Property (ps, es)
    >>> _ = PAP.Subject_has_Property (pt, et1)
    >>> _ = PAP.Subject_has_Property (pt, et2)

    >>> _ = PAP.Company_has_Email (cl, PAP.Email ("lucky@mangari.org"))
    >>> _ = PAP.Company_has_Email (co, PAP.Email ("office@runtux.com"))

    >>> _ = PAP.Person_has_Phone  (pg, PAP.Phone ("43", "1", "234567", raw = True))
    >>> _ = PAP.Person_has_Phone  (ps, PAP.Phone ("43", "1", "987654", raw = True))
    >>> _ = PAP.Person_has_Phone  (pt, PAP.Phone ("43", "1", "135790", raw = True))
    >>> _ = PAP.Company_has_Phone (co, PAP.Phone ("43", "1", "246802", raw = True), extension = "16", raw = True)

    >>> PAP.Subject_has_Email.query_s ().all ()
    [PAP.Person_has_Email ((u'glueck', u'martin', u'', u''), (u'martin@mangari.org', )), PAP.Company_has_Email ((u'lucky software', ), (u'lucky@mangari.org', )), PAP.Company_has_Email ((u'open source consulting', ), (u'office@runtux.com', )), PAP.Person_has_Email ((u'schlatterbeck', u'ralf', u'', u''), (u'ralf@runtux.com', )), PAP.Person_has_Email ((u'tanzer', u'christian', u'', u''), (u'tanzer@gg32.com', )), PAP.Person_has_Email ((u'tanzer', u'christian', u'', u''), (u'tanzer@swing.co.at', ))]
    >>> PAP.Company_has_Email.query_s ().all ()
    [PAP.Company_has_Email ((u'lucky software', ), (u'lucky@mangari.org', )), PAP.Company_has_Email ((u'open source consulting', ), (u'office@runtux.com', ))]
    >>> PAP.Person_has_Email.query_s ().all ()
    [PAP.Person_has_Email ((u'glueck', u'martin', u'', u''), (u'martin@mangari.org', )), PAP.Person_has_Email ((u'schlatterbeck', u'ralf', u'', u''), (u'ralf@runtux.com', )), PAP.Person_has_Email ((u'tanzer', u'christian', u'', u''), (u'tanzer@gg32.com', )), PAP.Person_has_Email ((u'tanzer', u'christian', u'', u''), (u'tanzer@swing.co.at', ))]

    >>> PAP.Subject_has_Email.query_s (Q.right.address.ENDSWITH ("@mangari.org")).all ()
    [PAP.Person_has_Email ((u'glueck', u'martin', u'', u''), (u'martin@mangari.org', )), PAP.Company_has_Email ((u'lucky software', ), (u'lucky@mangari.org', ))]
    >>> PAP.Subject_has_Email.query_s (Q.right.address.CONTAINS (".co")).all ()
    [PAP.Company_has_Email ((u'open source consulting', ), (u'office@runtux.com', )), PAP.Person_has_Email ((u'schlatterbeck', u'ralf', u'', u''), (u'ralf@runtux.com', )), PAP.Person_has_Email ((u'tanzer', u'christian', u'', u''), (u'tanzer@gg32.com', )), PAP.Person_has_Email ((u'tanzer', u'christian', u'', u''), (u'tanzer@swing.co.at', ))]
    >>> PAP.Person_has_Email.query_s (Q.right.address.ENDSWITH ("@mangari.org")).all ()
    [PAP.Person_has_Email ((u'glueck', u'martin', u'', u''), (u'martin@mangari.org', ))]
    >>> PAP.Person_has_Email.query_s (Q.right.address.CONTAINS (".co")).all ()
    [PAP.Person_has_Email ((u'schlatterbeck', u'ralf', u'', u''), (u'ralf@runtux.com', )), PAP.Person_has_Email ((u'tanzer', u'christian', u'', u''), (u'tanzer@gg32.com', )), PAP.Person_has_Email ((u'tanzer', u'christian', u'', u''), (u'tanzer@swing.co.at', ))]

    >>> sorted (pg.emails, key = PAP.Email.sorted_by)
    [PAP.Email (u'martin@mangari.org')]
    >>> sorted (ps.emails, key = PAP.Email.sorted_by)
    [PAP.Email (u'ralf@runtux.com')]
    >>> sorted (pt.emails, key = PAP.Email.sorted_by)
    [PAP.Email (u'tanzer@gg32.com'), PAP.Email (u'tanzer@swing.co.at')]

    >>> _ = PAP.Company_has_Email (co, "ralf@runtux.com")

    >>> sorted (cl.emails, key = PAP.Email.sorted_by)
    [PAP.Email (u'lucky@mangari.org')]
    >>> sorted (co.emails, key = PAP.Email.sorted_by)
    [PAP.Email (u'office@runtux.com'), PAP.Email (u'ralf@runtux.com')]

    >>> rr = PAP.Email.instance ("ralf@runtux.com")
    >>> sorted (rr.persons, key = PAP.Person.sorted_by)
    [PAP.Person (u'schlatterbeck', u'ralf', u'', u'')]
    >>> sorted (rr.companies, key = PAP.Company.sorted_by)
    [PAP.Company (u'open source consulting')]

    >>> PAP.Subject_has_Property.query_s ().all ()
    [PAP.Person_has_Phone ((u'glueck', u'martin', u'', u''), (u'43', u'1', u'234567'), u''), PAP.Person_has_Email ((u'glueck', u'martin', u'', u''), (u'martin@mangari.org', )), PAP.Company_has_Email ((u'lucky software', ), (u'lucky@mangari.org', )), PAP.Company_has_Phone ((u'open source consulting', ), (u'43', u'1', u'246802'), u'16'), PAP.Company_has_Email ((u'open source consulting', ), (u'office@runtux.com', )), PAP.Company_has_Email ((u'open source consulting', ), (u'ralf@runtux.com', )), PAP.Person_has_Phone ((u'schlatterbeck', u'ralf', u'', u''), (u'43', u'1', u'987654'), u''), PAP.Person_has_Email ((u'schlatterbeck', u'ralf', u'', u''), (u'ralf@runtux.com', )), PAP.Person_has_Phone ((u'tanzer', u'christian', u'', u''), (u'43', u'1', u'135790'), u''), PAP.Person_has_Email ((u'tanzer', u'christian', u'', u''), (u'tanzer@gg32.com', )), PAP.Person_has_Email ((u'tanzer', u'christian', u'', u''), (u'tanzer@swing.co.at', ))]
    >>> PAP.Subject_has_Property.query_s (left = pt).all ()
    [PAP.Person_has_Phone ((u'tanzer', u'christian', u'', u''), (u'43', u'1', u'135790'), u''), PAP.Person_has_Email ((u'tanzer', u'christian', u'', u''), (u'tanzer@gg32.com', )), PAP.Person_has_Email ((u'tanzer', u'christian', u'', u''), (u'tanzer@swing.co.at', ))]

    #>>> PAP.Subject_has_Property.query_s (subject = pt).all ()
    [PAP.Person_has_Phone ((u'tanzer', u'christian', u'', u''), (u'43', u'1', u'135790'), u''), PAP.Person_has_Email ((u'tanzer', u'christian', u'', u''), (u'tanzer@gg32.com', )), PAP.Person_has_Email ((u'tanzer', u'christian', u'', u''), (u'tanzer@swing.co.at', ))]

    >>> PAP.Subject_has_Phone.query_s (Q.right.number.CONTAINS ("2")).all ()
    [PAP.Person_has_Phone ((u'glueck', u'martin', u'', u''), (u'43', u'1', u'234567'), u''), PAP.Company_has_Phone ((u'open source consulting', ), (u'43', u'1', u'246802'), u'16')]

    >>> PAP.Subject_has_Phone.query_s (Q.extension != "").all ()
    [PAP.Company_has_Phone ((u'open source consulting', ), (u'43', u'1', u'246802'), u'16')]

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

    >>> sorted (PAP.Subject_has_Email.acr_map.values (), key = TFL.Getter.attr_name)
    [<Role_Cacher_n (GTW.OMP.PAP.Subject_has_Email) email --> emails [GTW.OMP.PAP.Subject]>]
    >>> sorted (PAP.Company_has_Email.acr_map.values (), key = TFL.Getter.attr_name)
    [<Role_Cacher_n (GTW.OMP.PAP.Company_has_Email) company --> companies [GTW.OMP.PAP.Email]>, <Role_Cacher_n (GTW.OMP.PAP.Company_has_Email) email --> emails [GTW.OMP.PAP.Company]>]
    >>> sorted (PAP.Person_has_Email.acr_map.values (), key = TFL.Getter.attr_name)
    [<Role_Cacher_n (GTW.OMP.PAP.Person_has_Email) email --> emails [GTW.OMP.PAP.Person]>, <Role_Cacher_n (GTW.OMP.PAP.Person_has_Email) person --> persons [GTW.OMP.PAP.Email]>]

    >>> def show_emails (ET) :
    ...     attr = ET.emails
    ...     print (attr.attr.__class__, ":", attr.description, "[", attr.assoc, "]")
    >>> show_emails (PAP.Subject)
    <class '_GTW._OMP._PAP.Subject.emails'> : `Emails` linked to `subject` [ GTW.OMP.PAP.Subject_has_Email ]

    >>> show_emails (PAP.Company)
    <class '_GTW._OMP._PAP.Company.emails'> : `Emails` linked to `company` [ GTW.OMP.PAP.Company_has_Email ]

    >>> show_emails (PAP.Person)
    <class '_GTW._OMP._PAP.Person.emails'> : `Emails` linked to `person` [ GTW.OMP.PAP.Person_has_Email ]

    >>> ET = PAP.Person_has_Address.E_Type
    >>> sorted (ET.role_map)
    ['Address', 'PAP.Address', 'PAP.Person', 'Person', u'address', u'left', u'person', u'right']
    >>> ET.Roles
    (Person `left`, Address `right`)
    >>> ET.edit_attr
    (Person `left`, Address `right`, String `desc`)
    >>> ET.left, ET.person
    (Person `left`, Person `left`)
    >>> ET.right, ET.address
    (Address `right`, Address `right`)

    >>> for T, l in children_trans_iter (scope.PAP.Subject_has_Property) :
    ...     rr = T.relevant_root.type_name if T.relevant_root else sorted (T.relevant_roots)
    ...     print ("%%-30s %%-5s %%s" %% ("%%s%%s" %% ("  " * l, T.type_name), T.is_partial, rr))
    PAP.Subject_has_Property       True  ['PAP.Company_has_Address', 'PAP.Company_has_Email', 'PAP.Company_has_Phone', 'PAP.Company_has_Url', 'PAP.Person_has_Address', 'PAP.Person_has_Email', 'PAP.Person_has_Phone', 'PAP.Person_has_Url']
      PAP.Subject_has_Phone        True  ['PAP.Company_has_Phone', 'PAP.Person_has_Phone']
        PAP.Person_has_Phone       False PAP.Person_has_Phone
        PAP.Company_has_Phone      False PAP.Company_has_Phone
      PAP.Subject_has_Address      True  ['PAP.Company_has_Address', 'PAP.Person_has_Address']
        PAP.Person_has_Address     False PAP.Person_has_Address
        PAP.Company_has_Address    False PAP.Company_has_Address
      PAP.Subject_has_Email        True  ['PAP.Company_has_Email', 'PAP.Person_has_Email']
        PAP.Person_has_Email       False PAP.Person_has_Email
        PAP.Company_has_Email      False PAP.Company_has_Email
      PAP.Subject_has_Url          True  ['PAP.Company_has_Url', 'PAP.Person_has_Url']
        PAP.Person_has_Url         False PAP.Person_has_Url
        PAP.Company_has_Url        False PAP.Company_has_Url

"""

from   _GTW.__test__.model      import *
from   _MOM.import_MOM          import Q
from   _MOM.inspect             import children_trans_iter

from   itertools                import chain as ichain

__test__ = Scaffold.create_test_dict (_test_code)

### __END__ GTW.__test__.Subjects
