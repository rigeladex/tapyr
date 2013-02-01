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
#    27-Jan-2013 (CT) Add another test for `.qt.last_name`
#    31-Jan-2013 (CT) Add tests for `Q.person` passed to `Account.query`
#     1-Feb-2013 (RS) Tests for query attribute via auto_cache attribute
#    ««revision-date»»···
#--

from   __future__ import absolute_import, division, print_function, unicode_literals

_query_test = """
    >>> scope = Scaffold.scope (%(p1)s, %(n1)s) # doctest:+ELLIPSIS
    Creating new scope MOMT__...
    >>> Auth  = scope.Auth
    >>> PAP   = scope.PAP
    >>> p1    = PAP.Person ("ln", "fn", lifetime = ("20130101", ), raw = True)
    >>> p2    = PAP.Person ("ln", "nf", lifetime = ("20130101", ), raw = True)
    >>> p3    = PAP.Person ("nl", "fn", lifetime = ("20130101", ), raw = True)
    >>> a1    = Auth.Account_T ("test ln fn")
    >>> a2    = Auth.Account_T ("test ln nf")
    >>> a3    = Auth.Account_T ("test nl fn")
    >>> pha1  = PAP.Person_has_Account_Test (p1, a1)
    >>> pha2  = PAP.Person_has_Account_Test (p2, a2)
    >>> pha3  = PAP.Person_has_Account_Test (p3, a3)
    >>> scope.commit ()

    >>> a1.person
    PAP.Person (u'ln', u'fn', u'', u'')

    >>> a1.qt
    PAP.Person (u'ln', u'fn', u'', u'')

    >>> p1.accounts
    set([Auth.Account_T (u'test ln fn')])

    >>> pha1.owner
    PAP.Person (u'ln', u'fn', u'', u'')

    >>> PAP.Person_has_Account_Test.query (Q.owner.last_name == "nl").all ()
    [PAP.Person_has_Account_Test ((u'nl', u'fn', u'', u''), (u'test nl fn', ))]

    >>> Auth.Account_T.query (Q.qt.last_name == "ln").count ()
    2

    >>> Auth.Account_T.query_s (Q.qt.last_name == "ln").all ()
    [Auth.Account_T (u'test ln fn'), Auth.Account_T (u'test ln nf')]

    >>> Auth.Account.query_s (Q.person == p1).all ()
    [Auth.Account_T (u'test ln fn')]

    >>> Auth.Account.query_s (Q.person.first_name == "nf").all ()
    [Auth.Account_T (u'test ln nf')]

    >>> nicky = PAP.Person_Nickname_Test (p1, 'nicky', raw = True)
    >>> nicky
    PAP.Person_Nickname_Test ((u'ln', u'fn', u'', u''), u'nicky')

    >>> wolp = PAP.Wolperdinger ("Wolp", raw = True)
    >>> wolp
    PAP.Wolperdinger (u'Wolp')
    >>> w = PAP.Wrzlbrmft ('WRZL', wolp, raw = True)
    >>> w
    PAP.Wrzlbrmft (u'WRZL', (u'Wolp', ))
    >>> phw = PAP.Person_has_Wrzlbrmft (p1, w)
    >>> phw
    PAP.Person_has_Wrzlbrmft ((u'ln', u'fn', u'', u''), (u'WRZL', (u'Wolp', )))
    >>> PAP.Person_has_Account_Test.query (Q.wrzlbrmft.wolp == wolp).all ()
    []
    >>> PAP.Person_has_Account_Test.query (Q.wrzlbrmft.my_wolp == wolp).all ()
    []

"""

from   _GTW.__test__.Test_Command import *
import _GTW._OMP._Auth.import_Auth
import _GTW._OMP._PAP .import_PAP

_Ancestor_Essence = GTW.OMP.PAP.Link1

class Person_Nickname_Test (_Ancestor_Essence) :
    """ A nickname with `max_links = 1` for testing """

    class _Attributes (_Ancestor_Essence._Attributes) :

        _Ancestor = _Ancestor_Essence._Attributes

        class left (_Ancestor.left) :

            role_type       = GTW.OMP.PAP.Person
            max_links       = 1
            auto_cache      = 'nick'

        # end class left

        class name (A_String) :

            kind            = Attr.Primary
            max_length      = 32

        # end class name

    # end class _Attributes

# end class Person_Nickname_Test

_Ancestor_Essence = GTW.OMP.PAP.Object

class Wolperdinger (_Ancestor_Essence) :
    """A class for testing an ID entitiy attribute"""

    class _Attributes (_Ancestor_Essence._Attributes) :

        _Ancestor = _Ancestor_Essence._Attributes

        class name (A_String) :

            kind               = Attr.Primary
            max_length         = 32

        # end class name

    # end class _Attributes
    
# end class Wolperdinger

_Ancestor_Essence = GTW.OMP.PAP.Object

class Wrzlbrmft (_Ancestor_Essence) :
    """ Wrzlbrmft: A special Person property for testing """

    class _Attributes (_Ancestor_Essence._Attributes) :

        _Ancestor = _Ancestor_Essence._Attributes

        class name (A_String) :

            kind               = Attr.Primary
            max_length         = 32

        # end class name

        class wolp (A_Id_Entity) :

            kind               = Attr.Primary
            P_Type             = Wolperdinger

        # end class wolp

        class my_wolp (A_Id_Entity) :
            """ model my own attribute as query """

            kind               = Attr.Query
            P_Type             = Wolperdinger
            auto_up_depends    = ("wolp", )
            hidden             = True
            query              = Q.wolp

        # end class my_wolp

    # end class _Attributes

# end class Wrzlbrmft

_Ancestor_Essence = GTW.OMP.PAP.Link2

class Person_has_Wrzlbrmft (_Ancestor_Essence) :
    """ A Person property for testing """

    class _Attributes (_Ancestor_Essence._Attributes) :

        _Ancestor = _Ancestor_Essence._Attributes

        class left (_Ancestor.left) :

            role_type          = GTW.OMP.PAP.Person

        # end class left

        class right (_Ancestor.right) :

            role_type          = Wrzlbrmft
            max_links          = 1
            auto_cache         = 'wrzlbrmft'

        # end class right

    # end class _Attributes

# end class Person_has_Wrzlbrmft

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

#        class account_nick (A_Id_Entity) :
#            """Test of access to query attributes via cached role"""
#
#            kind               = Attr.Query
#            auto_up_depends    = ("person.nick",)
#            P_Type             = Person_Nickname_Test
#            query              = Q.person.nick
#
#        # end class account_nick

#        class account_wrzl (A_Id_Entity) :
#            """ Test of access to query attribute via cached role """
#
#            kind               = Attr.Query
#            auto_up_depends    = ("person.wrzlbrmft",)
#            P_Type             = Wrzlbrmft
#            query              = Q.person.wrzlbrmft
#
#        # end class account_wrzl

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

GTW_Test_Command.PNS_Aliases           = dict \
    ( Auth            = GTW.OMP.Auth
    , PAP             = GTW.OMP.PAP
    )

Scaffold = GTW_Test_Command ()
__test__ = Scaffold.create_test_dict \
    ( _query_test
    )

### __END__ GTW.__test__.Query_Attribute
