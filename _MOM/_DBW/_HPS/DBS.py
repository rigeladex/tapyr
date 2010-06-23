# -*- coding: iso-8859-1 -*-
# Copyright (C) 2010 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# ****************************************************************************
# This module is part of the package MOM.DBW.HPS.
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
#    MOM.DBW.HPS.DBS
#
# Purpose
#    Encapsulate db-specific functionality for HPS
#
# Revision Dates
#    23-Jun-2010 (CT) Creation
#    ««revision-date»»···
#--

from   _MOM                      import MOM
from   _TFL                      import TFL
from   _TFL                      import sos

import _MOM._DBW._DBS_
import _TFL.Filename

class HPS (MOM.DBW._DBS_) :
    """DB-specific functionality for HPS"""

    scheme = "hps"

    @classmethod
    def Url (cls, value, ANS) :
        result = super (HPS, cls).Url (value, ANS)
        if result.authority :
            raise ValueError ("HPS url cannot specify authority: %s" % value)
        result._value.path = TFL.Filename \
            ( result.path
            , ANS.Version.db_version.db_extension
            , absolute = True
            ).name
        result.create = not sos.path.exists (result.path)
        return result
    # end def Url

# end class HPS

if __name__ != "__main__" :
    MOM.DBW.HPS._Export ("*")
### __END__ MOM.DBW.HPSDBS
