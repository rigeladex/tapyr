# -*- coding: utf-8 -*-
# Copyright (C) 2010-2014 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# ****************************************************************************
# This module is part of the package GTW.OMP.PAP.
#
# This module is licensed under the terms of the BSD 3-Clause License
# <http://www.c-tanzer.at/license/bsd_3c.html>.
# ****************************************************************************
#
#++
# Name
#    GTW.OMP.PAP.Attr_Type
#
# Purpose
#    Define attribute types for package GTW.OMP.PAP
#
# Revision Dates
#     4-Jun-2010 (CT) Creation
#    18-Nov-2011 (CT) Import `unicode_literals` from `__future__`
#    14-May-2012 (CT) Add `A_Sex.P_Type`
#    ««revision-date»»···
#--

from   __future__            import unicode_literals

from   _GTW                     import GTW
from   _MOM.import_MOM          import *
from   _MOM.import_MOM          import _A_Named_Object_

import _GTW._OMP._PAP

from   _TFL.I18N                import _, _T, _Tn
from   _TFL.pyk                 import pyk

class A_Sex (_A_Named_Object_) :
    """Sex of a person."""

    example   = u"F"
    typ       = "Sex"
    P_Type    = pyk.text_type
    Table     = \
        { u"F"  : _(u"Female")
        , u"M"  : _(u"Male")
        }

# end class A_Sex

if __name__ != "__main__" :
    GTW.OMP.PAP._Export ("*")
### __END__ GTW.OMP.PAP.Attr_Type
