# -*- coding: utf-8 -*-
# Copyright (C) 2006-2010 Mag. Christian Tanzer. All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# ****************************************************************************
#
# This module is licensed under the terms of the BSD 3-Clause License
# <http://www.c-tanzer.at/license/bsd_3c.html>.
# ****************************************************************************
#
#++
# Name
#    TGL.load_config_file
#
# Purpose
#    Load config file
#
# Revision Dates
#     5-Jan-2006 (CT) Creation
#    10-Nov-2009 (CT) s/execfile/exec/ to avoid `-3` warning
#    30-Jul-2010 (CT) Moved to `TFL`
#    ««revision-date»»···
#--

from _TGL import TGL
from _TFL.load_config_file import *

if __name__ != "__main__" :
    TGL._Export ("load_config_file")
### __END__ TGL.load_config_file
