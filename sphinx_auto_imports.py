# -*- coding: utf-8 -*-
# Copyright (C) 2015 Christian Tanzer All rights reserved
# tanzer@gg32.com                                      https://www.gg32.com
#
#++
# Name
#    auto_imports
#
# Purpose
#    Automatically import MOM-related modules that are needed during
#    sphinx run (import when a specific module is documented is too late!)
#
# Revision Dates
#    17-Aug-2015 (CT) Creation
#    ««revision-date»»···
#--

from _MOM                import MOM
from _GTW._OMP._Auth     import Auth
from _GTW._OMP._EVT      import EVT
from _GTW._OMP._PAP      import PAP
from _GTW._OMP._SRM      import SRM
from _GTW._OMP._SWP      import SWP

MOM._Import_All      ()
MOM.Attr._Import_All ()
Auth._Import_All     ()
EVT._Import_All      ()
PAP._Import_All      ()
SRM._Import_All      ()
SWP._Import_All      ()

### __END__ auto_imports
