# -*- coding: utf-8 -*-
# Copyright (C) 2012 Christian Tanzer All rights reserved
# tanzer@gg32.com                                      https://www.gg32.com
# #*** <License> ************************************************************#
# This module is part of the package GTW.OMP.PAP.
# 
# This module is licensed under the terms of the BSD 3-Clause License
# <https://www.gg32.com/license/bsd_3c.html>.
# #*** </License> ***********************************************************#
#
#++
# Name
#    GTW.OMP.PAP.Url
#
# Purpose
#    Model a URL
#
# Revision Dates
#    11-Oct-2012 (CT) Creation
#    ««revision-date»»···
#--

from   _MOM.import_MOM        import *
from   _GTW                   import GTW
from   _GTW._OMP._PAP         import PAP
from   _TFL.I18N              import _

import _GTW._OMP._PAP.Property

_Ancestor_Essence = PAP.Property

class _PAP_Url_ (_Ancestor_Essence) :
    """Uniform resource locator, aka URL"""

    _real_name = "Url"

    class _Attributes (_Ancestor_Essence._Attributes) :

        _Ancestor = _Ancestor_Essence._Attributes

        class value (A_Url_X) :
            """URL value referrring to a specific resource."""

            kind               = Attr.Primary
            example            = "http://xkcd.com/327/"

        # end class value

    # end class _Attributes

Url = _PAP_Url_ # end class

if __name__ != "__main__" :
    GTW.OMP.PAP._Export ("*")
### __END__ GTW.OMP.PAP.Url
