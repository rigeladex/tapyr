# -*- coding: iso-8859-1 -*-
# Copyright (C) 2000-2005 Mag. Christian Tanzer. All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# ****************************************************************************
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
# ****************************************************************************
#
#++
# Name
#    TFL.App_State
#
# Purpose
#    Encapsulate the persistent state of an interactive application
#
# Revision Dates
#    25-Apr-2000 (CT)  Creation
#     3-May-2000 (CT)  Import from `WindowsRegistry' moved into `try' block
#    11-May-2000 (RM)  Printing of traceback removed in load
#    12-May-2000 (CT)  Printing of traceback reintroduced in load (avoid
#                      syntax error)
#    13-Jul-2000 (CT)  `win32api.error' exception handlers added
#     8-Aug-2000 (CT)  Pickle before opening file
#    16-Aug-2000 (CT)  `if state' added to win32 version of `load'
#    22-Feb-2001 (CT)  Use `raise' instead of `raise exc' for re-raise
#    14-Sep-2001 (CT)  `__setattr__` added
#     6-Nov-2001 (CT)  Import of `traceback` moved from exception handler to
#                      global scope
#     5-Dec-2001 (MG)  Import of `WindowsRegistry` moved out of functions (not
#                      allowed in future versions of python)
#    10-Mar-2003 (AGO) `__repr__` added
#    20-Mar-2003 (CT)  Derive from `TFL.Meta.Object`
#    31-Jan-2005 (CT)  Calls to `pickle.dumps` changed to avoid
#                      DeprecationWarning
#                          The 'bin' argument to Pickler() is deprecated
#    20-May-2005 (CT)  Moved to TFL
#    23-Jul-2007 (CED) Activated absolute_import
#    06-Aug-2007 (CED) Future import removed again
#    ««revision-date»»···
#--



from   _TFL              import TFL
import _TFL._Meta.Object
import _TFL.Environment
from   _TFL              import sos

import cPickle as pickle
import sys
import traceback

try :
    from WindowsRegistry import *
except ImportError :
    pass

class App_State (TFL.Meta.Object) :
    """Encapsulate the persistent state of an interactive application."""

    product_name = None ### redefine in descendents
    bin          = False

    def __init__ (self, ** kw) :
        assert (self.product_name)
        self.__dict__ ["state"] = kw.copy ()
    # end def __init__

    def __getattr__ (self, name) :
        try :
            return self.state [name]
        except KeyError :
            raise AttributeError, name
    # end def __getattr__

    def __setattr__ (self, name, value) :
        if name in self.state :
            self.state [name] = value
        else :
            raise AttributeError, name
    # end def __setattr__

    def __repr__ (self) :
        return "App_State %s" % self.product_name
    # end def __repr__

    def add (self, ** kw) :
        state = kw.copy ()
        state.update (self.state)
        self.__dict__ ["state"] = state
    # end def add

    if TFL.Environment.system == "win32" :
        def foldername (self) :
            return r"Software\%s" % self.product_name
        # end def foldername

        def load (self) :
            """Load persistent application state from registry"""
            try :
                state = RegistryValue \
                    ( r"%s\%s" % (self.foldername (), "state")
                    , root = win32con.HKEY_CURRENT_USER
                    )
                if state.value :
                    state = pickle.loads  (state.value)
                    self.state.update     (state)
            except (SystemExit, KeyboardInterrupt) :
                raise
            except win32api.error :
                pass
            except :
                traceback.print_exc ()
        # end def load

        def dump (self) :
            """Dump persistent application state to registry"""
            try :
                reg_entry = RegistryFolder \
                    ( r"%s" % self.foldername ()
                    , root = win32con.HKEY_CURRENT_USER
                    )
                state     = pickle.dumps   ( self.state, self.bin)
                reg_entry.write            ( "state", state)
            except (SystemExit, KeyboardInterrupt) :
                raise
            except win32api.error, exc :
                print "Could not write application state to Windows registry"
                print exc
            except :
                traceback.print_exc ()
        # end def dump
    else :
        def filename (self) :
            return sos.path.join \
                (TFL.Environment.home_dir, ".%s.state" % (self.product_name, ))
        # end def filename

        def load (self) :
            """Load persistent application state from rc file"""
            try :
                file = open (self.filename (), "rb")
                try     :
                    state = pickle.load  (file)
                    self.state.update    (state)
                finally :
                    file.close           ()
            except (SystemExit, KeyboardInterrupt) :
                raise
            except :
                pass
        # end def load

        def dump (self) :
            """Dump persistent application state to rc file"""
            try :
                state = pickle.dumps (self.state, self.bin)
                file  = open         (self.filename (), "wb")
                try :
                    file.write (state)
                finally :
                    file.close ()
            except (SystemExit, KeyboardInterrupt) :
                raise
            except :
                traceback.print_exc ()
        # end def dump
    # end if TFL.Environment.system == "win32"

# end class App_State

if __name__ != "__main__" :
    TFL._Export ("*")
### __END__ TFL.App_State
