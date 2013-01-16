# -*- coding: iso-8859-15 -*-
# Copyright (C) 2013 Mag. Christian Tanzer All rights reserved
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
#    GTW.__test__.Certificate
#
# Purpose
#    Test GTW.OMP.Auth.Certificate
#
# Revision Dates
#    16-Jan-2013 (CT) Creation
#    ««revision-date»»···
#--

from   __future__ import absolute_import, division, print_function, unicode_literals

from   _GTW.__test__.model      import *

import datetime

_test_create = """
    >>> scope = Scaffold.scope (%(p1)s, %(n1)s) # doctest:+ELLIPSIS
    Creating new scope ...
    >>> Auth  = scope.Auth

    >>> Auth.Account.E_Type.primary_ais
    >>> Auth.Certificate.E_Type.primary_ais
    AIS `cert_id`

    >>> Auth.Certificate.query_s ().all ()
    []

    >>> c1 = Auth.Certificate (email = "foo@bar", validity = ("20130116", ))
    >>> c2 = Auth.Certificate (email = "foo@baz", validity = ("20130131", ))

    >>> cx = Auth.Certificate (42, email = "foo@qux", validity = ("20130301", ))
    Traceback (most recent call last):
    ...
    TypeError: Cannot pass value for attribute `cert_id` of Auth.Certificate, got `42`

    >>> scope.commit ()

    >>> all_cs = Auth.Certificate.query_s ().all ()
    >>> all_cs
    [Auth.Certificate (1), Auth.Certificate (2)]
    >>> for c in all_cs :
    ...     print (c.as_code (), c.validity.start)
    Auth.Certificate (1, email = u'foo@bar', validity = ('2013/01/16', )) 2013-01-16 00:00:00
    Auth.Certificate (2, email = u'foo@baz', validity = ('2013/01/31', )) 2013-01-31 00:00:00

    >>> c1.cert_id = 42
    Traceback (most recent call last):
    ...
    AttributeError: Init-only attribute `Certificate.cert_id` cannot be changed from `1` to `42` after object creation
    >>> print (c1.as_code ())
    Auth.Certificate (1, email = u'foo@bar', validity = ('2013/01/16', ))

    >>> c3 = Auth.Certificate (email = "foo@baz", validity = ("20150131", ))

    >>> scope.commit ()

    >>> all_cs = Auth.Certificate.query_s ().all ()
    >>> all_cs
    [Auth.Certificate (1), Auth.Certificate (2), Auth.Certificate (3)]

    >>> c1.pem = "fake value to fool `alive`"
    >>> (c1, c1.alive)
    (Auth.Certificate (1), True)
    >>> rdf = MOM.Attr.A_Date_Time.now () + datetime.timedelta (days = +1)
    >>> rdp = MOM.Attr.A_Date_Time.now () + datetime.timedelta (days = -1)
    >>> _ = c1.set (revocation_date = rdf) # doctest:+ELLIPSIS
    Traceback (most recent call last):
    ...
    Invariants: Condition `valid_revocation_date` : The revocation date cannot be in the future. (revocation_date <= today)
        revocation_date = ...
        today = ...
    >>> _ = c1.set (revocation_date = rdp) # doctest:+ELLIPSIS
    >>> (c1, c1.alive)
    (Auth.Certificate (1), False)

    >>> scope.destroy ()
"""

__test__ = Scaffold.create_test_dict \
    ( dict
        ( create = _test_create
        )
    , ignore = ("MYS", "SQL") ### XXX those backends should be fixed
    )

### __END__ GTW.__test__.Certificate
