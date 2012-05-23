# -*- coding: iso-8859-15 -*-
# Copyright (C) 2012 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# #*** <License> ************************************************************#
# This module is part of the package GTW.Werkzeug.
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
#    GTW.Werkzeug.deploy
#
# Purpose
#    Provide an extendable Command for the deployment of applications based
#    on GTW.Werkzeug
#
# Revision Dates
#    23-May-2012 (CT) Creation
#    ««revision-date»»···
#--

from   __future__  import absolute_import, division, print_function #, unicode_literals

from   _GTW                   import GTW
import _GTW.deploy

class GT2W_Command (GTW.deploy.Command) :
    """Manage deployment applications based on GTW.Werkzeug."""

    _rn_prefix              = "GT2W"

    class _GT2W_Babel_ (GTW.deploy.Command._Babel_) :

        _rn_prefix          = "_GT2W"
        _package_dirs       = [ "_JNJ", "_ReST"]

    _Babel_ = _GT2W_Babel_ # end class

Command = GT2W_Command # end class

if __name__ != "__main__" :
    GTW.Werkzeug._Export_Module ()
### __END__ GTW.Werkzeug.deploy
