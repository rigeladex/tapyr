# -*- coding: utf-8 -*-
# Copyright (C) 2015 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# #*** <License> ************************************************************#
# This module is part of the package MOM.
#
# This module is licensed under the terms of the BSD 3-Clause License
# <http://www.c-tanzer.at/license/bsd_3c.html>.
# #*** </License> ***********************************************************#
#
#++
# Name
#    MOM.ui_display
#
# Purpose
#    Generic function returning a string usable for display in user interface
#
# Revision Dates
#     6-Feb-2015 (CT) Creation
#    ««revision-date»»···
#--

from   __future__ import division, print_function
from   __future__ import absolute_import, unicode_literals

from   _MOM                       import MOM

import _MOM.Entity

from   _TFL.ui_display            import *

@ui_display.add_type (MOM.Entity)
def _ui_display_entity (obj) :
    return obj.ui_display
# end def _ui_display_entity

if __name__ != "__main__" :
    MOM._Export ("ui_display")
### __END__ MOM.ui_display
