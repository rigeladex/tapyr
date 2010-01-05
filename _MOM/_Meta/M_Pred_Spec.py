# -*- coding: iso-8859-1 -*-
# Copyright (C) 2009 Mag. Christian Tanzer. All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# ****************************************************************************
# This module is part of the package _MOM.
#
# This module is free software; you can redistribute it and/or
# modify it under the terms of the GNU Affero General Public
# License as published by the Free Software Foundation; either
# version 3 of the License, or (at your option) any later version.
#
# This module is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public
# License along with this library. If not, see <http://www.gnu.org/licenses/>.
# ****************************************************************************
#
#++
# Name
#    MOM.Meta.M_Pred_Spec
#
# Purpose
#    Meta class for MOM.Pred.Spec classes
#
# Revision Dates
#    29-Sep-2009 (CT) Creation (factored from TOM.Meta.M_Pred_Spec)
#    ««revision-date»»···
#--

from   _MOM                import MOM

import _MOM._Meta.M_Prop_Spec
import _MOM.Error

class M_Pred_Spec (MOM.Meta.M_Prop_Spec) :
    """Meta class for `MOM.Pred.Spec`. It gathers all (including all
       inherited) members of `Spec` which are derived from `_Condition_` and
       puts them into the class attribute `_names`.

       Setting a member to `None` in a derived `Spec` will remove the
       predicate from the `Spec`.
    """

    def _m_inconsistent_prop (cls, n, v, _names, dict) :
        return MOM.Error.Inconsistent_Predicate, \
            ( "%s: Predicate `%s = %r` of %s clashes with %s"
            ) % (dict ["__module__"], n, v, dict ["__name__"], _names [n])
    # end def _m_inconsistent_prop

# end class M_Pred_Spec

__doc__ = """
Class `MOM.Meta.M_Pred_Spec`
============================

.. moduleauthor:: Christian Tanzer <tanzer@swing.co.at>

.. autoclass:: M_Pred_Spec

"""

if __name__ != "__main__" :
    MOM.Meta._Export ("*")
### __END__ MOM.Meta.M_Pred_Spec
