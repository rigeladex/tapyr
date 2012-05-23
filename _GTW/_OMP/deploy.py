# -*- coding: iso-8859-15 -*-
# Copyright (C) 2012 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# #*** <License> ************************************************************#
# This module is part of the package GTW.OMP.
#
# This module is free software; you can redistribute it and/or
# modify it under the terms of the GNU Library General Public
# License as published by the Free Software Foundation; either
# version 2 of the License, or (at your option) any later version.
#
# This module is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# Library General Public License for more details.
#
# You should have received a copy of the GNU Library General Public License
# along with this module; if not, see <http://www.gnu.org/licenses/>.
# #*** </License> ***********************************************************#
#
#++
# Name
#    GTW.OMP.deploy
#
# Purpose
#    Provide an extendable Command for the deployment of applications based
#    on GTW.OMP
#
# Revision Dates
#    23-May-2012 (CT) Creation
#    ««revision-date»»···
#--

from   __future__  import absolute_import, division, print_function#, unicode_literals

from   _GTW                   import GTW
from   _MOM                   import MOM
from   _TFL                   import TFL

import _GTW.deploy

class GTW_OMP_Command (GTW.deploy.Command) :
    """Manage deployment applications based on GTW.OMP."""

    _rn_prefix              = "GTW_OMP_"

    class _GTW_OMP_Babel_ (GTW.deploy.Command._Babel_) :

        _rn_prefix              = "_GTW_OMP"
        _package_dirs           = \
            [ "_MOM"
            , "_GTW"
            , "_GTW/_OMP/_Auth"
            , "_GTW/_OMP/_PAP"
            , "_GTW/_OMP/_SWP"
            , "_GTW/_OMP/_SRM"
            , "_GTW/_OMP/_EVT"
            ]

    _Babel_ = _GTW_OMP_Babel_ # end class

Command = GTW_OMP_Command # end class

if __name__ != "__main__" :
    GTW.OMP._Export_Module ()
### __END__ GTW.OMP.deploy
