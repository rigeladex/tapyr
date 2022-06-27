# -*- coding: utf-8 -*-
# Copyright (C) 2010 Christian Tanzer All rights reserved
# tanzer@gg32.com                                      https://www.gg32.com
# ****************************************************************************
# This module is part of the package GTW.OMP.SRM.
#
# This module is licensed under the terms of the BSD 3-Clause License
# <https://www.gg32.com/license/bsd_3c.html>.
# ****************************************************************************
#
#++
# Name
#    GTW.OMP.SRM.__babel__
#
# Purpose
#    This file is the entry point for the Babel translation extraction
#    process.
#
# Revision Dates
#    10-May-2010 (CT) Creation
#    ««revision-date»»···
#--

from   _MOM.import_MOM import *
import _MOM.Babel
import _GTW._OMP._SRM.import_SRM

def main (encoding, config, method) :
    from   _MOM._EMS.Hash         import Manager as EMS
    from   _MOM._DBW._HPS.Manager import Manager as DBW
    from   _GTW                   import GTW

    return MOM.Babel.Add_Translations \
        ( encoding, config, method
        , MOM.App_Type ("SRM", GTW).Derived (EMS, DBW)
        )
# end def main

### __END__ GTW.OMP.SRM.__babel__
