# -*- coding: iso-8859-1 -*-
# Copyright (C) 2010 Martin Glueck All rights reserved
# Langstrasse 4, A--2244 Spannberg. martin@mangari.org
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
#    GTW.__test__.db_version_hash
#
# Purpose
#    Test for the database version hash check for the SAS backend
#
# Revision Dates
#    15-Jul-2010 (MG) Creation
#    ««revision-date»»···
#--
"""
    >>> scope    = Scope ("sqlite:///test.sql", create = True)
    Creating new scope MOMT__SAS__SAS test.sql
    >>> apt, url = scope.app_type, scope.db_url
    >>> dbv      = scope.ems.db_meta_data.dbv_hash
    >>> guid     = scope.guid
    >>> scope.destroy ()

Now, let's try to load this scope again (which should work since we have the
same database version):
    >>> scope    = Scope ("sqlite:///test.sql", create = False)
    Loading scope MOMT__SAS__SAS sqlite:///test.sql
    >>> scope.guid                      == guid
    True
    >>> scope.ems.db_meta_data.dbv_hash == dbv
    True
    >>> scope.destroy ()

Now let's simulate a change of teh database version hash:
    >>> apt.db_version_hash = "<a version hash which should never happen>"
    >>> scope    = Scope ("sqlite:///test.sql", create = False)
    Traceback (most recent call last):
       ...
    Incompatible_DB_Version: Cannot load database because of a database version hash missmatch:
      Tool  database version hash: <a version hash which should never happen>
      Scope database version hash: OeDh-_NaZcGLVfTpoLKCa9aWaV-uVIC39jGXcA

Cleanup:
    >>> apt.delete_database (url)
"""

from _GTW.__test__.model import *

### __END__ GTW.__test__.db_version_hash
