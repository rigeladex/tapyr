# -*- coding: utf-8 -*-
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
#    25-Feb-2013 (CT) Add tests
#    26-Apr-2013 (CT) Remove `cert_id`
#    ««revision-date»»···
#--

from   __future__ import absolute_import, division, print_function, unicode_literals

from   _GTW.__test__.model      import *

import datetime

_test_create = """
    >>> scope = Scaffold.scope (%(p1)s, %(n1)s) # doctest:+ELLIPSIS
    Creating new scope ...
    >>> Auth  = scope.Auth

    >>> a1 = Auth.Account (name = "foo@bar", raw = True)
    >>> a2 = Auth.Account (name = "foo@baz", raw = True)

    >>> Auth.Certificate.query_s ().all ()
    []

    >>> c1 = Auth.Certificate (email = "foo@bar", validity = ("20130116", ), raw = True)
    >>> c2 = Auth.Certificate (email = "foo@baz", validity = ("20130131", ), raw = True)

    >>> scope.commit ()

    >>> all_cs = Auth.Certificate.query_s ().all ()
    >>> all_cs
    [Auth.Certificate (u'foo@bar', ('2013/01/16', ), u''), Auth.Certificate (u'foo@baz', ('2013/01/31', ), u'')]

    >>> for c in all_cs :
    ...     print (c.as_code (), c.validity.start)
    Auth.Certificate (u'foo@bar', ('2013/01/16', ), u'', ) 2013-01-16 00:00:00
    Auth.Certificate (u'foo@baz', ('2013/01/31', ), u'', ) 2013-01-31 00:00:00

    >>> c3 = Auth.Certificate (email = "foo@baz", validity = ("20150131", ), raw = True)

    >>> scope.commit ()

    >>> all_cs = Auth.Certificate.query_s ().all ()
    >>> all_cs
    [Auth.Certificate (u'foo@bar', ('2013/01/16', ), u''), Auth.Certificate (u'foo@baz', ('2013/01/31', ), u''), Auth.Certificate (u'foo@baz', ('2015/01/31', ), u'')]

    >>> (c1, c1.alive)
    (Auth.Certificate (u'foo@bar', ('2013/01/16', ), u''), False)

    >>> c1.pem = b"fake value to fool `alive`"

    >>> (c1, c1.alive)
    (Auth.Certificate (u'foo@bar', ('2013/01/16', ), u''), True)

    >>> rdf = MOM.Attr.A_Date_Time.now () + datetime.timedelta (days = +1)
    >>> rdp = MOM.Attr.A_Date_Time.now () + datetime.timedelta (days = -1)
    >>> _ = c1.set (revocation_date = rdf) # doctest:+ELLIPSIS
    Traceback (most recent call last):
    ...
    Invariants: Condition `valid_revocation_date` : The revocation date cannot be in the future. (revocation_date <= today)
        revocation_date = ...
        today = ...

    >>> _ = c1.set (revocation_date = rdp)
    >>> (c1, c1.alive)
    (Auth.Certificate (u'foo@bar', ('2013/01/16', ), u''), False)

    >>> scope.commit ()
    >>> (c1, c1.alive)
    (Auth.Certificate (u'foo@bar', ('2013/01/16', ), u''), False)

    >>> c4 = Auth.Certificate (email = "foo@foo", validity = (), raw = True)

    >>> (c4, c4.alive)
    (Auth.Certificate (u'foo@foo', (), u''), None)

    >>> c4.validity.start = "20130225"
    >>> (c4, c4.alive)
    (Auth.Certificate (u'foo@foo', ('2013/02/25', ), u''), False)

    >>> c4.pem = b"fake value to fool `alive`"
    >>> (c4, c4.alive)
    (Auth.Certificate (u'foo@foo', ('2013/02/25', ), u''), True)

    >>> c5 = Auth.Certificate (email = "bar@foo", validity = ("20130225", ), raw = True)

    >>> (c5, c5.alive)
    (Auth.Certificate (u'bar@foo', ('2013/02/25', ), u''), False)

    >>> for c in Auth.Certificate.query ().order_by (Q.cert_id) :
    ...     (int (c.pid), int (c.cert_id or 0) or None)
    (3, 1)
    (4, 2)
    (5, 3)
    (6, 4)
    (7, 5)

"""

class _Certificate_Scaffold_ (Scaffold.__class__) :

    Backend_Parameters    = dict \
        ( Scaffold.Backend_Parameters
        , HPS             = "'hps:///test.hps'"
        , SQL             = "'sqlite:///test.sql'"
        , sq              = "'sqlite:///test.sql'"
        )

# end class _Certificate_Scaffold_

Scaffold = _Certificate_Scaffold_ ()

__test__ = Scaffold.create_test_dict \
    ( dict
        ( test_create  = _test_create
        )
    )

### __END__ GTW.__test__.Certificate
