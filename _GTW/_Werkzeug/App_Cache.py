# -*- coding: iso-8859-15 -*-
# Copyright (C) 2012-2013 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# #*** <License> ************************************************************#
# This module is part of the package GTW.Werkzeug.
#
# This module is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This module is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this module. If not, see <http://www.gnu.org/licenses/>.
# #*** </License> ***********************************************************#
#
#++
# Name
#    GTW.Werkzeug.App_Cache
#
# Purpose
#    Implement a cache for a GTW.Werkzeug application
#
# Revision Dates
#    28-Jun-2012 (CT) Creation
#    26-Jul-2012 (CT) Add and use `_stored_p`
#    26-Jul-2012 (CT) Fix typo
#    10-Aug-2012 (CT) Add `verbose`
#    ««revision-date»»···
#--

from   __future__  import absolute_import, division, print_function, unicode_literals

from   _GTW                     import GTW
from   _TFL                     import TFL

import _GTW._Werkzeug

from   _TFL.pyk                 import pyk
from   _TFL                     import sos

import _TFL._Meta.Object
import _TFL.Context

import logging

class App_Cache (TFL.Meta.Object) :
    """Implement a cache for a GTW.Werkzeug application."""

    def __init__ (self, cache_path, * cachers, ** kw) :
        self.cache_path = cache_path
        self.cachers    = set (cachers)
        self.DEBUG      = kw.pop ("DEBUG",   False)
        self.verbose    = kw.pop ("verbose", False)
        self.kw         = kw
        self._stored_p  = False
    # end def __init__

    def add (self, * cachers) :
        self.cachers.update (cachers)
    # end def add

    def load (self) :
        if not self.cachers :
            return
        kw   = self.kw
        path = self.cache_path
        try :
            with open (path, "rb") as file :
                cargo = pyk.pickle.load (file)
        except StandardError as exc :
            logging.warning \
                ( "Loading pickle dump %s failed with exception: %s"
                % (path, exc)
                )
            raise
        else :
            if self.verbose :
                logging.info ("Loaded pickle dump %s successfully" % (path, ))
            for cp in self._gen_cachers ("Unpickling", "Regenerate cache...") :
                cp.from_pickle_cargo (cargo = cargo, ** kw)
    # end def load

    def store (self) :
        if self._stored_p or not self.cachers :
            return
        cargo   = dict ()
        context = TFL.Context.time_block if self.DEBUG else TFL.Context.relaxed
        kw      = self.kw
        path    = self.cache_path
        fmt     = "*** Cache %s rebuilt in %%ss" % (path)
        with context (fmt) :
            self._stored_p = True
            for cp in self._gen_cachers ("Pickling") :
                cargo.update (cp.as_pickle_cargo (** kw))
            try :
                with open (path, "wb") as file :
                    pyk.pickle.dump (cargo, file, pyk.pickle.HIGHEST_PROTOCOL)
                if self.verbose :
                    print ("Stored pickle dump %s successfully" % path)
            except StandardError as exc :
                logging.warning \
                    ( "Storing pickle dump %s failed with exception: %s"
                    % (path, exc)
                    )
                raise
    # end def store

    def _gen_cachers (self, msg_head, msg_tail = "") :
        for cp in sorted (self.cachers, key = TFL.Getter.cache_rank) :
            try :
                yield cp
            except StandardError as exc :
                logging.warning \
                    ( "%s of %s failed with exception `%s`.\n%s"
                    % (msg_head, cp, exc, msg_tail)
                    )
                if self.DEBUG :
                    import traceback
                    traceback.print_exc ()
                raise
    # end def _gen_cachers

# end class App_Cache

if __name__ != "__main__" :
    GTW.Werkzeug._Export ("*")
### __END__ GTW.Werkzeug.App_Cache
