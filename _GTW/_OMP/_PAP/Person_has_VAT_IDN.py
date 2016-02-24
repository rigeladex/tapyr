# -*- coding: utf-8 -*-
# Copyright (C) 2016 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# #*** <License> ************************************************************#
# This module is part of the package GTW.OMP.PAP.
#
# This module is licensed under the terms of the BSD 3-Clause License
# <http://www.c-tanzer.at/license/bsd_3c.html>.
# #*** </License> ***********************************************************#
#
#++
# Name
#    GTW.OMP.PAP.Person_has_VAT_IDN
#
# Purpose
#    Link a person to a VAT identification number
#
# Revision Dates
#    24-Feb-2016 (CT) Creation
#    ««revision-date»»···
#--

from   __future__  import absolute_import
from   __future__  import division
from   __future__  import print_function
from   __future__  import unicode_literals

from   _MOM.import_MOM             import *

from   _GTW._OMP._PAP.Attr_Type    import *

from   _GTW                        import GTW
from   _GTW._OMP._PAP              import PAP
from   _TFL.I18N                   import _

from   _GTW._OMP._PAP.VAT_IDN      import A_VAT_IDN

import _GTW._OMP._PAP.Subject_has_VAT_IDN

_Ancestor_Essence = PAP.Subject_has_VAT_IDN

class Person_has_VAT_IDN (_Ancestor_Essence) :
    """Link a person to a VAT identification number"""

    class _Attributes (_Ancestor_Essence._Attributes) :

        _Ancestor = _Ancestor_Essence._Attributes

        ### Primary attributes

        class left (_Ancestor.left) :
            """Person that has a VAT identification number"""

            role_type          = PAP.Person

        # end class left

        class vin (_Ancestor.vin) :
            """VAT identification number of the Person"""

        # end class vin

    # end class _Attributes

# end class Person_has_VAT_IDN

if __name__ != "__main__" :
    GTW.OMP.PAP._Export ("*")
### __END__ GTW.OMP.PAP.Person_has_VAT_IDN
