# -*- coding: utf-8 -*-
# Copyright (C) 2009-2014 Mag. Christian Tanzer All rights reserved
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
#    GTW.OMP.PAP.Phone
#
# Purpose
#    Model a phone number
#
# Revision Dates
#    30-Dec-2009 (CT) Creation
#    14-Jan-2010 (CT) `ui_name` added to some attributes
#     3-Feb-2010 (MG) `extension`  removed
#    28-Feb-2010 (CT) Use `A_Numeric_String` instead of `A_Int` and
#                     `A_Decimal` for `country_code`, `area_code`, and `number`
#     7-Sep-2011 (CT) `completer` specifications for `country_code`,
#                     `area_code`, and `number` added
#    18-Nov-2011 (CT) Import `unicode_literals` from `__future__`
#     7-Aug-2012 (CT) Add `example`
#    12-Sep-2012 (CT) Derive from `Property`
#     7-Mar-2014 (CT) Add `ui_rank` in reverse order of `rank`
#                     (to improve completion)
#    24-Sep-2014 (CT) Add `polisher` to `country_code`, `area_code`, `number`
#    ««revision-date»»···
#--

from   __future__            import unicode_literals

from   _MOM.import_MOM        import *
from   _GTW                   import GTW
from   _GTW._OMP._PAP         import PAP

import _GTW._OMP._PAP.Property

_Ancestor_Essence = PAP.Property

class _PAP_Phone_ (_Ancestor_Essence) :
    """Model a phone number"""

    _real_name     = "Phone"

    ui_display_sep = "/"

    class _Attributes (_Ancestor_Essence._Attributes) :

        class country_code (A_Numeric_String) :
            """International country code of phone number (without prefix)"""

            kind           = Attr.Primary
            max_length     = 3
            check          = ("value != '0'", )
            example        = "43"
            rank           = 1
            ui_rank        = -1

            completer      = Attr.Completer_Spec  (1)
            polisher       = Attr.Polisher.country_code_clean

        # end class country_code

        class area_code (A_Numeric_String) :
            """National area code of phone number (without prefix)"""

            kind           = Attr.Primary
            max_length     = 5
            check          = ("value != '0'", )
            example        = "1"
            rank           = 2
            ui_rank        = -2

            completer      = Attr.Completer_Spec  \
                (1, Attr.Selector.Name ("country_code"))
            polisher       = Attr.Polisher.area_code_clean

        # end class area_code

        class number (A_Numeric_String) :
            """Phone number proper (without country code, area code, extension)"""

            kind           = Attr.Primary
            max_length     = 14
            check          = ("value != '0'", )
            example        = "234567"
            rank           = 3
            ui_rank        = -3

            completer      = Attr.Completer_Spec  (2, Attr.Selector.primary)
            polisher       = Attr.Polisher.phone_number_split

        # end class number

    # end class _Attributes

Phone = _PAP_Phone_ # end class

if __name__ != "__main__" :
    GTW.OMP.PAP._Export ("*")
### __END__ GTW.OMP.PAP.Phone
