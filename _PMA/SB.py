# -*- coding: utf-8 -*-
# Copyright (C) 2005-2010 Christian Tanzer. All rights reserved
# tanzer@gg32.com                                      https://www.gg32.com
# ****************************************************************************
#
# This module is licensed under the terms of the BSD 3-Clause License
# <https://www.gg32.com/license/bsd_3c.html>.
# ****************************************************************************
#
#++
# Name
#    PMA.SB
#
# Purpose
#    Interface to spambayes
#
# Revision Dates
#    22-May-2005 (CT) Creation
#    14-Apr-2006 (CT) Use `Decorator` to define decorators
#    14-Apr-2010 (CT) Import of `spambayes` modules moved into `try`-clause
#                     (to avoid gentoo-breakage `ImportError: No module named lockfile`)
#    ««revision-date»»···
#--

from   _PMA                    import PMA
from   _TFL                    import TFL
from   _TFL.Decorator          import Decorator

import _TFL._Meta.Object

try :
    import spambayes           as     sb
    import spambayes.hammie
    import spambayes.Options
    import spambayes.storage
except ImportError :
    SB = None
else :
    import atexit

    class _SB_ (TFL.Meta.Object) :
        """Interface to spambayes"""

        def __init__ (self) :
            self.dbname, self.usedb = sb.storage.database_type ([])
            self.hammie = None
            self.mode   = None
            atexit.register (self._close)
        # end def __init__

        def create_new_db (self) :
            self._open ("n")
            self._save ()
        # end def create_new_db

        def filter (self, msg) :
            self._open ("r")
            if isinstance (msg, PMA.Message) :
                msg = msg.email.as_string ()
            return self.hammie.filter (msg)
        # end def filter

        @Decorator
        def _trainer (method) :
            def wrapper (self, msg) :
                self._open ("c")
                if isinstance (msg, PMA.Message) :
                    msg = msg.email.as_string ()
                method     (self, msg)
                self._save ()
            return wrapper
        # end def _trainer

        @_trainer
        def train_ham (self, msg) :
            """Train classifier with ham `msg`"""
            self.hammie.train_ham (msg)
        # end def train_ham

        @_trainer
        def train_spam (self, msg) :
            """Train classifier with spam `msg`"""
            self.hammie.train_spam (msg)
        # end def train_spam

        @_trainer
        def untrain_ham (self, msg) :
            """Un-Train classifier with ham `msg`"""
            self.hammie.untrain_ham (msg)
        # end def untrain_ham

        @_trainer
        def untrain_spam (self, msg) :
            """Un-Train classifier with spam `msg`"""
            self.hammie.untrain_spam (msg)
        # end def untrain_spam

        def _close (self) :
            if self.hammie is not None and self.mode != "r" :
                self._save ()
            self.hammie = None
        # end def _close

        def _open (self, mode = "c") :
            if self.hammie is None or self.mode != mode :
                self.mode   = mode
                self.hammie = sb.hammie.open (self.dbname, self.usedb, mode)
        # end def _open

        def _save (self) :
            self.hammie.store ()
        # end def _save

    # end class _SB_

    SB = _SB_ ()

if __name__ != "__main__" :
    PMA._Export ("SB")
### __END__ PMA.SB
