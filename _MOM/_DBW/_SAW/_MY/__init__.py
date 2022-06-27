# -*- coding: utf-8 -*-
# Copyright (C) 2013 Christian Tanzer All rights reserved
# tanzer@gg32.com                                      https://www.gg32.com
# #*** <License> ************************************************************#
# This module is part of the package MOM.DBW.SAW.MY.
# 
# This module is licensed under the terms of the BSD 3-Clause License
# <https://www.gg32.com/license/bsd_3c.html>.
# #*** </License> ***********************************************************#
#
#++
# Name
#    MOM.DBW.SAW.MY.__init__
#
# Purpose
#    Database wrapper for mySQL accessed by sqlalchemy wrapped by SAW
#
# Revision Dates
#    24-Jun-2013 (CT) Creation
#    ««revision-date»»···
#--

from _MOM._DBW._SAW import SAW
from   _TFL.Package_Namespace import Derived_Package_Namespace

MY = Derived_Package_Namespace (parent = SAW)
SAW._Export ("MY")

del Derived_Package_Namespace

### __END__ .MOM.DBW.SAW.MY__init__
