# -*- coding: utf-8 -*-
# Copyright (C) 2005 Martin Glück. All rights reserved
# Langstrasse 4, A--2244 Spannberg, Austria. office@spannberg.com
# ****************************************************************************
#
# This module is licensed under the terms of the BSD 3-Clause License
# <http://www.c-tanzer.at/license/bsd_3c.html>.
# ****************************************************************************
#
#++
# Name
#    TGL.TKT.GTK.Accel_Group
#
# Purpose
#    Wrapper for the GTK widget AccelGroup
#
# Revision Dates
#    13-May-2005 (MG) Automated creation
#    ««revision-date»»···
#--

from   _TGL._TKT._GTK         import GTK
import _TGL._TKT._GTK.Object

class Accel_Group (GTK.Object) :
    """Wrapper for the GTK widget AccelGroup"""

    GTK_Class        = GTK.gtk.AccelGroup
    __gtk_properties = \
        (
        )

# end class Accel_Group

if __name__ != "__main__" :
    GTK._Export ("Accel_Group")
### __END__ TGL.TKT.GTK.Accel_Group
