# -*- coding: utf-8 -*-
# Copyright (C) 2009-2010 Christian Tanzer. All rights reserved
# tanzer@gg32.com                                      https://www.gg32.com
# ****************************************************************************
# This package is part of the package _MOM.
#
# This module is licensed under the terms of the BSD 3-Clause License
# <https://www.gg32.com/license/bsd_3c.html>.
# ****************************************************************************
#
#++
# Name
#    MOM.EMS.__init__
#
# Purpose
#    Package for entity manager strategies for MOM
#
# Revision Dates
#    14-Oct-2009 (CT) Creation
#    ««revision-date»»···
#--

from   _MOM                   import MOM
from   _TFL.Package_Namespace import Package_Namespace

EMS = Package_Namespace ()
MOM._Export ("EMS")

del Package_Namespace

### __END__ MOM.EMS.__init__
