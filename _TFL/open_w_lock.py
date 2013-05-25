# -*- coding: iso-8859-15 -*-
# Copyright (C) 2008-2013 Mag. Christian Tanzer. All rights reserved
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
#    TFL.open_w_lock
#
# Purpose
#    Provide a open_w_lock context manager that opens a file after
#    successfully locking it
#
# Revision Dates
#     3-Apr-2008 (CT) Creation (based on code in `TFL.Sync_File`)
#    ««revision-date»»···
#--

"""Provide locking via a lock file.

   >>> name = "/tmp/foo.bar"
   >>> show = "ls -1 %s*" % name
   >>> x=sos.system ("rm -f %s" % name)
   >>>
   >>> with lock_file (name) :
   ...     print (sos.popen (show, "r").read (), end = "")
   ...
   /tmp/foo.bar.lock
   >>> with open_w_lock (name, "w") as file :
   ...     print (sos.popen (show, "r").read (),)
   ...     try :
   ...         with lock_file (name) :
   ...             print (sos.popen (show, "r").read (), end = "")
   ...     except Sync_Conflict :
   ...         print ("Got Sync_Conflict:", name)
   ...
   /tmp/foo.bar
   /tmp/foo.bar.lock
   Got Sync_Conflict: /tmp/foo.bar
   >>> x=sos.system ("rm -f %s" % name)

"""

from   __future__          import print_function

from   __future__          import with_statement

from   _TFL                import TFL

from   _TFL.Error          import Sync_Conflict
from   _TFL.Filename       import Filename
from   _TFL                import sos
import _TFL.Decorator

import errno

@TFL.Contextmanager
def lock_file (file_name) :
    """Context manager providing a lock file."""
    ln = Filename (file_name + ".lock", absolute = 1)
    try :
        ### Don't try to open a lock file in a read-only directory (don't
        ### need a lock there anyway!)
        can_lock = sos.access (ln.directory, sos.W_OK)
        if can_lock :
            lf = sos.open (ln.name, sos.O_CREAT | sos.O_EXCL)
    except sos.error as exc :
        if exc.args [0] != errno.EEXIST :
            raise
        raise Sync_Conflict (file_name)
    else :
        try :
            yield None
        finally :
            if can_lock :
                try :
                    sos.close  (lf)
                finally :
                    sos.remove (ln.name)
# end def lock_file

@TFL.Contextmanager
def open_w_lock (file_name, mode = "r", bufsize = -1) :
    """Context manager that opens `file_name` after successfully locking it.
    """
    with lock_file (file_name) :
        with open (file_name, mode, bufsize) as file :
             yield file
# end def open_w_lock

if __name__ != "__main__" :
    TFL._Export ("*")
### __END__ TFL.open_w_lock
