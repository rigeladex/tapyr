# -*- coding: iso-8859-15 -*-
# Copyright (C) 2013 Martin Glueck All rights reserved
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
#    GTW.__test__.Query_Attribute
#
# Purpose
#    Test for query attributes
#
# Revision Dates
#    23-Jan-2013 (MG) Creation
#    26-Jan-2013 (CT) Add test for query attribute referring to cached role
#    ««revision-date»»···
#--

from   __future__ import absolute_import, division, print_function, unicode_literals

_query_test = """
    >>> scope = Scaffold.scope (%(p1)s, %(n1)s) # doctest:+ELLIPSIS
    Creating new scope MOMT__...
    >>> Auth  = scope.Auth
    >>> PAP   = scope.PAP
    >>> p     = PAP.Person ("ln", "fn", lifetime = ("20130101", ), raw = True)
    >>> a     = Auth.Account_T ("test")
    >>> pha   = PAP.Person_has_Account_Test (p, a)
    >>> scope.commit ()

    >>> a.person
    PAP.Person (u'ln', u'fn', u'', u'')

    >>> a.qt
    PAP.Person (u'ln', u'fn', u'', u'')

    >>> p.accounts
    set([Auth.Account_T (u'test')])

    >>> pha.owner
    PAP.Person (u'ln', u'fn', u'', u'')

    >>> PAP.Person_has_Account_Test.query (Q.owner.last_name == "ln").all ()
    [PAP.Person_has_Account_Test ((u'ln', u'fn', u'', u''), (u'test', ))]

"""

from   _GTW.__test__.model import *

_Ancestor_Essence = GTW.OMP.Auth.Account

class Account_T (_Ancestor_Essence) :
    """Test of query attributes"""

    class _Attributes (_Ancestor_Essence._Attributes) :

        _Ancestor = _Ancestor_Essence._Attributes

        class qt (A_Id_Entity) :
            """Test of access to cached role attribute"""

            kind               = Attr.Query
            auto_up_depends    = ("person",)
            P_Type             = GTW.OMP.PAP.Person
            query              = Q.person

        # end class qt

    # end class _Attributes

# end class Account_T

_Ancestor_Essence = GTW.OMP.PAP.Person_has_Account

class Person_has_Account_Test (_Ancestor_Essence) :
    """Test of query attribute"""

    class _Attributes (_Ancestor_Essence._Attributes) :

        _Ancestor = _Ancestor_Essence._Attributes

        ### Primary attributes

        ### Non-primary attributes

        class owner (A_Id_Entity) :
            """Alias for the person"""

            kind               = Attr.Query
            query              = Q.left
            auto_up_depends    = ("left", )
        # end class owner

    # end class _Attributes

# end class Person_has_Account_Test

__test__ = Scaffold.create_test_dict \
    ( _query_test
    )

### __END__ GTW.__test__.Query_Attribute
