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
#    GTW.__test__.Attr_surrogate
#
# Purpose
#    Test surrogate attributes
#
# Revision Dates
#     5-Jun-2013 (CT) Creation
#    ««revision-date»»···
#--

from   __future__ import division, print_function
from   __future__ import absolute_import, unicode_literals

from   _GTW.__test__.model import *
from   _MOM.inspect        import children_trans_iter

import _GTW._OMP._Auth.import_Auth

_test_map = """
    >>> scope = Scaffold.scope (%(p1)s, %(n1)s) # doctest:+ELLIPSIS
    Creating new scope MOMT__...

    >>> ET_Cert = scope.Auth.Certificate.E_Type
    >>> for a in ET_Cert.q_able :
    ...     print (repr (a))
    Email `email`
    Date_Time_Interval `validity`
    String `desc`
    Date-Time `revocation_date`
    Boolean `electric`
    Int `last_cid`
    Surrogate `pid`
    String `type_name`
    Surrogate `cert_id`
    None `pem`
    Boolean `alive`

    >>> sorted ((k, t.type_name) for k, t in pyk.iteritems (scope.app_type.surrogate_t_map))
    [(1, 'MOM.Id_Entity'), (2, 'Auth.Certificate')]

    >>> sorted ((str (k), a) for k, a in pyk.iteritems (scope.app_type.surrogate_map))
    [('Auth.Certificate.cert_id', Surrogate `cert_id`), ('MOM.Id_Entity.pid', Surrogate `pid`)]

"""

__test__ = Scaffold.create_test_dict \
    ( dict
        ( test_map = _test_map
        )
    )

### __END__ GTW.__test__.Attr_surrogate
