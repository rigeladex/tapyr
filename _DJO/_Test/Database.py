# -*- coding: iso-8859-1 -*-
# Copyright (C) 2005-2008 Martin Glück. All rights reserved
# Langstrasse 4, A--2244 Spannberg, Austria. martin@smangari.org
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
#    DJO.Test.Database
#
# Purpose
#    Test functions for preparing a database
#
# Revision Dates
#     8-Oct-2008 (MG) Creation
#    ««revision-date»»···
#--

from   _TFL              import TFL
import _TFL._Meta.Object
from    django.conf      import settings
from    django.core      import management

class Database (TFL.Meta.Object) :
    """A test database"""

    def __init__ (self, db_name = None, * fixtures, ** kw) :
        self.db_name  = db_name or settings.DATABASE_NAME
        self.synced   = kw.pop ("synced", False)
        self.kw       = kw
        self.fixtures = fixtures
    # end def __init__

    def _command ( self, command
                 , verbosity = 0, interactive = False
                 , * args, ** kw
                 ) :
        return management.call_command \
            (command, verbosity = verbosity, interactive = interactive, * args)
    # end def _command

    def setup (self, * fixtures, ** kw) :
        if not self.synced :
            self._command ("syncdb")
            self.synced = True
        if kw.pop ("flush", True) :
            self._command ("flush")
        if kw.pop ("load_db_fixtures", False) :
            self._command ("loaddata", * self.fixtures)
        self._command ("loaddata", * fixtures)
    # end def setup

    def reset (self, ** kw) :
        if kw.pop ("flush_after", False) :
            self.command ("flush")
    # end def reset

    def setup_database (self, * fixtures, ** db_kw) :
        def inner (fct) :
            def _ (* args, ** kw) :
                self.setup (* fixtures, ** db_kw)
                result = fct (* args, ** kw)
                self.reset (** db_kw)
                return result
            # end def _
            return _
        # end def inner
        return inner
    # end def setup_database

# end class Database

DB = Database ()

if __name__ != "__main__" :
    from _DJO._Test import Test
    Test._Export ("*")
### __END__ Database


