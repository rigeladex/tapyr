# -*- coding: utf-8 -*-
# Copyright (C) 2009-2015 Christian Tanzer All rights reserved
# tanzer@gg32.com                                      https://www.gg32.com
# ****************************************************************************
# This package is part of the package GTW.OMP.
#
# This module is licensed under the terms of the BSD 3-Clause License
# <https://www.gg32.com/license/bsd_3c.html>.
# ****************************************************************************
#
#++
# Name
#    GTW.OMP.PAP.__init__
#
# Purpose
#    Package defining a partial object model for Persons, Addresses, and
#    Phone-Numbers
#
# Revision Dates
#    30-Dec-2009 (CT) Creation
#     9-Oct-2012 (CT) Add `_desc_`
#    15-Jun-2013 (CT) Use `MOM.Derived_PNS`
#    ««revision-date»»···
#--

from   _GTW._OMP              import OMP
from   _MOM                   import MOM
import _MOM.Derived_PNS

_desc_ = __doc__ = """
Partial object model for (natural and legal) persons and their (contact)
properties.
"""

PAP = MOM.Derived_PNS (parent = MOM, pns_alias = "PAP")
OMP._Export ("PAP")

### __END__ GTW.OMP.PAP.__init__
