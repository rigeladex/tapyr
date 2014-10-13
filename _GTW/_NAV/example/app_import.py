# -*- coding: utf-8 -*-
# Copyright (C) 2010-2013 Martin Glueck All rights reserved
# Langstrasse 4, A--2244 Spannberg, Austria. martin@mangari.org
# ****************************************************************************
# This module is part of the package GTW.NAV.
#
# This module is licensed under the terms of the BSD 3-Clause License
# <http://www.c-tanzer.at/license/bsd_3c.html>.
# ****************************************************************************
#
#++
# Name
#    app_import
#
# Purpose
#    Import for the object model
#
# Revision Dates
#    20-Jan-2010 (MG) Creation
#    13-Jun-2013 (CT) Remove `PNS_Aliases`
#    ««revision-date»»···
#--

from   _MOM            import MOM
from   _GTW            import GTW
import _GTW._OMP._Auth.import_Auth
import _GTW._OMP._PAP. import_PAP
import _GTW._OMP._SWP.Page

from   _MOM._EMS.Hash         import Manager as EMS
from   _MOM._DBW._HPS.Manager import Manager as DBW

app_type = MOM.App_Type (u"HWO", GTW).Derived (EMS, DBW)

### __END__ app_import
