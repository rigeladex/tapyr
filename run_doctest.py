# -*- coding: utf-8 -*-
# Copyright (C) 2004-2016 Christian Tanzer. All rights reserved
# tanzer@gg32.com                                      https://www.gg32.com
# ****************************************************************************
#
# This module is licensed under the terms of the BSD 3-Clause License
# <https://www.gg32.com/license/bsd_3c.html>.
# ****************************************************************************
#
#++
# Name
#    run_doctest
#
# Purpose
#    Run doctest on all modules specified on command line
#
# Revision Dates
#    10-Oct-2016 (CT) Use `TFL.run_doctest`
#    17-Oct-2016 (CT) Use `import *`
#    ««revision-date»»···
#--

from   _TFL             import TFL
from   _TFL.run_doctest import *

if __name__ == "__main__" :
    TFL.run_doctest.Command ()
### __END__ run_doctest
