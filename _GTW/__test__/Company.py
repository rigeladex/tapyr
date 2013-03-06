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
#    GTW.__test__.Company
#
# Purpose
#    Test PAP.Company and descendents
#
# Revision Dates
#    26-Feb-2013 (CT) Creation
#     4-Mar-2013 (CT) Add tests for `PAP.Association`
#     6-Mar-2013 (CT) Adapt to new attribute `Company.registered_in`
#     6-Mar-2013 (CT) Add test for `polymorphic_epk` using `children_trans_iter`
#    ««revision-date»»···
#--

from   __future__ import absolute_import, division, print_function, unicode_literals

_test_code = """
    >>> scope = Scaffold.scope (%(p1)s, %(n1)s) # doctest:+ELLIPSIS
    Creating new scope MOMT__...
    >>> PAP = scope.PAP

    >>> p1 = PAP.Person ("Doe", "Jane", lifetime = ("20010101", ), raw = True)
    >>> bm = PAP.Biz_Man (p1)
    >>> cp = PAP.Company_P ("Doe, Inc.", bm, raw = True)
    >>> ta = PAP.Association ("Towel Carriers Association", short_name = "TCA", raw = True)

    >>> print (p1.ui_repr)
    PAP.Person (u'Doe', u'Jane', u'', u'')

    >>> print (bm.ui_repr)
    PAP.Biz_Man ((u'Doe', u'Jane', u'', u'', 'PAP.Person'),)

    >>> print (cp.ui_repr)
    PAP.Company_P (u'Doe, Inc.', ((u'Doe', u'Jane', u'', u'', 'PAP.Person'), 'PAP.Biz_Man'), u'')

    >>> print (ta.ui_repr)
    PAP.Association (u'Towel Carriers Association',)

    >>> scope.commit ()

    >>> PAP.Person.sorted_by_epk
    <Sorted_By: Getter function for `.last_name`, Getter function for `.first_name`, Getter function for `.middle_name`, Getter function for `.title`>

    >>> PAP.Biz_Man.sorted_by_epk
    <Sorted_By: Getter function for `.left.last_name`, Getter function for `.left.first_name`, Getter function for `.left.middle_name`, Getter function for `.left.title`>

    >>> PAP.Company_P.sorted_by_epk
    <Sorted_By: Getter function for `.name`, Getter function for `.owner.left.last_name`, Getter function for `.owner.left.first_name`, Getter function for `.owner.left.middle_name`, Getter function for `.owner.left.title`, Getter function for `.registered_in`>

    >>> PAP.Person.query (sort_key = TFL.Sorted_By ("pid")).count ()
    1
    >>> PAP.Biz_Man.query (sort_key = TFL.Sorted_By ("pid")).count ()
    1
    >>> PAP.Company_P.query (sort_key = TFL.Sorted_By ("pid")).count ()
    1

    >>> PAP.Person.query (sort_key = PAP.Person.sorted_by_epk).count ()
    1
    >>> PAP.Biz_Man.query (sort_key = PAP.Biz_Man.sorted_by_epk).count ()
    1
    >>> PAP.Company_P.query (sort_key = PAP.Company_P.sorted_by_epk).count ()
    1

    >>> cq = PAP.Company_P ("Jane's, Inc.", bm)

    >>> PAP.Company_P.query (sort_key = TFL.Sorted_By ("pid")).count ()
    2

    >>> PAP.Company_P.query (sort_key = PAP.Company_P.sorted_by_epk).count ()
    2

    >>> print (PAP.Association.E_Type.name.description)
    Name of association.

    >>> print (PAP.Company.E_Type.name.description)
    Name of company.

    >>> for s in PAP.Subject.query_s () :
    ...     print (s.ui_repr)
    PAP.Person (u'Doe', u'Jane', u'', u'')
    PAP.Company_P (u'Doe, Inc.', ((u'Doe', u'Jane', u'', u'', 'PAP.Person'), 'PAP.Biz_Man'), u'')
    PAP.Company_P (u"Jane's, Inc.", ((u'Doe', u'Jane', u'', u'', 'PAP.Person'), 'PAP.Biz_Man'), u'')
    PAP.Association (u'Towel Carriers Association',)

    >>> sk = lambda x : (not bool (x.children), x.i_rank)
    >>> for i, (T, l) in enumerate (children_trans_iter (PAP.Subject, sort_key = sk)) :
    ...     if not i :
    ...         print ("%%-50s %%5s %%5s %%5s" %% ("type_name", "relev", "p_epk", "p_epks"))
    ...         print ("=" * 70)
    ...     et = T.E_Type
    ...     fs = (et.is_relevant, et.polymorphic_epk, et.polymorphic_epks)
    ...     if any (fs) :
    ...         hd  = "%%s%%s" %% ("  " * l, et.type_name)
    ...         hdl = len (hd)
    ...         sep = (" " if hdl %% 2 else "") + ". " * ((50 - hdl) // 2)
    ...         r, p, s = ((x or "") for x in fs)
    ...         print ("%%s %%s %%5s %%5s %%5s" %% (hd, sep, r, p, s))
    type_name                                          relev p_epk p_epks
    ======================================================================
    PAP.Subject  . . . . . . . . . . . . . . . . . . .         True  True
      PAP.Legal_Entity . . . . . . . . . . . . . . . .         True  True
        PAP.Company  . . . . . . . . . . . . . . . . .   True  True  True
          PAP.Company_P  . . . . . . . . . . . . . . .   True
        PAP.Association  . . . . . . . . . . . . . . .   True
      PAP.Person . . . . . . . . . . . . . . . . . . .   True

"""

from   _GTW.__test__.model      import *
from   _MOM.import_MOM          import Q
from   _MOM.inspect             import children_trans_iter

import _GTW._OMP._PAP.Association

_Ancestor_Essence = GTW.OMP.PAP.Link1

class Biz_Man (_Ancestor_Essence) :
    """Russian in business"""

    class _Attributes (_Ancestor_Essence._Attributes) :

        _Ancestor = _Ancestor_Essence._Attributes

        class left (_Ancestor.left) :
            """Network device the interface is connected to."""

            role_type          = GTW.OMP.PAP.Person
            role_name          = "man"

        # end class left

    # end class _Attributes

# end class Biz_Man

_Ancestor_Essence = GTW.OMP.PAP.Company

class Company_P (_Ancestor_Essence) :
    """Company owned and operated by a single person"""

    class _Attributes (_Ancestor_Essence._Attributes) :

        _Ancestor = _Ancestor_Essence._Attributes

        class owner (A_Id_Entity) :
            """Owner of the company"""

            kind               = Attr.Primary
            P_Type             = Biz_Man

        # end class owner

    # end class _Attributes

# end class Company_P

__test__ = Scaffold.create_test_dict \
    ( dict
        ( main          = _test_code
        )
    )

### __END__ GTW.__test__.Company
