# -*- coding: utf-8 -*-
# Copyright (C) 2005-2009 Martin Glück. All rights reserved
# Langstrasse 4, A--2244 Spannberg, Austria. martin@smangari.org
# ****************************************************************************
#
# This module is licensed under the terms of the BSD 3-Clause License
# <http://www.c-tanzer.at/license/bsd_3c.html>.
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
