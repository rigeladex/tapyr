# -*- coding: iso-8859-1 -*-
# Copyright (C) 2009 Martin Glueck All rights reserved
# Langstrasse 4, A--2244 Spannberg, Austria. martin@mangari.org
# ****************************************************************************
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Library General Public
# License as published by the Free Software Foundation; either
# version 2 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Library General Public License for more details.
#
# You should have received a copy of the GNU Library General Public
# License along with this library; if not, write to the Free
# Software Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
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

from _MOM.__doc__ import dt_form, MOM, BMT, show
import re

filter_dbw_pat = re.compile \
    (  "\#\#\#\sDBW-specific\sstart.+?\#\#\#\sDBW-specific\sfinish"
    , re.DOTALL | re.X | re.MULTILINE
    )

doc__ = ( filter_dbw_pat.sub ("", dt_form)
        % dict ( import_DBW = "from _MOM._DBW._SA.Session import Session"
               , import_EMS = "from _MOM._EMS.SA          import Manager"
               )
        ).replace ("__Hash", "__SA").replace ("__XXX", "__SA")
__doc__ = doc__.replace \
    ( "MOM.Scope (apt)"
    , "MOM.Scope (apt)\n    >>> DBW.metadata.create_all   (DBW.engine)"
    )
### __END__ MOM.DBW.SA.__doc__
