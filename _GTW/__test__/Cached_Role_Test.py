# -*- coding: iso-8859-15 -*-
# Copyright (C) 2010-2012 Martin Glueck All rights reserved
# Langstrasse 4, A--2244 Spannberg, Austria. martin@mangari.org
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
#    GTW.__test__.Cached_Role_Test
#
# Purpose
#    Test cases for cached role behavior.
#
# Revision Dates
#    21-Apr-2010 (MG) Creation
#    20-Jul-2012 (RS) Add several left-sides (more than one `PAP.Person`)
#    13-Sep-2012 (CT) Add test for `auto_cache_roles`
#    ««revision-date»»···
#--

_test_code = """
    >>> scope = Scaffold.scope (%(p1)s, %(n1)s) # doctest:+ELLIPSIS
    Creating new scope MOMT__...
    >>> PAP      = scope.PAP
    >>> person   = PAP.Person  (u"Test", u"Person")
    >>> person2  = PAP.Person  (u"Another", u"Person")
    >>> address1 = PAP.Address (u"Street 1", u"Zip", u"City", u"Country")
    >>> address2 = PAP.Address (u"Street 2", u"Zip", u"City", u"Country")
    >>> email1   = PAP.Email   (u"person@example.com")
    >>> email2   = PAP.Email   (u"person2@example.com")
    >>> elink1   = PAP.Person_has_Email (person, email1)
    >>> elink2   = PAP.Person_has_Email (person2, email2)

    >>> PAP.Person.addresses
    Cached_Role_Set `addresses`

    >>> sorted (person.addresses) #1
    []
    >>> link = PAP.Person_has_Address (person, address1)
    >>> sorted (person.addresses) #2
    [PAP.Address (u'street 1', u'zip', u'city', u'country')]
    >>> sorted (PAP.Person_has_Address.query ().all ())
    [PAP.Person_has_Address ((u'test', u'person', u'', u''), (u'street 1', u'zip', u'city', u'country'))]
    >>> link.set (address = address2)
    1
    >>> sorted (person.addresses) #3
    [PAP.Address (u'street 2', u'zip', u'city', u'country')]
    >>> link
    PAP.Person_has_Address ((u'test', u'person', u'', u''), (u'street 2', u'zip', u'city', u'country'))
    >>> sorted (PAP.Person_has_Address.query ().all ())
    [PAP.Person_has_Address ((u'test', u'person', u'', u''), (u'street 2', u'zip', u'city', u'country'))]
    >>> link.set_raw (right = address1.epk_raw)
    1
    >>> [e.address for e in person.emails]
    [u'person@example.com']
    >>> [e.address for e in person2.emails]
    [u'person2@example.com']

    >>> scope.destroy ()

"""

