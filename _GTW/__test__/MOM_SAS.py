# -*- coding: iso-8859-15 -*-
# Copyright (C) 2010-2011 Martin Glueck All rights reserved
# Langstrasse 4, A--2244 Spannberg, Austria. martin@mangari.org
# ****************************************************************************
# This module is part of the package GTW.__test__.
#
# This module is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This module is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this module. If not, see <http://www.gnu.org/licenses/>.
# ****************************************************************************
#
#++
# Name
#    GTW.__test__.MOM_SAS
#
# Purpose
#    Proxy for the MOM.DBW.SAS.__doc__ tests
#
# Revision Dates
#    19-Apr-2010 (MG) Creation
#    17-May-2010 (MG) `__test__` added
#    ««revision-date»»···
#--
"""
This is just to make sure that run_doctest considers this file as a file with
doctests
    >>> Print
"""
from _MOM._DBW._SAS.__doc__ import \
     __doc__, __test__, MOM, BMT, show, NL, sos, remove, formatted

if __name__ == "__main__" :
    import doctest
    doctest.testmod ()
### __END__ GTW.__test__.MOM_SAS
