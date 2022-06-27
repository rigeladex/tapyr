# -*- coding: utf-8 -*-
# Copyright (C) 2013 Christian Tanzer All rights reserved
# tanzer@gg32.com                                      https://www.gg32.com
# #*** <License> ************************************************************#
# This module is part of the package MOM.DBW.SAW.
# 
# This module is licensed under the terms of the BSD 3-Clause License
# <https://www.gg32.com/license/bsd_3c.html>.
# #*** </License> ***********************************************************#
#
#++
# Name
#    MOM.DBW.SAW.SA
#
# Purpose
#    Wrap sqlalchemy for MOM.DBW.SAW
#
# Revision Dates
#     4-Jul-2013 (CT) Creation
#    10-Oct-2013 (CT) Add `func` as alias for `sqlalchemy.sql.func`
#    ««revision-date»»···
#--

from   _MOM                  import MOM

import _MOM._DBW._SAW

from   sqlalchemy.engine     import Engine
from   sqlalchemy            import engine
from   sqlalchemy.events     import event
from   sqlalchemy            import exc        as Exception
from   sqlalchemy.sql        import expression
from   sqlalchemy.sql        import func       as func
from   sqlalchemy            import interfaces
from   sqlalchemy            import MetaData
from   sqlalchemy            import schema
from   sqlalchemy            import sql
from   sqlalchemy            import types

try :
    from sqlalchemy.sql.operators  import Operators
except ImportError :
    from sqlalchemy.sql.expression import Operators

try :
    from sqlalchemy.sql.functions  import Function
except ImportError :
    from sqlalchemy.sql.expression import Function

if __name__ != "__main__" :
    MOM.DBW.SAW._Export_Module ()
### __END__ MOM.DBW.SAW.SA
