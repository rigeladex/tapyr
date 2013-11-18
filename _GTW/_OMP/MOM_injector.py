# -*- coding: utf-8 -*-
# Copyright (C) 2011-2013 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# #*** <License> ************************************************************#
# This module is part of the package GTW.OMP.
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
#    GTW.OMP.MOM_injector
#
# Purpose
#    Inject a class-valued  class attribute `GTW` into the essential classes
#
#    Due to `_nested_classes_to_combine`, each essential class gets their own
#    `GTW` class with proper inheritance
#
# Revision Dates
#    14-Mar-2011 (CT) Creation (factored from `_GTW._OMP.Scaffold`)
#    15-Mar-2011 (CT) `GTW.afs_id` and `.afs_spec` initialized to `None`
#    23-Mar-2011 (CT) `GTW.afs_kw` initialized to `None`
#    17-May-2013 (CT) Add `GTW.rst_mom_rbl_spec`
#    ««revision-date»»···
#--

from   _MOM import MOM

import _MOM._Meta.M_Entity, _MOM.Entity

MOM.Meta.M_Entity._nested_classes_to_combine += ("GTW", )

MOM.Entity.GTW = type \
    ( "GTW"
    , ()
    , dict
        ( afs_id             = None
        , afs_kw             = None
        , afs_spec           = None
        , rst_mom_rbl_spec   = None
        , __module__         = MOM.Entity.__module__
        )
    )
for _T in MOM.Entity._S_Extension [1:] :
    _T._m_combine_nested_class ("GTW", _T.__bases__, _T.__dict__)

### __END__ GTW.OMP.MOM_injector