_test_acr = """
    >>> scope = Scaffold.scope (%(p1)s, %(n1)s) # doctest:+ELLIPSIS
    Creating new scope MOMT__...
    >>> PAP      = scope.PAP

    >>> for T in scope.T_Extension [2:] :
    ...     if getattr (T, "Roles", None) and T.auto_cache_roles :
    ...         print T.auto_cache_roles
    (<Role_Cacher_n (GTW.OMP.Auth.Account_in_Group) account --> accounts [GTW.OMP.Auth.Group]>, <Role_Cacher_n (GTW.OMP.Auth.Account_in_Group) group --> groups [GTW.OMP.Auth.Account]>)
    (<Link_Cacher_1 (GTW.OMP.Auth.Account_Activation) account --> activation>,)
    (<Link_Cacher_1 (GTW.OMP.Auth.Account_Password_Change_Required) account --> password_change_required>,)
    (<Link_Cacher_n (GTW.OMP.EVT.Event) object --> events>,)
    (<Link_Cacher_n (GTW.OMP.EVT.Event_occurs) event --> occurs>,)
    (<Link_Cacher_1 (GTW.OMP.EVT.Recurrence_Spec) event --> recurrence>,)
    (<Link_Cacher_n (GTW.OMP.EVT.Recurrence_Rule) recurrence_spec --> rules>,)
    (<Role_Cacher_1 (GTW.OMP.PAP.Entity_created_by_Person) creator --> creator [MOM.Id_Entity]>,)
    (<Role_Cacher_n (GTW.OMP.PAP.Subject_has_Phone) phone --> phones [GTW.OMP.PAP.Subject]>,)
    (<Role_Cacher_n (GTW.OMP.PAP.Subject_has_Address) address --> addresses [GTW.OMP.PAP.Subject]>,)
    (<Role_Cacher_n (GTW.OMP.PAP.Subject_has_Email) email --> emails [GTW.OMP.PAP.Subject]>,)
    (<Link_Cacher_n (GTW.OMP.SWP.Clip_O) object --> clips>,)
    (<Link_Cacher_n (GTW.OMP.SWP.Picture) gallery --> pictures>,)
    (<Link_Cacher_n (GTW.OMP.SRM.Regatta) event --> regattas>,)
    (<Link_Cacher_n (GTW.OMP.SRM.Regatta_C) event --> regattas>,)
    (<Link_Cacher_n (GTW.OMP.SRM.Regatta_H) event --> regattas>,)
    (<Link_Cacher_n (GTW.OMP.SRM.Boat_in_Regatta) regatta --> boats>,)
    (<Link_Cacher_n (GTW.OMP.SRM.Race_Result) boat_in_regatta --> race_results>,)
    (<Link_Cacher_n (GTW.OMP.SRM.Team) regatta --> teams>,)
    (<Role_Cacher_n (GTW.OMP.SRM.Crew_Member) sailor --> _crew [GTW.OMP.SRM.Boat_in_Regatta]>,)
    (<Role_Cacher_n (GTW.OMP.SRM.Team_has_Boat_in_Regatta) team --> teams [GTW.OMP.SRM.Boat_in_Regatta]>, <Role_Cacher_n (GTW.OMP.SRM.Team_has_Boat_in_Regatta) boat --> boats [GTW.OMP.SRM.Team]>)
    (<Role_Cacher_n (GTW.OMP.PAP.Person_has_Email) person --> persons [GTW.OMP.PAP.Email]>, <Role_Cacher_n (GTW.OMP.PAP.Person_has_Email) email --> emails [GTW.OMP.PAP.Person]>)
    (<Role_Cacher_n (GTW.OMP.PAP.Company_has_Email) company --> companies [GTW.OMP.PAP.Email]>, <Role_Cacher_n (GTW.OMP.PAP.Company_has_Email) email --> emails [GTW.OMP.PAP.Company]>)
    (<Role_Cacher_n (GTW.OMP.PAP.Person_has_Address) person --> persons [GTW.OMP.PAP.Address]>, <Role_Cacher_n (GTW.OMP.PAP.Person_has_Address) address --> addresses [GTW.OMP.PAP.Person]>)
    (<Role_Cacher_n (GTW.OMP.PAP.Company_has_Address) company --> companies [GTW.OMP.PAP.Address]>, <Role_Cacher_n (GTW.OMP.PAP.Company_has_Address) address --> addresses [GTW.OMP.PAP.Company]>)
    (<Role_Cacher_n (GTW.OMP.PAP.Person_has_Phone) person --> persons [GTW.OMP.PAP.Phone]>, <Role_Cacher_n (GTW.OMP.PAP.Person_has_Phone) phone --> phones [GTW.OMP.PAP.Person]>)
    (<Role_Cacher_n (GTW.OMP.PAP.Company_has_Phone) company --> companies [GTW.OMP.PAP.Phone]>, <Role_Cacher_n (GTW.OMP.PAP.Company_has_Phone) phone --> phones [GTW.OMP.PAP.Company]>)

    >>> scope.destroy ()

"""

from _GTW.__test__.model import *

__test__ = dict \
    ( Scaffold.create_test_dict
        ( dict (acr = _test_acr)
        , ignore = ("SQL", "MYS", "POS")
        )
    , ** Scaffold.create_test_dict (dict (cache = _test_code))
    )

### __END__ GTW.__test__.Cached_Role_Test
