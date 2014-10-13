# -*- coding: utf-8 -*-
# Copyright (C) 2010-2013 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# ****************************************************************************
# This module is part of the package GTW.OMP.Auth.
#
# This module is licensed under the terms of the BSD 3-Clause License
# <http://www.c-tanzer.at/license/bsd_3c.html>.
# ****************************************************************************
#
#++
# Name
#    GTW.OMP.Auth.Nav
#
# Purpose
#    Provide configuration for GTW.NAV.E_Type.Admin entries
#
# Revision Dates
#    26-Feb-2010 (CT) Creation
#    30-Apr-2010 (MG) Adapted to new form's
#     2-May-2010 (MG) Simplified
#     6-May-2010 (MG) Switch to render mode rendering
#    18-Nov-2011 (CT) Import `unicode_literals` from `__future__`
#    24-Jan-2012 (CT) Remove `Form_args`, `*_completer`,
#                     i.e., stuff related to non-AFS forms
#    22-May-2012 (CT) Fix typo (`Account_P = dict`, not `Account = dict`)
#    26-Jul-2012 (CT) Import `_GTW._RST.Permission`, not `_GTW._NAV.Permission`
#    16-Jan-2013 (CT) Add `Certificate`
#    ««revision-date»»···
#--

from   __future__            import unicode_literals

from   _TFL.I18N                import _
from   _GTW                     import GTW

from   _GTW._RST.Permission     import Is_Superuser

class Admin (object) :
    """Provide configuration for GTW.NAV.E_Type.Admin entries"""

    Account          = dict \
        ( ETM        = "GTW.OMP.Auth.Account"
        , permission = Is_Superuser ()
        )

    Certificate      = dict \
        ( ETM        = "GTW.OMP.Auth.Certificate"
        , permission = Is_Superuser ()
        )

    Group            = dict \
        ( ETM        = "GTW.OMP.Auth.Group"
        , permission = Is_Superuser ()
        )

    Account_in_Group = dict \
        ( ETM        = "GTW.OMP.Auth.Account_in_Group"
        , permission = Is_Superuser ()
        )

# end class Admin

if __name__ != "__main__" :
    GTW.OMP.Auth._Export_Module ()
### __END__ GTW.OMP.Auth.Nav
