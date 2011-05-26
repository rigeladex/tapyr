# -*- coding: iso-8859-15 -*-
# Copyright (C) 2004-2005 Mag. Christian Tanzer. All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# ****************************************************************************
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Library General Public
# License as published by the Free Software Foundation; either
# version 2 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Library General Public License for more details.
#
# You should have received a copy of the GNU Library General Public
# License along with this library; if not, write to the Free
# Software Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
# ****************************************************************************
#
#++
# Name
#    TFL._test_import_module
#
# Purpose
#    Test if `import_module` works correctly
#
# Revision Dates
#    17-Jun-2004 (CT) Creation
#    23-Jul-2007 (CED) Activated absolute_import
#    06-Aug-2007 (CED) Future import removed again
#    ««revision-date»»···
#--



"""
This module tests _TFL.import_module in two ways. The doctest tests the
normal use of the module and can be triggered by running this module through
/swing/python/run_doctest.py as in

    python /swing/system/python/run_doctest.py \
        lib/python/_TFL/_test_import_module.py -p lib/python/_TFL

The other way tests the use of `import_module` for importing a module while
it is still being imported. This can be tested by importing this module into
a running python interpreter as in

    import _TFL._test_import_module

>>> import_module ("_TFL.import_module").__name__
'_TFL.import_module'
>>> import_module ("os").__name__
'os'
"""

from _TFL.import_module import *

print "Importing ", import_module ("_TFL._test_import_module"), "works"
try :
    import_module_brittle ("_TFL._test_import_module")
except ImportError, exc :
    print ("Importing _TFL._test_import_module with "
           "import_module_brittle fails as expected: \n    "
          ), exc
### __END__ TFL._test_import_module
