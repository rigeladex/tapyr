# -*- coding: utf-8 -*-
# Copyright (C) 2005 Mag. Christian Tanzer. All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# ****************************************************************************
#
# This module is licensed under the terms of the BSD 3-Clause License
# <http://www.c-tanzer.at/license/bsd_3c.html>.
# ****************************************************************************
#
#++
# Name
#    PMA
#
# Purpose
#    Main program for Pythonic Mail Agent
#
# Revision Dates
#    20-May-2005 (CT) Creation
#    29-Jul-2005 (CT) Call to `load_user_config` added
#    ««revision-date»»···
#--

from   _PMA import PMA
import _PMA._UI.Starter

def main () :
    PMA.load_user_config ()
    cmd = PMA.UI.Starter.command_spec ()
    PMA.UI.Starter (PMA, cmd)
# end def main

if __name__ == "__main__" :
    main ()
### __END__ PMA
