# -*- coding: iso-8859-1 -*-
# Copyright (C) 2009 Martin Glueck All rights reserved
# Langstrasse 4, A--2244 Spannberg, Austria. martin@mangari.org
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
#    MOM.DBW.SA.__doc__
#
# Purpose
#    Test for MOM meta object model using SQLAlchemy as database backend
#
# Revision Dates
#    26-Nov-2009 (MG) Creation
#    ««revision-date»»···
#--

from _MOM.__doc__ import dt_form, MOM, BMT, show, NL, sos
import re

filter_dbw_pat = re.compile \
    (  "\#\#\#\sDBW-specific\sstart.+?\#\#\#\sDBW-specific\sfinish"
    , re.DOTALL | re.X | re.MULTILINE
    )

doc__ = ( filter_dbw_pat.sub ("", dt_form)
        % dict ( import_DBW = "from _MOM._DBW._SA.Manager import Manager"
               , import_EMS = "from _MOM._EMS.SA          import Manager"
               , db_path    = "'test.sqlite'"
               , db_uri     = "'sqlite:///test.sqlite'"
               )
        ).replace ("__Hash", "__SA").replace ("__HPS", "__SA")
__doc__ = doc__

### __END__ MOM.DBW.SA.__doc__
