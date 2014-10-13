# -*- coding: utf-8 -*-
# Copyright (C) 2011 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# #*** <License> ************************************************************#
# This module is part of the package GTW.AFS.
# 
# This module is licensed under the terms of the BSD 3-Clause License
# <http://www.c-tanzer.at/license/bsd_3c.html>.
# #*** </License> ***********************************************************#
#
#++
# Name
#    GTW.AFS.__init__
#
# Purpose
#    AFS Forms for MOM entities
#
# Revision Dates
#     8-Feb-2011 (CT) Creation
#    ««revision-date»»···
#--

from   _TFL.Package_Namespace import Package_Namespace
from   _GTW._AFS              import AFS

MOM = Package_Namespace ()
AFS._Export ("MOM")

del Package_Namespace

### __END__ GTW.AFS.__init__
