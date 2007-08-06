# -*- coding: iso-8859-1 -*-
# Copyright (C) 1998-2005 Mag. Christian Tanzer. All rights reserved
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
#    TFL.Environment
#
# Purpose
#    Provide access to program's environment in os-independent way
#
# Revision Dates
#    17-Apr-1998 (CT)  Creation
#    16-Feb-1999 (CT)  Added `script_name' and `script_path'
#    16-Feb-1999 (CT)  Added `path_of' and `path_contains'
#    17-Feb-1999 (CT)  `path_expanded' added
#    13-Apr-2000 (CT)  `frozen' added
#    14-Apr-2000 (CT)  `module_path' added
#    25-Apr-2000 (CT)  `system' added
#    26-Apr-2000 (CT)  `default_dir' and `home_dir' added
#    13-Sep-2001 (AGO) Workaround for default paths of frozen modules
#    13-May-2003 (CT)  `module_path` changed to look in `sys.modules` first
#                      (can't be bothered to tweak `imp.find_module` for
#                      modules in packages)
#    28-May-2003 (CT)  Use `sos.uname` to find `hostname`
#    25-Jun-2003 (AGO) Fixed preliminarily [4629]
#    11-Jul-2003 (MG)  `try... except` added around `uname` call
#    21-Apr-2004 (CT)  Try to get `home_dir` from `USERPROFILE`, too
#    21-Apr-2004 (MUZ) s/sys/sos/ in sys.environ.get ("USERPROFILE")
#     7-Mar-2005 (MG)  `curdir_pat` fixed
#                      (the old pattern replaces `../../` -> `...`)
#    24-Mar-2005 (CT)  Moved into package `TFL`
#    28-Jul-2005 (CT)  `mailname` added
#     8-Aug-2006 (MSF) fixed [5608]
#    23-Jul-2007 (CED) Activated absolute_import
#    06-Aug-2007 (CED) Future import removed again
#    ««revision-date»»···
#--



from   _TFL      import TFL

import _TFL.sos
import imp
import re
import sys

default_dir = TFL.sos.getcwd       ()
home_dir    = TFL.sos.environ.get  ("HOME")
if home_dir is None :
    home_dir = TFL.sos.environ.get ("USERPROFILE")
    if home_dir is None :
        home_dir = default_dir

if   TFL.sos.name == "posix"                         :
    username = TFL.sos.environ.get ("USER",         "")
    hostname = TFL.sos.environ.get ("HOSTNAME",     "")
    system   = "posix"
elif (TFL.sos.name == "nt") or (TFL.sos.name == "win32") :
    username = TFL.sos.environ.get ("USERNAME",     "")
    hostname = TFL.sos.environ.get ("COMPUTERNAME", "")
    system   = "win32"
elif TFL.sos.name == "mac"                           :
    username = "" ### ???
    hostname = "" ### ???
    system   = "mac"

if not hostname :
    try :
        hostname = TFL.sos.uname () [1]
    except :
        pass

def mailname () :
    """Returns the mailname of the system the script is running on."""
    try :
        f = open ("/etc/mailname")
    except (IOError, TFL.sos.error) :
        pass
    else :
        try :
            return f.read ().strip ()
        except (IOError, TFL.sos.error) :
            pass
# end def mailname

def script_name () :
    """Returns the name of the currently running python script."""
    return TFL.sos.path.basename (sys.argv [0])
# end def script_name

curdir_pat = re.compile (r"\./\.[^\.]")

def script_path () :
    """Returns the path of the currently running python script."""
    path = TFL.sos.path.dirname (sys.argv [0])
    path = curdir_pat.sub   (".", path) ### hack around case "./."
    if not path :
        path = TFL.sos.curdir
    return path
# end def script_path

def path_expanded (filename) :
    """Returns filename expanded by `path_of (filename)'.

       If no path is found for `filename', it is returned as is.
    """
    path = path_of (filename)
    if path :
        return TFL.sos.path.join (path, filename)
    else :
        return filename
# end def path_expanded

def path_of (filename) :
    """Returns path where `filename' resides. `path_of' looks in the
       directory of the current python-script and in the python path and
       returns the first directory containing `filename'.
    """
    sc_path = script_path ()
    if path_contains (sc_path, filename)  : return sc_path
    for path in sys.path :
        if path_contains (path, filename) : return path
    return ""
# end def path_of

def path_contains (path, filename) :
    """Returns `path' if there exists a file named `filename' there."""
    if TFL.sos.path.isfile (TFL.sos.path.join (path, filename)) :
        return path
    else :
        return ""
# end def path_contains

def frozen () :
    """Returns true if application is frozen"""
    import sys
    return hasattr (sys, "frozen")
# end def frozen

_module_pathes = {}

# AGO:2001-09-13 Workaround due to inconsistency between imp.find_module
# and Gordon McMillan's installer. The latter puts object references into
# sys.path which imp.find_module does not understand. Remove workaround
# when either one is fixed.
def module_path (module) :
    """Returns path where `module' resides"""
    # print ">>> sys.path = %s" % sys.path #AGO
    # print ">>> dir () = %s" % dir () #AGO
    if not _module_pathes.has_key (module) :
        if frozen () :
            _path = script_path ()
        elif (   module in sys.modules
             and hasattr (sys.modules [module], "__file__")
             ) :
            p     = sys.modules [module].__file__
            _path = TFL.sos.path.dirname (p) or TFL.sos.getcwd ()
        else :
            try: #AGO
                (f, p, d) = imp.find_module (module)
            except ImportError:
                # Should check here if there is a reference in sys.path to an
                # archive, and then if the module is really in this archive ...
                # But which path should then be returned?
                # Maybe the files looked for are also
                # compressed/packed/frozen.
                _path = script_path ()
            else: #AGO
                _path = TFL.sos.path.dirname (p) or TFL.sos.getcwd ()
        if _path == TFL.sos.curdir :
            _path = TFL.sos.getcwd ()
        _module_pathes [module] = _path
    return _module_pathes [module]
# end def module_path

if __name__ != "__main__" :
    TFL._Export_Module ()
### __END__ TFL.Environment
