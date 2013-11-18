# -*- coding: utf-8 -*-
# Copyright (C) 2010-2012 Martin Glueck All rights reserved
# Langstrasse 4, A--2244 Spannberg. martin@mangari.org
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
#    GTW.__test__.Missing_Primary_Key
#
# Purpose
#    Test what happens if one tries to create an object where a primary key
#    is correctly specified during object creation
#
# Revision Dates
#    22-Jun-2010 (MG) Creation
#    22-Jun-2010 (CT) Creation continued
#    12-Apr-2012 (CT) Extend tests for `on_error`
#    15-Apr-2012 (CT) Adapt to changes of `MOM.Error`
#    16-Apr-2012 (CT) Adapt to more changes of `MOM.Error`
#    17-Apr-2012 (CT) Add test for `as_json_cargo (* errors)`
#    ««revision-date»»···
#--

_test_code = r"""
    >>> scope = Scaffold.scope (%(p1)s, %(n1)s) # doctest:+ELLIPSIS
    Creating new scope MOMT__...
    >>> PAP = scope.PAP
    >>> errors = []
    >>> print PAP.Person.count
    0
    >>> PAP.Person (last_name = u"", first_name = u"", raw = True)
    Traceback (most recent call last):
      ...
    Invariants: Condition `first_name_not_empty` : first_name is not None and first_name != ''
        first_name = ''
      Condition `last_name_not_empty` : last_name is not None and last_name != ''
        last_name = ''
    >>> errors
    []
    >>> print PAP.Person.count
    0

    >>> PAP.Person \
    ...     ( last_name  = u"last_name"
    ...     , first_name = u""
    ...     , raw        = True
    ...     , on_error   = errors.append
    ...     )
    ...
    Traceback (most recent call last):
      ...
    Invariants: Condition `first_name_not_empty` : first_name is not None and first_name != ''
        first_name = ''
    >>> errors
    [Invariants(Required_Empty(u'Person', Condition `first_name_not_empty` : first_name is not None and first_name != ''
        first_name = ''),)]
    >>> for e in errors :
    ...     print e
    Condition `first_name_not_empty` : first_name is not None and first_name != ''
        first_name = ''

    >>> print formatted (MOM.Error.as_json_cargo (* errors))
    [ { 'attributes' :
    [ 'first_name' ]
      , 'bindings' :
          [
            ( 'first_name'
            , "''"
            )
          ]
      , 'head' : "first_name is not None and first_name != ''"
      , 'is_required' : True
      }
    ]

    >>> errors = []
    >>> PAP.Person (last_name = u"", first_name = u"", raw = True, on_error = errors.append)
    Traceback (most recent call last):
      ...
    Invariants: Condition `first_name_not_empty` : first_name is not None and first_name != ''
        first_name = ''
      Condition `last_name_not_empty` : last_name is not None and last_name != ''
        last_name = ''
    >>> print formatted (MOM.Error.as_json_cargo (* errors))
    [ { 'attributes' :
    [ 'first_name' ]
      , 'bindings' :
          [
            ( 'first_name'
            , "''"
            )
          ]
      , 'head' : "first_name is not None and first_name != ''"
      , 'is_required' : True
      }
    , { 'attributes' :
    [ 'last_name' ]
      , 'bindings' :
          [
            ( 'last_name'
            , "''"
            )
          ]
      , 'head' : "last_name is not None and last_name != ''"
      , 'is_required' : True
      }
    ]

    >>> print PAP.Person.count
    0

    >>> PAP.Person.epkified_ckd.args
    u"last_name, first_name, middle_name = u'', title = u''"
    >>> PAP.Person.epk_sig
    ('last_name', 'first_name', 'middle_name', 'title')
    >>> PAP.Person.primary_required
    [String `last_name`, String `first_name`]

"""

from _GTW.__test__.model import *

__test__ = Scaffold.create_test_dict (_test_code)

### __END__ GTW.__test__.Missing_Primary_Key
